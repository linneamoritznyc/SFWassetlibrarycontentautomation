'use client';

import type { Slide } from '@/lib/wormhole-types';
import { imageUrl } from './util';

/**
 * One 4:5 slide. An uploaded image wins. Without one, the slide text is set
 * as a clean white tile so every post is readable from day one.
 */
export function SlideView({ slide, fallback }: { slide: Slide; fallback: string }) {
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
    <div className="absolute inset-0 bg-white" style={{ containerType: 'inline-size' }}>
    <div className="flex h-full flex-col p-[8cqw]">
      <p
        className="font-semibold uppercase text-black"
        style={{ fontSize: '2.6cqw', letterSpacing: '0.32em' }}
      >
        Soil Food Web
      </p>
      <div className="flex flex-1 flex-col justify-center">
        <p
          className={`whitespace-pre-line font-semibold leading-[1.15] [overflow-wrap:anywhere] ${empty ? 'text-neutral-400' : 'text-black'}`}
          style={{ fontSize: `${size}cqw` }}
        >
          {headline}
        </p>
        {small && (
          <p className="mt-[4cqw] whitespace-pre-line text-neutral-700" style={{ fontSize: '4cqw' }}>
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
