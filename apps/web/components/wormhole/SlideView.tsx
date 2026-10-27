'use client';

import type { Slide } from '@/lib/wormhole-types';
import { imageUrl } from './util';

/**
 * One 4:5 slide. An uploaded image wins. Without one, the slide text is set
 * on cream in the brand fonts and marked "No visual yet", so a missing visual
 * is easy to spot and never mistaken for a finished tile.
 */
export function SlideView({ slide, fallback }: { slide: Slide; fallback: string }) {
  if (slide.image && /\.(mp4|webm|mov)$/i.test(slide.image)) {
    // Reels: a video file in public/wormhole/reels plays muted on loop, with controls for sound.
    return (
      <video
        src={slide.image}
        muted
        loop
        playsInline
        autoPlay
        controls
        preload="metadata"
        className="absolute inset-0 h-full w-full bg-black object-cover"
      />
    );
  }
  if (slide.image) {
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={imageUrl(slide.image)}
        alt=""
        draggable={false}
        className="absolute inset-0 h-full w-full object-cover"
      />
    );
  }

  const raw = slide.text.trim();
  const empty = raw === '';
  const [headline, small] = splitSmall(empty ? fallback : raw);
  const len = headline.length;
  const size = len < 50 ? 8.5 : len < 110 ? 6.6 : len < 220 ? 5.2 : 4.2;

  return (
    <div
      className="absolute inset-0 bg-[#F4F1EA]"
      style={{ containerType: 'inline-size', fontFamily: 'var(--font-body), sans-serif' }}
    >
      <div className="flex h-full flex-col p-[8cqw]">
        <p
          className="self-start rounded-full bg-[#B23A2E] px-[3cqw] py-[1cqw] font-semibold uppercase text-white"
          style={{ fontSize: '2.6cqw', letterSpacing: '0.18em' }}
        >
          No visual yet
        </p>
        <div className="flex flex-1 flex-col justify-center">
          <p
            className={`whitespace-pre-line font-semibold leading-[1.15] [overflow-wrap:anywhere] ${empty ? 'text-neutral-400' : 'text-[#4F3433]'}`}
            style={{ fontSize: `${size}cqw`, fontFamily: 'var(--font-heading), sans-serif' }}
          >
            {headline}
          </p>
          {small && (
            <p
              className="mt-[4cqw] whitespace-pre-line text-[#22371F]"
              style={{ fontSize: '4cqw' }}
            >
              {small}
            </p>
          )}
          {empty && (
            <p className="mt-[4cqw] text-neutral-400" style={{ fontSize: '3.6cqw' }}>
              Visual coming. Drop the Canva export here in Edit.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

/** 'Headline Small text: detail' becomes a headline and a smaller line. */
function splitSmall(text: string): [string, string] {
  const m = text.match(/^([\s\S]*?)\s*small text:\s*([\s\S]*)$/i);
  if (!m) return [text.replace(/^"([\s\S]*)"$/, '$1'), ''];
  return [m[1]!.trim().replace(/^"([\s\S]*)"$/, '$1'), m[2]!.trim()];
}
