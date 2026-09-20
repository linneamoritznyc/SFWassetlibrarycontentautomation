import { passRate, runEval } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { db } from '../db.js';
import { appUrl, sendEmail } from '../notify.js';

/** A drop this big against the last run means something broke. */
const REGRESSION = 0.1;

/**
 * Runs the test set against the active prompts.
 *
 * If the pass rate has dropped by more than ten points against the last
 * recorded run, the active prompt is rolled back to the previous version and
 * Linnea is told. That is the safety rail under everything `learn_weekly`
 * does: a rule or a prompt that makes the system worse gets undone by a
 * machine at four in the morning rather than by someone noticing next month.
 */
export const evalNightly = handler<{ prompt?: string }>(async ({ job }) => {
  const pool = db();
  const promptName = job.payload.prompt ?? 'critique';

  const result = await runEval(pool, { promptName, jobId: job.id });
  const rate = passRate(result);

  const previous = (
    await pool.query<{ passed: number; failed: number; prompt_version: number }>(
      `select passed, failed, prompt_version from eval_runs
       where prompt_name = $1 order by created_at desc limit 1`,
      [promptName],
    )
  ).rows[0];

  await pool.query(
    `insert into eval_runs (prompt_name, prompt_version, passed, failed, details)
     values ($1, $2, $3, $4, $5::jsonb)`,
    [
      promptName,
      result.promptVersion,
      result.passed,
      result.failed,
      JSON.stringify({ rate, cases: result.cases }),
    ],
  );

  const failures = result.cases.filter((c) => !c.passed);
  console.log(
    `[eval_nightly] ${promptName} v${result.promptVersion}: ${result.passed}/${result.passed + result.failed}`,
  );
  for (const failure of failures) console.log(`  ${failure.name}: ${failure.why}`);

  if (!previous) return;

  const before = passRate(previous);
  if (rate >= before - REGRESSION) return;

  // Worse than it was. Put the old version back.
  const rolledBackTo = await rollBack(pool, promptName);

  const message = [
    `The ${promptName} prompt got worse overnight.`,
    '',
    `Before: ${Math.round(before * 100)}% (v${previous.prompt_version})`,
    `Now:    ${Math.round(rate * 100)}% (v${result.promptVersion})`,
    '',
    rolledBackTo
      ? `Rolled back to v${rolledBackTo}. Nothing is broken, but the change that caused this is still in the prompts table, inactive.`
      : 'There was no earlier version to roll back to, so the current one is still active.',
    '',
    'What failed:',
    ...failures.map((f) => `  - ${f.name}: ${f.why}`),
    '',
    appUrl('/learned'),
  ].join('\n');

  await sendEmail({
    to: process.env.NOTIFY_EMAIL ?? 'linnea@soilfoodweb.com',
    subject: `Prompt regression: ${promptName} rolled back`,
    text: message,
  });

  console.warn(`[eval_nightly] regression, rolled back ${promptName}`);
});

async function rollBack(pool: ReturnType<typeof db>, name: string): Promise<number | null> {
  const client = await pool.connect();
  try {
    await client.query('begin');

    const previous = await client.query<{ version: number }>(
      `select version from prompts
       where name = $1 and version < (select version from prompts where name = $1 and active)
       order by version desc limit 1`,
      [name],
    );

    const version = previous.rows[0]?.version;
    if (!version) {
      await client.query('rollback');
      return null;
    }

    await client.query('update prompts set active = false where name = $1 and active', [name]);
    await client.query('update prompts set active = true where name = $1 and version = $2', [
      name,
      version,
    ]);

    await client.query('commit');
    return version;
  } catch (err) {
    await client.query('rollback');
    throw err;
  } finally {
    client.release();
  }
}
