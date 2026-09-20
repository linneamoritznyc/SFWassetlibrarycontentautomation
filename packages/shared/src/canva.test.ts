import { randomBytes } from 'node:crypto';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { authorizeUrl, decrypt, encrypt, encryptionKey, SCOPES } from './canva.js';

const key = randomBytes(32);

describe('token encryption', () => {
  it('round-trips a token', () => {
    const token = 'canva_access_token_abc123';
    expect(decrypt(encrypt(token, key), key)).toBe(token);
  });

  it('produces a different ciphertext every time', () => {
    // A fresh IV per encryption, so two encryptions of the same token do not
    // look alike in the database.
    expect(encrypt('same', key)).not.toBe(encrypt('same', key));
  });

  it('refuses a tampered ciphertext rather than returning rubbish', () => {
    const sealed = encrypt('secret', key);
    const [iv, tag, data] = sealed.split('.') as [string, string, string];
    const flipped = Buffer.from(data, 'base64');
    flipped[0] = (flipped[0] ?? 0) ^ 0xff;

    expect(() => decrypt([iv, tag, flipped.toString('base64')].join('.'), key)).toThrow();
  });

  it('refuses the wrong key', () => {
    expect(() => decrypt(encrypt('secret', key), randomBytes(32))).toThrow();
  });

  it('says so plainly when the stored value is not a token', () => {
    expect(() => decrypt('nonsense', key)).toThrow(/does not look like an encrypted token/);
  });

  it('handles a unicode token', () => {
    const token = 'tøken-with-ünicode-✓';
    expect(decrypt(encrypt(token, key), key)).toBe(token);
  });
});

describe('the encryption key', () => {
  const original = process.env.TOKEN_ENC_KEY;
  beforeEach(() => {
    delete process.env.TOKEN_ENC_KEY;
  });
  afterEach(() => {
    if (original === undefined) delete process.env.TOKEN_ENC_KEY;
    else process.env.TOKEN_ENC_KEY = original;
  });

  it('says where to look when it is missing', () => {
    expect(() => encryptionKey()).toThrow(/TODO-LINNEA/);
  });

  it('refuses a key of the wrong length rather than failing later', () => {
    process.env.TOKEN_ENC_KEY = Buffer.from('too short').toString('base64');
    expect(() => encryptionKey()).toThrow(/32 bytes/);
  });

  it('accepts 32 bytes of base64', () => {
    process.env.TOKEN_ENC_KEY = randomBytes(32).toString('base64');
    expect(encryptionKey()).toHaveLength(32);
  });
});

describe('the authorize URL', () => {
  const original = { ...process.env };
  beforeEach(() => {
    process.env.CANVA_CLIENT_ID = 'client-123';
    process.env.CANVA_REDIRECT_URI = 'https://studio.example/api/canva/callback';
  });
  afterEach(() => {
    process.env = { ...original };
  });

  it('asks for every scope the jobs need', () => {
    const url = new URL(authorizeUrl('state-1', 'challenge-1'));
    const scopes = url.searchParams.get('scope')!.split(' ');

    for (const needed of ['asset:write', 'design:content:write', 'folder:write']) {
      expect(scopes).toContain(needed);
    }
    expect(scopes).toEqual(SCOPES);
  });

  it('uses PKCE with S256', () => {
    const url = new URL(authorizeUrl('state-1', 'challenge-1'));
    expect(url.searchParams.get('code_challenge_method')).toBe('S256');
    expect(url.searchParams.get('code_challenge')).toBe('challenge-1');
    expect(url.searchParams.get('state')).toBe('state-1');
  });

  it('carries the client id and redirect from the environment', () => {
    const url = new URL(authorizeUrl('s', 'c'));
    expect(url.searchParams.get('client_id')).toBe('client-123');
    expect(url.searchParams.get('redirect_uri')).toBe('https://studio.example/api/canva/callback');
  });
});
