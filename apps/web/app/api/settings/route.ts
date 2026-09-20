import { NextResponse, type NextRequest } from 'next/server';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

export const dynamic = 'force-dynamic';

/**
 * Everything the Settings screen shows: the cadence, the feeds, who answers
 * what, which prompt versions are live, and what the last month cost.
 *
 * Prompts are read-only here on purpose. Editing one in a text box would let a
 * change reach production without passing the test set, which is the one rule
 * the self-improvement loop rests on.
 */
export const GET = route(async () => {
  const pool = db();

  const [settings, feeds, people, prompts, cost, byPrompt] = await Promise.all([
    pool.query(`select key, value, updated_at from settings order by key`),
    pool.query(
      `select f.id, f.name, f.url, f.kind, f.active, f.region,
              f.last_ok_at, f.last_error, f.last_checked_at, f.consecutive_failures,
              (select count(*)::int from news_items n where n.feed_id = f.id) as items,
              (select max(n.created_at) from news_items n where n.feed_id = f.id) as last_item
       from feeds f
       order by f.consecutive_failures desc, f.region, f.name`,
    ),
    pool.query(
      `select id, name, role, org, email, topics,
              (select count(*)::int from questions q where q.asked_to = people.id and q.status = 'open') as open_questions
       from people order by cardinality(topics) desc, name`,
    ),
    pool.query(
      `select name, version, active, created_at, length(body) as size
       from prompts order by name, version desc`,
    ),
    pool.query<{ total: string; calls: number; days: number }>(
      `select coalesce(sum(cost_usd), 0)::text as total,
              count(*)::int as calls,
              30 as days
       from ai_calls where created_at > now() - interval '30 days'`,
    ),
    pool.query(
      `select prompt_name, model, count(*)::int as calls,
              coalesce(sum(cost_usd), 0)::float as cost,
              round(avg(latency_ms))::int as avg_ms
       from ai_calls where created_at > now() - interval '30 days'
       group by prompt_name, model order by cost desc`,
    ),
  ]);

  return NextResponse.json({
    settings: Object.fromEntries(settings.rows.map((r) => [r.key, r.value])),
    feeds: feeds.rows,
    people: people.rows,
    prompts: prompts.rows,
    cost: { ...cost.rows[0], byPrompt: byPrompt.rows },
  });
});

/** The handful of things that are safe to change from a browser. */
export const PATCH = route(async (request: NextRequest) => {
  const body = (await request.json()) as {
    feedId?: number;
    active?: boolean;
    personId?: number;
    email?: string;
    topics?: string[];
  };

  const pool = db();

  if (body.feedId !== undefined && body.active !== undefined) {
    await pool.query('update feeds set active = $2 where id = $1', [body.feedId, body.active]);
    return NextResponse.json({ ok: true });
  }

  if (body.personId !== undefined) {
    await pool.query(
      `update people
       set email = coalesce($2, email),
           topics = coalesce($3::text[], topics)
       where id = $1`,
      [body.personId, body.email ?? null, body.topics ?? null],
    );
    return NextResponse.json({ ok: true });
  }

  return fail('Nothing in that request is editable here');
});
