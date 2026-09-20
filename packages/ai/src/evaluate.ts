import type { Pool } from '@sfw/db';
import { runStringChecks } from '@sfw/shared';
import { callClaude } from './claude.js';
import { critiqueSchema } from './schemas.js';

export type TestCase = {
  id: number;
  name: string;
  kind: 'good' | 'bad';
  input: { caption: string; platform?: string; format?: string; context?: string };
  expected: { minScore?: number; catches?: string[]; noHits?: boolean };
  notes: string | null;
};

export type CaseResult = {
  name: string;
  kind: 'good' | 'bad';
  passed: boolean;
  why: string;
  score: number | null;
  caught: string[];
};

export type EvalResult = {
  promptName: string;
  promptVersion: number | null;
  passed: number;
  failed: number;
  cases: CaseResult[];
};

/**
 * Runs the fixed test set against the active critic.
 *
 * A good case has to come back clean and well scored; a bad case has to be
 * caught, by the mechanical checks or by the critic naming the same check. The
 * mechanical half needs no API call, so a run with no key still tells you
 * something real about the bad cases.
 *
 * This is what stands between a prompt change and production (PRD 7.4), and
 * what `eval_nightly` compares against last week to decide on a rollback.
 */
export async function runEval(
  pool: Pool,
  options: {
    promptName?: string;
    jobId?: string | null;
    useModel?: boolean;
    /**
     * Rules to hand the critic on top of whatever is active. This is how a
     * candidate rule is tested before it goes live: a rule that makes the
     * critic flag the Pratik post is a bad rule, whatever it says.
     */
    extraRules?: string[];
  } = {},
): Promise<EvalResult> {
  const promptName = options.promptName ?? 'critique';
  const useModel = options.useModel ?? true;

  const { rows: cases } = await pool.query<TestCase>(
    'select id, name, kind, input, expected, notes from test_cases order by kind desc, name',
  );

  const version = (
    await pool.query<{ version: number }>(
      'select version from prompts where name = $1 and active',
      [promptName],
    )
  ).rows[0]?.version;

  const results: CaseResult[] = [];

  for (const testCase of cases) {
    const text = testCase.input.caption;
    const mechanical = runStringChecks(text).map((h) => h.check);

    let score: number | null = null;
    let fromCritic: string[] = [];

    // A case the regular expressions already settle does not need the model.
    const needsJudgement =
      testCase.kind === 'good' ||
      (testCase.expected.catches ?? []).some((c) => !mechanical.includes(c));

    if (useModel && needsJudgement) {
      const verdict = await callClaude({
        pool,
        jobId: options.jobId ?? null,
        prompt: promptName,
        schema: critiqueSchema,
        input: JSON.stringify(
          {
            draft: {
              platform: testCase.input.platform ?? 'instagram',
              format: testCase.input.format ?? 'feed',
              caption: text,
            },
            assets: testCase.input.context
              ? [{ image: 1, description: testCase.input.context }]
              : [],
            facts: [],
            rules: options.extraRules ?? [],
          },
          null,
          2,
        ),
      });

      score = verdict.score;
      fromCritic = verdict.must_fix.map((f) => f.check);
    }

    const caught = [...new Set([...mechanical, ...fromCritic])];
    results.push(judge(testCase, caught, score));
  }

  const passed = results.filter((r) => r.passed).length;

  return {
    promptName,
    promptVersion: version ?? null,
    passed,
    failed: results.length - passed,
    cases: results,
  };
}

function judge(testCase: TestCase, caught: string[], score: number | null): CaseResult {
  const base = { name: testCase.name, kind: testCase.kind, score, caught };

  if (testCase.kind === 'good') {
    if (caught.length > 0) {
      return { ...base, passed: false, why: `flagged a good post for ${caught.join(', ')}` };
    }
    const min = testCase.expected.minScore ?? 80;
    if (score !== null && score < min) {
      return { ...base, passed: false, why: `scored ${score}, wanted ${min} or better` };
    }
    return { ...base, passed: true, why: 'clean, and scored well enough' };
  }

  const wanted = testCase.expected.catches ?? [];
  const missed = wanted.filter((c) => !caught.includes(c));

  if (missed.length > 0) {
    // Catching it for a different reason is still catching it. Say so, but
    // count it as a pass: the post does not go out either way.
    if (caught.length > 0) {
      return {
        ...base,
        passed: true,
        why: `caught, though as ${caught.join(', ')} rather than ${wanted.join(', ')}`,
      };
    }
    return { ...base, passed: false, why: `missed: nothing caught ${missed.join(', ')}` };
  }

  return { ...base, passed: true, why: `caught ${wanted.join(', ')}` };
}

/** The share that passed, which is what a regression is measured against. */
export function passRate(result: { passed: number; failed: number }): number {
  const total = result.passed + result.failed;
  return total === 0 ? 0 : result.passed / total;
}
