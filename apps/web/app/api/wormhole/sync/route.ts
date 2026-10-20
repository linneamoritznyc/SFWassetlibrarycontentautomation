import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import {
  POST_COLUMNS,
  createPost,
  keepVersion,
  sanitizePatch,
  savePost,
  type WormholePost,
} from '@/lib/wormhole';
import {
  SYNC_EDITOR,
  SYNC_EDITOR_NOT_APPLIED,
  decide,
  forDoc,
  keepImages,
  syncTokenMatches,
} from '@/lib/wormhole-sync';
import { applyChanges } from '@/lib/wormhole-changes';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

// The doc never sends status or platform; those stay Wormhole's.
const DOC_FIELDS = [
  'iso_date',
  'date_tbd',
  'topic',
  'cta',
  'slides',
  'link',
  'sources',
  'visual_note',
  'caption',
] as const;

function unauthorized() {
  return NextResponse.json({ error: 'Sync token needed' }, { status: 401 });
}

/** Every post, in the shape the doc script reads. */
export async function GET(request: Request) {
  if (!syncTokenMatches(request.headers.get('authorization'))) return unauthorized();
  await applyChanges();
  const { rows } = await db().query(
    `select ${POST_COLUMNS} from wormhole_posts order by iso_date, id`,
  );
  const { rows: clock } = await db().query(`select now() as now`);
  return NextResponse.json({ posts: (rows as WormholePost[]).map(forDoc), now: clock[0].now });
}

type Change = {
  id?: string;
  fields?: Record<string, unknown>;
  base_updated_at?: string | null;
  edited_at?: string | null;
};

/**
 * Edits from the doc. Each change carries only the fields that changed in the
 * doc since the last sync. When Wormhole changed the same post in the
 * meantime, the newer edit wins and the older one is kept in
 * wormhole_versions, so nothing is lost.
 */
export async function POST(request: Request) {
  if (!syncTokenMatches(request.headers.get('authorization'))) return unauthorized();

  const body = (await request.json().catch(() => ({}))) as { changes?: Change[] };
  const changes = Array.isArray(body.changes) ? body.changes.slice(0, 200) : [];
  const results = [];

  for (const c of changes) {
    const raw = Object.fromEntries(
      Object.entries(c.fields ?? {}).filter(([k]) => (DOC_FIELDS as readonly string[]).includes(k)),
    );
    // The doc sends slide text only.
    if (Array.isArray(raw.slides))
      raw.slides = raw.slides.map((t) => ({ text: String(t ?? ''), image: null }));
    const patch = sanitizePatch(raw);

    if (!c.id) {
      const post = await createPost(patch, SYNC_EDITOR);
      results.push({ id: post.id, status: 'created', post: forDoc(post) });
      continue;
    }

    const { rows } = await db().query(`select ${POST_COLUMNS} from wormhole_posts where id = $1`, [
      c.id,
    ]);
    const current = rows[0] as WormholePost | undefined;
    if (!current) {
      results.push({ id: c.id, status: 'missing' });
      continue;
    }
    if (Object.keys(patch).length === 0) {
      results.push({ id: c.id, status: 'unchanged', post: forDoc(current) });
      continue;
    }
    if (patch.slides) patch.slides = keepImages(patch.slides, current.slides);

    if (decide(current.updated_at, c.base_updated_at, c.edited_at) === 'keep_wormhole') {
      await keepVersion(db(), c.id, { ...current, ...patch }, SYNC_EDITOR_NOT_APPLIED);
      results.push({ id: c.id, status: 'kept_wormhole', post: forDoc(current) });
      continue;
    }
    const post = await savePost(c.id, patch, SYNC_EDITOR);
    results.push(
      post ? { id: c.id, status: 'applied', post: forDoc(post) } : { id: c.id, status: 'missing' },
    );
  }

  const { rows: clock } = await db().query(`select now() as now`);
  return NextResponse.json({ results, now: clock[0].now });
}
