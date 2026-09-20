import { describe, expect, it } from 'vitest';
import { mediaIdFrom } from './results_pull.js';

describe('reading an Instagram permalink', () => {
  it('handles posts, reels and IGTV', () => {
    expect(mediaIdFrom('https://www.instagram.com/p/CxYz123_-/')).toBe('CxYz123_-');
    expect(mediaIdFrom('https://instagram.com/reel/ABC999/')).toBe('ABC999');
    expect(mediaIdFrom('https://www.instagram.com/tv/DEF111/?utm_source=ig')).toBe('DEF111');
  });

  it('returns null for anything else', () => {
    expect(mediaIdFrom('https://soilfoodweb.com')).toBeNull();
    expect(mediaIdFrom('https://www.instagram.com/soilfoodwebschool/')).toBeNull();
  });
});
