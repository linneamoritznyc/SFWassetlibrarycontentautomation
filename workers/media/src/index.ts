import { runWorker, workerTypesFromEnv } from '@sfw/queue';
import { db } from './db.js';
import { AVAILABLE_TYPES, handlers } from './jobs/index.js';

/**
 * worker-media: FFmpeg and Whisper. Concurrency 1, because two ffmpeg runs on
 * one container fight over the CPU and finish later than they would in turn.
 */
runWorker({
  pool: db(),
  name: 'worker-media',
  types: workerTypesFromEnv(AVAILABLE_TYPES),
  handlers,
  concurrency: Number(process.env.WORKER_CONCURRENCY ?? 1),
});
