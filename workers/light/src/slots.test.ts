import { describe, expect, it } from 'vitest';
import { CADENCE } from '@sfw/shared';
import {
  markExploration,
  pillarBalance,
  scoreCandidate,
  slotsForWeek,
  type Slot,
} from './slots.js';

// A Monday.
const MONDAY = new Date('2026-09-21T00:00:00Z');

describe('the week the cadence asks for', () => {
  const slots = slotsForWeek(MONDAY, CADENCE);

  it('puts a feed post on Monday, Wednesday and Friday', () => {
    const feed = slots.filter((s) => s.format === 'feed');
    expect(feed).toHaveLength(3);
    expect(feed.map((s) => s.date)).toEqual(['2026-09-21', '2026-09-23', '2026-09-25']);
  });

  it('adds the Stories, Shorts and LinkedIn the cadence calls for', () => {
    expect(slots.filter((s) => s.format === 'story')).toHaveLength(CADENCE.storiesPerWeek[1]);
    expect(slots.filter((s) => s.format === 'short')).toHaveLength(CADENCE.shortsPerWeek);
    expect(slots.filter((s) => s.format === 'linkedin')).toHaveLength(CADENCE.linkedinPerWeek[0]);
  });

  it('keeps every slot inside the seven days', () => {
    for (const slot of slots) {
      expect(slot.date >= '2026-09-21').toBe(true);
      expect(slot.date <= '2026-09-27').toBe(true);
    }
  });

  it('uses the posting windows rather than inventing times', () => {
    const times = new Set(slots.map((s) => s.time));
    for (const time of times) {
      expect(CADENCE.postingWindows.some(([start]) => start === time)).toBe(true);
    }
  });

  it('comes back in chronological order', () => {
    const keys = slots.map((s) => s.date + s.time);
    expect(keys).toEqual([...keys].sort());
  });

  it('holds about a fifth of the slots for experiments', () => {
    const experiments = slots.filter((s) => s.exploration).length;
    expect(experiments).toBe(Math.round(slots.length * 0.2));
  });
});

describe('spreading the experiments out', () => {
  const slot = (i: number): Slot => ({
    date: `2026-09-${21 + i}`,
    time: '08:00',
    platform: 'instagram',
    format: 'feed',
    exploration: false,
  });

  it('never puts two experiments next to each other at a fifth', () => {
    const marked = markExploration(
      Array.from({ length: 10 }, (_, i) => slot(i)),
      0.2,
    );
    const positions = marked.flatMap((s, i) => (s.exploration ? [i] : []));
    expect(positions).toHaveLength(2);
    expect(positions[1]! - positions[0]!).toBeGreaterThan(1);
  });

  it('marks nothing when the share is zero', () => {
    const marked = markExploration([slot(0), slot(1)], 0);
    expect(marked.every((s) => !s.exploration)).toBe(true);
  });
});

describe('scoring', () => {
  const base = {
    relevance: 1,
    ageDays: 0,
    materialStrength: 1,
    formatWeight: 1,
    pillarBalance: 1,
  };

  it('scores a fresh, relevant, well-supplied story at one', () => {
    expect(scoreCandidate(base)).toBeCloseTo(1);
  });

  it('decays with age', () => {
    expect(scoreCandidate({ ...base, ageDays: 21 })).toBeCloseTo(0.5);
    expect(scoreCandidate({ ...base, ageDays: 63 })).toBeLessThan(0.3);
  });

  it('punishes a story with thin material', () => {
    expect(scoreCandidate({ ...base, materialStrength: 0.2 })).toBeCloseTo(0.2);
  });

  it('multiplies rather than averages, so one zero sinks the story', () => {
    expect(scoreCandidate({ ...base, relevance: 0 })).toBe(0);
  });

  it('never returns a negative score', () => {
    expect(scoreCandidate({ ...base, relevance: -5, materialStrength: -1 })).toBeGreaterThanOrEqual(
      0,
    );
  });
});

describe('pillar balance', () => {
  const pillars = ['PROVE IT', 'TEACH IT', 'PRACTICE IT', 'GROW IT'];

  it('is even when nothing has run yet', () => {
    const balance = pillarBalance({}, pillars);
    expect(new Set(Object.values(balance)).size).toBe(1);
  });

  it('pushes back against a pillar that has run a lot', () => {
    const balance = pillarBalance({ 'PROVE IT': 6, 'TEACH IT': 0 }, pillars);
    expect(balance['PROVE IT']!).toBeLessThan(balance['TEACH IT']!);
  });

  it('stays finite for a pillar with no history', () => {
    const balance = pillarBalance({ 'PROVE IT': 100 }, pillars);
    expect(Number.isFinite(balance['GROW IT']!)).toBe(true);
  });
});
