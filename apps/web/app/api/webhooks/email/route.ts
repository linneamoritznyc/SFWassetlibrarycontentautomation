import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { db } from '@/lib/db';
import { questionIdFrom, stripQuotedReply, verifySignature } from '@/lib/email';
import { fail, route } from '@/lib/http';

export const dynamic = 'force-dynamic';

/**
 * People answer questions by replying to the email.
 *
 * The question id is carried in the reply-to address
 * (`questions+<id>@...`) and, as a fallback, in a marker line in the body.
 * The provider signs the delivery; the signature is checked before anything is
 * written, because this endpoint is public and its whole job is to put text
 * into the knowledge base.
 */
export const POST = route(async (request: NextRequest) => {
  const secret = process.env.INBOUND_EMAIL_SECRET;
  if (!secret) return fail('Inbound email is not configured', 503);

  const raw = await request.text();
  const signature = request.headers.get('x-webhook-signature') ?? '';

  if (!verifySignature(raw, signature, secret)) return fail('Bad signature', 401);

  const payload = JSON.parse(raw) as {
    to?: string;
    from?: string;
    subject?: string;
    text?: string;
  };

  const questionId = questionIdFrom(payload.to, payload.subject, payload.text);
  if (!questionId) return fail('Could not tell which question this answers');

  const answer = stripQuotedReply(payload.text ?? '');
  if (!answer) return fail('That reply had no answer in it');

  const pool = db();
  const { rowCount } = await pool.query(
    `update questions set answer = $2, answered_at = now(), status = 'answered'
     where id = $1 and status = 'open'`,
    [questionId, answer],
  );

  // Already answered is not an error: people reply twice.
  if (rowCount === 0) return NextResponse.json({ status: 'already answered' });

  await enqueue(pool, {
    type: 'save_fact',
    payload: { question_id: questionId },
    priority: 2,
    dedupeKey: `save_fact:${questionId}`,
  });

  return NextResponse.json({ status: 'answered', questionId });
});
