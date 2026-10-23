'use client';

import { useCallback, useEffect, useState, type ReactNode } from 'react';
import type { WormholePost } from '@/lib/wormhole-types';
import { STATUSES } from '@/lib/wormhole-types';
import { DateChip } from './Posts';
import { STATUS_STYLE, dayLabel, imageUrl, slidesOf } from './util';

const FRAME_MS = 6000;

/** Instagram Stories live in their own tab, never in the feed or the grid. */
export function isStory(p: WormholePost): boolean {
  return /stor(y|ies)/i.test(p.platform) || /\bstory\b/i.test(p.topic);
}

function Avatar({ size = 32 }: { size?: number }) {
  return (
    <span
      className="flex shrink-0 items-center justify-center overflow-hidden rounded-full bg-white"
      style={{ width: size, height: size }}
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src="/wormhole/sfw-foundation-wordmark-240.png"
        alt=""
        className="h-[80%] w-[80%] object-contain"
      />
    </span>
  );
}

/** One frame inside the 9:16 phone screen. 4:5 images sit on a blurred copy of themselves. */
function Frame({ image, text }: { image: string | null; text: string }) {
  if (!image) {
    return (
      <div
        className="absolute inset-0 flex items-center bg-[#22371F] p-[8%]"
        style={{ containerType: 'inline-size' }}
      >
        <p
          className="whitespace-pre-line font-semibold leading-snug text-[#F4F1EA]"
          style={{ fontSize: '7cqw' }}
        >
          {text || 'No image yet'}
        </p>
      </div>
    );
  }
  return (
    <>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={imageUrl(image)}
        alt=""
        className="absolute inset-0 h-full w-full scale-110 object-cover blur-2xl brightness-75"
      />
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={imageUrl(image)}
        alt=""
        draggable={false}
        className="absolute inset-0 h-full w-full object-contain"
      />
    </>
  );
}

/** Full-screen story player: tap the right side for the next frame, the left for the previous one. */
function Viewer({
  stories,
  start,
  onClose,
  onSeen,
}: {
  stories: WormholePost[];
  start: { story: number; frame: number };
  onClose: () => void;
  onSeen: (id: string) => void;
}) {
  const [pos, setPos] = useState(start);
  const [paused, setPaused] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const story = stories[pos.story];
  const frames = story ? slidesOf(story) : [];

  const next = useCallback(() => {
    setElapsed(0);
    const n = slidesOf(stories[pos.story]!).length;
    if (pos.frame + 1 < n) setPos({ ...pos, frame: pos.frame + 1 });
    else if (pos.story + 1 < stories.length) setPos({ story: pos.story + 1, frame: 0 });
    else onClose();
  }, [pos, stories, onClose]);

  const prev = useCallback(() => {
    setElapsed(0);
    if (pos.frame > 0) setPos({ ...pos, frame: pos.frame - 1 });
    else if (pos.story > 0)
      setPos({ story: pos.story - 1, frame: slidesOf(stories[pos.story - 1]!).length - 1 });
  }, [pos, stories]);

  useEffect(() => {
    if (story) onSeen(story.id);
  }, [story, onSeen]);

  // Advance on a timer, like Instagram. Holding the screen pauses it.
  useEffect(() => {
    if (paused) return;
    let raf = 0;
    let last = performance.now();
    const tick = (t: number) => {
      setElapsed((e) => e + (t - last));
      last = t;
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [paused]);
  useEffect(() => {
    if (elapsed >= FRAME_MS) next();
  }, [elapsed, next]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
      if (e.key === 'ArrowRight') next();
      if (e.key === 'ArrowLeft') prev();
      if (e.key === ' ') setPaused((v) => !v);
    };
    window.addEventListener('keydown', onKey);
    const overflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = overflow;
    };
  }, [next, prev, onClose]);

  if (!story) return null;
  const frame = frames[pos.frame]!;

  return (
    <div
      className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-neutral-950/95 p-3"
      onClick={onClose}
    >
      <div
        className="relative aspect-[9/16] h-[min(86vh,calc((100vw-24px)*16/9))] overflow-hidden rounded-xl bg-black select-none"
        onClick={(e) => e.stopPropagation()}
        onPointerDown={() => setPaused(true)}
        onPointerUp={() => setPaused(false)}
        onPointerLeave={() => setPaused(false)}
      >
        <Frame image={frame.image} text={frame.text} />
        <div className="absolute inset-x-0 top-0 bg-gradient-to-b from-black/60 to-transparent px-3 pb-8 pt-3">
          <div className="flex gap-1">
            {frames.map((_, i) => (
              <span key={i} className="h-[3px] flex-1 overflow-hidden rounded-full bg-white/35">
                <span
                  className="block h-full bg-white"
                  style={{
                    width:
                      i < pos.frame
                        ? '100%'
                        : i === pos.frame
                          ? `${(elapsed / FRAME_MS) * 100}%`
                          : '0%',
                  }}
                />
              </span>
            ))}
          </div>
          <div className="mt-3 flex items-center gap-2 text-white">
            <Avatar size={30} />
            <span className="text-sm font-semibold">soilfoodwebschool</span>
            <span className="text-sm text-white/70">
              {story.date_tbd ? 'Date TBD' : dayLabel(story.iso_date, 'short')}
            </span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onClose();
              }}
              aria-label="Close"
              className="ml-auto px-2 text-2xl leading-none"
            >
              ×
            </button>
          </div>
        </div>
        <button
          aria-label="Previous frame"
          className="absolute bottom-0 left-0 top-16 w-1/3"
          onClick={prev}
        />
        <button
          aria-label="Next frame"
          className="absolute bottom-0 right-0 top-16 w-2/3"
          onClick={next}
        />
        {paused && (
          <span className="pointer-events-none absolute bottom-4 left-1/2 -translate-x-1/2 rounded-full bg-black/50 px-3 py-1 text-xs text-white">
            Paused
          </span>
        )}
      </div>
      <div
        className="mt-3 w-full max-w-[420px] text-center text-sm text-white/80"
        onClick={(e) => e.stopPropagation()}
      >
        <p className="font-semibold text-white">{story.topic}</p>
        <p>
          Frame {pos.frame + 1} of {frames.length} · story {pos.story + 1} of {stories.length}
        </p>
        {frame.text && <p className="mt-1 whitespace-pre-line text-white/70">{frame.text}</p>}
      </div>
    </div>
  );
}

/** The Stories tab: a row of story circles to click through, then each story with its frames. */
export function Stories({
  stories,
  controls,
}: {
  stories: WormholePost[];
  controls: (p: WormholePost) => ReactNode;
}) {
  const [open, setOpen] = useState<{ story: number; frame: number } | null>(null);
  const [seen, setSeen] = useState<Set<string>>(new Set());
  const markSeen = useCallback(
    (id: string) => setSeen((s) => (s.has(id) ? s : new Set(s).add(id))),
    [],
  );
  const close = useCallback(() => setOpen(null), []);

  if (stories.length === 0) {
    return <p className="text-lg text-neutral-500">No stories match. Try “All weeks”.</p>;
  }

  return (
    <div className="mx-auto max-w-[760px]">
      <p className="mb-3 text-base text-neutral-500">
        Tap a circle to watch the stories in order. Tap the right side for the next frame, the left
        side to go back, hold to pause.
      </p>
      <div className="-mx-4 flex gap-4 overflow-x-auto px-4 pb-4">
        {stories.map((p, i) => {
          const cover = slidesOf(p)[0]!;
          return (
            <button
              key={p.id}
              onClick={() => setOpen({ story: i, frame: 0 })}
              className="flex w-20 shrink-0 flex-col items-center gap-1"
            >
              <span
                className={`rounded-full p-[3px] ${
                  seen.has(p.id)
                    ? 'bg-neutral-300'
                    : 'bg-gradient-to-tr from-[#C89B7B] via-[#59A66C] to-[#22371F]'
                }`}
              >
                <span className="block h-[70px] w-[70px] overflow-hidden rounded-full border-2 border-white bg-[#22371F]">
                  {cover.image && (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={imageUrl(cover.image)}
                      alt=""
                      className="h-full w-full object-cover"
                    />
                  )}
                </span>
              </span>
              <span className="text-xs font-semibold text-neutral-700">
                {p.date_tbd ? 'TBD' : dayLabel(p.iso_date, 'short')}
              </span>
            </button>
          );
        })}
      </div>

      <div className="mt-4 space-y-8">
        {stories.map((p, i) => (
          <section
            key={p.id}
            id={`post-${p.id}`}
            className="scroll-mt-40 overflow-hidden rounded-xl border border-neutral-200"
          >
            <div className="px-4 pt-4">
              <DateChip iso={p.iso_date} tbd={p.date_tbd} />
              <div className="flex flex-wrap items-center gap-2">
                <h2 className="text-lg font-semibold">{p.topic}</h2>
                <span
                  className={`rounded-full border px-2 py-0.5 text-xs font-medium ${STATUS_STYLE[p.status]}`}
                >
                  {STATUSES.find((s) => s.value === p.status)?.label}
                </span>
              </div>
              <div className="mt-3 flex gap-2 overflow-x-auto pb-3">
                {slidesOf(p).map((f, j) => (
                  <button
                    key={j}
                    onClick={() => setOpen({ story: i, frame: j })}
                    className="relative aspect-[9/16] w-28 shrink-0 overflow-hidden rounded-lg bg-black"
                    aria-label={`Play frame ${j + 1}`}
                  >
                    <Frame image={f.image} text={f.text} />
                    <span className="absolute left-1.5 top-1.5 rounded bg-black/55 px-1.5 text-xs font-semibold text-white">
                      {j + 1}
                    </span>
                  </button>
                ))}
              </div>
            </div>
            {controls(p)}
          </section>
        ))}
      </div>

      {open && <Viewer stories={stories} start={open} onClose={close} onSeen={markSeen} />}
    </div>
  );
}
