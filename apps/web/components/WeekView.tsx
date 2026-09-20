'use client';

import { useCallback, useEffect, useState } from 'react';
import { REJECT_REASONS } from '@sfw/shared';
import { PhoneFrame } from './PhoneFrame';

type Post = {
  id: string;
  slot_date: string | null;
  slot_time: string | null;
  platform: string;
  format: string;
  hook: string | null;
  caption: string | null;
  hashtags: string[];
  cta_text: string | null;
  cta_url: string | null;
  collaborators: string[];
  status: string;
  experiment: boolean;
  critic_score: number | null;
  critic_notes: {
    verdict?: string;
    must_fix?: { check: string; quote: string; fix: string }[];
    issues?: { check: string; quote: string; note: string }[];
  } | null;
  angle: string | null;
  pillar: string | null;
  assets: { id: string; thumbUrl: string | null; description: string | null; type: string }[];
  open_questions: { id: number; text: string; asked_to: string | null }[];
};

const REASON_LABELS: Record<string, string> = {
  too_vague: 'Too vague',
  wrong_image: 'Wrong image',
  ai_tone: 'AI tone',
  fact_wrong: 'Fact wrong',
  off_brand: 'Off brand',
};

/**
 * The weekly review. One screen, fifteen minutes.
 *
 * Each post shows as it will look on the phone, with why it was chosen, what
 * the critic flagged, and anything still unanswered behind it. Approve, edit in
 * place, or reject with a reason.
 */
export function WeekView() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [note, setNote] = useState('');
  const [editing, setEditing] = useState<string | null>(null);
  const [draft, setDraft] = useState({ hook: '', caption: '' });

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/week');
      const body = (await res.json()) as { posts: Post[] };
      setPosts(body.posts ?? []);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  async function act(post: Post, action: string, body?: unknown) {
    const res = await fetch(`/api/posts/${post.id}/${action}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body ?? {}),
    });

    const result = (await res.json()) as { error?: string; status?: string };
    setNote(res.ok ? (result.status ?? 'done') : (result.error ?? 'That did not work.'));
    setTimeout(() => setNote(''), 2500);
    await load();
  }

  const waiting = posts.filter((p) => p.status === 'in_review');
  const stuck = posts.filter((p) => p.status === 'revising' || p.status === 'proposed');
  const done = posts.filter((p) => p.status === 'approved');

  return (
    <main className="mx-auto max-w-6xl p-6">
      <header className="mb-4 flex flex-wrap items-baseline gap-3">
        <h1 className="text-lg font-semibold">This week</h1>
        <p className="text-sm text-green-mid">
          {loading
            ? 'Loading'
            : `${waiting.length} to review, ${stuck.length} waiting, ${done.length} approved`}
        </p>
      </header>

      {note && <p className="mb-3 text-sm font-medium text-green-deep">{note}</p>}

      {!loading && posts.length === 0 && (
        <p className="text-sm text-green-mid">
          Nothing planned yet. The planner runs on Monday, or paste something and a story gets
          proposed from it.
        </p>
      )}

      {[
        { title: `To review (${waiting.length})`, items: waiting },
        { title: `Waiting on something (${stuck.length})`, items: stuck },
        { title: `Approved (${done.length})`, items: done },
      ].map(
        (group) =>
          group.items.length > 0 && (
            <section key={group.title} className="mb-8">
              <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-green-mid">
                {group.title}
              </h2>

              <div className="space-y-6">
                {group.items.map((post) => (
                  <article
                    key={post.id}
                    className="flex flex-wrap gap-4 rounded border border-green-mid/20 bg-white p-4"
                  >
                    <PhoneFrame
                      platform={post.platform}
                      format={post.format}
                      hook={post.hook}
                      caption={post.caption}
                      hashtags={post.hashtags}
                      images={post.assets}
                      collaborators={post.collaborators}
                    />

                    <div className="min-w-[280px] flex-1 text-sm">
                      <p className="text-xs text-green-mid">
                        {post.slot_date ?? 'no date'} {post.slot_time?.slice(0, 5) ?? ''} &middot;{' '}
                        {post.platform} &middot; {post.format}
                        {post.experiment && ' · experiment'}
                        {post.pillar && ` · ${post.pillar}`}
                      </p>

                      {post.angle && (
                        <p className="mt-2">
                          <span className="font-medium">Why this post: </span>
                          {post.angle}
                        </p>
                      )}

                      {post.critic_score != null && (
                        <p className="mt-2 text-xs">
                          <span
                            className={
                              post.critic_score >= 85
                                ? 'font-medium text-green-deep'
                                : 'font-medium text-gold'
                            }
                          >
                            Critic {Math.round(post.critic_score)}/100
                          </span>
                          {post.critic_notes?.verdict && ` — ${post.critic_notes.verdict}`}
                        </p>
                      )}

                      {(post.critic_notes?.must_fix?.length ?? 0) > 0 && (
                        <ul className="mt-1 space-y-0.5 text-xs text-gold">
                          {post.critic_notes!.must_fix!.map((f, i) => (
                            <li key={i}>
                              <strong>{f.check}</strong>: &ldquo;{f.quote}&rdquo; — {f.fix}
                            </li>
                          ))}
                        </ul>
                      )}

                      {post.open_questions.length > 0 && (
                        <div className="mt-2 rounded border border-gold/40 bg-gold/10 p-2 text-xs">
                          <p className="font-medium">Waiting on an answer:</p>
                          <ul className="mt-1 space-y-0.5">
                            {post.open_questions.map((q) => (
                              <li key={q.id}>
                                {q.text} {q.asked_to && <em>({q.asked_to})</em>}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {editing === post.id ? (
                        <div className="mt-3 space-y-2">
                          <input
                            value={draft.hook}
                            onChange={(e) => setDraft({ ...draft, hook: e.target.value })}
                            className="w-full rounded border border-green-mid/40 px-2 py-1"
                            placeholder="Hook"
                          />
                          <textarea
                            value={draft.caption}
                            onChange={(e) => setDraft({ ...draft, caption: e.target.value })}
                            rows={8}
                            className="w-full rounded border border-green-mid/40 p-2 text-xs"
                          />
                          <div className="flex gap-2">
                            <button
                              onClick={async () => {
                                await act(post, 'edit', draft);
                                setEditing(null);
                              }}
                              className="rounded bg-green-deep px-2 py-1 text-xs text-cream"
                            >
                              Save edit
                            </button>
                            <button
                              onClick={() => setEditing(null)}
                              className="rounded border border-green-mid/40 px-2 py-1 text-xs"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      ) : (
                        <div className="mt-3 flex flex-wrap gap-2">
                          {post.status !== 'approved' && (
                            <button
                              onClick={() => act(post, 'approve')}
                              className="rounded bg-green-deep px-3 py-1.5 text-sm text-cream"
                            >
                              Approve
                            </button>
                          )}
                          <button
                            onClick={() => {
                              setEditing(post.id);
                              setDraft({ hook: post.hook ?? '', caption: post.caption ?? '' });
                            }}
                            className="rounded border border-green-mid/40 px-3 py-1.5 text-sm"
                          >
                            Edit
                          </button>
                          {REJECT_REASONS.map((reason) => (
                            <button
                              key={reason}
                              onClick={() => act(post, 'reject', { reason })}
                              className="rounded border border-green-mid/30 px-2 py-1 text-xs"
                              title={`Reject: ${REASON_LABELS[reason]}`}
                            >
                              {REASON_LABELS[reason]}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  </article>
                ))}
              </div>
            </section>
          ),
      )}
    </main>
  );
}
