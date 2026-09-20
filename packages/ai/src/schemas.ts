import { z } from 'zod';

/**
 * One zod schema per AI call in backend spec section 7, plus the two paste
 * additions. These are handed to the API as the output format, so the model is
 * constrained to the shape rather than asked nicely for it, and they are
 * validated again on the way back.
 *
 * Each schema matches the "Schema:" block at the end of the matching prompt in
 * `@sfw/prompts`. Change one, change the other, and bump the prompt version.
 */

const confidence = z.number().min(0).max(1);

export const tagSchema = z.object({
  description: z.string(),
  tags: z.array(z.object({ facet: z.string(), name: z.string(), confidence })),
  people_guess: z.array(z.object({ name: z.string(), confidence })),
  hero_candidate: z.boolean(),
  quality: z.number().int().min(1).max(5),
  notes: z.string(),
});
export type TagResult = z.infer<typeof tagSchema>;

export const findClipsSchema = z.object({
  clips: z.array(
    z.object({
      start: z.number().nonnegative(),
      end: z.number().nonnegative(),
      hook: z.string(),
      why: z.string(),
      pillar: z.string(),
      speaker: z.string(),
      score: z.number().min(0).max(100),
    }),
  ),
});
export type FindClipsResult = z.infer<typeof findClipsSchema>;

export const extractFactsSchema = z.object({
  facts: z.array(
    z.object({
      subject: z.string(),
      predicate: z.string(),
      object: z.string(),
      text: z.string(),
      page: z.string(),
      confidence,
      conflict: z.boolean(),
      note: z.string(),
    }),
  ),
});
export type ExtractFactsResult = z.infer<typeof extractFactsSchema>;

export const gapCheckSchema = z.object({
  assumptions: z.array(z.object({ text: z.string(), basis: z.string() })),
  unknowns: z.array(
    z.object({ question: z.string(), topic: z.string(), blocks_post: z.boolean() }),
  ),
});
export type GapCheckResult = z.infer<typeof gapCheckSchema>;

export const writeSchema = z.object({
  hook: z.string(),
  caption: z.string(),
  hashtags: z.array(z.string()),
  cta_text: z.string(),
  cta_url: z.string(),
  alt_text: z.string(),
  pillar: z.string(),
  sources_used: z.array(z.number().int()),
  blocked_reason: z.string(),
});
export type WriteResult = z.infer<typeof writeSchema>;

export const critiqueSchema = z.object({
  score: z.number().min(0).max(100),
  issues: z.array(z.object({ check: z.string(), quote: z.string(), note: z.string() })),
  must_fix: z.array(z.object({ check: z.string(), quote: z.string(), fix: z.string() })),
  verdict: z.string(),
});
export type CritiqueResult = z.infer<typeof critiqueSchema>;

export const planSchema = z.object({
  posts: z.array(
    z.object({
      slot_date: z.string(),
      slot_time: z.string(),
      platform: z.string(),
      format: z.string(),
      story_id: z.number().int().nullable(),
      asset_ids: z.array(z.string()),
      angle: z.string(),
      pillar: z.string(),
      experiment: z.boolean(),
      why: z.string(),
      score: z.number(),
    }),
  ),
  unfilled: z.array(
    z.object({
      slot_date: z.string(),
      platform: z.string(),
      format: z.string(),
      missing: z.string(),
      ask: z.string(),
    }),
  ),
});
export type PlanResult = z.infer<typeof planSchema>;

export const learnSchema = z.object({
  rules: z.array(
    z.object({
      text: z.string(),
      scope: z.string(),
      evidence: z.array(z.string()),
      why: z.string(),
    }),
  ),
  already_covered: z.array(z.object({ rule_id: z.number().int(), note: z.string() })),
  note: z.string(),
});
export type LearnResult = z.infer<typeof learnSchema>;

export const scoutRankSchema = z.object({
  summary: z.string(),
  relevance: confidence,
  topics: z.array(z.string()),
  // Added in scout_rank v2, with defaults so a database still running v1
  // validates rather than failing every item.
  language: z.string().default('en'),
  original_title: z.string().default(''),
});
export type ScoutRankResult = z.infer<typeof scoutRankSchema>;

export const pasteIntakeSchema = z.object({
  kind: z.string(),
  sender: z.string(),
  sent_at: z.string(),
  message_text: z.string(),
  urls: z.array(z.string()),
  unreadable_urls: z.array(z.string()),
  link_preview_title: z.string(),
  link_preview_source: z.string(),
  image_description: z.string(),
  is_sfw_material: z.boolean(),
  sensitive: z.boolean(),
  note: z.string(),
});
export type PasteIntakeResult = z.infer<typeof pasteIntakeSchema>;

export const proposeStorySchema = z.object({
  has_story: z.boolean(),
  no_story_reason: z.string(),
  angle: z.string(),
  pillar: z.string(),
  platform: z.string(),
  format: z.string(),
  attribution: z.string(),
  asset_ids: z.array(z.string()),
  fact_ids: z.array(z.number().int()),
  material_needed: z.string(),
  questions: z.array(z.object({ question: z.string(), topic: z.string() })),
  score: z.number(),
});
export type ProposeStoryResult = z.infer<typeof proposeStorySchema>;

/** Every schema by the prompt name it belongs to. */
export const SCHEMAS = {
  tag: tagSchema,
  find_clips: findClipsSchema,
  extract_facts: extractFactsSchema,
  gap_check: gapCheckSchema,
  write: writeSchema,
  critique: critiqueSchema,
  plan: planSchema,
  learn: learnSchema,
  scout_rank: scoutRankSchema,
  paste_intake: pasteIntakeSchema,
  propose_story: proposeStorySchema,
} as const;

export type PromptName = keyof typeof SCHEMAS;
