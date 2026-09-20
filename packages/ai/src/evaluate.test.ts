import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { createTestDatabase, seed, testDatabaseUrl, type Pool } from '@sfw/db';
import { passRate, runEval } from './evaluate.js';

const hasDb = Boolean(testDatabaseUrl());
const describeDb = hasDb ? describe : describe.skip;

if (!hasDb) {
  console.warn('TEST_DATABASE_URL is not set, skipping the eval tests.');
}

/**
 * The evaluator against the real seeded test set, with the model switched off.
 * That half needs no API key and is exactly the half that decides whether a
 * mechanically-bad caption gets through.
 */
describeDb('the eval', () => {
  let pool: Pool;

  beforeAll(async () => {
    pool = await createTestDatabase('eval');
    await seed(pool);
  }, 60_000);

  afterAll(async () => {
    await pool?.end();
  });

  it('passes every good case on the string checks alone', async () => {
    const result = await runEval(pool, { useModel: false });
    const good = result.cases.filter((c) => c.kind === 'good');

    expect(good.length).toBeGreaterThanOrEqual(2);
    for (const testCase of good) {
      expect(testCase.passed, `${testCase.name}: ${testCase.why}`).toBe(true);
    }
  });

  it('catches every mechanically-bad case without calling the model', async () => {
    const result = await runEval(pool, { useModel: false });

    const mechanical = [
      'negation_framing',
      'em_dash',
      'internal_acronym',
      'unsourced_figure',
      'banned_phrase',
    ];
    const shouldCatch = result.cases.filter(
      (c) => c.kind === 'bad' && c.caught.some((check) => mechanical.includes(check)),
    );

    expect(shouldCatch.length).toBeGreaterThanOrEqual(5);
    for (const testCase of shouldCatch) {
      expect(testCase.passed, `${testCase.name}: ${testCase.why}`).toBe(true);
    }
  });

  it('honestly fails the judgement cases when the model is off', async () => {
    const result = await runEval(pool, { useModel: false });
    const failed = result.cases.filter((c) => !c.passed);

    // Expertise bar, platform fit and image-text match cannot be settled by a
    // regular expression, and the eval must say so rather than pass them.
    expect(failed.length).toBeGreaterThanOrEqual(3);
    for (const testCase of failed) {
      expect(testCase.kind).toBe('bad');
      expect(testCase.why).toContain('missed');
    }
  });

  it('records which prompt version it ran against', async () => {
    const result = await runEval(pool, { useModel: false });
    expect(result.promptVersion).toBe(1);
    expect(result.promptName).toBe('critique');
  });

  it('computes a pass rate that matches the counts', async () => {
    const result = await runEval(pool, { useModel: false });
    expect(passRate(result)).toBeCloseTo(result.passed / (result.passed + result.failed));
  });

  it('gives zero rather than dividing by zero for an empty run', () => {
    expect(passRate({ passed: 0, failed: 0 })).toBe(0);
  });
});
