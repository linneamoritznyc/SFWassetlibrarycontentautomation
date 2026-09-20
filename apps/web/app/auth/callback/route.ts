import { NextResponse, type NextRequest } from 'next/server';
import { supabaseServer } from '@/lib/supabase';

/** Where the magic link lands. Swaps the code for a session, then goes in. */
export async function GET(request: NextRequest) {
  const code = request.nextUrl.searchParams.get('code');
  const next = request.nextUrl.searchParams.get('next') ?? '/library';

  if (!code) return NextResponse.redirect(new URL('/login', request.url));

  const supabase = await supabaseServer();
  const { error } = await supabase.auth.exchangeCodeForSession(code);

  if (error) {
    const to = new URL('/login', request.url);
    to.searchParams.set('denied', '1');
    return NextResponse.redirect(to);
  }

  return NextResponse.redirect(new URL(next, request.url));
}
