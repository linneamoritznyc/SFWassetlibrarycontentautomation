import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

export const dynamic = 'force-dynamic';

/**
 * Answering a question. The answer is stored, then `save_fact` turns it into
 * permanent facts and releases whatever post was waiting on it.
 */
export const POST = route(
  async (request: NextRequest, { params }: { params: Promise<{ id: string }> }) => {
    const { id } = await params;
    const body = (await request.json()) as { answer?: string; drop?: boolean };
    const pool = db();

    if (body.drop) {
      await pool.query(`update questions set status = 'dropped' where id = $1`, [id]);
      return NextResponse.json({ status: 'dropped' });
    }

    if (!body.answer?.trim()) return fail('An answer needs some words in it');

    const { rowCount } = await pool.query(
      `update questions set answer = $2, answered_at = now(), status = 'answered'
     where id = $1 and status <> 'dropped'`,
      [id, body.answer.trim()],
    );

    if (rowCount === 0) return fail('No such question, or it was dropped', 404);

    await enqueue(pool, {
      type: 'save_fact',
      payload: { question_id: Number(id) },
      priority: 2,
      dedupeKey: `save_fact:${id}`,
    });

    return NextResponse.json({ status: 'answered' });
  },
);
