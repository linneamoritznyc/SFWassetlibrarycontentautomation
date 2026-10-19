/**
 * Wormhole's shared-password door. Runs in middleware (edge) and in route
 * handlers (node), so it only uses Web Crypto.
 *
 * The cookie holds a hash of the password and a server secret, never the
 * password itself. Changing either env var signs everyone out. With no
 * WORMHOLE_PASSWORD set, nobody gets in.
 */
export const AUTH_COOKIE = 'wh_auth';
export const NAME_COOKIE = 'wh_name';
export const COOKIE_MAX_AGE = 60 * 60 * 24 * 30;

export async function expectedToken(): Promise<string | null> {
  const password = process.env.WORMHOLE_PASSWORD;
  if (!password) return null;
  const secret = process.env.WORMHOLE_SECRET ?? '';
  const data = new TextEncoder().encode(`wormhole:${password}:${secret}`);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

export async function isValidToken(token: string | undefined): Promise<boolean> {
  if (!token) return false;
  const expected = await expectedToken();
  if (!expected || expected.length !== token.length) return false;
  let diff = 0;
  for (let i = 0; i < expected.length; i++) diff |= expected.charCodeAt(i) ^ token.charCodeAt(i);
  return diff === 0;
}

export function passwordMatches(given: string): boolean {
  const password = process.env.WORMHOLE_PASSWORD;
  if (!password) return false;
  return given.trim().toLowerCase() === password.trim().toLowerCase();
}

export function cleanName(raw: string | undefined | null): string {
  const name = (raw ?? '').replace(/\s+/g, ' ').trim().slice(0, 40);
  return name || 'Someone';
}
