'use client';

import { useEffect, useState } from 'react';

type Rule = {
  id: number;
  scope: string;
  text: string;
  origin: string;
  evidence: string[];
  active: boolean;
  applied_count: number;
  created_at: string;
};

type Weight = {
  key: string;
  kind: string;
  weight: number;
  data_points: number;
  updated_at: string;
};

type EvalRun = {
  prompt_name: string;
  prompt_version: number | null;
  passed: number;
  failed: number;
  details: { rate?: number; cases?: { name: string; passed: boolean; why: string }[] };
  created_at: string;
};

type Learned = {
  rules: Rule[];
  weights: Weight[];
  evals: EvalRun[];
  latest: { at: string; note: string } | null;
  lightReview: string[];
};

/**
 * What it learned.
 *
 * Every rule says which posts argued for it, every weight says how many data
 * points are behind it, and the eval history says whether the last change made
 * things better or worse. Nothing here is a number without a reason.
 */
export function LearnedView() {
  const [data, setData] = useState<Learned | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void fetch('/api/learned')
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <main className="p-6 text-sm text-green-mid">Loading</main>;
  if (!data) return <main className="p-6 text-sm text-gold">Could not read the learning log.</main>;

  const active = data.rules.filter((r) => r.active);
  const discarded = data.rules.filter((r) => !r.active);

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="text-lg font-semibold">What it learned</h1>

      {data.latest ? (
        <p className="mt-2 rounded border border-green-mid/25 bg-white p-3 text-sm">
          {data.latest.note}
          <span className="mt-1 block text-xs text-green-mid">
            {new Date(data.latest.at).toLocaleDateString()}
          </span>
        </p>
      ) : (
        <p className="mt-2 text-sm text-green-mid">
          Nothing yet. The weekly run needs four weeks of edits before it has anything to say.
        </p>
      )}

      {data.lightReview.length > 0 && (
        <p className="mt-3 rounded border border-green-bright/40 bg-green-bright/10 p-3 text-sm">
          Approved almost every time without edits, so these could move to lighter review:{' '}
          <strong>{data.lightReview.join(', ')}</strong>.
        </p>
      )}

      <Section title={`Rules in force (${active.length})`}>
        {active.length === 0 && (
          <p className="text-sm text-green-mid">None yet, beyond what is in the prompts.</p>
        )}
        <ul className="space-y-2">
          {active.map((rule) => (
            <li key={rule.id} className="rounded border border-green-mid/20 bg-white p-3 text-sm">
              <p>{rule.text}</p>
              <p className="mt-1 text-xs text-green-mid">
                {rule.scope} &middot; learned from {rule.origin} &middot;{' '}
                {Array.isArray(rule.evidence) ? rule.evidence.length : 0} post(s) argued for it
                {rule.applied_count > 0 && ` · applied ${rule.applied_count}x`}
                {' · '}
                {new Date(rule.created_at).toLocaleDateString()}
              </p>
            </li>
          ))}
        </ul>
      </Section>

      {discarded.length > 0 && (
        <Section title={`Proposed and discarded (${discarded.length})`}>
          <p className="mb-2 text-xs text-green-mid">
            These were suggested but made the test set worse, so they were never switched on.
          </p>
          <ul className="space-y-1 text-xs text-green-mid">
            {discarded.map((rule) => (
              <li key={rule.id}>{rule.text}</li>
            ))}
          </ul>
        </Section>
      )}

      <Section title="Planner weights">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs text-green-mid">
              <th className="py-1">What</th>
              <th>Weight</th>
              <th>Data points</th>
            </tr>
          </thead>
          <tbody>
            {data.weights.map((weight) => (
              <tr key={weight.key} className="border-t border-green-mid/10">
                <td className="py-1">{weight.key}</td>
                <td className={weight.weight > 1 ? 'text-green-deep' : ''}>
                  {weight.weight.toFixed(2)}
                </td>
                <td className="text-xs text-green-mid">
                  {weight.data_points || 'none yet, so unchanged'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title="Eval history">
        {data.evals.length === 0 && (
          <p className="text-sm text-green-mid">The test set has not been run yet.</p>
        )}
        <ul className="space-y-1 text-sm">
          {data.evals.map((run, i) => {
            const total = run.passed + run.failed;
            const failures = run.details?.cases?.filter((c) => !c.passed) ?? [];

            return (
              <li key={i} className="border-t border-green-mid/10 py-1">
                <span className={run.failed === 0 ? 'text-green-deep' : 'text-gold'}>
                  {run.passed}/{total}
                </span>{' '}
                <span className="text-xs text-green-mid">
                  {run.prompt_name} v{run.prompt_version} &middot;{' '}
                  {new Date(run.created_at).toLocaleDateString()}
                </span>
                {failures.length > 0 && (
                  <ul className="mt-0.5 text-xs text-gold">
                    {failures.map((f) => (
                      <li key={f.name}>
                        {f.name}: {f.why}
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            );
          })}
        </ul>
      </Section>
    </main>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-6">
      <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-green-mid">{title}</h2>
      {children}
    </section>
  );
}
