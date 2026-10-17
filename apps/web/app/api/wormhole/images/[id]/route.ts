import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { guard, isUuid } from '@/lib/wormhole';

export const runtime = 'nodejs';

export async function GET(_request: Request, { params }: { params: { id: string } }) {
  const g = await guard();
  if (g instanceof NextResponse) return g;
  if (!isUuid(params.id)) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  const { rows } = await db().query(`select mime, bytes from wormhole_images where id = $1`, [
    params.id,
  ]);
  if (rows.length === 0) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  // Images never change once uploaded; a new upload gets a new id.
  return new NextResponse(new Uint8Array(rows[0].bytes as Buffer), {
    headers: {
      'Content-Type': rows[0].mime,
      'Cache-Control': 'private, max-age=31536000, immutable',
    },
  });
}
