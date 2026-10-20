'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { STATUSES, type WormholePost, type WormholeStatus } from '@/lib/wormhole-types';
import { Editor } from './Editor';
import { DateChip, GridTile, InstagramPost, LinkedInPost, PostBar } from './Posts';
import { byDate, toDocHtml, weekLabel, weekOf } from './util';

type View = 'instagram' | 'grid' | 'linkedin';
type SaveState = 'saving' | 'saved' | 'error';
type Patch = Partial<WormholePost>;

const POLL_MS = 3000;
const SAVE_DELAY = 800;

export function Wormhole({ editor, docUrl }: { editor: string; docUrl: string | null }) {
  const [posts, setPosts] = useState<WormholePost[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [loadError, setLoadError] = useState('');
  const [view, setView] = useState<View>('instagram');
  const [week, setWeek] = useState<string>('all');
  const [status, setStatus] = useState<'all' | WormholeStatus>('all');
  const [editing, setEditing] = useState<string | null>(null);
  const [saveState, setSaveState] = useState<Record<string, SaveState>>({});
  const [big, setBig] = useState(false);
  const [copied, setCopied] = useState(false);

  const since = useRef<string | null>(null);
  const pending = useRef<Record<string, Patch>>({});
  const timers = useRef<Record<string, ReturnType<typeof setTimeout>>>({});
  const inFlight = useRef<Record<string, number>>({});

  // Larger text for everything on the page, remembered on this device.
  useEffect(() => {
    try {
      setBig(localStorage.getItem('wormhole-big') === '1');
    } catch {}
  }, []);
  useEffect(() => {
    document.documentElement.style.fontSize = big ? '20px' : '17px';
    try {
      localStorage.setItem('wormhole-big', big ? '1' : '0');
    } catch {}
    return () => {
      document.documentElement.style.fontSize = '';
    };
  }, [big]);

  const merge = useCallback((incoming: WormholePost[]) => {
    setPosts((prev) => {
      const map = new Map(prev.map((p) => [p.id, p]));
      for (const p of incoming) {
        // Never overwrite what someone is typing right now on this screen.
        if (pending.current[p.id] || inFlight.current[p.id]) continue;
        map.set(p.id, p);
      }
      return Array.from(map.values()).sort(byDate);
    });
  }, []);

  // Load, then pick up everyone else's changes every few seconds.
  useEffect(() => {
    let stop = false;
    async function tick() {
      try {
        const q = since.current ? `?since=${encodeURIComponent(since.current)}` : '';
        const res = await fetch(`/api/wormhole/posts${q}`, { cache: 'no-store' });
        if (res.status === 401) {
          window.location.href = '/wormhole/login';
          return;
        }
        if (!res.ok) throw new Error(`The server said ${res.status}`);
        const body = await res.json();
        since.current = body.now;
        merge(body.posts);
        setLoaded(true);
        setLoadError('');
      } catch (e) {
        setLoadError((e as Error).message);
      }
      if (!stop) setTimeout(tick, POLL_MS);
    }
    tick();
    return () => {
      stop = true;
    };
  }, [merge]);

  const flush = useCallback(async (id: string) => {
    const patch = pending.current[id];
    if (!patch) return;
    delete pending.current[id];
    inFlight.current[id] = (inFlight.current[id] ?? 0) + 1;
    setSaveState((s) => ({ ...s, [id]: 'saving' }));
    try {
      const res = await fetch(`/api/wormhole/posts/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patch),
      });
      if (!res.ok) throw new Error();
      const { post } = await res.json();
      inFlight.current[id] -= 1;
      if (!pending.current[id] && inFlight.current[id] === 0) {
        setPosts((prev) => prev.map((p) => (p.id === id ? post : p)));
        setSaveState((s) => ({ ...s, [id]: 'saved' }));
      }
    } catch {
      inFlight.current[id] -= 1;
      // Keep the unsaved change and try again shortly.
      pending.current[id] = { ...patch, ...pending.current[id] };
      setSaveState((s) => ({ ...s, [id]: 'error' }));
      clearTimeout(timers.current[id]);
      timers.current[id] = setTimeout(() => flush(id), 4000);
    }
  }, []);

  const update = useCallback(
    (id: string, patch: Patch, now = false) => {
      setPosts((prev) => prev.map((p) => (p.id === id ? { ...p, ...patch } : p)));
      pending.current[id] = { ...pending.current[id], ...patch };
      setSaveState((s) => ({ ...s, [id]: 'saving' }));
      clearTimeout(timers.current[id]);
      timers.current[id] = setTimeout(() => flush(id), now ? 0 : SAVE_DELAY);
    },
    [flush],
  );

  // Do not lose a last keystroke when the tab closes.
  useEffect(() => {
    const warn = (e: BeforeUnloadEvent) => {
      if (Object.keys(pending.current).length) e.preventDefault();
    };
    window.addEventListener('beforeunload', warn);
    return () => window.removeEventListener('beforeunload', warn);
  }, []);

  const weeks = useMemo(
    () => Array.from(new Set(posts.map((p) => weekOf(p)))).sort(),
    [posts],
  );

  const visible = useMemo(
    () =>
      posts.filter(
        (p) =>
          (week === 'all' || weekOf(p) === week) &&
          (status === 'all' || p.status === status),
      ),
    [posts, week, status],
  );

  async function newPost() {
    const iso = week !== 'all' && week !== 'tbd' ? week : new Date().toISOString().slice(0, 10);
    const res = await fetch('/api/wormhole/posts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ iso_date: iso, topic: 'New post' }),
    });
    if (!res.ok) return;
    const { post } = await res.json();
    setPosts((prev) => [...prev, post].sort(byDate));
    setStatus('all');
    setView('instagram');
    setEditing(post.id);
    setTimeout(() => document.getElementById(`post-${post.id}`)?.scrollIntoView({ behavior: 'smooth' }), 100);
  }

  function exportTitle() {
    if (week === 'all') return 'Wormhole, all planned posts';
    return week === 'tbd' ? 'Wormhole, posts without a date' : `Wormhole, week of ${weekLabel(week)}`;
  }

  function download() {
    const html = toDocHtml(visible, exportTitle());
    const url = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = `${exportTitle().replace(/[^\w]+/g, '-').toLowerCase()}.html`;
    a.click();
    URL.revokeObjectURL(url);
  }

  async function copyForDoc() {
    const html = toDocHtml(visible, exportTitle());
    try {
      await navigator.clipboard.write([
        new ClipboardItem({
          'text/html': new Blob([html], { type: 'text/html' }),
          'text/plain': new Blob([html.replace(/<[^>]+>/g, '\n')], { type: 'text/plain' }),
        }),
      ]);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch {
      download();
    }
  }

  function openInFeed(id: string) {
    setView('instagram');
    setTimeout(() => document.getElementById(`post-${id}`)?.scrollIntoView({ behavior: 'smooth' }), 80);
  }

  async function signOut() {
    await fetch('/api/wormhole/logout', { method: 'POST' });
    window.location.href = '/wormhole/login';
  }

  const select =
    'rounded-lg border border-neutral-300 bg-white px-3 py-2 text-base text-black outline-none focus:border-[#2f6b46]';

  function card(p: WormholePost, Kind: typeof InstagramPost, i: number, list: WormholePost[]) {
    const day = (q: WormholePost) => (q.date_tbd ? 'tbd' : q.iso_date);
    const firstOfDay = i === 0 || day(list[i - 1]!) !== day(p);
    const sameDay = list.filter((q) => day(q) === day(p)).length;
    const isEditing = editing === p.id;
    return (
      <section key={p.id} id={`post-${p.id}`} className="scroll-mt-40">
        {firstOfDay && <DateChip iso={p.iso_date} tbd={p.date_tbd} count={sameDay} />}
        <Kind
          post={p}
          caption={{
            editing: isEditing,
            onChange: (v) => update(p.id, { caption: v }),
            onStart: () => setEditing(p.id),
          }}
        >
          <PostBar
            post={p}
            editing={isEditing}
            saveState={saveState[p.id]}
            onEdit={() => setEditing(isEditing ? null : p.id)}
            onStatus={(s) => update(p.id, { status: s }, true)}
          />
          {isEditing && <Editor post={p} onChange={(patch) => update(p.id, patch)} />}
        </Kind>
      </section>
    );
  }

  // Instagram shows pinned posts first, then newest first.
  const gridPosts = [
    ...visible.filter((p) => p.pinned).sort((a, b) => (a.pinned ?? 0) - (b.pinned ?? 0)),
    ...visible.filter((p) => !p.pinned).reverse(),
  ];

  return (
    <div className="min-h-screen bg-white text-black">
      <header className="z-20 sm:sticky sm:top-0 border-b border-neutral-200 bg-white/95 backdrop-blur">
        <div className="mx-auto max-w-5xl px-4 py-3">
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.3em] text-[#2f6b46]">
                Soil Food Web
              </p>
              <h1 className="text-2xl font-bold leading-tight">Wormhole</h1>
            </div>
            <div className="ml-auto flex flex-wrap items-center gap-2">
              <button
                onClick={() => setBig(!big)}
                className="rounded-lg border border-neutral-300 px-3 py-2 text-base font-semibold"
                aria-pressed={big}
              >
                {big ? 'A−' : 'A+'}
              </button>
              <button onClick={newPost} className="rounded-lg border border-[#2f6b46] px-3 py-2 text-base font-semibold text-[#2f6b46]">
                + New post
              </button>
              <button onClick={copyForDoc} className="rounded-lg bg-[#2f6b46] px-3 py-2 text-base font-semibold text-white">
                {copied ? 'Copied. Paste in the doc' : 'Copy for the doc'}
              </button>
              <button onClick={download} className="rounded-lg border border-neutral-300 px-3 py-2 text-base">
                Download
              </button>
              {docUrl && (
                <a
                  href={docUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="rounded-lg border border-neutral-300 px-3 py-2 text-base underline"
                >
                  Open the Google Doc
                </a>
              )}
            </div>
          </div>
          <nav className="mt-3 grid grid-cols-3 gap-1 rounded-xl bg-neutral-100 p-1">
            {(
              [
                ['instagram', 'Instagram feed'],
                ['grid', 'Instagram grid'],
                ['linkedin', 'LinkedIn'],
              ] as const
            ).map(([v, label]) => (
              <button
                key={v}
                onClick={() => setView(v)}
                className={`rounded-lg px-2 py-2.5 text-base font-semibold ${
                  view === v ? 'bg-white text-black shadow' : 'text-neutral-600'
                }`}
              >
                {label}
              </button>
            ))}
          </nav>
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <select className={select} value={week} onChange={(e) => setWeek(e.target.value)} aria-label="Week">
              <option value="all">All weeks</option>
              {weeks.map((w) => (
                <option key={w} value={w}>
                  {w === 'tbd' ? 'Date TBD' : `Week of ${weekLabel(w)}`}
                </option>
              ))}
            </select>
            <select
              className={select}
              value={status}
              onChange={(e) => setStatus(e.target.value as typeof status)}
              aria-label="Status"
            >
              <option value="all">Every status</option>
              {STATUSES.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
            <span className="text-base text-neutral-500">
              {visible.length} post{visible.length === 1 ? '' : 's'}
            </span>
            <span className="ml-auto text-sm text-neutral-500">
              Editing as <strong className="text-black">{editor}</strong> ·{' '}
              <button onClick={signOut} className="underline">
                sign out
              </button>
            </span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 py-6">
        {loadError && (
          <p className="mb-4 rounded-lg bg-red-50 px-4 py-3 text-base text-red-800">
            Can’t reach the posts right now ({loadError}). Your edits are kept and will save when
            the connection is back.
          </p>
        )}
        {!loaded && !loadError && <p className="text-lg text-neutral-500">Opening the wormhole…</p>}
        {loaded && visible.length === 0 && (
          <p className="text-lg text-neutral-500">No posts match. Try “All weeks”.</p>
        )}

        {view === 'instagram' && (
          <div className="mx-auto max-w-[470px] space-y-8">
            {visible.map((p, i, list) => card(p, InstagramPost, i, list))}
          </div>
        )}

        {view === 'linkedin' && (
          <div className="mx-auto max-w-[555px] space-y-8">
            {visible
              .filter((p) => /linkedin/i.test(p.platform))
              .map((p, i, list) => card(p, LinkedInPost, i, list))}
          </div>
        )}

        {view === 'grid' && (
          <div className="mx-auto max-w-[935px]">
            <p className="mb-3 text-base text-neutral-500">
              Newest first, the way the profile will look. Tap a post to open it in the feed.
            </p>
            <div className="grid grid-cols-3 gap-px border border-neutral-200 bg-neutral-200">
              {gridPosts.map((p) => (
                <GridTile key={p.id} post={p} onOpen={() => openInFeed(p.id)} />
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
