'use client';

import { useCallback, useEffect, useState } from 'react';
import type { Asset, LibraryResponse } from '@/lib/types';
import { AssetDetail } from './AssetDetail';
import { PasteBox } from './PasteBox';

const SHORTCUTS = [
  ['arrows', 'move'],
  ['1 to 5', 'quality'],
  ['A', 'accept all AI tags'],
  ['C', 'cleared to post'],
  ['X', 'archive'],
  ['H', 'hero'],
] as const;

/**
 * Confirming what the AI guessed, fast.
 *
 * Everything is on the keyboard, because the job is a few hundred assets in one
 * sitting and reaching for the mouse each time is what makes people stop doing
 * it. An asset leaves the inbox when it is cleared or archived, so the list
 * empties as you work.
 */
export function InboxView() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [index, setIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [flash, setFlash] = useState('');

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/assets?status=inbox&status=tagged&limit=200');
      const body = (await res.json()) as LibraryResponse;
      setAssets(body.assets ?? []);
      setIndex((i) => Math.min(i, Math.max(0, (body.assets?.length ?? 1) - 1)));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const current = assets[index];

  const patch = useCallback(
    async (body: Record<string, unknown>, message?: string) => {
      if (!current) return;
      const res = await fetch(`/api/assets/${current.id}`, {
        method: 'PATCH',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body),
      });
      const updated = (await res.json()) as Asset;

      if (message) {
        setFlash(message);
        setTimeout(() => setFlash(''), 1200);
      }

      // Cleared or archived means it has left the inbox: drop it and stay put,
      // so the next one slides under the cursor.
      if (updated.status === 'cleared' || updated.status === 'archived') {
        setAssets((prev) => prev.filter((a) => a.id !== updated.id));
        setIndex((i) => Math.max(0, Math.min(i, assets.length - 2)));
      } else {
        setAssets((prev) => prev.map((a) => (a.id === updated.id ? updated : a)));
      }
    },
    [current, assets.length],
  );

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      const target = event.target as HTMLElement | null;
      if (target && ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName)) return;
      if (event.metaKey || event.ctrlKey || event.altKey) return;

      const key = event.key.toLowerCase();

      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
        event.preventDefault();
        setIndex((i) => Math.min(i + 1, assets.length - 1));
        return;
      }
      if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
        event.preventDefault();
        setIndex((i) => Math.max(i - 1, 0));
        return;
      }

      if (['1', '2', '3', '4', '5'].includes(key)) {
        event.preventDefault();
        void patch({ quality: Number(key) }, `Quality ${key}`);
        return;
      }

      if (key === 'a') {
        event.preventDefault();
        void patch({ acceptAllTags: true }, 'Tags accepted');
      } else if (key === 'c') {
        event.preventDefault();
        void patch({ status: 'cleared' }, 'Cleared to post');
      } else if (key === 'x') {
        event.preventDefault();
        void patch({ status: 'archived' }, 'Archived');
      } else if (key === 'h') {
        event.preventDefault();
        void patch({ heroCandidate: !current?.hero_candidate }, 'Hero');
      }
    }

    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [assets.length, current?.hero_candidate, patch]);

  return (
    <div className="flex h-[calc(100vh-41px)]">
      <main className="flex-1 overflow-y-auto p-4">
        <div className="mb-4 grid gap-4 lg:grid-cols-[2fr,1fr]">
          <div>
            <h1 className="text-lg font-semibold">Inbox</h1>
            <p className="mt-1 text-sm text-green-mid">
              {loading
                ? 'Loading'
                : assets.length === 0
                  ? 'Nothing waiting. Everything has been confirmed.'
                  : `${index + 1} of ${assets.length}`}
            </p>
            <dl className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-green-mid">
              {SHORTCUTS.map(([key, what]) => (
                <div key={key} className="flex gap-1">
                  <dt className="rounded bg-green-bright/20 px-1 font-mono">{key}</dt>
                  <dd>{what}</dd>
                </div>
              ))}
            </dl>
            {flash && <p className="mt-2 text-xs font-medium text-green-deep">{flash}</p>}
          </div>
          <PasteBox />
        </div>

        {current ? (
          <div className="flex flex-col items-start gap-4">
            {current.thumbUrl ? (
              <img
                src={current.thumbUrl}
                alt={current.description ?? current.filename}
                className="max-h-[55vh] rounded border border-green-mid/20"
              />
            ) : (
              <p className="rounded border border-green-mid/20 p-8 text-sm">{current.filename}</p>
            )}
            <div className="flex gap-1 overflow-x-auto">
              {assets.slice(Math.max(0, index - 6), index + 12).map((asset) => (
                <button
                  key={asset.id}
                  onClick={() => setIndex(assets.indexOf(asset))}
                  className={`h-14 w-14 shrink-0 overflow-hidden rounded border ${
                    asset.id === current.id
                      ? 'border-green-deep ring-2 ring-green-deep'
                      : 'border-green-mid/20'
                  }`}
                >
                  {asset.thumbUrl && (
                    <img src={asset.thumbUrl} alt="" className="h-full w-full object-cover" />
                  )}
                </button>
              ))}
            </div>
          </div>
        ) : (
          !loading && <p className="text-sm text-green-mid">Nothing to confirm.</p>
        )}
      </main>

      {current && (
        <AssetDetail
          asset={current}
          onChange={(body) => patch(body)}
          onClose={() => setIndex(0)}
          onFindSimilar={() => undefined}
        />
      )}
    </div>
  );
}
