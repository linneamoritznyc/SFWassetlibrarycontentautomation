import type { Pool } from '@sfw/db';
import type { EnqueueInput, Job } from './types.js';

/**
 * Put a job on the queue.
 *
 * Returns the job id, or the id of the live job already holding the same
 * dedupe key. Never throws on a duplicate: asking twice for the same work is a
 * normal thing for a retrying caller to do.
 *
 * `id` comes back as a string because Postgres bigints do not fit in a JS
 * number, and node-postgres hands them over as strings for that reason.
 */
export async function enqueue(pool: Pool, input: EnqueueInput): Promise<string | null> {
  const res = await pool.query<{ enqueue_job: string | null }>(
    'select enqueue_job($1, $2::jsonb, $3, $4, $5) as enqueue_job',
    [
      input.type,
      JSON.stringify(input.payload ?? {}),
      input.priority ?? 5,
      input.dedupeKey ?? null,
      input.runAfter ?? new Date(),
    ],
  );
  return res.rows[0]?.enqueue_job ?? null;
}

/** Enqueue several jobs of the same type in one round trip. */
export async function enqueueMany(pool: Pool, inputs: EnqueueInput[]): Promise<(string | null)[]> {
  const ids: (string | null)[] = [];
  for (const input of inputs) {
    ids.push(await enqueue(pool, input));
  }
  return ids;
}

/**
 * Claim up to `limit` due jobs of these types and mark them running.
 *
 * Several workers can call this at once for the same types: the underlying
 * query uses FOR UPDATE SKIP LOCKED, so nobody blocks and no job is handed to
 * two workers.
 */
export async function claim(pool: Pool, types: string[], limit = 1): Promise<Job[]> {
  if (types.length === 0) return [];
  const res = await pool.query<Job>('select * from claim_job($1::text[], $2)', [types, limit]);
  return res.rows;
}

export async function complete(pool: Pool, jobId: string): Promise<Job | null> {
  const res = await pool.query<Job>('select * from complete_job($1)', [jobId]);
  return res.rows[0]?.id ? res.rows[0] : null;
}

/**
 * Record a failure. The job goes back on the queue with an exponential backoff
 * of 2^attempts minutes, or dies once it has used up max_attempts and shows up
 * in the Errors view.
 */
export async function fail(pool: Pool, jobId: string, error: unknown): Promise<Job | null> {
  const message = error instanceof Error ? `${error.message}\n${error.stack ?? ''}` : String(error);
  const res = await pool.query<Job>('select * from fail_job($1, $2)', [
    jobId,
    message.slice(0, 8000),
  ]);
  return res.rows[0]?.id ? res.rows[0] : null;
}

/** The Errors view's retry button. Null when a live job already holds the key. */
export async function retry(pool: Pool, jobId: string): Promise<Job | null> {
  const res = await pool.query<Job>('select * from retry_job($1)', [jobId]);
  return res.rows[0]?.id ? res.rows[0] : null;
}

export async function deadJobs(pool: Pool, limit = 100): Promise<Job[]> {
  const res = await pool.query<Job>(
    `select * from jobs where status = 'dead' order by updated_at desc limit $1`,
    [limit],
  );
  return res.rows;
}
