/**
 * Runs the test set on your own machine, the same checks `eval_nightly` runs.
 *
 *   node scripts/eval/dist/index.js                 the critic, with the model
 *   node scripts/eval/dist/index.js --no-model      the string checks only, free
 *   node scripts/eval/dist/index.js --prompt write  a different prompt
 *   node scripts/eval/dist/index.js --activate 3    promote a version that passed
 *
 * Use it before switching a prompt version on by hand. The nightly job does the
 * same thing and rolls back on a regression, but waiting until 4am to find out
 * a prompt is worse is a slow way to work.
 */
import { activatePrompt, passRate, runEval } from '@sfw/ai';
import { createPool } from '@sfw/db';

function arg(name: string): string | null {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? (process.argv[i + 1] ?? null) : null;
}

async function main(): Promise<void> {
  const pool = createPool();
  const promptName = arg('prompt') ?? 'critique';
  const useModel = !process.argv.includes('--no-model');

  try {
    const result = await runEval(pool, { promptName, useModel });
    const rate = passRate(result);

    console.log(`\n${promptName} v${result.promptVersion ?? '?'}`);
    console.log(useModel ? '' : 'String checks only, no model calls.\n');

    for (const testCase of result.cases) {
      const mark = testCase.passed ? 'pass' : 'FAIL';
      const score = testCase.score !== null ? ` (${testCase.score})` : '';
      console.log(`  ${mark}  ${testCase.name}${score}`);
      if (!testCase.passed) console.log(`        ${testCase.why}`);
    }

    console.log(
      `\n${result.passed} of ${result.passed + result.failed} (${Math.round(rate * 100)}%)\n`,
    );

    const activate = arg('activate');
    if (activate) {
      if (result.failed > 0) {
        console.error('Not activating: the test set did not pass.');
        process.exitCode = 1;
      } else {
        await activatePrompt(pool, promptName, Number(activate));
        console.log(`Activated ${promptName} v${activate}.`);
      }
    }

    if (result.failed > 0) process.exitCode = 1;
  } finally {
    await pool.end();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
