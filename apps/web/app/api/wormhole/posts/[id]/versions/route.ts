import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { guard } from '@/lib/wormhole';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function GET(_request: Request, { params }: { params: { id: string } }) {
  const g = await guard();
  if (g instanceof NextResponse) return g;

  const { rows } = await db().query(
    `select id, data, editor, created_at from wormhole_versions
     where post_id = $1 order by created_at desc limit 30`,
    [params.id],
  );
  return NextResponse.json({ versions: rows });
}
