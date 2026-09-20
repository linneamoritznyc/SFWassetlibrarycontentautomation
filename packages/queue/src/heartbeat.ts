import type { Pool } from '@sfw/db';

/** How often a worker says it is alive. The app shows a red dot past 5 minutes. */
export const HEARTBEAT_INTERVAL_MS = 60_000;

export async function beat(pool: Pool, worker: string, types: string[]): Promise<void> {
  await pool.query(
    `insert into worker_heartbeats (worker, types, beat_at)
     values ($1, $2::text[], now())
     on conflict (worker) do update set types = excluded.types, beat_at = now()`,
    [worker, types],
  );
}

export type Heartbeat = { worker: string; types: string[]; beat_at: Date; stale: boolean };

export async function heartbeats(pool: Pool): Promise<Heartbeat[]> {
  const res = await pool.query<Heartbeat>(
    `select worker, types, beat_at, beat_at < now() - interval '5 minutes' as stale
     from worker_heartbeats
     order by worker`,
  );
  return res.rows;
}

/**
 * Starts a heartbeat in the background and hands back a function that stops it.
 * A failed beat is logged and otherwise ignored: losing the database for a
 * minute should not take a worker down.
 */
export function startHeartbeat(pool: Pool, worker: string, types: string[]): () => void {
  const tick = () => {
    void beat(pool, worker, types).catch((err) => {
      console.error(`[${worker}] heartbeat failed:`, err);
    });
  };

  tick();
  const timer = setInterval(tick, HEARTBEAT_INTERVAL_MS);
  timer.unref();

  return () => clearInterval(timer);
}
