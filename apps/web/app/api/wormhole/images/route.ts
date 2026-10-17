import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { guard } from '@/lib/wormhole';

export const runtime = 'nodejs';

const TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
const MAX_BYTES = 4 * 1024 * 1024;

/**
 * Takes one image as the raw request body. The browser shrinks Canva exports
 * to 1440 px wide before sending, so they stay well under Vercel's body limit.
 */
export async function POST(request: Request) {
  const g = await guard();
  if (g instanceof NextResponse) return g;

  const mime = (request.headers.get('content-type') ?? '').split(';')[0]?.trim() ?? '';
  if (!TYPES.includes(mime)) {
    return NextResponse.json({ error: 'Use a JPG, PNG, WebP or GIF.' }, { status: 415 });
  }
  const bytes = Buffer.from(await request.arrayBuffer());
  if (bytes.length === 0 || bytes.length > MAX_BYTES) {
    return NextResponse.json({ error: 'That image is too big.' }, { status: 413 });
  }
  const width = Number(request.headers.get('x-width')) || null;
  const height = Number(request.headers.get('x-height')) || null;

  const { rows } = await db().query(
    `insert into wormhole_images (mime, bytes, width, height, uploaded_by)
     values ($1, $2, $3, $4, $5) returning id`,
    [mime, bytes, width, height, g.editor],
  );
  return NextResponse.json({ id: rows[0].id });
}
