import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { assFilter } from './ffmpeg.js';
import { brandFontsDir } from './fonts.js';

describe('brand fonts', () => {
  it('finds the font directory in the brand package', () => {
    const dir = brandFontsDir();
    expect(dir.endsWith(join('packages', 'brand', 'fonts'))).toBe(true);
    expect(existsSync(join(dir, 'Montserrat-SemiBold.ttf'))).toBe(true);
    // The licence sits beside the directory, not in it: libass tries to open
    // every file in `fontsdir` as a font.
    expect(existsSync(join(dir, '..', 'OFL-Montserrat.txt'))).toBe(true);
  });

  it('points libass at the brand font directory', () => {
    const filter = assFilter('/tmp/x/captions.ass', '/app/packages/brand/fonts');
    expect(filter).toBe("ass='/tmp/x/captions.ass':fontsdir='/app/packages/brand/fonts'");
  });

  it('escapes colons and backslashes in both paths', () => {
    const filter = assFilter('C:\\clips\\captions.ass', 'C:\\fonts');
    expect(filter).toBe("ass='C\\:/clips/captions.ass':fontsdir='C\\:/fonts'");
  });

  it('uses the repository fonts by default', () => {
    expect(assFilter('/tmp/captions.ass')).toContain(`fontsdir='${brandFontsDir()}'`);
  });
});
