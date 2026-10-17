import { NextResponse } from 'next/server';
import { AUTH_COOKIE, NAME_COOKIE } from '@/lib/wormhole-auth';

export async function POST() {
  const res = NextResponse.json({ ok: true });
  res.cookies.delete(AUTH_COOKIE);
  res.cookies.delete(NAME_COOKIE);
  return res;
}
