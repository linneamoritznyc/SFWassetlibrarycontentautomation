'use client';

import { useEffect, useRef, type ReactNode } from 'react';
import { STATUSES, type WormholePost } from '@/lib/wormhole-types';
import { Caption } from './Caption';
import { Carousel } from './Carousel';
import { SlideView } from './SlideView';
import { STATUS_STYLE, ago, dayLabel, postDay, slidesOf } from './util';

const Icon = ({ d }: { d: string }) => (
  <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path d={d} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);
const HEART =
  'M12 20.5s-7.5-4.6-9.2-9.4C1.6 7.6 3.9 4.5 7.2 4.5c2 0 3.6 1.2 4.8 2.9 1.2-1.7 2.8-2.9 4.8-2.9 3.3 0 5.6 3.1 4.4 6.6-1.7 4.8-9.2 9.4-9.2 9.4z';
const COMMENT = 'M20.5 12a8.5 8.5 0 1 1-3.4-6.8A8.4 8.4 0 0 1 20.5 12zm0 0 1 8.5-6-2.5';
const SHARE = 'M22 3 9.5 13M22 3l-7 18-4-8-8-4 19-6z';
const SAVE = 'M19 21l-7-5-7 5V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1z';

function Avatar({ size = 32 }: { size?: number }) {
  return (
    <span
      className="flex shrink-0 items-center justify-center overflow-hidden rounded-full border border-neutral-200 bg-white"
      style={{ width: size, height: size }}
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src="/wormhole/sfw-foundation-wordmark-240.png" alt="" className="h-[80%] w-[80%] object-contain" />
    </span>
  );
}

/** Status chips, the Edit button and who touched the post last. */
export function PostBar({
  post,
  editing,
  saveState,
  onEdit,
  onStatus,
}: {
  post: WormholePost;
  editing: boolean;
  saveState?: 'saving' | 'saved' | 'error';
  onEdit: () => void;
  onStatus: (s: WormholePost['status']) => void;
}) {
  return (
    <div className="space-y-3 border-t border-neutral-200 px-4 py-3">
      <div className="flex flex-wrap gap-2">
        {STATUSES.map((s) => (
          <button
            key={s.value}
            onClick={() => onStatus(s.value)}
            className={`rounded-full border px-3 py-1 text-sm font-medium ${
              post.status === s.value ? STATUS_STYLE[s.value] : 'border-neutral-200 text-neutral-400'
            }`}
          >
            {s.label}
          </button>
        ))}
      </div>
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm text-neutral-500">
          {saveState === 'saving'
            ? 'Saving…'
            : saveState === 'error'
              ? 'Not saved. Check your connection.'
              : saveState === 'saved'
                ? 'Saved'
                : post.updated_by !== 'seed'
                  ? `Edited by ${post.updated_by}, ${ago(post.updated_at)}`
                  : ''}
        </span>
        <button
          onClick={onEdit}
          className={`rounded-lg px-5 py-2 text-base font-semibold ${
            editing ? 'bg-neutral-200 text-black' : 'bg-[#2f6b46] text-white'
          }`}
        >
          {editing ? 'Done' : 'Edit'}
        </button>
      </div>
    </div>
  );
}

export function DateChip({ iso, tbd, count }: { iso: string; tbd?: boolean; count?: number }) {
  return (
    <div className="mb-2 flex items-center gap-2">
      <span className="rounded-full bg-[#2f6b46] px-3 py-1 text-sm font-semibold text-white">
        {tbd ? 'Date TBD' : dayLabel(iso, 'short')}
      </span>
      {count !== undefined && count > 1 && (
        <span className="text-sm text-neutral-500">{count} posts this day</span>
      )}
    </div>
  );
}

/** The caption as a box you type in, sized to its text, styled like the caption. */
function CaptionBox({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  const ref = useRef<HTMLTextAreaElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = `${el.scrollHeight + 2}px`;
  }, [value]);
  return (
    <>
      <textarea
        ref={ref}
        autoFocus
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Write the caption"
        className="block w-full resize-none rounded-md border border-[#2f6b46]/40 bg-[#f6faf7] p-2 leading-snug outline-none focus:border-[#2f6b46]"
      />
      <span className="mt-1 block text-xs text-neutral-500">
        {value.length} characters{value.length > 2200 ? ' (Instagram stops at 2,200)' : ''}
      </span>
    </>
  );
}

export type CaptionEdit = { editing: boolean; onChange: (v: string) => void; onStart: () => void };

function EditableCaption({ edit, children }: { edit?: CaptionEdit; children: ReactNode }) {
  if (!edit) return <>{children}</>;
  return (
    <div onClick={edit.editing ? undefined : edit.onStart} className={edit.editing ? '' : 'cursor-text'} title={edit.editing ? undefined : 'Click to edit the caption'}>
      {children}
    </div>
  );
}

export function InstagramPost({ post, children, caption }: { post: WormholePost; children?: ReactNode; caption?: CaptionEdit }) {
  return (
    <article className="overflow-hidden rounded-xl border border-neutral-200 bg-white text-[15px] text-black">
      <header className="flex items-center gap-3 px-3 py-2.5">
        <Avatar />
        <div className="min-w-0 flex-1 leading-tight">
          <p className="font-semibold">soilfoodwebschool</p>
          <p className="truncate text-xs text-neutral-500">{post.topic}</p>
        </div>
        <span className="text-xl leading-none text-neutral-600">···</span>
      </header>
      <Carousel slides={slidesOf(post)} fallback={post.topic} />
      <div className="flex items-center gap-4 px-3 pt-2">
        <Icon d={HEART} />
        <Icon d={COMMENT} />
        <Icon d={SHARE} />
        <span className="ml-auto">
          <Icon d={SAVE} />
        </span>
      </div>
      <div className="px-3 pb-3 pt-2">
        <EditableCaption edit={caption}>
          {caption?.editing ? (
            <CaptionBox value={post.caption} onChange={caption.onChange} />
          ) : (
            <Caption
              text={post.caption}
              prefix="soilfoodwebschool"
              limit={125}
              moreLabel="more"
              color="#00376b"
            />
          )}
        </EditableCaption>
      </div>
      {children}
    </article>
  );
}

export function LinkedInPost({ post, children, caption }: { post: WormholePost; children?: ReactNode; caption?: CaptionEdit }) {
  const slides = slidesOf(post);
  return (
    <article className="overflow-hidden rounded-lg border border-neutral-300 bg-white text-[15px] text-[#191919]">
      <header className="flex items-start gap-3 px-4 pt-3">
        <Avatar size={48} />
        <div className="leading-tight">
          <p className="font-semibold">Soil Food Web Foundation</p>
          <p className="text-xs text-neutral-500">Nonprofit Organization</p>
          <p className="text-xs text-neutral-500">{postDay(post, 'short')} · 🌐</p>
        </div>
        <span className="ml-auto text-xl leading-none text-neutral-600">···</span>
      </header>
      <div className="px-4 py-3">
        <EditableCaption edit={caption}>
          {caption?.editing ? (
            <CaptionBox value={post.caption} onChange={caption.onChange} />
          ) : (
            <Caption text={post.caption} limit={210} moreLabel="…see more" color="#0a66c2" />
          )}
        </EditableCaption>
      </div>
      {slides.length > 1 ? (
        <div className="border-y border-neutral-200">
          <Carousel slides={slides} fallback={post.topic} counter />
        </div>
      ) : (
        <div className="relative aspect-[4/5] w-full border-y border-neutral-200">
          <SlideView slide={slides[0]!} fallback={post.topic} />
        </div>
      )}
      <div className="grid grid-cols-4 px-2 py-1 text-sm font-semibold text-neutral-600">
        {['Like', 'Comment', 'Repost', 'Send'].map((a) => (
          <span key={a} className="py-2 text-center">
            {a}
          </span>
        ))}
      </div>
      {children}
    </article>
  );
}

export function GridTile({ post, onOpen }: { post: WormholePost; onOpen: () => void }) {
  const slides = slidesOf(post);
  return (
    <button onClick={onOpen} className="relative block aspect-[4/5] w-full overflow-hidden bg-white text-left" title={post.topic}>
      <SlideView slide={slides[0]!} fallback={post.topic} />
      {slides.length > 1 && (
        <svg viewBox="0 0 24 24" className="absolute right-1.5 top-1.5 h-5 w-5 drop-shadow" fill="white">
          <path d="M8 3h11a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zM3 8v11a2 2 0 0 0 2 2h11" stroke="#555" strokeWidth="1" />
        </svg>
      )}
      <span className="absolute bottom-1 left-1 rounded bg-black/60 px-1.5 py-0.5 text-[11px] text-white">
        {postDay(post, 'short')}
      </span>
    </button>
  );
}
