import { handler } from '@sfw/queue';
import { presignGet, type Bucket } from '@sfw/storage';
import { accessToken, canvaEnabled, canvaFetch } from '@sfw/shared/canva';
import { db } from '../db.js';

/**
 * Sends a post's images into Canva and creates a design from them.
 *
 * Upload by URL rather than by bytes: R2 already has the file and can hand out
 * a presigned link, so the asset never passes through this worker.
 *
 * Autofill stays behind its own flag until Canva approves that scope. Without
 * it, this creates a plain Instagram-sized design holding the image, which is
 * still the useful part: Linnea opens the edit URL and finishes it on the
 * existing templates.
 */
export const canvaPush = handler<{ post_id: string; design_keys?: string[] }>(async ({ job }) => {
  const pool = db();
  const postId = job.payload.post_id;

  if (!(await canvaEnabled(pool))) {
    console.log('[canva_push] Canva is switched off in settings, skipping');
    return;
  }

  const token = await accessToken(pool);
  if (!token) {
    console.log('[canva_push] Canva has never been connected. Visit /api/canva/auth first.');
    return;
  }

  const { rows } = await pool.query<{ hook: string | null; asset_ids: string[] }>(
    'select hook, asset_ids from posts where id = $1',
    [postId],
  );
  const post = rows[0];
  if (!post) throw new Error(`No post ${postId}`);

  // Prefer what build_post made; fall back to the originals.
  const sources: { key: string; bucket: Bucket }[] = job.payload.design_keys?.length
    ? job.payload.design_keys.map((key) => ({ key, bucket: 'sfw-media' as Bucket }))
    : (
        await pool.query<{ r2_key: string; bucket: Bucket }>(
          `select r2_key, bucket from assets where id = any($1::uuid[])`,
          [post.asset_ids],
        )
      ).rows.map((r) => ({ key: r.r2_key, bucket: r.bucket }));

  if (sources.length === 0) throw new Error(`Post ${postId} has nothing to send to Canva`);

  const folderId = await ensureFolder(token);
  const assetIds: string[] = [];

  for (const source of sources) {
    const url = await presignGet(source.bucket, source.key);

    const upload = await canvaFetch<{ job: { id: string } }>(token, '/asset-uploads', {
      method: 'POST',
      body: JSON.stringify({
        name_base64: Buffer.from(post.hook?.slice(0, 50) ?? 'SFW post').toString('base64'),
        url,
        parent_folder_id: folderId,
      }),
    });

    const asset = await waitForUpload(token, upload.job.id);
    if (asset) assetIds.push(asset);
  }

  if (assetIds.length === 0) throw new Error('Canva accepted no assets');

  const design = await canvaFetch<{ design: { id: string; urls: { edit_url: string } } }>(
    token,
    '/designs',
    {
      method: 'POST',
      body: JSON.stringify({
        design_type: { type: 'preset', name: 'instagram_post' },
        asset_id: assetIds[0],
        title: post.hook?.slice(0, 80) ?? 'SFW post',
      }),
    },
  );

  await pool.query(
    `insert into canva_links (post_id, canva_design_id, edit_url, status)
     values ($1, $2, $3, 'created')
     on conflict (post_id, canva_design_id) do update set edit_url = excluded.edit_url`,
    [postId, design.design.id, design.design.urls.edit_url],
  );

  console.log(`[canva_push] ${postId} -> ${design.design.urls.edit_url}`);
});

/** One folder for everything this system sends, created once. */
async function ensureFolder(token: string): Promise<string | undefined> {
  const existing = process.env.CANVA_FOLDER_ID;
  if (existing) return existing;

  try {
    const folder = await canvaFetch<{ folder: { id: string } }>(token, '/folders', {
      method: 'POST',
      body: JSON.stringify({ name: 'SFW Content Studio', parent_folder_id: 'root' }),
    });
    return folder.folder.id;
  } catch (err) {
    // Not worth failing the push over: without a folder the asset lands in
    // Uploads, which still works.
    console.warn('[canva_push] could not create the folder:', err);
    return undefined;
  }
}

/** Canva uploads are a job; poll until it finishes. */
async function waitForUpload(token: string, jobId: string): Promise<string | null> {
  for (let attempt = 0; attempt < 20; attempt += 1) {
    const status = await canvaFetch<{
      job: { status: string; asset?: { id: string }; error?: { message: string } };
    }>(token, `/asset-uploads/${jobId}`);

    if (status.job.status === 'success') return status.job.asset?.id ?? null;
    if (status.job.status === 'failed') {
      throw new Error(`Canva upload failed: ${status.job.error?.message ?? 'no reason given'}`);
    }

    await new Promise((resolve) => setTimeout(resolve, 1500));
  }

  throw new Error('Canva upload did not finish in 30 seconds');
}
