import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

export const dynamic = 'force-dynamic';

type Params = { params: Promise<{ id: string; action: string }> };

/**
 * Dismiss a news card, or push one into the pipeline by hand when the ranker
 * scored it below the bar but a human can see the angle.
 */
export const POST = route(async (_request: NextRequest, { params }: Params) => {
  const { id, action } = await params;
  const pool = db();

  if (action === 'dismiss') {
    await pool.query(`update news_items set status = 'dismissed' where id = $1`, [id]);
    return NextResponse.json({ status: 'dismissed' });
  }

  if (action === 'draft') {
    const { rows } = await pool.query<{ url: string; title: string | null }>(
      'select url, title from news_items where id = $1',
      [id],
    );
    const item = rows[0];
    if (!item) return fail('No such news item', 404);

    // Fetch the page properly rather than working from the feed summary: the
    // facts a post cites should come from the article, not the teaser.
    await enqueue(pool, {
      type: 'web_fetch',
      payload: { url: item.url, from_asset_id: null },
      priority: 2,
      dedupeKey: `web_fetch:${item.url}`,
    });

    await pool.query(`update news_items set status = 'drafted' where id = $1`, [id]);
    return NextResponse.json({
      status: 'drafted',
      note: 'Fetching the article and proposing a story.',
    });
  }

  return fail(`"${action}" is not something a news card can do. Try dismiss or draft.`);
});
