import { describe, expect, it } from 'vitest';
import { cropExpression, smooth, type Track } from './speaker.js';

const track = (xs: (number | null)[], width = 1920): Track => ({
  width,
  height: 1080,
  fps: 25,
  samples: xs.map((x, i) => ({ t: i * 0.5, x, confidence: x === null ? 0 : 0.1 })),
});

/** A 9:16 crop out of a 1920-wide frame is 607 pixels. */
const CROP = 607;

describe('smoothing a face track', () => {
  it('centres on the speaker when they stand still', () => {
    const points = smooth(track([960, 960, 960, 960, 960, 960, 960, 960]), CROP);
    const expected = 960 - CROP / 2;
    expect(points[points.length - 1]!.x).toBeCloseTo(expected, -1);
  });

  it('holds the last known position through frames with no face', () => {
    // Someone turns away, then turns back.
    const points = smooth(track([1400, 1400, null, null, null, 1400, 1400, 1400]), CROP);
    const xs = points.map((p) => p.x);
    expect(Math.max(...xs) - Math.min(...xs)).toBeLessThan(120);
  });

  it('never crops outside the frame', () => {
    const points = smooth(track([0, 0, 1920, 1920, 0, 0, 1919, 1919]), CROP);
    for (const point of points) {
      expect(point.x).toBeGreaterThanOrEqual(0);
      expect(point.x).toBeLessThanOrEqual(1920 - CROP);
    }
  });

  it('drifts rather than chasing, so the crop is watchable', () => {
    // A hard cut from one side to the other.
    const points = smooth(track([200, 200, 200, 1700, 1700, 1700, 1700, 1700]), CROP);

    for (let i = 1; i < points.length; i += 1) {
      const step = Math.abs(points[i]!.x - points[i - 1]!.x);
      // A quarter of the frame per second, sampled twice a second.
      expect(step).toBeLessThanOrEqual(1920 * 0.25 * 0.5 + 1);
    }
  });

  it('ignores jitter inside the deadzone', () => {
    // Detections wobbling by twenty pixels around one spot.
    const points = smooth(track([960, 975, 950, 968, 955, 962, 958, 965]), CROP);
    const xs = points.map((p) => p.x);
    expect(Math.max(...xs) - Math.min(...xs)).toBeLessThan(20);
  });

  it('falls back to the centre when no face is ever found', () => {
    const points = smooth(track([null, null, null, null]), CROP);
    const centre = (1920 - CROP) / 2;
    for (const point of points) expect(point.x).toBeCloseTo(centre, -1);
  });

  it('returns something usable for an empty track', () => {
    const points = smooth({ width: 1920, height: 1080, fps: 25, samples: [] }, CROP);
    expect(points).toHaveLength(1);
    expect(points[0]!.x).toBe((1920 - CROP) / 2);
  });
});

describe('the ffmpeg crop expression', () => {
  it('compiles a static shot to a constant', () => {
    expect(
      cropExpression(
        [
          { t: 0, x: 656 },
          { t: 0.5, x: 656 },
          { t: 1, x: 657 },
        ],
        0,
      ),
    ).toBe('656');
  });

  it('steps at the right times, relative to the start of the clip', () => {
    const expression = cropExpression(
      [
        { t: 10, x: 100 },
        { t: 10.5, x: 300 },
      ],
      10,
    );
    // Before 0.5s into the clip, 100; after, 300.
    expect(expression).toBe('if(lt(t,0.50),100,300)');
  });

  it('nests in time order', () => {
    const expression = cropExpression(
      [
        { t: 0, x: 0 },
        { t: 0.5, x: 200 },
        { t: 1, x: 400 },
      ],
      0,
    );
    expect(expression).toBe('if(lt(t,0.50),0,if(lt(t,1.00),200,400))');
  });

  it('handles an empty track', () => {
    expect(cropExpression([], 0)).toBe('0');
  });
});
