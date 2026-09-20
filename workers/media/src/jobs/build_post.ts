import sharp from 'sharp';
import { COLOURS, RATIOS } from '@sfw/brand';
import { handler } from '@sfw/queue';
import { getObject, keys, putObject, type Bucket } from '@sfw/storage';
import { db } from '../db.js';

/**
 * Builds the images a post goes out with.
 *
 * A feed post is one 4:5 image; a carousel is one per asset. Each is the photo
 * itself, filled to the frame and centred, on the deep green so a photo with
 * the wrong shape has a background rather than white bars.
 *
 * Deliberately restrained: CLAUDE.md section 5 says graphics are built on the
 * existing Canva templates with real photos swapped in, so this is the plain
 * crop-and-frame, and anything with type on it goes through Canva in Phase 7.
 *
 * Idempotent: writes `designs/{post_id}/{n}.png` every time.
 */
export const buildPost = handler<{ post_id: string }>(async ({ job, enqueue }) => {
  const pool = db();
  const postId = job.payload.post_id;

  const { rows } = await pool.query<{
    id: string;
    format: string;
    platform: string;
    asset_ids: string[];
  }>('select id, format, platform, asset_ids from posts where id = $1', [postId]);

  const post = rows[0];
  if (!post) throw new Error(`No post ${postId}`);
  if (post.asset_ids.length === 0) throw new Error(`Post ${postId} has no assets to build from`);

  // Stories and Reels are 9:16; everything else the builder makes is 4:5.
  const ratio = post.format === 'story' || post.format === 'reel' ? '9x16' : '4x5';
  const { width, height } = RATIOS[ratio];

  // A carousel gets every asset, anything else gets the first.
  const assetIds = post.format === 'carousel' ? post.asset_ids : post.asset_ids.slice(0, 1);

  const { rows: assets } = await pool.query<{
    id: string;
    bucket: Bucket;
    r2_key: string;
    thumb_key: string | null;
  }>(`select id, bucket, r2_key, thumb_key from assets where id = any($1::uuid[])`, [assetIds]);

  // Keep the order the post chose, not whatever the database returned.
  const ordered = assetIds
    .map((id) => assets.find((a) => a.id === id))
    .filter((a): a is NonNullable<typeof a> => Boolean(a));

  const built: string[] = [];

  for (const [index, asset] of ordered.entries()) {
    const source = await getObject(asset.bucket, asset.r2_key);

    const image = await sharp(source, { failOn: 'none' })
      .rotate() // Honour the EXIF orientation before cropping.
      .resize(width, height, {
        fit: 'cover',
        position: 'attention', // Crop towards whatever the photo is actually of.
        background: COLOURS.greenDeep,
      })
      .png({ compressionLevel: 9 })
      .toBuffer();

    const key = keys.design(postId, index + 1);
    await putObject('sfw-media', key, image, 'image/png');
    built.push(key);
  }

  console.log(`[build_post] ${built.length} image(s) for ${postId} at ${ratio}`);

  // Canva is off until Linnea's integration is approved; when it is on, the
  // built images are what gets pushed.
  const flags = (
    await pool.query<{ value: { canva_enabled?: boolean } }>(
      `select value from settings where key = 'flags'`,
    )
  ).rows[0]?.value;

  if (flags?.canva_enabled) {
    await enqueue({
      type: 'canva_push',
      payload: { post_id: postId, design_keys: built },
      dedupeKey: `canva_push:${postId}`,
    });
  }
});
