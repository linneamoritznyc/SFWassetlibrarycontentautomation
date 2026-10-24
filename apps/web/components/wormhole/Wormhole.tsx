'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { STATUSES, type WormholePost, type WormholeStatus } from '@/lib/wormhole-types';
import type { ScoutStory } from '@/lib/scout';
import { Editor } from './Editor';
import { News } from './News';
import { DateChip, GridTile, InstagramPost, LinkedInPost, PostBar } from './Posts';
import { Stories, isStory } from './Stories';
import { byDate, toDocHtml, weekLabel, weekOf } from './util';

type View = 'instagram' | 'grid' | 'stories' | 'linkedin' | 'news';
type SaveState = 'saving' | 'saved' | 'error';
type Patch = Partial<WormholePost>;

const POLL_MS = 3000;

/** A post none of whose slides has an image yet. */
const noVisual = (p: WormholePost) => !p.slides.some((s) => s.image);
const SAVE_DELAY = 800;

export function Wormhole({ editor, docUrl }: { editor: string; docUrl: string | null }) {
  const [posts, setPosts] = useState<WormholePost[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [loadError, setLoadError] = useState('');
  const [view, setView] = useState<View>('instagram');
  const [week, setWeek] = useState<string>('all');
  const [status, setStatus] = useState<'all' | WormholeStatus>('all');
  const [missingOnly, setMissingOnly] = useState(false);
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

  const weeks = useMemo(() => Array.from(new Set(posts.map((p) => weekOf(p)))).sort(), [posts]);

  const visible = useMemo(
    () =>
      posts.filter(
        (p) =>
          (week === 'all' || weekOf(p) === week) &&
          (status === 'all' || p.status === status) &&
          (!missingOnly || noVisual(p)),
      ),
    [posts, week, status, missingOnly],
  );
  const missingCount = useMemo(() => posts.filter(noVisual).length, [posts]);

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
    if (view === 'stories') {
      update(post.id, { platform: 'Instagram Stories', topic: 'New story' }, true);
    } else {
      setView('instagram');
    }
    setEditing(post.id);
    setTimeout(
      () => document.getElementById(`post-${post.id}`)?.scrollIntoView({ behavior: 'smooth' }),
      100,
    );
  }

  /** A Scout story becomes a draft post with no date, its link as the source. */
  async function planStory(s: ScoutStory) {
    const today = new Date().toISOString().slice(0, 10);
    const found = s.published ? s.published.slice(0, 10) : 'date unknown';
    const res = await fetch('/api/wormhole/posts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        iso_date: today,
        date_tbd: true,
        topic: `Soil news: ${s.title}`.slice(0, 200),
        platform: 'Instagram, Facebook, LinkedIn',
        sources: [s.url],
        caption: [
          '[Hook: the finding in one plain line.]',
          '[One concrete detail from the study itself: the organism, the place, the number.]',
          '[Why it matters for living soil.]',
          `Source: ${s.source}, ${found}.`,
          '#SoilFoodWeb #SoilBiology #SoilHealth',
        ].join('\n\n'),
        visual_note: [
          `Found by Scout on ${today} in ${s.feed} (${s.region}).`,
          'Read the study itself before writing; press releases overstate. Every number needs its source in the notes.',
          s.summary ? `From the feed: ${s.summary}` : '',
        ]
          .filter(Boolean)
          .join(' '),
      }),
    });
    if (!res.ok) throw new Error(`The server said ${res.status}`);
    const { post } = await res.json();
    setPosts((prev) => [...prev, post].sort(byDate));
    openPost(post.id, true);
  }

  function openPost(id: string, edit = false) {
    setWeek('all');
    setStatus('all');
    setMissingOnly(false);
    setView('instagram');
    if (edit) setEditing(id);
    setTimeout(
      () => document.getElementById(`post-${id}`)?.scrollIntoView({ behavior: 'smooth' }),
      150,
    );
  }

  function exportTitle() {
    if (week === 'all') return 'Wormhole, all planned posts';
    return week === 'tbd'
      ? 'Wormhole, posts without a date'
      : `Wormhole, week of ${weekLabel(week)}`;
  }

  function download() {
    const html = toDocHtml(visible, exportTitle());
    const url = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = `${exportTitle()
      .replace(/[^\w]+/g, '-')
      .toLowerCase()}.html`;
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

  const [expanded, setExpanded] = useState<string | null>(null);
  useEffect(() => {
    if (!expanded) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setExpanded(null);
    window.addEventListener('keydown', onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = prev;
    };
  }, [expanded]);

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
  // The Instagram feed and grid show only what goes to Instagram: a LinkedIn-only
  // post (a 1200 x 627 image) lives on the LinkedIn tab.
  const onInstagram = (p: WormholePost) => !p.platform.trim() || /instagram/i.test(p.platform);
  const feedPosts = visible.filter((p) => !isStory(p) && onInstagram(p));
  const storyPosts = visible.filter(isStory);
  const gridPosts = [
    ...feedPosts.filter((p) => p.pinned).sort((a, b) => (a.pinned ?? 0) - (b.pinned ?? 0)),
    ...feedPosts.filter((p) => !p.pinned).reverse(),
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
              <button
                onClick={newPost}
                className="rounded-lg border border-[#2f6b46] px-3 py-2 text-base font-semibold text-[#2f6b46]"
              >
                {view === 'stories' ? '+ New story' : '+ New post'}
              </button>
              <button
                onClick={copyForDoc}
                className="rounded-lg bg-[#2f6b46] px-3 py-2 text-base font-semibold text-white"
              >
                {copied ? 'Copied. Paste in the doc' : 'Copy for the doc'}
              </button>
              <button
                onClick={download}
                className="rounded-lg border border-neutral-300 px-3 py-2 text-base"
              >
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
          <nav className="mt-3 grid grid-cols-2 gap-1 sm:grid-cols-5 rounded-xl bg-neutral-100 p-1">
            {(
              [
                ['instagram', 'Instagram feed'],
                ['grid', 'Instagram grid'],
                ['stories', 'Instagram stories'],
                ['linkedin', 'LinkedIn'],
                ['news', 'Soil news'],
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
            {view !== 'news' && (
              <>
                <select
                  className={select}
                  value={week}
                  onChange={(e) => setWeek(e.target.value)}
                  aria-label="Week"
                >
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
                {(missingCount > 0 || missingOnly) && (
                  <button
                    onClick={() => setMissingOnly(!missingOnly)}
                    aria-pressed={missingOnly}
                    className={`rounded-lg px-3 py-2 text-base font-semibold ${
                      missingOnly
                        ? 'bg-[#B23A2E] text-white'
                        : 'border border-[#B23A2E] text-[#B23A2E]'
                    }`}
                  >
                    {missingOnly
                      ? 'Showing posts with no visual · show all'
                      : `${missingCount} post${missingCount === 1 ? '' : 's'} with no visual`}
                  </button>
                )}
              </>
            )}
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
        {view === 'news' && <News posts={posts} onPlan={planStory} onOpen={(id) => openPost(id)} />}

        {loaded && visible.length === 0 && view !== 'news' && (
          <p className="text-lg text-neutral-500">No posts match. Try “All weeks”.</p>
        )}

        {view === 'instagram' && (
          <div className="mx-auto max-w-[470px] space-y-8">
            {feedPosts.map((p, i, list) => card(p, InstagramPost, i, list))}
          </div>
        )}

        {view === 'linkedin' && (
          <div className="mx-auto max-w-[555px] space-y-8">
            {visible
              .filter((p) => /linkedin/i.test(p.platform))
              .map((p, i, list) => card(p, LinkedInPost, i, list))}
          </div>
        )}

        {view === 'stories' && (
          <Stories
            stories={storyPosts}
            controls={(p) => (
              <>
                <PostBar
                  post={p}
                  editing={editing === p.id}
                  saveState={saveState[p.id]}
                  onEdit={() => setEditing(editing === p.id ? null : p.id)}
                  onStatus={(s) => update(p.id, { status: s }, true)}
                />
                {editing === p.id && <Editor post={p} onChange={(patch) => update(p.id, patch)} />}
              </>
            )}
          />
        )}

        {view === 'grid' && (
          <div className="mx-auto max-w-[935px]">
            <p className="mb-3 text-base text-neutral-500">
              Newest first, the way the profile will look. Tap a post to open it.
            </p>
            <div className="grid grid-cols-3 gap-px border border-neutral-200 bg-neutral-200">
              {gridPosts.map((p) => (
                <GridTile key={p.id} post={p} onOpen={() => setExpanded(p.id)} />
              ))}
            </div>
          </div>
        )}
      </main>
      {expanded &&
        (() => {
          const p = visible.find((q) => q.id === expanded) ?? posts.find((q) => q.id === expanded);
          if (!p) return null;
          return (
            <div
              className="fixed inset-0 z-50 overflow-y-auto bg-black/60 px-3 py-6 sm:py-10"
              onClick={() => setExpanded(null)}
            >
              <div className="relative mx-auto max-w-[470px]" onClick={(e) => e.stopPropagation()}>
                <button
                  onClick={() => setExpanded(null)}
                  aria-label="Close"
                  className="absolute -top-1 right-0 z-10 -translate-y-full rounded-full bg-white/90 px-3 py-1 text-base font-semibold text-black shadow"
                >
                  Close
                </button>
                {card(p, InstagramPost, 0, [p])}
              </div>
            </div>
          );
        })()}
    </div>
  );
}
