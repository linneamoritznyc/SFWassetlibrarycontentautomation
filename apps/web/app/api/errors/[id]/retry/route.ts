import { NextResponse, type NextRequest } from 'next/server';
import { retry } from '@sfw/queue';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

/**
 * Put a dead job back on the queue with a fresh budget. Returns 409 when a
 * live job already holds the same dedupe key, because the retry has in effect
 * already happened.
 */
export const POST = route(
  async (_request: NextRequest, { params }: { params: Promise<{ id: string }> }) => {
    const { id } = await params;
    const job = await retry(db(), id);
    if (!job)
      return fail('Nothing to retry: the job is not dead, or newer work already replaced it', 409);
    return NextResponse.json(job);
  },
);
