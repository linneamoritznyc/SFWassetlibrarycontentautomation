import { afterEach, describe, expect, it } from 'vitest';
import { decide, keepImages, syncTokenMatches } from './wormhole-sync';

describe('decide', () => {
  const t = (m: number) => new Date(Date.UTC(2026, 9, 17, 12, m)).toISOString();

  it('applies a doc edit when Wormhole has not changed since the last sync', () => {
    expect(decide(t(0), t(0), t(1))).toBe('apply');
  });
  it('lets the newer edit win when both changed', () => {
    expect(decide(t(5), t(0), t(7))).toBe('apply');
    expect(decide(t(5), t(0), t(3))).toBe('keep_wormhole');
  });
  it('compares times when the doc never synced the post', () => {
    expect(decide(t(5), null, t(6))).toBe('apply');
    expect(decide(t(5), null, t(4))).toBe('keep_wormhole');
  });
  it('keeps Wormhole when the doc gives no edit time', () => {
    expect(decide(t(5), t(0), null)).toBe('keep_wormhole');
  });
});

describe('keepImages', () => {
  it('keeps images by position and drops extra ones', () => {
    const current = [
      { text: 'a', image: '11111111-1111-1111-1111-111111111111' },
      { text: 'b', image: null },
      { text: 'c', image: '33333333-3333-3333-3333-333333333333' },
    ];
    expect(
      keepImages(
        [
          { text: 'A', image: null },
          { text: 'B', image: null },
        ],
        current,
      ),
    ).toEqual([
      { text: 'A', image: '11111111-1111-1111-1111-111111111111' },
      { text: 'B', image: null },
    ]);
  });
});

describe('syncTokenMatches', () => {
  const before = process.env.WORMHOLE_SYNC_TOKEN;
  afterEach(() => {
    process.env.WORMHOLE_SYNC_TOKEN = before;
  });

  it('needs the exact token', () => {
    process.env.WORMHOLE_SYNC_TOKEN = 'x'.repeat(40);
    expect(syncTokenMatches(`Bearer ${'x'.repeat(40)}`)).toBe(true);
    expect(syncTokenMatches(`Bearer ${'x'.repeat(39)}y`)).toBe(false);
    expect(syncTokenMatches(null)).toBe(false);
  });
  it('lets nobody in without a long enough token set', () => {
    process.env.WORMHOLE_SYNC_TOKEN = '';
    expect(syncTokenMatches('Bearer ')).toBe(false);
    process.env.WORMHOLE_SYNC_TOKEN = 'short';
    expect(syncTokenMatches('Bearer short')).toBe(false);
  });
});
