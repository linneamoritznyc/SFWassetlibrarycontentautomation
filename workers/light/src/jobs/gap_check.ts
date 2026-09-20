import { callClaude, embedOne, gapCheckSchema, toVector } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { DEFAULT_QUESTION_RECIPIENT } from '@sfw/shared';
import type { Pool } from '@sfw/db';
import { buildBrief, type Briefing } from '../brief.js';
import { db } from '../db.js';

/** A fact this confident answers the question without asking a person. */
const CONFIDENT_ENOUGH = 0.8;

/** After this long with no answer, the post goes to review flagged. */
const WAIT_HOURS = 72;

export type GapResult = {
  blocked: boolean;
  asked: number;
  attachedFactIds: number[];
  assumptions: { text: string; basis: string }[];
};

/**
 * Lists what the writer would be assuming, then tries to answer each unknown
 * from the knowledge base before bothering a person.
 *
 * An unknown that vector search answers confidently is attached to the story as
 * a fact. One it cannot becomes a one-line question routed by topic: programs
 * to Stephanie, mentors and graduates to Carla, India and partners to Kavi,
 * workshops to Loida.
 *
 * A post with a blocking unknown waits in `revising`. After 72 hours it goes to
 * review anyway, flagged, because a post that never ships helps nobody.
 */
export async function runGapCheck(
  pool: Pool,
  postId: string,
  briefing: Briefing,
  jobId: string | null,
): Promise<GapResult> {
  const result = await callClaude({
    pool,
    jobId,
    prompt: 'gap_check',
    schema: gapCheckSchema,
    input: JSON.stringify(
      {
        story: briefing.story,
        post: briefing.post,
        assets: briefing.assets.map((a) => ({
          id: a.id,
          description: a.description,
          credit: a.credit_line,
        })),
        facts: briefing.facts.map((f) => ({ id: f.id, text: f.text })),
        calendar: briefing.calendar_context,
      },
      null,
      2,
    ),
  });

  const attachedFactIds: number[] = [];
  let asked = 0;
  let blocked = false;

  for (const unknown of result.unknowns) {
    const found = await lookUp(pool, unknown.question);

    if (found) {
      attachedFactIds.push(found.id);
      continue;
    }

    const existing = await pool.query<{ id: number; status: string; created_at: Date }>(
      `select id, status, created_at from questions
       where text = $1 and context->>'post_id' = $2
       limit 1`,
      [unknown.question, postId],
    );

    const already = existing.rows[0];

    if (!already) {
      await pool.query(
        `insert into questions (text, asked_to, context, status)
         values ($1, (select id from people where $2 = any(topics) limit 1), $3::jsonb, 'open')`,
        [
          unknown.question,
          unknown.topic,
          JSON.stringify({ post_id: postId, story_id: briefing.story.id, topic: unknown.topic }),
        ],
      );
      asked += 1;
    }

    if (unknown.blocks_post) {
      const askedAt = already?.created_at ?? new Date();
      const hoursWaiting = (Date.now() - askedAt.getTime()) / 3_600_000;
      if (already?.status !== 'answered' && hoursWaiting < WAIT_HOURS) blocked = true;
    }
  }

  // Anyone with no topic match gets Stephanie, who owns social.
  await pool.query(
    `update questions
     set asked_to = (select id from people where name = $1)
     where asked_to is null and status = 'open'`,
    [DEFAULT_QUESTION_RECIPIENT],
  );

  if (attachedFactIds.length > 0) {
    await pool.query(
      `update stories
       set material_fact_ids = (
         select array(select distinct unnest(material_fact_ids || $2::int[]))
       )
       where id = $1`,
      [briefing.story.id, attachedFactIds],
    );
  }

  return { blocked, asked, attachedFactIds, assumptions: result.assumptions };
}

async function lookUp(pool: Pool, question: string): Promise<{ id: number; text: string } | null> {
  const vector = toVector(await embedOne(question));

  const { rows } = await pool.query<{
    id: number;
    text: string;
    confidence: number;
    distance: number;
  }>(
    `select id, text, confidence, embedding <=> $1::vector as distance
     from facts
     where status = 'active' and embedding is not null
     order by distance
     limit 1`,
    [vector],
  );

  const best = rows[0];
  if (!best) return null;

  // Close in meaning and confident in itself. Either alone is not enough: a
  // confident fact about something else is worse than no fact.
  const similarity = 1 - best.distance;
  if (similarity < 0.55 || best.confidence < CONFIDENT_ENOUGH) return null;

  return { id: best.id, text: best.text };
}

/** Callable on its own, so a post can be re-checked after an answer arrives. */
export const gapCheck = handler<{ post_id: string }>(async ({ job, enqueue }) => {
  const pool = db();
  const postId = job.payload.post_id;

  const { rows } = await pool.query<{ story_id: number | null }>(
    'select story_id from posts where id = $1',
    [postId],
  );
  const storyId = rows[0]?.story_id;
  if (!storyId) throw new Error(`Post ${postId} has no story to brief from`);

  const briefing = await buildBrief(pool, storyId, { postId });
  const result = await runGapCheck(pool, postId, briefing, job.id);

  await pool.query(
    `update posts set status = $2 where id = $1 and status in ('proposed', 'revising')`,
    [postId, result.blocked ? 'revising' : 'proposed'],
  );

  if (!result.blocked) {
    await enqueue({ type: 'write', payload: { post_id: postId }, dedupeKey: `write:${postId}` });
  }
});
