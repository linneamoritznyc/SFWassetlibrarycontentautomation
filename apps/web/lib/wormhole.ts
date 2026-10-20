import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';
import { db } from './db';
import { AUTH_COOKIE, NAME_COOKIE, cleanName, isValidToken } from './wormhole-auth';

import { EDITABLE, STATUSES, type Slide, type WormholePost } from './wormhole-types';

/** Tiles built by tools/wormhole-visuals live in the app's public folder. */
export function isRepoImage(v: string): boolean {
  return /^\/wormhole\/(tiles|ig)\/[a-z0-9._-]+\.(jpg|png)$/i.test(v);
}

export * from './wormhole-types';

export const POST_COLUMNS = `id, to_char(iso_date, 'YYYY-MM-DD') as iso_date, date_tbd, topic, platform, caption,
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
        const image =
          typeof slide.image === 'string' && (isUuid(slide.image) || isRepoImage(slide.image))
            ? slide.image
            : null;
        return { text: String(slide.text ?? '').slice(0, 2000), image };
      });
    } else if (key === 'sources') {
      if (!Array.isArray(v)) continue;
      out.sources = v.slice(0, 20).map((s) => String(s).slice(0, 500));
    } else if (key === 'status') {
      if (STATUSES.some((s) => s.value === v)) out.status = v;
    } else if (key === 'iso_date') {
      if (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v)) out.iso_date = v;
    } else if (key === 'date_tbd') {
      if (typeof v === 'boolean') out.date_tbd = v;
    } else {
      out[key] = String(v ?? '').slice(0, 10_000);
    }
  }
  return out as Partial<WormholePost>;
}

type Editable = (typeof EDITABLE)[number];
type Queryable = { query: (text: string, values?: unknown[]) => Promise<unknown> };

function snapshotOf(post: Record<string, unknown>): Record<string, unknown> {
  return Object.fromEntries(EDITABLE.map((k) => [k, post[k]]));
}

/** Keeps a copy of a post in wormhole_versions, with who and when. */
export async function keepVersion(
  q: Queryable,
  postId: string,
  data: Record<string, unknown>,
  editor: string,
): Promise<void> {
  await q.query(`insert into wormhole_versions (post_id, data, editor) values ($1, $2, $3)`, [
    postId,
    JSON.stringify(snapshotOf(data)),
    editor,
  ]);
}

/**
 * Saves an edit and keeps the new state in wormhole_versions, in one
 * transaction. Every edit goes through here: the editor in the browser and
 * the Google Doc sync alike. Returns null when the post does not exist.
 */
export async function savePost(
  id: string,
  patch: Partial<WormholePost>,
  editor: string,
): Promise<WormholePost | null> {
  const keys = Object.keys(patch) as Editable[];
  const sets: string[] = [];
  const values: unknown[] = [id];
  for (const k of keys) {
    const v = patch[k];
    values.push(k === 'slides' || k === 'sources' ? JSON.stringify(v) : v);
    sets.push(`${k} = $${values.length}${k === 'slides' || k === 'sources' ? '::jsonb' : ''}`);
  }
  values.push(editor);
  sets.push(`updated_by = $${values.length}`, 'updated_at = now()');

  const client = await db().connect();
  try {
    await client.query('begin');
    const { rows } = await client.query(
      `update wormhole_posts set ${sets.join(', ')} where id = $1 returning ${POST_COLUMNS}`,
      values,
    );
    if (rows.length === 0) {
      await client.query('rollback');
      return null;
    }
    await keepVersion(client, id, rows[0], editor);
    await client.query('commit');
    return rows[0] as WormholePost;
  } catch (err) {
    await client.query('rollback').catch(() => {});
    throw err;
  } finally {
    client.release();
  }
}

/** A new post. Starts with one empty slide so it is never invisible. */
export async function createPost(
  patch: Partial<WormholePost>,
  editor: string,
): Promise<WormholePost> {
  const id = `n${Date.now().toString(36)}${Math.random().toString(36).slice(2, 5)}`;
  const iso = patch.iso_date ?? new Date().toISOString().slice(0, 10);
  const { rows } = await db().query(
    `insert into wormhole_posts (id, iso_date, topic, slides, created_by, updated_by)
     values ($1, $2, $3, $4, $5, $5)
     returning ${POST_COLUMNS}`,
    [id, iso, patch.topic ?? 'New post', JSON.stringify([{ text: '', image: null }]), editor],
  );
  const rest: Partial<WormholePost> = { ...patch };
  delete rest.iso_date;
  delete rest.topic;
  if (Object.keys(rest).length === 0) return rows[0] as WormholePost;
  return (await savePost(id, rest, editor)) ?? (rows[0] as WormholePost);
}
