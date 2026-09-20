import { XMLParser } from 'fast-xml-parser';

export type FeedItem = {
  url: string;
  title: string;
  publishedAt: Date | null;
  summary: string | null;
};

/**
 * Reads RSS and Atom without caring which it got.
 *
 * Real feeds are inconsistent: dates in three formats, summaries under four
 * different tag names, links as attributes in Atom and as text in RSS. All of
 * that is normalised here so `scout_fetch` only deals with items.
 */
const parser = new XMLParser({
  ignoreAttributes: false,
  attributeNamePrefix: '@',
  textNodeName: '#text',
  trimValues: true,
});

export function parseFeed(xml: string): FeedItem[] {
  const doc = parser.parse(xml) as Record<string, unknown>;

  const rss = get(doc, ['rss', 'channel', 'item']);
  const atom = get(doc, ['feed', 'entry']);
  const rdf = get(doc, ['rdf:RDF', 'item']);

  const raw = toArray(rss ?? atom ?? rdf);

  return raw.map(toItem).filter((item): item is FeedItem => item !== null);
}

function toItem(entry: unknown): FeedItem | null {
  if (typeof entry !== 'object' || entry === null) return null;
  const record = entry as Record<string, unknown>;

  const url = linkOf(record);
  if (!url) return null;

  const title = text(record.title) ?? '(untitled)';
  const summary =
    text(record.description) ??
    text(record.summary) ??
    text(record['content:encoded']) ??
    text(record.content) ??
    null;

  const published =
    date(record.pubDate) ??
    date(record.published) ??
    date(record.updated) ??
    date(record['dc:date']);

  return {
    url,
    title: stripTags(title).slice(0, 500),
    publishedAt: published,
    // Feeds put whole articles in here. The ranker only needs the gist.
    summary: summary ? stripTags(summary).slice(0, 2000) : null,
  };
}

/** RSS puts the URL in the text; Atom puts it in an href attribute. */
function linkOf(record: Record<string, unknown>): string | null {
  const direct = text(record.link);
  if (direct?.startsWith('http')) return direct;

  const link = record.link;
  if (Array.isArray(link)) {
    for (const candidate of link) {
      const href = (candidate as Record<string, unknown>)?.['@href'];
      if (typeof href === 'string' && href.startsWith('http')) return href;
    }
  } else if (typeof link === 'object' && link !== null) {
    const href = (link as Record<string, unknown>)['@href'];
    if (typeof href === 'string') return href;
  }

  const guid = text(record.guid);
  return guid?.startsWith('http') ? guid : null;
}

function text(value: unknown): string | null {
  if (typeof value === 'string') return value.trim() || null;
  if (typeof value === 'number') return String(value);
  if (typeof value === 'object' && value !== null) {
    const inner = (value as Record<string, unknown>)['#text'];
    if (typeof inner === 'string') return inner.trim() || null;
  }
  return null;
}

function date(value: unknown): Date | null {
  const raw = text(value);
  if (!raw) return null;
  const parsed = new Date(raw);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function toArray(value: unknown): unknown[] {
  if (Array.isArray(value)) return value;
  return value === undefined || value === null ? [] : [value];
}

function get(source: Record<string, unknown>, path: string[]): unknown {
  let current: unknown = source;
  for (const key of path) {
    if (typeof current !== 'object' || current === null) return undefined;
    current = (current as Record<string, unknown>)[key];
  }
  return current;
}

/** Feed summaries are full of HTML. The ranker wants the words. */
export function stripTags(html: string): string {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}
