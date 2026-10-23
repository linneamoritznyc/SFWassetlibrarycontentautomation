'use client';

import { useEffect, useRef, useState } from 'react';
import { STATUSES, type WormholePost } from '@/lib/wormhole-types';
import { ago } from './util';

type Patch = Partial<WormholePost>;

const field =
  'mt-1 w-full rounded-lg border border-neutral-300 bg-white px-3 py-2 text-base text-black outline-none focus:border-[#2f6b46]';
const label = 'block text-sm font-semibold uppercase tracking-wide text-neutral-600';

function AutoText({
  value,
  onChange,
  rows = 2,
  placeholder,
}: {
  value: string;
  onChange: (v: string) => void;
  rows?: number;
  placeholder?: string;
}) {
  const ref = useRef<HTMLTextAreaElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = `${el.scrollHeight + 2}px`;
  }, [value]);
  return (
    <textarea
      ref={ref}
      rows={rows}
      value={value}
      placeholder={placeholder}
      onChange={(e) => onChange(e.target.value)}
      className={`${field} resize-none leading-relaxed`}
    />
  );
}

/** The first web link in the visual note: the post's Canva design. */
function designLink(note: string): string {
  return note.match(/https?:\/\/\S+/)?.[0] ?? '';
}

/** Everything about one post, edited in place under its preview. */
export function Editor({ post, onChange }: { post: WormholePost; onChange: (p: Patch) => void }) {
  const [history, setHistory] = useState<
    { id: number; data: Patch; editor: string; created_at: string }[] | null
  >(null);

  async function loadHistory() {
    const res = await fetch(`/api/wormhole/posts/${post.id}/versions`);
    if (res.ok) setHistory((await res.json()).versions);
  }

  const [design, setDesignText] = useState(() => designLink(post.visual_note));
  useEffect(() => setDesignText(designLink(post.visual_note)), [post.id]); // eslint-disable-line react-hooks/exhaustive-deps

  /** Keeps the Canva link as the first line of the visual note, replacing the old one. */
  function setDesign(text: string) {
    setDesignText(text);
    const v = text.trim();
    if (v && !/^https?:\/\/\S+$/.test(v)) return; // half-typed: wait for a whole link
    const old = designLink(post.visual_note);
    const rest = post.visual_note
      .split('\n')
      .filter((l) => !l.startsWith('Canva: ') && !(old && l.includes(old)))
      .join('\n')
      .trim();
    onChange({ visual_note: v ? `Canva: ${v}${rest ? `\n${rest}` : ''}` : rest });
  }

  return (
    <div className="space-y-5 border-t border-neutral-200 bg-neutral-50 px-4 py-5">
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className={label}>What the post is about</span>
          <input
            className={field}
            value={post.topic}
            onChange={(e) => onChange({ topic: e.target.value })}
          />
        </label>
        <label className="block">
          <span className={label}>Date</span>
          <input
            type="date"
            className={field}
            value={post.iso_date}
            disabled={post.date_tbd}
            onChange={(e) => e.target.value && onChange({ iso_date: e.target.value })}
          />
          <span className="mt-1 flex items-center gap-2 text-base">
            <input
              type="checkbox"
              checked={post.date_tbd}
              onChange={(e) => onChange({ date_tbd: e.target.checked })}
            />
            No date yet (Date TBD)
          </span>
        </label>
      </div>

      <label className="block">
        <span className={label}>Status</span>
        <select
          className={field}
          value={post.status}
          onChange={(e) => onChange({ status: e.target.value as WormholePost['status'] })}
        >
          {STATUSES.map((s) => (
            <option key={s.value} value={s.value}>
              {s.label}
            </option>
          ))}
        </select>
      </label>

      <div>
        <span className={label}>Slides</span>
        <div className="mt-1 flex gap-2">
          <input
            className={field.replace('mt-1 ', '')}
            type="url"
            inputMode="url"
            placeholder="Paste the Canva link for these slides"
            value={design}
            onChange={(e) => setDesign(e.target.value)}
          />
          {/^https?:\/\/\S+$/.test(design.trim()) && (
            <a
              href={design.trim()}
              target="_blank"
              rel="noreferrer"
              className="shrink-0 self-center rounded-lg border border-[#2f6b46] px-4 py-2 font-semibold text-[#2f6b46]"
            >
              Open
            </a>
          )}
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className={label}>CTA</span>
          <input
            className={field}
            value={post.cta}
            onChange={(e) => onChange({ cta: e.target.value })}
          />
        </label>
        <label className="block">
          <span className={label}>Link</span>
          <input
            className={field}
            value={post.link}
            inputMode="url"
            onChange={(e) => onChange({ link: e.target.value })}
          />
        </label>
      </div>

      <label className="block">
        <span className={label}>Sources, one per line</span>
        <AutoText
          value={post.sources.join('\n')}
          onChange={(v) => onChange({ sources: v.split('\n') })}
        />
      </label>

      <label className="block">
        <span className={label}>Visual asset and Canva link</span>
        <AutoText value={post.visual_note} onChange={(v) => onChange({ visual_note: v })} />
      </label>

      {post.note && <p className="text-sm text-neutral-500">Planning note: {post.note}</p>}

      <div>
        {history === null ? (
          <button
            onClick={loadHistory}
            className="text-base font-semibold text-[#2f6b46] underline"
          >
            Show every saved version
          </button>
        ) : history.length === 0 ? (
          <p className="text-neutral-500">No edits yet.</p>
        ) : (
          <ul className="space-y-2">
            {history.map((v) => (
              <li key={v.id} className="flex items-center justify-between gap-3 text-base">
                <span>
                  <strong>{v.editor}</strong>, {ago(v.created_at)}
                  <span className="ml-2 text-neutral-500">
                    {(v.data.caption ?? '').slice(0, 50)}
                    {(v.data.caption ?? '').length > 50 ? '…' : ''}
                  </span>
                </span>
                <button
                  onClick={() => onChange(v.data)}
                  className="shrink-0 rounded border border-neutral-300 px-3 py-1 text-sm"
                >
                  Restore
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
