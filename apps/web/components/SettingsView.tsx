'use client';

import { useEffect, useState } from 'react';

type Health = {
  workers: { worker: string; types: string[]; beat_at: string; stale: boolean }[];
  pending: { type: string; count: number }[];
};

/**
 * Settings, starting with the two things that are needed now: importing results
 * by hand when the Instagram API is not available, and seeing whether anything
 * is actually running.
 *
 * Cadence, feeds, people and the prompt list arrive in Phase 8.
 */
export function SettingsView() {
  const [health, setHealth] = useState<Health | null>(null);
  const [result, setResult] = useState<string>('');
  const [busy, setBusy] = useState(false);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    setConnected(new URLSearchParams(window.location.search).get('canva') === 'connected');
  }, []);

  useEffect(() => {
    void fetch('/api/errors')
      .then((r) => r.json())
      .then(setHealth)
      .catch(() => setHealth(null));
  }, []);

  async function importCsv(file: File) {
    setBusy(true);
    setResult('');
    try {
      const form = new FormData();
      form.set('file', file);

      const res = await fetch('/api/results/import', { method: 'POST', body: form });
      const body = (await res.json()) as {
        imported?: number;
        rows?: number;
        unmatchedColumns?: string[];
        unknownPosts?: string[];
        error?: string;
      };

      if (!res.ok) {
        setResult(body.error ?? 'That did not import.');
        return;
      }

      setResult(
        [
          `Imported ${body.imported} of ${body.rows} row(s).`,
          body.unmatchedColumns?.length
            ? `Columns not found in the CSV: ${body.unmatchedColumns.join(', ')}.`
            : '',
          body.unknownPosts?.length
            ? `${body.unknownPosts.length} row(s) matched no post here, probably published by hand.`
            : '',
        ]
          .filter(Boolean)
          .join(' '),
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="text-lg font-semibold">Settings</h1>

      <section className="mt-6 rounded border border-green-mid/20 bg-white p-4">
        <h2 className="text-sm font-semibold">Import results from Later</h2>
        <p className="mt-1 text-xs text-green-mid">
          Use this when the Instagram Graph API is not set up. In Later, go to Analytics, choose the
          date range and export the CSV. Rows are matched to posts by their permalink, so only posts
          this system knows about are imported.
        </p>

        <input
          type="file"
          accept=".csv,text/csv"
          disabled={busy}
          className="mt-3 text-xs"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) void importCsv(file);
          }}
        />

        {busy && <p className="mt-2 text-xs text-green-mid">Reading it</p>}
        {result && <p className="mt-2 text-xs">{result}</p>}
      </section>

      <section className="mt-4 rounded border border-green-mid/20 bg-white p-4">
        <h2 className="text-sm font-semibold">Canva</h2>
        <p className="mt-1 text-xs text-green-mid">
          Connects through your own Canva account. Approved photo posts get sent into a Canva folder
          as an Instagram-sized design, and the finished design comes back into the library. Brand
          template autofill needs a separate approval from Canva and stays off until then.
        </p>
        <a
          href="/api/canva/auth"
          className="mt-3 inline-block rounded bg-green-deep px-3 py-1.5 text-sm text-cream"
        >
          {connected ? 'Reconnect Canva' : 'Connect Canva'}
        </a>
        {connected && <p className="mt-2 text-xs text-green-deep">Connected.</p>}
      </section>

      <section className="mt-4 rounded border border-green-mid/20 bg-white p-4">
        <h2 className="text-sm font-semibold">What is running</h2>
        {!health && <p className="mt-1 text-xs text-green-mid">Checking</p>}

        {health && health.workers.length === 0 && (
          <p className="mt-1 text-xs text-gold">
            No worker has checked in. Nothing will be tagged, clipped or written.
          </p>
        )}

        <ul className="mt-2 space-y-1 text-xs">
          {health?.workers.map((worker) => (
            <li key={worker.worker} className="flex items-center gap-2">
              <span
                className={`inline-block h-2 w-2 rounded-full ${
                  worker.stale ? 'bg-gold' : 'bg-green-bright'
                }`}
                aria-hidden
              />
              {worker.worker}: {worker.types.length} job types, last beat{' '}
              {new Date(worker.beat_at).toLocaleTimeString()}
            </li>
          ))}
        </ul>

        {(health?.pending.length ?? 0) > 0 && (
          <p className="mt-2 text-xs text-green-mid">
            Waiting: {health!.pending.map((p) => `${p.type} (${p.count})`).join(', ')}
          </p>
        )}
      </section>

      <p className="mt-4 text-xs text-green-mid">
        Cadence, feeds, people and the prompt list arrive in Phase 8. Until then they live in
        <code> packages/shared </code> and the <code>settings</code> table.
      </p>
    </main>
  );
}
