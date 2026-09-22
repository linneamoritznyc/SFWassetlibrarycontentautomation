import { handler } from '@sfw/queue';
import { db } from '../db.js';
import { discoverFeed } from '../discover.js';
import { fetchFeed, isDead, type FetchOutcome } from '../feed-fetch.js';
import type { FeedItem } from '../rss.js';

/** Nothing older than this is worth reacting to. */
const MAX_AGE_DAYS = 14;

/** After this many dead mornings in a row, stop asking. */
const GIVE_UP_AFTER = 5;

/** Feeds fetched at once. Enough to finish quickly, few enough to be polite. */
const CONCURRENCY = 6;

type FeedRow = {
  id: number;
  name: string;
  url: string;
  kind: string;
  consecutive_failures: number;
  etag: string | null;
  last_modified: string | null;
};

/**
 * Pulls every active feed and stores what is new.
 *
 * A feed that fails is recorded and skipped, never thrown: one dead URL out of
 * twenty-seven should not stop the other twenty-six.
 *
 * What happens next depends on how it failed. A feed that 404s or hands back a
 * web page has moved, so the scout goes and looks for it: the site's
 * autodiscovery tags first, then the usual feed paths, and if something there
 * parses into real items the feed's URL is repaired on the spot and the old
 * one kept beside it. Only a feed that is dead and cannot be found again gets
 * switched off, after five mornings. A feed behind bot protection, or one
 * whose server is having a bad week, stays in the list and stays visible in
 * Settings, because switching it off would lose the source and fix nothing.
 */
export const scoutFetch = handler(async ({ enqueue }) => {
  const pool = db();

  const { rows: feeds } = await pool.query<FeedRow>(
    `select id, name, url, kind, consecutive_failures, etag, last_modified
     from feeds where active order by name`,
  );

  let added = 0;
  let unchanged = 0;
  const failures: string[] = [];
  const repaired: string[] = [];
  const switchedOff: string[] = [];

  // Feeds are independent, so they go in small batches rather than one after
  // another: twenty-seven sequential fetches that each wait twenty seconds for
  // a dead host is nine minutes of a worker doing nothing.
  for (let i = 0; i < feeds.length; i += CONCURRENCY) {
    await Promise.all(feeds.slice(i, i + CONCURRENCY).map(runFeed));
  }

  if (repaired.length > 0) {
    console.log(`[scout_fetch] repaired ${repaired.length} feed URL(s): ${repaired.join('; ')}`);
  }
  if (failures.length > 0) {
    console.warn(`[scout_fetch] ${failures.length} feed(s) failed: ${failures.join('; ')}`);
  }
  if (switchedOff.length > 0) {
    console.warn(
      `[scout_fetch] switched off after ${GIVE_UP_AFTER} dead mornings each: ` +
        `${switchedOff.join(', ')}. Replace or re-enable them in Settings.`,
    );
  }
  console.log(
    `[scout_fetch] ${added} new item(s) from ${feeds.length} feed(s)` +
      (unchanged > 0 ? `, ${unchanged} unchanged` : ''),
  );

  if (added > 0) {
    await enqueue({
      type: 'scout_rank',
      payload: {},
      priority: 7,
      dedupeKey: `scout_rank:${new Date().toISOString().slice(0, 10)}`,
    });
  }

  async function runFeed(feed: FeedRow): Promise<void> {
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
        await recordOk(feed.id, null, null);
        return;
      }

      let outcome = await fetchFeed(feed.url, {
        conditional: { etag: feed.etag, lastModified: feed.last_modified },
      });

      // The URL looks wrong. Go and find where the feed went.
      if (isDead(outcome.kind)) {
        const found = await discoverFeed(feed.url);

        if (found) {
          await pool.query(
            `update feeds
             set previous_url = url, url = $2, url_fixed_at = now()
             where id = $1`,
            [feed.id, found.url],
          );
          repaired.push(`${feed.name} -> ${found.url} (${found.how})`);
          // The validated candidate is re-fetched rather than reused, so this
          // run stores items under the same code path as every other feed.
          outcome = await fetchFeed(found.url);
          feed.url = found.url;
        }
      }

      if (outcome.kind === 'unchanged') {
        unchanged += 1;
        await recordOk(feed.id, feed.etag, feed.last_modified);
        return;
      }

      if (outcome.kind !== 'ok') {
        await recordFailure(feed, outcome);
        failures.push(`${feed.name} (${outcome.detail})`);
        return;
      }

      // Read into a local first. `added += await store(...)` would capture
      // `added` before the await resolved, and with six feeds in flight two
      // finishing together would lose an increment.
      const stored = await store(feed.id, outcome.items);
      added += stored;

      await recordOk(feed.id, outcome.etag, outcome.lastModified);
    } catch (err) {
      // Anything unexpected is the worker's problem, not the feed's, so it is
      // recorded as transient and never counts towards switching a feed off.
      const message = err instanceof Error ? err.message : 'failed';
      await recordFailure(feed, { kind: 'transient', detail: message });
      failures.push(`${feed.name} (${message})`);
    }
  }

  async function store(feedId: number, items: FeedItem[]): Promise<number> {
    const cutoff = Date.now() - MAX_AGE_DAYS * 86_400_000;
    let stored = 0;

    for (const item of items) {
      if (item.publishedAt && item.publishedAt.getTime() < cutoff) continue;

      const inserted = await pool.query<{ id: number }>(
        `insert into news_items (feed_id, url, title, published_at, summary, status)
         values ($1, $2, $3, $4, $5, 'new')
         on conflict (url) do nothing
         returning id`,
        [feedId, item.url, item.title, item.publishedAt, item.summary],
      );

      if (inserted.rows[0]) stored += 1;
    }

    return stored;
  }

  async function recordOk(
    feedId: number,
    etag: string | null,
    lastModified: string | null,
  ): Promise<void> {
    await pool.query(
      `update feeds
       set last_ok_at = now(), last_checked_at = now(),
           last_error = null, failure_kind = null, consecutive_failures = 0,
           etag = $2, last_modified = $3
       where id = $1`,
      [feedId, etag, lastModified],
    );
  }

  async function recordFailure(
    feed: { id: number; name: string; consecutive_failures: number },
    outcome: Exclude<FetchOutcome, { kind: 'ok' } | { kind: 'unchanged' }>,
  ): Promise<void> {
    const failures = feed.consecutive_failures + 1;

    // Only a feed whose URL is dead, and which could not be found anywhere
    // else, is worth giving up on. Bot protection and a flaky server are both
    // things a person has to look at, and a switched-off feed is one nobody
    // looks at.
    const disable = isDead(outcome.kind) && failures >= GIVE_UP_AFTER;

    await pool.query(
      `update feeds
       set last_checked_at = now(),
           last_error = $2,
           failure_kind = $3,
           consecutive_failures = $4,
           active = case when $5 then false else active end
       where id = $1`,
      [feed.id, outcome.detail.slice(0, 500), outcome.kind, failures, disable],
    );

    if (disable) switchedOff.push(feed.name);
  }
});
