import { NextResponse, type NextRequest } from 'next/server';
import { presignGet } from '@sfw/storage';
import { db } from '@/lib/db';
import { route } from '@/lib/http';

export const dynamic = 'force-dynamic';

type PostRow = {
  id: string;
  story_id: number | null;
  slot_date: string | null;
  slot_time: string | null;
  platform: string;
  format: string;
  hook: string | null;
  caption: string | null;
  hashtags: string[];
  cta_text: string | null;
  cta_url: string | null;
  collaborators: string[];
  status: string;
  experiment: boolean;
  critic_score: number | null;
  critic_notes: Record<string, unknown> | null;
  angle: string | null;
  pillar: string | null;
  assets: { id: string; thumb_key: string | null; description: string | null; type: string }[];
  open_questions: { id: number; text: string; asked_to: string | null }[];
};

/**
 * The weekly review: every post waiting on a human, with the images it would
 * go out with, why it was chosen, what the critic said, and any question still
 * unanswered behind it.
 *
 * Everything needed to decide is on the row, because the point is fifteen
 * minutes a week, and that only works if nothing needs looking up.
 */
export const GET = route(async (request: NextRequest) => {
  const status = request.nextUrl.searchParams.getAll('status');
  const statuses = status.length ? status : ['proposed', 'revising', 'in_review', 'approved'];

  const { rows } = await db().query<PostRow>(
    `select p.id, p.story_id, p.slot_date::text, p.slot_time::text, p.platform, p.format,
            p.hook, p.caption, p.hashtags, p.cta_text, p.cta_url, p.collaborators,
            p.status, p.experiment, p.critic_score, p.critic_notes,
            s.angle, s.pillar,
            coalesce((
              select json_agg(json_build_object(
                'id', a.id, 'thumb_key', a.thumb_key,
                'description', a.description, 'type', a.type
              ))
              from assets a where a.id = any(p.asset_ids)
            ), '[]'::json) as assets,
            coalesce((
              select json_agg(json_build_object(
                'id', q.id, 'text', q.text, 'asked_to', pe.name
              ))
              from questions q
              left join people pe on pe.id = q.asked_to
              where q.status = 'open' and q.context->>'post_id' = p.id::text
            ), '[]'::json) as open_questions
     from posts p
     left join stories s on s.id = p.story_id
     where p.status = any($1::text[])
     order by p.slot_date nulls last, p.slot_time nulls last, p.created_at`,
    [statuses],
  );

  const posts = await Promise.all(
    rows.map(async (post) => ({
      ...post,
      assets: await Promise.all(
        post.assets.map(async (asset) => ({
          ...asset,
          thumbUrl: asset.thumb_key ? await presignGet('sfw-media', asset.thumb_key) : null,
        })),
      ),
    })),
  );

  return NextResponse.json({ posts });
});
