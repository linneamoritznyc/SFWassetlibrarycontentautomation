/**
 * Browser-side thumbnails, so a 4 GB video never has to be read by a server to
 * get a preview out of it. 800px on the long edge, JPEG at quality 0.82, which
 * is what the spec's storage layout asks for.
 */
const MAX_EDGE = 800;
const QUALITY = 0.82;

export type Measured = {
  blob: Blob | null;
  width: number | null;
  height: number | null;
  durationS: number | null;
};

export async function makeThumbnail(file: File): Promise<Measured> {
  if (file.type.startsWith('image/')) return fromImage(file);
  if (file.type.startsWith('video/')) return fromVideo(file);
  return { blob: null, width: null, height: null, durationS: null };
}

async function fromImage(file: File): Promise<Measured> {
  const url = URL.createObjectURL(file);
  try {
    const image = await loadImage(url);
    const blob = await draw(image, image.naturalWidth, image.naturalHeight);
    return { blob, width: image.naturalWidth, height: image.naturalHeight, durationS: null };
  } finally {
    URL.revokeObjectURL(url);
  }
}

/** A frame at two seconds, which is usually past the slate and into the shot. */
async function fromVideo(file: File): Promise<Measured> {
  const url = URL.createObjectURL(file);
  const video = document.createElement('video');
  video.preload = 'metadata';
  video.muted = true;
  video.src = url;

  try {
    await once(video, 'loadedmetadata');
    const duration = Number.isFinite(video.duration) ? video.duration : null;

    video.currentTime = Math.min(2, duration ? duration / 2 : 2);
    await once(video, 'seeked');

    const blob = await draw(video, video.videoWidth, video.videoHeight);
    return { blob, width: video.videoWidth, height: video.videoHeight, durationS: duration };
  } catch {
    // A codec the browser cannot decode is not a failure worth stopping for:
    // the asset uploads without a thumbnail and the media worker makes one.
    return { blob: null, width: null, height: null, durationS: null };
  } finally {
    URL.revokeObjectURL(url);
  }
}

async function draw(
  source: CanvasImageSource,
  width: number,
  height: number,
): Promise<Blob | null> {
  if (!width || !height) return null;

  const scale = Math.min(1, MAX_EDGE / Math.max(width, height));
  const canvas = document.createElement('canvas');
  canvas.width = Math.round(width * scale);
  canvas.height = Math.round(height * scale);

  const context = canvas.getContext('2d');
  if (!context) return null;
  context.drawImage(source, 0, 0, canvas.width, canvas.height);

  return new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg', QUALITY));
}

function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error('Could not read that image'));
    image.src = src;
  });
}

function once(element: HTMLElement, event: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`${event} never happened`)), 15_000);
    element.addEventListener(
      event,
      () => {
        clearTimeout(timer);
        resolve();
      },
      { once: true },
    );
    element.addEventListener(
      'error',
      () => {
        clearTimeout(timer);
        reject(new Error('Could not read that file'));
      },
      { once: true },
    );
  });
}

/** photo | video | graphic | doc | reference, from the file itself. */
export function assetTypeFor(file: File): string {
  if (file.type.startsWith('video/')) return 'video';
  if (file.type === 'application/pdf') return 'doc';
  if (file.type === 'image/png' || file.type === 'image/svg+xml') return 'graphic';
  if (file.type.startsWith('image/')) return 'photo';
  return 'reference';
}
