/**
 * The R2 layout from backend spec section 3. Every key in the system is built
 * here, so the layout is described in one place and a typo cannot invent a new
 * folder.
 *
 *   sfw-raw/
 *     originals/{asset_id}/{filename}
 *   sfw-media/
 *     thumbs/{asset_id}.jpg
 *     proxies/{asset_id}.mp4
 *     audio/{asset_id}.m4a
 *     clips/{clip_id}/{ratio}.mp4
 *     clips/{clip_id}/captions.srt
 *     renders/{render_id}.mp4
 *     designs/{post_id}/{n}.png
 *     docs/{doc_id}/{filename}
 */

export const BUCKETS = {
  /** Originals and video. Infrequent Access. */
  raw: 'sfw-raw',
  /** Everything derived, plus documents. Standard. */
  media: 'sfw-media',
} as const;

export type Bucket = (typeof BUCKETS)[keyof typeof BUCKETS];

/**
 * Strips anything that would make a key awkward: path separators, control
 * characters, leading dots. Keeps the extension.
 */
export function safeFilename(filename: string): string {
  const cleaned = filename
    .replace(/[\\/]+/g, '_')
    // eslint-disable-next-line no-control-regex
    .replace(/[\u0000-\u001f\u007f]/g, '')
    .replace(/^\.+/, '')
    .trim();
  return cleaned.slice(0, 200) || 'file';
}

export const keys = {
  original: (assetId: string, filename: string) => `originals/${assetId}/${safeFilename(filename)}`,
  thumb: (assetId: string) => `thumbs/${assetId}.jpg`,
  proxy: (assetId: string) => `proxies/${assetId}.mp4`,
  audio: (assetId: string) => `audio/${assetId}.m4a`,
  clip: (clipId: string, ratio: string) => `clips/${clipId}/${ratio}.mp4`,
  captions: (clipId: string) => `clips/${clipId}/captions.srt`,
  render: (renderId: string) => `renders/${renderId}.mp4`,
  design: (postId: string, n: number) => `designs/${postId}/${n}.png`,
  doc: (docId: string, filename: string) => `docs/${docId}/${safeFilename(filename)}`,
};

/**
 * Where an upload goes. Video originals are large and rarely read, so they go
 * to the Infrequent Access bucket; everything else goes to Standard.
 */
export function bucketForType(type: string): Bucket {
  return type === 'video' ? BUCKETS.raw : BUCKETS.media;
}

/** The object key for a newly uploaded original of any type. */
export function originalKey(type: string, assetId: string, filename: string): string {
  if (type === 'doc') return keys.doc(assetId, filename);
  if (type === 'video') return keys.original(assetId, filename);
  return keys.original(assetId, filename);
}
