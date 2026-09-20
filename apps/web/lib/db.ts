import { createPool, type Pool } from '@sfw/db';

/**
 * One pool, kept on globalThis so a warm serverless instance reuses it instead
 * of opening a new pool per request. Point DATABASE_URL at Supabase's
 * transaction pooler (port 6543) in production.
 */
const globalForDb = globalThis as unknown as { sfwPool?: Pool };

export function db(): Pool {
  if (!globalForDb.sfwPool) globalForDb.sfwPool = createPool();
  return globalForDb.sfwPool;
}
