import { callClaude, cheapModel, embedOne, scoutRankSchema, toVector } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { db } from '../db.js';

/** At or above this, it becomes a story candidate. */
const WORTH_A_SLOT = 0.7;

/** Haiku, and one call per item, so a hundred items is still pennies. */
const BATCH = 40;

/**
 * Rates what the scout found.
 *
 * Every item gets a summary, a relevance score and topics, then is linked to
 * the facts and assets nearest to it by meaning. Anything at 0.7 or above
 * becomes a story candidate, which is what puts it in front of the planner on
 * Monday.
 *
 * Idempotent: only items still marked `new` are ranked.
 */
export const scoutRank = handler(async ({ enqueue }) => {
  const pool = db();

  const { rows: items } = await pool.query<{
    id: number;
    url: string;
    title: string | null;
    summary: string | null;
    feed: string | null;
  }>(
    `select n.id, n.url, n.title, n.summary, f.name as feed
     from news_items n left join feeds f on f.id = n.feed_id
     where n.status = 'new' and n.relevance is null
     order by n.published_at desc nulls last
     limit $1`,
    [BATCH],
  );

  let promoted = 0;

  for (const item of items) {
    const result = await callClaude({
      pool,
      jobId: null,
      prompt: 'scout_rank',
      schema: scoutRankSchema,
      model: cheapModel(),
      maxTokens: 1000,
      input: [
        `Source: ${item.feed ?? 'unknown'}`,
        `Title: ${item.title ?? ''}`,
        `URL: ${item.url}`,
        '',
        item.summary ?? '',
      ].join('\n'),
    });

    const vector = toVector(await embedOne(`${item.title ?? ''}. ${result.summary}`));

    // What we already know that is closest to this.
    const facts = await pool.query<{ id: number }>(
      `select id from facts
       where status = 'active' and embedding is not null
       order by embedding <=> $1::vector limit 5`,
      [vector],
    );

    const assets = await pool.query<{ id: string }>(
      `select id from assets
       where embedding is not null and status in ('cleared', 'tagged')
       order by embedding <=> $1::vector limit 5`,
      [vector],
    );

    await pool.query(
      `update news_items
       set summary = $2, relevance = $3, embedding = $4::vector,
           linked_facts = $5::int[], linked_assets = $6::uuid[]
       where id = $1`,
      [
        item.id,
        result.summary,
        result.relevance,
        vector,
        facts.rows.map((f) => f.id),
        assets.rows.map((a) => a.id),
      ],
    );

    if (result.relevance < WORTH_A_SLOT) continue;

    const story = await pool.query<{ id: number }>(
      `insert into stories
         (origin, origin_ref, angle, material_asset_ids, material_fact_ids, score, status)
       values ('news', $1, $2, $3::uuid[], $4::int[], $5, 'candidate')
       returning id`,
      [
        String(item.id),
        result.summary,
        assets.rows.map((a) => a.id),
        facts.rows.map((f) => f.id),
        result.relevance,
      ],
    );

    await pool.query(`update news_items set status = 'drafted' where id = $1`, [item.id]);
    promoted += 1;
    void story;
  }

  console.log(`[scout_rank] ranked ${items.length}, ${promoted} became story candidates`);

  // More waiting? Come back for them rather than doing a hundred in one job.
  const { rows: left } = await pool.query<{ n: number }>(
    `select count(*)::int as n from news_items where status = 'new' and relevance is null`,
  );

  if (left[0]!.n > 0) {
    await enqueue({
      type: 'scout_rank',
      payload: {},
      priority: 8,
      dedupeKey: `scout_rank:more:${Date.now()}`,
      runAfter: new Date(Date.now() + 60_000),
    });
  }
});
