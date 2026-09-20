import { runWorker, workerTypesFromEnv } from '@sfw/queue';
import { db } from './db.js';
import { AVAILABLE_TYPES, handlers } from './jobs/index.js';

/**
 * worker-render: Remotion and Chromium. Concurrency 1, because a render is
 * already using every core it can and a second browser would only swap.
 */
runWorker({
  pool: db(),
  name: 'worker-render',
  types: workerTypesFromEnv(AVAILABLE_TYPES),
  handlers,
  concurrency: Number(process.env.WORKER_CONCURRENCY ?? 1),
});
