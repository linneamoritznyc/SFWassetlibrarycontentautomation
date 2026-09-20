import { describe, expect, it } from 'vitest';
import { fixWords } from './edit_clip.js';
import type { Word } from '../captions.js';

const said = (text: string): Word[] =>
  text.split(' ').map((w, i) => ({ w, start: i * 0.4, end: i * 0.4 + 0.35 }));

/**
 * Whisper mishears names and jargon constantly, and a burned-in caption is the
 * one place a mistake cannot be quietly fixed later.
 */
describe('correcting what Whisper heard', () => {
  it('replaces a word everywhere it appears', () => {
    const words = fixWords(said('the vermacompost and more vermacompost'), [
      { from: 'vermacompost', to: 'vermicompost' },
    ]);
    expect(words.map((w) => w.w).join(' ')).toBe('the vermicompost and more vermicompost');
  });

  it('matches without caring about case', () => {
    const words = fixWords(said('Loyda said so'), [{ from: 'loyda', to: 'Loida' }]);
    expect(words[0]!.w).toBe('Loida');
  });

  it('keeps the punctuation attached to the original word', () => {
    const words = fixWords(said('it was Loyda, then Gerald.'), [{ from: 'loyda', to: 'Loida' }]);
    expect(words[2]!.w).toBe('Loida,');
  });

  it('leaves the timings alone, so the highlight still lands', () => {
    const before = said('the vermacompost pile');
    const after = fixWords(before, [{ from: 'vermacompost', to: 'vermicompost' }]);
    expect(after.map((w) => [w.start, w.end])).toEqual(before.map((w) => [w.start, w.end]));
  });

  it('does nothing when there is nothing to fix', () => {
    const words = said('nothing to correct here');
    expect(fixWords(words, [])).toBe(words);
    expect(fixWords(words, [{ from: 'absent', to: 'x' }])).toEqual(words);
  });

  it('does not match a word that merely contains the correction', () => {
    const words = fixWords(said('composting is not compost'), [{ from: 'compost', to: 'COMPOST' }]);
    expect(words[0]!.w).toBe('composting');
    expect(words[3]!.w).toBe('COMPOST');
  });
});
