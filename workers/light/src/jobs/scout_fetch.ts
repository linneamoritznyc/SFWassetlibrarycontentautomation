import { handler } from '@sfw/queue';
import { db } from '../db.js';
import { parseFeed } from '../rss.js';

/** Nothing older than this is worth reacting to. */
const MAX_AGE_DAYS = 14;

/** After this many failures in a row, stop asking. */
const GIVE_UP_AFTER = 5;

/**
 * Pulls every active feed and stores what is new.
 *
 * A feed that fails is recorded and skipped, never thrown: one dead URL out of
 * twenty-seven should not stop the other twenty-six. The failure is counted on
 * the feed row, and after five in a row the feed switches itself off, because
 * a URL that has been dead for a week will still be dead tomorrow and the
 * Settings screen is where someone decides what to replace it with.
 *
 * A feed that answers but parses to nothing counts as a failure too. A page
 * that returns 200 and a cookie banner is the most common way a feed dies.
 */
export const scoutFetch = handler(async ({ enqueue }) => {
  const pool = db();

  const { rows: feeds } = await pool.query<{
    id: number;
    name: string;
    url: string;
    kind: string;
    consecutive_failures: number;
  }>(
    `select id, name, url, kind, consecutive_failures
     from feeds where active order by name`,
  );

  let added = 0;
  const failures: string[] = [];
  const switchedOff: string[] = [];

  for (const feed of feeds) {
    try {
      // A `page` feed has no RSS. It is read as a source page instead, which
      // turns it into facts rather than news cards, and is the right answer
      // for the ones that publish a highlights list and nothing machine
      // readable.
      if (feed.kind !== 'rss') {
        await enqueue({
          type: 'web_fetch',
          payload: { url: feed.url },
          priority: 8,
          dedupeKey: `web_fetch:${feed.url}`,
        });
        await recordOk(feed.id);
        continue;
      }

      const res = await fetch(feed.url, {
        headers: {
          'user-agent': 'SFWContentStudio/0.1 (+https://soilfoodweb.com)',
          // Some feeds serve HTML unless asked for XML.
          accept:
            'application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.5',
        },
        redirect: 'follow',
        signal: AbortSignal.timeout(20_000),
      });

      if (!res.ok) {
        await recordFailure(feed, `HTTP ${res.status}`);
        failures.push(`${feed.name} (${res.status})`);
        continue;
      }

      const items = parseFeed(await res.text());

      if (items.length === 0) {
        // 200 and nothing usable: a redirect to a landing page, a cookie
        // wall, or a feed that moved. Worth reporting as a failure.
        await recordFailure(feed, 'answered, but no items could be parsed');
        failures.push(`${feed.name} (no items)`);
        continue;
      }

      const cutoff = Date.now() - MAX_AGE_DAYS * 86_400_000;
      let fromThisFeed = 0;

      for (const item of items) {
        if (item.publishedAt && item.publishedAt.getTime() < cutoff) continue;

        const inserted = await pool.query<{ id: number }>(
          `insert into news_items (feed_id, url, title, published_at, summary, status)
           values ($1, $2, $3, $4, $5, 'new')
           on conflict (url) do nothing
           returning id`,
          [feed.id, item.url, item.title, item.publishedAt, item.summary],
        );

        if (inserted.rows[0]) fromThisFeed += 1;
      }

      added += fromThisFeed;
      await recordOk(feed.id);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'failed';
      await recordFailure(feed, message);
      failures.push(`${feed.name} (${message})`);
    }
  }

  if (failures.length > 0) {
    console.warn(`[scout_fetch] ${failures.length} feed(s) failed: ${failures.join('; ')}`);
  }
  if (switchedOff.length > 0) {
    console.warn(
      `[scout_fetch] switched off after ${GIVE_UP_AFTER} failures each: ${switchedOff.join(', ')}. ` +
        'Replace or re-enable them in Settings.',
    );
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

  async function recordOk(feedId: number): Promise<void> {
    await pool.query(
      `update feeds
       set last_ok_at = now(), last_checked_at = now(),
           last_error = null, consecutive_failures = 0
       where id = $1`,
      [feedId],
    );
  }

  async function recordFailure(
    feed: { id: number; name: string; consecutive_failures: number },
    reason: string,
  ): Promise<void> {
    const failures = feed.consecutive_failures + 1;
    const disable = failures >= GIVE_UP_AFTER;

    await pool.query(
      `update feeds
       set last_checked_at = now(),
           last_error = $2,
           consecutive_failures = $3,
           active = case when $4 then false else active end
       where id = $1`,
      [feed.id, reason.slice(0, 500), failures, disable],
    );

    if (disable) switchedOff.push(feed.name);
  }
});
