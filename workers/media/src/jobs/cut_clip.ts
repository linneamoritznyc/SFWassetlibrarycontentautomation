import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { CAPTION_STYLE, LOUDNESS, RATIOS, type Ratio } from '@sfw/brand';
import { handler } from '@sfw/queue';
import { getObject, keys, putObject, type Bucket } from '@sfw/storage';
import { db } from '../db.js';
import { buildAss, buildSrt, shiftWords, wordsBetween, type Word } from '../captions.js';
import { cutClip as runCut, probe } from '../ffmpeg.js';
import { cropExpression, smooth, trackSpeaker } from '../speaker.js';
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

    // Speaker tracking, when it is switched on. A centre crop loses whoever is
    // standing off to one side, which in workshop footage is most of the time.
    let cropX: string | null = null;
    const flags = (
      await pool.query<{ value: { speaker_tracking_crop?: boolean } }>(
        `select value from settings where key = 'flags'`,
      )
    ).rows[0]?.value;

    // Only worth it when the crop is narrower than the source. A 16:9 cut out
    // of 16:9 footage has nowhere to pan to.
    const narrower = size.width / size.height < (info.width ?? 16) / (info.height ?? 9);

    if (flags?.speaker_tracking_crop && narrower && info.width) {
      const track = await trackSpeaker(input, {
        startS: clip.clip_start_s,
        durationS: duration,
      });

      if (track && track.samples.some((s) => s.x !== null)) {
        // The crop width in the scaled frame, expressed on the source frame so
        // the track and the crop agree about coordinates.
        const scaled = (info.height ?? size.height) * (size.width / size.height);
        cropX = cropExpression(smooth(track, scaled), clip.clip_start_s);
        console.log(`[cut_clip] ${clipId} ${ratio}: following the speaker`);
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
      cropX,
      sourceWidth: info.width,
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
