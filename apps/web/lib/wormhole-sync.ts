/**
 * The Google Doc sync. A script bound to the doc (integrations/google-doc)
 * calls /api/wormhole/sync with a shared token, so Wormhole needs no Google
 * credentials. Edits from the doc go through savePost like any other edit.
 */
import type { Slide, WormholePost } from './wormhole-types';

export const SYNC_EDITOR = 'Google Doc';
export const SYNC_EDITOR_NOT_APPLIED = 'Google Doc (older edit, not applied)';

/** Constant-time check of "Authorization: Bearer <token>" against WORMHOLE_SYNC_TOKEN. */
export function syncTokenMatches(header: string | null): boolean {
  const expected = process.env.WORMHOLE_SYNC_TOKEN ?? '';
  // A short token is too easy to guess; treat it as not configured.
  if (expected.length < 24) return false;
  const given = (header ?? '').replace(/^Bearer\s+/i, '');
  if (given.length !== expected.length) return false;
  let diff = 0;
  for (let i = 0; i < expected.length; i++) diff |= expected.charCodeAt(i) ^ given.charCodeAt(i);
  return diff === 0;
}

export type Decision = 'apply' | 'keep_wormhole';

/**
 * Who wins when the doc sends an edit.
 *
 * baseUpdatedAt is the post's updated_at the last time the doc and Wormhole
 * agreed (null when the doc has never synced this post). If Wormhole has not
 * changed since then, the doc's edit applies. If both changed, the newer edit
 * wins; the doc's edit time is the doc file's last-modified time, which is
 * never earlier than the edit itself.
 */
export function decide(
  currentUpdatedAt: string | Date,
  baseUpdatedAt: string | null | undefined,
  editedAt: string | null | undefined,
): Decision {
  const current = new Date(currentUpdatedAt).getTime();
  const base = baseUpdatedAt ? new Date(baseUpdatedAt).getTime() : NaN;
  if (!Number.isNaN(base) && current <= base) return 'apply';
  const edited = editedAt ? new Date(editedAt).getTime() : NaN;
  if (Number.isNaN(edited)) return 'keep_wormhole';
  return edited >= current ? 'apply' : 'keep_wormhole';
}

/** The doc knows only slide text. Keep each slide's image by position. */
export function keepImages(incoming: Slide[], current: Slide[]): Slide[] {
  return incoming.map((s, i) => ({ text: s.text, image: s.image ?? current[i]?.image ?? null }));
}

/** What the doc shows for a post, plus what the script needs to sync it. */
export function forDoc(p: WormholePost) {
  return {
    id: p.id,
    iso_date: p.iso_date,
    date_tbd: p.date_tbd,
    topic: p.topic,
    cta: p.cta,
    slides: p.slides.map((s) => s.text),
    link: p.link,
    sources: p.sources,
    visual_note: p.visual_note,
    caption: p.caption,
    status: p.status,
    thumb: p.slides.find((s) => s.image)?.image ?? null,
    updated_at: p.updated_at,
    updated_by: p.updated_by,
  };
}
