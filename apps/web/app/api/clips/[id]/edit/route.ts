import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { CLIP_RATIOS } from '@sfw/shared';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

export const dynamic = 'force-dynamic';

/**
 * The light editor.
 *
 * Trim, split and reorder all arrive as one list of segments in the order they
 * should play, because that is what they are once you stop thinking in verbs.
 * Caption fixes, crop focus and a music bed come along on the same call, so a
 * round of edits is one re-render rather than four.
 */
export const POST = route(
  async (request: NextRequest, { params }: { params: Promise<{ id: string }> }) => {
    const { id } = await params;
    const body = (await request.json()) as {
      segments?: { start: number; end: number }[];
      captionFixes?: { from: string; to: string }[];
      cropFocus?: number;
      musicAssetId?: string | null;
      musicGainDb?: number;
      ratios?: string[];
    };

    const pool = db();
    const { rows } = await pool.query<{ id: string }>(
      `select id from assets where id = $1 and type = 'clip'`,
      [id],
    );
    if (!rows[0]) return fail('No such clip', 404);

    for (const segment of body.segments ?? []) {
      if (!(segment.end > segment.start)) return fail('A segment has to end after it starts');
      if (segment.end - segment.start < 1) return fail('A segment under a second is not a segment');
    }

    const ratios = (body.ratios ?? ['9x16']).filter((r) =>
      (CLIP_RATIOS as readonly string[]).includes(r),
    );
    if (ratios.length === 0) return fail(`Ratios must be some of ${CLIP_RATIOS.join(', ')}`);

    // A new key each time, so an edit genuinely re-runs rather than being
    // swallowed as a duplicate of the last one.
    const stamp = Date.now();

    for (const ratio of ratios) {
      await enqueue(pool, {
        type: 'edit_clip',
        payload: { clip_id: id, ratio, ...body },
        priority: 2,
        dedupeKey: `edit_clip:${id}:${ratio}:${stamp}`,
      });
    }

    return NextResponse.json({ queued: ratios, note: 'Re-cutting. It takes a minute.' });
  },
);
