export type JobStatus = 'queued' | 'running' | 'done' | 'failed' | 'dead';

export type Job<P = Record<string, unknown>> = {
  id: string;
  type: string;
  payload: P;
  priority: number;
  status: JobStatus;
  attempts: number;
  max_attempts: number;
  run_after: Date;
  error: string | null;
  dedupe_key: string | null;
  created_at: Date;
  updated_at: Date;
};

export type EnqueueInput = {
  type: string;
  payload?: Record<string, unknown>;
  /** Lower runs first. Default 5. */
  priority?: number;
  /**
   * Blocks a duplicate while an identical job is still queued or running. Once
   * the job finishes the key frees up, so the same work can be asked for again.
   */
  dedupeKey?: string;
  runAfter?: Date;
};

/** What a job handler is given. */
export type JobContext<P = Record<string, unknown>> = {
  job: Job<P>;
  /** Enqueue follow-on work from inside a handler. */
  enqueue: (input: EnqueueInput) => Promise<string | null>;
};

export type JobHandler<P = Record<string, unknown>> = (ctx: JobContext<P>) => Promise<void>;

export type HandlerMap = Record<string, JobHandler>;

/**
 * Declares a handler with a typed payload. The queue stores payloads as jsonb,
 * so nothing can prove the shape at runtime; validate inside the handler with
 * the zod schema for that job. This only saves the casting.
 *
 *   export const ingest = handler<{ asset_id: string }>(async ({ job }) => {
 *     ...job.payload.asset_id
 *   });
 */
export function handler<P extends Record<string, unknown>>(fn: JobHandler<P>): JobHandler {
  return fn as unknown as JobHandler;
}
