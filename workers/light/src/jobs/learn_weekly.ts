import { callClaude, learnSchema, passRate, runEval } from '@sfw/ai';
import { handler } from '@sfw/queue';
import type { Pool } from '@sfw/db';
import { db } from '../db.js';

/** A pattern seen fewer times than this is a preference on a day, not a rule. */
const MIN_EVIDENCE = 3;

/** The spec's cap: no weight may move more than this in a week. */
const MAX_WEIGHT_CHANGE = 0.2;

/** The autonomy ladder's bar. */
const LIGHT_REVIEW_RATE = 0.9;

/**
 * Turns a month of corrections into rules, weights and examples.
 *
 * Six things, in order, because each depends on the one before: read the edits
 * and rejections, propose rules from them, test each candidate before
 * activating it, reweight the planner from what actually performed, promote the
 * best posts to examples, and write down what changed in a sentence a person
 * can read.
 *
 * Nothing here activates without passing the test set. A rule that makes the
 * critic flag the Pratik post is a bad rule however sensible it sounds.
 */
export const learnWeekly = handler(async ({ job }) => {
  const pool = db();

  const edits = await recentEdits(pool);
  const rules = await proposeRules(pool, edits, job.id);
  const activated = await testAndActivate(pool, rules, job.id);
  const weights = await reweight(pool);
  const promoted = await promoteExamples(pool);
  const autonomous = await autonomyLadder(pool);

  const note = [
    edits.length === 0
      ? 'No edits or rejections in the last four weeks, so nothing to learn from yet.'
      : `Read ${edits.length} edit${edits.length === 1 ? '' : 's'} and rejection${edits.length === 1 ? '' : 's'} from the last four weeks.`,
    activated.length > 0
      ? `Learned ${activated.length} new rule${activated.length === 1 ? '' : 's'}: ${activated.map((r) => `"${r}"`).join('; ')}.`
      : rules.length > 0
        ? `Proposed ${rules.length} rule${rules.length === 1 ? '' : 's'} but none passed the test set, so nothing changed.`
        : '',
    weights.length > 0 ? `Adjusted ${weights.join(', ')}.` : 'Left the planner weights alone.',
    promoted > 0 ? `Promoted ${promoted} post${promoted === 1 ? '' : 's'} to examples.` : '',
    autonomous.length > 0
      ? `These are now approved almost every time and could go to lighter review: ${autonomous.join(', ')}.`
      : '',
  ]
    .filter(Boolean)
    .join(' ');

  await pool.query(
    `insert into settings (key, value) values ('learned_latest', $1::jsonb)
     on conflict (key) do update set value = excluded.value, updated_at = now()`,
    [
      JSON.stringify({
        at: new Date().toISOString(),
        note,
        activated,
        weights,
        promoted,
        autonomous,
      }),
    ],
  );

  console.log(`[learn_weekly] ${note}`);
});

type Edit = {
  post_id: string;
  format: string;
  platform: string;
  pillar: string | null;
  diff: Record<string, unknown>;
};

async function recentEdits(pool: Pool): Promise<Edit[]> {
  const { rows } = await pool.query<Edit>(
    `select v.post_id, p.format, p.platform, s.pillar, v.diff
     from post_versions v
     join posts p on p.id = v.post_id
     left join stories s on s.id = p.story_id
     where v.author = 'human' and v.diff is not null
       and v.created_at > now() - interval '28 days'
     order by v.created_at desc
     limit 100`,
  );
  return rows;
}

async function proposeRules(
  pool: Pool,
  edits: Edit[],
  jobId: string,
): Promise<{ text: string; scope: string; evidence: string[] }[]> {
  if (edits.length < MIN_EVIDENCE) return [];

  const active = (
    await pool.query<{ id: number; scope: string; text: string }>(
      'select id, scope, text from rules where active order by id',
    )
  ).rows;

  const result = await callClaude({
    pool,
    jobId,
    prompt: 'learn',
    schema: learnSchema,
    maxTokens: 6000,
    input: JSON.stringify({ edits, active_rules: active }, null, 2),
  });

  // The spec's bar: three separate posts arguing for it.
  return result.rules.filter((r) => new Set(r.evidence).size >= MIN_EVIDENCE);
}

/**
 * A candidate rule is handed to the critic on top of the active ones and the
 * whole test set is run. It only goes live if nothing that used to pass now
 * fails.
 */
async function testAndActivate(
  pool: Pool,
  candidates: { text: string; scope: string; evidence: string[] }[],
  jobId: string,
): Promise<string[]> {
  if (candidates.length === 0) return [];

  const baseline = passRate(await runEval(pool, { jobId }));
  const activated: string[] = [];

  for (const candidate of candidates) {
    const withRule = await runEval(pool, { jobId, extraRules: [candidate.text] });

    const inserted = await pool.query<{ id: number }>(
      `insert into rules (scope, text, origin, evidence, active)
       values ($1, $2, 'edit', $3::jsonb, false)
       returning id`,
      [candidate.scope, candidate.text, JSON.stringify(candidate.evidence)],
    );
    const ruleId = inserted.rows[0]!.id;

    if (passRate(withRule) >= baseline) {
      await pool.query('update rules set active = true where id = $1', [ruleId]);
      activated.push(candidate.text);
    } else {
      console.log(
        `[learn_weekly] discarded "${candidate.text}": it made the test set worse ` +
          `(${Math.round(passRate(withRule) * 100)}% against ${Math.round(baseline * 100)}%)`,
      );
    }
  }

  return activated;
}

/**
 * Reweights the planner from saves and shares per impression, capped at plus or
 * minus twenty per cent a week so one unusual week cannot swing the plan.
 */
async function reweight(pool: Pool): Promise<string[]> {
  const { rows } = await pool.query<{ key: string; kind: string; rate: number; posts: number }>(
    `with performance as (
       select p.format as format, s.pillar as pillar,
              sum(coalesce(m.saves, 0) + coalesce(m.shares, 0))::float as engaged,
              nullif(sum(coalesce(m.reach, 0)), 0)::float as reach,
              count(distinct p.id)::int as posts
       from posts p
       join metrics m on m.post_id = p.id
       left join stories s on s.id = p.story_id
       where p.published_at > now() - interval '84 days'
       group by grouping sets ((p.format), (s.pillar))
     )
     select coalesce(format, pillar) as key,
            case when format is not null then 'format' else 'pillar' end as kind,
            coalesce(engaged / reach, 0) as rate,
            posts
     from performance
     where coalesce(format, pillar) is not null`,
  );

  if (rows.length === 0) return [];

  // Everything is measured against the average, so a weight is "better or
  // worse than the rest", not an absolute.
  const byKind = new Map<string, number[]>();
  for (const row of rows) {
    byKind.set(row.kind, [...(byKind.get(row.kind) ?? []), row.rate]);
  }

  const changed: string[] = [];

  for (const row of rows) {
    const peers = byKind.get(row.kind)!;
    const average = peers.reduce((a, b) => a + b, 0) / peers.length;
    if (average === 0) continue;

    // Under three data points it is noise, per the spec's exploration rule.
    if (row.posts < 3) continue;

    const target = row.rate / average;

    const current = (
      await pool.query<{ weight: number }>('select weight from planner_weights where key = $1', [
        row.key,
      ])
    ).rows[0]?.weight;

    if (current === undefined) continue;

    const capped = Math.min(
      current * (1 + MAX_WEIGHT_CHANGE),
      Math.max(current * (1 - MAX_WEIGHT_CHANGE), target),
    );

    // A moving average, so a weight drifts rather than jumps.
    const next = Number(((current + capped) / 2).toFixed(3));
    if (Math.abs(next - current) < 0.01) continue;

    await pool.query(
      `update planner_weights set weight = $2, data_points = $3, updated_at = now() where key = $1`,
      [row.key, next, row.posts],
    );
    changed.push(`${row.key} ${current.toFixed(2)} to ${next.toFixed(2)}`);
  }

  // Anything with no data keeps the weight it was seeded with, which is what
  // makes the exploration slots worth having: an untried format is not
  // penalised for being untried.
  return changed;
}

/** Barely edited and in the top quarter for saves becomes an example. */
async function promoteExamples(pool: Pool): Promise<number> {
  const { rowCount } = await pool.query(
    `with scored as (
       select p.id,
              coalesce((v.diff->'caption'->>'ratio')::float, 0) as edit_ratio,
              percent_rank() over (partition by p.format order by max(m.saves)) as saves_rank
       from posts p
       left join metrics m on m.post_id = p.id
       left join post_versions v on v.post_id = p.id and v.author = 'human'
       where p.status in ('approved', 'exported', 'published')
       group by p.id, v.diff
     )
     update posts set is_example = true
     where id in (select id from scored where edit_ratio <= 0.1 and saves_rank >= 0.75)
       and not is_example`,
  );
  return rowCount ?? 0;
}

/** Post types approved without edits nine times out of ten, over four weeks. */
async function autonomyLadder(pool: Pool): Promise<string[]> {
  const { rows } = await pool.query<{ kind: string; rate: number; posts: number }>(
    `select p.platform || ' ' || p.format as kind,
            avg(case when coalesce((v.diff->'caption'->>'ratio')::float, 0) <= 0.1 then 1 else 0 end) as rate,
            count(*)::int as posts
     from posts p
     left join post_versions v on v.post_id = p.id and v.author = 'human'
     where p.status in ('approved', 'exported', 'published')
       and p.created_at > now() - interval '28 days'
     group by p.platform, p.format
     having count(*) >= 4`,
  );

  const ready = rows.filter((r) => r.rate >= LIGHT_REVIEW_RATE).map((r) => r.kind);

  if (ready.length > 0) {
    await pool.query(
      `insert into settings (key, value) values ('light_review', $1::jsonb)
       on conflict (key) do update set value = excluded.value, updated_at = now()`,
      [JSON.stringify(ready)],
    );
  }

  return ready;
}
