import { NextResponse, type NextRequest } from 'next/server';
import { db } from '@/lib/db';
import { route } from '@/lib/http';

export const dynamic = 'force-dynamic';

/** News cards, best first, with what they were linked to. */
export const GET = route(async (request: NextRequest) => {
  const status = request.nextUrl.searchParams.get('status') ?? 'all';

  const { rows } = await db().query(
    `select n.id, n.url, n.title, n.published_at, n.summary, n.relevance, n.status,
            f.name as feed,
            coalesce((
              select json_agg(fa.text order by fa.confidence desc)
              from facts fa where fa.id = any(n.linked_facts)
            ), '[]'::json) as facts,
            coalesce((
              select json_agg(json_build_object('id', a.id, 'description', a.description, 'thumb_key', a.thumb_key))
              from assets a where a.id = any(n.linked_assets)
            ), '[]'::json) as assets,
            (select count(*)::int from stories s
              where s.origin = 'news' and s.origin_ref = n.id::text) as stories
     from news_items n
     left join feeds f on f.id = n.feed_id
     where ($1 = 'all' or n.status = $1)
       and n.relevance is not null
     order by n.relevance desc nulls last, n.published_at desc nulls last
     limit 80`,
    [status],
  );

  const feeds = await db().query(
    `select f.id, f.name, f.url, f.kind, f.active,
            (select count(*)::int from news_items n where n.feed_id = f.id) as items
     from feeds f order by f.name`,
  );

  return NextResponse.json({ items: rows, feeds: feeds.rows });
});
