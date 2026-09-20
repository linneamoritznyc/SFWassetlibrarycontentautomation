'use client';

import { useCallback, useEffect, useState } from 'react';

type Feed = {
  id: number;
  name: string;
  url: string;
  kind: string;
  active: boolean;
  items: number;
  last_item: string | null;
};

type Person = {
  id: number;
  name: string;
  role: string | null;
  email: string | null;
  topics: string[];
  open_questions: number;
};

type Prompt = { name: string; version: number; active: boolean; created_at: string; size: number };

type Settings = {
  settings: Record<string, unknown>;
  feeds: Feed[];
  people: Person[];
  prompts: Prompt[];
  cost: {
    total: string;
    calls: number;
    byPrompt: { prompt_name: string; model: string; calls: number; cost: number; avg_ms: number }[];
  };
};

type Health = { workers: { worker: string; beat_at: string; stale: boolean }[] };

/**
 * Settings.
 *
 * Everything here is either a switch or a fact about how the system is
 * configured. Prompts are shown but not editable: a prompt change has to go
 * through the eval, and a text box here would be a way round that.
 */
export function SettingsView() {
  const [data, setData] = useState<Settings | null>(null);
  const [health, setHealth] = useState<Health | null>(null);
  const [note, setNote] = useState('');
  const [busy, setBusy] = useState(false);
  const [connected, setConnected] = useState(false);

  const load = useCallback(async () => {
    const [settings, errors] = await Promise.all([
      fetch('/api/settings').then((r) => r.json() as Promise<Settings>),
      fetch('/api/errors').then((r) => r.json() as Promise<Health>),
    ]);
    setData(settings);
    setHealth(errors);
  }, []);

  useEffect(() => {
    setConnected(new URLSearchParams(window.location.search).get('canva') === 'connected');
    void load().catch(() => setNote('Could not read the settings.'));
  }, [load]);

  async function patch(body: unknown, message: string) {
    await fetch('/api/settings', {
      method: 'PATCH',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body),
    });
    setNote(message);
    setTimeout(() => setNote(''), 2500);
    await load();
  }

  async function importCsv(file: File) {
    setBusy(true);
    try {
      const form = new FormData();
      form.set('file', file);
      const res = await fetch('/api/results/import', { method: 'POST', body: form });
      const body = (await res.json()) as {
        imported?: number;
        rows?: number;
        unmatchedColumns?: string[];
        error?: string;
      };
      setNote(
        res.ok
          ? `Imported ${body.imported} of ${body.rows} rows.` +
              (body.unmatchedColumns?.length
                ? ` Columns not found: ${body.unmatchedColumns.join(', ')}.`
                : '')
          : (body.error ?? 'That did not import.'),
      );
    } finally {
      setBusy(false);
    }
  }

  if (!data) return <main className="p-6 text-sm text-green-mid">{note || 'Loading'}</main>;

  const cadence = data.settings.cadence as
    | {
        feedDays: string[];
        storiesPerWeek: number[];
        shortsPerWeek: number;
        linkedinPerWeek: number[];
        explorationShare: number;
      }
    | undefined;

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="text-lg font-semibold">Settings</h1>
      {note && <p className="mt-2 text-sm font-medium text-green-deep">{note}</p>}

      <Panel title="Cadence">
        {cadence ? (
          <ul className="space-y-0.5 text-sm">
            <li>Feed posts on {cadence.feedDays.join(', ')}</li>
            <li>
              {cadence.storiesPerWeek.join(' to ')} Stories, {cadence.shortsPerWeek} Shorts,{' '}
              {cadence.linkedinPerWeek.join(' to ')} LinkedIn a week
            </li>
            <li>{Math.round(cadence.explorationShare * 100)}% of slots held for experiments</li>
          </ul>
        ) : (
          <p className="text-sm text-green-mid">Not seeded. Run pnpm db:seed.</p>
        )}
        <p className="mt-2 text-xs text-green-mid">
          Edited in <code>packages/shared/src/cadence.ts</code>, then seeded. It decides how many
          slots a week has, which is a decision rather than a setting to fiddle with.
        </p>
      </Panel>

      <Panel title={`Who answers what (${data.people.length})`}>
        <p className="mb-2 text-xs text-green-mid">
          A question goes to the first person whose topics match. Without an email it appears in the
          Questions view but is not sent.
        </p>
        <ul className="space-y-1 text-sm">
          {data.people
            .filter((p) => p.topics.length > 0)
            .map((person) => (
              <li key={person.id} className="flex flex-wrap items-center gap-2">
                <span className="w-40 shrink-0 font-medium">{person.name}</span>
                <input
                  defaultValue={person.email ?? ''}
                  placeholder="no email on file"
                  onBlur={(e) =>
                    e.target.value !== (person.email ?? '') &&
                    patch({ personId: person.id, email: e.target.value }, `Saved ${person.name}.`)
                  }
                  className="w-56 rounded border border-green-mid/40 px-2 py-0.5 text-xs"
                />
                <span className="text-xs text-green-mid">{person.topics.join(', ')}</span>
                {person.open_questions > 0 && (
                  <span className="text-xs text-gold">{person.open_questions} waiting</span>
                )}
              </li>
            ))}
        </ul>
      </Panel>

      <Panel
        title={`Feeds (${data.feeds.filter((f) => f.active).length} of ${data.feeds.length} on)`}
      >
        <ul className="space-y-0.5 text-sm">
          {data.feeds.map((feed) => (
            <li key={feed.id} className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={feed.active}
                onChange={(e) =>
                  patch(
                    { feedId: feed.id, active: e.target.checked },
                    `${feed.name} ${e.target.checked ? 'on' : 'off'}.`,
                  )
                }
              />
              <span className={feed.active ? '' : 'text-green-mid'}>{feed.name}</span>
              <span className="text-xs text-green-mid">
                {feed.items} item{feed.items === 1 ? '' : 's'}
                {feed.active && feed.items === 0 && ' · nothing yet, check the URL'}
              </span>
            </li>
          ))}
        </ul>
      </Panel>

      <Panel title="Prompts">
        <p className="mb-2 text-xs text-green-mid">
          Read-only. A change has to pass the test set before it goes live: edit the file, bump the
          version, seed, then <code>scripts/eval --activate</code>.
        </p>
        <ul className="space-y-0.5 text-sm">
          {data.prompts
            .filter((p) => p.active)
            .map((prompt) => (
              <li key={`${prompt.name}-${prompt.version}`} className="flex gap-2">
                <span className="w-36">{prompt.name}</span>
                <span className="text-green-deep">v{prompt.version}</span>
                <span className="text-xs text-green-mid">
                  {Math.round(prompt.size / 100) / 10}k characters
                  {data.prompts.filter((p) => p.name === prompt.name).length > 1 &&
                    ` · ${data.prompts.filter((p) => p.name === prompt.name).length} versions`}
                </span>
              </li>
            ))}
        </ul>
      </Panel>

      <Panel title="What it costs">
        <p className="text-sm">
          <strong>${Number(data.cost.total).toFixed(2)}</strong> of AI over the last 30 days, across{' '}
          {data.cost.calls} calls.
        </p>
        {data.cost.byPrompt.length > 0 && (
          <table className="mt-2 w-full text-xs">
            <thead>
              <tr className="text-left text-green-mid">
                <th className="py-1">Prompt</th>
                <th>Model</th>
                <th>Calls</th>
                <th>Cost</th>
                <th>Average</th>
              </tr>
            </thead>
            <tbody>
              {data.cost.byPrompt.map((row) => (
                <tr
                  key={`${row.prompt_name}-${row.model}`}
                  className="border-t border-green-mid/10"
                >
                  <td className="py-1">{row.prompt_name}</td>
                  <td className="text-green-mid">{row.model}</td>
                  <td>{row.calls}</td>
                  <td>${row.cost.toFixed(3)}</td>
                  <td className="text-green-mid">{(row.avg_ms / 1000).toFixed(1)}s</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <p className="mt-2 text-xs text-green-mid">
          Storage, Railway and Whisper are billed by those providers and are not in this figure.
        </p>
      </Panel>

      <Panel title="Canva">
        <p className="text-xs text-green-mid">
          Connects through your own Canva account. Approved photo posts get sent into a Canva folder
          as an Instagram-sized design, and the finished design comes back into the library. Brand
          template autofill needs a separate approval from Canva.
        </p>
        <a
          href="/api/canva/auth"
          className="mt-2 inline-block rounded bg-green-deep px-3 py-1.5 text-sm text-cream"
        >
          {connected ? 'Reconnect Canva' : 'Connect Canva'}
        </a>
      </Panel>

      <Panel title="Import results from Later">
        <p className="text-xs text-green-mid">
          Use this when the Instagram Graph API is not set up. In Later: Analytics, pick the range,
          export the CSV. Rows are matched by permalink.
        </p>
        <input
          type="file"
          accept=".csv,text/csv"
          disabled={busy}
          className="mt-2 text-xs"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) void importCsv(file);
          }}
        />
      </Panel>

      <Panel title="What is running">
        {health?.workers.length === 0 && (
          <p className="text-xs text-gold">
            No worker has checked in. Nothing will be tagged, clipped or written.
          </p>
        )}
        <ul className="space-y-1 text-xs">
          {health?.workers.map((worker) => (
            <li key={worker.worker} className="flex items-center gap-2">
              <span
                className={`inline-block h-2 w-2 rounded-full ${worker.stale ? 'bg-gold' : 'bg-green-bright'}`}
                aria-hidden
              />
              {worker.worker}, last beat {new Date(worker.beat_at).toLocaleTimeString()}
            </li>
          ))}
        </ul>
      </Panel>
    </main>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-4 rounded border border-green-mid/20 bg-white p-4">
      <h2 className="mb-2 text-sm font-semibold">{title}</h2>
      {children}
    </section>
  );
}
