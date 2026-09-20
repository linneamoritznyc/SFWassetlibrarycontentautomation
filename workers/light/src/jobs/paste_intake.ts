import { callClaude, pasteIntakeSchema } from '@sfw/ai';
import { handler } from '@sfw/queue';
import { getObject, type Bucket } from '@sfw/storage';
import { db } from '../db.js';

const MEDIA_TYPES: Record<string, 'image/jpeg' | 'image/png' | 'image/webp' | 'image/gif'> = {
  jpg: 'image/jpeg',
  jpeg: 'image/jpeg',
  png: 'image/png',
  webp: 'image/webp',
  gif: 'image/gif',
};

/**
 * Reads a pasted screenshot.
 *
 * Someone pastes a Google Chat message, an email or an article into the inbox.
 * Claude reads the image and pulls out who sent it, what they said and the
 * links in it. Each link becomes a `web_fetch` job, which turns into sourced
 * facts, which is what lets a draft cite the thing rather than paraphrase a
 * screenshot.
 *
 * The screenshot itself is stored as a `reference` asset: provenance, never a
 * post visual. See docs/paste-intake.md.
 */
export const pasteIntake = handler<{ asset_id: string }>(async ({ job, enqueue }) => {
  const pool = db();
  const assetId = job.payload.asset_id;

  const { rows } = await pool.query<{
    id: string;
    filename: string;
    bucket: Bucket;
    r2_key: string;
    thumb_key: string | null;
  }>('select id, filename, bucket, r2_key, thumb_key from assets where id = $1', [assetId]);

  const asset = rows[0];
  if (!asset) throw new Error(`No asset ${assetId}`);

  const ext = asset.filename.split('.').pop()?.toLowerCase() ?? '';
  const image = asset.thumb_key
    ? { data: await getObject('sfw-media', asset.thumb_key), mediaType: 'image/jpeg' as const }
    : MEDIA_TYPES[ext]
      ? { data: await getObject(asset.bucket, asset.r2_key), mediaType: MEDIA_TYPES[ext]! }
      : null;

  if (!image) throw new Error(`Pasted asset ${assetId} is not an image this can read`);

  const result = await callClaude({
    pool,
    jobId: job.id,
    prompt: 'paste_intake',
    schema: pasteIntakeSchema,
    images: [{ mediaType: image.mediaType, data: image.data, label: 'The pasted screenshot:' }],
    input: `Filename: ${asset.filename}`,
  });

  const summary = [
    result.sender ? `From ${result.sender}${result.sent_at ? ` at ${result.sent_at}` : ''}.` : '',
    result.message_text ? `"${result.message_text}"` : '',
    result.link_preview_title
      ? `Links to "${result.link_preview_title}"${result.link_preview_source ? ` (${result.link_preview_source})` : ''}.`
      : '',
    result.image_description ? `The screenshot shows: ${result.image_description}` : '',
  ]
    .filter(Boolean)
    .join(' ');

  const notes = [
    result.note,
    result.sensitive ? 'Flagged as sensitive on read. Check before this goes anywhere.' : '',
    result.is_sfw_material
      ? ''
      : 'Not SFW material: this image is provenance only and must not be used as a post visual.',
    result.unreadable_urls.length
      ? `Could not read these links with confidence: ${result.unreadable_urls.join(', ')}`
      : '',
  ]
    .filter(Boolean)
    .join('\n');

  await pool.query(
    `update assets
     set description = coalesce(description, $2),
         notes = coalesce(nullif(notes, ''), nullif($3, '')),
         credit_line = coalesce(credit_line, nullif($4, '')),
         status = case when status = 'inbox' then 'tagged' else status end
     where id = $1`,
    [assetId, summary || 'A pasted screenshot.', notes, result.sender],
  );

  for (const url of unique(result.urls)) {
    if (!isHttpUrl(url)) continue;
    await enqueue({
      type: 'web_fetch',
      payload: { url, from_asset_id: assetId },
      dedupeKey: `web_fetch:${url}`,
    });
  }
});

function unique(values: string[]): string[] {
  return [...new Set(values.map((v) => v.trim()).filter(Boolean))];
}

function isHttpUrl(value: string): boolean {
  try {
    const url = new URL(value);
    return url.protocol === 'http:' || url.protocol === 'https:';
  } catch {
    return false;
  }
}
