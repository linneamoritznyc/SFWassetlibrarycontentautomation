'use client';

import { useState } from 'react';

type Segment = { start: number; end: number };

/**
 * The light editor.
 *
 * Trim, split and reorder are one list of segments in the order they play, so
 * the three buttons all edit the same thing. Caption fixes, crop focus and a
 * music bed ride along on the same save, because a round of changes should be
 * one re-render rather than four.
 *
 * Heavy editing still belongs in a real editor. This is for the last ten per
 * cent: an edge half a word out, a name Whisper misheard, a crop that cut
 * someone out of frame.
 */
export function ClipEditor({
  clip,
  onClose,
  onSaved,
}: {
  clip: { id: string; clip_start_s: number; clip_end_s: number; url: string | null };
  onClose: () => void;
  onSaved: (note: string) => void;
}) {
  const [segments, setSegments] = useState<Segment[]>([
    { start: clip.clip_start_s, end: clip.clip_end_s },
  ]);
  const [fixes, setFixes] = useState<{ from: string; to: string }[]>([]);
  const [focus, setFocus] = useState(0.5);
  const [gain, setGain] = useState(-18);
  const [music, setMusic] = useState('');
  const [busy, setBusy] = useState(false);

  const total = segments.reduce((sum, s) => sum + (s.end - s.start), 0);

  function update(index: number, patch: Partial<Segment>) {
    setSegments((prev) => prev.map((s, i) => (i === index ? { ...s, ...patch } : s)));
  }

  function split(index: number) {
    setSegments((prev) => {
      const segment = prev[index]!;
      const middle = (segment.start + segment.end) / 2;
      return [
        ...prev.slice(0, index),
        { start: segment.start, end: middle },
        { start: middle, end: segment.end },
        ...prev.slice(index + 1),
      ];
    });
  }

  function move(index: number, by: -1 | 1) {
    setSegments((prev) => {
      const next = [...prev];
      const to = index + by;
      if (to < 0 || to >= next.length) return prev;
      [next[index], next[to]] = [next[to]!, next[index]!];
      return next;
    });
  }

  async function save() {
    setBusy(true);
    try {
      const res = await fetch(`/api/clips/${clip.id}/edit`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          segments,
          captionFixes: fixes.filter((f) => f.from.trim() && f.to.trim()),
          cropFocus: focus,
          musicAssetId: music.trim() || null,
          musicGainDb: gain,
        }),
      });

      const body = (await res.json()) as { note?: string; error?: string };
      onSaved(body.error ?? body.note ?? 'Re-cutting.');
      if (res.ok) onClose();
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mt-3 rounded border border-green-deep/40 bg-green-bright/5 p-3 text-xs">
      <div className="flex items-baseline">
        <h4 className="text-sm font-semibold">Edit</h4>
        <span className="ml-2 text-green-mid">{total.toFixed(1)}s total</span>
        <button onClick={onClose} className="ml-auto text-green-mid">
          Close
        </button>
      </div>

      <p className="mt-2 font-medium">Segments, in the order they play</p>
      <ul className="mt-1 space-y-1">
        {segments.map((segment, index) => (
          <li key={index} className="flex flex-wrap items-center gap-1">
            <span className="w-4 text-green-mid">{index + 1}</span>
            <input
              type="number"
              step="0.1"
              value={segment.start}
              onChange={(e) => update(index, { start: Number(e.target.value) })}
              className="w-20 rounded border border-green-mid/40 px-1 py-0.5"
            />
            <span className="text-green-mid">to</span>
            <input
              type="number"
              step="0.1"
              value={segment.end}
              onChange={(e) => update(index, { end: Number(e.target.value) })}
              className="w-20 rounded border border-green-mid/40 px-1 py-0.5"
            />
            <span className="text-green-mid">{(segment.end - segment.start).toFixed(1)}s</span>

            <button
              onClick={() => split(index)}
              className="rounded border border-green-mid/40 px-1"
            >
              Split
            </button>
            <button
              onClick={() => move(index, -1)}
              className="rounded border border-green-mid/40 px-1"
            >
              Up
            </button>
            <button
              onClick={() => move(index, 1)}
              className="rounded border border-green-mid/40 px-1"
            >
              Down
            </button>
            {segments.length > 1 && (
              <button
                onClick={() => setSegments((prev) => prev.filter((_, i) => i !== index))}
                className="rounded border border-green-mid/40 px-1"
              >
                Drop
              </button>
            )}
          </li>
        ))}
      </ul>

      <label className="mt-3 block">
        <span className="font-medium">Crop focus</span>
        <input
          type="range"
          min={0}
          max={1}
          step={0.05}
          value={focus}
          onChange={(e) => setFocus(Number(e.target.value))}
          className="ml-2 align-middle"
        />
        <span className="ml-2 text-green-mid">
          {focus < 0.4 ? 'left' : focus > 0.6 ? 'right' : 'centre'}
        </span>
      </label>

      <div className="mt-3">
        <p className="font-medium">Caption fixes</p>
        {fixes.map((fix, index) => (
          <div key={index} className="mt-1 flex gap-1">
            <input
              value={fix.from}
              onChange={(e) =>
                setFixes((prev) =>
                  prev.map((f, i) => (i === index ? { ...f, from: e.target.value } : f)),
                )
              }
              placeholder="heard"
              className="w-32 rounded border border-green-mid/40 px-1 py-0.5"
            />
            <input
              value={fix.to}
              onChange={(e) =>
                setFixes((prev) =>
                  prev.map((f, i) => (i === index ? { ...f, to: e.target.value } : f)),
                )
              }
              placeholder="should be"
              className="w-32 rounded border border-green-mid/40 px-1 py-0.5"
            />
          </div>
        ))}
        <button
          onClick={() => setFixes((prev) => [...prev, { from: '', to: '' }])}
          className="mt-1 rounded border border-green-mid/40 px-1"
        >
          Add a fix
        </button>
      </div>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <span className="font-medium">Music bed</span>
        <input
          value={music}
          onChange={(e) => setMusic(e.target.value)}
          placeholder="asset id, or leave empty"
          className="w-56 rounded border border-green-mid/40 px-1 py-0.5"
        />
        <label>
          {gain} dB
          <input
            type="range"
            min={-30}
            max={-6}
            value={gain}
            onChange={(e) => setGain(Number(e.target.value))}
            className="ml-2 align-middle"
          />
        </label>
      </div>

      <button
        onClick={save}
        disabled={busy}
        className="mt-3 rounded bg-green-deep px-3 py-1.5 text-cream disabled:opacity-60"
      >
        {busy ? 'Saving' : 'Re-cut'}
      </button>
    </div>
  );
}
