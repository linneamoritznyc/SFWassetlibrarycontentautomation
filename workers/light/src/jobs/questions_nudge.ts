import { handler } from '@sfw/queue';
import { db } from '../db.js';
import { appUrl, replyToFor, sendEmail } from '../notify.js';

/** One reminder, after 48 hours, and only one. */
const AFTER_HOURS = 48;

/**
 * Nudges people who have not answered.
 *
 * `nudged_at` is what makes this once and not hourly: the query only picks up
 * questions that have never been nudged, and sets the column as it goes. A
 * second reminder is nagging, and nagging is how people start ignoring the
 * first one.
 */
export const questionsNudge = handler(async () => {
  const pool = db();

  const { rows } = await pool.query<{
    id: number;
    text: string;
    person: string | null;
    email: string | null;
  }>(
    `select q.id, q.text, p.name as person, p.email
     from questions q join people p on p.id = q.asked_to
     where q.status = 'open'
       and q.nudged_at is null
       and q.created_at < now() - ($1 || ' hours')::interval
       and p.email is not null
     order by q.created_at
     limit 20`,
    [AFTER_HOURS],
  );

  for (const question of rows) {
    await sendEmail({
      to: question.email!,
      subject: `Still stuck on this one`,
      replyTo: replyToFor(question.id),
      text: [
        `Hi ${question.person?.split(' ')[0] ?? 'there'},`,
        '',
        'This is holding up a post:',
        '',
        `  ${question.text}`,
        '',
        'One line is enough. Reply to this email, or answer here:',
        appUrl('/questions'),
      ].join('\n'),
    });

    await pool.query('update questions set nudged_at = now() where id = $1', [question.id]);
  }

  // Questions to people with no email on file are not a failure to report
  // every hour, but they are invisible, so say so once per run.
  const unreachable = (
    await pool.query<{ n: number }>(
      `select count(*)::int as n
       from questions q left join people p on p.id = q.asked_to
       where q.status = 'open' and (p.email is null or q.asked_to is null)`,
    )
  ).rows[0]!.n;

  console.log(
    `[questions_nudge] nudged ${rows.length}` +
      (unreachable > 0
        ? `, ${unreachable} open with no email on file (see the Questions view)`
        : ''),
  );
});
