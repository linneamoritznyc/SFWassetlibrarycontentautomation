import { describe, expect, it } from 'vitest';
import { withUtm } from './export_bundle.js';

/** Every link in a post gets a UTM (CLAUDE.md section 10). */
describe('UTM tagging', () => {
  it('tags a plain link with the platform and the month', () => {
    const tagged = withUtm(
      'https://school.soilfoodweb.com/courses/india',
      'instagram',
      '2026-10-05',
    );
    const url = new URL(tagged!);
    expect(url.searchParams.get('utm_source')).toBe('instagram');
    expect(url.searchParams.get('utm_medium')).toBe('social');
    expect(url.searchParams.get('utm_campaign')).toBe('2026-10');
  });

  it('leaves a link that already has a UTM alone', () => {
    const already = 'https://soilfoodweb.com/?utm_source=newsletter&utm_campaign=spring';
    expect(
      new URL(withUtm(already, 'instagram', '2026-10-05')!).searchParams.get('utm_source'),
    ).toBe('newsletter');
  });

  it('keeps the existing query string', () => {
    const tagged = withUtm('https://soilfoodweb.com/courses?ref=bio', 'linkedin', '2026-10-05');
    expect(new URL(tagged!).searchParams.get('ref')).toBe('bio');
  });

  it('hands back something that is not a URL untouched rather than losing it', () => {
    expect(withUtm('link in bio', 'instagram', '2026-10-05')).toBe('link in bio');
  });

  it('passes null through', () => {
    expect(withUtm(null, 'instagram', '2026-10-05')).toBeNull();
  });

  it('falls back to organic when there is no date', () => {
    expect(
      new URL(withUtm('https://x.com/', 'facebook', null)!).searchParams.get('utm_campaign'),
    ).toBe('organic');
  });
});
