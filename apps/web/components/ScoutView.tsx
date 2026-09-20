'use client';

import { useCallback, useEffect, useState } from 'react';

type Item = {
  id: number;
  url: string;
  title: string | null;
  published_at: string | null;
  summary: string | null;
  relevance: number | null;
  status: string;
  feed: string | null;
  region: string | null;
  language: string | null;
  original_title: string | null;
  original_summary: string | null;
  facts: string[];
  assets: { id: string; description: string | null }[];
  stories: number;
};

type Feed = {
  id: number;
  name: string;
  url: string;
  kind: string;
  active: boolean;
  region: string | null;
  items: number;
  last_ok_at: string | null;
  last_error: string | null;
  last_checked_at: string | null;
  consecutive_failures: number;
};

/**
 * "pt-BR" on a card reads as a file format, not a language. Browsers already
 * carry the full list, so ask them; fall back to the raw tag when they cannot
 * name it rather than showing nothing.
 */
function languageName(tag: string): string {
  try {
    return new Intl.DisplayNames(['en'], { type: 'language' }).of(tag) ?? tag;
  } catch {
    return tag;
  }
}

/**
 * What the scout found.
 *
 * Each card says how relevant it is, what the Foundation already knows that
 * touches it, and whether there is material in the library to carry it.
 * Anything at 0.7 or above has already become a story candidate; the rest sit
 * here in case a human sees an angle the ranker missed.
 */
export function ScoutView() {
  const [items, setItems] = useState<Item[]>([]);
  const [feeds, setFeeds] = useState<Feed[]>([]);
  const [loading, setLoading] = useState(true);
  const [note, setNote] = useState('');

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/scout');
      const body = (await res.json()) as { items: Item[]; feeds: Feed[] };
      setItems(body.items ?? []);
      setFeeds(body.feeds ?? []);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  async function act(item: Item, action: 'dismiss' | 'draft') {
    const res = await fetch(`/api/scout/${item.id}/${action}`, { method: 'POST' });
    const body = (await res.json()) as { note?: string; error?: string };
    setNote(body.error ?? body.note ?? `${action}ed`);
    setTimeout(() => setNote(''), 3000);
    await load();
  }

  const strong = items.filter((i) => (i.relevance ?? 0) >= 0.7 && i.status !== 'dismissed');
  const rest = items.filter((i) => (i.relevance ?? 0) < 0.7 && i.status !== 'dismissed');
  const failing = feeds.filter((f) => f.consecutive_failures > 0);
  const regions = [...new Set(feeds.map((f) => f.region ?? 'Unknown'))];

  return (
    <main className="mx-auto max-w-4xl p-6">
      <header className="mb-4">
        <h1 className="text-lg font-semibold">Scout</h1>
        <p className="mt-1 text-sm text-green-mid">
          {loading
            ? 'Loading'
            : `${strong.length} worth a slot, ${rest.length} adjacent, from ${feeds.filter((f) => f.active).length} feeds.`}
        </p>
      </header>

      {note && <p className="mb-3 text-sm font-medium text-green-deep">{note}</p>}

      {!loading && items.length === 0 && (
        <p className="text-sm text-green-mid">
          Nothing ranked yet. The scout runs at 06:00 and ranks at 06:30.
        </p>
      )}

      <Cards title={`Worth a slot (${strong.length})`} items={strong} onAct={act} />
      <Cards title={`Adjacent (${rest.length})`} items={rest} onAct={act} />

      <section className="mt-8">
        <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-green-mid">
          Feeds ({feeds.length})
        </h2>

        {failing.length > 0 && (
          <p className="mb-2 text-xs font-medium text-green-deep">
            {failing.length} feed{failing.length === 1 ? ' is' : 's are'} failing. Settings has the
            errors.
          </p>
        )}

        {regions.map((region) => (
          <div key={region} className="mb-2">
            <p className="text-xs font-medium">{region}</p>
            <ul className="space-y-0.5 text-xs">
              {feeds
                .filter((f) => (f.region ?? 'Unknown') === region)
                .map((feed) => (
                  <li key={feed.id} className="flex gap-2">
                    <span className={feed.active ? '' : 'text-green-mid line-through'}>
                      {feed.name}
                    </span>
                    <span className="text-green-mid">
                      {feed.items} item{feed.items === 1 ? '' : 's'}
                      {feed.kind !== 'rss' && ` · ${feed.kind}`}
                      {feed.consecutive_failures > 0 && ` · failing (${feed.consecutive_failures})`}
                    </span>
                  </li>
                ))}
            </ul>
          </div>
        ))}

        <p className="mt-2 text-xs text-green-mid">
          A feed with no items after a few days is probably a dead URL. They are listed in
          <code> packages/shared/src/feeds.ts</code>, and <code>pnpm feeds:check</code> tests every
          one of them from a machine with a normal internet connection.
        </p>
      </section>
    </main>
  );
}

function Cards({
  title,
  items,
  onAct,
}: {
  title: string;
  items: Item[];
  onAct: (item: Item, action: 'dismiss' | 'draft') => void;
}) {
  if (items.length === 0) return null;

  return (
    <section className="mb-8">
      <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-green-mid">{title}</h2>
      <ul className="space-y-3">
        {items.map((item) => (
          <li key={item.id} className="rounded border border-green-mid/20 bg-white p-3">
            <div className="flex items-baseline gap-2">
              <a href={item.url} target="_blank" rel="noreferrer" className="font-medium underline">
                {item.title ?? item.url}
              </a>
              <span className="ml-auto shrink-0 text-xs text-green-mid">
                {item.relevance != null && `${Math.round(item.relevance * 100)}%`}
              </span>
            </div>

            <p className="mt-1 flex flex-wrap items-center gap-1 text-xs text-green-mid">
              {item.region && (
                <span className="rounded bg-green-deep/10 px-1.5 py-0.5 text-green-deep">
                  {item.region}
                </span>
              )}
              {item.original_title && item.language && (
                <span className="rounded bg-green-deep/10 px-1.5 py-0.5 text-green-deep">
                  {languageName(item.language)}
                </span>
              )}
              <span>
                {item.feed}
                {item.published_at && ` · ${new Date(item.published_at).toLocaleDateString()}`}
                {item.stories > 0 && ' · already a story candidate'}
              </span>
            </p>

            {item.summary && <p className="mt-2 text-sm">{item.summary}</p>}

            {/* Published in another language: the summary above is ours, in
                English. These are the source's own words, kept so a reader who
                does speak it can check us. */}
            {item.original_title && (
              <p className="mt-1 text-xs text-green-mid" lang={item.language ?? undefined}>
                {item.original_title}
                {item.original_summary && ` — ${item.original_summary}`}
              </p>
            )}

            {item.facts.length > 0 && (
              <details className="mt-2 text-xs">
                <summary className="cursor-pointer text-green-mid">
                  What we already know about this ({item.facts.length})
                </summary>
                <ul className="mt-1 list-disc space-y-0.5 pl-5">
                  {item.facts.slice(0, 5).map((fact, i) => (
                    <li key={i}>{fact}</li>
                  ))}
                </ul>
              </details>
            )}

            <p className="mt-2 text-xs text-green-mid">
              {item.assets.length > 0
                ? `${item.assets.length} asset(s) in the library could carry this.`
                : 'Nothing in the library matches it yet, so a post would need a shot.'}
            </p>

            <div className="mt-2 flex gap-2">
              {item.status !== 'drafted' && (
                <button
                  onClick={() => onAct(item, 'draft')}
                  className="rounded bg-green-deep px-2 py-1 text-xs text-cream"
                >
                  Make a story
                </button>
              )}
              <button
                onClick={() => onAct(item, 'dismiss')}
                className="rounded border border-green-mid/40 px-2 py-1 text-xs"
              >
                Dismiss
              </button>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
