import { createCipheriv, createDecipheriv, randomBytes } from 'node:crypto';

/**
 * The smallest thing that can run a query. Both the worker's pool and the web
 * app's pool satisfy it, which is what lets this file be shared without
 * dragging a database driver into every package that imports it.
 */
export type Queryable = {
  query<T>(text: string, values?: unknown[]): Promise<{ rows: T[] }>;
};

/**
 * Canva Connect, through Linnea's own Canva account.
 *
 * Tokens are encrypted at rest with AES-256-GCM under `TOKEN_ENC_KEY` (backend
 * spec section 9). They are stored in `settings` rather than a table of their
 * own: there is exactly one Canva account, and a table for one row is a table
 * that will be wrong about something later.
 *
 * Everything here no-ops when the integration is off, which it is until
 * Canva approves the access request.
 */

const AUTH_BASE = 'https://www.canva.com/api/oauth';
const API_BASE = 'https://api.canva.com/rest/v1';

export const SCOPES = [
  'asset:read',
  'asset:write',
  'design:content:read',
  'design:content:write',
  'design:meta:read',
  'folder:read',
  'folder:write',
];

export type CanvaTokens = {
  accessToken: string;
  refreshToken: string;
  /** Epoch milliseconds. */
  expiresAt: number;
};

export function encryptionKey(): Buffer {
  const raw = process.env.TOKEN_ENC_KEY;
  if (!raw) throw new Error('TOKEN_ENC_KEY is not set. See docs/TODO-LINNEA.md.');

  const key = Buffer.from(raw, 'base64');
  if (key.length !== 32) {
    throw new Error(`TOKEN_ENC_KEY must be 32 bytes of base64, got ${key.length}.`);
  }
  return key;
}

export function encrypt(plain: string, key = encryptionKey()): string {
  const iv = randomBytes(12);
  const cipher = createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(plain, 'utf8'), cipher.final()]);
  // iv.tag.ciphertext, all base64, so it is one column and one string.
  return [
    iv.toString('base64'),
    cipher.getAuthTag().toString('base64'),
    encrypted.toString('base64'),
  ].join('.');
}

export function decrypt(sealed: string, key = encryptionKey()): string {
  const [iv, tag, data] = sealed.split('.');
  if (!iv || !tag || !data) throw new Error('That does not look like an encrypted token.');

  const decipher = createDecipheriv('aes-256-gcm', key, Buffer.from(iv, 'base64'));
  decipher.setAuthTag(Buffer.from(tag, 'base64'));
  return Buffer.concat([decipher.update(Buffer.from(data, 'base64')), decipher.final()]).toString(
    'utf8',
  );
}

export function authorizeUrl(state: string, codeChallenge: string): string {
  const url = new URL(`${AUTH_BASE}/authorize`);
  url.searchParams.set('code_challenge', codeChallenge);
  url.searchParams.set('code_challenge_method', 'S256');
  url.searchParams.set('scope', SCOPES.join(' '));
  url.searchParams.set('response_type', 'code');
  url.searchParams.set('client_id', process.env.CANVA_CLIENT_ID ?? '');
  url.searchParams.set('redirect_uri', process.env.CANVA_REDIRECT_URI ?? '');
  url.searchParams.set('state', state);
  return url.toString();
}

export async function exchangeCode(code: string, codeVerifier: string): Promise<CanvaTokens> {
  return tokenRequest({
    grant_type: 'authorization_code',
    code,
    code_verifier: codeVerifier,
    redirect_uri: process.env.CANVA_REDIRECT_URI ?? '',
  });
}

async function tokenRequest(body: Record<string, string>): Promise<CanvaTokens> {
  const id = process.env.CANVA_CLIENT_ID;
  const secret = process.env.CANVA_CLIENT_SECRET;
  if (!id || !secret) throw new Error('CANVA_CLIENT_ID or CANVA_CLIENT_SECRET is not set.');

  const res = await fetch(`${AUTH_BASE}/token`, {
    method: 'POST',
    headers: {
      authorization: `Basic ${Buffer.from(`${id}:${secret}`).toString('base64')}`,
      'content-type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams(body),
  });

  if (!res.ok)
    throw new Error(`Canva refused the token request (${res.status}): ${await res.text()}`);

  const json = (await res.json()) as {
    access_token: string;
    refresh_token: string;
    expires_in: number;
  };

  return {
    accessToken: json.access_token,
    refreshToken: json.refresh_token,
    expiresAt: Date.now() + json.expires_in * 1000,
  };
}

export async function saveTokens(pool: Queryable, tokens: CanvaTokens): Promise<void> {
  await pool.query(
    `insert into settings (key, value) values ('canva_tokens', $1::jsonb)
     on conflict (key) do update set value = excluded.value, updated_at = now()`,
    [
      JSON.stringify({
        access: encrypt(tokens.accessToken),
        refresh: encrypt(tokens.refreshToken),
        expiresAt: tokens.expiresAt,
      }),
    ],
  );
}

/**
 * A valid access token, refreshing it first when it is close to expiry.
 *
 * Returns null rather than throwing when Canva has never been connected, so a
 * job can decide that means "skip" rather than "fail".
 */
export async function accessToken(pool: Queryable): Promise<string | null> {
  const { rows } = await pool.query<{
    value: { access: string; refresh: string; expiresAt: number };
  }>(`select value from settings where key = 'canva_tokens'`);

  const stored = rows[0]?.value;
  if (!stored) return null;

  // A minute of slack, so a token does not expire mid-upload.
  if (stored.expiresAt > Date.now() + 60_000) return decrypt(stored.access);

  const refreshed = await tokenRequest({
    grant_type: 'refresh_token',
    refresh_token: decrypt(stored.refresh),
  });

  await saveTokens(pool, refreshed);
  return refreshed.accessToken;
}

export async function canvaFetch<T>(
  token: string,
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      authorization: `Bearer ${token}`,
      'content-type': 'application/json',
      ...(init.headers ?? {}),
    },
  });

  if (!res.ok) throw new Error(`Canva ${path} returned ${res.status}: ${await res.text()}`);
  return (await res.json()) as T;
}

/** Whether the integration is switched on at all. */
export async function canvaEnabled(pool: Queryable): Promise<boolean> {
  const { rows } = await pool.query<{ value: { canva_enabled?: boolean } }>(
    `select value from settings where key = 'flags'`,
  );
  return Boolean(rows[0]?.value?.canva_enabled);
}
