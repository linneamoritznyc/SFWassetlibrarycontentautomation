import { describe, expect, it } from 'vitest';
import { MIN_SCORE, parseFeed, plain, score } from './scout';

describe('scout', () => {
  it('reads RSS items, CDATA and encoded HTML included', () => {
    const xml = `<rss><channel><item><title><![CDATA[Fungi &amp; roots]]></title>
      <link>https://example.org/a</link><pubDate>Wed, 21 Oct 2026 10:00:00 GMT</pubDate>
      <description>&lt;p&gt;Mycorrhizal fungi trade &lt;b&gt;phosphorus&lt;/b&gt;.&lt;/p&gt;</description></item></channel></rss>`;
    const [it] = parseFeed(xml);
    expect(it).toMatchObject({
      title: 'Fungi & roots',
      url: 'https://example.org/a',
      published: '2026-10-21T10:00:00.000Z',
      summary: 'Mycorrhizal fungi trade phosphorus .',
    });
  });

  it('reads Atom entries with a link href', () => {
    const [it] = parseFeed(
      `<feed><entry><title>Soil carbon</title><link rel="alternate" href="https://example.org/b"/><updated>2026-10-20T00:00:00Z</updated></entry></feed>`,
    );
    expect(it?.url).toBe('https://example.org/b');
  });

  it('splits the outlet off a Google News title', () => {
    const [it] = parseFeed(
      `<rss><item><title>Healthy soil on the farm - NZ Herald</title><link>https://news.google.com/x</link><source url="https://nzherald.co.nz">NZ Herald</source><description>&lt;a href="x"&gt;Healthy soil on the farm&lt;/a&gt;</description></item></rss>`,
    );
    expect(it).toMatchObject({ title: 'Healthy soil on the farm', source: 'NZ Herald', summary: '' });
  });

  it('keeps going past a malformed feed', () => {
    const xml = `<rss><item><title>Good & bad</title><link>https://example.org/c</link></item><broken`;
    expect(parseFeed(xml)).toHaveLength(1);
  });

  it('scores soil biology above general farm news', () => {
    expect(score('Nematodes and protozoa release nitrogen in compost').score).toBeGreaterThan(8);
    expect(score('Tractor sales rise for farmers').score).toBeLessThan(MIN_SCORE);
    expect(plain('a&nbsp;&#8217;b')).toBe('a ’b');
  });
});
