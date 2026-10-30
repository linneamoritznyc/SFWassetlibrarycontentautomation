import { describe, expect, it } from 'vitest';
import type { WormholePost } from '@/lib/wormhole-types';
import { matchesSearch } from './util';

const post = (over: Partial<WormholePost> = {}): WormholePost => ({
  id: 'cr20261112',
  iso_date: '2026-11-12',
  date_tbd: false,
  topic: 'A day at the Costa Rica workshop',
  platform: 'Instagram, Facebook',
  caption: 'Students build thermophilic piles at Armonía.',
  slides: [{ text: 'Welcome, new consultants.', image: null }],
  cta: '',
  link: 'https://school.soilfoodweb.com',
  sources: ['Workshop Handbook, March 2025'],
  visual_note: 'Family: D, full-bleed photo.',
  note: '',
  status: 'draft',
  updated_by: 'Allison',
  updated_at: '2026-10-30T10:00:00Z',
  ...over,
});

describe('matchesSearch', () => {
  it('matches everything when the query is empty', () => {
    expect(matchesSearch(post(), '')).toBe(true);
    expect(matchesSearch(post(), '   ')).toBe(true);
  });

  it('finds words in the topic, caption, slides, notes, sources and id', () => {
    expect(matchesSearch(post(), 'costa rica')).toBe(true);
    expect(matchesSearch(post(), 'thermophilic')).toBe(true);
    expect(matchesSearch(post(), 'consultants')).toBe(true);
    expect(matchesSearch(post(), 'full-bleed')).toBe(true);
    expect(matchesSearch(post(), 'handbook')).toBe(true);
    expect(matchesSearch(post(), 'cr20261112')).toBe(true);
  });

  it('needs every word, in any order and any case', () => {
    expect(matchesSearch(post(), 'PILES costa')).toBe(true);
    expect(matchesSearch(post(), 'costa nematode')).toBe(false);
  });

  it('ignores accents', () => {
    expect(matchesSearch(post(), 'armonia')).toBe(true);
  });

  it('finds a post by its date', () => {
    expect(matchesSearch(post(), 'november 12')).toBe(true);
    expect(matchesSearch(post(), 'thursday')).toBe(true);
    expect(matchesSearch(post(), '2026-11')).toBe(true);
    expect(matchesSearch(post({ date_tbd: true }), 'tbd')).toBe(true);
  });
});
