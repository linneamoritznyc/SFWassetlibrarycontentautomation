import { describe, expect, it } from 'vitest';
import {
  buildAss,
  buildSrt,
  shiftWords,
  windowWords,
  wordsBetween,
  type Word,
} from './captions.js';

const say = (text: string, from = 0, step = 0.4): Word[] =>
  text.split(' ').map((w, i) => ({ w, start: from + i * step, end: from + i * step + step * 0.9 }));

describe('caption windows', () => {
  it('keeps to two lines at most', () => {
    const windows = windowWords(
      say('one two three four five six seven eight nine ten eleven twelve'),
    );
    for (const window of windows) {
      expect(window.lines.length).toBeLessThanOrEqual(2);
    }
  });

  it('puts every word in exactly one window', () => {
    const words = say('the soil food web is alive and it is doing the work for you');
    const windows = windowWords(words);
    const seen = windows.flatMap((w) => w.words.map((x) => x.w));
    expect(seen).toEqual(words.map((w) => w.w));
  });

  it('breaks at a long pause rather than holding half a sentence through silence', () => {
    const words: Word[] = [
      { w: 'before', start: 0, end: 0.4 },
      { w: 'the', start: 0.4, end: 0.6 },
      { w: 'pause', start: 0.6, end: 1.0 },
      // Three seconds of nothing.
      { w: 'after', start: 4.0, end: 4.4 },
    ];
    const windows = windowWords(words);
    expect(windows).toHaveLength(2);
    expect(windows[1]!.words.map((w) => w.w)).toEqual(['after']);
  });

  it('indexes lines into the word list, so rendering cannot drift', () => {
    const words = say(
      'nematodes eat bacteria and release nitrogen right where roots can take it up',
    );
    for (const window of windowWords(words)) {
      const indices = window.lines.flat();
      expect(indices).toEqual(indices.map((_, i) => i));
      expect(indices.length).toBe(window.words.length);
    }
  });
});

describe('ASS output', () => {
  const words = say('finished vermicompost should be dark and crumbly');
  const frame = { width: 1080, height: 1920 };

  it('emits one event per word, which is what makes the highlight move', () => {
    const ass = buildAss(words, frame);
    expect(ass.match(/^Dialogue:/gm)).toHaveLength(words.length);
  });

  it('highlights exactly one word per event', () => {
    // ASS colours are &HAABBGGRR: eight hex digits, not six.
    const highlight = /\{\\c&H00689A4C\}/g;
    const restore = /\{\\c&H00E4EFF4\}/g;

    for (const line of buildAss(words, frame)
      .split('\n')
      .filter((l) => l.startsWith('Dialogue:'))) {
      expect(line.match(highlight)).toHaveLength(1);
      expect(line.match(restore)).toHaveLength(1);
    }
  });

  it('writes colours in ASS byte order, not CSS order', () => {
    // Cream is #f4efe4, so ASS wants &H00E4EFF4.
    expect(buildAss(words, frame)).toContain('&H00E4EFF4');
  });

  it('scales with the frame, so a 4:5 cut is not captioned at 9:16 sizes', () => {
    const tall = buildAss(words, { width: 1080, height: 1920 });
    const wide = buildAss(words, { width: 1920, height: 1080 });
    expect(tall).toContain('PlayResY: 1920');
    expect(wide).toContain('PlayResY: 1080');
    expect(tall).not.toBe(wide);
  });

  it('escapes braces so a transcript cannot inject ASS markup', () => {
    const ass = buildAss([{ w: '{\\an8}gotcha', start: 0, end: 1 }], frame);
    expect(ass).toContain('\\{');
    expect(ass).not.toMatch(/,\{\\an8\}/);
  });

  it('holds each word until the next begins, so captions never flicker off', () => {
    const lines = buildAss(words, frame)
      .split('\n')
      .filter((l) => l.startsWith('Dialogue:'))
      .map((l) => l.split(',').slice(1, 3));

    for (let i = 0; i < lines.length - 1; i += 1) {
      expect(lines[i]![1]).toBe(lines[i + 1]![0]);
    }
  });
});

describe('SRT output', () => {
  it('writes one numbered block per window with comma milliseconds', () => {
    const srt = buildSrt(say('one two three four five six seven eight nine ten'));
    expect(srt).toMatch(/^1\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n/);
  });
});

describe('slicing a clip out of a transcript', () => {
  const words = say('zero one two three four five six seven eight nine', 0, 1);

  it('takes only the words that overlap the clip', () => {
    expect(wordsBetween(words, 3, 6).map((w) => w.w)).toEqual(['three', 'four', 'five']);
  });

  it('clips a word that straddles the edge rather than dropping it', () => {
    const [first] = wordsBetween(words, 3.5, 6);
    expect(first!.w).toBe('three');
    expect(first!.start).toBe(3.5);
  });

  it('shifts times so the clip starts at zero', () => {
    const shifted = shiftWords(wordsBetween(words, 3, 6), 3);
    expect(shifted[0]!.start).toBe(0);
    expect(shifted.every((w) => w.start >= 0)).toBe(true);
  });
});
