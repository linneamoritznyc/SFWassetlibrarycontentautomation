import { callClaude, writeSchema } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { buildBrief } from '../brief.js';
import { db } from '../db.js';
import { thumbnailsFor } from '../images.js';
import { runGapCheck } from './gap_check.js';

/**
 * Drafts one post.
 *
 * Three steps, in the order the spec sets: build the briefing, check what the
 * writer would be assuming, then write with the chosen images attached so the
 * caption can describe what is actually in the picture.
 *
 * A blocking unknown stops here and leaves the post in `revising` with a
 * question out to a named person. That is the point of the gap check: a post
 * built on an invented date is worse than a post that is late.
 *
 * Idempotent: every run appends a new `post_versions` row, so the history of
 * what the AI wrote is kept, and the post itself carries the latest.
 */
export const write = handler<{ post_id: string; issues?: string[]; loop?: number }>(
  async ({ job, enqueue }) => {
    const pool = db();
    const postId = job.payload.post_id;
    const loop = job.payload.loop ?? 0;

    const postRows = await pool.query<{
      id: string;
      story_id: number | null;
      platform: string;
      format: string;
      asset_ids: string[];
      slot_date: string | null;
    }>(
      `select id, story_id, platform, format, asset_ids, slot_date::text
       from posts where id = $1`,
      [postId],
    );

    const post = postRows.rows[0];
    if (!post) throw new Error(`No post ${postId}`);
    if (!post.story_id) throw new Error(`Post ${postId} has no story to write from`);

    // PRD principle 1, checked here as well as in the database: a post exists
    // only when its material exists.
    if (post.asset_ids.length === 0) {
      throw new Error(
        `Post ${postId} has no material. A post needs at least one asset or document.`,
      );
    }

    const briefing = await buildBrief(pool, post.story_id, { postId });

    // Only on the first pass: a rewrite is answering the critic, not
    // re-asking the same questions.
    if (loop === 0) {
      const gaps = await runGapCheck(pool, postId, briefing, job.id);

      if (gaps.blocked) {
        await pool.query(`update posts set status = 'revising' where id = $1`, [postId]);
        console.log(`[write] ${postId} is waiting on ${gaps.asked} question(s)`);
        return;
      }
    }

    const images = await thumbnailsFor(briefing.assets);

    const result = await callClaude({
      pool,
      jobId: job.id,
      prompt: 'write',
      schema: writeSchema,
      images,
      input: JSON.stringify(
        {
          slot: { date: post.slot_date, platform: post.platform, format: post.format },
          story: briefing.story,
          assets: briefing.assets.map((a, i) => ({
            image: i + 1,
            id: a.id,
            description: a.description,
            credit_line: a.credit_line,
            workshop: a.workshop,
          })),
          facts: briefing.facts.map((f) => ({ id: f.id, text: f.text, source: f.source })),
          rules: briefing.rules,
          examples: briefing.examples,
          calendar: briefing.calendar_context,
          issues_to_fix: job.payload.issues ?? [],
        },
        null,
        2,
      ),
    });

    if (result.blocked_reason) {
      await pool.query(
        `update posts set status = 'revising', critic_notes = $2::jsonb where id = $1`,
        [postId, JSON.stringify({ blocked: result.blocked_reason })],
      );
      console.log(`[write] ${postId} could not be written: ${result.blocked_reason}`);
      return;
    }

    const client = await pool.connect();
    try {
      await client.query('begin');

      const version = await client.query<{ next: number }>(
        `select coalesce(max(version), 0) + 1 as next from post_versions where post_id = $1`,
        [postId],
      );

      await client.query(
        `insert into post_versions
           (post_id, version, author, caption, hook, hashtags, asset_ids, prompt_version)
         values ($1, $2, 'ai', $3, $4, $5::text[], $6::uuid[],
                 (select version::text from prompts where name = 'write' and active))`,
        [
          postId,
          version.rows[0]!.next,
          result.caption,
          result.hook,
          result.hashtags,
          post.asset_ids,
        ],
      );

      await client.query(
        `update posts
         set hook = $2, caption = $3, hashtags = $4::text[], cta_text = $5, cta_url = $6,
             status = 'proposed'
         where id = $1`,
        [postId, result.hook, result.caption, result.hashtags, result.cta_text, result.cta_url],
      );

      await client.query('commit');
    } catch (err) {
      await client.query('rollback');
      throw err;
    } finally {
      client.release();
    }

    await enqueue({
      type: 'critique',
      payload: { post_id: postId, loop },
      dedupeKey: `critique:${postId}:${loop}`,
    });
  },
);
