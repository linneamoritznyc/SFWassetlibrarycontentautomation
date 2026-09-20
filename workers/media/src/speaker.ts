import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { run } from './ffmpeg.js';

export type Sample = { t: number; x: number | null; confidence: number };
export type Track = { width: number; height: number; fps: number; samples: Sample[] };

/** How far the crop may travel in a second, as a share of the frame width. */
const MAX_PAN_PER_SECOND = 0.25;

/** Ignore a jump smaller than this; it is jitter, not the speaker moving. */
const DEADZONE = 0.02;

/**
 * Following the speaker instead of taking the middle.
 *
 * A centre crop loses whoever is standing off to one side, which in workshop
 * footage is most of the time. This samples where the face is twice a second,
 * smooths the result hard, and turns it into a crop that drifts rather than
 * chases: a crop that snaps to every detection is unwatchable, and worse than
 * the centre crop it replaced.
 */
export async function trackSpeaker(
  video: string,
  options: { startS: number; durationS: number; everyS?: number },
): Promise<Track | null> {
  const script = join(dirname(fileURLToPath(import.meta.url)), '../python/face_track.py');

  try {
    const output = await run(process.env.PYTHON_PATH ?? 'python3', [
      script,
      video,
      '--start',
      String(options.startS),
      '--duration',
      String(options.durationS),
      '--every',
      String(options.everyS ?? 0.5),
    ]);

    return JSON.parse(output) as Track;
  } catch (err) {
    // No Python, no OpenCV, or a video it cannot open. The caller falls back
    // to the centre crop, which is what the clip would have got anyway.
    console.warn('[speaker] could not track, falling back to the centre crop:', err);
    return null;
  }
}

/**
 * Turns raw detections into a crop track.
 *
 * Three passes: carry the last known position through frames with no face,
 * average over a window, then limit how fast the crop may move. The order
 * matters. Smoothing before filling would average a null; limiting before
 * smoothing would ratchet.
 */
export function smooth(track: Track, cropWidth: number): { t: number; x: number }[] {
  const maxX = Math.max(0, track.width - cropWidth);
  const centre = maxX / 2;

  // 1. Fill the gaps. A frame with no face holds the last known position.
  const filled: number[] = [];
  let last = centre + cropWidth / 2;

  for (const sample of track.samples) {
    if (sample.x !== null) last = sample.x;
    filled.push(last);
  }

  if (filled.length === 0) return [{ t: 0, x: centre }];

  // 2. Average over a window either side, so one bad detection cannot yank it.
  const window = 3;
  const averaged = filled.map((_, i) => {
    const from = Math.max(0, i - window);
    const to = Math.min(filled.length, i + window + 1);
    const slice = filled.slice(from, to);
    return slice.reduce((a, b) => a + b, 0) / slice.length;
  });

  // 3. Limit the speed, and ignore anything inside the deadzone.
  const everyS = track.samples[1] ? track.samples[1].t - track.samples[0]!.t : 0.5;
  const maxStep = track.width * MAX_PAN_PER_SECOND * everyS;
  const deadzone = track.width * DEADZONE;

  const out: { t: number; x: number }[] = [];
  let current = clamp(averaged[0]! - cropWidth / 2, 0, maxX);

  for (const [i, target] of averaged.entries()) {
    const wanted = clamp(target - cropWidth / 2, 0, maxX);
    const delta = wanted - current;

    if (Math.abs(delta) > deadzone) {
      current = clamp(current + Math.sign(delta) * Math.min(Math.abs(delta), maxStep), 0, maxX);
    }

    out.push({ t: track.samples[i]?.t ?? i * everyS, x: Math.round(current) });
  }

  return out;
}

/**
 * The crop x as an ffmpeg expression.
 *
 * Steps rather than interpolation, because ffmpeg expressions get unreadable
 * fast and a step every half second under a deadzone is not visible. Points
 * where nothing changed are dropped, so a static shot compiles to a constant.
 */
export function cropExpression(points: { t: number; x: number }[], startS: number): string {
  if (points.length === 0) return '0';

  const kept: { t: number; x: number }[] = [];
  for (const point of points) {
    const previous = kept[kept.length - 1];
    if (!previous || Math.abs(point.x - previous.x) >= 2) kept.push(point);
  }

  if (kept.length === 1) return String(kept[0]!.x);

  // Built from the end backwards: if(lt(t,t1), x0, if(lt(t,t2), x1, ...)).
  let expression = String(kept[kept.length - 1]!.x);

  for (let i = kept.length - 1; i > 0; i -= 1) {
    // Times are relative to the clip, and the clip starts at zero.
    const at = (kept[i]!.t - startS).toFixed(2);
    expression = `if(lt(t,${at}),${kept[i - 1]!.x},${expression})`;
  }

  return expression;
}

function clamp(value: number, low: number, high: number): number {
  return Math.min(Math.max(value, low), high);
}
