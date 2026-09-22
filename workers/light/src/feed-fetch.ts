import { parseFeed, type FeedItem } from './rss.js';

/**
 * One place that knows how to ask a website for a feed.
 *
 * `scout_fetch` and `pnpm feeds:check` both need this and used to carry their
 * own copy, which meant the morning job and the thing you run to debug the
 * morning job could disagree about what "working" means.
 *
 * The important part is the classification. A feed can fail in four quite
 * different ways and the right response to each one is different:
 *
 * - `moved`   the URL is wrong or the feed has gone. Worth going to look for
 *             the new one, and worth giving up on eventually.
 * - `empty`   200, but nothing parsed out of it. Usually a cookie wall or a
 *             redirect to a landing page, so it is treated like `moved`.
 * - `blocked` 401, 403, 429. The feed is almost certainly fine and something
 *             in front of it does not like us. Retrying tomorrow will not
 *             help and neither will switching the source off; a person has to
 *             decide what to do.
 * - `transient` 5xx, a timeout, a reset. The internet being the internet.
 *
 * Treating all four as "a failure" is what the first version did, and it meant
 * a partner site behind Cloudflare and a site down for maintenance both
 * quietly disappeared from the source list after five mornings.
 */

export const USER_AGENT = 'SFWContentStudio/0.1 (+https://soilfoodweb.com)';

export const FEED_ACCEPT =
  'application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.5';

export const PAGE_ACCEPT = 'text/html, application/xhtml+xml, */*;q=0.5';

export const TIMEOUT_MS = 20_000;

export type FetchOutcome =
  | { kind: 'ok'; items: FeedItem[]; etag: string | null; lastModified: string | null }
  /** 304. The feed has not published anything since we last asked. */
  | { kind: 'unchanged' }
  | { kind: 'moved'; detail: string }
  | { kind: 'empty'; detail: string }
  | { kind: 'blocked'; detail: string }
  | { kind: 'transient'; detail: string };

/** The kinds that mean the URL itself is probably wrong. */
export function isDead(kind: FetchOutcome['kind']): boolean {
  return kind === 'moved' || kind === 'empty';
}

export type Conditional = {
  etag?: string | null;
  lastModified?: string | null;
};

export type Fetcher = typeof fetch;

/**
 * Fetches one feed URL and says what came back.
 *
 * `conditional` carries the validators the feed gave us last time. Sending
 * them back turns an unchanged feed into a 304 with no body, which is faster
 * for us and considerably politer to a small institutional server we are
 * hitting every morning.
 */
export async function fetchFeed(
  url: string,
  options: { conditional?: Conditional; fetchImpl?: Fetcher; timeoutMs?: number } = {},
): Promise<FetchOutcome> {
  const doFetch = options.fetchImpl ?? fetch;

  const headers: Record<string, string> = {
    'user-agent': USER_AGENT,
    accept: FEED_ACCEPT,
    // Institutional sites often sit behind a CDN that serves a compressed
    // variant only when asked. undici decompresses it for us.
    'accept-encoding': 'gzip, deflate',
  };

  if (options.conditional?.etag) headers['if-none-match'] = options.conditional.etag;
  if (options.conditional?.lastModified) {
    headers['if-modified-since'] = options.conditional.lastModified;
  }

  let res: Response;
  try {
    res = await doFetch(url, {
      headers,
      redirect: 'follow',
      signal: AbortSignal.timeout(options.timeoutMs ?? TIMEOUT_MS),
    });
  } catch (err) {
    // A timeout, a DNS failure, a reset mid-body. None of these say anything
    // about whether the URL is right.
    return { kind: 'transient', detail: reason(err) };
  }

  if (res.status === 304) return { kind: 'unchanged' };

  if (res.status === 404 || res.status === 410) {
    return { kind: 'moved', detail: `HTTP ${res.status}` };
  }

  if (res.status === 401 || res.status === 403 || res.status === 429) {
    return {
      kind: 'blocked',
      detail:
        res.status === 429
          ? 'HTTP 429, rate limited'
          : `HTTP ${res.status}, blocked before the feed (bot protection or a login)`,
    };
  }

  if (!res.ok) {
    return { kind: 'transient', detail: `HTTP ${res.status}` };
  }

  let body: string;
  try {
    body = await res.text();
  } catch (err) {
    return { kind: 'transient', detail: reason(err) };
  }

  const items = parseFeed(body);

  if (items.length === 0) {
    // Saying which of the two happened matters: HTML at a feed URL means go
    // and look for the real one, while XML that parsed to nothing means the
    // feed is real and we cannot read it, which is a different bug.
    return looksLikeHtml(body)
      ? { kind: 'moved', detail: 'answered with a web page, not a feed' }
      : { kind: 'empty', detail: 'answered, but no items could be parsed' };
  }

  return {
    kind: 'ok',
    items,
    etag: res.headers.get('etag'),
    lastModified: res.headers.get('last-modified'),
  };
}

/** Fetches something we expect to be a web page, for discovery. */
export async function fetchPage(
  url: string,
  options: { fetchImpl?: Fetcher; timeoutMs?: number } = {},
): Promise<{ ok: true; body: string; url: string } | { ok: false; detail: string }> {
  const doFetch = options.fetchImpl ?? fetch;

  try {
    const res = await doFetch(url, {
      headers: { 'user-agent': USER_AGENT, accept: PAGE_ACCEPT },
      redirect: 'follow',
      signal: AbortSignal.timeout(options.timeoutMs ?? TIMEOUT_MS),
    });
    if (!res.ok) return { ok: false, detail: `HTTP ${res.status}` };
    return { ok: true, body: await res.text(), url: res.url || url };
  } catch (err) {
    return { ok: false, detail: reason(err) };
  }
}

function looksLikeHtml(body: string): boolean {
  const head = body.slice(0, 2000).toLowerCase();
  return head.includes('<!doctype html') || head.includes('<html');
}

function reason(err: unknown): string {
  if (err instanceof Error) {
    // AbortSignal.timeout throws a TimeoutError whose message is unhelpfully
    // "The operation was aborted due to timeout".
    if (err.name === 'TimeoutError') return 'timed out';
    return err.message;
  }
  return 'failed';
}
