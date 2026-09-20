import { describe, expect, it } from 'vitest';
import { formatTranscript, snapToWords, type Candidate } from './find_clips.js';

type Word = { w: string; start: number; end: number };

/** Two words a second for two minutes. */
const words: Word[] = Array.from({ length: 240 }, (_, i) => ({
  w: `w${i}`,
  start: i * 0.5,
  end: i * 0.5 + 0.45,
}));

const candidate = (start: number, end: number): Candidate => ({
  start,
  end,
  hook: 'A hook',
  why: 'Because',
  pillar: 'PROVE IT',
  speaker: 'Loida',
  score: 80,
});

describe('snapping a clip to word boundaries', () => {
  it('moves the edges onto real words and pads them', () => {
    const snapped = snapToWords(candidate(10.2, 40.7), words);
    expect(snapped).not.toBeNull();
    // The word containing 10.2 starts at 10.0; padding takes it to 9.7.
    expect(snapped!.start).toBeCloseTo(9.7, 2);
    expect(snapped!.end).toBeGreaterThan(40.7);
  });

  it('never starts before the beginning of the video', () => {
    const snapped = snapToWords(candidate(0, 30), words);
    expect(snapped!.start).toBe(0);
  });

  it('drops anything shorter than twenty seconds', () => {
    expect(snapToWords(candidate(10, 25), words)).toBeNull();
  });

  it('drops anything longer than a minute', () => {
    expect(snapToWords(candidate(10, 75), words)).toBeNull();
  });

  it('keeps the hook, pillar, speaker and score untouched', () => {
    const snapped = snapToWords(candidate(10, 40), words);
    expect(snapped).toMatchObject({
      hook: 'A hook',
      pillar: 'PROVE IT',
      speaker: 'Loida',
      score: 80,
    });
  });

  it('returns null rather than throwing when the times are past the transcript', () => {
    expect(snapToWords(candidate(9999, 10030), words)).toBeNull();
  });
});

describe('transcript formatting', () => {
  it('starts each line with the time, so the model can cite one', () => {
    const lines = formatTranscript([
      { w: 'Finished', start: 2, end: 2.4 },
      { w: 'vermicompost', start: 2.4, end: 3 },
      { w: 'is', start: 3, end: 3.2 },
      { w: 'dark.', start: 3.2, end: 3.6 },
      { w: 'Next', start: 5, end: 5.4 },
      { w: 'sentence.', start: 5.4, end: 6 },
    ]).split('\n');

    expect(lines).toHaveLength(2);
    expect(lines[0]).toBe('[2.0] Finished vermicompost is dark.');
    expect(lines[1]).toBe('[5.0] Next sentence.');
  });
});
