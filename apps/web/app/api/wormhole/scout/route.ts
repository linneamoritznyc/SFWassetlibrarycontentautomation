import { NextResponse } from 'next/server';
import { guard } from '@/lib/wormhole';
import { scout } from '@/lib/scout';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
// Thirty-odd feeds at once; each is cached for three hours, so this is slow only on a cold start.
export const maxDuration = 60;

/** Fresh soil stories from every feed, best match first, and which feeds answered. */
export async function GET(request: Request) {
  const g = await guard();
  if (g instanceof NextResponse) return g;

  const asked = Number(new URL(request.url).searchParams.get('days'));
  const days = Number.isFinite(asked) && asked >= 1 && asked <= 60 ? asked : 14;
  const { stories, health } = await scout(days);
  return NextResponse.json({ stories, health, days, checked_at: new Date().toISOString() });
}
