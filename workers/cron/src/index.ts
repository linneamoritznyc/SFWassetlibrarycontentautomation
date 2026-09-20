import { Cron } from 'croner';
import { createPool } from '@sfw/db';
import { enqueue } from '@sfw/queue';
import { SCHEDULES, TIMEZONE } from './schedule.js';

/**
 * The cron service. It inserts job rows and does nothing else.
 *
 * Two ways to run it, because Railway can do either:
 *
 *   node dist/index.js plan_week    enqueue one job and exit (Railway cron)
 *   node dist/index.js              stay up and fire on the schedule
 *
 * The one-shot form is what a Railway cron trigger calls. The long-running
 * form is for local development and for anywhere without a scheduler. Both
 * enqueue with the same dedupe key, so running both at once is harmless.
 */
const pool = createPool();

async function fire(job: string, at = new Date()): Promise<void> {
  const schedule = SCHEDULES.find((s) => s.job === job);
  const id = await enqueue(pool, {
    type: job,
    payload: { scheduled_at: at.toISOString() },
    priority: schedule?.priority ?? 5,
    dedupeKey: schedule?.dedupe?.(at) ?? `${job}:${at.toISOString().slice(0, 13)}`,
  });

  console.log(id ? `[cron] queued ${job} as job ${id}` : `[cron] ${job} already queued`);
}

async function main(): Promise<void> {
  const asked = process.argv[2];

  if (asked) {
    const known = SCHEDULES.some((s) => s.job === asked);
    if (!known) {
      console.error(
        `[cron] "${asked}" is not scheduled. Known: ${SCHEDULES.map((s) => s.job).join(', ')}`,
      );
      process.exitCode = 1;
      return;
    }

    await fire(asked);
    await pool.end();
    return;
  }

  console.log(`[cron] scheduling ${SCHEDULES.length} jobs in ${TIMEZONE}`);

  for (const schedule of SCHEDULES) {
    const task = new Cron(schedule.cron, { timezone: TIMEZONE }, () => {
      void fire(schedule.job).catch((err) => console.error(`[cron] ${schedule.job} failed:`, err));
    });
    console.log(
      `  ${schedule.cron.padEnd(12)} ${schedule.job.padEnd(20)} next ${task.nextRun()?.toISOString()}`,
    );
  }

  for (const signal of ['SIGTERM', 'SIGINT'] as const) {
    process.once(signal, () => {
      console.log(`[cron] ${signal}, stopping`);
      void pool.end().then(() => process.exit(0));
    });
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
