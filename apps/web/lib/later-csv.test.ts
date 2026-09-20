import { describe, expect, it } from 'vitest';
import { parseLaterCsv, splitRows } from './later-csv';

describe('CSV splitting', () => {
  it('handles a quoted cell containing a comma', () => {
    expect(splitRows('a,"b,c",d')).toEqual([['a', 'b,c', 'd']]);
  });

  it('handles an escaped quote inside a quoted cell', () => {
    expect(splitRows('a,"say ""hi""",c')).toEqual([['a', 'say "hi"', 'c']]);
  });

  it('handles a newline inside a quoted cell, which a caption always has', () => {
    expect(splitRows('caption,reach\n"line one\nline two",42')).toEqual([
      ['caption', 'reach'],
      ['line one\nline two', '42'],
    ]);
  });

  it('copes with Windows line endings', () => {
    expect(splitRows('a,b\r\nc,d')).toEqual([
      ['a', 'b'],
      ['c', 'd'],
    ]);
  });
});

describe('reading a Later export', () => {
  it('matches columns by what the header contains, not an exact name', () => {
    const csv = [
      'Post URL,Published Date,Impressions,Likes,Comments,Saved,Shares,Website Clicks',
      'https://instagram.com/p/ABC123/,2026-09-16,5120,310,22,180,14,45',
    ].join('\n');

    const { rows, unmatched } = parseLaterCsv(csv);
    expect(unmatched).toEqual([]);
    expect(rows[0]).toEqual({
      permalink: 'https://instagram.com/p/ABC123/',
      postedAt: '2026-09-16',
      reach: 5120,
      likes: 310,
      comments: 22,
      saves: 180,
      shares: 14,
      linkClicks: 45,
    });
  });

  it('says which columns it could not find rather than importing zeros', () => {
    const { unmatched } = parseLaterCsv('Post URL,Likes\nhttps://x/p/A/,10');
    expect(unmatched).toContain('saves');
    expect(unmatched).toContain('shares');
  });

  it('strips thousands separators', () => {
    const { rows } = parseLaterCsv('Post URL,Reach\nhttps://x/p/A/,"12,480"');
    expect(rows[0]!.reach).toBe(12480);
  });

  it('understands the abbreviated form Later sometimes writes', () => {
    const { rows } = parseLaterCsv('Post URL,Reach\nhttps://x/p/A/,2.1k');
    expect(rows[0]!.reach).toBe(2100);
  });

  it('gives null rather than zero for a blank cell', () => {
    const { rows } = parseLaterCsv('Post URL,Reach,Saved\nhttps://x/p/A/,,7');
    expect(rows[0]!.reach).toBeNull();
    expect(rows[0]!.saves).toBe(7);
  });

  it('ignores blank lines at the end of the file', () => {
    const { rows } = parseLaterCsv('Post URL,Reach\nhttps://x/p/A/,10\n\n');
    expect(rows).toHaveLength(1);
  });

  it('returns nothing for a header with no rows', () => {
    expect(parseLaterCsv('Post URL,Reach').rows).toEqual([]);
  });
});
