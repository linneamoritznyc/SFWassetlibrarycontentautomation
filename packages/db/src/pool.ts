import { readFileSync } from 'node:fs';
import pg from 'pg';

/**
 * Workers talk to Postgres directly. The queue is a polling loop, and going
 * through PostgREST for it would mean an HTTP round trip every tick for work
 * that is one `update ... returning`. The web app uses supabase-js instead,
 * because it needs auth and the row-level query builder.
 *
 * DATABASE_URL is the connection string from the Supabase dashboard
 * (Project Settings, Database, Connection string, URI). Use the pooled one on
 * port 6543 for the workers.
 */
export function createPool(url = process.env.DATABASE_URL): pg.Pool {
  if (!url) {
    throw new Error('DATABASE_URL is not set. See .env.example and docs/TODO-LINNEA.md.');
  }

  return new pg.Pool({
    connectionString: url,
    max: Number(process.env.DATABASE_POOL_MAX ?? 5),
    // Supabase terminates idle connections; do not hold them open longer.
    idleTimeoutMillis: 10_000,
    connectionTimeoutMillis: 10_000,
    ssl: sslFor(url),
  });
}

function sslFor(url: string): pg.PoolConfig['ssl'] {
  // Local Postgres in tests has no TLS.
  if (url.includes('localhost') || url.includes('127.0.0.1')) return undefined;

  const ca = process.env.DATABASE_CA_CERT_PATH;
  if (ca) return { ca: readFileSync(ca, 'utf8') };

  // Supabase presents a certificate signed by a CA that is not in Node's
  // default store on every platform. Set DATABASE_CA_CERT_PATH in production;
  // see docs/TODO-LINNEA.md for where to download it.
  return { rejectUnauthorized: false };
}

export type Pool = pg.Pool;
export type PoolClient = pg.PoolClient;
