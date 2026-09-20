import { createHash, randomBytes } from 'node:crypto';
import { NextResponse, type NextRequest } from 'next/server';
import { authorizeUrl } from '@sfw/shared/canva';
import { fail, route } from '@/lib/http';

export const dynamic = 'force-dynamic';

/**
 * Starts the Canva OAuth flow.
 *
 * PKCE, because the code exchange happens on the server but the browser does
 * the redirect: the verifier never leaves this machine, and an intercepted
 * code is useless without it. The state cookie is httpOnly and short-lived,
 * and the callback refuses anything that does not match it.
 */
export const GET = route(async (request: NextRequest) => {
  if (!process.env.CANVA_CLIENT_ID) {
    return fail('Canva is not configured. See docs/TODO-LINNEA.md.', 503);
  }

  const verifier = randomBytes(48).toString('base64url');
  const challenge = createHash('sha256').update(verifier).digest('base64url');
  const state = randomBytes(16).toString('base64url');

  const response = NextResponse.redirect(authorizeUrl(state, challenge));

  const options = {
    httpOnly: true,
    secure: request.nextUrl.protocol === 'https:',
    sameSite: 'lax' as const,
    path: '/api/canva',
    maxAge: 600,
  };

  response.cookies.set('canva_verifier', verifier, options);
  response.cookies.set('canva_state', state, options);

  return response;
});
