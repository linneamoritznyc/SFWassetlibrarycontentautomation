import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

/**
 * The door. Every request refreshes the Supabase session and is then checked
 * against APP_ALLOWLIST. Anyone not on the list is signed out and sent back to
 * the login page, whatever they were asking for.
 *
 * The allowlist is read here rather than in each page so there is one place to
 * get it wrong. An empty or missing allowlist means nobody gets in.
 */
export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request });

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  // Not configured yet. Say so plainly instead of failing with a stack trace.
  if (!url || !key) {
    if (request.nextUrl.pathname === '/setup') return response;
    return NextResponse.redirect(new URL('/setup', request.url));
  }

  const supabase = createServerClient(url, key, {
    cookies: {
      getAll() {
        return request.cookies.getAll();
      },
      setAll(toSet) {
        for (const { name, value } of toSet) request.cookies.set(name, value);
        response = NextResponse.next({ request });
        for (const { name, value, options } of toSet) response.cookies.set(name, value, options);
      },
    },
  });

  const {
    data: { user },
  } = await supabase.auth.getUser();

  const allowed = (process.env.APP_ALLOWLIST ?? '')
    .split(',')
    .map((e) => e.trim().toLowerCase())
    .filter(Boolean);

  const email = user?.email?.toLowerCase();
  const isAllowed = Boolean(email) && allowed.includes(email!);

  const path = request.nextUrl.pathname;
  const isPublic = path.startsWith('/login') || path.startsWith('/auth') || path === '/setup';

  if (!isAllowed && !isPublic) {
    const to = new URL('/login', request.url);
    // Signed in but not on the list: say which, rather than looping silently.
    if (user) to.searchParams.set('denied', '1');
    return NextResponse.redirect(to);
  }

  if (isAllowed && path.startsWith('/login')) {
    return NextResponse.redirect(new URL('/library', request.url));
  }

  return response;
}

export const config = {
  // Everything except Next's own assets and the health check.
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|api/health|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
