import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { CAPTION_STYLE, LOUDNESS, RATIOS, type Ratio } from '@sfw/brand';
import { handler } from '@sfw/queue';
import { getObject, keys, putObject, type Bucket } from '@sfw/storage';
import { buildAss, buildSrt, shiftWords, wordsBetween, type Word } from '../captions.js';
import { db } from '../db.js';
import { FFMPEG, probe, run } from '../ffmpeg.js';
import { withTempDir } from '../temp.js';

export type Segment = { start: number; end: number };

export type EditPayload = {
  clip_id: string;
  ratio?: Ratio;
  /** Trim, split and reorder in one: the segments, in the order they play. */
  segments?: Segment[];
  /** Corrections to what Whisper heard, applied to the burned-in captions. */
  captionFixes?: { from: string; to: string }[];
  /** Where to take the crop from: 0 is hard left, 1 hard right, 0.5 centre. */
  cropFocus?: number;
  /** An asset id for a music bed, mixed under the speech. */
  musicAssetId?: string | null;
  musicGainDb?: number;
};

/**
 * The light editor's one job: re-cut a clip the way a human just said to.
 *
 * Trim, split and reorder are all the same thing once they are expressed as a
 * list of segments, so the UI can offer three verbs and this can implement
 * one. Caption fixes are applied to the words before they are burned in, so
 * correcting "vermicompost" fixes it everywhere it appears.
 *
 * Heavy editing still belongs somewhere else. This is for the last ten per
 * cent: the edge that lands half a word late, a name Whisper misheard, a crop
 * that cut someone out.
 */
export const editClip = handler<EditPayload>(async ({ job }) => {
  const pool = db();
  const clipId = job.payload.clip_id;
  const ratio: Ratio = job.payload.ratio ?? '9x16';

  const { rows } = await pool.query<{
    id: string;
    clip_start_s: number;
    clip_end_s: number;
    parent_bucket: Bucket;
    parent_key: string;
    parent_filename: string;
    words: Word[] | null;
  }>(
    `select c.id, c.clip_start_s, c.clip_end_s,
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

  const segments: Segment[] = job.payload.segments?.length
    ? job.payload.segments
    : [{ start: clip.clip_start_s, end: clip.clip_end_s }];

  for (const segment of segments) {
    if (!(segment.end > segment.start)) throw new Error('A segment has to end after it starts');
  }

  const size = RATIOS[ratio];
  const focus = clampFocus(job.payload.cropFocus);

  await withTempDir(async (dir) => {
    const input = join(dir, clip.parent_filename.replace(/[^\w.-]/g, '_') || 'input');
    await writeFile(input, await getObject(clip.parent_bucket, clip.parent_key));

    const info = await probe(input);
    const music = job.payload.musicAssetId ? await loadMusic(dir, job.payload.musicAssetId) : null;

    // One pass per segment, then concatenate. Doing it in a single filter
    // graph is possible and unreadable, and a re-edit is not a hot path.
    const pieces: string[] = [];
    let elapsed = 0;

    for (const [index, segment] of segments.entries()) {
      const piece = join(dir, `piece-${index}.mp4`);
      const duration = segment.end - segment.start;

      const words = fixWords(clip.words ?? [], job.payload.captionFixes ?? []);
      const inSegment = shiftWords(wordsBetween(words, segment.start, segment.end), segment.start);

      let assPath: string | null = null;
      if (inSegment.length > 0) {
        assPath = join(dir, `captions-${index}.ass`);
        await writeFile(assPath, buildAss(inSegment, size, CAPTION_STYLE));
      }

      const filters = [
        `scale=${size.width}:${size.height}:force_original_aspect_ratio=increase`,
        // focus 0 is hard left, 1 hard right. `iw-ow` is how much there is to
        // slide across, which is zero when the shapes already match.
        `crop=${size.width}:${size.height}:x='(iw-${size.width})*${focus.toFixed(3)}':y=0`,
        'setsar=1',
      ];
      if (assPath) filters.push(`ass='${assPath.replace(/\\/g, '/').replace(/:/g, '\\:')}'`);

      const args = [
        '-y',
        '-ss',
        segment.start.toFixed(3),
        '-i',
        input,
        '-t',
        duration.toFixed(3),
        '-vf',
        filters.join(','),
        '-c:v',
        'libx264',
        '-preset',
        'medium',
        '-crf',
        '20',
        '-pix_fmt',
        'yuv420p',
      ];

      if (info.hasAudio) {
        args.push(
          '-af',
          `loudnorm=I=${LOUDNESS.integrated}:TP=${LOUDNESS.truePeak}:LRA=${LOUDNESS.range}`,
          '-c:a',
          'aac',
          '-b:a',
          '128k',
          '-ar',
          '48000',
        );
      } else {
        args.push('-an');
      }

      args.push(piece);
      await run(FFMPEG, args);

      pieces.push(piece);
      elapsed += duration;
    }

    // Concatenate. The demuxer needs a list file and identical encodings,
    // which the loop above guarantees by using the same settings every time.
    const listPath = join(dir, 'pieces.txt');
    await writeFile(listPath, pieces.map((p) => `file '${p}'`).join('\n'));

    const joined = join(dir, 'joined.mp4');
    await run(FFMPEG, ['-y', '-f', 'concat', '-safe', '0', '-i', listPath, '-c', 'copy', joined]);

    let final = joined;

    if (music && info.hasAudio) {
      final = join(dir, 'final.mp4');
      const gain = job.payload.musicGainDb ?? -18;

      await run(FFMPEG, [
        '-y',
        '-i',
        joined,
        '-stream_loop',
        '-1',
        '-i',
        music,
        '-filter_complex',
        // The bed sits well under the speech and ducks nothing: at -18dB it
        // does not need to, and a compressor on a workshop clip sounds worse.
        `[1:a]volume=${gain}dB[bed];[0:a][bed]amix=inputs=2:duration=first:dropout_transition=0[a]`,
        '-map',
        '0:v',
        '-map',
        '[a]',
        '-c:v',
        'copy',
        '-c:a',
        'aac',
        '-b:a',
        '128k',
        '-shortest',
        final,
      ]);
    }

    await putObject('sfw-media', keys.clip(clipId, ratio), await readFile(final), 'video/mp4');

    const allWords = fixWords(clip.words ?? [], job.payload.captionFixes ?? []);
    const firstSegment = segments[0]!;
    await putObject(
      'sfw-media',
      keys.captions(clipId),
      buildSrt(
        shiftWords(
          wordsBetween(allWords, firstSegment.start, firstSegment.end),
          firstSegment.start,
        ),
      ),
      'application/x-subrip',
    );

    if (ratio === '9x16') {
      await pool.query(
        `update assets
         set r2_key = $2, proxy_key = $2, duration_s = $3,
             clip_start_s = $4, clip_end_s = $5
         where id = $1`,
        [
          clipId,
          keys.clip(clipId, ratio),
          elapsed,
          firstSegment.start,
          segments[segments.length - 1]!.end,
        ],
      );
    }

    console.log(
      `[edit_clip] ${clipId} re-cut: ${segments.length} segment(s), ${elapsed.toFixed(1)}s` +
        (music ? ', with a music bed' : ''),
    );
  });
});

/** Corrections to what Whisper heard, applied everywhere the word appears. */
export function fixWords(words: Word[], fixes: { from: string; to: string }[]): Word[] {
  if (fixes.length === 0) return words;

  return words.map((word) => {
    const fix = fixes.find(
      (f) => f.from.toLowerCase() === word.w.toLowerCase().replace(/[^\w'-]/g, ''),
    );
    if (!fix) return word;

    // Keep the punctuation that was attached to the original word.
    const trailing = word.w.match(/[^\w'-]+$/)?.[0] ?? '';
    return { ...word, w: fix.to + trailing };
  });
}

function clampFocus(value: number | undefined): number {
  if (value === undefined || Number.isNaN(value)) return 0.5;
  return Math.min(Math.max(value, 0), 1);
}

async function loadMusic(dir: string, assetId: string): Promise<string | null> {
  const { rows } = await db().query<{ bucket: Bucket; r2_key: string }>(
    'select bucket, r2_key from assets where id = $1',
    [assetId],
  );
  const asset = rows[0];
  if (!asset) return null;

  const path = join(dir, 'music');
  await writeFile(path, await getObject(asset.bucket, asset.r2_key));
  return path;
}
