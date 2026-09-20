'use client';

import type { Asset } from '@/lib/types';

/**
 * The tiles.
 *
 * Plain <img> rather than next/image on purpose: every thumbnail is a
 * presigned R2 URL whose host and query string change every hour, which
 * next/image cannot cache and would only proxy. Videos get their own row at the top of every folder, because a
 * workshop video is a different kind of thing from a photo and burying it in a
 * grid of stills makes it unfindable.
 */
export function AssetGrid({
  assets,
  tileSize,
  selectedId,
  onSelect,
}: {
  assets: Asset[];
  tileSize: number;
  selectedId: string | null;
  onSelect: (asset: Asset) => void;
}) {
  const moving = assets.filter(
    (a) => a.type === 'video' || a.type === 'clip' || a.type === 'render',
  );
  const still = assets.filter((a) => !['video', 'clip', 'render'].includes(a.type));

  return (
    <div className="space-y-6">
      {moving.length > 0 && (
        <Row
          title={`Video (${moving.length})`}
          assets={moving}
          tileSize={Math.round(tileSize * 1.4)}
          selectedId={selectedId}
          onSelect={onSelect}
        />
      )}
      {still.length > 0 && (
        <Row
          title={moving.length > 0 ? `Stills (${still.length})` : null}
          assets={still}
          tileSize={tileSize}
          selectedId={selectedId}
          onSelect={onSelect}
        />
      )}
      {assets.length === 0 && (
        <p className="p-8 text-center text-sm text-green-mid">
          Nothing here. Try a different folder, or clear the filters.
        </p>
      )}
    </div>
  );
}

function Row({
  title,
  assets,
  tileSize,
  selectedId,
  onSelect,
}: {
  title: string | null;
  assets: Asset[];
  tileSize: number;
  selectedId: string | null;
  onSelect: (asset: Asset) => void;
}) {
  return (
    <section>
      {title && (
        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-green-mid">
          {title}
        </h3>
      )}
      <div
        className="grid gap-2"
        style={{ gridTemplateColumns: `repeat(auto-fill, minmax(${tileSize}px, 1fr))` }}
      >
        {assets.map((asset) => (
          <Tile
            key={asset.id}
            asset={asset}
            selected={asset.id === selectedId}
            onSelect={() => onSelect(asset)}
          />
        ))}
      </div>
    </section>
  );
}

function Tile({
  asset,
  selected,
  onSelect,
}: {
  asset: Asset;
  selected: boolean;
  onSelect: () => void;
}) {
  const unconfirmed = asset.tags.filter((t) => t.source === 'ai' && !t.confirmed).length;

  return (
    <button
      onClick={onSelect}
      className={`group relative aspect-square overflow-hidden rounded border text-left ${
        selected ? 'border-green-deep ring-2 ring-green-deep' : 'border-green-mid/20'
      }`}
      title={asset.description ?? asset.filename}
    >
      {asset.thumbUrl ? (
        <img
          src={asset.thumbUrl}
          alt={asset.description ?? asset.filename}
          loading="lazy"
          className="h-full w-full object-cover"
        />
      ) : (
        <span className="flex h-full w-full items-center justify-center bg-green-bright/10 p-2 text-center text-[10px] text-green-mid">
          {asset.filename}
        </span>
      )}

      <span className="pointer-events-none absolute left-1 top-1 flex gap-1">
        {asset.duration_s != null && <Badge>{formatDuration(asset.duration_s)}</Badge>}
        {asset.type === 'doc' && <Badge>PDF</Badge>}
        {asset.type === 'reference' && <Badge>Ref</Badge>}
      </span>

      <span className="pointer-events-none absolute right-1 top-1 flex gap-1">
        {asset.hero_candidate && <Badge>Hero</Badge>}
        {unconfirmed > 0 && <Badge>{unconfirmed} to check</Badge>}
      </span>

      {asset.status === 'cleared' && (
        <span className="pointer-events-none absolute bottom-1 left-1">
          <Badge>Cleared</Badge>
        </span>
      )}
      {asset.used_in > 0 && (
        <span className="pointer-events-none absolute bottom-1 right-1">
          <Badge>Used {asset.used_in}x</Badge>
        </span>
      )}
    </button>
  );
}

function Badge({ children }: { children: React.ReactNode }) {
  return (
    <span className="rounded bg-green-deep/80 px-1 py-0.5 text-[10px] leading-none text-cream">
      {children}
    </span>
  );
}

export function formatDuration(seconds: number): string {
  const total = Math.round(seconds);
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${m}:${String(s).padStart(2, '0')}`;
}
