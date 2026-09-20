import { describe, expect, it } from 'vitest';
import { parseFeed, stripTags } from './rss.js';

/**
 * Real feeds are inconsistent, so the fixtures here are the shapes actually
 * seen in the wild: RSS 2.0, Atom with the link in an attribute, RDF, and RSS
 * with the summary in `content:encoded` and HTML inside it.
 */

const rss2 = `<?xml version="1.0"?>
<rss version="2.0"><channel>
  <title>ScienceDaily: Soil</title>
  <item>
    <title>Fungal networks move nitrogen further than thought</title>
    <link>https://example.org/fungal-networks</link>
    <description>&lt;p&gt;Researchers found &lt;b&gt;mycorrhizal&lt;/b&gt; networks moving nitrogen.&lt;/p&gt;</description>
    <pubDate>Fri, 18 Sep 2026 09:00:00 GMT</pubDate>
  </item>
  <item>
    <title>Second item</title>
    <link>https://example.org/second</link>
    <pubDate>Thu, 17 Sep 2026 09:00:00 GMT</pubDate>
  </item>
</channel></rss>`;

const atom = `<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>EU soil monitoring law clears committee</title>
    <link rel="alternate" href="https://example.org/eu-soil-law"/>
    <summary>A summary of the vote.</summary>
    <updated>2026-09-19T11:30:00Z</updated>
  </entry>
</feed>`;

const rdf = `<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <item>
    <title>Old school feed</title>
    <link>https://example.org/rdf-item</link>
    <dc:date>2026-09-15T08:00:00Z</dc:date>
  </item>
</rdf:RDF>`;

describe('parsing a feed', () => {
  it('reads RSS 2.0', () => {
    const items = parseFeed(rss2);
    expect(items).toHaveLength(2);
    expect(items[0]!.url).toBe('https://example.org/fungal-networks');
    expect(items[0]!.title).toBe('Fungal networks move nitrogen further than thought');
    expect(items[0]!.publishedAt?.toISOString().slice(0, 10)).toBe('2026-09-18');
  });

  it('strips the HTML feeds put in a description', () => {
    expect(parseFeed(rss2)[0]!.summary).toBe(
      'Researchers found mycorrhizal networks moving nitrogen.',
    );
  });

  it('reads Atom, where the link is an attribute', () => {
    const items = parseFeed(atom);
    expect(items).toHaveLength(1);
    expect(items[0]!.url).toBe('https://example.org/eu-soil-law');
    expect(items[0]!.summary).toBe('A summary of the vote.');
    expect(items[0]!.publishedAt?.toISOString().slice(0, 10)).toBe('2026-09-19');
  });

  it('reads RDF, and finds the date under dc:date', () => {
    const items = parseFeed(rdf);
    expect(items[0]!.url).toBe('https://example.org/rdf-item');
    expect(items[0]!.publishedAt?.toISOString().slice(0, 10)).toBe('2026-09-15');
  });

  it('copes with a feed holding exactly one item, which is not an array', () => {
    const single = `<rss><channel><item><title>One</title><link>https://example.org/one</link></item></channel></rss>`;
    expect(parseFeed(single)).toHaveLength(1);
  });

  it('drops an item with no usable link rather than storing a broken row', () => {
    const broken = `<rss><channel><item><title>No link here</title></item></channel></rss>`;
    expect(parseFeed(broken)).toHaveLength(0);
  });

  it('falls back to guid when it is a URL', () => {
    const guid = `<rss><channel><item><title>T</title><guid>https://example.org/from-guid</guid></item></channel></rss>`;
    expect(parseFeed(guid)[0]!.url).toBe('https://example.org/from-guid');
  });

  it('returns nothing for an empty or unparseable feed rather than throwing', () => {
    expect(parseFeed('<rss><channel></channel></rss>')).toEqual([]);
    expect(parseFeed('not xml at all')).toEqual([]);
  });

  it('leaves the date null rather than inventing one', () => {
    const undated = `<rss><channel><item><title>T</title><link>https://example.org/x</link><pubDate>nonsense</pubDate></item></channel></rss>`;
    expect(parseFeed(undated)[0]!.publishedAt).toBeNull();
  });

  it('caps a full-article summary so the ranker is not handed a novel', () => {
    const long = `<rss><channel><item><title>T</title><link>https://example.org/x</link><description>${'word '.repeat(2000)}</description></item></channel></rss>`;
    expect(parseFeed(long)[0]!.summary!.length).toBeLessThanOrEqual(2000);
  });
});

describe('stripping HTML', () => {
  it('removes tags, scripts and styles', () => {
    expect(stripTags('<p>Soil is <b>alive</b></p><script>bad()</script>')).toBe('Soil is alive');
  });

  it('decodes the entities feeds actually use', () => {
    expect(stripTags('Soil &amp; water &#39;here&#39; &quot;now&quot;')).toBe(
      `Soil & water 'here' "now"`,
    );
  });

  it('collapses the whitespace tags leave behind', () => {
    expect(stripTags('<p>one</p>\n\n   <p>two</p>')).toBe('one two');
  });
});
