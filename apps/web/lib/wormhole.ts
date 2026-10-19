import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';
import { AUTH_COOKIE, NAME_COOKIE, cleanName, isValidToken } from './wormhole-auth';

import { EDITABLE, STATUSES, type Slide, type WormholePost } from './wormhole-types';

export * from './wormhole-types';

export const POST_COLUMNS = `id, to_char(iso_date, 'YYYY-MM-DD') as iso_date, topic, platform, caption,
  slides, cta, link, sources, visual_note, note, status, updated_by, updated_at`;

/** Second check behind the middleware, so a route never runs unguarded. */
export async function guard(): Promise<{ editor: string } | NextResponse> {
  const jar = cookies();
  if (!(await isValidToken(jar.get(AUTH_COOKIE)?.value))) {
    return NextResponse.json({ error: 'Password needed' }, { status: 401 });
  }
  return { editor: cleanName(jar.get(NAME_COOKIE)?.value) };
}

export function isUuid(s: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(s);
}

/** Keeps only fields people may edit, in the shapes the table expects. */
export function sanitizePatch(body: Record<string, unknown>): Partial<WormholePost> {
  const out: Record<string, unknown> = {};
  for (const key of EDITABLE) {
    if (!(key in body)) continue;
    const v = body[key];
    if (key === 'slides') {
      if (!Array.isArray(v)) continue;
      out.slides = v.slice(0, 20).map((s) => {
        const slide = (s ?? {}) as Partial<Slide>;
        const image = typeof slide.image === 'string' && isUuid(slide.image) ? slide.image : null;
        return { text: String(slide.text ?? '').slice(0, 2000), image };
      });
    } else if (key === 'sources') {
      if (!Array.isArray(v)) continue;
      out.sources = v.slice(0, 20).map((s) => String(s).slice(0, 500));
    } else if (key === 'status') {
      if (STATUSES.some((s) => s.value === v)) out.status = v;
    } else if (key === 'iso_date') {
      if (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v)) out.iso_date = v;
    } else {
      out[key] = String(v ?? '').slice(0, 10_000);
    }
  }
  return out as Partial<WormholePost>;
}
