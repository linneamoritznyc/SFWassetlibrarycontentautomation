import { FEEDS, type FeedSeed } from '@sfw/shared';
import { parseFeed } from './rss.js';

/**
 * Tests every feed in the source list and prints a table.
 *
 * This exists because the feed URLs could not be verified where this was
 * built: the sandbox's egress proxy refuses every host that is not on its
 * allowlist, so `curl` returned nothing for all of them. Rather than claim
 * they work, the check is a command anyone can run from a machine with a
 * normal internet connection:
 *
 *     pnpm feeds:check
 *
 * It touches no database and needs no API key. It exits 1 when any feed fails,
 * so it can be a scheduled job later if that turns out to be useful.
 */

type Result = {
  feed: FeedSeed;
  ok: boolean;
  detail: string;
  ms: number;
};

const TIMEOUT_MS = 20_000;

async function check(feed: FeedSeed): Promise<Result> {
  const started = Date.now();

  try {
    const res = await fetch(feed.url, {
      headers: {
        'user-agent': 'SFWContentStudio/0.1 (+https://soilfoodweb.com)',
        accept:
          feed.kind === 'rss'
            ? 'application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.5'
            : 'text/html, */*;q=0.5',
      },
      redirect: 'follow',
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });

    const ms = Date.now() - started;

    if (!res.ok) {
      return { feed, ok: false, detail: `HTTP ${res.status}`, ms };
    }

    const body = await res.text();

    // A `page` feed has no RSS to parse. The only thing worth asserting is
    // that something came back that looks like a document, because that is
    // all web_fetch needs from it.
    if (feed.kind !== 'rss') {
      const ok = body.length > 500;
      return {
        feed,
        ok,
        detail: ok ? `page, ${Math.round(body.length / 1024)}kb` : 'page, almost empty',
        ms,
      };
    }

    const items = parseFeed(body);

    if (items.length === 0) {
      return { feed, ok: false, detail: 'answered, but no items could be parsed', ms };
    }

    const newest = items
      .map((i) => i.publishedAt)
      .filter((d): d is Date => d instanceof Date)
      .sort((a, b) => b.getTime() - a.getTime())[0];

    return {
      feed,
      ok: true,
      detail: `${items.length} items${newest ? `, newest ${newest.toISOString().slice(0, 10)}` : ''}`,
      ms,
    };
  } catch (err) {
    return {
      feed,
      ok: false,
      detail: err instanceof Error ? err.message : 'failed',
      ms: Date.now() - started,
    };
  }
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
      console.log(
        `  ${r.ok ? 'ok  ' : 'FAIL'} ${pad(r.feed.name, nameWidth)}  ${pad(`${r.ms}ms`, 7)} ${r.detail}`,
      );
    }
    console.log('');
  }

  const failed = results.filter((r) => !r.ok);
  console.log(`${results.length - failed.length} of ${results.length} feeds working.`);

  if (failed.length > 0) {
    console.log('\nFailing URLs, to fix in packages/shared/src/feeds.ts:');
    for (const r of failed) console.log(`  ${r.feed.name}\n    ${r.feed.url}\n    ${r.detail}`);
    process.exitCode = 1;
  }
}

void main();
