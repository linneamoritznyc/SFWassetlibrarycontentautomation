import type { Pool } from '@sfw/db';

export type LoadedPrompt = { name: string; version: number; body: string };

/**
 * Loads the active version of a prompt at job start, as the spec requires.
 * Workers read the table, never the files in `@sfw/prompts`: those are the seed
 * texts, and the table is what is actually live.
 */
export async function loadPrompt(pool: Pool, name: string): Promise<LoadedPrompt> {
  const { rows } = await pool.query<LoadedPrompt>(
    'select name, version, body from prompts where name = $1 and active limit 1',
    [name],
  );

  const prompt = rows[0];
  if (!prompt) {
    throw new Error(
      `No active prompt named "${name}". Run \`pnpm db:seed\`, or activate a version.`,
    );
  }
  return prompt;
}

/** Promotes a version, leaving exactly one active. Used by the eval. */
export async function activatePrompt(pool: Pool, name: string, version: number): Promise<void> {
  const client = await pool.connect();
  try {
    await client.query('begin');
    await client.query('update prompts set active = false where name = $1 and active', [name]);
    const res = await client.query(
      'update prompts set active = true where name = $1 and version = $2',
      [name, version],
    );
    if (res.rowCount === 0) throw new Error(`No prompt ${name} v${version} to activate.`);
    await client.query('commit');
  } catch (err) {
    await client.query('rollback');
    throw err;
  } finally {
    client.release();
  }
}

/** The version before the active one. eval_nightly rolls back to this. */
export async function previousVersion(pool: Pool, name: string): Promise<number | null> {
  const { rows } = await pool.query<{ version: number }>(
    `select version from prompts
     where name = $1 and version < (select version from prompts where name = $1 and active)
     order by version desc limit 1`,
    [name],
  );
  return rows[0]?.version ?? null;
}
