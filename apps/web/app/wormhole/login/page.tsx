'use client';

import { useState } from 'react';

export default function WormholeLogin() {
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError('');
    const res = await fetch('/api/wormhole/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password, name }),
    });
    if (res.ok) {
      window.location.href = '/wormhole';
      return;
    }
    const body = await res.json().catch(() => ({}));
    setError(body.error ?? 'Something went wrong. Try again.');
    setBusy(false);
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-white px-4">
      <form onSubmit={submit} className="w-full max-w-sm space-y-6">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#2f6b46]">
            Soil Food Web
          </p>
          <h1 className="mt-2 text-4xl font-bold text-black">Wormhole</h1>
          <p className="mt-2 text-lg text-neutral-600">Every planned post, the way it will look.</p>
        </div>
        <label className="block">
          <span className="text-lg font-medium text-black">Your first name</span>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            autoComplete="given-name"
            placeholder="So we know who changed what"
            className="mt-1 w-full rounded-lg border border-neutral-300 px-4 py-3 text-lg outline-none focus:border-[#2f6b46]"
          />
        </label>
        <label className="block">
          <span className="text-lg font-medium text-black">Password</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
            className="mt-1 w-full rounded-lg border border-neutral-300 px-4 py-3 text-lg outline-none focus:border-[#2f6b46]"
          />
        </label>
        {error && <p className="text-lg font-medium text-red-700">{error}</p>}
        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-lg bg-[#2f6b46] px-4 py-3 text-lg font-semibold text-white disabled:opacity-60"
        >
          {busy ? 'Opening…' : 'Open Wormhole'}
        </button>
      </form>
    </main>
  );
}
