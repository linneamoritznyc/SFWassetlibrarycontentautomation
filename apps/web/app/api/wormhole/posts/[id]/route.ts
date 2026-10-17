import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { EDITABLE, POST_COLUMNS, guard, sanitizePatch } from '@/lib/wormhole';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

/**
 * Saves an edit. Every save also lands in wormhole_versions with who and when,
 * so nothing anyone types is ever lost.
 */
export async function PATCH(request: Request, { params }: { params: { id: string } }) {
  const g = await guard();
  if (g instanceof NextResponse) return g;

  const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
  const patch = sanitizePatch(body);
  const keys = Object.keys(patch) as (typeof EDITABLE)[number][];
  if (keys.length === 0) return NextResponse.json({ error: 'Nothing to save' }, { status: 400 });

  const sets: string[] = [];
  const values: unknown[] = [params.id];
  for (const k of keys) {
    const v = patch[k];
    values.push(k === 'slides' || k === 'sources' ? JSON.stringify(v) : v);
    sets.push(`${k} = $${values.length}${k === 'slides' || k === 'sources' ? '::jsonb' : ''}`);
  }
  values.push(g.editor);
  sets.push(`updated_by = $${values.length}`, 'updated_at = now()');

  const client = await db().connect();
  try {
    await client.query('begin');
    const { rows } = await client.query(
      `update wormhole_posts set ${sets.join(', ')} where id = $1 returning ${POST_COLUMNS}`,
      values,
    );
    if (rows.length === 0) {
      await client.query('rollback');
      return NextResponse.json({ error: 'No such post' }, { status: 404 });
    }
    const post = rows[0];
    const snapshot = Object.fromEntries(EDITABLE.map((k) => [k, post[k]]));
    await client.query(
      `insert into wormhole_versions (post_id, data, editor) values ($1, $2, $3)`,
      [params.id, JSON.stringify(snapshot), g.editor],
    );
    await client.query('commit');
    return NextResponse.json({ post });
  } catch (err) {
    await client.query('rollback').catch(() => {});
    throw err;
  } finally {
    client.release();
  }
}
