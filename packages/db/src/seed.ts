import {
  CADENCE,
  FEEDS,
  SOURCE_PAGES,
  FORMAT_WEIGHTS,
  PEOPLE,
  PILLARS,
  SMART_FOLDERS,
  TAG_VOCABULARY,
  TEST_CASES,
} from '@sfw/shared';
import { PROMPTS } from '@sfw/prompts';
import type { Pool } from './pool.js';

/**
 * Seeds the reference data the system cannot start without: the tag
 * vocabulary, the smart folders, the people and the question routing, the
 * cadence, the starting planner weights, every prompt, and the eval test set.
 *
 * Idempotent. Run it as often as you like. It upserts by natural key and never
 * deletes, so a tag someone added by hand survives a re-seed.
 *
 * Prompts are seeded as inactive when a version is new, except on a database
 * that has no active version of that prompt yet. A prompt change therefore
 * cannot reach production just by being deployed: something has to run the
 * test set and activate it.
 */
export async function seed(pool: Pool): Promise<Record<string, number>> {
  const counts: Record<string, number> = {};

  counts.tags = await seedTags(pool);
  counts.smart_folders = await seedSmartFolders(pool);
  counts.people = await seedPeople(pool);
  counts.settings = await seedSettings(pool);
  counts.planner_weights = await seedPlannerWeights(pool);
  counts.prompts = await seedPrompts(pool);
  counts.test_cases = await seedTestCases(pool);
  counts.sources = await seedSources(pool);
  counts.feeds = await seedFeeds(pool);

  return counts;
}

async function seedTags(pool: Pool): Promise<number> {
  const res = await pool.query(
    `insert into tags (name, facet)
     select * from unnest($1::text[], $2::text[])
     on conflict (name, facet) do nothing`,
    [TAG_VOCABULARY.map((t) => t.name), TAG_VOCABULARY.map((t) => t.facet)],
  );
  return res.rowCount ?? 0;
}

async function seedSmartFolders(pool: Pool): Promise<number> {
  let n = 0;
  for (const f of SMART_FOLDERS) {
    const res = await pool.query(
      `insert into smart_folders (name, section, filters, position)
       values ($1, $2, $3::jsonb, $4)
       on conflict (section, name) do update
         set filters = excluded.filters, position = excluded.position`,
      [f.name, f.section, JSON.stringify(f.filters), f.position],
    );
    n += res.rowCount ?? 0;
  }
  return n;
}

async function seedPeople(pool: Pool): Promise<number> {
  let n = 0;
  for (const p of PEOPLE) {
    // Email is left alone on update: once a real address is filled in, a
    // re-seed must not wipe it back to null.
    const res = await pool.query(
      `insert into people (name, role, org, topics, notes)
       values ($1, $2, $3, $4::text[], $5)
       on conflict (name) do update
         set role = excluded.role,
             org = excluded.org,
             topics = excluded.topics,
             notes = excluded.notes`,
      [p.name, p.role, p.org, p.topics, p.notes ?? null],
    );
    n += res.rowCount ?? 0;
  }
  return n;
}

async function seedSettings(pool: Pool): Promise<number> {
  const rows: [string, unknown][] = [
    ['cadence', CADENCE],
    // Feature flags. Canva autofill stays off until Canva approves the access
    // request; see docs/TODO-LINNEA.md.
    ['flags', { canva_enabled: false, canva_autofill: false, speaker_tracking_crop: false }],
  ];

  let n = 0;
  for (const [key, value] of rows) {
    // Settings are editable from the Settings view, so a re-seed must not
    // overwrite a value someone changed. Insert only.
    const res = await pool.query(
      `insert into settings (key, value) values ($1, $2::jsonb)
       on conflict (key) do nothing`,
      [key, JSON.stringify(value)],
    );
    n += res.rowCount ?? 0;
  }
  return n;
}

async function seedPlannerWeights(pool: Pool): Promise<number> {
  const rows = [
    ...FORMAT_WEIGHTS.map((k) => ({ key: k, kind: 'format' })),
    ...PILLARS.map((k) => ({ key: k, kind: 'pillar' })),
  ];

  let n = 0;
  for (const r of rows) {
    // learn_weekly owns these after the first week. Never overwrite.
    const res = await pool.query(
      `insert into planner_weights (key, kind, weight) values ($1, $2, 1.0)
       on conflict (key) do nothing`,
      [r.key, r.kind],
    );
    n += res.rowCount ?? 0;
  }
  return n;
}

async function seedPrompts(pool: Pool): Promise<number> {
  let n = 0;
  for (const p of PROMPTS) {
    n += await seedOnePrompt(pool, p);
  }
  return n;
}

/**
 * Stores one prompt version and decides whether it goes live.
 *
 * A new version is activated only when nothing is active yet, or when this
 * prompt has never been through the eval. The rule that a prompt change must
 * pass the test set protects a *running* system; before the first eval there
 * is nothing to protect, and leaving a brand new prompt dormant would only
 * mean the feature silently does nothing.
 *
 * Exported for the tests, which need to run the rule against a prompt they
 * made up rather than against the real list.
 *
 * @returns 1 if the version was new, 0 if it already existed.
 */
export async function seedOnePrompt(
  pool: Pool,
  p: { name: string; version: number; body: string },
): Promise<number> {
  const inserted = await pool.query(
    `insert into prompts (name, version, body, active)
     values ($1, $2, $3, false)
     on conflict (name, version) do update set body = excluded.body
     returning id, (xmax = 0) as is_new`,
    [p.name, p.version, p.body],
  );
  const isNew = (inserted.rows[0] as { is_new: boolean } | undefined)?.is_new ? 1 : 0;

  const state = await pool.query<{
    has_active: boolean;
    has_eval: boolean;
    already: boolean;
  }>(
    `select
       exists (select 1 from prompts where name = $1 and active) as has_active,
       exists (select 1 from eval_runs where prompt_name = $1) as has_eval,
       exists (select 1 from prompts where name = $1 and version = $2 and active) as already`,
    [p.name, p.version],
  );

  const row = state.rows[0];
  if (!row || row.already) return isNew;
  if (row.has_active && row.has_eval) return isNew;

  // `prompts_one_active_idx` allows exactly one active version per name, so
  // the old version has to be switched off *before* the new one comes on, and
  // both have to happen on one connection inside one transaction or a crash in
  // between would leave the prompt with no active version at all.
  const client = await pool.connect();
  try {
    await client.query('begin');
    await client.query(`update prompts set active = false where name = $1 and active`, [p.name]);
    await client.query(`update prompts set active = true where name = $1 and version = $2`, [
      p.name,
      p.version,
    ]);
    await client.query('commit');
  } catch (err) {
    await client.query('rollback');
    throw err;
  } finally {
    client.release();
  }

  return isNew;
}

async function seedFeeds(pool: Pool): Promise<number> {
  let n = 0;
  for (const feed of FEEDS) {
    // A feed the scout has repaired no longer sits at its seeded URL, so
    // matching on `url` alone would find nothing, insert the broken URL again
    // as a second row, and undo the repair every time anyone re-seeds. Such a
    // row is matched on where it came from instead, and keeps its new URL.
    const moved = await pool.query(
      `update feeds set name = $1, kind = $3, region = $4 where previous_url = $2`,
      [feed.name, feed.url, feed.kind, feed.region],
    );

    if ((moved.rowCount ?? 0) > 0) {
      n += moved.rowCount ?? 0;
      continue;
    }

    // `active` is left alone on update: turning a dead feed off in Settings
    // must survive a re-seed.
    const res = await pool.query(
      `insert into feeds (name, url, kind, region, active) values ($1, $2, $3, $4, true)
       on conflict (url) do update
         set name = excluded.name, kind = excluded.kind, region = excluded.region`,
      [feed.name, feed.url, feed.kind, feed.region],
    );
    n += res.rowCount ?? 0;
  }
  return n;
}

async function seedSources(pool: Pool): Promise<number> {
  let n = 0;
  for (const source of SOURCE_PAGES) {
    // fetched_at and content_hash are left alone: web_fetch owns them, and a
    // re-seed must not make an already-read page look unread.
    const res = await pool.query(
      `insert into sources (kind, ref, title) values ('url', $1, $2)
       on conflict (kind, ref) do update set title = excluded.title`,
      [source.url, source.title],
    );
    n += res.rowCount ?? 0;
  }
  return n;
}

async function seedTestCases(pool: Pool): Promise<number> {
  let n = 0;
  for (const t of TEST_CASES) {
    const res = await pool.query(
      `insert into test_cases (name, kind, input, expected, notes)
       values ($1, $2, $3::jsonb, $4::jsonb, $5)
       on conflict (name) do update
         set kind = excluded.kind,
             input = excluded.input,
             expected = excluded.expected,
             notes = excluded.notes`,
      [t.name, t.kind, JSON.stringify(t.input), JSON.stringify(t.expected), t.notes],
    );
    n += res.rowCount ?? 0;
  }
  return n;
}
