'use client';

import { useRef, useState } from 'react';
import type { Slide } from '@/lib/wormhole-types';
import { SlideView } from './SlideView';

/** A swipeable 4:5 carousel with dots, like Instagram's. */
export function Carousel({
  slides,
  fallback,
  counter = false,
}: {
  slides: Slide[];
  fallback: string;
  counter?: boolean;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [index, setIndex] = useState(0);

  function onScroll() {
    const el = ref.current;
    if (!el) return;
    setIndex(Math.round(el.scrollLeft / el.clientWidth));
  }

  function go(i: number) {
    const el = ref.current;
    if (!el) return;
    el.scrollTo({ left: i * el.clientWidth, behavior: 'smooth' });
  }

  const many = slides.length > 1;

  return (
    <div>
      <div className="group relative">
        <div
          ref={ref}
          onScroll={onScroll}
          className="flex snap-x snap-mandatory overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
        >
          {slides.map((s, i) => (
            <div key={i} className="relative aspect-[4/5] w-full shrink-0 snap-center bg-white">
              <SlideView slide={s} fallback={fallback} />
            </div>
          ))}
        </div>
        {many && index > 0 && (
          <button
            aria-label="Previous slide"
            onClick={() => go(index - 1)}
            className="absolute left-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-full bg-white/90 text-lg text-black shadow"
          >
            ‹
          </button>
        )}
        {many && index < slides.length - 1 && (
          <button
            aria-label="Next slide"
            onClick={() => go(index + 1)}
            className="absolute right-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-full bg-white/90 text-lg text-black shadow"
          >
            ›
          </button>
        )}
        {many && counter && (
          <span className="absolute right-3 top-3 rounded-full bg-black/70 px-2 py-0.5 text-xs text-white">
            {index + 1} / {slides.length}
          </span>
        )}
      </div>
      {many && !counter && (
        <div className="flex justify-center gap-1 pt-2">
          {slides.map((_, i) => (
            <span
              key={i}
              className={`h-1.5 w-1.5 rounded-full ${i === index ? 'bg-[#0095f6]' : 'bg-neutral-300'}`}
            />
          ))}
        </div>
      )}
    </div>
  );
}
