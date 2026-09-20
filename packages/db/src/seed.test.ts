import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { PROMPTS } from '@sfw/prompts';
import { FEEDS, PEOPLE, TAG_VOCABULARY, TEST_CASES } from '@sfw/shared';
import { seed, seedOnePrompt } from './seed.js';
import { createTestDatabase, testDatabaseUrl } from './testing.js';
import type { Pool } from './pool.js';

const hasDb = Boolean(testDatabaseUrl());
const describeDb = hasDb ? describe : describe.skip;

if (!hasDb) {
  console.warn('TEST_DATABASE_URL is not set, skipping the schema and seed tests.');
}

describeDb('schema and seed', () => {
  let pool: Pool;

  beforeAll(async () => {
    pool = await createTestDatabase('db');
    await seed(pool);
  }, 60_000);

  afterAll(async () => {
    await pool?.end();
  });

  async function one<T>(sql: string, params: unknown[] = []): Promise<T> {
    const { rows } = await pool.query(sql, params);
    return rows[0] as T;
  }

  /** Runs the seed's prompt rule against one made-up prompt. */
  async function activate(name: string, version: number, body: string): Promise<void> {
    await seedOnePrompt(pool, { name, version, body });
  }

  it('creates every table the spec names', async () => {
    const { rows } = await pool.query<{ tablename: string }>(
      `select tablename from pg_tables where schemaname = 'public'`,
    );
    const tables = rows.map((r) => r.tablename);

    for (const t of [
      'batches',
      'assets',
      'tags',
      'asset_tags',
      'transcripts',
      'people',
      'asset_people',
      'smart_folders',
      'sources',
      'facts',
      'rules',
      'questions',
      'feeds',
      'news_items',
      'stories',
      'posts',
      'post_versions',
      'renders',
      'canva_links',
      'metrics',
      'test_cases',
      'eval_runs',
      'prompts',
      'ai_calls',
      'jobs',
    ]) {
      expect(tables, `missing table ${t}`).toContain(t);
    }
  });

  it('has row level security on every table', async () => {
    const { rows } = await pool.query<{ tablename: string }>(
      `select tablename from pg_tables
       where schemaname = 'public' and not rowsecurity and tablename <> 'schema_migrations'`,
    );
    expect(rows.map((r) => r.tablename)).toEqual([]);
  });

  it('has no policies, so only a bypassrls role gets through', async () => {
    const { rows } = await pool.query(`select 1 from pg_policies where schemaname = 'public'`);
    expect(rows).toHaveLength(0);
  });

  it('seeds the whole tag vocabulary', async () => {
    const { n } = await one<{ n: number }>('select count(*)::int as n from tags');
    expect(n).toBe(TAG_VOCABULARY.length);

    const { n: pillars } = await one<{ n: number }>(
      `select count(*)::int as n from tags where facet = 'pillar'`,
    );
    expect(pillars).toBe(4);
  });

  it('seeds the people and the question-routing map', async () => {
    const { n } = await one<{ n: number }>('select count(*)::int as n from people');
    expect(n).toBe(PEOPLE.length);

    // programs -> Stephanie, mentors and graduates -> Carla, india and
    // partners -> Kavi, workshops -> Loida.
    const routes: [string, string][] = [
      ['programs', 'Stephanie McDaniel'],
      ['mentors', 'Carla Portugal'],
      ['graduates', 'Carla Portugal'],
      ['india', 'Kavi Reddy'],
      ['partners', 'Kavi Reddy'],
      ['workshops', 'Loida Vasquez'],
    ];

    for (const [topic, name] of routes) {
      const row = await one<{ name: string }>(
        'select name from people where $1 = any (topics) limit 1',
        [topic],
      );
      expect(row?.name, `${topic} should route to ${name}`).toBe(name);
    }
  });

  it('seeds the smart folders in their four sections', async () => {
    const { rows } = await pool.query<{ section: string; n: number }>(
      'select section, count(*)::int as n from smart_folders group by section order by section',
    );
    const bySection = Object.fromEntries(rows.map((r) => [r.section, r.n]));
    expect(bySection.workshops).toBeGreaterThan(0);
    expect(bySection.asset_types).toBeGreaterThan(0);
    expect(bySection.views).toBeGreaterThan(0);
  });

  it('seeds every prompt with exactly one active version', async () => {
    const { n } = await one<{ n: number }>('select count(*)::int as n from prompts');
    expect(n).toBe(PROMPTS.length);

    const { rows } = await pool.query<{ name: string; n: number }>(
      'select name, count(*) filter (where active)::int as n from prompts group by name',
    );
    for (const row of rows) {
      expect(row.n, `${row.name} should have one active version`).toBe(1);
    }
  });

  it('a new prompt version supersedes the old one before the first eval', async () => {
    // `prompts_one_active_idx` allows one active version per name, so the old
    // one has to be switched off before the new one comes on. Getting that
    // order wrong leaves the new version dormant and the feature silently
    // running last month's prompt.
    await pool.query(
      `insert into prompts (name, version, body, active)
       values ('scratch_prompt', 1, 'v1 body', true)`,
    );

    await activate('scratch_prompt', 2, 'v2 body');

    const { rows } = await pool.query<{ version: number; active: boolean }>(
      `select version, active from prompts where name = 'scratch_prompt' order by version`,
    );
    expect(rows).toEqual([
      { version: 1, active: false },
      { version: 2, active: true },
    ]);
  });

  it('a new prompt version waits for the eval once the prompt has been through one', async () => {
    await pool.query(
      `insert into prompts (name, version, body, active)
       values ('evalled_prompt', 1, 'v1 body', true)`,
    );
    await pool.query(
      `insert into eval_runs (prompt_name, prompt_version, passed, failed)
       values ('evalled_prompt', 1, 11, 0)`,
    );

    await activate('evalled_prompt', 2, 'v2 body');

    const { rows } = await pool.query<{ version: number; active: boolean }>(
      `select version, active from prompts where name = 'evalled_prompt' order by version`,
    );
    expect(rows).toEqual([
      { version: 1, active: true },
      { version: 2, active: false },
    ]);
  });

  it('gives every feed a region', async () => {
    const { n } = await one<{ n: number }>(
      'select count(*)::int as n from feeds where region is null',
    );
    expect(n).toBe(0);

    const { regions } = await one<{ regions: number }>(
      'select count(distinct region)::int as regions from feeds',
    );
    expect(regions).toBeGreaterThanOrEqual(5);
  });

  it('starts every feed healthy', async () => {
    const { n } = await one<{ n: number }>(
      `select count(*)::int as n from feeds
       where consecutive_failures <> 0 or last_error is not null`,
    );
    expect(n).toBe(0);
  });

  it('a re-seed does not switch a feed someone turned off back on', async () => {
    await pool.query(`update feeds set active = false where name = $1`, [FEEDS[0]!.name]);
    await seed(pool);
    const row = await one<{ active: boolean }>('select active from feeds where name = $1', [
      FEEDS[0]!.name,
    ]);
    expect(row.active).toBe(false);
    await pool.query(`update feeds set active = true where name = $1`, [FEEDS[0]!.name]);
  });

  it('seeds the eval test set with good and bad cases', async () => {
    const { n } = await one<{ n: number }>('select count(*)::int as n from test_cases');
    expect(n).toBe(TEST_CASES.length);

    const { good, bad } = await one<{ good: number; bad: number }>(
      `select count(*) filter (where kind = 'good')::int as good,
              count(*) filter (where kind = 'bad')::int as bad
       from test_cases`,
    );
    expect(good).toBeGreaterThanOrEqual(2);
    expect(bad).toBeGreaterThanOrEqual(5);
  });

  it('seeds the cadence', async () => {
    const row = await one<{ value: { feedDays: string[]; explorationShare: number } }>(
      `select value from settings where key = 'cadence'`,
    );
    expect(row.value.feedDays).toEqual(['mon', 'wed', 'fri']);
    expect(row.value.explorationShare).toBe(0.2);
  });

  it('is idempotent: seeding twice changes nothing', async () => {
    const before = await one<{ tags: number; people: number; prompts: number }>(
      `select (select count(*) from tags)::int as tags,
              (select count(*) from people)::int as people,
              (select count(*) from prompts)::int as prompts`,
    );
    await seed(pool);
    const after = await one<typeof before>(
      `select (select count(*) from tags)::int as tags,
              (select count(*) from people)::int as people,
              (select count(*) from prompts)::int as prompts`,
    );
    expect(after).toEqual(before);
  });

  it('a re-seed does not wipe an email someone filled in', async () => {
    await pool.query(`update people set email = 'someone@example.org' where name = $1`, [
      'Stephanie McDaniel',
    ]);
    await seed(pool);
    const row = await one<{ email: string }>('select email from people where name = $1', [
      'Stephanie McDaniel',
    ]);
    expect(row.email).toBe('someone@example.org');
  });

  it('tagging an asset enqueues exactly one embed job', async () => {
    const batch = await one<{ id: string }>(
      `insert into batches (creator) values ('test') returning id`,
    );
    const asset = await one<{ id: string }>(
      `insert into assets (batch_id, type, filename, bucket, r2_key)
       values ($1, 'photo', 'a.jpg', 'sfw-media', 'thumbs/a.jpg') returning id`,
      [batch.id],
    );

    await pool.query(`update assets set status = 'tagged' where id = $1`, [asset.id]);
    await pool.query(`update assets set status = 'cleared' where id = $1`, [asset.id]);
    await pool.query(`update assets set status = 'tagged' where id = $1`, [asset.id]);

    const { n } = await one<{ n: number }>(
      `select count(*)::int as n from jobs where type = 'embed' and payload->>'asset_id' = $1`,
      [asset.id],
    );
    expect(n).toBe(1);
  });

  it('refuses a post that has no material', async () => {
    await expect(
      pool.query(
        `insert into posts (platform, format, status) values ('instagram', 'feed', 'approved')`,
      ),
    ).rejects.toThrow(/post_has_material/);
  });

  it('allows a proposed post to be empty, because the planner fills it later', async () => {
    await expect(
      pool.query(
        `insert into posts (platform, format, status) values ('instagram', 'feed', 'proposed')`,
      ),
    ).resolves.toBeTruthy();
  });

  it('refuses a rejection with no reason', async () => {
    await expect(
      pool.query(
        `insert into posts (platform, format, status, asset_ids)
         values ('instagram', 'feed', 'rejected', array[gen_random_uuid()])`,
      ),
    ).rejects.toThrow(/rejection_has_reason/);
  });

  it('refuses a clip with no parent or range', async () => {
    const batch = await one<{ id: string }>(
      `insert into batches (creator) values ('test') returning id`,
    );
    await expect(
      pool.query(
        `insert into assets (batch_id, type, filename, bucket, r2_key)
         values ($1, 'clip', 'c.mp4', 'sfw-media', 'clips/c.mp4')`,
        [batch.id],
      ),
    ).rejects.toThrow(/clip_has_range/);
  });
});
