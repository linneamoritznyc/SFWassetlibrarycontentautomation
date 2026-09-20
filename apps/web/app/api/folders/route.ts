import { NextResponse, type NextRequest } from 'next/server';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

/** The sidebar. Smart folders are saved filters, grouped into four sections. */
export const GET = route(async () => {
  const { rows } = await db().query(
    `select id, name, section, filters, position
     from smart_folders order by section, position, name`,
  );
  return NextResponse.json({ folders: rows });
});

/** "Save current filters as folder". */
export const POST = route(async (request: NextRequest) => {
  const body = (await request.json()) as { name?: string; filters?: unknown };
  if (!body.name?.trim()) return fail('A folder needs a name');

  const { rows } = await db().query(
    `insert into smart_folders (name, section, filters, position)
     values ($1, 'saved', $2::jsonb,
             coalesce((select max(position) + 1 from smart_folders where section = 'saved'), 0))
     on conflict (section, name) do update set filters = excluded.filters
     returning id, name, section, filters, position`,
    [body.name.trim(), JSON.stringify(body.filters ?? {})],
  );

  return NextResponse.json(rows[0]);
});
