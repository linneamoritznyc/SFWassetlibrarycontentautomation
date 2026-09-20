import { randomUUID } from 'node:crypto';
import { handler } from '@sfw/queue';
import { keys, putObject } from '@sfw/storage';
import { accessToken, canvaEnabled, canvaFetch } from '@sfw/shared/canva';
import { db } from '../db.js';

/**
 * Brings a finished Canva design back into the library as an asset.
 *
 * The export is a job on Canva's side too, so this polls for it, then fetches
 * the file from the URL Canva returns and puts it in R2. The new asset is a
 * `render` pointing at the post, so the design that actually went out is the
 * one on file rather than whatever the original photo was.
 */
export const canvaPull = handler<{ post_id: string; design_id?: string }>(
  async ({ job, enqueue }) => {
    const pool = db();
    const postId = job.payload.post_id;

    if (!(await canvaEnabled(pool))) {
      console.log('[canva_pull] Canva is switched off in settings, skipping');
      return;
    }

    const token = await accessToken(pool);
    if (!token) throw new Error('Canva has never been connected. Visit /api/canva/auth first.');

    const designId =
      job.payload.design_id ??
      (
        await pool.query<{ canva_design_id: string }>(
          `select canva_design_id from canva_links where post_id = $1 order by created_at desc limit 1`,
          [postId],
        )
      ).rows[0]?.canva_design_id;

    if (!designId) throw new Error(`No Canva design for post ${postId}`);

    const started = await canvaFetch<{ job: { id: string } }>(token, '/exports', {
      method: 'POST',
      body: JSON.stringify({ design_id: designId, format: { type: 'png' } }),
    });

    const urls = await waitForExport(token, started.job.id);
    const assetIds: string[] = [];

    for (const [index, url] of urls.entries()) {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Could not download the Canva export (${res.status})`);

      const bytes = Buffer.from(await res.arrayBuffer());
      const assetId = randomUUID();
      const key = keys.design(postId, index + 1);

      await putObject('sfw-media', key, bytes, 'image/png');

      await pool.query(
        `insert into assets (id, type, filename, bucket, r2_key, status, description, notes)
       values ($1, 'render', $2, 'sfw-media', $3, 'cleared', $4, $5)`,
        [
          assetId,
          `canva-${designId.slice(0, 8)}-${index + 1}.png`,
          key,
          'Finished in Canva.',
          `Exported from Canva design ${designId}.`,
        ],
      );

      assetIds.push(assetId);
    }

    if (assetIds.length > 0) {
      // The post now points at what actually goes out.
      await pool.query('update posts set asset_ids = $2::uuid[] where id = $1', [postId, assetIds]);

      await pool.query(
        `update canva_links set status = 'exported', exported_asset_id = $2
       where post_id = $1 and canva_design_id = $3`,
        [postId, assetIds[0], designId],
      );

      for (const id of assetIds) {
        await enqueue({ type: 'embed', payload: { asset_id: id }, dedupeKey: `embed:${id}` });
      }
    }

    console.log(`[canva_pull] ${assetIds.length} design(s) back from Canva for ${postId}`);
  },
);

async function waitForExport(token: string, jobId: string): Promise<string[]> {
  for (let attempt = 0; attempt < 40; attempt += 1) {
    const status = await canvaFetch<{
      job: { status: string; urls?: string[]; error?: { message: string } };
    }>(token, `/exports/${jobId}`);

    if (status.job.status === 'success') return status.job.urls ?? [];
    if (status.job.status === 'failed') {
      throw new Error(`Canva export failed: ${status.job.error?.message ?? 'no reason given'}`);
    }

    await new Promise((resolve) => setTimeout(resolve, 1500));
  }

  throw new Error('Canva export did not finish in a minute');
}
