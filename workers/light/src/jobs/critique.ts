import { callClaude, critiqueSchema } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { runStringChecks } from '@sfw/shared';
import { buildBrief } from '../brief.js';
import { db } from '../db.js';
import { thumbnailsFor } from '../images.js';

/** Two rewrites and then a human looks at it, however it turned out. */
const MAX_LOOPS = 2;

/**
 * Checks a draft before a human sees it.
 *
 * A separate Claude call with a different prompt, given the images so it can
 * catch a caption that does not match the picture. The mechanical checks run
 * first and are added to its must-fix list: a regular expression cannot be
 * talked round about an em dash.
 *
 * `must_fix` sends the draft back to the writer with the issues quoted, at most
 * twice. After that it goes to review with the notes attached, because a loop
 * that never terminates is worse than a draft a human has to fix.
 */
export const critique = handler<{ post_id: string; loop?: number }>(async ({ job, enqueue }) => {
  const pool = db();
  const postId = job.payload.post_id;
  const loop = job.payload.loop ?? 0;

  const postRows = await pool.query<{
    id: string;
    story_id: number | null;
    platform: string;
    format: string;
    hook: string | null;
    caption: string | null;
    hashtags: string[];
    cta_url: string | null;
  }>(
    `select id, story_id, platform, format, hook, caption, hashtags, cta_url
     from posts where id = $1`,
    [postId],
  );

  const post = postRows.rows[0];
  if (!post) throw new Error(`No post ${postId}`);
  if (!post.caption) throw new Error(`Post ${postId} has nothing to critique yet`);
  if (!post.story_id) throw new Error(`Post ${postId} has no story`);

  const briefing = await buildBrief(pool, post.story_id, { postId });
  const images = await thumbnailsFor(briefing.assets);

  // The mechanical half. These are not opinions.
  const mechanical = runStringChecks(`${post.hook ?? ''}\n${post.caption}`).map((hit) => ({
    check: hit.check,
    quote: hit.quote,
    fix: hit.note,
  }));

  const result = await callClaude({
    pool,
    jobId: job.id,
    prompt: 'critique',
    schema: critiqueSchema,
    images,
    input: JSON.stringify(
      {
        draft: {
          platform: post.platform,
          format: post.format,
          hook: post.hook,
          caption: post.caption,
          hashtags: post.hashtags,
          cta_url: post.cta_url,
        },
        assets: briefing.assets.map((a, i) => ({ image: i + 1, description: a.description })),
        facts: briefing.facts.map((f) => ({ id: f.id, text: f.text, source: f.source })),
        rules: briefing.rules,
      },
      null,
      2,
    ),
  });

  const mustFix = [...mechanical, ...result.must_fix];

  // The mechanical failures are not negotiable, so they cap the score too.
  const score = mechanical.length > 0 ? Math.min(result.score, 55) : result.score;

  await pool.query(`update posts set critic_score = $2, critic_notes = $3::jsonb where id = $1`, [
    postId,
    score,
    JSON.stringify({
      verdict: result.verdict,
      issues: result.issues,
      must_fix: mustFix,
      mechanical,
      loop,
    }),
  ]);

  if (mustFix.length > 0 && loop < MAX_LOOPS) {
    await pool.query(`update posts set status = 'revising' where id = $1`, [postId]);
    await enqueue({
      type: 'write',
      payload: {
        post_id: postId,
        loop: loop + 1,
        issues: mustFix.map((f) => `${f.check}: "${f.quote}" - ${f.fix}`),
      },
      dedupeKey: `write:${postId}:${loop + 1}`,
    });
    console.log(
      `[critique] ${postId} back to the writer with ${mustFix.length} must-fix (loop ${loop + 1})`,
    );
    return;
  }

  await pool.query(`update posts set status = 'in_review' where id = $1`, [postId]);
  console.log(`[critique] ${postId} scored ${score}, ready for review`);
});
