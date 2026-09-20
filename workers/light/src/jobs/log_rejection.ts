import { handler } from '@sfw/queue';
import { db } from '../db.js';

/**
 * Stores why a post was turned down, with enough of the post to see the
 * pattern later.
 *
 * A reason code on its own says nothing: "off brand" across twenty posts is
 * only useful if you can see what the twenty had in common. So the caption,
 * the pillar, the format and what the critic had said are kept alongside it.
 */
export const logRejection = handler<{ post_id: string; reason: string }>(async ({ job }) => {
  const pool = db();
  const { post_id: postId, reason } = job.payload;

  const { rows } = await pool.query<{
    hook: string | null;
    caption: string | null;
    platform: string;
    format: string;
    critic_score: number | null;
    critic_notes: unknown;
    pillar: string | null;
    asset_ids: string[];
  }>(
    `select p.hook, p.caption, p.platform, p.format, p.critic_score, p.critic_notes,
            s.pillar, p.asset_ids
     from posts p left join stories s on s.id = p.story_id
     where p.id = $1`,
    [postId],
  );

  const post = rows[0];
  if (!post) throw new Error(`No post ${postId}`);

  const version = await pool.query<{ next: number }>(
    'select coalesce(max(version), 0) + 1 as next from post_versions where post_id = $1',
    [postId],
  );

  // Kept as a version row with a diff, so learn_weekly reads edits and
  // rejections from one place.
  await pool.query(
    `insert into post_versions (post_id, version, author, caption, hook, diff)
     values ($1, $2, 'human', $3, $4, $5::jsonb)`,
    [
      postId,
      version.rows[0]!.next,
      post.caption,
      post.hook,
      JSON.stringify({
        rejected: true,
        reason,
        platform: post.platform,
        format: post.format,
        pillar: post.pillar,
        critic_score: post.critic_score,
        critic_notes: post.critic_notes,
        had_assets: post.asset_ids.length,
      }),
    ],
  );

  // The story goes back in the pool rather than dying with the post: the angle
  // may have been fine and the execution wrong.
  await pool.query(
    `update stories set status = 'candidate'
     where id = (select story_id from posts where id = $1) and status = 'planned'`,
    [postId],
  );

  console.log(`[log_rejection] ${postId} rejected as ${reason}`);
});
