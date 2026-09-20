import { readFile, readdir, stat, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { mergeTranscripts, transcribeFile, WHISPER_MAX_BYTES, type Transcript } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { getObject, keys, putObject } from '@sfw/storage';
import { db } from '../db.js';
import { extractAudio, probe, splitAudio } from '../ffmpeg.js';
import { withTempDir } from '../temp.js';

/** Long enough to be worth clipping, per spec section 5. */
const CLIPPABLE_SECONDS = 180;

/** Ten minutes of 64k mono is about 5 MB, comfortably inside Whisper's limit. */
const CHUNK_SECONDS = 600;

/**
 * Transcribes a video with word-level timestamps.
 *
 * Audio over 25 MB is split on a time boundary and the pieces transcribed
 * separately, with each piece's timestamps shifted back by its offset. Time
 * rather than size, because then the arithmetic is just multiplication.
 *
 * Idempotent: the transcript is upserted on the asset id.
 */
export const transcribe = handler<{ asset_id: string }>(async ({ job, enqueue }) => {
  const pool = db();
  const assetId = job.payload.asset_id;

  const { rows } = await pool.query<{
    id: string;
    bucket: 'sfw-raw' | 'sfw-media';
    r2_key: string;
    audio_key: string | null;
    duration_s: number | null;
  }>('select id, bucket, r2_key, audio_key, duration_s from assets where id = $1', [assetId]);

  const asset = rows[0];
  if (!asset) throw new Error(`No asset ${assetId}`);

  const transcript = await withTempDir(async (dir) => {
    const audioPath = join(dir, 'audio.m4a');

    if (asset.audio_key) {
      await writeFile(audioPath, await getObject('sfw-media', asset.audio_key));
    } else {
      // proxy usually makes this, but transcribe should work on its own too.
      const original = join(dir, 'original');
      await writeFile(original, await getObject(asset.bucket, asset.r2_key));
      const info = await probe(original);
      if (!info.hasAudio) throw new Error(`Asset ${assetId} has no audio track to transcribe`);

      await extractAudio(original, audioPath);
      await putObject('sfw-media', keys.audio(assetId), await readFile(audioPath), 'audio/mp4');
      await pool.query('update assets set audio_key = $2 where id = $1', [
        assetId,
        keys.audio(assetId),
      ]);
    }

    const { size } = await stat(audioPath);

    if (size <= WHISPER_MAX_BYTES) {
      return transcribeFile(audioPath);
    }

    await splitAudio(audioPath, join(dir, 'chunk-%03d.m4a'), CHUNK_SECONDS);
    const chunks = (await readdir(dir)).filter((f) => f.startsWith('chunk-')).sort();

    const parts: Transcript[] = [];
    for (const [index, chunk] of chunks.entries()) {
      parts.push(await transcribeFile(join(dir, chunk), index * CHUNK_SECONDS));
    }
    return mergeTranscripts(parts);
  });

  await pool.query(
    `insert into transcripts (asset_id, language, text, words)
     values ($1, $2, $3, $4::jsonb)
     on conflict (asset_id) do update
       set language = excluded.language, text = excluded.text, words = excluded.words`,
    [assetId, transcript.language, transcript.text, JSON.stringify(transcript.words)],
  );

  // The transcript changes what the asset is about, so its vector is stale.
  await enqueue({ type: 'embed', payload: { asset_id: assetId }, dedupeKey: `embed:${assetId}` });

  // Spec section 5: transcribe done and over three minutes means find clips.
  const duration = asset.duration_s ?? transcript.words[transcript.words.length - 1]?.end ?? 0;
  if (duration > CLIPPABLE_SECONDS) {
    await enqueue({
      type: 'find_clips',
      payload: { asset_id: assetId },
      dedupeKey: `find_clips:${assetId}`,
    });
  }
});
