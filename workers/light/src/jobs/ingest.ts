import { callClaude, tagSchema } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { getObject, type Bucket } from '@sfw/storage';
import { TAG_NAMES_BY_FACET } from '@sfw/shared';
import { db } from '../db.js';

type Asset = {
  id: string;
  type: string;
  filename: string;
  bucket: Bucket;
  r2_key: string;
  thumb_key: string | null;
  description: string | null;
  quality: number | null;
  status: string;
  duration_s: number | null;
  workshop: string | null;
  creator: string | null;
  original_path: string | null;
};

/**
 * Describes and tags one asset.
 *
 * Idempotent: re-running replaces this asset's unconfirmed AI tags and leaves
 * anything a human has touched alone. A description someone wrote by hand is
 * never overwritten, and a quality someone set by hand is never overwritten.
 *
 * On success the asset moves to `tagged`, which the database trigger turns into
 * an `embed` job. It stays in the Inbox until a human confirms the tags.
 */
export const ingest = handler<{ asset_id: string }>(async ({ job, enqueue }) => {
  const pool = db();
  const assetId = job.payload.asset_id;

  const { rows } = await pool.query<Asset>(
    `select a.id, a.type, a.filename, a.bucket, a.r2_key, a.thumb_key, a.description,
            a.quality, a.status, a.duration_s,
            b.workshop, b.creator, b.original_path
     from assets a
     left join batches b on b.id = a.batch_id
     where a.id = $1`,
    [assetId],
  );

  const asset = rows[0];
  if (!asset) throw new Error(`No asset ${assetId}`);

  // A document's facts come from extract_doc, not from looking at a thumbnail.
  if (asset.type === 'doc') {
    await enqueue({
      type: 'extract_doc',
      payload: { asset_id: assetId },
      dedupeKey: `extract_doc:${assetId}`,
    });
    return;
  }

  const image = await loadImage(asset);
  if (!image) {
    throw new Error(`Asset ${assetId} has no thumbnail to look at (thumb_key is empty)`);
  }

  const people = await pool.query<{ name: string; role: string | null }>(
    'select name, role from people order by name',
  );

  const result = await callClaude({
    pool,
    jobId: job.id,
    prompt: 'tag',
    schema: tagSchema,
    images: [{ mediaType: image.mediaType, data: image.data, label: 'The asset:' }],
    input: [
      'Batch context:',
      `  workshop: ${asset.workshop ?? 'unknown'}`,
      `  creator: ${asset.creator ?? 'unknown'}`,
      `  original path: ${asset.original_path ?? 'unknown'}`,
      `  filename: ${asset.filename}`,
      `  type: ${asset.type}`,
      asset.duration_s ? `  duration: ${Math.round(asset.duration_s)}s` : '',
      '',
      'Tag vocabulary, by facet. Choose only from these:',
      ...Object.entries(TAG_NAMES_BY_FACET).map(
        ([facet, names]) => `  ${facet}: ${names.join(', ')}`,
      ),
      '',
      'People on file, for people_guess:',
      ...people.rows.map((p) => `  ${p.name}${p.role ? ` (${p.role})` : ''}`),
    ]
      .filter(Boolean)
      .join('\n'),
  });

  const client = await pool.connect();
  try {
    await client.query('begin');

    // Replace only what the AI put there last time.
    await client.query(
      `delete from asset_tags where asset_id = $1 and source = 'ai' and not confirmed`,
      [assetId],
    );

    for (const tag of result.tags) {
      if (tag.confidence < 0.4) continue;
      await client.query(
        `insert into asset_tags (asset_id, tag_id, source, confirmed, confidence)
         select $1, t.id, 'ai', false, $4
         from tags t where t.name = $2 and t.facet = $3
         on conflict (asset_id, tag_id) do nothing`,
        [assetId, tag.name, tag.facet, tag.confidence],
      );
    }

    await client.query(
      `delete from asset_people where asset_id = $1 and source = 'ai' and not confirmed`,
      [assetId],
    );

    for (const guess of result.people_guess) {
      if (guess.confidence < 0.6) continue;
      await client.query(
        `insert into asset_people (asset_id, person_id, source, confirmed)
         select $1, p.id, 'ai', false from people p where p.name = $2
         on conflict (asset_id, person_id) do nothing`,
        [assetId, guess.name],
      );
    }

    // coalesce keeps anything a human already wrote.
    await client.query(
      `update assets
       set description = coalesce(description, $2),
           quality = coalesce(quality, $3),
           hero_candidate = $4,
           notes = coalesce(nullif(notes, ''), nullif($5, '')),
           status = case when status = 'inbox' then 'tagged' else status end
       where id = $1`,
      [assetId, result.description, result.quality, result.hero_candidate, result.notes],
    );

    await client.query('commit');
  } catch (err) {
    await client.query('rollback');
    throw err;
  } finally {
    client.release();
  }

  // Spec section 5: ingest done on video enqueues proxy and transcribe.
  if (asset.type === 'video') {
    await enqueue({ type: 'proxy', payload: { asset_id: assetId }, dedupeKey: `proxy:${assetId}` });
    await enqueue({
      type: 'transcribe',
      payload: { asset_id: assetId },
      dedupeKey: `transcribe:${assetId}`,
    });
  }
});

const MEDIA_TYPES: Record<string, 'image/jpeg' | 'image/png' | 'image/webp' | 'image/gif'> = {
  jpg: 'image/jpeg',
  jpeg: 'image/jpeg',
  png: 'image/png',
  webp: 'image/webp',
  gif: 'image/gif',
};

async function loadImage(asset: Asset): Promise<{
  data: Buffer;
  mediaType: 'image/jpeg' | 'image/png' | 'image/webp' | 'image/gif';
} | null> {
  // Thumbnails are always JPEG and always small, which is what Claude should
  // see. Originals stay in R2 (spec section 9).
  if (asset.thumb_key) {
    return { data: await getObject('sfw-media', asset.thumb_key), mediaType: 'image/jpeg' };
  }

  // A graphic or reference uploaded without a browser-made thumbnail: use the
  // original if it is an image format Claude accepts.
  const ext = asset.filename.split('.').pop()?.toLowerCase() ?? '';
  const mediaType = MEDIA_TYPES[ext];
  if (!mediaType) return null;

  return { data: await getObject(asset.bucket, asset.r2_key), mediaType };
}
