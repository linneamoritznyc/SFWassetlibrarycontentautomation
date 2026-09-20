import { NextResponse, type NextRequest } from 'next/server';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';
import { parseLaterCsv } from '@/lib/later-csv';

export const dynamic = 'force-dynamic';

/**
 * Takes a Later CSV export when the Instagram Graph API is not available.
 *
 * Rows are matched to posts by their permalink. A row that matches nothing is
 * reported rather than dropped, because the usual cause is a post published by
 * hand that the system never knew about, and that is worth knowing.
 */
export const POST = route(async (request: NextRequest) => {
  const form = await request.formData();
  const file = form.get('file');

  if (!(file instanceof File)) return fail('Attach the CSV Later exported');

  const { rows, unmatched } = parseLaterCsv(await file.text());
  if (rows.length === 0) return fail('That CSV had no rows in it');

  const pool = db();
  let imported = 0;
  const missed: string[] = [];

  for (const row of rows) {
    if (!row.permalink) continue;

    const post = await pool.query<{ id: string }>(
      `select id from posts where published_url = $1
          or published_url like $2
       limit 1`,
      [row.permalink, `%${lastPathSegment(row.permalink)}%`],
    );

    const id = post.rows[0]?.id;
    if (!id) {
      missed.push(row.permalink);
      continue;
    }

    await pool.query(
      `insert into metrics (post_id, captured_at, reach, likes, comments, saves, shares, link_clicks)
       values ($1, now(), $2, $3, $4, $5, $6, $7)`,
      [id, row.reach, row.likes, row.comments, row.saves, row.shares, row.linkClicks],
    );
    imported += 1;
  }

  return NextResponse.json({
    imported,
    rows: rows.length,
    unmatchedColumns: unmatched,
    unknownPosts: missed.slice(0, 20),
  });
});

function lastPathSegment(url: string): string {
  return url.replace(/\/+$/, '').split('/').pop() ?? url;
}
