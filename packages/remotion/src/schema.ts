import { z } from 'zod';

/**
 * What a Reel render is given.
 *
 * Deliberately flat and serialisable: these props travel from a job payload in
 * Postgres, through the renderer's command line, into React. Anything that
 * cannot survive JSON does not belong here.
 */

export const clipSchema = z.object({
  /** A presigned URL the renderer can fetch. */
  src: z.string(),
  durationS: z.number().positive(),
  /** Burned-in captions are already in the clip; this is the on-screen line. */
  label: z.string().optional(),
});

export const fieldNotesSchema = z.object({
  /** "FIELD NOTES No. 01" */
  eyebrow: z.string(),
  title: z.string(),
  /** Who, where, when. The named person, place and season the series needs. */
  subtitle: z.string(),
  clips: z.array(clipSchema),
  endCard: z.string(),
  ctaUrl: z.string(),
});

export const workshopMomentSchema = z.object({
  hook: z.string(),
  speaker: z.string().optional(),
  place: z.string().optional(),
  clips: z.array(clipSchema),
  endCard: z.string(),
  ctaUrl: z.string(),
});

export type FieldNotesProps = z.infer<typeof fieldNotesSchema>;
export type WorkshopMomentProps = z.infer<typeof workshopMomentSchema>;

export const FPS = 30;

/** Reels are 9:16. */
export const FRAME = { width: 1080, height: 1920 } as const;

/** How long the intro and end cards hold, in seconds. */
export const INTRO_SECONDS = 2.5;
export const END_SECONDS = 2.5;

/** Total frames for a set of clips plus the cards either side. */
export function totalFrames(clips: { durationS: number }[]): number {
  const clipSeconds = clips.reduce((total, clip) => total + clip.durationS, 0);
  return Math.round((INTRO_SECONDS + clipSeconds + END_SECONDS) * FPS);
}
