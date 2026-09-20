'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import type { Asset, Facet, LibraryResponse, SmartFolder } from '@/lib/types';
import { AssetDetail } from './AssetDetail';
import { AssetGrid } from './AssetGrid';
import { PasteBox } from './PasteBox';
import { Sidebar } from './Sidebar';
import { UploadPanel } from './UploadPanel';

type Filters = {
  type?: string[];
  status?: string[];
  tags?: { facet: string; name: string }[];
  untagged?: boolean;
  unused?: boolean;
  q?: string;
  meaning?: string;
  similarTo?: string;
};

function toQuery(filters: Filters): string {
  const p = new URLSearchParams();
  for (const t of filters.type ?? []) p.append('type', t);
  for (const s of filters.status ?? []) p.append('status', s);
  for (const tag of filters.tags ?? []) p.append('tag', `${tag.facet}:${tag.name}`);
  if (filters.untagged) p.set('untagged', '1');
  if (filters.unused) p.set('unused', '1');
  if (filters.q) p.set('q', filters.q);
  if (filters.meaning) p.set('meaning', filters.meaning);
  if (filters.similarTo) p.set('similarTo', filters.similarTo);
  p.set('limit', '200');
  return p.toString();
}

/** The library. Every other view is this with the filters pinned. */
export function LibraryView({ initialFilters = {} }: { initialFilters?: Filters }) {
  const [folders, setFolders] = useState<SmartFolder[]>([]);
  const [activeFolder, setActiveFolder] = useState<SmartFolder | null>(null);
  const [filters, setFilters] = useState<Filters>(initialFilters);
  const [result, setResult] = useState<LibraryResponse | null>(null);
  const [selected, setSelected] = useState<Asset | null>(null);
  const [tileSize, setTileSize] = useState(170);
  const [search, setSearch] = useState('');
  const [mode, setMode] = useState<'text' | 'meaning'>('text');
  const [loading, setLoading] = useState(true);
  const [showUpload, setShowUpload] = useState(false);

  useEffect(() => {
    const saved = window.localStorage.getItem('sfw.tileSize');
    if (saved) setTileSize(Number(saved));
  }, []);

  useEffect(() => {
    void fetch('/api/folders')
      .then((r) => r.json())
      .then((body: { folders: SmartFolder[] }) => setFolders(body.folders ?? []))
      .catch(() => setFolders([]));
  }, []);

  const load = useCallback(async (next: Filters) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/assets?${toQuery(next)}`);
      setResult(await res.json());
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load(filters);
  }, [filters, load]);

  const pickFolder = useCallback(
    (folder: SmartFolder | null) => {
      setActiveFolder(folder);
      setSelected(null);
      setSearch('');
      setFilters({ ...initialFilters, ...((folder?.filters as Filters) ?? {}) });
    },
    [initialFilters],
  );

  async function patchAsset(patch: Record<string, unknown>) {
    if (!selected) return;
    const res = await fetch(`/api/assets/${selected.id}`, {
      method: 'PATCH',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(patch),
    });
    const updated = (await res.json()) as Asset;
    setSelected(updated);
    setResult((prev) =>
      prev
        ? {
            ...prev,
            assets: prev.assets.map((a) => (a.id === updated.id ? { ...a, ...updated } : a)),
          }
        : prev,
    );
  }

  async function saveCurrentAsFolder() {
    const name = window.prompt('Name this folder');
    if (!name) return;
    const res = await fetch('/api/folders', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ name, filters }),
    });
    if (res.ok) {
      const folder = (await res.json()) as SmartFolder;
      setFolders((prev) => [...prev.filter((f) => f.id !== folder.id), folder]);
    }
  }

  const facetGroups = useMemo(() => groupFacets(result?.facets ?? []), [result]);

  return (
    <div className="flex h-[calc(100vh-41px)]">
      <Sidebar
        folders={folders}
        activeId={activeFolder?.id ?? null}
        onPick={pickFolder}
        onSaveCurrent={saveCurrentAsFolder}
      />

      <main className="flex-1 overflow-y-auto p-4">
        <div className="mb-4 grid gap-4 lg:grid-cols-[2fr,1fr]">
          <div>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                setFilters((f) => ({
                  ...f,
                  similarTo: undefined,
                  q: mode === 'text' ? search || undefined : undefined,
                  meaning: mode === 'meaning' ? search || undefined : undefined,
                }));
              }}
              className="flex gap-2"
            >
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder={
                  mode === 'meaning'
                    ? 'steaming compost at sunrise'
                    : 'filename, description, creator'
                }
                className="flex-1 rounded border border-green-mid/40 px-3 py-2 text-sm"
              />
              <button
                type="button"
                onClick={() => setMode(mode === 'text' ? 'meaning' : 'text')}
                className="rounded border border-green-mid/40 px-3 py-2 text-xs"
                title="Text search matches words. Meaning search matches what is in the picture."
              >
                {mode === 'text' ? 'Text' : 'Meaning'}
              </button>
              <button type="submit" className="rounded bg-green-deep px-3 py-2 text-sm text-cream">
                Search
              </button>
            </form>

            <div className="mt-2 flex flex-wrap items-center gap-2 text-xs">
              <span className="text-green-mid">
                {loading ? 'Loading' : `${result?.total ?? 0} assets`}
              </span>
              {filters.similarTo && (
                <Chip onClear={() => setFilters((f) => ({ ...f, similarTo: undefined }))}>
                  similar to one asset
                </Chip>
              )}
              {(filters.tags ?? []).map((tag) => (
                <Chip
                  key={`${tag.facet}:${tag.name}`}
                  onClear={() =>
                    setFilters((f) => ({
                      ...f,
                      tags: (f.tags ?? []).filter(
                        (t) => t.name !== tag.name || t.facet !== tag.facet,
                      ),
                    }))
                  }
                >
                  {tag.name}
                </Chip>
              ))}
              <button
                onClick={() => setShowUpload((v) => !v)}
                className="rounded border border-green-mid/40 px-2 py-1"
              >
                {showUpload ? 'Hide upload' : 'Upload'}
              </button>
              <label className="ml-auto flex items-center gap-2">
                Tile size
                <input
                  type="range"
                  min={90}
                  max={320}
                  value={tileSize}
                  onChange={(e) => {
                    setTileSize(Number(e.target.value));
                    window.localStorage.setItem('sfw.tileSize', e.target.value);
                  }}
                />
              </label>
            </div>

            {facetGroups.length > 0 && (
              <div className="mt-3 space-y-1">
                {facetGroups.map(([facet, values]) => (
                  <div key={facet} className="flex flex-wrap items-baseline gap-1 text-xs">
                    <span className="w-20 shrink-0 text-green-mid">{facet}</span>
                    {values.slice(0, 12).map((f) => (
                      <button
                        key={f.name}
                        onClick={() =>
                          setFilters((prev) => ({
                            ...prev,
                            tags: [...(prev.tags ?? []), { facet: f.facet, name: f.name }],
                          }))
                        }
                        className="rounded bg-green-bright/15 px-2 py-0.5 hover:bg-green-bright/30"
                      >
                        {f.name} <span className="text-green-mid">{f.count}</span>
                      </button>
                    ))}
                  </div>
                ))}
              </div>
            )}
          </div>

          <PasteBox />
        </div>

        {showUpload && (
          <div className="mb-4">
            <UploadPanel
              onDone={() => {
                setShowUpload(false);
                void load(filters);
              }}
            />
          </div>
        )}

        <AssetGrid
          assets={result?.assets ?? []}
          tileSize={tileSize}
          selectedId={selected?.id ?? null}
          onSelect={setSelected}
        />
      </main>

      {selected && (
        <AssetDetail
          asset={selected}
          onChange={patchAsset}
          onClose={() => setSelected(null)}
          onFindSimilar={(asset) => {
            setSearch('');
            setFilters({ similarTo: asset.id });
          }}
        />
      )}
    </div>
  );
}

function Chip({ children, onClear }: { children: React.ReactNode; onClear: () => void }) {
  return (
    <button onClick={onClear} className="rounded bg-green-deep px-2 py-0.5 text-cream">
      {children} &times;
    </button>
  );
}

function groupFacets(facets: Facet[]): [string, Facet[]][] {
  const map = new Map<string, Facet[]>();
  for (const facet of facets) {
    const list = map.get(facet.facet) ?? [];
    list.push(facet);
    map.set(facet.facet, list);
  }
  return [...map.entries()];
}
