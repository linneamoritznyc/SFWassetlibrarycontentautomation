import { createPool, type Pool } from '@sfw/db';

let pool: Pool | null = null;

/** One pool per worker process, opened lazily so tests can skip it. */
export function db(): Pool {
  if (!pool) pool = createPool();
  return pool;
}
