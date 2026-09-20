'use client';

import { useCallback, useEffect, useState } from 'react';

type Job = {
  id: string;
  type: string;
  payload: Record<string, unknown>;
  attempts: number;
  max_attempts: number;
  error: string | null;
  updated_at: string;
};

type Worker = { worker: string; types: string[]; beat_at: string; stale: boolean };
type Pending = { type: string; count: number };

/**
 * Dead jobs and worker health on one screen, because the two questions run
 * together: work piling up with no heartbeat is a worker that is down, which is
 * a different problem from a job that keeps failing for its own reasons.
 */
export function ErrorsView() {
  const [dead, setDead] = useState<Job[]>([]);
  const [workers, setWorkers] = useState<Worker[]>([]);
  const [pending, setPending] = useState<Pending[]>([]);
  const [loading, setLoading] = useState(true);
  const [note, setNote] = useState('');

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/errors');
      const body = (await res.json()) as { dead: Job[]; workers: Worker[]; pending: Pending[] };
      setDead(body.dead ?? []);
      setWorkers(body.workers ?? []);
      setPending(body.pending ?? []);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
    const timer = setInterval(() => void load(), 30_000);
    return () => clearInterval(timer);
  }, [load]);

  async function retry(id: string) {
    const res = await fetch(`/api/errors/${id}/retry`, { method: 'POST' });
    if (res.ok) {
      setDead((prev) => prev.filter((j) => j.id !== id));
      setNote('Back on the queue.');
    } else {
      const body = (await res.json()) as { error?: string };
      setNote(body.error ?? 'Could not retry that one.');
    }
    setTimeout(() => setNote(''), 3000);
  }

  return (
    <main className="mx-auto max-w-5xl p-6">
      <h1 className="text-lg font-semibold">Errors</h1>

      <section className="mt-4">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-green-mid">Workers</h2>
        {workers.length === 0 ? (
          <p className="mt-1 text-sm text-gold">
            No worker has ever checked in. Nothing will be tagged, transcribed or written until one
            is running.
          </p>
        ) : (
          <ul className="mt-1 space-y-1 text-sm">
            {workers.map((worker) => (
              <li key={worker.worker} className="flex items-center gap-2">
                <span
                  className={`inline-block h-2 w-2 rounded-full ${
                    worker.stale ? 'bg-gold' : 'bg-green-bright'
                  }`}
                  aria-hidden
                />
                <span className="font-medium">{worker.worker}</span>
                <span className="text-xs text-green-mid">
                  {worker.stale ? 'last seen' : 'alive, last beat'}{' '}
                  {new Date(worker.beat_at).toLocaleString()}
                </span>
                <span className="text-xs text-green-mid">{worker.types.length} job types</span>
              </li>
            ))}
          </ul>
        )}
      </section>

      {pending.length > 0 && (
        <section className="mt-4">
          <h2 className="text-xs font-semibold uppercase tracking-wide text-green-mid">Waiting</h2>
          <ul className="mt-1 flex flex-wrap gap-2 text-xs">
            {pending.map((p) => (
              <li key={p.type} className="rounded bg-green-bright/15 px-2 py-1">
                {p.type} <span className="text-green-mid">{p.count}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="mt-6">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-green-mid">
          Dead jobs ({dead.length})
        </h2>
        {note && <p className="mt-1 text-xs text-green-deep">{note}</p>}

        {loading && dead.length === 0 ? (
          <p className="mt-2 text-sm text-green-mid">Loading</p>
        ) : dead.length === 0 ? (
          <p className="mt-2 text-sm text-green-mid">Nothing has died. Good.</p>
        ) : (
          <ul className="mt-2 space-y-2">
            {dead.map((job) => (
              <li key={job.id} className="rounded border border-green-mid/20 bg-white p-3 text-sm">
                <div className="flex items-baseline gap-2">
                  <span className="font-medium">{job.type}</span>
                  <span className="text-xs text-green-mid">
                    #{job.id} &middot; {job.attempts} of {job.max_attempts} attempts &middot;{' '}
                    {new Date(job.updated_at).toLocaleString()}
                  </span>
                  <button
                    onClick={() => retry(job.id)}
                    className="ml-auto rounded bg-green-deep px-2 py-1 text-xs text-cream"
                  >
                    Retry
                  </button>
                </div>
                <pre className="mt-2 max-h-32 overflow-auto whitespace-pre-wrap rounded bg-green-bright/10 p-2 text-xs">
                  {job.error ?? 'No error recorded.'}
                </pre>
                <p className="mt-1 text-xs text-green-mid">{JSON.stringify(job.payload)}</p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
