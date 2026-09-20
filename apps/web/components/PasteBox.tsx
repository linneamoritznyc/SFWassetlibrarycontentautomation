'use client';

import { useCallback, useEffect, useRef, useState } from 'react';

type Result =
  | { kind: 'screenshot'; assetId: string }
  | { kind: 'link'; url: string }
  | { kind: 'text'; sourceId: number };

/**
 * Paste a screenshot, a link or some text and the machine starts.
 *
 * Listens for Cmd-V anywhere on the page, so a screenshot copied from Google
 * Chat goes in without finding a button first. The screenshot is stored as a
 * reference asset: it is where the story came from, never the picture the post
 * goes out with.
 */
export function PasteBox() {
  const [state, setState] = useState<'idle' | 'sending' | 'done' | 'error'>('idle');
  const [message, setMessage] = useState('');
  const [preview, setPreview] = useState<string | null>(null);
  const [text, setText] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const send = useCallback(async (form: FormData) => {
    setState('sending');
    try {
      const res = await fetch('/api/paste', { method: 'POST', body: form });
      const body = (await res.json()) as Result & { error?: string };

      if (!res.ok) {
        setState('error');
        setMessage(body.error ?? 'That did not go in.');
        return;
      }

      setState('done');
      setMessage(
        body.kind === 'screenshot'
          ? 'Reading the screenshot. Any links in it get fetched and turned into facts.'
          : body.kind === 'link'
            ? 'Fetching the page and pulling the facts out of it.'
            : 'Stored as a source.',
      );
    } catch (err) {
      setState('error');
      setMessage(err instanceof Error ? err.message : 'That did not go in.');
    }
  }, []);

  const sendFile = useCallback(
    (file: File) => {
      setPreview(URL.createObjectURL(file));
      const form = new FormData();
      form.set('file', file);
      void send(form);
    },
    [send],
  );

  useEffect(() => {
    function onPaste(event: ClipboardEvent) {
      // Let a paste into a text field be an ordinary paste.
      const target = event.target as HTMLElement | null;
      if (target && ['INPUT', 'TEXTAREA'].includes(target.tagName) && target !== inputRef.current) {
        return;
      }

      const image = Array.from(event.clipboardData?.items ?? []).find((i) =>
        i.type.startsWith('image/'),
      );

      if (image) {
        const file = image.getAsFile();
        if (file) {
          event.preventDefault();
          sendFile(file);
        }
      }
    }

    window.addEventListener('paste', onPaste);
    return () => window.removeEventListener('paste', onPaste);
  }, [sendFile]);

  function submitText(event: React.FormEvent) {
    event.preventDefault();
    if (!text.trim()) return;

    const form = new FormData();
    const looksLikeUrl = /^https?:\/\//i.test(text.trim());
    form.set(looksLikeUrl ? 'url' : 'text', text.trim());
    void send(form);
    setText('');
  }

  return (
    <section className="rounded border border-green-mid/30 bg-white p-4 shadow-sfw">
      <h2 className="text-sm font-semibold">Paste something</h2>
      <p className="mt-1 text-xs text-green-mid">
        A screenshot of a message, a link, or a note. Cmd-V works anywhere on this page.
      </p>

      <form onSubmit={submitText} className="mt-3 flex gap-2">
        <input
          ref={inputRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste a link, or type a note"
          className="flex-1 rounded border border-green-mid/40 px-3 py-2 text-sm"
        />
        <button
          type="submit"
          disabled={state === 'sending'}
          className="rounded bg-green-deep px-3 py-2 text-sm text-cream disabled:opacity-60"
        >
          Go
        </button>
      </form>

      <label className="mt-2 block text-xs text-green-mid">
        or choose an image:{' '}
        <input
          type="file"
          accept="image/*"
          className="text-xs"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) sendFile(file);
          }}
        />
      </label>

      {preview && (
        <img src={preview} alt="What you pasted" className="mt-3 max-h-40 rounded border" />
      )}

      {state !== 'idle' && (
        <p
          className={`mt-3 text-xs ${state === 'error' ? 'text-gold' : 'text-green-mid'}`}
          role="status"
        >
          {state === 'sending' ? 'Sending' : message}
        </p>
      )}
    </section>
  );
}
