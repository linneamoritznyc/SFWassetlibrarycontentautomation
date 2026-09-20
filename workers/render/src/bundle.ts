import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { bundle } from '@remotion/bundler';
import { ENTRY_POINT } from '@sfw/remotion';

/**
 * Bundling the templates is slow, so it happens once per process and is reused
 * by every render after that.
 *
 * The entry point is resolved out of the installed `@sfw/remotion` package
 * rather than guessed from a relative path, so it works the same in the Docker
 * image as it does from the repository root.
 */
let bundled: Promise<string> | null = null;

export function templateBundle(): Promise<string> {
  if (!bundled) {
    const require = createRequire(import.meta.url);
    const packageJson = require.resolve('@sfw/remotion/package.json');
    const entry = join(dirname(packageJson), ENTRY_POINT);

    console.log(`[render] bundling ${entry}`);
    bundled = bundle({
      entryPoint: entry,
      onProgress: (percent) => {
        if (percent % 25 === 0) console.log(`[render] bundling ${percent}%`);
      },
      // The templates import each other with the `.js` extensions that Node's
      // ESM resolver needs, because `dist/index.js` is loaded by this worker
      // directly. Webpack resolves like a bundler and would look for a literal
      // `.js` file, so it is told to try the TypeScript sources too. Without
      // this the package would need two different import conventions in one
      // folder.
      webpackOverride: (config) => ({
        ...config,
        resolve: {
          ...config.resolve,
          extensionAlias: { '.js': ['.js', '.ts', '.tsx'] },
        },
      }),
    });
  }

  return bundled;
}
