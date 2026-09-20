import { describe, expect, it } from 'vitest';
import { barelyEdited, diffCaption, sentences, words } from './diff.js';

describe('word splitting', () => {
  it('keeps hashtags and handles, which are part of a caption', () => {
    expect(words('#SoilFoodWeb with @visionary_permaculture')).toContain('#soilfoodweb');
    expect(words('#SoilFoodWeb with @visionary_permaculture')).toContain('@visionary_permaculture');
  });

  it('drops punctuation so a full stop is not a change', () => {
    expect(words('Dark, crumbly soil.')).toEqual(['dark', 'crumbly', 'soil']);
  });
});

describe('sentence splitting', () => {
  it('splits on terminators and newlines', () => {
    expect(sentences('One. Two!\nThree?')).toEqual(['One.', 'Two!', 'Three?']);
  });
});

describe('measuring an edit', () => {
  it('is zero when nothing changed', () => {
    const text = 'Finished vermicompost should be dark and crumbly.';
    expect(diffCaption(text, text).ratio).toBe(0);
  });

  it('ignores punctuation and case', () => {
    expect(diffCaption('Dark and crumbly.', 'dark and crumbly').ratio).toBe(0);
  });

  it('counts a small tweak as a small edit', () => {
    const before =
      'Finished vermicompost should be dark and crumbly and hold together when squeezed.';
    const after =
      'Finished vermicompost should be dark and crumbly and hold together when pressed.';
    const diff = diffCaption(before, after);

    expect(diff.ratio).toBeLessThan(0.1);
    expect(barelyEdited(diff)).toBe(true);
    expect(diff.removedWords).toBe(1);
    expect(diff.addedWords).toBe(1);
  });

  it('counts a rewrite as a large edit', () => {
    const diff = diffCaption(
      'Healthy soil is the foundation of everything we grow.',
      'Pratik checks moisture between 50 and 70 percent before he calls a batch finished.',
    );
    expect(diff.ratio).toBeGreaterThan(0.6);
    expect(barelyEdited(diff)).toBe(false);
  });

  it('is one when nothing survived', () => {
    expect(diffCaption('one two three', 'four five six').ratio).toBe(1);
  });

  it('does not treat a reordered sentence as a full rewrite', () => {
    const a = 'The pile heats. The worms arrive later.';
    const b = 'The worms arrive later. The pile heats.';
    expect(diffCaption(a, b).ratio).toBe(0);
  });

  it('names the sentences that were dropped and added', () => {
    const diff = diffCaption(
      'Soil is alive. Skip the bag. Feed the web instead.',
      'Soil is alive. Pratik checks four things before he calls a batch done.',
    );

    expect(diff.removedSentences).toContain('Skip the bag.');
    expect(diff.addedSentences.join(' ')).toContain('Pratik');
    expect(diff.removedSentences).not.toContain('Soil is alive.');
  });

  it('handles an empty draft without dividing by zero', () => {
    expect(diffCaption('', '').ratio).toBe(0);
    expect(diffCaption('', 'something new').ratio).toBe(0.5);
  });

  it('counts a repeated word as many times as it appears', () => {
    const diff = diffCaption('soil soil soil', 'soil');
    expect(diff.removedWords).toBe(2);
  });
});
