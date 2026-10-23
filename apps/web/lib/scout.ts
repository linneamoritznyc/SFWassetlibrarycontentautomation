import { FEEDS, type FeedSeed } from '@sfw/shared';

/**
 * Scout: reads every feed in packages/shared/src/feeds.ts, keeps the stories
 * from the last few days and scores each one for how close it sits to the
 * soil food web. Runs on the server when someone opens the Soil news tab; each
 * feed is cached for a few hours, so opening the tab is cheap.
 */

export type ScoutStory = {
  title: string;
  url: string;
  /** Who published it: the feed, or the outlet a news search found. */
  source: string;
  feed: string;
  region: string;
  published: string | null;
  summary: string;
  score: number;
  /** The words that earned the score, so the reason is visible. */
  matched: string[];
};

export type FeedHealth = {
  feed: string;
  region: string;
  ok: boolean;
  usedFallback: boolean;
  items: number;
  fresh: number;
  error: string | null;
};

const CACHE_SECONDS = 3 * 60 * 60;
const TIMEOUT_MS = 12_000;
// A plain, honest name. Some feeds (Civil Eats) refuse anything posing as a browser.
const UA = 'SoilFoodWebScout/1.0 (+https://soilfoodweb.com)';

/** Words that put a story close to the soil food web, and their weight. */
const TERMS: [RegExp, number, string][] = [
  [/soil food ?web/i, 6, 'soil food web'],
  [/mycorrhiz/i, 5, 'mycorrhizal fungi'],
  [/nematode/i, 5, 'nematodes'],
  [/protozoa|amoeba|ciliate|flagellate/i, 5, 'protozoa'],
  [/earthworm|vermicompost/i, 4, 'earthworms'],
  [/rhizosphere|root exudate/i, 4, 'rhizosphere'],
  [/soil (?:microb|bacteri|fung|biolog|life|organism|biodiversity|microbiome)/i, 5, 'soil life'],
  [/\b(?:microb\w*|microbiome|bacteri\w*|fung(?:i|us|al))\b/i, 2, 'microbes'],
  [/compost/i, 4, 'compost'],
  [/soil health|healthy soil/i, 4, 'soil health'],
  [/soil (?:organic )?carbon|soil organic matter|humus/i, 4, 'soil carbon'],
  [/regenerative|agroecolog|natural farming|permaculture/i, 3, 'regenerative'],
  [/cover crop|no-?till|tillage|mulch/i, 3, 'cover and tillage'],
  [
    /erosion|degraded (?:land|soil)|land degradation|desertification|land restoration/i,
    3,
    'degraded land',
  ],
  [/\bsoils?\b|\bsuelos?\b|\bsolos?\b/i, 2, 'soil'],
  [/fertili[sz]er|nitrogen|phosphorus/i, 1, 'nutrients'],
  [/\bfarm(?:er|ers|ing)?\b|agricultur|\bcrops?\b|harvest/i, 1, 'farming'],
  [/drought|water retention|infiltration/i, 1, 'water'],
];

/** Below this a story is noise for us: a farm story with nothing on soil. */
export const MIN_SCORE = 3;

export function score(text: string): { score: number; matched: string[] } {
  let total = 0;
  const matched: string[] = [];
  for (const [re, weight, label] of TERMS) {
    if (re.test(text)) {
      total += weight;
      matched.push(label);
    }
  }
  return { score: total, matched };
}

const ENTITIES: Record<string, string> = {
  amp: '&',
  lt: '<',
  gt: '>',
  quot: '"',
  apos: "'",
  nbsp: ' ',
  rsquo: '’',
  lsquo: '‘',
  rdquo: '”',
  ldquo: '“',
  ndash: '–',
  mdash: '—',
  hellip: '…',
};

function decode(s: string): string {
  return s.replace(/&(#x[0-9a-f]+|#\d+|\w+);/gi, (m, e: string) => {
    if (e[0] === '#') {
      const n = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return Number.isFinite(n) ? String.fromCodePoint(n) : m;
    }
    return ENTITIES[e.toLowerCase()] ?? m;
  });
}

/** Text of an XML or HTML fragment: CDATA unwrapped, tags and entities gone. */
export function plain(s: string): string {
  const unwrapped = s.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1');
  // Entity-encoded HTML (common in descriptions) is decoded first, then stripped.
  return decode(decode(unwrapped).replace(/<[^>]+>/g, ' '))
    .replace(/\s+/g, ' ')
    .trim();
}

function tag(block: string, names: string[]): string | null {
  for (const name of names) {
    const m = block.match(new RegExp(`<${name}(?:\\s[^>]*)?>([\\s\\S]*?)</${name}>`, 'i'));
    if (m) return m[1]!;
  }
  return null;
}

function when(s: string | null): string | null {
  if (!s) return null;
  const d = new Date(plain(s));
  return Number.isNaN(d.getTime()) ? null : d.toISOString();
}

type Item = {
  title: string;
  url: string;
  source: string | null;
  published: string | null;
  summary: string;
};

/**
 * RSS and Atom items, read with patterns rather than an XML parser so that a
 * feed with one stray character (Down To Earth, Embrapa) still gives its items.
 */
export function parseFeed(xml: string): Item[] {
  const out: Item[] = [];
  for (const m of xml.matchAll(/<(item|entry)(?:\s[^>]*)?>([\s\S]*?)<\/\1>/gi)) {
    const b = m[2]!;
    const href = b.match(/<link\b[^>]*?href=["']([^"']+)["'][^>]*>/i)?.[1];
    const url = plain(href ?? tag(b, ['link', 'guid']) ?? '');
    let title = plain(tag(b, ['title']) ?? '');
    const sourceTag = b.match(/<source\b[^>]*>([\s\S]*?)<\/source>/i)?.[1];
    const source = sourceTag ? plain(sourceTag) : null;
    // Google News titles end in " - Outlet"; the outlet is shown separately.
    if (source && title.endsWith(` - ${source}`)) title = title.slice(0, -(source.length + 3));
    let summary = plain(tag(b, ['description', 'summary', 'content:encoded', 'content']) ?? '');
    if (source && summary.startsWith(title)) summary = '';
    if (!title || !/^https?:\/\//.test(url)) continue;
    out.push({
      title,
      url,
      source,
      published: when(tag(b, ['pubDate', 'published', 'updated', 'dc:date'])),
      summary: summary.slice(0, 600),
    });
  }
  return out;
}

async function read(url: string): Promise<Item[]> {
  const res = await fetch(url, {
    headers: {
      'user-agent': UA,
      accept:
        'application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.5',
    },
    signal: AbortSignal.timeout(TIMEOUT_MS),
    next: { revalidate: CACHE_SECONDS },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const items = parseFeed(await res.text());
  if (items.length === 0) throw new Error('answered, but with no stories in it');
  return items;
}

async function readFeed(feed: FeedSeed): Promise<{ items: Item[]; usedFallback: boolean }> {
  try {
    return { items: await read(feed.url), usedFallback: false };
  } catch (err) {
    if (!feed.fallback) throw err;
    return { items: await read(feed.fallback), usedFallback: true };
  }
}

const key = (title: string) =>
  title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();

/** Every feed at once; stories from the last `days`, best match first. */
export async function scout(days = 14): Promise<{ stories: ScoutStory[]; health: FeedHealth[] }> {
  const cutoff = Date.now() - days * 86_400_000;
  const results = await Promise.allSettled(FEEDS.map(readFeed));
  const seen = new Set<string>();
  const stories: ScoutStory[] = [];
  const health: FeedHealth[] = [];

  results.forEach((r, i) => {
    const feed = FEEDS[i]!;
    if (r.status === 'rejected') {
      const e = r.reason as Error;
      health.push({
        feed: feed.name,
        region: feed.region,
        ok: false,
        usedFallback: false,
        items: 0,
        fresh: 0,
        error:
          e.name === 'TimeoutError' ? 'took too long to answer' : String(e.message).slice(0, 160),
      });
      return;
    }
    let fresh = 0;
    for (const it of r.value.items) {
      if (it.published && Date.parse(it.published) < cutoff) continue;
      const k = key(it.title);
      if (seen.has(it.url) || seen.has(k)) continue;
      seen.add(it.url);
      seen.add(k);
      fresh++;
      const s = score(`${it.title} ${it.summary}`);
      if (s.score < MIN_SCORE) continue;
      stories.push({
        title: it.title,
        url: it.url,
        source: it.source ?? feed.name,
        feed: feed.name,
        region: feed.region,
        published: it.published,
        summary: it.summary,
        ...s,
      });
    }
    health.push({
      feed: feed.name,
      region: feed.region,
      ok: true,
      usedFallback: r.value.usedFallback,
      items: r.value.items.length,
      fresh,
      error: null,
    });
  });

  stories.sort((a, b) => b.score - a.score || (b.published ?? '').localeCompare(a.published ?? ''));
  return { stories, health };
}
