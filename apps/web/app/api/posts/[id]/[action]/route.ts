import { NextResponse, type NextRequest } from 'next/server';
import { enqueue } from '@sfw/queue';
import { REJECT_REASONS } from '@sfw/shared';
import { db } from '@/lib/db';
import { fail, route } from '@/lib/http';

export const dynamic = 'force-dynamic';

type Params = { params: Promise<{ id: string; action: string }> };

/**
 * Approve, reject or edit one post.
 *
 * An edit is stored as a new `post_versions` row authored by a human, and the
 * diff against what the AI wrote is what `learn_weekly` reads. That is the
 * whole self-improvement loop: a correction made once turns into a rule.
 *
 * A rejection needs a reason code, enforced here and in the database, because
 * "no" with no reason teaches the system nothing.
 */
export const POST = route(async (request: NextRequest, { params }: Params) => {
  const { id, action } = await params;
  const pool = db();

  const existing = await pool.query<{ id: string; format: string; asset_ids: string[] }>(
    'select id, format, asset_ids from posts where id = $1',
    [id],
  );
  const post = existing.rows[0];
  if (!post) return fail('No such post', 404);

  if (action === 'approve') {
    await pool.query(`update posts set status = 'approved' where id = $1`, [id]);

    // Spec section 5: approving queues the thing that builds the media.
    const job = post.format === 'reel' || post.format === 'short' ? 'render_reel' : 'build_post';
    await enqueue(pool, {
      type: job,
      payload: { post_id: id },
      priority: 3,
      dedupeKey: `${job}:${id}`,
    });

    return NextResponse.json({ status: 'approved', queued: job });
  }

  if (action === 'reject') {
    const body = (await request.json()) as { reason?: string };
    if (!body.reason || !(REJECT_REASONS as readonly string[]).includes(body.reason)) {
      return fail(`A rejection needs one of: ${REJECT_REASONS.join(', ')}`);
    }

    await pool.query(`update posts set status = 'rejected', reject_reason = $2 where id = $1`, [
      id,
      body.reason,
    ]);

    await enqueue(pool, {
      type: 'log_rejection',
      payload: { post_id: id, reason: body.reason },
      dedupeKey: `log_rejection:${id}:${body.reason}`,
    });

    return NextResponse.json({ status: 'rejected', reason: body.reason });
  }

  if (action === 'edit') {
    const body = (await request.json()) as {
      hook?: string;
      caption?: string;
      hashtags?: string[];
      ctaText?: string;
      ctaUrl?: string;
    };

    const client = await pool.connect();
    try {
      await client.query('begin');

      const version = await client.query<{ next: number }>(
        'select coalesce(max(version), 0) + 1 as next from post_versions where post_id = $1',
        [id],
      );

      await client.query(
        `insert into post_versions (post_id, version, author, caption, hook, hashtags, asset_ids)
         select $1, $2, 'human',
                coalesce($3, p.caption), coalesce($4, p.hook),
                coalesce($5::text[], p.hashtags), p.asset_ids
         from posts p where p.id = $1`,
        [id, version.rows[0]!.next, body.caption ?? null, body.hook ?? null, body.hashtags ?? null],
      );

      await client.query(
        `update posts
         set caption = coalesce($2, caption),
             hook = coalesce($3, hook),
             hashtags = coalesce($4::text[], hashtags),
             cta_text = coalesce($5, cta_text),
             cta_url = coalesce($6, cta_url)
         where id = $1`,
        [
          id,
          body.caption ?? null,
          body.hook ?? null,
          body.hashtags ?? null,
          body.ctaText ?? null,
          body.ctaUrl ?? null,
        ],
      );

      await client.query('commit');
    } catch (err) {
      await client.query('rollback');
      throw err;
    } finally {
      client.release();
    }

    // The diff between what the AI wrote and what the human kept is the
    // lesson. log_edit works it out.
    await enqueue(pool, {
      type: 'log_edit',
      payload: { post_id: id },
      dedupeKey: `log_edit:${id}:${Date.now()}`,
    });

    return NextResponse.json({ status: 'edited' });
  }

  return fail(`"${action}" is not something a post can do. Try approve, reject or edit.`);
});
