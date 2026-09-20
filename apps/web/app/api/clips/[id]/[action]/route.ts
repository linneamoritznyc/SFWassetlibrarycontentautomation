import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { CLIP_RATIOS } from '@sfw/shared';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

/** Reads the database on every call, so it is never prerendered. */
export const dynamic = 'force-dynamic';

type Params = { params: Promise<{ id: string; action: string }> };

/**
 * Keep, cut or trim a clip candidate.
 *
 * Keep clears it to post and cuts the other three ratios, which is why only
 * 9:16 is cut up front: cutting four ratios for fifteen candidates when twelve
 * of them get thrown away is most of the cost of the phase.
 *
 * Cut archives it. Trim moves the boundaries and re-cuts.
 */
export const POST = route(async (request: NextRequest, { params }: Params) => {
  const { id, action } = await params;
  const pool = db();

  const { rows } = await pool.query<{ id: string; clip_start_s: number; clip_end_s: number }>(
    `select id, clip_start_s, clip_end_s from assets where id = $1 and type = 'clip'`,
    [id],
  );
  if (!rows[0]) return fail('No such clip', 404);

  if (action === 'keep') {
    await pool.query(`update assets set status = 'cleared' where id = $1`, [id]);

    for (const ratio of CLIP_RATIOS) {
      await enqueue(pool, {
        type: 'cut_clip',
        payload: { clip_id: id, ratio },
        priority: 4,
        dedupeKey: `cut_clip:${id}:${ratio}`,
      });
    }
    return NextResponse.json({ status: 'cleared', ratios: CLIP_RATIOS });
  }

  if (action === 'cut') {
    await pool.query(`update assets set status = 'archived' where id = $1`, [id]);
    return NextResponse.json({ status: 'archived' });
  }

  if (action === 'trim') {
    const body = (await request.json()) as { start?: number; end?: number };
    const start = body.start ?? rows[0].clip_start_s;
    const end = body.end ?? rows[0].clip_end_s;

    if (!(end > start)) return fail('The end has to come after the start');
    if (end - start < 5) return fail('That is too short to be a clip');
    if (end - start > 180) return fail('That is too long to be a clip');

    await pool.query(
      `update assets set clip_start_s = $2, clip_end_s = $3, duration_s = $3 - $2 where id = $1`,
      [id, start, end],
    );

    // Re-cut the preview. The dedupe key is free again because the previous
    // cut has finished, so this genuinely re-runs.
    await enqueue(pool, {
      type: 'cut_clip',
      payload: { clip_id: id, ratio: '9x16' },
      priority: 3,
      dedupeKey: `cut_clip:${id}:9x16:${start.toFixed(2)}`,
    });

    return NextResponse.json({ start, end });
  }

  return fail(`"${action}" is not something a clip can do. Try keep, cut or trim.`);
});
