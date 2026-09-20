import { NextResponse, type NextRequest } from 'next/server';
import { exchangeCode, saveTokens } from '@sfw/shared/canva';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

export const dynamic = 'force-dynamic';

/**
 * Where Canva sends the browser back.
 *
 * The state has to match the cookie set when the flow started, or this is not
 * our redirect. The tokens are encrypted before they touch the database.
 */
export const GET = route(async (request: NextRequest) => {
  const code = request.nextUrl.searchParams.get('code');
  const state = request.nextUrl.searchParams.get('state');
  const error = request.nextUrl.searchParams.get('error');

  if (error) return fail(`Canva said: ${error}`);
  if (!code) return fail('Canva sent no code back');

  const expectedState = request.cookies.get('canva_state')?.value;
  const verifier = request.cookies.get('canva_verifier')?.value;

  if (!expectedState || !verifier) {
    return fail('That link has expired. Start again from /settings.', 400);
  }
  if (state !== expectedState) return fail('State did not match. Start again.', 400);

  const tokens = await exchangeCode(code, verifier);
  const pool = db();
  await saveTokens(pool, tokens);

  // Connecting it is the point at which it should start working.
  await pool.query(
    `insert into settings (key, value) values ('flags', jsonb_build_object('canva_enabled', true))
     on conflict (key) do update
       set value = settings.value || jsonb_build_object('canva_enabled', true),
           updated_at = now()`,
  );

  const response = NextResponse.redirect(new URL('/settings?canva=connected', request.url));
  response.cookies.delete('canva_state');
  response.cookies.delete('canva_verifier');
  return response;
});
