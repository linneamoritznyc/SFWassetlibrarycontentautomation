import { handler } from '@sfw/queue';
import { db } from '../db.js';
import { appUrl, sendEmail } from '../notify.js';

/**
 * The Monday email.
 *
 * One link, the count, the open questions and what the week cost. The point of
 * the whole system is a fifteen-minute review, and this is what starts it, so
 * it says what is waiting and nothing else.
 */
export const reviewReadyNotify = handler(async () => {
  const pool = db();

  const counts = (
    await pool.query<{ in_review: number; revising: number; approved: number }>(
      `select count(*) filter (where status = 'in_review')::int as in_review,
              count(*) filter (where status = 'revising')::int as revising,
              count(*) filter (where status = 'approved')::int as approved
       from posts
       where slot_date between current_date and current_date + 7`,
    )
  ).rows[0]!;

  const questions = (
    await pool.query<{ text: string; person: string | null }>(
      `select q.text, p.name as person
       from questions q left join people p on p.id = q.asked_to
       where q.status = 'open' order by q.created_at limit 10`,
    )
  ).rows;

  const cost = (
    await pool.query<{ ai: string; calls: number; clips: number }>(
      `select coalesce(sum(cost_usd), 0)::text as ai,
              count(*)::int as calls,
              (select count(*)::int from assets
                where type = 'clip' and created_at > now() - interval '7 days') as clips
       from ai_calls where created_at > now() - interval '7 days'`,
    )
  ).rows[0]!;

  const lines = [
    `${counts.in_review} post${counts.in_review === 1 ? '' : 's'} ready to review.`,
    '',
    appUrl('/week'),
    '',
  ];

  if (counts.revising > 0) {
    lines.push(`${counts.revising} still waiting on something.`, '');
  }

  if (questions.length > 0) {
    lines.push(`${questions.length} open question${questions.length === 1 ? '' : 's'}:`);
    for (const q of questions) {
      lines.push(`  - ${q.text}${q.person ? ` (${q.person})` : ''}`);
    }
    lines.push('', appUrl('/questions'), '');
  }

  lines.push(
    `Last seven days: $${Number(cost.ai).toFixed(2)} of AI across ${cost.calls} calls` +
      `${cost.clips > 0 ? `, ${cost.clips} clips proposed` : ''}.`,
    '',
    'Storage, Railway and Whisper are billed separately and are not in that figure.',
  );

  const result = await sendEmail({
    to: process.env.NOTIFY_EMAIL ?? 'linnea@soilfoodweb.com',
    subject:
      counts.in_review > 0
        ? `${counts.in_review} post${counts.in_review === 1 ? '' : 's'} ready for review`
        : 'Nothing to review this week',
    text: lines.join('\n'),
  });

  console.log(
    `[review_ready_notify] ${result}: ${counts.in_review} ready, ${questions.length} questions`,
  );
});
