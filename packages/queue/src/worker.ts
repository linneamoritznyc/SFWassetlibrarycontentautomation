import type { Pool } from '@sfw/db';
import { startHeartbeat } from './heartbeat.js';
import { claim, complete, enqueue, fail } from './queue.js';
import type { HandlerMap, Job } from './types.js';

export type WorkerOptions = {
  pool: Pool;
  /** Shows up in worker_heartbeats and in every log line. */
  name: string;
  /** Job types this process claims. Usually from WORKER_TYPES. */
  types: string[];
  handlers: HandlerMap;
  /** How many jobs may run at once. Light 4, media and render 1. */
  concurrency?: number;
  /** How long to wait after finding nothing to do. */
  idleDelayMs?: number;
};

/**
 * The claim loop.
 *
 * Claims up to the number of free slots, runs each job, and marks it done or
 * failed. A handler that throws is a failure, and the queue handles the
 * backoff. A job type with no handler fails loudly rather than silently
 * sitting in the queue forever: that is nearly always a WORKER_TYPES that
 * disagrees with what this process can actually do.
 *
 * Shutdown is graceful. On SIGTERM it stops claiming and waits for jobs in
 * flight, so a Railway redeploy does not leave rows stuck in `running`.
 */
export function runWorker(options: WorkerOptions): { stop: () => Promise<void> } {
  const { pool, name, types, handlers } = options;
  const concurrency = options.concurrency ?? 1;
  const idleDelayMs = options.idleDelayMs ?? 2_000;

  const unknown = types.filter((t) => !handlers[t]);
  if (unknown.length > 0) {
    throw new Error(
      `[${name}] WORKER_TYPES asks for ${unknown.join(', ')}, which this worker has no handler for.`,
    );
  }

  let running = 0;
  let stopping = false;

  const stopHeartbeat = startHeartbeat(pool, name, types);

  async function runOne(job: Job): Promise<void> {
    running += 1;
    const started = Date.now();
    try {
      const handler = handlers[job.type];
      if (!handler) throw new Error(`No handler for job type "${job.type}"`);

      await handler({ job, enqueue: (input) => enqueue(pool, input) });

      await complete(pool, job.id);
      console.log(`[${name}] ${job.type} #${job.id} done in ${Date.now() - started}ms`);
    } catch (err) {
      const after = await fail(pool, job.id, err);
      const state = after?.status === 'dead' ? 'dead' : `retry in ${2 ** (after?.attempts ?? 1)}m`;
      console.error(`[${name}] ${job.type} #${job.id} failed (${state}):`, err);
    } finally {
      running -= 1;
    }
  }

  async function tick(): Promise<void> {
    while (!stopping) {
      const free = concurrency - running;
      if (free <= 0) {
        await sleep(100);
        continue;
      }

      let jobs: Job[] = [];
      try {
        jobs = await claim(pool, types, free);
      } catch (err) {
        console.error(`[${name}] could not claim:`, err);
        await sleep(idleDelayMs);
        continue;
      }

      if (jobs.length === 0) {
        await sleep(idleDelayMs);
        continue;
      }

      // Deliberately not awaited: the loop goes straight back to claiming so a
      // long job does not hold up the other slots.
      for (const job of jobs) void runOne(job);
    }
  }

  const loop = tick();

  async function stop(): Promise<void> {
    stopping = true;
    stopHeartbeat();
    await loop;
    while (running > 0) await sleep(100);
  }

  for (const signal of ['SIGTERM', 'SIGINT'] as const) {
    process.once(signal, () => {
      console.log(`[${name}] ${signal}, finishing ${running} job(s) in flight`);
      void stop().then(() => process.exit(0));
    });
  }

  console.log(`[${name}] claiming ${types.join(', ')} at concurrency ${concurrency}`);
  return { stop };
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/** Reads WORKER_TYPES, and checks it against what this worker can actually do. */
export function workerTypesFromEnv(available: string[]): string[] {
  const raw = (process.env.WORKER_TYPES ?? '').trim();
  if (!raw) return available;

  const asked = raw
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean);

  const unknown = asked.filter((t) => !available.includes(t));
  if (unknown.length > 0) {
    throw new Error(`WORKER_TYPES contains unknown types for this worker: ${unknown.join(', ')}`);
  }
  return asked;
}
