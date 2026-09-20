import { createPool, type Pool } from '@sfw/db';

let pool: Pool | null = null;

export function db(): Pool {
  if (!pool) pool = createPool();
  return pool;
}
