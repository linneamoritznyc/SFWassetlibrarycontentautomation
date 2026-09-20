import { handler } from '@sfw/queue';
import { db } from '../db.js';

/**
 * Fans out `write` for everything the planner proposed.
 *
 * Spread over a few minutes rather than fired at once: every one of them makes
 * two or three Claude calls, and a dozen posts starting simultaneously is a
 * rate limit rather than a fast week.
 */
export const writeBatch = handler(async ({ enqueue }) => {
  const { rows } = await db().query<{ id: string }>(
    `select id from posts
     where status = 'proposed' and caption is null
     order by slot_date nulls last, slot_time nulls last`,
  );

  for (const [index, post] of rows.entries()) {
    await enqueue({
      type: 'write',
      payload: { post_id: post.id },
      priority: 4,
      dedupeKey: `write:${post.id}`,
      runAfter: new Date(Date.now() + index * 15_000),
    });
  }

  console.log(`[write_batch] queued ${rows.length} post(s)`);
});
