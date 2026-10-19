import { NextResponse } from 'next/server';
import {
  AUTH_COOKIE,
  COOKIE_MAX_AGE,
  NAME_COOKIE,
  cleanName,
  expectedToken,
  passwordMatches,
} from '@/lib/wormhole-auth';

export const runtime = 'nodejs';

export async function POST(request: Request) {
  const body = (await request.json().catch(() => ({}))) as { password?: string; name?: string };
  if (!passwordMatches(String(body.password ?? ''))) {
    // A short pause makes guessing slow without bothering real people.
    await new Promise((r) => setTimeout(r, 600));
    return NextResponse.json({ error: 'That password is not right.' }, { status: 401 });
  }
  const token = await expectedToken();
  const res = NextResponse.json({ ok: true });
  const base = {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax' as const,
    path: '/',
    maxAge: COOKIE_MAX_AGE,
  };
  res.cookies.set(AUTH_COOKIE, token!, base);
  res.cookies.set(NAME_COOKIE, cleanName(body.name), base);
  return res;
}
