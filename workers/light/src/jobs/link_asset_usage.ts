import { handler } from '@sfw/queue';
import { db } from '../db.js';

/**
 * Records that a post used its assets.
 *
 * Marks each one `used` and writes a usage row, which is what the library's
 * "used in" list and the Unused view read. Without this the planner would keep
 * proposing the same photo every week.
 *
 * Idempotent: the usage row's primary key is the pair, so re-running does
 * nothing the second time.
 */
export const linkAssetUsage = handler<{ post_id: string }>(async ({ job }) => {
  const pool = db();
  const postId = job.payload.post_id;

  const { rows } = await pool.query<{ asset_ids: string[]; render_id: string | null }>(
    'select asset_ids, render_id from posts where id = $1',
    [postId],
  );

  const post = rows[0];
  if (!post) throw new Error(`No post ${postId}`);

  const ids = post.asset_ids ?? [];
  if (ids.length === 0) {
    console.log(`[link_asset_usage] post ${postId} used no library assets`);
    return;
  }

  const client = await pool.connect();
  try {
    await client.query('begin');

    await client.query(
      `insert into asset_usage (asset_id, post_id)
       select unnest($1::uuid[]), $2
       on conflict (asset_id, post_id) do nothing`,
      [ids, postId],
    );

    // Archived stays archived: someone put it there on purpose.
    await client.query(
      `update assets set status = 'used'
       where id = any($1::uuid[]) and status in ('cleared', 'tagged', 'inbox')`,
      [ids],
    );

    await client.query('commit');
  } catch (err) {
    await client.query('rollback');
    throw err;
  } finally {
    client.release();
  }

  console.log(`[link_asset_usage] ${ids.length} asset(s) marked used by ${postId}`);
});
