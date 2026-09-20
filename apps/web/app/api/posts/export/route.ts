import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

export const dynamic = 'force-dynamic';

/** Packs the approved posts into a ZIP for Later. */
export const POST = route(async (request: NextRequest) => {
  const body = (await request.json().catch(() => ({}))) as { postIds?: string[] };
  const pool = db();

  const { rows } = await pool.query<{ n: number }>(
    `select count(*)::int as n from posts where status = 'approved'
     ${body.postIds?.length ? 'and id = any($1::uuid[])' : ''}`,
    body.postIds?.length ? [body.postIds] : [],
  );

  if (rows[0]!.n === 0) return fail('Nothing approved to export');

  const jobId = await enqueue(pool, {
    type: 'export_bundle',
    payload: { post_ids: body.postIds ?? [] },
    priority: 3,
    dedupeKey: `export_bundle:${new Date().toISOString().slice(0, 16)}`,
  });

  return NextResponse.json({ queued: jobId, posts: rows[0]!.n });
});
