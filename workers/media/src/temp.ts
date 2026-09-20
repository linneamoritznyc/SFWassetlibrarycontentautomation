import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

/**
 * A scratch directory that always gets cleaned up.
 *
 * The media worker downloads multi-gigabyte originals, and Railway containers
 * have a fixed disk. A job that throws halfway through must not leave the file
 * behind, or the tenth failure fills the disk and every job after it fails for
 * a reason that has nothing to do with the job.
 */
export async function withTempDir<T>(fn: (dir: string) => Promise<T>): Promise<T> {
  const dir = await mkdtemp(join(process.env.MEDIA_TMPDIR ?? tmpdir(), 'sfw-'));
  try {
    return await fn(dir);
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}
