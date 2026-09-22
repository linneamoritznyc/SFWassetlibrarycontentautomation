import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest';
import { createTestDatabase, testDatabaseUrl, type Pool } from '@sfw/db';

const hasDb = Boolean(testDatabaseUrl());
const describeDb = hasDb ? describe : describe.skip;

if (!hasDb) {
  console.warn('TEST_DATABASE_URL is not set, skipping the scout_fetch tests.');
}

const RSS = `<?xml version="1.0"?>
<rss version="2.0"><channel>
  <item>
    <title>Soil carbon trial in Coimbatore</title>
    <link>https://example.org/one</link>
    <pubDate>${new Date().toUTCString()}</pubDate>
    <description>A first season of results.</description>
  </item>
</channel></rss>`;

/**
 * The point of these is the health tracking. A global source list means feeds
 * that go dead in a language nobody on the team reads, on sites nobody checks,
 * so the system has to notice by itself and say so in Settings.
 */
describeDb('scout_fetch', () => {
  let pool: Pool;
  let scoutFetch: (ctx: {
    job: Record<string, unknown>;
    enqueue: () => Promise<null>;
  }) => Promise<void>;

  beforeAll(async () => {
    pool = await createTestDatabase('scout_fetch');

    // The worker opens its own pool from DATABASE_URL, so point it at the
    // throwaway database before the module is loaded.
    const url = new URL(testDatabaseUrl()!);
    url.pathname = '/sfw_test_scout_fetch';
    process.env.DATABASE_URL = url.toString();

    const mod = await import('./scout_fetch.js');
    scoutFetch = mod.scoutFetch as unknown as typeof scoutFetch;
  }, 60_000);

  afterAll(async () => {
    vi.unstubAllGlobals();
    await pool?.end();
  });

  async function run(): Promise<void> {
    await scoutFetch({
      job: { id: '1', type: 'scout_fetch', payload: {} },
      enqueue: async () => null,
    });
  }

  async function feed(name: string): Promise<{
    url: string;
    active: boolean;
    last_error: string | null;
    last_ok_at: Date | null;
    last_checked_at: Date | null;
    consecutive_failures: number;
    failure_kind: string | null;
    previous_url: string | null;
  }> {
    const { rows } = await pool.query(
      `select url, active, last_error, last_ok_at, last_checked_at, consecutive_failures,
              failure_kind, previous_url
       from feeds where name = $1`,
      [name],
    );
    return rows[0];
  }

  it('records health for every feed, and one dead feed does not stop the others', async () => {
    await pool.query(`delete from news_items`);
    await pool.query(`delete from feeds`);
    await pool.query(
      `insert into feeds (name, url, kind, region, active) values
        ('Working', 'https://example.org/good.xml', 'rss', 'Global', true),
        ('Gone', 'https://example.org/404.xml', 'rss', 'Africa', true),
        ('Cookie wall', 'https://example.org/empty.xml', 'rss', 'Asia', true)`,
    );

    vi.stubGlobal(
      'fetch',
      vi.fn(async (url: string) => {
        if (url.includes('good')) return new Response(RSS, { status: 200 });
        if (url.includes('404')) return new Response('nope', { status: 404 });
        return new Response('<html><body>Accept cookies</body></html>', { status: 200 });
      }),
    );

    await run();

    const working = await feed('Working');
    expect(working.consecutive_failures).toBe(0);
    expect(working.last_error).toBeNull();
    expect(working.last_ok_at).toBeInstanceOf(Date);

    const gone = await feed('Gone');
    expect(gone.consecutive_failures).toBe(1);
    expect(gone.last_error).toBe('HTTP 404');
    expect(gone.last_ok_at).toBeNull();
    expect(gone.active, 'one failure is not enough to switch a feed off').toBe(true);

    // 200 with a web page is the most common way a feed dies, so it counts as
    // a failure rather than as a quiet day, and it is called a move rather
    // than an unreadable feed because the two need different answers.
    const wall = await feed('Cookie wall');
    expect(wall.consecutive_failures).toBe(1);
    expect(wall.last_error).toContain('not a feed');
    expect(wall.failure_kind).toBe('moved');

    const { rows } = await pool.query<{ n: number }>(`select count(*)::int as n from news_items`);
    expect(rows[0]!.n, 'the working feed still delivered').toBe(1);
  });

  it('switches a feed off after five failures in a row', async () => {
    for (let i = 0; i < 4; i += 1) await run();

    const gone = await feed('Gone');
    expect(gone.consecutive_failures).toBe(5);
    expect(gone.active).toBe(false);

    const working = await feed('Working');
    expect(working.active).toBe(true);
    expect(working.consecutive_failures).toBe(0);
  });

  it('clears the failure count when a feed comes back', async () => {
    await pool.query(`update feeds set active = true where name = 'Gone'`);

    vi.stubGlobal(
      'fetch',
      vi.fn(async () => new Response(RSS, { status: 200 })),
    );

    await run();

    const gone = await feed('Gone');
    expect(gone.consecutive_failures).toBe(0);
    expect(gone.last_error).toBeNull();
    expect(gone.last_ok_at).toBeInstanceOf(Date);
  });

  it('finds a feed that moved, and uses the new address from then on', async () => {
    await pool.query(`delete from news_items`);
    await pool.query(`delete from feeds`);
    await pool.query(
      `insert into feeds (name, url, kind, region, active)
       values ('Moved', 'https://example.org/news/rss.xml', 'rss', 'Europe', true)`,
    );

    // The shape this takes in the wild: the old URL is gone, and the section
    // page it lived under declares where the feed went.
    vi.stubGlobal(
      'fetch',
      vi.fn(async (url: string) => {
        if (url.endsWith('/news/rss.xml')) return new Response('gone', { status: 404 });
        if (url.endsWith('/news/')) {
          return new Response(
            `<!doctype html><html><head><link rel="alternate"
               type="application/rss+xml" href="/news/feed.xml"></head></html>`,
            { status: 200, headers: { 'content-type': 'text/html' } },
          );
        }
        if (url.endsWith('/news/feed.xml')) return new Response(RSS, { status: 200 });
        return new Response('<html></html>', { status: 200 });
      }),
    );

    await run();

    const moved = await feed('Moved');
    expect(moved.url).toBe('https://example.org/news/feed.xml');
    expect(moved.previous_url, 'the old URL is kept so the change is visible').toBe(
      'https://example.org/news/rss.xml',
    );
    expect(moved.consecutive_failures, 'a repaired feed is not a failing feed').toBe(0);
    expect(moved.last_ok_at).toBeInstanceOf(Date);

    const { rows } = await pool.query<{ n: number }>(`select count(*)::int as n from news_items`);
    expect(rows[0]!.n, 'and it delivered on the same run').toBe(1);
  });

  it('never switches off a feed that is only being refused', async () => {
    await pool.query(`delete from news_items`);
    await pool.query(`delete from feeds`);
    await pool.query(
      `insert into feeds (name, url, kind, region, active)
       values ('Walled', 'https://example.org/walled.xml', 'rss', 'Asia', true)`,
    );

    vi.stubGlobal(
      'fetch',
      vi.fn(async () => new Response('Forbidden', { status: 403 })),
    );

    // Well past the five that would retire a dead URL.
    for (let i = 0; i < 7; i += 1) await run();

    const walled = await feed('Walled');
    expect(walled.consecutive_failures).toBe(7);
    expect(walled.failure_kind).toBe('blocked');
    // Bot protection is a decision for a person. Switching the source off
    // would lose it and fix nothing.
    expect(walled.active).toBe(true);
  });

  it('keeps a feed whose server is having a bad week', async () => {
    await pool.query(`delete from feeds`);
    await pool.query(
      `insert into feeds (name, url, kind, region, active)
       values ('Flaky', 'https://example.org/flaky.xml', 'rss', 'Global', true)`,
    );

    vi.stubGlobal(
      'fetch',
      vi.fn(async () => new Response('Service Unavailable', { status: 503 })),
    );

    for (let i = 0; i < 6; i += 1) await run();

    const flaky = await feed('Flaky');
    expect(flaky.failure_kind).toBe('transient');
    expect(flaky.active).toBe(true);
  });

  it('sends a page feed to web_fetch instead of trying to parse it', async () => {
    await pool.query(`delete from feeds`);
    await pool.query(
      `insert into feeds (name, url, kind, region, active)
       values ('Highlights page', 'https://example.org/highlights', 'page', 'Europe', true)`,
    );

    const fetchSpy = vi.fn(async () => new Response('', { status: 500 }));
    vi.stubGlobal('fetch', fetchSpy);

    const enqueued: { type: string; payload?: Record<string, unknown> }[] = [];
    await scoutFetch({
      job: { id: '1', type: 'scout_fetch', payload: {} },
      enqueue: (async (input: { type: string; payload?: Record<string, unknown> }) => {
        enqueued.push(input);
        return null;
      }) as unknown as () => Promise<null>,
    });

    expect(fetchSpy, 'a page feed is never fetched here').not.toHaveBeenCalled();
    expect(enqueued).toContainEqual(
      expect.objectContaining({
        type: 'web_fetch',
        payload: { url: 'https://example.org/highlights' },
      }),
    );
  });
});
