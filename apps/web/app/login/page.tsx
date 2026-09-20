'use client';

import { createBrowserClient } from '@supabase/ssr';
import { useState } from 'react';

/**
 * Magic link. No passwords to lose, and the allowlist in the middleware is the
 * real gate: a link sent to an address that is not on it will sign in and then
 * be turned away.
 */
export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [state, setState] = useState<'idle' | 'sending' | 'sent' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const denied = typeof window !== 'undefined' && window.location.search.includes('denied=1');

  async function send(event: React.FormEvent) {
    event.preventDefault();
    setState('sending');

    const supabase = createBrowserClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    );

    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: `${window.location.origin}/auth/callback` },
    });

    if (error) {
      setState('error');
      setMessage(error.message);
      return;
    }
    setState('sent');
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-sm flex-col justify-center p-8">
      <h1 className="text-2xl font-semibold">SFW Content Studio</h1>
      <p className="mt-2 text-sm text-green-mid">
        Asset library and content machine for the Soil Food Web Foundation.
      </p>

      {denied && (
        <p className="mt-6 rounded border border-gold bg-gold/10 p-3 text-sm">
          That address is signed in but is not on the allowlist, so there is nothing to show you.
          Add it to <code>APP_ALLOWLIST</code> if it should be.
        </p>
      )}

      {state === 'sent' ? (
        <p className="mt-6 rounded border border-green-mid bg-white p-4 text-sm">
          Check <strong>{email}</strong>. The link signs you in and expires in an hour.
        </p>
      ) : (
        <form onSubmit={send} className="mt-6 space-y-3">
          <label className="block text-sm font-medium" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="linnea@soilfoodweb.com"
            className="w-full rounded border border-green-mid/40 bg-white px-3 py-2"
          />
          <button
            type="submit"
            disabled={state === 'sending'}
            className="w-full rounded bg-green-deep px-3 py-2 text-cream disabled:opacity-60"
          >
            {state === 'sending' ? 'Sending' : 'Send me a link'}
          </button>
          {state === 'error' && <p className="text-sm text-gold">{message}</p>}
        </form>
      )}
    </main>
  );
}
