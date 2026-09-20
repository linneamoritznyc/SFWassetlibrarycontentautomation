import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { handler } from '@sfw/queue';
import { getObject, keys, putObject, type Bucket } from '@sfw/storage';
import { db } from '../db.js';
import { extractAudio, makeProxy, probe } from '../ffmpeg.js';
import { withTempDir } from '../temp.js';

/**
 * Makes the 720p proxy the browser plays and the mono audio Whisper reads.
 *
 * The original is never touched and never leaves `sfw-raw`. Idempotent: it
 * writes to the same two keys every time, so a re-run just overwrites them.
 */
export const proxy = handler<{ asset_id: string }>(async ({ job }) => {
  const pool = db();
  const assetId = job.payload.asset_id;

  const { rows } = await pool.query<{
    id: string;
    bucket: Bucket;
    r2_key: string;
    filename: string;
    width: number | null;
  }>('select id, bucket, r2_key, filename, width from assets where id = $1', [assetId]);

  const asset = rows[0];
  if (!asset) throw new Error(`No asset ${assetId}`);

  await withTempDir(async (dir) => {
    const input = join(dir, asset.filename.replace(/[^\w.-]/g, '_') || 'input');
    await writeFile(input, await getObject(asset.bucket, asset.r2_key));

    const info = await probe(input);

    const proxyPath = join(dir, 'proxy.mp4');
    await makeProxy(input, proxyPath);
    await putObject('sfw-media', keys.proxy(assetId), await readFile(proxyPath), 'video/mp4');

    let audioKey: string | null = null;
    if (info.hasAudio) {
      const audioPath = join(dir, 'audio.m4a');
      await extractAudio(input, audioPath);
      audioKey = keys.audio(assetId);
      await putObject('sfw-media', audioKey, await readFile(audioPath), 'audio/mp4');
    }

    await pool.query(
      `update assets
       set proxy_key = $2,
           audio_key = $3,
           width = coalesce(width, $4),
           height = coalesce(height, $5),
           duration_s = coalesce(duration_s, $6)
       where id = $1`,
      [assetId, keys.proxy(assetId), audioKey, info.width, info.height, info.durationS],
    );
  });
});
