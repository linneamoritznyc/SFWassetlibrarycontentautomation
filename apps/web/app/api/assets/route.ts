import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { db } from '@/lib/db';
import { queryAssets } from '@/lib/assets';
import { fail, route } from '@/lib/http';

type IncomingAsset = {
  assetId: string;
  type: string;
  filename: string;
  bucket: string;
  r2Key: string;
  thumbKey?: string | null;
  width?: number | null;
  height?: number | null;
  durationS?: number | null;
  takenAt?: string | null;
  camera?: string | null;
  gpsLat?: number | null;
  gpsLng?: number | null;
};

/**
 * Creates the batch and its assets, then enqueues one `ingest` per asset.
 *
 * Batch provenance (Drive link, original path, creator, workshop) is entered
 * once and copied onto every asset, so an asset always knows where it came
 * from even if the batch row is later edited.
 *
 * Idempotent on re-submission: an asset whose bucket and key already exist is
 * left alone, because `assets(bucket, r2_key)` is unique.
 */
export const POST = route(async (request: NextRequest) => {
  const body = (await request.json()) as {
    batch?: { driveLink?: string; originalPath?: string; creator?: string; workshop?: string };
    assets?: IncomingAsset[];
  };

  const assets = body.assets ?? [];
  if (assets.length === 0) return fail('No assets given');

  const pool = db();
  const client = await pool.connect();
  const created: string[] = [];

  try {
    await client.query('begin');

    const batch = await client.query<{ id: string }>(
      `insert into batches (drive_link, original_path, creator, workshop)
       values ($1, $2, $3, $4) returning id`,
      [
        body.batch?.driveLink ?? null,
        body.batch?.originalPath ?? null,
        body.batch?.creator ?? null,
        body.batch?.workshop ?? null,
      ],
    );
    const batchId = batch.rows[0]!.id;

    for (const asset of assets) {
      const res = await client.query<{ id: string }>(
        `insert into assets
           (id, batch_id, type, filename, bucket, r2_key, thumb_key,
            width, height, duration_s, taken_at, camera, gps_lat, gps_lng,
            drive_link, original_path, creator, credit_line)
         values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
         on conflict (bucket, r2_key) do nothing
         returning id`,
        [
          asset.assetId,
          batchId,
          asset.type,
          asset.filename,
          asset.bucket,
          asset.r2Key,
          asset.thumbKey ?? null,
          asset.width ?? null,
          asset.height ?? null,
          asset.durationS ?? null,
          asset.takenAt ?? null,
          asset.camera ?? null,
          asset.gpsLat ?? null,
          asset.gpsLng ?? null,
          body.batch?.driveLink ?? null,
          body.batch?.originalPath ?? null,
          body.batch?.creator ?? null,
          body.batch?.creator ? `Photo: ${body.batch.creator}` : null,
        ],
      );

      const id = res.rows[0]?.id;
      if (id) created.push(id);
    }

    await client.query('commit');
  } catch (err) {
    await client.query('rollback');
    throw err;
  } finally {
    client.release();
  }

  // Enqueued after the transaction commits, so a worker cannot pick up a job
  // for an asset that is not visible yet.
  for (const id of created) {
    await enqueue(pool, { type: 'ingest', payload: { asset_id: id }, dedupeKey: `ingest:${id}` });
  }

  return NextResponse.json({ created: created.length, assetIds: created });
});

/** The library query. Every screen is this with different filters. */
export const GET = route(async (request: NextRequest) => {
  const p = request.nextUrl.searchParams;

  const tags = p.getAll('tag').flatMap((raw) => {
    const [facet, ...rest] = raw.split(':');
    const name = rest.join(':');
    return facet && name ? [{ facet, name }] : [];
  });

  const result = await queryAssets({
    type: p.getAll('type').filter(Boolean),
    status: p.getAll('status').filter(Boolean),
    releaseStatus: p.getAll('release').filter(Boolean),
    tags,
    untagged: p.get('untagged') === '1',
    unused: p.get('unused') === '1',
    q: p.get('q') ?? undefined,
    meaning: p.get('meaning') ?? undefined,
    similarTo: p.get('similarTo') ?? undefined,
    workshop: p.get('workshop') ?? undefined,
    minQuality: p.get('minQuality') ? Number(p.get('minQuality')) : undefined,
    limit: p.get('limit') ? Number(p.get('limit')) : undefined,
    offset: p.get('offset') ? Number(p.get('offset')) : undefined,
  });

  return NextResponse.json(result);
});
