import { NextResponse, type NextRequest } from 'next/server';
import { db } from '@/lib/db';
import { route } from '@/lib/http';

export const dynamic = 'force-dynamic';

/** Open questions, oldest first, with who they went to and what they block. */
export const GET = route(async (request: NextRequest) => {
  const status = request.nextUrl.searchParams.get('status') ?? 'open';

  const { rows } = await db().query(
    `select q.id, q.text, q.status, q.answer, q.answered_at, q.created_at, q.nudged_at,
            q.context, p.name as asked_to, p.email as asked_to_email,
            post.hook as post_hook, post.slot_date::text as post_slot
     from questions q
     left join people p on p.id = q.asked_to
     left join posts post on post.id::text = q.context->>'post_id'
     where ($1 = 'all' or q.status = $1)
     order by q.created_at`,
    [status],
  );

  return NextResponse.json({ questions: rows });
});
