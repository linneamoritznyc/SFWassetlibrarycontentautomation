import type { Slide, WormholePost, WormholeStatus } from '@/lib/wormhole-types';

export const GREEN = '#2f6b46';

export function dayLabel(iso: string, style: 'long' | 'short' = 'long'): string {
  const d = new Date(`${iso}T12:00:00Z`);
  if (style === 'short') {
    return d.toLocaleDateString('en-US', {
      weekday: 'short',
      day: 'numeric',
      month: 'short',
      timeZone: 'UTC',
    });
  }
  return d.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC',
  });
}

/** The post's day as people read it, or "Date TBD". */
export function postDay(post: WormholePost, style: 'long' | 'short' = 'long'): string {
  return post.date_tbd ? 'Date TBD' : dayLabel(post.iso_date, style);
}

/** Dated posts in date order, then the ones with no date yet. */
export function byDate(a: WormholePost, b: WormholePost): number {
  return (
    Number(a.date_tbd) - Number(b.date_tbd) ||
    a.iso_date.localeCompare(b.iso_date) ||
    a.id.localeCompare(b.id)
  );
}

/** Monday of the week the post falls in, as YYYY-MM-DD, or "tbd". */
export function weekOf(post: WormholePost): string {
  if (post.date_tbd) return 'tbd';
  const d = new Date(`${post.iso_date}T12:00:00Z`);
  const dow = (d.getUTCDay() + 6) % 7;
  d.setUTCDate(d.getUTCDate() - dow);
  return d.toISOString().slice(0, 10);
}

export function weekLabel(monday: string): string {
  const a = new Date(`${monday}T12:00:00Z`);
  const b = new Date(a);
  b.setUTCDate(b.getUTCDate() + 6);
  const f = (d: Date) =>
    d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' });
  return `${f(a)} to ${f(b)}`;
}

export function ago(iso: string): string {
  const s = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
  if (s < 45) return 'just now';
  if (s < 3600) return `${Math.round(s / 60)} min ago`;
  if (s < 86400) return `${Math.round(s / 3600)} h ago`;
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

/** Every post shows at least one slide, so nothing is invisible on day one. */
export function slidesOf(post: WormholePost): Slide[] {
  return post.slides.length > 0 ? post.slides : [{ text: '', image: null }];
}

export function imageUrl(id: string): string {
  return `/api/wormhole/images/${id}`;
}

export const STATUS_STYLE: Record<WormholeStatus, string> = {
  draft: 'border-neutral-400 bg-white text-neutral-700',
  copy_approved: 'border-[#2f6b46] bg-[#e8f2ec] text-[#1d3b2a]',
  approved: 'border-[#2f6b46] bg-[#2f6b46] text-white',
  scheduled: 'border-[#1d3b2a] bg-[#1d3b2a] text-white',
};

/** Shrinks a Canva export to 1440 px wide JPEG on white before upload. */
export async function prepareImage(
  file: File,
): Promise<{ blob: Blob; width: number; height: number }> {
  const bitmap = await createImageBitmap(file);
  const scale = Math.min(1, 1440 / bitmap.width);
  const width = Math.round(bitmap.width * scale);
  const height = Math.round(bitmap.height * scale);
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d')!;
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, width, height);
  ctx.drawImage(bitmap, 0, 0, width, height);
  const blob = await new Promise<Blob>((resolve, reject) =>
    canvas.toBlob((b) => (b ? resolve(b) : reject(new Error('Could not read image'))), 'image/jpeg', 0.9),
  );
  return { blob, width, height };
}

export async function uploadImage(file: File): Promise<string> {
  const { blob, width, height } = await prepareImage(file);
  const res = await fetch('/api/wormhole/images', {
    method: 'POST',
    headers: { 'Content-Type': 'image/jpeg', 'x-width': String(width), 'x-height': String(height) },
    body: blob,
  });
  const body = await res.json();
  if (!res.ok) throw new Error(body.error ?? 'Upload failed');
  return body.id as string;
}

function esc(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function linkify(s: string): string {
  const t = esc(s.trim());
  return /^https?:\/\//.test(s.trim()) ? `<a href="${t}">${t}</a>` : t;
}

/** The posts in Stephanie's planning-doc template, ready to paste into Google Docs. */
export function toDocHtml(posts: WormholePost[], title: string): string {
  const parts = posts.map((p) => {
    const words = p.slides
      .map((s, i) => (s.text.trim() ? `<p>Slide ${i + 1}: ${esc(s.text).replace(/\n/g, '<br>')}</p>` : ''))
      .join('');
    const sources = p.sources.filter((s) => s.trim()).map((s) => `<p>${linkify(s)}</p>`).join('');
    return [
      `<h2>${esc(postDay(p))}</h2>`,
      `<h3>${esc(p.topic)}</h3>`,
      `<h3>CTA (Optional): ${esc(p.cta)}</h3>`,
      `<p>Words:</p>${words}`,
      `<p>Link: ${p.link ? linkify(p.link) : ''}</p>`,
      `<p>Source:</p>${sources}`,
      `<h3>Visual Asset (Image Thumbnail for preview and Link to Canva Project):</h3>`,
      `<p>${esc(p.visual_note).replace(/\n/g, '<br>')}</p>`,
      `<h3>Caption/Body Copy:</h3>`,
      `<p>${esc(p.caption).replace(/\n/g, '<br>')}</p>`,
    ].join('\n');
  });
  return `<!doctype html><html><head><meta charset="utf-8"><title>${esc(title)}</title></head><body>\n${parts.join('\n<hr>\n')}\n</body></html>`;
}
