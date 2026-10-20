import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { POST_COLUMNS, createPost, guard, sanitizePatch } from '@/lib/wormhole';
import { withDesigns } from '@/lib/wormhole-designs';
import { applyChanges } from '@/lib/wormhole-changes';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

/** All posts, or only those changed after ?since= (for live updates). */
export async function GET(request: Request) {
  const g = await guard();
  if (g instanceof NextResponse) return g;

  await applyChanges();
  const since = new URL(request.url).searchParams.get('since');
  const { rows } = since
    ? await db().query(
        `select ${POST_COLUMNS} from wormhole_posts where updated_at > $1 order by iso_date, id`,
        [since],
      )
    : await db().query(`select ${POST_COLUMNS} from wormhole_posts order by iso_date, id`);

  const { rows: clock } = await db().query(`select now() as now`);
  return NextResponse.json({ posts: withDesigns(rows, !since), now: clock[0].now });
}

/** A new post, for an idea that is not in the plan yet. */
export async function POST(request: Request) {
  const g = await guard();
  if (g instanceof NextResponse) return g;

  const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
  const patch = sanitizePatch(body);
  const post = await createPost(
    { iso_date: patch.iso_date, topic: patch.topic ?? 'New post' },
    g.editor,
  );
  return NextResponse.json({ post });
}
