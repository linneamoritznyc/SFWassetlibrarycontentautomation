'use client';

import { useCallback, useEffect, useState } from 'react';

type Question = {
  id: number;
  text: string;
  status: string;
  answer: string | null;
  answered_at: string | null;
  created_at: string;
  asked_to: string | null;
  asked_to_email: string | null;
  post_hook: string | null;
  post_slot: string | null;
  context: { topic?: string; post_id?: string; story_id?: number };
};

/**
 * What the machine does not know, and who can tell it.
 *
 * Each question is one line someone can answer from memory. Answering it here
 * does the same thing as replying to the email: the answer becomes permanent
 * facts and whatever post was waiting gets written.
 */
export function QuestionsView() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [status, setStatus] = useState<'open' | 'answered' | 'all'>('open');
  const [drafts, setDrafts] = useState<Record<number, string>>({});
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/questions?status=${status}`);
      const body = (await res.json()) as { questions: Question[] };
      setQuestions(body.questions ?? []);
    } finally {
      setLoading(false);
    }
  }, [status]);

  useEffect(() => {
    void load();
  }, [load]);

  async function answer(question: Question, drop = false) {
    const text = drafts[question.id]?.trim();
    if (!drop && !text) return;

    const res = await fetch(`/api/questions/${question.id}/answer`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(drop ? { drop: true } : { answer: text }),
    });

    setNote(
      res.ok
        ? drop
          ? 'Dropped.'
          : 'Saved. Turning it into facts and releasing the post.'
        : (((await res.json()) as { error?: string }).error ?? 'That did not work.'),
    );
    setTimeout(() => setNote(''), 3000);
    await load();
  }

  const ageInHours = (iso: string) => (Date.now() - new Date(iso).getTime()) / 3_600_000;

  return (
    <main className="mx-auto max-w-3xl p-6">
      <header className="mb-4 flex flex-wrap items-baseline gap-3">
        <h1 className="text-lg font-semibold">Questions</h1>
        <div className="flex gap-1 text-xs">
          {(['open', 'answered', 'all'] as const).map((s) => (
            <button
              key={s}
              onClick={() => setStatus(s)}
              className={`rounded px-2 py-1 ${
                status === s ? 'bg-green-deep text-cream' : 'border border-green-mid/30'
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </header>

      {note && <p className="mb-3 text-sm font-medium text-green-deep">{note}</p>}

      {loading && <p className="text-sm text-green-mid">Loading</p>}
      {!loading && questions.length === 0 && (
        <p className="text-sm text-green-mid">
          Nothing outstanding. The machine has everything it asked for.
        </p>
      )}

      <ul className="space-y-3">
        {questions.map((question) => {
          const hours = ageInHours(question.created_at);
          const stale = question.status === 'open' && hours > 72;

          return (
            <li key={question.id} className="rounded border border-green-mid/20 bg-white p-3">
              <p className="font-medium">{question.text}</p>

              <p className="mt-1 text-xs text-green-mid">
                {question.asked_to ? `For ${question.asked_to}` : 'Unrouted'}
                {question.asked_to &&
                  !question.asked_to_email &&
                  ' (no email on file, so not sent)'}
                {question.context?.topic && ` · ${question.context.topic}`}
                {' · '}
                {Math.round(hours)}h ago
                {stale && (
                  <span className="ml-1 text-gold">
                    · past 72h, the post went to review flagged
                  </span>
                )}
              </p>

              {question.post_hook && (
                <p className="mt-1 text-xs text-green-mid">
                  Blocking: &ldquo;{question.post_hook}&rdquo;{' '}
                  {question.post_slot && `(${question.post_slot})`}
                </p>
              )}

              {question.status === 'open' ? (
                <div className="mt-2 flex gap-2">
                  <input
                    value={drafts[question.id] ?? ''}
                    onChange={(e) => setDrafts({ ...drafts, [question.id]: e.target.value })}
                    onKeyDown={(e) => e.key === 'Enter' && answer(question)}
                    placeholder="One line is enough"
                    className="flex-1 rounded border border-green-mid/40 px-2 py-1 text-sm"
                  />
                  <button
                    onClick={() => answer(question)}
                    className="rounded bg-green-deep px-3 py-1 text-sm text-cream"
                  >
                    Answer
                  </button>
                  <button
                    onClick={() => answer(question, true)}
                    className="rounded border border-green-mid/40 px-2 py-1 text-xs"
                    title="Not worth answering"
                  >
                    Drop
                  </button>
                </div>
              ) : (
                question.answer && (
                  <p className="mt-2 rounded bg-green-bright/10 p-2 text-sm">{question.answer}</p>
                )
              )}
            </li>
          );
        })}
      </ul>
    </main>
  );
}
