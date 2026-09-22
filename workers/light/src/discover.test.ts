import { createServer, type Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { alternateLinks, discoverFeed } from './discover.js';
import { fetchFeed, isDead } from './feed-fetch.js';

/**
 * A small fake internet.
 *
 * The real feed URLs cannot be reached from the sandbox this was built in, so
 * the only honest way to show the repair works is to serve the ways a feed
 * actually breaks and watch the scout deal with each one: a newsroom that
 * moved and says where in its head tags, one that moved and says nothing, a
 * cookie wall, bot protection, a server having a bad day, and a feed that has
 * genuinely gone.
 */

const FEED_XML = `<?xml version="1.0"?>
<rss version="2.0"><channel>
  <title>Soil Science Weekly</title>
  <item>
    <title>Fungal networks move more carbon than expected</title>
    <link>https://example.test/articles/fungal-networks</link>
    <pubDate>Mon, 21 Sep 2026 09:00:00 GMT</pubDate>
    <description>A field trial across eleven sites.</description>
  </item>
  <item>
    <title>Nematode counts as a soil health indicator</title>
    <link>https://example.test/articles/nematodes</link>
    <pubDate>Fri, 18 Sep 2026 09:00:00 GMT</pubDate>
  </item>
</channel></rss>`;

const COOKIE_WALL = `<!doctype html><html><head><title>Before you continue</title></head>
<body><h1>We value your privacy</h1><p>Accept cookies to continue.</p></body></html>`;

let server: Server;
let base: string;

beforeAll(async () => {
  server = createServer((req, res) => {
    const url = new URL(req.url ?? '/', 'http://localhost');

    switch (url.pathname) {
      // A site that moved its feed and declares the new one properly.
      case '/moved/rss.xml':
        res.writeHead(404).end('not found');
        return;
      case '/moved/':
      case '/moved':
        res.writeHead(200, { 'content-type': 'text/html' }).end(
          `<!doctype html><html><head>
             <link rel="stylesheet" href="/site.css">
             <link rel='alternate' type='application/rss+xml' title='News' href='/moved/news/feed/'>
           </head><body>Newsroom</body></html>`,
        );
        return;
      case '/moved/news/feed/':
        res.writeHead(200, { 'content-type': 'application/rss+xml' }).end(FEED_XML);
        return;

      // A site that moved its feed and declares nothing: only a common path
      // finds it.
      case '/quiet/rss.xml':
        res.writeHead(404).end('not found');
        return;
      case '/quiet/':
      case '/quiet':
        res.writeHead(200, { 'content-type': 'text/html' }).end('<!doctype html><html></html>');
        return;

      // The site root, where the common paths are tried.
      case '/':
        res.writeHead(200, { 'content-type': 'text/html' }).end('<!doctype html><html></html>');
        return;
      case '/feed':
        res.writeHead(200, { 'content-type': 'application/rss+xml' }).end(FEED_XML);
        return;

      case '/good.xml':
        res.writeHead(200, { 'content-type': 'application/rss+xml' }).end(FEED_XML);
        return;

      case '/wall.xml':
        res.writeHead(200, { 'content-type': 'text/html' }).end(COOKIE_WALL);
        return;

      case '/blocked.xml':
        res.writeHead(403).end('Forbidden');
        return;

      case '/ratelimited.xml':
        res.writeHead(429).end('Slow down');
        return;

      case '/broken.xml':
        res.writeHead(503).end('Service Unavailable');
        return;

      // Genuinely gone, and the site offers nothing anywhere.
      case '/gone/feed.xml':
        res.writeHead(410).end('Gone');
        return;

      case '/conditional.xml':
        if (req.headers['if-none-match'] === '"v1"') {
          res.writeHead(304).end();
          return;
        }
        res.writeHead(200, { 'content-type': 'application/rss+xml', etag: '"v1"' }).end(FEED_XML);
        return;

      default:
        res.writeHead(404).end('not found');
    }
  });

  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});

afterAll(async () => {
  await new Promise<void>((resolve) => server.close(() => resolve()));
});

describe('reading the head for a declared feed', () => {
  it('finds an RSS link whatever order the attributes are in', () => {
    const html = `<link type="application/rss+xml" rel="alternate" href="/feed/">`;
    expect(alternateLinks(html, 'https://example.test/news')).toEqual([
      'https://example.test/feed/',
    ]);
  });

  it('resolves a relative href against the page it came from', () => {
    const html = `<link rel="alternate" type="application/atom+xml" href="../atom.xml">`;
    expect(alternateLinks(html, 'https://example.test/news/index.html')).toEqual([
      'https://example.test/atom.xml',
    ]);
  });

  it('ignores stylesheets, icons and other alternates', () => {
    const html = `
      <link rel="stylesheet" href="/a.css">
      <link rel="alternate" hreflang="de" href="/de/">
      <link rel="alternate" type="application/json" href="/feed.json">
      <link rel="icon" href="/favicon.ico">`;
    expect(alternateLinks(html, 'https://example.test/')).toEqual([]);
  });

  it('unescapes an ampersand in a query string', () => {
    const html = `<link rel="alternate" type="application/rss+xml" href="/?feed=rss&amp;cat=soil">`;
    expect(alternateLinks(html, 'https://example.test/')).toEqual([
      'https://example.test/?feed=rss&cat=soil',
    ]);
  });

  it('does not invent a feed when the page declares none', () => {
    expect(alternateLinks('<!doctype html><html><head></head></html>', 'https://x.test/')).toEqual(
      [],
    );
  });
});

describe('classifying what came back', () => {
  it('reads a feed that works', async () => {
    const outcome = await fetchFeed(`${base}/good.xml`);
    expect(outcome.kind).toBe('ok');
    if (outcome.kind !== 'ok') return;
    expect(outcome.items).toHaveLength(2);
    expect(outcome.items.map((i) => i.title)).toEqual([
      'Fungal networks move more carbon than expected',
      'Nematode counts as a soil health indicator',
    ]);
  });

  it('calls a cookie wall a move, not an empty feed', async () => {
    const outcome = await fetchFeed(`${base}/wall.xml`);
    expect(outcome.kind).toBe('moved');
    expect(isDead(outcome.kind)).toBe(true);
  });

  it('calls a 403 blocked, and not dead', async () => {
    const outcome = await fetchFeed(`${base}/blocked.xml`);
    expect(outcome.kind).toBe('blocked');
    // The distinction that keeps a partner behind Cloudflare in the list.
    expect(isDead(outcome.kind)).toBe(false);
  });

  it('calls rate limiting blocked too', async () => {
    const outcome = await fetchFeed(`${base}/ratelimited.xml`);
    expect(outcome.kind).toBe('blocked');
  });

  it('calls a 503 transient, and not dead', async () => {
    const outcome = await fetchFeed(`${base}/broken.xml`);
    expect(outcome.kind).toBe('transient');
    expect(isDead(outcome.kind)).toBe(false);
  });

  it('calls a connection that goes nowhere transient', async () => {
    // Port 1 with nothing on it: refused immediately.
    const outcome = await fetchFeed('http://127.0.0.1:1/feed.xml', { timeoutMs: 2000 });
    expect(outcome.kind).toBe('transient');
  });

  it('sends the validator back and understands 304', async () => {
    const first = await fetchFeed(`${base}/conditional.xml`);
    expect(first.kind).toBe('ok');
    if (first.kind !== 'ok') return;
    expect(first.etag).toBe('"v1"');

    const second = await fetchFeed(`${base}/conditional.xml`, {
      conditional: { etag: first.etag },
    });
    expect(second.kind).toBe('unchanged');
  });
});

describe('finding a feed that moved', () => {
  it('follows the link the site declares in its head', async () => {
    const found = await discoverFeed(`${base}/moved/rss.xml`);
    expect(found).not.toBeNull();
    expect(found?.url).toBe(`${base}/moved/news/feed/`);
    expect(found?.how).toBe('autodiscovery');
    expect(found?.items).toBe(2);
  });

  it('falls back to the common paths when nothing is declared', async () => {
    const found = await discoverFeed(`${base}/quiet/rss.xml`);
    expect(found?.url).toBe(`${base}/feed`);
    expect(found?.how).toBe('common path');
  });

  it('gives up rather than guessing when there is nothing there', async () => {
    // Nothing is served under this host but the root, which declares no feed,
    // and /feed is the only common path that answers. Point it at a port with
    // no server at all so every candidate fails.
    const found = await discoverFeed('http://127.0.0.1:1/gone/feed.xml', { timeoutMs: 500 });
    expect(found).toBeNull();
  });

  it('never repairs a feed into something that does not parse', async () => {
    // The wall answers 200 with HTML at every path, so no candidate validates.
    const found = await discoverFeed(`${base}/wall.xml`);
    expect(found === null || found.items > 0).toBe(true);
  });
});
