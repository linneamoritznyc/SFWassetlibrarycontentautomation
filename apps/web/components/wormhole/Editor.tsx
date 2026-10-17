'use client';

import { useEffect, useRef, useState } from 'react';
import { STATUSES, type Slide, type WormholePost } from '@/lib/wormhole-types';
import { ago, imageUrl, uploadImage } from './util';

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

/** Everything about one post, edited in place under its preview. */
export function Editor({ post, onChange }: { post: WormholePost; onChange: (p: Patch) => void }) {
  const [uploading, setUploading] = useState<number | 'many' | null>(null);
  const [error, setError] = useState('');
  const [drag, setDrag] = useState<number | null>(null);
  const [history, setHistory] = useState<
    { id: number; data: Patch; editor: string; created_at: string }[] | null
  >(null);
  const slides = post.slides;

  function setSlides(next: Slide[]) {
    onChange({ slides: next });
  }

  async function putImage(i: number, file: File) {
    setError('');
    setUploading(i);
    try {
      const id = await uploadImage(file);
      const next = [...slides];
      while (next.length <= i) next.push({ text: '', image: null });
      next[i] = { ...next[i]!, image: id };
      setSlides(next);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setUploading(null);
    }
  }

  /** Several Canva pages at once: fill slides without images, then add more. */
  async function putMany(files: File[]) {
    setError('');
    setUploading('many');
    try {
      const next = [...slides];
      for (const file of files) {
        const id = await uploadImage(file);
        const free = next.findIndex((s) => !s.image);
        if (free >= 0) next[free] = { ...next[free]!, image: id };
        else next.push({ text: '', image: id });
      }
      setSlides(next);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setUploading(null);
    }
  }

  function move(from: number, to: number) {
    if (to < 0 || to >= slides.length || from === to) return;
    const next = [...slides];
    const [s] = next.splice(from, 1) as [Slide];
    next.splice(to, 0, s);
    setSlides(next);
  }

  async function loadHistory() {
    const res = await fetch(`/api/wormhole/posts/${post.id}/versions`);
    if (res.ok) setHistory((await res.json()).versions);
  }

  function images(e: React.DragEvent): File[] {
    return Array.from(e.dataTransfer.files).filter((f) => f.type.startsWith('image/'));
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
            onChange={(e) => e.target.value && onChange({ iso_date: e.target.value })}
          />
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

      <label className="block">
        <span className={label}>Caption</span>
        <AutoText
          rows={6}
          value={post.caption}
          onChange={(v) => onChange({ caption: v })}
          placeholder="Paste or write the caption"
        />
        <span className="mt-1 block text-sm text-neutral-500">
          {post.caption.length} characters
          {post.caption.length > 2200 ? ' (Instagram stops at 2,200)' : ''}
        </span>
      </label>

      <div>
        <span className={label}>Slides</span>
        <div
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            const files = images(e);
            if (files.length) putMany(files);
          }}
          className="mt-1 rounded-lg border-2 border-dashed border-neutral-300 bg-white px-4 py-4 text-center text-base text-neutral-600"
        >
          {uploading === 'many' ? (
            'Uploading…'
          ) : (
            <>
              Drop all the Canva pages here at once, or{' '}
              <label className="cursor-pointer font-semibold text-[#2f6b46] underline">
                choose files
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  className="hidden"
                  onChange={(e) => {
                    const files = Array.from(e.target.files ?? []);
                    e.target.value = '';
                    if (files.length) putMany(files);
                  }}
                />
              </label>
            </>
          )}
        </div>

        <ol className="mt-3 space-y-3">
          {slides.map((s, i) => (
            <li
              key={i}
              draggable
              onDragStart={(e) => {
                setDrag(i);
                e.dataTransfer.effectAllowed = 'move';
              }}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                const files = images(e);
                if (files[0]) putImage(i, files[0]);
                else if (drag !== null) move(drag, i);
                setDrag(null);
              }}
              onDragEnd={() => setDrag(null)}
              className={`flex gap-3 rounded-lg border bg-white p-3 ${drag === i ? 'border-[#2f6b46] opacity-60' : 'border-neutral-200'}`}
            >
              <div className="flex flex-col items-center gap-1">
                <span className="cursor-grab select-none text-lg text-neutral-400" title="Drag to reorder">
                  ⋮⋮
                </span>
                <span className="text-sm font-semibold text-neutral-600">{i + 1}</span>
                <button
                  aria-label="Move up"
                  onClick={() => move(i, i - 1)}
                  className="text-neutral-500 disabled:opacity-30"
                  disabled={i === 0}
                >
                  ▲
                </button>
                <button
                  aria-label="Move down"
                  onClick={() => move(i, i + 1)}
                  className="text-neutral-500 disabled:opacity-30"
                  disabled={i === slides.length - 1}
                >
                  ▼
                </button>
              </div>
              <label className="relative block aspect-[4/5] w-20 shrink-0 cursor-pointer overflow-hidden rounded border border-neutral-200 bg-neutral-50 sm:w-24">
                {s.image ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={imageUrl(s.image)} alt="" className="h-full w-full object-cover" />
                ) : (
                  <span className="flex h-full items-center justify-center p-1 text-center text-xs text-neutral-500">
                    {uploading === i ? 'Uploading…' : 'Drop or tap for image'}
                  </span>
                )}
                <input
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    e.target.value = '';
                    if (f) putImage(i, f);
                  }}
                />
              </label>
              <div className="min-w-0 flex-1">
                <AutoText
                  value={s.text}
                  placeholder="Text on this slide"
                  onChange={(v) => {
                    const next = [...slides];
                    next[i] = { ...next[i]!, text: v };
                    setSlides(next);
                  }}
                />
                <div className="mt-1 flex gap-4 text-sm">
                  {s.image && (
                    <button
                      className="text-neutral-600 underline"
                      onClick={() => {
                        const next = [...slides];
                        next[i] = { ...next[i]!, image: null };
                        setSlides(next);
                      }}
                    >
                      Remove image
                    </button>
                  )}
                  <button
                    className="text-neutral-600 underline"
                    onClick={() => setSlides(slides.filter((_, j) => j !== i))}
                  >
                    Delete slide
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ol>
        <button
          onClick={() => setSlides([...slides, { text: '', image: null }])}
          className="mt-3 rounded-lg border border-[#2f6b46] px-4 py-2 font-semibold text-[#2f6b46]"
        >
          + Add slide
        </button>
        {error && <p className="mt-2 font-medium text-red-700">{error}</p>}
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className={label}>CTA</span>
          <input className={field} value={post.cta} onChange={(e) => onChange({ cta: e.target.value })} />
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
          <button onClick={loadHistory} className="text-base font-semibold text-[#2f6b46] underline">
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
