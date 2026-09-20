/**
 * Applies the migrations and seeds the reference data.
 *
 *   pnpm db:migrate     apply every migration that has not run yet
 *   pnpm db:seed        upsert tags, folders, people, prompts, test cases
 *   pnpm db:setup       both, in that order
 *
 * Reads DATABASE_URL. Safe to run repeatedly: migrations are recorded in
 * schema_migrations and the seed is idempotent.
 */
import { applyMigrations } from './migrate.js';
import { createPool } from './pool.js';
import { seed } from './seed.js';
import { MIGRATIONS_DIR } from './testing.js';

const command = process.argv[2] ?? 'setup';

async function main(): Promise<void> {
  const pool = createPool();

  try {
    if (command === 'migrate' || command === 'setup') {
      const ran = await applyMigrations(pool, MIGRATIONS_DIR);
      console.log(ran.length ? `Applied: ${ran.join(', ')}` : 'No new migrations.');
    }

    if (command === 'seed' || command === 'setup') {
      const counts = await seed(pool);
      const written = Object.entries(counts)
        .map(([k, v]) => `${k} ${v}`)
        .join(', ');
      console.log(`Seeded: ${written}`);
    }

    if (!['migrate', 'seed', 'setup'].includes(command)) {
      console.error(`Unknown command "${command}". Use migrate, seed or setup.`);
      process.exitCode = 1;
    }
  } finally {
    await pool.end();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
