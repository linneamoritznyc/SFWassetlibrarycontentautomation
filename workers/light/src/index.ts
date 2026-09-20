import { runWorker, workerTypesFromEnv } from '@sfw/queue';
import { db } from './db.js';
import { AVAILABLE_TYPES, handlers } from './jobs/index.js';

/**
 * worker-light: Claude calls, database work, the scout and the planner.
 * Concurrency 4, because these jobs are mostly waiting on an API.
 */
runWorker({
  pool: db(),
  name: 'worker-light',
  types: workerTypesFromEnv(AVAILABLE_TYPES),
  handlers,
  concurrency: Number(process.env.WORKER_CONCURRENCY ?? 4),
});
