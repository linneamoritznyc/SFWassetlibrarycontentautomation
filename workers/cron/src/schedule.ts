/**
 * Every schedule from backend spec section 5, in CET.
 *
 * The cron service only inserts job rows. It never does work, so a missed run
 * costs nothing but a delay, and two runs firing at once are absorbed by the
 * dedupe key rather than doing the work twice.
 */

export type Schedule = {
  /** Standard five-field cron, in the timezone below. */
  cron: string;
  job: string;
  /** Lower runs first. The Monday chain is ordered by its own times anyway. */
  priority?: number;
  /** Stops the same run being queued twice. Includes the date where it matters. */
  dedupe?: (now: Date) => string;
  why: string;
};

export const TIMEZONE = process.env.CRON_TIMEZONE ?? 'Europe/Berlin';

const day = (now: Date) => now.toISOString().slice(0, 10);
const hour = (now: Date) => now.toISOString().slice(0, 13);

export const SCHEDULES: Schedule[] = [
  {
    cron: '0 6 * * *',
    job: 'scout_fetch',
    why: 'Pull the soil source list before anyone is awake.',
    dedupe: (now) => `scout_fetch:${day(now)}`,
  },
  {
    cron: '30 6 * * *',
    job: 'scout_rank',
    why: 'Half an hour later, so the fetch has finished.',
    dedupe: (now) => `scout_rank:${day(now)}`,
  },

  // The Monday chain. Each step needs the one before it, which is why they are
  // half an hour apart rather than all at once.
  {
    cron: '0 5 * * 1',
    job: 'results_pull',
    priority: 2,
    why: 'Last week actually happened before anything is learned from it.',
    dedupe: (now) => `results_pull:${day(now)}`,
  },
  {
    cron: '30 5 * * 1',
    job: 'learn_weekly',
    priority: 2,
    why: 'Turn last week into rules and weights.',
    dedupe: (now) => `learn_weekly:${day(now)}`,
  },
  {
    cron: '0 6 * * 1',
    job: 'plan_week',
    priority: 2,
    why: 'Plan with the new weights.',
    dedupe: (now) => `plan_week:${day(now)}`,
  },
  {
    cron: '45 6 * * 1',
    job: 'write_batch',
    priority: 3,
    why: 'Write everything the planner proposed.',
    dedupe: (now) => `write_batch:${day(now)}`,
  },
  {
    cron: '30 7 * * 1',
    job: 'review_ready_notify',
    priority: 3,
    why: 'Tell Linnea the week is ready.',
    dedupe: (now) => `review_ready_notify:${day(now)}`,
  },

  {
    cron: '0 4 * * 0',
    job: 'eval_nightly',
    why: 'Run the test set against the active prompts.',
    dedupe: (now) => `eval_nightly:${day(now)}`,
  },
  {
    cron: '30 4 * * 0',
    job: 'web_refresh',
    why: 'Re-read the source pages and retire anything that changed.',
    dedupe: (now) => `web_refresh:${day(now)}`,
  },

  {
    cron: '0 * * * *',
    job: 'questions_nudge',
    priority: 8,
    why: 'One reminder after 48 hours, and only one.',
    dedupe: (now) => `questions_nudge:${hour(now)}`,
  },
];
