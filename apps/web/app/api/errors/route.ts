import { NextResponse } from 'next/server';
import { deadJobs, heartbeats } from '@sfw/queue';
import { db } from '@/lib/db';
import { route } from '@/lib/http';

/**
 * Dead jobs, and whether the workers are alive. The two belong on one screen:
 * a pile of queued work and no heartbeat means the worker is down, which is a
 * different problem from a job that keeps failing.
 */
export const GET = route(async () => {
  const pool = db();
  const [dead, beats, queued] = await Promise.all([
    deadJobs(pool, 200),
    heartbeats(pool),
    pool.query<{ type: string; count: number }>(
      `select type, count(*)::int as count from jobs
       where status in ('queued', 'running') group by type order by count desc`,
    ),
  ]);

  return NextResponse.json({ dead, workers: beats, pending: queued.rows });
});
