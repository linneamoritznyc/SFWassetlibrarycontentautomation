import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';

/**
 * Where the brand's font files live.
 *
 * Montserrat SemiBold is checked into `packages/brand/fonts` under the Open
 * Font License (the licence text is `packages/brand/OFL-Montserrat.txt`, kept
 * out of this directory because libass tries to open every file in it as a
 * font), so the caption burner does not depend on a download at image build
 * time or on fontconfig having been told about it. libass is pointed at
 * this directory directly (the `fontsdir` option on the `ass` filter), so a
 * developer laptop with nothing installed burns the same captions as the
 * Railway image.
 *
 * `@sfw/brand` resolves to `packages/brand/dist/index.js`, so the fonts are two
 * directories up from there. pnpm links the workspace package rather than
 * copying it, so this is the real repository path in development and
 * `/app/packages/brand/fonts` in the container.
 */
export function brandFontsDir(): string {
  const require = createRequire(import.meta.url);
  const entry = require.resolve('@sfw/brand');
  return join(dirname(dirname(entry)), 'fonts');
}
