import { callClaude, planSchema } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { CADENCE, DEFAULT_QUESTION_RECIPIENT, PILLARS, type Cadence } from '@sfw/shared';
import { db } from '../db.js';
import { pillarBalance, scoreCandidate, slotsForWeek } from '../slots.js';

/**
 * Plans the coming week.
 *
 * The slots come from the cadence in code, not from the model: how many posts
 * a week is a decision, not a judgement. What goes in each slot is the
 * judgement, and that is what Claude is asked for, with every candidate
 * pre-scored so it is arguing against arithmetic rather than inventing it.
 *
 * The hard rule from PRD principle 1 is enforced twice over: a proposed post
 * with no material is not created, and the slot becomes a shot-list question
 * to a named person instead. The database check constraint catches anything
 * that gets past this.
 */
export const planWeek = handler<{ from?: string }>(async ({ job, enqueue }) => {
  const pool = db();

  const cadence =
    (await pool.query<{ value: Cadence }>(`select value from settings where key = 'cadence'`))
      .rows[0]?.value ?? CADENCE;

  const from = job.payload.from ? new Date(job.payload.from) : nextMonday();
  const slots = slotsForWeek(from, cadence);

  // Slots already filled by a previous run or by hand.
  const taken = new Set(
    (
      await pool.query<{ key: string }>(
        `select slot_date::text || coalesce(slot_time::text, '') as key
         from posts
         where slot_date between $1::date and $1::date + 6
           and status not in ('rejected', 'dropped')`,
        [from.toISOString().slice(0, 10)],
      )
    ).rows.map((r) => r.key),
  );

  const open = slots.filter((s) => !taken.has(s.date + s.time + ':00'));
  if (open.length === 0) {
    console.log('[plan_week] every slot is already filled');
    return;
  }

  const weights = Object.fromEntries(
    (
      await pool.query<{ key: string; weight: number }>(
        `select key, weight from planner_weights where kind = 'format'`,
      )
    ).rows.map((r) => [r.key, r.weight]),
  );

  // How the pillars have actually run over the last four weeks.
  const recent = Object.fromEntries(
    (
      await pool.query<{ pillar: string; count: number }>(
        `select s.pillar, count(*)::int as count
         from posts p join stories s on s.id = p.story_id
         where p.created_at > now() - interval '28 days' and s.pillar is not null
         group by s.pillar`,
      )
    ).rows.map((r) => [r.pillar, r.count]),
  );
  const balance = pillarBalance(recent, [...PILLARS]);

  const candidates = (
    await pool.query<{
      id: number;
      angle: string | null;
      pillar: string | null;
      origin: string;
      score: number | null;
      age_days: number;
      asset_count: number;
      fact_count: number;
      assets: { id: string; description: string | null; type: string }[];
    }>(
      `select s.id, s.angle, s.pillar, s.origin, s.score,
              extract(epoch from now() - s.created_at) / 86400 as age_days,
              cardinality(s.material_asset_ids) as asset_count,
              cardinality(s.material_fact_ids) as fact_count,
              coalesce((
                select json_agg(json_build_object('id', a.id, 'description', a.description, 'type', a.type))
                from assets a
                where a.id = any(s.material_asset_ids) and a.status in ('cleared', 'tagged')
              ), '[]'::json) as assets
       from stories s
       where s.status = 'candidate'
       order by s.created_at desc
       limit 60`,
    )
  ).rows;

  // Cleared material nobody has used, which is a story waiting to be written.
  const unused = (
    await pool.query<{
      id: string;
      description: string | null;
      type: string;
      workshop: string | null;
    }>(
      `select a.id, a.description, a.type, b.workshop
       from assets a left join batches b on b.id = a.batch_id
       where a.status = 'cleared'
         and not exists (select 1 from asset_usage u where u.asset_id = a.id)
       order by a.hero_candidate desc, a.quality desc nulls last, a.created_at desc
       limit 40`,
    )
  ).rows;

  const scored = candidates.map((c) => ({
    id: c.id,
    angle: c.angle,
    pillar: c.pillar,
    origin: c.origin,
    assets: c.assets,
    has_material: c.asset_count > 0 || c.fact_count > 0,
    score: scoreCandidate({
      relevance: c.score ?? 0.6,
      ageDays: Number(c.age_days),
      // Two assets and a few facts is a well-supplied story.
      materialStrength: Math.min(1, c.assets.length * 0.4 + c.fact_count * 0.1 || 0.1),
      formatWeight: 1,
      pillarBalance: c.pillar ? (balance[c.pillar] ?? 1) : 1,
    }),
  }));

  const result = await callClaude({
    pool,
    jobId: job.id,
    prompt: 'plan',
    schema: planSchema,
    maxTokens: 8000,
    input: JSON.stringify(
      {
        week_starting: from.toISOString().slice(0, 10),
        slots: open,
        cadence,
        format_weights: weights,
        pillar_balance: balance,
        story_candidates: scored.sort((a, b) => b.score - a.score).slice(0, 30),
        unused_cleared_material: unused,
      },
      null,
      2,
    ),
  });

  let created = 0;
  let asked = 0;

  for (const proposed of result.posts) {
    // Only assets that exist and are cleared. A post cannot be built on an id
    // the model produced from nothing.
    const assetIds = proposed.asset_ids.length
      ? (
          await pool.query<{ id: string }>(
            `select id from assets where id = any($1::uuid[]) and status in ('cleared', 'tagged')`,
            [proposed.asset_ids],
          )
        ).rows.map((r) => r.id)
      : [];

    if (assetIds.length === 0) {
      await shotList(proposed.slot_date, proposed.platform, proposed.angle, proposed.why);
      asked += 1;
      continue;
    }

    const post = await pool.query<{ id: string }>(
      `insert into posts
         (story_id, slot_date, slot_time, platform, format, asset_ids, status, experiment)
       values ($1, $2::date, $3::time, $4, $5, $6::uuid[], 'proposed', $7)
       returning id`,
      [
        proposed.story_id,
        proposed.slot_date,
        proposed.slot_time,
        proposed.platform,
        proposed.format,
        assetIds,
        proposed.experiment,
      ],
    );

    if (proposed.story_id) {
      await pool.query(
        `update stories set status = 'planned', angle = coalesce(angle, $2) where id = $1`,
        [proposed.story_id, proposed.angle],
      );
    }

    created += 1;
    void post;
  }

  for (const gap of result.unfilled) {
    await shotList(gap.slot_date, gap.platform, gap.missing, gap.ask);
    asked += 1;
  }

  console.log(`[plan_week] ${created} post(s) proposed, ${asked} slot(s) short of material`);

  if (created > 0) {
    await enqueue({
      type: 'write_batch',
      payload: {},
      priority: 3,
      dedupeKey: `write_batch:${from.toISOString().slice(0, 10)}`,
    });
  }

  async function shotList(
    date: string,
    platform: string,
    missing: string,
    ask: string,
  ): Promise<void> {
    const text = `${date} ${platform}: ${ask || missing || 'needs material'}`;
    await pool.query(
      `insert into questions (text, asked_to, context, status)
       values ($1, (select id from people where name = $2), $3::jsonb, 'open')
       on conflict do nothing`,
      [
        text.slice(0, 500),
        DEFAULT_QUESTION_RECIPIENT,
        JSON.stringify({ topic: 'material', slot_date: date, platform }),
      ],
    );
  }
});

/** The planner runs on Monday for the week that starts that day. */
function nextMonday(): Date {
  const now = new Date();
  const date = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  // Monday is 1. If today is Monday, plan today.
  const offset = (1 - date.getUTCDay() + 7) % 7;
  date.setUTCDate(date.getUTCDate() + offset);
  return date;
}
