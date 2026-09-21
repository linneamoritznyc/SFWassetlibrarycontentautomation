/**
 * Brand tokens from CLAUDE.md section 5. One place, used by the caption
 * burner in `workers/media`, the image builder in `build_post`, the Remotion
 * templates and the web app's Tailwind config.
 *
 * Greens and cream. Cream works as a shape; the background stays green or
 * photographic. Gold is donate CTAs only. Purple is Dr. Elaine memorial
 * content only. One shadow value.
 */

export const COLOURS = {
  greenDeep: '#1d3b2a',
  greenMid: '#2f6b46',
  greenBright: '#4c9a68',
  cream: '#f4efe4',
  /** Donate CTAs only. */
  gold: '#c8963e',
  /** Dr. Elaine memorial content only. */
  elaine: '#6b4f8a',
  white: '#ffffff',
  black: '#000000',
} as const;

/** The single shadow value. */
export const SHADOW = '0 2px 8px rgba(29, 59, 42, 0.12)';

export const FONTS = {
  /**
   * Montserrat 600 for burned-in captions, per the spec. The face itself is
   * checked in at `packages/brand/fonts/Montserrat-SemiBold.ttf` (Open Font
   * License, `OFL-Montserrat.txt` beside it), so the media worker points
   * libass straight at it and the two Docker images copy it in for fontconfig.
   *
   * This is the face's own name, not the family's. libass matches a static
   * font by its family name, which for a single-weight file is "Montserrat
   * SemiBold", and fontconfig and Chromium answer to it too. Asking for plain
   * "Montserrat" finds nothing and quietly falls back to DejaVu.
   *
   * The fallbacks are there so a run with no font at all still produces a
   * legible clip rather than failing.
   */
  caption: 'Montserrat SemiBold',
  captionWeight: 600,
  captionFallbacks: ['DejaVu Sans', 'Liberation Sans', 'sans-serif'],
} as const;

/**
 * Burned-in caption style. Sizes are for a 1080-wide frame and are scaled to
 * whatever the real frame is.
 */
export const CAPTION_STYLE = {
  fontSize: 64,
  /** Never more than two lines on screen, per the spec. */
  maxLines: 2,
  /** Roughly how many characters fit on one line at this size. */
  charsPerLine: 26,
  /** Colour of everything except the word being spoken. */
  text: COLOURS.cream,
  /** The word being spoken right now. */
  highlight: COLOURS.greenBright,
  outline: COLOURS.greenDeep,
  outlineWidth: 4,
  shadowDepth: 2,
  /** Distance from the bottom of the frame, as a share of frame height. */
  marginBottomRatio: 0.16,
} as const;

/** Loudness target for anything with audio. */
export const LOUDNESS = { integrated: -14, truePeak: -1.5, range: 11 } as const;

/** Frame sizes per ratio, at the resolution clips are delivered in. */
export const RATIOS = {
  '9x16': { width: 1080, height: 1920 },
  '4x5': { width: 1080, height: 1350 },
  '1x1': { width: 1080, height: 1080 },
  '16x9': { width: 1920, height: 1080 },
} as const;

export type Ratio = keyof typeof RATIOS;

/** The hashtag anchors, so a caption builder never has to hardcode them. */
export const ANCHOR_HASHTAGS = [
  '#SoilFoodWeb',
  '#LivingSoil',
  '#SoilHealth',
  '#SoilBiology',
  '#RegenerativeAgriculture',
] as const;
