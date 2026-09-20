import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

/** Reads the database on every call, so it is never prerendered. */
export const dynamic = 'force-dynamic';

/** The "Find clips" button. The transcript has to exist first. */
export const POST = route(
  async (_request: NextRequest, { params }: { params: Promise<{ id: string }> }) => {
    const { id } = await params;
    const pool = db();

    const { rows } = await pool.query<{ has_transcript: boolean; type: string }>(
      `select a.type, (t.asset_id is not null) as has_transcript
     from assets a left join transcripts t on t.asset_id = a.id
     where a.id = $1`,
      [id],
    );

    const asset = rows[0];
    if (!asset) return fail('No such asset', 404);
    if (asset.type !== 'video') return fail('Only a video can be clipped');

    if (!asset.has_transcript) {
      // Queue the transcript and let find_clips follow from it, rather than
      // failing at the user.
      await enqueue(pool, {
        type: 'transcribe',
        payload: { asset_id: id },
        dedupeKey: `transcribe:${id}`,
      });
      return NextResponse.json({ queued: 'transcribe', note: 'Transcribing first. Clips follow.' });
    }

    const jobId = await enqueue(pool, {
      type: 'find_clips',
      payload: { asset_id: id },
      priority: 3,
      dedupeKey: `find_clips:${id}`,
    });

    return NextResponse.json({ queued: 'find_clips', jobId });
  },
);
