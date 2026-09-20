import { callClaude, embed as embedTexts, extractFactsSchema, toVector } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { db } from '../db.js';

/**
 * Turns an answer into permanent facts.
 *
 * Someone replied to a question, by email or in the app. The answer is parsed
 * into atomic facts with `source.kind = 'human'` and the person's name against
 * them, so a caption built on it can say where it came from. Then the post that
 * was waiting goes back to the writer.
 *
 * A human answer is trusted more than a web page, but not blindly: the extractor
 * still has to turn it into self-contained sentences, and anything it cannot is
 * left out rather than guessed at.
 */
export const saveFact = handler<{ question_id: number }>(async ({ job, enqueue }) => {
  const pool = db();
  const questionId = job.payload.question_id;

  const { rows } = await pool.query<{
    id: number;
    text: string;
    answer: string | null;
    context: { post_id?: string; story_id?: number; topic?: string };
    person: string | null;
  }>(
    `select q.id, q.text, q.answer, q.context, p.name as person
     from questions q left join people p on p.id = q.asked_to
     where q.id = $1`,
    [questionId],
  );

  const question = rows[0];
  if (!question) throw new Error(`No question ${questionId}`);
  if (!question.answer?.trim()) throw new Error(`Question ${questionId} has no answer yet`);

  const source = await pool.query<{ id: number }>(
    `insert into sources (kind, ref, title, fetched_at)
     values ('human', $1, $2, now())
     on conflict (kind, ref) do update set fetched_at = now()
     returning id`,
    [
      `question:${questionId}`,
      `${question.person ?? 'Someone'} answered: ${question.text}`.slice(0, 200),
    ],
  );
  const sourceId = source.rows[0]!.id;

  const result = await callClaude({
    pool,
    jobId: job.id,
    prompt: 'extract_facts',
    schema: extractFactsSchema,
    input: [
      `${question.person ?? 'Someone at the Foundation'} was asked:`,
      `  ${question.text}`,
      '',
      'They answered:',
      `  ${question.answer}`,
      '',
      'Turn the answer into facts. The page reference is "answered by ' +
        `${question.person ?? 'a colleague'}".`,
    ].join('\n'),
  });

  const keep = result.facts.filter((f) => f.confidence >= 0.5);

  if (keep.length > 0) {
    const vectors = await embedTexts(keep.map((f) => f.text));

    for (const [i, fact] of keep.entries()) {
      await pool.query(
        `insert into facts
           (subject, predicate, object, text, source_id, confidence, status, confirmed_by, embedding)
         values ($1, $2, $3, $4, $5, $6, 'active', $7, $8::vector)`,
        [
          fact.subject,
          fact.predicate,
          fact.object,
          fact.text,
          sourceId,
          // A named person saying so is worth more than a page saying so.
          Math.max(fact.confidence, 0.85),
          question.person,
          toVector(vectors[i]!),
        ],
      );
    }
  }

  await pool.query(
    `update questions set status = 'answered', answered_at = coalesce(answered_at, now())
     where id = $1`,
    [questionId],
  );

  // The post that was waiting can go on now.
  const postId = question.context?.post_id;
  if (postId) {
    await pool.query(`update posts set status = 'proposed' where id = $1 and status = 'revising'`, [
      postId,
    ]);
    await enqueue({
      type: 'write',
      payload: { post_id: postId },
      priority: 3,
      dedupeKey: `write:${postId}:after-${questionId}`,
    });
  }

  console.log(`[save_fact] ${keep.length} fact(s) from question ${questionId}`);
});
