import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import pg from 'pg';
import { applyMigrations } from './migrate.js';
import { createPool, type Pool } from './pool.js';

/**
 * Builds a throwaway database, applies every migration to it and hands back a
 * pool. Each test file gets its own so they cannot tread on each other when
 * Turborepo runs them in parallel.
 *
 * Set TEST_DATABASE_URL to a Postgres the test user can create databases on,
 * with the `vector` and `pgcrypto` extensions available. Tests that need it
 * skip themselves when it is unset, so `pnpm test` still passes on a machine
 * with no database.
 *
 *   postgres://postgres@127.0.0.1:5433/postgres
 */
export function testDatabaseUrl(): string | null {
  return process.env.TEST_DATABASE_URL ?? null;
}

export const MIGRATIONS_DIR = resolve(
  dirname(fileURLToPath(import.meta.url)),
  '../../../supabase/migrations',
);

export async function createTestDatabase(name: string): Promise<Pool> {
  const base = testDatabaseUrl();
  if (!base) throw new Error('TEST_DATABASE_URL is not set');

  const dbName = `sfw_test_${name}`.toLowerCase().replace(/[^a-z0-9_]/g, '_');

  const admin = new pg.Client({ connectionString: base });
  await admin.connect();
  try {
    // Identifiers cannot be parameterised, so the name is scrubbed above.
    await admin.query(`drop database if exists ${dbName} with (force)`);
    await admin.query(`create database ${dbName}`);
  } finally {
    await admin.end();
  }

  const url = new URL(base);
  url.pathname = `/${dbName}`;

  const pool = createPool(url.toString());
  await applyMigrations(pool, MIGRATIONS_DIR);
  return pool;
}
