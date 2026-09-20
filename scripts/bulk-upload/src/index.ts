/**
 * Registers objects already in R2 as assets and enqueues `ingest` for each.
 *
 * The companion to the rclone copy in this folder's README: rclone moves seven
 * terabytes of footage into `sfw-raw` without going near a browser, and this
 * tells the database those files exist.
 *
 * Idempotent. `assets(bucket, r2_key)` is unique, so an object that already has
 * an asset row is skipped. Re-run it after an interrupted copy and only the new
 * files are added.
 *
 *   node scripts/bulk-upload/dist/index.js \
 *     --prefix originals/ \
 *     --creator "SFW" \
 *     --workshop "Wild Ken Hill" \
 *     --drive-link "https://drive.google.com/..." \
 *     --dry-run
 */
import { randomUUID } from 'node:crypto';
import { createPool } from '@sfw/db';
import { enqueue } from '@sfw/queue';
import { listObjects, type Bucket } from '@sfw/storage';

type Options = {
  bucket: Bucket;
  prefix: string;
  creator: string | null;
  workshop: string | null;
  driveLink: string | null;
  originalPath: string | null;
  dryRun: boolean;
  limit: number;
};

const VIDEO = new Set(['mp4', 'mov', 'm4v', 'avi', 'mkv', 'mts', 'mxf', 'webm']);
const PHOTO = new Set([
  'jpg',
  'jpeg',
  'heic',
  'tif',
  'tiff',
  'webp',
  'dng',
  'raf',
  'cr2',
  'nef',
  'arw',
]);
const GRAPHIC = new Set(['png', 'svg', 'ai', 'psd']);
const DOC = new Set(['pdf']);

function typeFor(key: string): string | null {
  const ext = key.split('.').pop()?.toLowerCase() ?? '';
  if (VIDEO.has(ext)) return 'video';
  if (PHOTO.has(ext)) return 'photo';
  if (GRAPHIC.has(ext)) return 'graphic';
  if (DOC.has(ext)) return 'doc';
  // Sidecar files, .DS_Store, anything unrecognised: not an asset.
  return null;
}

function parseArgs(argv: string[]): Options {
  const get = (name: string): string | null => {
    const i = argv.indexOf(`--${name}`);
    return i >= 0 ? (argv[i + 1] ?? null) : null;
  };

  return {
    bucket: (get('bucket') as Bucket) ?? 'sfw-raw',
    prefix: get('prefix') ?? 'originals/',
    creator: get('creator'),
    workshop: get('workshop'),
    driveLink: get('drive-link'),
    originalPath: get('original-path'),
    dryRun: argv.includes('--dry-run'),
    limit: Number(get('limit') ?? '0') || Number.POSITIVE_INFINITY,
  };
}

async function main(): Promise<void> {
  const options = parseArgs(process.argv.slice(2));
  const pool = createPool();

  console.log(`Listing ${options.bucket}/${options.prefix}`);
  const objects = await listObjects(options.bucket, options.prefix);
  console.log(`${objects.length} object(s) found.`);

  const candidates = objects
    .filter((o) => o.size > 0)
    .map((o) => ({ ...o, type: typeFor(o.key) }))
    .filter((o): o is typeof o & { type: string } => o.type !== null)
    .slice(0, options.limit);

  const skippedByType = objects.length - candidates.length;
  if (skippedByType > 0) console.log(`${skippedByType} skipped: folders, empties, unknown types.`);

  if (candidates.length === 0) {
    await pool.end();
    return;
  }

  if (options.dryRun) {
    console.log('\nDry run. Would register:');
    for (const c of candidates.slice(0, 20)) {
      console.log(`  ${c.type.padEnd(8)} ${c.key}`);
    }
    if (candidates.length > 20) console.log(`  ... and ${candidates.length - 20} more`);
    console.log('\nRe-run without --dry-run to write.');
    await pool.end();
    return;
  }

  const batch = await pool.query<{ id: string }>(
    `insert into batches (drive_link, original_path, creator, workshop)
     values ($1, $2, $3, $4) returning id`,
    [options.driveLink, options.originalPath ?? options.prefix, options.creator, options.workshop],
  );
  const batchId = batch.rows[0]!.id;

  let added = 0;
  let already = 0;

  for (const object of candidates) {
    const filename = object.key.split('/').pop() ?? object.key;

    const res = await pool.query<{ id: string }>(
      `insert into assets
         (id, batch_id, type, filename, bucket, r2_key,
          drive_link, original_path, creator, credit_line)
       values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
       on conflict (bucket, r2_key) do nothing
       returning id`,
      [
        randomUUID(),
        batchId,
        object.type,
        filename,
        options.bucket,
        object.key,
        options.driveLink,
        options.originalPath ?? object.key,
        options.creator,
        options.creator ? `Photo: ${options.creator}` : null,
      ],
    );

    const id = res.rows[0]?.id;
    if (!id) {
      already += 1;
      continue;
    }

    await enqueue(pool, { type: 'ingest', payload: { asset_id: id }, dedupeKey: `ingest:${id}` });
    added += 1;

    if (added % 100 === 0) console.log(`  ${added} registered`);
  }

  // An empty batch means every object was already known. Do not leave it.
  if (added === 0) {
    await pool.query('delete from batches where id = $1', [batchId]);
  }

  console.log(`\nRegistered ${added}. Already known: ${already}.`);
  console.log(added > 0 ? 'Tagging is queued. Watch it in the Errors view.' : 'Nothing to do.');

  await pool.end();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
