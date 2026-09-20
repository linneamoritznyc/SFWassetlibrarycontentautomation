import { handler } from '@sfw/queue';
import { db } from '../db.js';
import { parseFeed } from '../rss.js';

/** Nothing older than this is worth reacting to. */
const MAX_AGE_DAYS = 14;

/**
 * Pulls every active feed and stores what is new.
 *
 * A feed that fails is reported and skipped, not thrown: one dead URL out of
 * fourteen should not stop the other thirteen. Items are deduped by URL, which
 * is the table's unique key, so re-running mid-morning costs nothing.
 */
export const scoutFetch = handler(async ({ enqueue }) => {
  const pool = db();

  const { rows: feeds } = await pool.query<{ id: number; name: string; url: string; kind: string }>(
    `select id, name, url, kind from feeds where active order by name`,
  );

  let added = 0;
  const failures: string[] = [];

  for (const feed of feeds) {
    try {
      // `page` feeds have no RSS. Until someone writes a scraper for one, it
      // is read as a source page by web_fetch instead.
      if (feed.kind !== 'rss') {
        await enqueue({
          type: 'web_fetch',
          payload: { url: feed.url },
          priority: 8,
          dedupeKey: `web_fetch:${feed.url}`,
        });
        continue;
      }

      const res = await fetch(feed.url, {
        headers: { 'user-agent': 'SFWContentStudio/0.1 (+https://soilfoodweb.com)' },
        signal: AbortSignal.timeout(20_000),
      });

      if (!res.ok) {
        failures.push(`${feed.name} (${res.status})`);
        continue;
      }

      const items = parseFeed(await res.text());
      const cutoff = Date.now() - MAX_AGE_DAYS * 86_400_000;

      for (const item of items) {
        if (item.publishedAt && item.publishedAt.getTime() < cutoff) continue;

        const inserted = await pool.query<{ id: number }>(
          `insert into news_items (feed_id, url, title, published_at, summary, status)
           values ($1, $2, $3, $4, $5, 'new')
           on conflict (url) do nothing
           returning id`,
          [feed.id, item.url, item.title, item.publishedAt, item.summary],
        );

        if (inserted.rows[0]) added += 1;
      }
    } catch (err) {
      failures.push(`${feed.name} (${err instanceof Error ? err.message : 'failed'})`);
    }
  }

  if (failures.length > 0) {
    console.warn(`[scout_fetch] ${failures.length} feed(s) failed: ${failures.join('; ')}`);
  }
  console.log(`[scout_fetch] ${added} new item(s) from ${feeds.length} feed(s)`);

  if (added > 0) {
    await enqueue({
      type: 'scout_rank',
      payload: {},
      priority: 7,
      dedupeKey: `scout_rank:${new Date().toISOString().slice(0, 10)}`,
    });
  }
});
