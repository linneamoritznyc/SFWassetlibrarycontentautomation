import { describe, expect, it } from 'vitest';
import { scopeFor } from './brief.js';

/**
 * Which rules a draft is held to. Getting this wrong means a LinkedIn post
 * checked against the Instagram rules, which is how a post ends up restating
 * org facts on the one platform where that performs worst.
 */
describe('rule scope', () => {
  it('sends LinkedIn posts to the LinkedIn rules whatever their format', () => {
    expect(scopeFor('linkedin', 'feed')).toBe('linkedin');
    expect(scopeFor('linkedin', 'carousel')).toBe('linkedin');
  });

  it('treats reels and shorts as reels, whichever platform they are on', () => {
    expect(scopeFor('instagram', 'reel')).toBe('reel');
    expect(scopeFor('youtube', 'short')).toBe('reel');
  });

  it('sends the rest of Instagram to the Instagram rules', () => {
    expect(scopeFor('instagram', 'feed')).toBe('instagram');
    expect(scopeFor('instagram', 'carousel')).toBe('instagram');
  });

  it('falls back to the caption rules', () => {
    expect(scopeFor('facebook', 'feed')).toBe('caption');
  });
});
