import { randomUUID } from 'node:crypto';
import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { keys, putObject } from '@sfw/storage';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

/** Reads the database on every call, so it is never prerendered. */
export const dynamic = 'force-dynamic';

/** A screenshot is small. Anything larger than this is not a paste. */
const MAX_IMAGE_BYTES = 12 * 1024 * 1024;

const IMAGE_TYPES: Record<string, string> = {
  'image/png': 'png',
  'image/jpeg': 'jpg',
  'image/webp': 'webp',
  'image/gif': 'gif',
};

/**
 * The paste box.
 *
 * Paste a screenshot, a link or a block of text and the machine starts. A
 * screenshot is read by `paste_intake`, which pulls out the sender, the message
 * and any links, and sends each link to `web_fetch`, which turns the page into
 * sourced facts. A bare link skips straight to `web_fetch`.
 *
 * Screenshots go in as `reference` assets: provenance, never a post visual.
 * See docs/paste-intake.md.
 */
export const POST = route(async (request: NextRequest) => {
  const form = await request.formData();
  const file = form.get('file');
  const url = (form.get('url') as string | null)?.trim();
  const text = (form.get('text') as string | null)?.trim();
  const note = (form.get('note') as string | null)?.trim() ?? null;

  const pool = db();

  if (file instanceof File) {
    const extension = IMAGE_TYPES[file.type];
    if (!extension) {
      return fail(`${file.type || 'That file'} is not an image this can read. Paste a screenshot.`);
    }
    if (file.size > MAX_IMAGE_BYTES) {
      return fail(
        'That image is larger than a screenshot should be. Upload it as an asset instead.',
      );
    }

    const assetId = randomUUID();
    const filename = `pasted-${new Date().toISOString().slice(0, 10)}.${extension}`;
    const r2Key = keys.original(assetId, filename);
    const bytes = Buffer.from(await file.arrayBuffer());

    await putObject('sfw-media', r2Key, bytes, file.type);

    await pool.query(
      `insert into assets (id, type, filename, bucket, r2_key, notes, release_status)
       values ($1, 'reference', $2, 'sfw-media', $3, $4, 'unknown')`,
      [assetId, filename, r2Key, note],
    );

    await enqueue(pool, {
      type: 'paste_intake',
      payload: { asset_id: assetId },
      // Highest priority: someone is standing there having just pasted it.
      priority: 1,
      dedupeKey: `paste_intake:${assetId}`,
    });

    return NextResponse.json({ kind: 'screenshot', assetId });
  }

  if (url) {
    if (!isHttpUrl(url)) return fail('That does not look like a web address');
    const jobId = await enqueue(pool, {
      type: 'web_fetch',
      payload: { url },
      priority: 1,
      dedupeKey: `web_fetch:${url}`,
    });
    return NextResponse.json({ kind: 'link', url, jobId });
  }

  if (text) {
    // A note from a person is a source in its own right, per spec section 4.2.
    const { rows } = await pool.query<{ id: number }>(
      `insert into sources (kind, ref, title, fetched_at)
       values ('human', $1, $2, now())
       on conflict (kind, ref) do update set fetched_at = now()
       returning id`,
      [`pasted:${hash(text)}`, text.slice(0, 120)],
    );

    return NextResponse.json({ kind: 'text', sourceId: rows[0]!.id, note: 'Stored as a source.' });
  }

  return fail('Nothing to paste. Give me a screenshot, a link or some text.');
});

function isHttpUrl(value: string): boolean {
  try {
    const parsed = new URL(value);
    return parsed.protocol === 'http:' || parsed.protocol === 'https:';
  } catch {
    return false;
  }
}

function hash(value: string): string {
  // Short, stable, and enough to stop the same note being stored twice.
  let h = 0;
  for (let i = 0; i < value.length; i += 1) {
    h = (Math.imul(31, h) + value.charCodeAt(i)) | 0;
  }
  return Math.abs(h).toString(36);
}
