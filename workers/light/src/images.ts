import type { ImageInput } from '@sfw/ai';
import { getObject } from '@sfw/storage';
import type { BriefAsset } from './brief.js';

/** Claude sees thumbnails, never originals. Backend spec section 9. */
const MAX_IMAGES = 6;

export async function thumbnailsFor(assets: BriefAsset[]): Promise<ImageInput[]> {
  const images: ImageInput[] = [];

  for (const asset of assets.slice(0, MAX_IMAGES)) {
    if (!asset.thumb_key) continue;
    try {
      images.push({
        mediaType: 'image/jpeg',
        data: await getObject('sfw-media', asset.thumb_key),
        label: `Image ${images.length + 1} (asset ${asset.id}): ${asset.description ?? 'no description'}`,
      });
    } catch (err) {
      // A missing thumbnail should not stop a post being written; the critic
      // will notice the caption does not match anything.
      console.warn(`[images] could not load thumbnail for ${asset.id}:`, err);
    }
  }

  return images;
}
