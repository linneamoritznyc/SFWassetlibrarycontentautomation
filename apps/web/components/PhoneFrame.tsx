'use client';

import { useState } from 'react';

/**
 * A post as it will actually look.
 *
 * CLAUDE.md section 5 is explicit that mockups must look like a real post on a
 * real phone feed: the right aspect ratio, a real profile header, and the
 * caption truncated where Instagram truncates it. A slide-deck layout hides
 * exactly the problem a review is meant to catch, which is a hook that falls
 * below the fold.
 */

const RATIOS: Record<string, { aspect: string; label: string }> = {
  feed: { aspect: '4 / 5', label: 'Instagram feed' },
  carousel: { aspect: '4 / 5', label: 'Instagram carousel' },
  reel: { aspect: '9 / 16', label: 'Reel' },
  story: { aspect: '9 / 16', label: 'Story' },
  short: { aspect: '9 / 16', label: 'YouTube Short' },
  linkedin: { aspect: '4 / 5', label: 'LinkedIn' },
};

/** Instagram cuts the caption at about 125 characters. */
const TRUNCATE_AT = 125;

export function PhoneFrame({
  platform,
  format,
  hook,
  caption,
  hashtags,
  images,
  collaborators,
}: {
  platform: string;
  format: string;
  hook: string | null;
  caption: string | null;
  hashtags: string[];
  images: { id: string; thumbUrl: string | null; description: string | null }[];
  collaborators: string[];
}) {
  const [expanded, setExpanded] = useState(false);
  const shape = RATIOS[format] ?? RATIOS.feed!;
  const body = caption ?? '';
  const isLong = body.length > TRUNCATE_AT;
  const shown = expanded || !isLong ? body : body.slice(0, TRUNCATE_AT);

  const handle = platform === 'linkedin' ? 'Soil Food Web School' : 'soilfoodwebschool';

  return (
    <div className="w-[300px] shrink-0 overflow-hidden rounded-xl border border-green-mid/25 bg-white">
      <header className="flex items-center gap-2 px-3 py-2">
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-green-deep text-[10px] font-semibold text-cream">
          SFW
        </span>
        <span className="text-sm font-semibold">{handle}</span>
        <span className="ml-auto text-xs text-green-mid">{shape.label}</span>
      </header>

      <div className="relative bg-green-deep" style={{ aspectRatio: shape.aspect }}>
        {images[0]?.thumbUrl ? (
          <img
            src={images[0].thumbUrl}
            alt={images[0].description ?? ''}
            className="h-full w-full object-cover"
          />
        ) : (
          <p className="flex h-full items-center justify-center p-4 text-center text-xs text-cream">
            No image chosen. A post cannot go out without one.
          </p>
        )}

        {images.length > 1 && (
          <span className="absolute right-2 top-2 rounded bg-black/60 px-1.5 py-0.5 text-[10px] text-white">
            1/{images.length}
          </span>
        )}
      </div>

      <div className="px-3 py-2 text-sm">
        <p className="whitespace-pre-line">
          <span className="font-semibold">{handle}</span>{' '}
          {hook && <span className="font-medium">{hook}</span>}
          {hook && body.startsWith(hook) ? shown.slice(hook.length) : shown}
          {isLong && !expanded && (
            <button onClick={() => setExpanded(true)} className="text-green-mid">
              ... more
            </button>
          )}
        </p>

        {hashtags.length > 0 && <p className="mt-1 text-xs text-green-mid">{hashtags.join(' ')}</p>}
        {collaborators.length > 0 && (
          <p className="mt-1 text-xs text-green-mid">with {collaborators.join(', ')}</p>
        )}
      </div>
    </div>
  );
}
