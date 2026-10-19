'use client';

import { useState, type ReactNode } from 'react';

/** Hashtags, @mentions and links in blue, the way the apps show them. */
function highlight(text: string, color: string): ReactNode[] {
  return text.split(/(#[\p{L}\p{N}_]+|@[\w.]+|https?:\/\/\S+)/gu).map((part, i) =>
    /^(#|@|https?:\/\/)/.test(part) ? (
      <span key={i} style={{ color }}>
        {part}
      </span>
    ) : (
      part
    ),
  );
}

/**
 * Caption cut where the app cuts it: Instagram after about two lines with
 * "more", LinkedIn after about three with "...see more".
 */
export function Caption({
  text,
  prefix,
  limit,
  moreLabel,
  color,
}: {
  text: string;
  prefix?: string;
  limit: number;
  moreLabel: string;
  color: string;
}) {
  const [open, setOpen] = useState(false);
  if (!text.trim()) {
    return <p className="italic text-neutral-400">No caption yet.</p>;
  }
  const firstBreak = text.indexOf('\n');
  const cut = Math.min(limit, firstBreak > 20 ? firstBreak : limit);
  const short = !open && text.length > cut;
  const shown = short ? text.slice(0, cut).trimEnd() : text;

  return (
    <p className="whitespace-pre-line break-words leading-snug">
      {prefix && <span className="mr-1 font-semibold">{prefix}</span>}
      {highlight(shown, color)}
      {short && (
        <>
          {moreLabel.startsWith('…') ? '' : '… '}
          <button onClick={() => setOpen(true)} className="text-neutral-500">
            {moreLabel}
          </button>
        </>
      )}
    </p>
  );
}
