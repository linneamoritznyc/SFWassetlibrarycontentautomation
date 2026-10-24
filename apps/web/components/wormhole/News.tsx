'use client';

import { useEffect, useMemo, useState } from 'react';
import type { FeedHealth, ScoutStory } from '@/lib/scout';
import type { WormholePost } from '@/lib/wormhole-types';
import { GREEN } from './util';

type Result = {
  stories: ScoutStory[];
  health: FeedHealth[];
  hidden: string[];
  days: number;
  checked_at: string;
};

/** Where "Not for us" used to live, on one device only. Moved to the server once, then cleared. */
const OLD_HIDDEN_KEY = 'wormhole-news-hidden';

function takeOldHidden(): string[] {
  try {
    const old = JSON.parse(localStorage.getItem(OLD_HIDDEN_KEY) ?? '[]');
    return Array.isArray(old) ? old : [];
  } catch {
    return [];
  }
}

function saveHidden(urls: string[], hidden: boolean) {
  return fetch('/api/wormhole/scout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ urls, hidden }),
  });
}

function shortDate(iso: string | null): string {
  if (!iso) return 'date unknown';
  return new Date(iso).toLocaleDateString('en-US', { day: 'numeric', month: 'short' });
}

/**
 * The Soil news tab: what Scout found in the feeds, best match first. One tap
 * turns a story into a draft post in the plan, with the source already in it.
 */
export function News({
  posts,
  onPlan,
  onOpen,
}: {
  posts: WormholePost[];
  onPlan: (story: ScoutStory) => Promise<void>;
  onOpen: (id: string) => void;
}) {
  const [days, setDays] = useState(14);
  const [data, setData] = useState<Result | null>(null);
  const [error, setError] = useState('');
  const [region, setRegion] = useState('all');
  const [hidden, setHidden] = useState<string[]>([]);
  const [showHidden, setShowHidden] = useState(false);
  const [showFeeds, setShowFeeds] = useState(false);
  const [planning, setPlanning] = useState<string | null>(null);

  // Move anything this device hid before "Not for us" was shared.
  useEffect(() => {
    const old = takeOldHidden();
    if (old.length === 0) return;
    setHidden((h) => Array.from(new Set([...h, ...old])));
    saveHidden(old, true)
      .then((res) => {
        if (!res.ok) return;
        try {
          localStorage.removeItem(OLD_HIDDEN_KEY);
        } catch {
          // Storage blocked; the server copy is what counts.
        }
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    let stop = false;
    setData(null);
    setError('');
    fetch(`/api/wormhole/scout?days=${days}`, { cache: 'no-store' })
      .then(async (res) => {
        if (!res.ok) throw new Error(`The server said ${res.status}`);
        const body = (await res.json()) as Result;
        if (stop) return;
        setData(body);
        setHidden((h) => Array.from(new Set([...body.hidden, ...h])));
      })
      .catch((e) => !stop && setError((e as Error).message));
    return () => {
      stop = true;
    };
  }, [days]);

  // A story is in the plan when a post lists its link as a source.
  const planned = useMemo(() => {
    const m = new Map<string, string>();
    for (const p of posts) for (const s of p.sources) m.set(s.trim(), p.id);
    return m;
  }, [posts]);

  function hide(url: string, on: boolean) {
    const next = on ? [...hidden, url] : hidden.filter((u) => u !== url);
    setHidden(next);
    saveHidden([url], on).catch(() => {});
  }

  const regions = useMemo(
    () => Array.from(new Set(data?.stories.map((s) => s.region) ?? [])).sort(),
    [data],
  );
  const stories = (data?.stories ?? []).filter(
    (s) => (region === 'all' || s.region === region) && showHidden === hidden.includes(s.url),
  );
  const answered = data?.health.filter((h) => h.ok).length ?? 0;
  const failed = data?.health.filter((h) => !h.ok) ?? [];

  const select =
    'rounded-lg border border-neutral-300 bg-white px-3 py-2 text-base text-black outline-none focus:border-[#2f6b46]';

  return (
    <div className="mx-auto max-w-[640px]">
      <div className="mb-4 flex flex-wrap items-center gap-2">
        <select
          className={select}
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
          aria-label="How far back"
        >
          <option value={7}>Last 7 days</option>
          <option value={14}>Last 14 days</option>
          <option value={30}>Last 30 days</option>
        </select>
        <select
          className={select}
          value={region}
          onChange={(e) => setRegion(e.target.value)}
          aria-label="Region"
        >
          <option value="all">Every region</option>
          {regions.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
        <button
          onClick={() => setShowHidden(!showHidden)}
          className="rounded-lg border border-neutral-300 px-3 py-2 text-base"
          aria-pressed={showHidden}
        >
          {showHidden ? 'Back to the news' : `Not for us (${hidden.length})`}
        </button>
      </div>

      {data && (
        <p className="mb-4 text-base text-neutral-600">
          {data.stories.length} soil stories from {answered} of {data.health.length} sources,
          checked{' '}
          {new Date(data.checked_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          .{' '}
          <button onClick={() => setShowFeeds(!showFeeds)} className="underline">
            {showFeeds
              ? 'Hide sources'
              : failed.length
                ? `${failed.length} not answering`
                : 'See sources'}
          </button>
        </p>
      )}

      {showFeeds && data && (
        <ul className="mb-6 space-y-1 rounded-xl border border-neutral-200 p-4 text-sm">
          {data.health.map((h) => (
            <li key={h.feed} className="flex gap-2">
              <span className={h.ok ? 'text-[#2f6b46]' : 'text-[#B23A2E]'}>{h.ok ? '●' : '○'}</span>
              <span>
                <strong>{h.feed}</strong> · {h.region} ·{' '}
                {h.ok
                  ? `${h.fresh} new${h.usedFallback ? ', via news search' : ''}`
                  : `not answering: ${h.error}`}
              </span>
            </li>
          ))}
        </ul>
      )}

      {error && (
        <p className="rounded-lg bg-red-50 px-4 py-3 text-base text-red-800">
          Can’t read the news right now ({error}).
        </p>
      )}
      {!data && !error && (
        <p className="text-lg text-neutral-500">Reading the soil news from every source…</p>
      )}
      {data && stories.length === 0 && (
        <p className="text-lg text-neutral-500">
          {showHidden
            ? 'Nothing set aside.'
            : 'No soil stories here. Try a longer time or every region.'}
        </p>
      )}

      <div className="space-y-4">
        {stories.map((s) => {
          const postId = planned.get(s.url);
          const strong = s.score >= 8;
          return (
            <article key={s.url} className="rounded-xl border border-neutral-200 p-4">
              <div className="mb-1 flex flex-wrap items-center gap-x-2 text-sm text-neutral-500">
                <span
                  className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
                    strong ? 'bg-[#2f6b46] text-white' : 'bg-neutral-100 text-neutral-700'
                  }`}
                >
                  {strong ? 'Close to the soil food web' : 'Soil story'}
                </span>
                <span>
                  {s.source} · {s.region} · {shortDate(s.published)}
                </span>
              </div>
              <a
                href={s.url}
                target="_blank"
                rel="noreferrer"
                className="block text-lg font-semibold leading-snug text-black underline-offset-2 hover:underline"
              >
                {s.title}
              </a>
              {s.summary && (
                <p className="mt-1 line-clamp-3 text-base text-neutral-700">{s.summary}</p>
              )}
              <p className="mt-2 text-sm text-neutral-500">Mentions: {s.matched.join(', ')}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {postId ? (
                  <button
                    onClick={() => onOpen(postId)}
                    className="rounded-lg border px-3 py-2 text-base font-semibold"
                    style={{ borderColor: GREEN, color: GREEN }}
                  >
                    In the plan · open the post
                  </button>
                ) : (
                  <button
                    disabled={planning === s.url}
                    onClick={async () => {
                      setPlanning(s.url);
                      try {
                        await onPlan(s);
                      } finally {
                        setPlanning(null);
                      }
                    }}
                    className="rounded-lg px-3 py-2 text-base font-semibold text-white disabled:opacity-60"
                    style={{ background: GREEN }}
                  >
                    {planning === s.url ? 'Adding…' : 'Add to the plan'}
                  </button>
                )}
                <button
                  onClick={() => hide(s.url, !showHidden)}
                  className="rounded-lg border border-neutral-300 px-3 py-2 text-base"
                >
                  {showHidden ? 'Put it back' : 'Not for us'}
                </button>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
