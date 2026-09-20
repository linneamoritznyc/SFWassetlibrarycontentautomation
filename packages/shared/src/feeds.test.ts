import { describe, expect, it } from 'vitest';
import { FEEDS, REGIONS } from './feeds.js';

/**
 * These check the shape of the source list, not that the URLs answer. Whether
 * a URL answers is a question about the internet, and `pnpm feeds:check` is
 * where it gets asked.
 */
describe('the feed list', () => {
  it('gives every feed a region from the known set', () => {
    for (const feed of FEEDS) {
      expect(REGIONS, `${feed.name} has region "${feed.region}"`).toContain(feed.region);
    }
  });

  it('reaches past the English-speaking north', () => {
    const covered = new Set(FEEDS.map((f) => f.region));
    for (const region of ['Africa', 'Asia', 'Latin America', 'Oceania'] as const) {
      expect(covered, `no feed covers ${region}`).toContain(region);
    }
  });

  it('names the organisations the Foundation asked for', () => {
    const names = FEEDS.map((f) => f.name.toLowerCase()).join(' | ');
    for (const org of [
      'fao',
      'unccd',
      'ipbes',
      'cgiar',
      'world resources institute',
      'african union',
      'agra',
      'regeneration international',
      'embrapa',
      'iica',
      'soils for life',
      'apcnf',
      'icrisat',
      'eu soil observatory',
    ]) {
      expect(names, `no feed for ${org}`).toContain(org);
    }
  });

  it('has no duplicate URLs', () => {
    // `feeds.url` is the conflict target on seed, so a duplicate here would
    // quietly mean one fewer feed than the list claims.
    const urls = FEEDS.map((f) => f.url);
    expect(new Set(urls).size).toBe(urls.length);
  });

  it('has no duplicate names', () => {
    const names = FEEDS.map((f) => f.name);
    expect(new Set(names).size).toBe(names.length);
  });

  it('uses https everywhere', () => {
    for (const feed of FEEDS) {
      expect(feed.url.startsWith('https://'), `${feed.name}: ${feed.url}`).toBe(true);
      expect(() => new URL(feed.url)).not.toThrow();
    }
  });

  it('marks each feed as something the scout knows how to read', () => {
    for (const feed of FEEDS) {
      expect(['rss', 'page'], `${feed.name}`).toContain(feed.kind);
    }
  });
});
