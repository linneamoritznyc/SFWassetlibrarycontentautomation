/**
 * Cadence from CLAUDE.md section 7 and the planner inputs in backend spec
 * section 6. The planner reads this to work out how many slots a week has and
 * what shape each one is.
 */

export type Cadence = {
  /** Feed posts land on these days. */
  feedDays: ('mon' | 'tue' | 'wed' | 'thu' | 'fri' | 'sat' | 'sun')[];
  storiesPerWeek: [number, number];
  shortsPerWeek: number;
  linkedinPerWeek: [number, number];
  /** Local to the target audience, from CLAUDE.md section 7. */
  postingWindows: [string, string][];
  /** Share of slots held back for formats or topics with under 3 data points. */
  explorationShare: number;
};

export const CADENCE: Cadence = {
  feedDays: ['mon', 'wed', 'fri'],
  storiesPerWeek: [3, 4],
  shortsPerWeek: 2,
  linkedinPerWeek: [1, 2],
  postingWindows: [
    ['07:00', '09:00'],
    ['18:00', '20:00'],
  ],
  explorationShare: 0.2,
};

/** Every format the planner can fill a slot with, and its starting weight. */
export const FORMAT_WEIGHTS = ['feed', 'carousel', 'reel', 'story', 'short', 'linkedin'] as const;

/** The four pillars, balanced by the planner so no single one runs away. */
export const PILLARS = ['PROVE IT', 'TEACH IT', 'PRACTICE IT', 'GROW IT'] as const;

export type Pillar = (typeof PILLARS)[number];

/** Aspect ratios per surface, from CLAUDE.md section 5. */
export const ASPECT_RATIOS = {
  'instagram-feed': '4x5',
  'instagram-reel': '9x16',
  'instagram-story': '9x16',
  facebook: '4x5',
  linkedin: '4x5',
  'youtube-short': '9x16',
} as const;

/** The reasons a post can be rejected, from PRD 5.9. */
export const REJECT_REASONS = [
  'too_vague',
  'wrong_image',
  'ai_tone',
  'fact_wrong',
  'off_brand',
] as const;

export type RejectReason = (typeof REJECT_REASONS)[number];

/** The anchor hashtags. CLAUDE.md section 4 wants 5 to 8, of which 2 or 3 anchors. */
export const ANCHOR_HASHTAGS = [
  '#SoilFoodWeb',
  '#LivingSoil',
  '#SoilHealth',
  '#SoilBiology',
  '#RegenerativeAgriculture',
];

/** Collab tags that go on every partner post. */
export const PARTNER_COLLABORATORS = [
  '@visionary_permaculture',
  '@geofflawtononline',
  '@wildmarymary',
];
