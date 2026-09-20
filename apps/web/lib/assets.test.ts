import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { createTestDatabase, seed, testDatabaseUrl, type Pool } from '@sfw/db';
import type { LibraryQuery, LibraryResult } from './assets';

const hasDb = Boolean(testDatabaseUrl());
const describeDb = hasDb ? describe : describe.skip;

if (!hasDb) {
  console.warn('TEST_DATABASE_URL is not set, skipping the library query tests.');
}

/**
 * The library query against a real database. These catch the things a type
 * checker cannot: parameter numbering, the facet counts running the same WHERE
 * clause as the rows, and filters that silently match everything.
 */
describeDb('library query', () => {
  let pool: Pool;
  let queryAssets: (query: LibraryQuery) => Promise<LibraryResult>;
  const ids: Record<string, string> = {};

  beforeAll(async () => {
    pool = await createTestDatabase('web');
    await seed(pool);

    // assets.ts opens its own pool from DATABASE_URL, so point it at this one
    // before the module is first imported.
    const url = new URL(testDatabaseUrl()!);
    url.pathname = '/sfw_test_web';
    process.env.DATABASE_URL = url.toString();
    ({ queryAssets } = await import('./assets'));

    const batch = await pool.query<{ id: string }>(
      `insert into batches (creator, workshop) values ('Linnea', 'Wild Ken Hill') returning id`,
    );
    const batchId = batch.rows[0]!.id;

    const add = async (
      name: string,
      type: string,
      status: string,
      description: string,
      tags: [string, string][],
    ) => {
      const res = await pool.query<{ id: string }>(
        `insert into assets (batch_id, type, filename, bucket, r2_key, status, description)
         values ($1, $2, $3, 'sfw-media', $4, $5, $6) returning id`,
        [batchId, type, `${name}.jpg`, `originals/${name}.jpg`, status, description],
      );
      const id = res.rows[0]!.id;
      ids[name] = id;

      for (const [facet, tagName] of tags) {
        await pool.query(
          `insert into asset_tags (asset_id, tag_id, source, confirmed, confidence)
           select $1, t.id, 'ai', $4, 0.9 from tags t where t.facet = $2 and t.name = $3`,
          [id, facet, tagName, true],
        );
      }
      return id;
    };

    await add('compost', 'photo', 'cleared', 'A steaming thermophilic pile', [
      ['subject', 'compost'],
      ['workshop', 'Wild Ken Hill'],
    ]);
    await add('nematode', 'photo', 'tagged', 'A bacterial-feeding nematode under the scope', [
      ['organism', 'nematodes'],
      ['subject', 'microscopy'],
    ]);
    await add('talk', 'video', 'tagged', 'Loida talking about failed piles', [
      ['subject', 'teaching'],
    ]);
    // No tags at all, so it is the only thing "Untagged" should find.
    await add('bare', 'photo', 'inbox', 'Nothing confirmed about this one', []);
  }, 60_000);

  afterAll(async () => {
    await pool?.end();
  });

  it('returns everything when nothing is filtered', async () => {
    const result = await queryAssets({});
    expect(result.total).toBe(4);
    expect(result.assets).toHaveLength(4);
  });

  it('filters by type', async () => {
    const result = await queryAssets({ type: ['video'] });
    expect(result.assets.map((a) => a.filename)).toEqual(['talk.jpg']);
  });

  it('filters by status', async () => {
    const result = await queryAssets({ status: ['cleared'] });
    expect(result.total).toBe(1);
  });

  it('requires every named tag, not just one of them', async () => {
    const both = await queryAssets({
      tags: [
        { facet: 'subject', name: 'compost' },
        { facet: 'workshop', name: 'Wild Ken Hill' },
      ],
    });
    expect(both.total).toBe(1);

    const impossible = await queryAssets({
      tags: [
        { facet: 'subject', name: 'compost' },
        { facet: 'organism', name: 'nematodes' },
      ],
    });
    expect(impossible.total).toBe(0);
  });

  it('finds only the asset with no confirmed tags under Untagged', async () => {
    const result = await queryAssets({ untagged: true });
    expect(result.assets.map((a) => a.filename)).toEqual(['bare.jpg']);
  });

  it('counts as Unused anything never used in a post', async () => {
    const before = await queryAssets({ unused: true });
    expect(before.total).toBe(4);

    const post = await pool.query<{ id: string }>(
      `insert into posts (platform, format, status, asset_ids)
       values ('instagram', 'feed', 'published', array[$1::uuid]) returning id`,
      [ids.compost],
    );
    await pool.query('insert into asset_usage (asset_id, post_id) values ($1, $2)', [
      ids.compost,
      post.rows[0]!.id,
    ]);

    const after = await queryAssets({ unused: true });
    expect(after.total).toBe(3);
    expect(after.assets.map((a) => a.filename)).not.toContain('compost.jpg');

    const used = await queryAssets({ type: ['photo'] });
    expect(used.assets.find((a) => a.filename === 'compost.jpg')?.used_in).toBe(1);
  });

  it('searches text across description, filename and creator', async () => {
    expect((await queryAssets({ q: 'nematode' })).total).toBe(1);
    expect((await queryAssets({ q: 'STEAMING' })).total).toBe(1);
    expect((await queryAssets({ q: 'nothing at all like this' })).total).toBe(0);
  });

  it('returns facet counts over the filtered set, not the whole library', async () => {
    const all = await queryAssets({});
    const subjects = all.facets.filter((f) => f.facet === 'subject');
    expect(subjects.map((f) => f.name).sort()).toEqual(['compost', 'microscopy', 'teaching']);

    // Narrow to one asset: the counts must narrow with it. This is the bit
    // that breaks if the facet query and the row query disagree about
    // parameters.
    const narrowed = await queryAssets({ type: ['video'] });
    expect(narrowed.facets.map((f) => f.name)).toEqual(['teaching']);
  });

  it('carries the batch provenance onto every asset', async () => {
    const result = await queryAssets({ q: 'compost' });
    expect(result.assets[0]?.workshop).toBe('Wild Ken Hill');
  });

  it('pages without losing the total', async () => {
    const page = await queryAssets({ limit: 2, offset: 0 });
    expect(page.assets).toHaveLength(2);
    expect(page.total).toBe(4);

    const second = await queryAssets({ limit: 2, offset: 2 });
    expect(second.assets).toHaveLength(2);
    expect(second.assets[0]?.id).not.toBe(page.assets[0]?.id);
  });
});
