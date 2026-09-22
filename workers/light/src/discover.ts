import { fetchFeed, fetchPage, type Fetcher } from './feed-fetch.js';

/**
 * Goes and finds a feed when the URL we have stops working.
 *
 * Every URL in the seeded source list is the best known URL for that
 * organisation rather than a tested one, and feeds move: a site changes CMS,
 * a newsroom moves under a new path, a `/rss.xml` becomes a `/feed`. Left
 * alone that is a source that quietly stops producing news and a person who
 * has to notice and go hunting.
 *
 * So when a feed answers 404, or answers with a web page, the scout does what
 * a person would do. It opens the site, reads the `<link rel="alternate">`
 * tags that browsers and feed readers have used for autodiscovery since 2002,
 * and failing that tries the handful of paths that nearly every publishing
 * system uses. A candidate only wins if it actually parses into at least one
 * item, so this cannot "fix" a feed into something unreadable.
 *
 * It is deliberately a small number of requests against one host, run only
 * when that host's feed has already broken.
 */

/** Tried in order, on the site root, when the page names no feed itself. */
const CANDIDATE_PATHS = [
  '/feed',
  '/feed/',
  '/rss',
  '/rss.xml',
  '/feed.xml',
  '/atom.xml',
  '/index.xml',
  '/news/feed',
  '/blog/feed',
  '/?feed=rss2',
];

export type Discovery = {
  url: string;
  /** How it was found, for the line a human reads in Settings. */
  how: 'autodiscovery' | 'common path';
  items: number;
};

export async function discoverFeed(
  brokenUrl: string,
  options: { fetchImpl?: Fetcher; timeoutMs?: number } = {},
): Promise<Discovery | null> {
  let origin: string;
  try {
    origin = new URL(brokenUrl).origin;
  } catch {
    return null;
  }

  const tried = new Set([brokenUrl]);

  // 1. Ask the pages most likely to declare a feed, nearest first: the URL we
  //    were given, which is often now an ordinary page, then the section it
  //    sits in, then the site root. A newsroom that moved its feed usually
  //    still declares the new one on the newsroom page, and that is a better
  //    answer than whatever the front page points at.
  for (const pageUrl of pageCandidates(brokenUrl, origin)) {
    const page = await fetchPage(pageUrl, options);
    if (!page.ok) continue;

    for (const href of alternateLinks(page.body, page.url)) {
      if (tried.has(href)) continue;
      tried.add(href);

      const items = await validate(href, options);
      if (items !== null) return { url: href, how: 'autodiscovery', items };
    }
  }

  // 2. Nothing declared. Try what the common publishing systems use.
  for (const path of CANDIDATE_PATHS) {
    const candidate = origin + path;
    if (tried.has(candidate)) continue;
    tried.add(candidate);

    const items = await validate(candidate, options);
    if (items !== null) return { url: candidate, how: 'common path', items };
  }

  return null;
}

/**
 * The pages worth reading for a declared feed, nearest the broken URL first.
 *
 * Walking up the path is what a person does: a feed that was at
 * `/en/newsroom/rss.xml` is most likely declared on `/en/newsroom/`, and only
 * failing that on the front page. Capped so a deep URL cannot turn one broken
 * feed into a dozen requests.
 */
export function pageCandidates(brokenUrl: string, origin: string, maxLevels = 3): string[] {
  const pages = [brokenUrl];

  let url: URL;
  try {
    url = new URL(brokenUrl);
  } catch {
    return pages;
  }

  // '/en/newsroom/rss.xml' -> ['en', 'newsroom']
  const segments = url.pathname.split('/').filter(Boolean).slice(0, -1);

  for (let depth = segments.length; depth > 0 && segments.length - depth < maxLevels; depth -= 1) {
    pages.push(`${origin}/${segments.slice(0, depth).join('/')}/`);
  }

  pages.push(origin);

  return [...new Set(pages)];
}

/** A candidate counts only when it parses into real items. */
async function validate(
  url: string,
  options: { fetchImpl?: Fetcher; timeoutMs?: number },
): Promise<number | null> {
  const outcome = await fetchFeed(url, options);
  return outcome.kind === 'ok' ? outcome.items.length : null;
}

/**
 * Pulls feed URLs out of a page's `<link rel="alternate">` tags.
 *
 * Done with a regex rather than a DOM parser on purpose: this runs against
 * whatever a broken site happened to serve, the tags live in the head, and
 * adding a full HTML parser to the light worker to read one attribute is not
 * worth the dependency. Attribute order varies, so each tag is matched first
 * and then read.
 */
export function alternateLinks(html: string, baseUrl: string): string[] {
  const found: string[] = [];

  // The head is where these live. Stopping there keeps us away from a page
  // full of <a> tags and keeps the regex cheap on a large document.
  const head = html.slice(0, 200_000);

  for (const tag of head.match(/<link\b[^>]*>/gi) ?? []) {
    const rel = attribute(tag, 'rel');
    if (!rel || !/\balternate\b/i.test(rel)) continue;

    const type = attribute(tag, 'type');
    if (!type || !/^application\/(rss|atom)\+xml$/i.test(type.trim())) continue;

    const href = attribute(tag, 'href');
    if (!href) continue;

    try {
      // Feeds are routinely declared relative: href="/feed/".
      const resolved = new URL(decodeEntities(href), baseUrl).toString();
      if (!found.includes(resolved)) found.push(resolved);
    } catch {
      // A malformed href is not worth failing discovery over.
    }
  }

  return found;
}

function attribute(tag: string, name: string): string | null {
  const match = tag.match(new RegExp(`\\b${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s>]+))`, 'i'));
  if (!match) return null;
  return match[2] ?? match[3] ?? match[4] ?? null;
}

function decodeEntities(value: string): string {
  return value.replace(/&amp;/g, '&').replace(/&#38;/g, '&');
}
