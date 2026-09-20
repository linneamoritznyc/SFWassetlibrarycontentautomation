import { handler } from '@sfw/queue';
import { db } from '../db.js';

type Insight = { name: string; values?: { value: number }[] };

/**
 * Pulls last week's numbers onto each post.
 *
 * Instagram's Graph API when both tokens are set, and nothing otherwise: the
 * CSV import screen is the other route, and it is not this job's business. A
 * missing token is logged, not thrown, because a Monday that fails on a
 * missing token would also stop the planner behind it.
 *
 * One row per pull rather than an update, so the history is kept and a post
 * that kept gaining saves for a fortnight can be seen doing it.
 */
export const resultsPull = handler(async () => {
  const pool = db();

  const token = process.env.IG_ACCESS_TOKEN;
  const account = process.env.IG_BUSINESS_ACCOUNT_ID;

  if (!token || !account) {
    console.log(
      '[results_pull] IG_ACCESS_TOKEN or IG_BUSINESS_ACCOUNT_ID is not set. ' +
        'Import a Later CSV from the Settings view instead.',
    );
    return;
  }

  const { rows } = await pool.query<{ id: string; published_url: string | null }>(
    `select id, published_url from posts
     where status = 'published' and published_url is not null
       and published_at > now() - interval '60 days'`,
  );

  let updated = 0;

  for (const post of rows) {
    const mediaId = mediaIdFrom(post.published_url!);
    if (!mediaId) continue;

    const url = new URL(`https://graph.facebook.com/v21.0/${mediaId}/insights`);
    url.searchParams.set('metric', 'reach,likes,comments,saved,shares,total_interactions');
    url.searchParams.set('access_token', token);

    const res = await fetch(url);
    if (!res.ok) {
      console.warn(`[results_pull] ${post.id}: Instagram said ${res.status}`);
      continue;
    }

    const body = (await res.json()) as { data?: Insight[] };
    const value = (name: string) =>
      body.data?.find((d) => d.name === name)?.values?.[0]?.value ?? null;

    await pool.query(
      `insert into metrics (post_id, captured_at, reach, likes, comments, saves, shares)
       values ($1, now(), $2, $3, $4, $5, $6)`,
      [post.id, value('reach'), value('likes'), value('comments'), value('saved'), value('shares')],
    );
    updated += 1;
  }

  console.log(`[results_pull] ${updated} post(s) updated from Instagram`);
});

/** The shortcode out of an Instagram permalink. */
export function mediaIdFrom(url: string): string | null {
  const match = /instagram\.com\/(?:p|reel|tv)\/([A-Za-z0-9_-]+)/.exec(url);
  return match?.[1] ?? null;
}
