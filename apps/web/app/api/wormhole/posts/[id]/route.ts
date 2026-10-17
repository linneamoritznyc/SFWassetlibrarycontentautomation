import { NextResponse } from 'next/server';
import { guard, sanitizePatch, savePost } from '@/lib/wormhole';

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
  if (Object.keys(patch).length === 0) {
    return NextResponse.json({ error: 'Nothing to save' }, { status: 400 });
  }

  const post = await savePost(params.id, patch, g.editor);
  if (!post) return NextResponse.json({ error: 'No such post' }, { status: 404 });
  return NextResponse.json({ post });
}
