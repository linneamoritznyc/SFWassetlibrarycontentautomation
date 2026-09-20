import JSZip from 'jszip';
import { handler } from '@sfw/queue';
import { getObject, putObject, type Bucket } from '@sfw/storage';
import { db } from '../db.js';

/**
 * Packs approved posts into a ZIP that can be dropped into Later.
 *
 * One folder per post: the media, `caption.txt` with the caption and hashtags
 * exactly as they should be pasted, and `meta.json` with the time, platform,
 * collaborators and the UTM link. The Later API path replaces this when there
 * is access; until then this is the handover, and it is deliberately something
 * a human can open and check.
 */
export const exportBundle = handler<{ post_ids?: string[] }>(async ({ job, enqueue }) => {
  const pool = db();

  const { rows: posts } = await pool.query<{
    id: string;
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
    asset_ids: string[];
    angle: string | null;
  }>(
    `select p.id, p.slot_date::text, p.slot_time::text, p.platform, p.format,
            p.hook, p.caption, p.hashtags, p.cta_text, p.cta_url, p.collaborators,
            p.asset_ids, s.angle
     from posts p left join stories s on s.id = p.story_id
     where p.status = 'approved'
       ${job.payload.post_ids?.length ? 'and p.id = any($1::uuid[])' : ''}
     order by p.slot_date nulls last, p.slot_time nulls last`,
    job.payload.post_ids?.length ? [job.payload.post_ids] : [],
  );

  if (posts.length === 0) {
    console.log('[export_bundle] nothing approved to export');
    return;
  }

  const zip = new JSZip();
  const index: Record<string, unknown>[] = [];

  for (const post of posts) {
    const folder = `${post.slot_date ?? 'undated'}-${post.platform}-${post.format}-${post.id.slice(0, 8)}`;
    const dir = zip.folder(folder)!;

    const utm = withUtm(post.cta_url, post.platform, post.slot_date);

    const caption = [
      post.caption ?? '',
      '',
      post.hashtags.join(' '),
      post.collaborators.length ? `\nCollab: ${post.collaborators.join(', ')}` : '',
    ]
      .join('\n')
      .trim();

    dir.file('caption.txt', `${caption}\n`);

    dir.file(
      'meta.json',
      JSON.stringify(
        {
          post_id: post.id,
          when:
            post.slot_date && post.slot_time
              ? `${post.slot_date}T${post.slot_time}`
              : post.slot_date,
          platform: post.platform,
          format: post.format,
          hook: post.hook,
          hashtags: post.hashtags,
          collaborators: post.collaborators,
          cta_text: post.cta_text,
          link: utm,
          why: post.angle,
        },
        null,
        2,
      ),
    );

    const { rows: assets } = await pool.query<{
      id: string;
      filename: string;
      bucket: Bucket;
      r2_key: string;
    }>(`select id, filename, bucket, r2_key from assets where id = any($1::uuid[])`, [
      post.asset_ids,
    ]);

    for (const [i, asset] of assets.entries()) {
      try {
        const bytes = await getObject(asset.bucket, asset.r2_key);
        dir.file(`${String(i + 1).padStart(2, '0')}-${asset.filename}`, bytes);
      } catch (err) {
        // A missing file should not lose the whole bundle. Say so in the zip.
        dir.file(
          `${String(i + 1).padStart(2, '0')}-MISSING.txt`,
          `${asset.r2_key}\n${String(err)}\n`,
        );
      }
    }

    index.push({ folder, post_id: post.id, when: post.slot_date, platform: post.platform });
  }

  zip.file(
    'index.json',
    JSON.stringify({ exported_at: new Date().toISOString(), posts: index }, null, 2),
  );

  const bytes = await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' });
  const key = `docs/exports/${new Date().toISOString().slice(0, 10)}-${Date.now()}.zip`;
  await putObject('sfw-media', key, bytes, 'application/zip');

  await pool.query(
    `update posts set status = 'exported' where id = any($1::uuid[]) and status = 'approved'`,
    [posts.map((p) => p.id)],
  );

  for (const post of posts) {
    await enqueue({
      type: 'link_asset_usage',
      payload: { post_id: post.id },
      dedupeKey: `link_asset_usage:${post.id}`,
    });
  }

  console.log(`[export_bundle] ${posts.length} post(s) into ${key}`);
});

/**
 * Every link in a post gets a UTM (CLAUDE.md section 10). Anything already
 * tagged is left alone, because someone added it on purpose.
 */
export function withUtm(url: string | null, platform: string, date: string | null): string | null {
  if (!url) return null;

  try {
    const parsed = new URL(url);
    if (parsed.searchParams.has('utm_source')) return parsed.toString();

    parsed.searchParams.set('utm_source', platform);
    parsed.searchParams.set('utm_medium', 'social');
    parsed.searchParams.set('utm_campaign', date ? date.slice(0, 7) : 'organic');
    return parsed.toString();
  } catch {
    // Not a URL. Hand it back untouched rather than losing it.
    return url;
  }
}
