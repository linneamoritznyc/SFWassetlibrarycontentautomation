import { handler } from '@sfw/queue';
import { db } from '../db.js';

/**
 * Weekly re-read of every source page.
 *
 * It does not fetch anything itself: it queues one `web_fetch` per URL, which
 * already knows how to hash the page, skip it when nothing has changed, and
 * retire the old facts when something has. Keeping the fetching in one job
 * means there is one place where a page turns into facts.
 */
export const webRefresh = handler(async ({ enqueue }) => {
  const pool = db();

  const { rows } = await pool.query<{ ref: string }>(
    `select ref from sources where kind = 'url' order by fetched_at nulls first`,
  );

  for (const [index, source] of rows.entries()) {
    await enqueue({
      type: 'web_fetch',
      payload: { url: source.ref },
      priority: 8,
      dedupeKey: `web_fetch:${source.ref}`,
      // Spread them out: a burst of fetches at one site looks like an attack.
      runAfter: new Date(Date.now() + index * 20_000),
    });
  }

  console.log(`[web_refresh] queued ${rows.length} page(s)`);
});
