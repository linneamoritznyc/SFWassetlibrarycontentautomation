import { describe, expect, it } from 'vitest';
import { BUCKETS, bucketForType, keys, safeFilename } from './keys.js';

describe('R2 key layout', () => {
  it('builds every path in the spec', () => {
    expect(keys.original('a1', 'clip.mov')).toBe('originals/a1/clip.mov');
    expect(keys.thumb('a1')).toBe('thumbs/a1.jpg');
    expect(keys.proxy('a1')).toBe('proxies/a1.mp4');
    expect(keys.audio('a1')).toBe('audio/a1.m4a');
    expect(keys.clip('c1', '9x16')).toBe('clips/c1/9x16.mp4');
    expect(keys.captions('c1')).toBe('clips/c1/captions.srt');
    expect(keys.render('r1')).toBe('renders/r1.mp4');
    expect(keys.design('p1', 3)).toBe('designs/p1/3.png');
    expect(keys.doc('d1', 'report.pdf')).toBe('docs/d1/report.pdf');
  });

  it('sends video originals to the Infrequent Access bucket and the rest to Standard', () => {
    expect(bucketForType('video')).toBe(BUCKETS.raw);
    for (const type of ['photo', 'graphic', 'doc', 'clip', 'render', 'reference']) {
      expect(bucketForType(type)).toBe(BUCKETS.media);
    }
  });

  it('will not let a filename escape its folder', () => {
    // Separators collapse to underscores, so no traversal survives. The dots
    // that are left are just characters in a name.
    expect(safeFilename('../../etc/passwd')).toBe('_.._etc_passwd');
    expect(keys.original('a1', '../../evil.mp4')).toBe('originals/a1/_.._evil.mp4');
    expect(safeFilename('a\\b/c.jpg')).toBe('a_b_c.jpg');

    for (const nasty of ['../../etc/passwd', 'a\\b/c.jpg', '/absolute/path.jpg']) {
      expect(safeFilename(nasty)).not.toMatch(/[\\/]/);
    }
  });

  it('strips leading dots so nothing becomes a hidden file', () => {
    expect(safeFilename('...hidden.jpg')).toBe('hidden.jpg');
  });

  it('falls back to a name rather than an empty key', () => {
    expect(safeFilename('   ')).toBe('file');
    expect(safeFilename('...')).toBe('file');
  });

  it('keeps keys to a sane length', () => {
    expect(safeFilename('x'.repeat(500))).toHaveLength(200);
  });
});
