import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { route } from '@/lib/http';

export const dynamic = 'force-dynamic';

/**
 * What the system has learned: the rules with their evidence, the planner
 * weights, the eval history, and the note from the last weekly run.
 *
 * The point of the screen is that none of this is a black box. Every rule says
 * which posts argued for it, and every weight says how many data points are
 * behind it.
 */
export const GET = route(async () => {
  const pool = db();

  const [rules, weights, evals, latest, lightReview] = await Promise.all([
    pool.query(
      `select id, scope, text, origin, evidence, active, applied_count, created_at
       from rules order by active desc, created_at desc limit 100`,
    ),
    pool.query(
      `select key, kind, weight, data_points, updated_at
       from planner_weights order by kind, weight desc`,
    ),
    pool.query(
      `select prompt_name, prompt_version, passed, failed, details, created_at
       from eval_runs order by created_at desc limit 20`,
    ),
    pool.query(`select value from settings where key = 'learned_latest'`),
    pool.query(`select value from settings where key = 'light_review'`),
  ]);

  return NextResponse.json({
    rules: rules.rows,
    weights: weights.rows,
    evals: evals.rows,
    latest: latest.rows[0]?.value ?? null,
    lightReview: lightReview.rows[0]?.value ?? [],
  });
});
