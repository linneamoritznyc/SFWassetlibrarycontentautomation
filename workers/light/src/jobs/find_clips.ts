import { callClaude, findClipsSchema } from '@sfw/ai';
import { CLIP_RATIOS } from '@sfw/shared';
import { handler } from '@sfw/queue';
import { db } from '../db.js';

type Word = { w: string; start: number; end: number; speaker?: string | null };

/** The spec's constraints: 20 to 60 seconds, padded by 0.3 s at each end. */
const MIN_SECONDS = 20;
const MAX_SECONDS = 60;
const PAD_SECONDS = 0.3;

/**
 * Finds the moments in a long video worth cutting.
 *
 * Claude reads the transcript and proposes 12 to 15 candidates, more than are
 * needed so the weakest can be cut by a human. Its timings are then snapped to
 * real word boundaries: a model asked for a number will give one, and the
 * difference between 41.7 and the end of the actual word is the difference
 * between a clean cut and one that clips a syllable.
 *
 * Idempotent: candidates from a previous run that nobody has kept are replaced.
 */
export const findClips = handler<{ asset_id: string }>(async ({ job, enqueue }) => {
  const pool = db();
  const assetId = job.payload.asset_id;

  const { rows } = await pool.query<{
    id: string;
    filename: string;
    duration_s: number | null;
    text: string | null;
    words: Word[] | null;
  }>(
    `select a.id, a.filename, a.duration_s, t.text, t.words
     from assets a left join transcripts t on t.asset_id = a.id
     where a.id = $1`,
    [assetId],
  );

  const asset = rows[0];
  if (!asset) throw new Error(`No asset ${assetId}`);

  const words = asset.words ?? [];
  if (words.length === 0) {
    throw new Error(`Asset ${assetId} has no transcript yet. Transcribe it first.`);
  }

  const rules = await pool.query<{ text: string }>(
    `select text from rules where active and scope in ('all', 'reel') order by created_at`,
  );

  // The clips that actually performed, so it can see what good looked like.
  const examples = await pool.query<{ hook: string | null; saves: number | null }>(
    `select p.hook, max(m.saves) as saves
     from posts p
     join metrics m on m.post_id = p.id
     where p.format in ('reel', 'short') and p.hook is not null
     group by p.id, p.hook
     order by saves desc nulls last
     limit 5`,
  );

  const result = await callClaude({
    pool,
    jobId: job.id,
    prompt: 'find_clips',
    schema: findClipsSchema,
    maxTokens: 8000,
    input: [
      `Video: ${asset.filename}`,
      asset.duration_s ? `Duration: ${Math.round(asset.duration_s)} seconds.` : '',
      '',
      rules.rows.length ? 'Active rules for reels:' : '',
      ...rules.rows.map((r) => `- ${r.text}`),
      '',
      examples.rows.length ? 'Hooks that performed best in the past:' : '',
      ...examples.rows.map((e) => `- ${e.hook}`),
      '',
      'Transcript, with the time each word starts:',
      formatTranscript(words),
    ]
      .filter(Boolean)
      .join('\n'),
  });

  const candidates = result.clips
    .map((clip) => snapToWords(clip, words))
    .filter((clip): clip is NonNullable<typeof clip> => clip !== null)
    .sort((a, b) => b.score - a.score);

  const client = await pool.connect();
  const created: string[] = [];

  try {
    await client.query('begin');

    // Clear out the previous run's untouched suggestions. A clip somebody kept,
    // trimmed or archived is theirs and is left alone.
    await client.query(
      `delete from assets
       where parent_id = $1 and type = 'clip' and status = 'inbox'
         and not exists (select 1 from asset_usage u where u.asset_id = assets.id)`,
      [assetId],
    );

    for (const clip of candidates) {
      const res = await client.query<{ id: string }>(
        `insert into assets
           (parent_id, type, filename, bucket, r2_key, status,
            clip_start_s, clip_end_s, duration_s, description, notes)
         values ($1, 'clip', $2, 'sfw-media', $3, 'inbox', $4, $5, $6, $7, $8)
         returning id`,
        [
          assetId,
          `${asset.filename.replace(/\.[^.]+$/, '')}-${Math.round(clip.start)}s.mp4`,
          // Filled in by cut_clip once the file exists. Unique per row.
          `clips/pending/${assetId}-${clip.start.toFixed(2)}`,
          clip.start,
          clip.end,
          clip.end - clip.start,
          clip.hook,
          [
            clip.why,
            `Pillar: ${clip.pillar}`,
            `Speaker: ${clip.speaker || 'unknown'}`,
            `Score: ${clip.score}`,
          ]
            .filter(Boolean)
            .join('\n'),
        ],
      );

      const id = res.rows[0]!.id;
      created.push(id);

      await client.query(
        `insert into asset_tags (asset_id, tag_id, source, confirmed, confidence)
         select $1, t.id, 'ai', false, $3 from tags t where t.facet = 'pillar' and t.name = $2
         on conflict do nothing`,
        [id, clip.pillar, clip.score / 100],
      );
    }

    await client.query('commit');
  } catch (err) {
    await client.query('rollback');
    throw err;
  } finally {
    client.release();
  }

  // A 9:16 preview for each, so the Clips view has something to play. The
  // other ratios are cut only once a human keeps the clip.
  for (const id of created) {
    await enqueue({
      type: 'cut_clip',
      payload: { clip_id: id, ratio: CLIP_RATIOS[0] },
      priority: 6,
      dedupeKey: `cut_clip:${id}:${CLIP_RATIOS[0]}`,
    });
  }

  console.log(`[find_clips] ${created.length} candidates from ${asset.filename}`);
});

/** One line per sentence, prefixed with the time it starts. Exported for the tests. */
export function formatTranscript(words: Word[]): string {
  const lines: string[] = [];
  let current: Word[] = [];

  for (const word of words) {
    current.push(word);
    if (/[.!?]$/.test(word.w.trim()) || current.length > 40) {
      lines.push(
        `[${current[0]!.start.toFixed(1)}] ${current
          .map((w) => w.w)
          .join(' ')
          .trim()}`,
      );
      current = [];
    }
  }
  if (current.length > 0) {
    lines.push(
      `[${current[0]!.start.toFixed(1)}] ${current
        .map((w) => w.w)
        .join(' ')
        .trim()}`,
    );
  }
  return lines.join('\n');
}

export type Candidate = {
  start: number;
  end: number;
  hook: string;
  why: string;
  pillar: string;
  speaker: string;
  score: number;
};

/**
 * Moves the boundaries onto real word edges and pads them, then throws away
 * anything that is not a usable length.
 */
export function snapToWords(clip: Candidate, words: Word[]): Candidate | null {
  const first = words.find((w) => w.end > clip.start);
  const last = [...words].reverse().find((w) => w.start < clip.end);
  if (!first || !last) return null;

  const start = Math.max(0, first.start - PAD_SECONDS);
  const end = last.end + PAD_SECONDS;
  const length = end - start;

  // The model was told 20 to 60 seconds. Anything outside that after snapping
  // is dropped rather than trimmed, because trimming it would cut mid-sentence,
  // which is the thing the snapping exists to prevent.
  if (length < MIN_SECONDS || length > MAX_SECONDS) return null;
  if (end <= start) return null;

  return { ...clip, start, end };
}
