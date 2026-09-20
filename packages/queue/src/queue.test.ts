import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { createTestDatabase, testDatabaseUrl, type Pool } from '@sfw/db';
import { claim, complete, deadJobs, enqueue, fail, retry } from './queue.js';
import { beat, heartbeats } from './heartbeat.js';

const hasDb = Boolean(testDatabaseUrl());
const describeDb = hasDb ? describe : describe.skip;

if (!hasDb) {
  console.warn('TEST_DATABASE_URL is not set, skipping the queue integration tests.');
}

describeDb('queue', () => {
  let pool: Pool;

  beforeAll(async () => {
    pool = await createTestDatabase('queue');
  }, 60_000);

  afterAll(async () => {
    await pool?.end();
  });

  async function clearJobs() {
    await pool.query('delete from jobs');
  }

  it('enqueues a job and claims it', async () => {
    await clearJobs();
    const id = await enqueue(pool, { type: 'dummy', payload: { n: 1 } });
    expect(id).toBeTruthy();

    const [job] = await claim(pool, ['dummy']);
    expect(job?.id).toBe(id);
    expect(job?.status).toBe('running');
    expect(job?.attempts).toBe(1);
    expect(job?.payload).toEqual({ n: 1 });
  });

  it('does not hand the same job to two workers', async () => {
    await clearJobs();
    await enqueue(pool, { type: 'dummy' });

    const [first, second] = await Promise.all([claim(pool, ['dummy']), claim(pool, ['dummy'])]);
    expect(first.length + second.length).toBe(1);
  });

  it('a dedupe key blocks a duplicate while the job is live', async () => {
    await clearJobs();
    const a = await enqueue(pool, { type: 'embed', dedupeKey: 'embed:1' });
    const b = await enqueue(pool, { type: 'embed', dedupeKey: 'embed:1' });

    expect(b).toBe(a);
    const { rows } = await pool.query('select count(*)::int as n from jobs');
    expect(rows[0].n).toBe(1);
  });

  it('frees the dedupe key once the job is done', async () => {
    await clearJobs();
    const a = await enqueue(pool, { type: 'embed', dedupeKey: 'embed:2' });
    await claim(pool, ['embed']);
    await complete(pool, a!);

    const b = await enqueue(pool, { type: 'embed', dedupeKey: 'embed:2' });
    expect(b).not.toBe(a);
  });

  it('backs off exponentially and then dies', async () => {
    await clearJobs();
    const id = (await enqueue(pool, { type: 'dummy' }))!;

    await claim(pool, ['dummy']);
    const first = await fail(pool, id, new Error('boom 1'));
    expect(first?.status).toBe('queued');
    expect(first?.attempts).toBe(1);
    expect(minutesOut(first!.run_after)).toBeCloseTo(2, 0);

    await pool.query('update jobs set run_after = now()');
    await claim(pool, ['dummy']);
    const second = await fail(pool, id, new Error('boom 2'));
    expect(second?.status).toBe('queued');
    expect(minutesOut(second!.run_after)).toBeCloseTo(4, 0);

    await pool.query('update jobs set run_after = now()');
    await claim(pool, ['dummy']);
    const third = await fail(pool, id, new Error('boom 3'));
    expect(third?.status).toBe('dead');
    expect(third?.attempts).toBe(3);
    expect(third?.error).toContain('boom 3');

    const dead = await deadJobs(pool);
    expect(dead.map((j) => j.id)).toContain(id);
  });

  it('a job waiting on its backoff is not claimable', async () => {
    await clearJobs();
    const id = (await enqueue(pool, { type: 'dummy' }))!;
    await claim(pool, ['dummy']);
    await fail(pool, id, new Error('boom'));

    expect(await claim(pool, ['dummy'])).toHaveLength(0);
  });

  it('retries a dead job, which then completes', async () => {
    await clearJobs();
    const id = (await enqueue(pool, { type: 'dummy' }))!;
    await pool.query(`update jobs set status = 'dead', attempts = 3 where id = $1`, [id]);

    const retried = await retry(pool, id);
    expect(retried?.status).toBe('queued');
    expect(retried?.attempts).toBe(0);

    const [job] = await claim(pool, ['dummy']);
    const done = await complete(pool, job!.id);
    expect(done?.status).toBe('done');
    expect(done?.error).toBeNull();
  });

  it('will not retry a dead job while a live one holds its dedupe key', async () => {
    await clearJobs();
    const dead = (await enqueue(pool, { type: 'dummy', dedupeKey: 'k' }))!;
    await pool.query(`update jobs set status = 'dead' where id = $1`, [dead]);
    await enqueue(pool, { type: 'dummy', dedupeKey: 'k' });

    expect(await retry(pool, dead)).toBeNull();
  });

  it('claims in priority order, then oldest first', async () => {
    await clearJobs();
    await enqueue(pool, { type: 'ord', payload: { p: 9 }, priority: 9 });
    await enqueue(pool, { type: 'ord', payload: { p: 1 }, priority: 1 });

    const [job] = await claim(pool, ['ord']);
    expect(job?.payload).toEqual({ p: 1 });
  });

  it('claims several at once, up to the limit', async () => {
    await clearJobs();
    for (let i = 0; i < 5; i += 1) await enqueue(pool, { type: 'batch', payload: { i } });

    expect(await claim(pool, ['batch'], 3)).toHaveLength(3);
    expect(await claim(pool, ['batch'], 3)).toHaveLength(2);
  });

  it('claims only the types it was asked for', async () => {
    await clearJobs();
    await enqueue(pool, { type: 'media_only' });
    expect(await claim(pool, ['light_only'])).toHaveLength(0);
    expect(await claim(pool, ['media_only'])).toHaveLength(1);
  });

  it('writes a heartbeat and marks an old one stale', async () => {
    await beat(pool, 'worker-light', ['ingest', 'embed']);
    const live = await heartbeats(pool);
    expect(live.find((h) => h.worker === 'worker-light')?.stale).toBe(false);

    await pool.query(`update worker_heartbeats set beat_at = now() - interval '10 minutes'`);
    const stale = await heartbeats(pool);
    expect(stale.find((h) => h.worker === 'worker-light')?.stale).toBe(true);
  });
});

function minutesOut(at: Date): number {
  return (at.getTime() - Date.now()) / 60_000;
}
