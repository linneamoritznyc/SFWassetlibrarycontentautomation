import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { POST_COLUMNS, guard, sanitizePatch } from '@/lib/wormhole';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

/** All posts, or only those changed after ?since= (for live updates). */
export async function GET(request: Request) {
  const g = await guard();
  if (g instanceof NextResponse) return g;

  const since = new URL(request.url).searchParams.get('since');
  const { rows } = since
    ? await db().query(
        `select ${POST_COLUMNS} from wormhole_posts where updated_at > $1 order by iso_date, id`,
        [since],
      )
    : await db().query(`select ${POST_COLUMNS} from wormhole_posts order by iso_date, id`);

  const { rows: clock } = await db().query(`select now() as now`);
  return NextResponse.json({ posts: rows, now: clock[0].now });
}

/** A new post, for an idea that is not in the plan yet. */
export async function POST(request: Request) {
  const g = await guard();
  if (g instanceof NextResponse) return g;

  const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
  const patch = sanitizePatch(body);
  const iso = patch.iso_date ?? new Date().toISOString().slice(0, 10);
  const id = `n${Date.now().toString(36)}`;

  const { rows } = await db().query(
    `insert into wormhole_posts (id, iso_date, topic, slides, created_by, updated_by)
     values ($1, $2, $3, $4, $5, $5)
     returning ${POST_COLUMNS}`,
    [id, iso, patch.topic ?? 'New post', JSON.stringify([{ text: '', image: null }]), g.editor],
  );
  return NextResponse.json({ post: rows[0] });
}
