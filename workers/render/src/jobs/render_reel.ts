import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { mkdtemp, rm } from 'node:fs/promises';
import { renderMedia, selectComposition } from '@remotion/renderer';
import { handler } from '@sfw/queue';
import { isTemplate, TEMPLATES } from '@sfw/remotion';
import { keys, presignGet, putObject, type Bucket } from '@sfw/storage';
import { db } from '../db.js';
import { templateBundle } from '../bundle.js';

/**
 * Renders a Reel.
 *
 * The clips are handed over as presigned URLs rather than downloaded: Remotion
 * fetches them itself while rendering, and a three-clip Reel would otherwise
 * mean writing a few hundred megabytes to disk first.
 *
 * Idempotent through the `renders` row: the same render id writes to the same
 * key, and the post points at the row rather than at a file.
 */
export const renderReel = handler<{ post_id: string; template?: string }>(async ({ job }) => {
  const pool = db();
  const postId = job.payload.post_id;

  const { rows } = await pool.query<{
    id: string;
    format: string;
    hook: string | null;
    caption: string | null;
    cta_url: string | null;
    asset_ids: string[];
    angle: string | null;
    pillar: string | null;
  }>(
    `select p.id, p.format, p.hook, p.caption, p.cta_url, p.asset_ids, s.angle, s.pillar
     from posts p left join stories s on s.id = p.story_id
     where p.id = $1`,
    [postId],
  );

  const post = rows[0];
  if (!post) throw new Error(`No post ${postId}`);

  const template = job.payload.template ?? 'WorkshopMoment';
  if (!isTemplate(template)) {
    throw new Error(`"${template}" is not a template. Try ${TEMPLATES.join(' or ')}.`);
  }

  // Only clips and renders can go in a Reel, and only ones that have a file.
  const { rows: clips } = await pool.query<{
    id: string;
    bucket: Bucket;
    r2_key: string;
    duration_s: number | null;
    description: string | null;
  }>(
    `select id, bucket, r2_key, duration_s, description
     from assets
     where id = any($1::uuid[]) and type in ('clip', 'render', 'video')
       and r2_key not like 'clips/pending/%'`,
    [post.asset_ids],
  );

  if (clips.length === 0) {
    throw new Error(`Post ${postId} has no cut clips to render. Keep a clip first.`);
  }

  const render = await pool.query<{ id: string }>(
    `insert into renders (template, input, status)
     values ($1, $2::jsonb, 'running')
     returning id`,
    [template, JSON.stringify({ post_id: postId, clip_ids: clips.map((c) => c.id) })],
  );
  const renderId = render.rows[0]!.id;

  const inputProps =
    template === 'FieldNotes'
      ? {
          eyebrow: 'Field Notes',
          title: post.hook ?? post.angle ?? 'Field Notes',
          subtitle: post.angle ?? '',
          clips: await clipProps(clips),
          endCard:
            'Practicum graduates publish their trials, including the ones that did not work.',
          ctaUrl: displayUrl(post.cta_url),
        }
      : {
          hook: post.hook ?? post.angle ?? '',
          speaker: '',
          place: '',
          clips: await clipProps(clips),
          endCard: 'Learn in person at the next Accelerator Workshop.',
          ctaUrl: displayUrl(post.cta_url),
        };

  const started = Date.now();
  const dir = await mkdtemp(join(process.env.MEDIA_TMPDIR ?? tmpdir(), 'sfw-render-'));

  try {
    const serveUrl = await templateBundle();

    const composition = await selectComposition({
      serveUrl,
      id: template,
      inputProps,
      browserExecutable: process.env.REMOTION_CHROME_EXECUTABLE,
    });

    const output = join(dir, `${renderId}.mp4`);

    await renderMedia({
      serveUrl,
      composition,
      codec: 'h264',
      outputLocation: output,
      inputProps,
      browserExecutable: process.env.REMOTION_CHROME_EXECUTABLE,
      // One at a time: the worker is concurrency 1 and Chromium is the memory.
      concurrency: 1,
      onProgress: ({ progress }) => {
        const percent = Math.round(progress * 100);
        if (percent % 25 === 0) console.log(`[render_reel] ${postId} ${percent}%`);
      },
    });

    const key = keys.render(renderId);
    await putObject('sfw-media', key, await readFile(output), 'video/mp4');

    const durationS = composition.durationInFrames / composition.fps;

    await pool.query(
      `update renders set status = 'done', bucket = 'sfw-media', r2_key = $2, duration_s = $3
       where id = $1`,
      [renderId, key, durationS],
    );

    await pool.query('update posts set render_id = $2 where id = $1', [postId, renderId]);

    console.log(
      `[render_reel] ${postId} rendered ${durationS.toFixed(1)}s in ${Math.round((Date.now() - started) / 1000)}s`,
    );
  } catch (err) {
    await pool.query(`update renders set status = 'failed' where id = $1`, [renderId]);
    throw err;
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
});

async function clipProps(
  clips: {
    bucket: Bucket;
    r2_key: string;
    duration_s: number | null;
    description: string | null;
  }[],
): Promise<{ src: string; durationS: number; label?: string }[]> {
  return Promise.all(
    clips.map(async (clip) => ({
      src: await presignGet(clip.bucket, clip.r2_key),
      durationS: clip.duration_s ?? 10,
      // The hook already shows on the intro card; a label on every clip would
      // be the same words twice.
      label: undefined,
    })),
  );
}

/** The end card shows a readable address, not a tracking URL. */
function displayUrl(url: string | null): string {
  if (!url) return 'soilfoodweb.com';
  try {
    return new URL(url).host.replace(/^www\./, '');
  } catch {
    return url;
  }
}
