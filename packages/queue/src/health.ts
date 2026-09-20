import { createServer, type Server } from 'node:http';
import type { Pool } from '@sfw/db';

/**
 * A health endpoint for the workers.
 *
 * Railway wants something to poll, and "the process is running" is not the
 * question worth asking: a worker that cannot reach the database is up and
 * useless. So this checks the connection and reports what the process is
 * claiming, and only answers 200 when both are true.
 *
 * Off unless PORT is set, because a worker does not otherwise need a socket.
 */
export function startHealthServer(options: {
  pool: Pool;
  name: string;
  types: string[];
  port?: number;
}): Server | null {
  const port = options.port ?? Number(process.env.PORT ?? 0);
  if (!port) return null;

  const server = createServer((request, response) => {
    void (async () => {
      const started = Date.now();
      try {
        await options.pool.query('select 1');
        response.writeHead(200, { 'content-type': 'application/json' });
        response.end(
          JSON.stringify({
            ok: true,
            worker: options.name,
            types: options.types,
            dbLatencyMs: Date.now() - started,
          }),
        );
      } catch (err) {
        response.writeHead(503, { 'content-type': 'application/json' });
        response.end(
          JSON.stringify({
            ok: false,
            worker: options.name,
            error: err instanceof Error ? err.message : 'database unreachable',
          }),
        );
      }
    })();
  });

  server.listen(port, () => console.log(`[${options.name}] health on :${port}`));
  server.unref();
  return server;
}
