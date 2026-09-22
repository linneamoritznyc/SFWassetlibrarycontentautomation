import { FEEDS, type FeedSeed } from '@sfw/shared';
import { discoverFeed, type Discovery } from './discover.js';
import { fetchFeed, fetchPage, isDead, type FetchOutcome } from './feed-fetch.js';

/**
 * Tests every feed in the source list and prints a table.
 *
 * This exists because the feed URLs could not be verified where this was
 * built: the sandbox's egress proxy refuses every host that is not on its
 * allowlist, so nothing could reach them. Rather than claim they work, the
 * check is a command anyone can run from a machine with a normal internet
 * connection:
 *
 *     pnpm feeds:check
 *
 * It touches no database and needs no API key. It uses exactly the code the
 * morning job uses, including the repair, so a URL it reports as fixable is
 * one `scout_fetch` would have fixed by itself. Failing feeds are printed at
 * the end with the replacement to paste into `packages/shared/src/feeds.ts`.
 *
 * It exits 1 when any feed fails and cannot be repaired.
 */

type Result = {
  feed: FeedSeed;
  ok: boolean;
  detail: string;
  ms: number;
  found?: Discovery;
};

async function check(feed: FeedSeed): Promise<Result> {
  const started = Date.now();
  const since = () => Date.now() - started;

  // A `page` feed has no RSS to parse. The only thing worth asserting is that
  // something came back that looks like a document, because that is all
  // web_fetch needs from it.
  if (feed.kind !== 'rss') {
    const page = await fetchPage(feed.url);
    if (!page.ok) return { feed, ok: false, detail: page.detail, ms: since() };

    const ok = page.body.length > 500;
    return {
      feed,
      ok,
      detail: ok ? `page, ${Math.round(page.body.length / 1024)}kb` : 'page, almost empty',
      ms: since(),
    };
  }

  const outcome = await fetchFeed(feed.url);

  if (outcome.kind === 'ok') {
    return { feed, ok: true, detail: describe(outcome), ms: since() };
  }

  // This check never sends validators, so a feed has no way to answer 304.
  // Handled rather than cast away, so that if it ever does start sending them
  // the report says something true instead of crashing.
  if (outcome.kind === 'unchanged') {
    return { feed, ok: true, detail: 'unchanged since the last check', ms: since() };
  }

  // Same repair the morning job would attempt, so this report says what the
  // scout would actually do rather than only that something is broken.
  if (isDead(outcome.kind)) {
    const found = await discoverFeed(feed.url);
    if (found) {
      return {
        feed,
        ok: true,
        detail: `${outcome.detail} -> found at ${found.url} by ${found.how}, ${found.items} items`,
        ms: since(),
        found,
      };
    }
  }

  return { feed, ok: false, detail: `${outcome.kind}: ${outcome.detail}`, ms: since() };
}

function describe(outcome: Extract<FetchOutcome, { kind: 'ok' }>): string {
  const newest = outcome.items
    .map((i) => i.publishedAt)
    .filter((d): d is Date => d instanceof Date)
    .sort((a, b) => b.getTime() - a.getTime())[0];

  return `${outcome.items.length} items${newest ? `, newest ${newest.toISOString().slice(0, 10)}` : ''}`;
}

function pad(value: string, width: number): string {
  return value.length >= width ? value.slice(0, width) : value + ' '.repeat(width - value.length);
}

async function main(): Promise<void> {
  console.log(`Checking ${FEEDS.length} feeds. This takes about a minute.\n`);

  // Six at a time: polite to the smaller institutional sites, and still fast
  // enough that nobody walks away from it.
  const results: Result[] = [];
  for (let i = 0; i < FEEDS.length; i += 6) {
    results.push(...(await Promise.all(FEEDS.slice(i, i + 6).map(check))));
  }

  const nameWidth = Math.max(...results.map((r) => r.feed.name.length));

  for (const region of [...new Set(results.map((r) => r.feed.region))]) {
    console.log(region);
    for (const r of results.filter((x) => x.feed.region === region)) {
      const mark = r.found ? 'MOVED' : r.ok ? 'ok   ' : 'FAIL ';
      console.log(`  ${mark} ${pad(r.feed.name, nameWidth)}  ${pad(`${r.ms}ms`, 7)} ${r.detail}`);
    }
    console.log('');
  }

  const moved = results.filter((r) => r.found);
  const failed = results.filter((r) => !r.ok);

  console.log(`${results.length - failed.length} of ${results.length} feeds working.`);

  if (moved.length > 0) {
    console.log(
      `\n${moved.length} moved. The scout repairs these by itself on the next run; ` +
        'paste them into packages/shared/src/feeds.ts to fix the seed too:',
    );
    for (const r of moved) console.log(`  ${r.feed.name}\n    url: '${r.found!.url}',`);
  }

  if (failed.length > 0) {
    console.log('\nFailing, and nothing found to replace them:');
    for (const r of failed) console.log(`  ${r.feed.name}\n    ${r.feed.url}\n    ${r.detail}`);
    process.exitCode = 1;
  }
}

void main();
