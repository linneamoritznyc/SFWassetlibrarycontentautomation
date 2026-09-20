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
    const inserted = await pool.query(
      `insert into prompts (name, version, body, active)
       values ($1, $2, $3, false)
       on conflict (name, version) do update set body = excluded.body
       returning id`,
      [p.name, p.version, p.body],
    );
    n += inserted.rowCount ?? 0;

    // First time this prompt has been seeded at all: activate it, otherwise
    // nothing could ever run. Later versions arrive inactive and wait for the
    // eval to promote them.
    await pool.query(
      `update prompts set active = true
       where name = $1 and version = $2
         and not exists (select 1 from prompts where name = $1 and active)`,
      [p.name, p.version],
    );
  }
  return n;
}

async function seedFeeds(pool: Pool): Promise<number> {
  let n = 0;
  for (const feed of FEEDS) {
    // `active` is left alone on update: turning a dead feed off in Settings
    // must survive a re-seed.
    const res = await pool.query(
      `insert into feeds (name, url, kind, active) values ($1, $2, $3, true)
       on conflict (url) do update set name = excluded.name, kind = excluded.kind`,
      [feed.name, feed.url, feed.kind],
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
