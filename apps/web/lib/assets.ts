import { embedOne, toVector } from '@sfw/ai';
import type { AssetFilter } from '@sfw/shared';
import { presignGet, type Bucket } from '@sfw/storage';
import { db } from './db';

export type AssetRow = {
  id: string;
  type: string;
  filename: string;
  bucket: Bucket;
  r2_key: string;
  thumb_key: string | null;
  proxy_key: string | null;
  width: number | null;
  height: number | null;
  duration_s: number | null;
  clip_start_s: number | null;
  clip_end_s: number | null;
  status: string;
  quality: number | null;
  hero_candidate: boolean;
  description: string | null;
  notes: string | null;
  drive_link: string | null;
  original_path: string | null;
  creator: string | null;
  credit_line: string | null;
  taken_at: string | null;
  camera: string | null;
  release_status: string;
  created_at: string;
  workshop: string | null;
  tags: {
    name: string;
    facet: string;
    source: string;
    confirmed: boolean;
    confidence: number | null;
  }[];
  people: { name: string; confirmed: boolean }[];
  used_in: number;
};

export type AssetWithUrls = AssetRow & { thumbUrl: string | null };

export type LibraryQuery = AssetFilter & {
  /** Meaning search: "steaming compost at sunrise". */
  meaning?: string;
  /** Find assets like this one. */
  similarTo?: string;
  workshop?: string;
  releaseStatus?: string[];
  minQuality?: number;
  limit?: number;
  offset?: number;
};

export type LibraryResult = {
  assets: AssetWithUrls[];
  total: number;
  facets: { facet: string; name: string; count: number }[];
};

/**
 * The library query. One function, because every screen is the same query with
 * different filters: a smart folder is a saved filter, the inbox is a status
 * filter, "find similar" is a vector filter.
 *
 * Every value is bound as a parameter. Nothing is interpolated into SQL.
 */
export async function queryAssets(query: LibraryQuery): Promise<LibraryResult> {
  const pool = db();
  const where: string[] = [];
  const params: unknown[] = [];

  const bind = (value: unknown): string => {
    params.push(value);
    return `$${params.length}`;
  };

  if (query.type?.length) where.push(`a.type = any(${bind(query.type)}::text[])`);
  if (query.status?.length) where.push(`a.status = any(${bind(query.status)}::text[])`);
  if (query.releaseStatus?.length) {
    where.push(`a.release_status = any(${bind(query.releaseStatus)}::text[])`);
  }
  if (query.minQuality) where.push(`a.quality >= ${bind(query.minQuality)}`);
  if (query.workshop) where.push(`b.workshop = ${bind(query.workshop)}`);

  // Every named tag must be present, not just one of them.
  for (const tag of query.tags ?? []) {
    where.push(`exists (
      select 1 from asset_tags at join tags t on t.id = at.tag_id
      where at.asset_id = a.id and t.facet = ${bind(tag.facet)} and t.name = ${bind(tag.name)}
    )`);
  }

  if (query.untagged) {
    where.push(`not exists (
      select 1 from asset_tags at where at.asset_id = a.id and at.confirmed
    )`);
  }

  if (query.unused) {
    where.push(`not exists (select 1 from asset_usage u where u.asset_id = a.id)`);
  }

  if (query.q) {
    const q = bind(`%${query.q}%`);
    where.push(`(a.description ilike ${q} or a.filename ilike ${q} or a.notes ilike ${q}
                 or a.creator ilike ${q} or a.original_path ilike ${q})`);
  }

  // Meaning search and "find similar" both come down to ordering by distance.
  // The exclusion goes in the WHERE clause, so it is bound before the vector:
  // the facet-count query reuses the WHERE parameters as a prefix and would
  // break if anything from the ORDER BY landed among them.
  let vector: string | null = null;
  if (query.similarTo) {
    vector = await embeddingOf(query.similarTo);
    if (vector) {
      where.push('a.embedding is not null');
      where.push(`a.id <> ${bind(query.similarTo)}`);
    }
  } else if (query.meaning) {
    vector = toVector(await embedOne(query.meaning));
    where.push('a.embedding is not null');
  }

  const clause = where.length ? `where ${where.join('\n and ')}` : '';
  // Everything bound so far belongs to the WHERE clause. Remember how many,
  // because the facet query runs the same clause and nothing after it.
  const whereParams = params.slice();

  const orderBy = vector ? `a.embedding <=> ${bind(vector)}::vector` : 'a.created_at desc';

  const limit = Math.min(query.limit ?? 120, 500);
  const offset = query.offset ?? 0;

  const sql = `
    select a.id, a.type, a.filename, a.bucket, a.r2_key, a.thumb_key, a.proxy_key,
           a.width, a.height, a.duration_s, a.clip_start_s, a.clip_end_s,
           a.status, a.quality, a.hero_candidate, a.description, a.notes,
           a.drive_link, a.original_path, a.creator, a.credit_line,
           a.taken_at, a.camera, a.release_status, a.created_at,
           b.workshop,
           coalesce((
             select json_agg(json_build_object(
               'name', t.name, 'facet', t.facet, 'source', at.source,
               'confirmed', at.confirmed, 'confidence', at.confidence
             ) order by t.facet, t.name)
             from asset_tags at join tags t on t.id = at.tag_id
             where at.asset_id = a.id
           ), '[]'::json) as tags,
           coalesce((
             select json_agg(json_build_object('name', p.name, 'confirmed', ap.confirmed)
                             order by p.name)
             from asset_people ap join people p on p.id = ap.person_id
             where ap.asset_id = a.id
           ), '[]'::json) as people,
           (select count(*)::int from asset_usage u where u.asset_id = a.id) as used_in,
           count(*) over () as total_count
    from assets a
    left join batches b on b.id = a.batch_id
    ${clause}
    order by ${orderBy}
    limit ${bind(limit)} offset ${bind(offset)}
  `;

  const { rows } = await pool.query<AssetRow & { total_count: string }>(sql, params);
  const total = rows[0] ? Number(rows[0].total_count) : 0;

  const assets: AssetWithUrls[] = await Promise.all(
    rows.map(async (row) => ({
      ...row,
      thumbUrl: row.thumb_key ? await presignGet('sfw-media', row.thumb_key) : null,
    })),
  );

  return { assets, total, facets: await facetCounts(clause, whereParams) };
}

/** Counts for the filter chips, over the same filtered set. */
async function facetCounts(
  clause: string,
  params: unknown[],
): Promise<{ facet: string; name: string; count: number }[]> {
  const { rows } = await db().query<{ facet: string; name: string; count: number }>(
    `select t.facet, t.name, count(*)::int as count
     from assets a
     left join batches b on b.id = a.batch_id
     join asset_tags at on at.asset_id = a.id
     join tags t on t.id = at.tag_id
     ${clause}
     group by t.facet, t.name
     order by t.facet, count desc, t.name`,
    params,
  );
  return rows;
}

async function embeddingOf(assetId: string): Promise<string | null> {
  const { rows } = await db().query<{ embedding: string | null }>(
    'select embedding::text as embedding from assets where id = $1',
    [assetId],
  );
  return rows[0]?.embedding ?? null;
}

export async function getAsset(id: string): Promise<(AssetWithUrls & { fileUrl: string }) | null> {
  const { rows } = await db().query<AssetRow>(
    `select a.*, b.workshop,
            coalesce((
              select json_agg(json_build_object(
                'name', t.name, 'facet', t.facet, 'source', at.source,
                'confirmed', at.confirmed, 'confidence', at.confidence
              ) order by t.facet, t.name)
              from asset_tags at join tags t on t.id = at.tag_id where at.asset_id = a.id
            ), '[]'::json) as tags,
            coalesce((
              select json_agg(json_build_object('name', p.name, 'confirmed', ap.confirmed))
              from asset_people ap join people p on p.id = ap.person_id where ap.asset_id = a.id
            ), '[]'::json) as people,
            (select count(*)::int from asset_usage u where u.asset_id = a.id) as used_in
     from assets a left join batches b on b.id = a.batch_id
     where a.id = $1`,
    [id],
  );

  const asset = rows[0];
  if (!asset) return null;

  return {
    ...asset,
    thumbUrl: asset.thumb_key ? await presignGet('sfw-media', asset.thumb_key) : null,
    // The proxy for video, the original for anything else.
    fileUrl: asset.proxy_key
      ? await presignGet('sfw-media', asset.proxy_key)
      : await presignGet(asset.bucket, asset.r2_key),
  };
}
