'use client';

import { useState } from 'react';
import { STATUS_LABELS, type Asset } from '@/lib/types';
import { formatDuration } from './AssetGrid';

type Patch = Record<string, unknown>;

/**
 * Everything known about one asset, and everything a human can change about it.
 *
 * The AI's suggestions are shown as suggestions: each one can be accepted or
 * rejected, and accepting keeps the record that the AI suggested it, which is
 * what lets the weekly learning see how often its guesses survive.
 */
export function AssetDetail({
  asset,
  onChange,
  onFindSimilar,
  onClose,
}: {
  asset: Asset;
  onChange: (patch: Patch) => Promise<void>;
  onFindSimilar: (asset: Asset) => void;
  onClose: () => void;
}) {
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState(false);
  const [notes, setNotes] = useState(asset.notes ?? '');

  async function patch(body: Patch) {
    setBusy(true);
    try {
      await onChange(body);
    } finally {
      setBusy(false);
    }
  }

  const suggested = asset.tags.filter((t) => t.source === 'ai' && !t.confirmed);
  const confirmed = asset.tags.filter((t) => t.confirmed);

  return (
    <aside className="w-96 shrink-0 overflow-y-auto border-l border-green-mid/20 bg-white p-4 text-sm">
      <div className="flex items-start justify-between gap-2">
        <h2 className="font-semibold">{asset.filename}</h2>
        <button onClick={onClose} className="text-green-mid" aria-label="Close">
          &times;
        </button>
      </div>

      {asset.thumbUrl && (
        <img
          src={asset.thumbUrl}
          alt={asset.description ?? asset.filename}
          className="mt-3 w-full rounded border border-green-mid/20"
        />
      )}

      {asset.description && <p className="mt-3">{asset.description}</p>}

      <Section title="Status">
        <div className="flex flex-wrap gap-1">
          {Object.entries(STATUS_LABELS).map(([value, label]) => (
            <button
              key={value}
              disabled={busy}
              onClick={() => patch({ status: value })}
              className={`rounded px-2 py-1 text-xs ${
                asset.status === value
                  ? 'bg-green-deep text-cream'
                  : 'border border-green-mid/30 hover:bg-green-bright/10'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </Section>

      <Section title="Quality">
        <div className="flex gap-1">
          {[1, 2, 3, 4, 5].map((n) => (
            <button
              key={n}
              disabled={busy}
              onClick={() => patch({ quality: asset.quality === n ? null : n })}
              className={`h-7 w-7 rounded text-xs ${
                (asset.quality ?? 0) >= n
                  ? 'bg-green-deep text-cream'
                  : 'border border-green-mid/30'
              }`}
            >
              {n}
            </button>
          ))}
          <label className="ml-3 flex items-center gap-1 text-xs">
            <input
              type="checkbox"
              checked={asset.hero_candidate}
              disabled={busy}
              onChange={(e) => patch({ heroCandidate: e.target.checked })}
            />
            Hero
          </label>
        </div>
      </Section>

      {suggested.length > 0 && (
        <Section title={`Suggested tags (${suggested.length})`}>
          <button
            disabled={busy}
            onClick={() => patch({ acceptAllTags: true })}
            className="mb-2 rounded bg-green-deep px-2 py-1 text-xs text-cream"
          >
            Accept all
          </button>
          <ul className="space-y-1">
            {suggested.map((tag) => (
              <li key={`${tag.facet}:${tag.name}`} className="flex items-center gap-2">
                <span className="flex-1 truncate">
                  <span className="text-green-mid">{tag.facet}</span> {tag.name}
                  {tag.confidence != null && (
                    <span className="ml-1 text-xs text-green-mid">
                      {Math.round(tag.confidence * 100)}%
                    </span>
                  )}
                </span>
                <button
                  disabled={busy}
                  onClick={() => patch({ confirmTags: [`${tag.facet}:${tag.name}`] })}
                  className="rounded border border-green-mid/40 px-1.5 text-xs"
                  aria-label={`Accept ${tag.name}`}
                >
                  Keep
                </button>
                <button
                  disabled={busy}
                  onClick={() => patch({ rejectTags: [`${tag.facet}:${tag.name}`] })}
                  className="rounded border border-green-mid/40 px-1.5 text-xs"
                  aria-label={`Reject ${tag.name}`}
                >
                  No
                </button>
              </li>
            ))}
          </ul>
        </Section>
      )}

      {confirmed.length > 0 && (
        <Section title="Tags">
          <div className="flex flex-wrap gap-1">
            {confirmed.map((tag) => (
              <button
                key={`${tag.facet}:${tag.name}`}
                disabled={busy}
                onClick={() => patch({ rejectTags: [`${tag.facet}:${tag.name}`] })}
                title={`Remove ${tag.name}`}
                className="rounded bg-green-bright/20 px-2 py-0.5 text-xs"
              >
                {tag.name} &times;
              </button>
            ))}
          </div>
        </Section>
      )}

      {asset.people.length > 0 && (
        <Section title="People">
          <ul className="space-y-1">
            {asset.people.map((person) => (
              <li key={person.name} className="flex items-center gap-2">
                <span className="flex-1">{person.name}</span>
                {!person.confirmed && (
                  <>
                    <button
                      disabled={busy}
                      onClick={() => patch({ confirmPeople: [person.name] })}
                      className="rounded border border-green-mid/40 px-1.5 text-xs"
                    >
                      Yes
                    </button>
                    <button
                      disabled={busy}
                      onClick={() => patch({ rejectPeople: [person.name] })}
                      className="rounded border border-green-mid/40 px-1.5 text-xs"
                    >
                      No
                    </button>
                  </>
                )}
              </li>
            ))}
          </ul>
        </Section>
      )}

      <Section title="Release">
        <div className="flex gap-1">
          {['unknown', 'signed', 'missing'].map((value) => (
            <button
              key={value}
              disabled={busy}
              onClick={() => patch({ releaseStatus: value })}
              className={`rounded px-2 py-1 text-xs ${
                asset.release_status === value
                  ? 'bg-green-deep text-cream'
                  : 'border border-green-mid/30'
              }`}
            >
              {value}
            </button>
          ))}
        </div>
        {asset.people.length > 0 && asset.release_status !== 'signed' && (
          <p className="mt-1 text-xs text-gold">
            Someone is in this. Check the release before it goes in a post.
          </p>
        )}
      </Section>

      <Section title="Where it came from">
        <dl className="space-y-1 text-xs">
          <Field label="Workshop" value={asset.workshop} />
          <Field label="Creator" value={asset.creator} />
          <Field label="Original path" value={asset.original_path} />
          <Field label="Taken" value={asset.taken_at?.slice(0, 10) ?? null} />
          <Field label="Camera" value={asset.camera} />
          <Field
            label="Size"
            value={asset.width && asset.height ? `${asset.width} x ${asset.height}` : null}
          />
          <Field
            label="Duration"
            value={asset.duration_s != null ? formatDuration(asset.duration_s) : null}
          />
          <Field
            label="Used in"
            value={asset.used_in > 0 ? `${asset.used_in} post(s)` : 'Not yet'}
          />
        </dl>

        <div className="mt-2 flex flex-wrap gap-2">
          {asset.drive_link && (
            <a
              href={asset.drive_link}
              target="_blank"
              rel="noreferrer"
              className="rounded border border-green-mid/40 px-2 py-1 text-xs underline"
            >
              Open original in Drive
            </a>
          )}
          {asset.credit_line && (
            <button
              onClick={async () => {
                await navigator.clipboard.writeText(asset.credit_line!);
                setCopied(true);
                setTimeout(() => setCopied(false), 1500);
              }}
              className="rounded border border-green-mid/40 px-2 py-1 text-xs"
            >
              {copied ? 'Copied' : 'Copy credit line'}
            </button>
          )}
          <button
            onClick={() => onFindSimilar(asset)}
            className="rounded border border-green-mid/40 px-2 py-1 text-xs"
          >
            Find similar
          </button>
        </div>
      </Section>

      <Section title="Notes">
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          onBlur={() => notes !== (asset.notes ?? '') && patch({ notes })}
          rows={3}
          className="w-full rounded border border-green-mid/30 p-2 text-xs"
          placeholder="Anything worth remembering about this one."
        />
      </Section>
    </aside>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-4 border-t border-green-mid/15 pt-3">
      <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-green-mid">{title}</h3>
      {children}
    </section>
  );
}

function Field({ label, value }: { label: string; value: string | null }) {
  if (!value) return null;
  return (
    <div className="flex gap-2">
      <dt className="w-24 shrink-0 text-green-mid">{label}</dt>
      <dd className="flex-1 break-words">{value}</dd>
    </div>
  );
}
