import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { CAPTION_STYLE, LOUDNESS, RATIOS, type Ratio } from '@sfw/brand';
import { handler } from '@sfw/queue';
import { getObject, keys, putObject, type Bucket } from '@sfw/storage';
import { db } from '../db.js';
import { buildAss, buildSrt, shiftWords, wordsBetween, type Word } from '../captions.js';
import { cutClip as runCut, probe } from '../ffmpeg.js';
import { withTempDir } from '../temp.js';

/**
 * Cuts one clip at one ratio, with the captions burned in.
 *
 * Cut from the original in `sfw-raw`, never from the proxy: the proxy is 720p
 * and a 9:16 crop out of it would be soft. The captions come from the parent's
 * word timestamps, shifted so the clip starts at zero.
 *
 * Idempotent: writes to `clips/{clip_id}/{ratio}.mp4` every time.
 */
export const cutClip = handler<{ clip_id: string; ratio?: Ratio }>(async ({ job }) => {
  const pool = db();
  const clipId = job.payload.clip_id;
  const ratio: Ratio = job.payload.ratio ?? '9x16';

  if (!RATIOS[ratio]) throw new Error(`${ratio} is not a ratio this cuts`);

  const { rows } = await pool.query<{
    id: string;
    clip_start_s: number;
    clip_end_s: number;
    parent_id: string;
    parent_bucket: Bucket;
    parent_key: string;
    parent_filename: string;
    words: Word[] | null;
  }>(
    `select c.id, c.clip_start_s, c.clip_end_s, c.parent_id,
            p.bucket as parent_bucket, p.r2_key as parent_key, p.filename as parent_filename,
            t.words
     from assets c
     join assets p on p.id = c.parent_id
     left join transcripts t on t.asset_id = p.id
     where c.id = $1 and c.type = 'clip'`,
    [clipId],
  );

  const clip = rows[0];
  if (!clip) throw new Error(`No clip ${clipId}`);

  const size = RATIOS[ratio];
  const duration = clip.clip_end_s - clip.clip_start_s;

  await withTempDir(async (dir) => {
    const input = join(dir, clip.parent_filename.replace(/[^\w.-]/g, '_') || 'input');
    await writeFile(input, await getObject(clip.parent_bucket, clip.parent_key));

    const info = await probe(input);

    // Captions, if the parent has a transcript.
    let assPath: string | null = null;
    const words = clip.words ?? [];
    if (words.length > 0) {
      const inClip = shiftWords(
        wordsBetween(words, clip.clip_start_s, clip.clip_end_s),
        clip.clip_start_s,
      );

      if (inClip.length > 0) {
        assPath = join(dir, 'captions.ass');
        await writeFile(assPath, buildAss(inClip, size, CAPTION_STYLE));

        // One .srt per clip, whatever ratios get cut.
        await putObject(
          'sfw-media',
          keys.captions(clipId),
          buildSrt(inClip),
          'application/x-subrip',
        );
      }
    }

    const output = join(dir, `${ratio}.mp4`);
    await runCut({
      input,
      output,
      startS: clip.clip_start_s,
      durationS: duration,
      width: size.width,
      height: size.height,
      assPath,
      hasAudio: info.hasAudio,
      loudness: LOUDNESS,
    });

    await putObject('sfw-media', keys.clip(clipId, ratio), await readFile(output), 'video/mp4');

    // The 9:16 cut is the one the library shows, because it is the one that
    // goes out most often.
    if (ratio === '9x16') {
      await pool.query(
        `update assets
         set bucket = 'sfw-media', r2_key = $2, proxy_key = $2, duration_s = $3
         where id = $1`,
        [clipId, keys.clip(clipId, ratio), duration],
      );
    }
  });
});
