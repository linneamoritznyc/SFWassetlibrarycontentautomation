/**
 * Designs built in tools/wormhole-visuals, shown on top of the database.
 *
 * - designs: finished slides (text and image) for a post that has no images yet.
 * - posted: the real Instagram tile, as slide 1, for posts already on the profile.
 * - virtual: Instagram posts that are not in the database yet (pinned and older).
 *
 * A post's own images always win, so an upload in Wormhole replaces the design.
 */
import data from './wormhole-designs.json';
import type { Slide, WormholePost } from './wormhole-types';

type Designs = {
  designs: Record<string, Slide[]>;
  posted: Record<string, string>;
  virtual: (Omit<WormholePost, 'updated_by' | 'updated_at'> & { pinned: number | null })[];
};
const D = data as unknown as Designs;

const hasImages = (p: WormholePost) => p.slides?.some((s) => s.image);

export function withDesigns(rows: WormholePost[], includeVirtual = true): WormholePost[] {
  const out = rows.map((p): WormholePost => {
    if (hasImages(p)) return p;
    const design = D.designs[p.id];
    if (design) return { ...p, slides: design };
    const tile = D.posted[p.id];
    if (tile) {
      const slides: Slide[] = p.slides?.length ? p.slides : [{ text: '', image: null }];
      const first: Slide = { text: slides[0]?.text ?? '', image: tile };
      return { ...p, status: 'scheduled' as const, slides: [first, ...slides.slice(1)] };
    }
    return p;
  });
  if (!includeVirtual) return out;
  const have = new Set(rows.map((r) => r.id));
  const extra = D.virtual
    .filter((v) => !have.has(v.id))
    .map((v) => ({ ...v, updated_by: 'Instagram', updated_at: '2026-10-18T00:00:00Z' }) as WormholePost);
  return [...out, ...extra];
}
