import { NextResponse } from 'next/server';

/** One shape for every error the API returns, so the UI can rely on it. */
export function fail(message: string, status = 400) {
  return NextResponse.json({ error: message }, { status });
}

/**
 * Wraps a route handler so a thrown error becomes a 500 with a readable
 * message in the log, rather than an opaque crash. A missing environment
 * variable is the common case and its message already says what to do.
 */
export function route<T extends unknown[]>(
  handler: (...args: T) => Promise<NextResponse>,
): (...args: T) => Promise<NextResponse> {
  return async (...args: T) => {
    try {
      return await handler(...args);
    } catch (err) {
      console.error(err);
      return fail(err instanceof Error ? err.message : 'Something went wrong', 500);
    }
  };
}
