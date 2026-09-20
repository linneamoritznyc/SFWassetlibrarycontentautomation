'use client';

import { useCallback, useEffect, useState } from 'react';
import { ClipEditor } from './ClipEditor';

type Clip = {
  id: string;
  parent_id: string;
  filename: string;
  status: string;
  clip_start_s: number;
  clip_end_s: number;
  duration_s: number | null;
  description: string | null;
  notes: string | null;
  has_file: boolean;
  url: string | null;
};

type Video = {
  id: string;
  filename: string;
  duration_s: number | null;
  has_transcript: boolean;
  clips: number;
};

type Week = { spentUsd: number; kept: number; proposed: number; perClipUsd: number | null };

/**
 * The clipping machine.
 *
 * A source video on the left, its candidates on the right, each with the hook
 * the speaker actually said and why it is worth cutting. Keep, Trim or Cut.
 *
 * The cost line at the top is the argument the whole phase exists to make: the
 * contractor was about $100 a clip.
 */
export function ClipsView() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [videoId, setVideoId] = useState<string | null>(null);
  const [clips, setClips] = useState<Clip[]>([]);
  const [week, setWeek] = useState<Week | null>(null);
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState<string | null>(null);

  useEffect(() => {
    void fetch('/api/clips', { method: 'POST' })
      .then((r) => r.json())
      .then((body: { videos: Video[] }) => {
        setVideos(body.videos ?? []);
        const first = body.videos?.find((v) => v.clips > 0) ?? body.videos?.[0];
        if (first) setVideoId(first.id);
      })
      .finally(() => setLoading(false));
  }, []);

  const loadClips = useCallback(async (id: string) => {
    const res = await fetch(`/api/clips?parent=${id}`);
    const body = (await res.json()) as { clips: Clip[]; week: Week };
    setClips(body.clips ?? []);
    setWeek(body.week ?? null);
  }, []);

  useEffect(() => {
    if (videoId) void loadClips(videoId);
  }, [videoId, loadClips]);

  async function act(clip: Clip, action: 'keep' | 'cut', body?: unknown) {
    const res = await fetch(`/api/clips/${clip.id}/${action}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body ?? {}),
    });

    if (!res.ok) {
      setNote(((await res.json()) as { error?: string }).error ?? 'That did not work.');
      return;
    }

    setNote(action === 'keep' ? 'Kept. Cutting the other ratios.' : 'Cut.');
    setTimeout(() => setNote(''), 2000);
    if (videoId) void loadClips(videoId);
  }

  function openEditor(clip: Clip) {
    setEditing((current) => (current === clip.id ? null : clip.id));
  }

  async function trim(clip: Clip) {
    const start = Number(window.prompt('Start, in seconds', clip.clip_start_s.toFixed(1)));
    if (Number.isNaN(start)) return;
    const end = Number(window.prompt('End, in seconds', clip.clip_end_s.toFixed(1)));
    if (Number.isNaN(end)) return;

    const res = await fetch(`/api/clips/${clip.id}/trim`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ start, end }),
    });

    setNote(
      res.ok ? 'Trimmed. Re-cutting.' : (((await res.json()) as { error?: string }).error ?? 'No.'),
    );
    setTimeout(() => setNote(''), 2500);
    if (videoId) void loadClips(videoId);
  }

  async function findClips(id: string) {
    const res = await fetch(`/api/assets/${id}/find-clips`, { method: 'POST' });
    const body = (await res.json()) as { queued?: string; note?: string; error?: string };
    setNote(body.error ?? body.note ?? `Queued ${body.queued}. This takes a few minutes.`);
    setTimeout(() => setNote(''), 5000);
  }

  // The same handlers for both sections; only the title and the list differ.
  const sectionProps = {
    onAct: act,
    onTrim: trim,
    editing,
    onEdit: openEditor,
    onSaved: (message: string) => {
      setNote(message);
      setTimeout(() => setNote(''), 4000);
      if (videoId) void loadClips(videoId);
    },
  };

  const pending = clips.filter((c) => c.status === 'inbox');
  const kept = clips.filter((c) => c.status === 'cleared' || c.status === 'used');

  return (
    <div className="flex h-[calc(100vh-41px)]">
      <aside className="w-72 shrink-0 overflow-y-auto border-r border-green-mid/20 p-3 text-sm">
        <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-green-mid">
          Source video
        </h2>
        {loading && <p className="text-green-mid">Loading</p>}
        {!loading && videos.length === 0 && (
          <p className="text-xs text-green-mid">
            No video in the library yet. Upload one and it gets transcribed automatically.
          </p>
        )}
        <ul className="space-y-1">
          {videos.map((video) => (
            <li key={video.id}>
              <button
                onClick={() => setVideoId(video.id)}
                className={`w-full rounded px-2 py-1 text-left ${
                  videoId === video.id ? 'bg-green-deep text-cream' : 'hover:bg-green-bright/15'
                }`}
              >
                <span className="block truncate">{video.filename}</span>
                <span className="block text-xs opacity-80">
                  {video.duration_s ? `${Math.round(video.duration_s / 60)} min` : 'unknown length'}
                  {' · '}
                  {video.clips > 0
                    ? `${video.clips} clips`
                    : video.has_transcript
                      ? 'no clips yet'
                      : 'no transcript'}
                </span>
              </button>
            </li>
          ))}
        </ul>
      </aside>

      <main className="flex-1 overflow-y-auto p-4">
        <header className="mb-4 flex flex-wrap items-baseline gap-4">
          <h1 className="text-lg font-semibold">Clips</h1>
          {week && (
            <p className="text-sm text-green-mid">
              This week: {week.proposed} proposed, {week.kept} kept, ${week.spentUsd.toFixed(2)} of
              AI.{' '}
              {week.perClipUsd != null && (
                <strong className="text-green-deep">
                  ${week.perClipUsd.toFixed(2)} per kept clip
                </strong>
              )}
            </p>
          )}
          {videoId && (
            <button
              onClick={() => findClips(videoId)}
              className="ml-auto rounded bg-green-deep px-3 py-1.5 text-sm text-cream"
            >
              Find clips
            </button>
          )}
        </header>

        {note && <p className="mb-3 text-sm font-medium text-green-deep">{note}</p>}

        {pending.length === 0 && kept.length === 0 && (
          <p className="text-sm text-green-mid">
            No candidates yet. Press Find clips, or wait for a long video to finish transcribing.
          </p>
        )}

        <Section title={`To decide (${pending.length})`} clips={pending} {...sectionProps} />
        <Section title={`Kept (${kept.length})`} clips={kept} {...sectionProps} />
      </main>
    </div>
  );
}

function Section({
  title,
  clips,
  onAct,
  onTrim,
  editing,
  onEdit,
  onSaved,
}: {
  title: string;
  clips: Clip[];
  onAct: (clip: Clip, action: 'keep' | 'cut') => void;
  onTrim: (clip: Clip) => void;
  editing: string | null;
  onEdit: (clip: Clip) => void;
  onSaved: (note: string) => void;
}) {
  if (clips.length === 0) return null;

  return (
    <section className="mb-8">
      <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-green-mid">{title}</h2>
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {clips.map((clip) => (
          <article key={clip.id} className="rounded border border-green-mid/20 bg-white p-3">
            {clip.url ? (
              <video
                src={clip.url}
                controls
                preload="metadata"
                className="w-full rounded bg-black"
              />
            ) : (
              <p className="rounded bg-green-bright/10 p-6 text-center text-xs text-green-mid">
                Cutting the preview
              </p>
            )}

            <p className="mt-2 font-medium">{clip.description ?? 'No hook'}</p>
            {clip.notes && (
              <p className="mt-1 whitespace-pre-line text-xs text-green-mid">{clip.notes}</p>
            )}
            <p className="mt-1 text-xs text-green-mid">
              {clip.clip_start_s.toFixed(1)}s to {clip.clip_end_s.toFixed(1)}s (
              {Math.round(clip.clip_end_s - clip.clip_start_s)}s)
            </p>

            {clip.status === 'inbox' && (
              <div className="mt-2 flex gap-2">
                <button
                  onClick={() => onAct(clip, 'keep')}
                  className="rounded bg-green-deep px-2 py-1 text-xs text-cream"
                >
                  Keep
                </button>
                <button
                  onClick={() => onTrim(clip)}
                  className="rounded border border-green-mid/40 px-2 py-1 text-xs"
                >
                  Trim
                </button>
                <button
                  onClick={() => onAct(clip, 'cut')}
                  className="rounded border border-green-mid/40 px-2 py-1 text-xs"
                >
                  Cut
                </button>
              </div>
            )}

            <button onClick={() => onEdit(clip)} className="mt-2 text-xs text-green-mid underline">
              {editing === clip.id ? 'Hide editor' : 'Edit'}
            </button>

            {editing === clip.id && (
              <ClipEditor clip={clip} onClose={() => onEdit(clip)} onSaved={onSaved} />
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
