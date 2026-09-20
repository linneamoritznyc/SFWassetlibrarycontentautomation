import { NextResponse, type NextRequest } from 'next/server';
import { presignGet } from '@sfw/storage';
import { db } from '@/lib/db';
import { route } from '@/lib/http';

/** Reads the database on every call, so it is never prerendered. */
export const dynamic = 'force-dynamic';

type ClipRow = {
  id: string;
  parent_id: string;
  filename: string;
  status: string;
  clip_start_s: number;
  clip_end_s: number;
  duration_s: number | null;
  description: string | null;
  notes: string | null;
  r2_key: string;
  has_file: boolean;
  parent_filename: string;
};

/**
 * The clips for one source video, plus what the week has cost.
 *
 * The cost line is the point of the whole phase: the contractor was about $100
 * a clip, so the number next to each clip is the argument.
 */
export const GET = route(async (request: NextRequest) => {
  const pool = db();
  const parent = request.nextUrl.searchParams.get('parent');

  const { rows } = await pool.query<ClipRow>(
    `select c.id, c.parent_id, c.filename, c.status, c.clip_start_s, c.clip_end_s,
            c.duration_s, c.description, c.notes, c.r2_key,
            c.r2_key not like 'clips/pending/%' as has_file,
            p.filename as parent_filename
     from assets c
     join assets p on p.id = c.parent_id
     where c.type = 'clip' ${parent ? 'and c.parent_id = $1' : ''}
     order by c.clip_start_s`,
    parent ? [parent] : [],
  );

  const clips = await Promise.all(
    rows.map(async (row) => ({
      ...row,
      url: row.has_file ? await presignGet('sfw-media', row.r2_key) : null,
    })),
  );

  // Everything spent on AI in the last seven days, against the clips kept in
  // the same window. Worker time is not billed per job, so this is the part
  // that actually varies.
  const { rows: costRows } = await pool.query<{ spent: string; kept: number; proposed: number }>(
    `select coalesce((select sum(cost_usd) from ai_calls
                      where created_at > now() - interval '7 days'), 0) as spent,
            (select count(*)::int from assets
              where type = 'clip' and status in ('cleared', 'used')
                and created_at > now() - interval '7 days') as kept,
            (select count(*)::int from assets
              where type = 'clip' and created_at > now() - interval '7 days') as proposed`,
  );

  const cost = costRows[0]!;
  const kept = cost.kept;

  return NextResponse.json({
    clips,
    week: {
      spentUsd: Number(cost.spent),
      kept,
      proposed: cost.proposed,
      perClipUsd: kept > 0 ? Number(cost.spent) / kept : null,
    },
  });
});

/** The videos that have clips, or are long enough to. */
export const POST = route(async () => {
  const { rows } = await db().query(
    `select a.id, a.filename, a.duration_s,
            (t.asset_id is not null) as has_transcript,
            (select count(*)::int from assets c where c.parent_id = a.id and c.type = 'clip') as clips
     from assets a
     left join transcripts t on t.asset_id = a.id
     where a.type = 'video'
     order by a.created_at desc
     limit 50`,
  );
  return NextResponse.json({ videos: rows });
});
