import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import type { Pool } from './pool.js';

/**
 * Applies every file in supabase/migrations in filename order, once each.
 *
 * Supabase's own CLI (`supabase db push`) does the same thing for the hosted
 * project. This exists so the tests can build a database from nothing, and so
 * a migration can be applied to any Postgres with a connection string.
 */
export async function applyMigrations(pool: Pool, dir: string): Promise<string[]> {
  await pool.query(`
    create table if not exists schema_migrations (
      filename   text primary key,
      applied_at timestamptz not null default now()
    )
  `);

  const applied = new Set(
    (await pool.query<{ filename: string }>('select filename from schema_migrations')).rows.map(
      (r) => r.filename,
    ),
  );

  const files = readdirSync(dir)
    .filter((f) => f.endsWith('.sql'))
    .sort();

  const ran: string[] = [];

  for (const file of files) {
    if (applied.has(file)) continue;

    const sql = readFileSync(join(dir, file), 'utf8');
    const client = await pool.connect();
    try {
      await client.query('begin');
      await client.query(sql);
      await client.query('insert into schema_migrations (filename) values ($1)', [file]);
      await client.query('commit');
      ran.push(file);
    } catch (err) {
      await client.query('rollback');
      throw new Error(`Migration ${file} failed: ${(err as Error).message}`, { cause: err });
    } finally {
      client.release();
    }
  }

  return ran;
}
