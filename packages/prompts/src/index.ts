import { critique } from './critique.js';
import { extractFacts } from './extract_facts.js';
import { findClips } from './find_clips.js';
import { gapCheck } from './gap_check.js';
import { learn } from './learn.js';
import { pasteIntake } from './paste_intake.js';
import { plan } from './plan.js';
import { proposeStory } from './propose_story.js';
import { scoutRank } from './scout_rank.js';
import { tag } from './tag.js';
import type { Prompt } from './types.js';
import { write } from './write.js';

export type { Prompt } from './types.js';
export { BRAND_RULES, JSON_ONLY } from './brand.js';

/**
 * Every prompt, in the order of the AI call table in backend spec section 7,
 * with the two paste-intake additions at the end.
 */
export const PROMPTS: Prompt[] = [
  tag,
  findClips,
  extractFacts,
  gapCheck,
  write,
  critique,
  plan,
  learn,
  scoutRank,
  pasteIntake,
  proposeStory,
];

export function promptByName(name: string): Prompt {
  const found = PROMPTS.find((p) => p.name === name);
  if (!found) {
    throw new Error(
      `No seed prompt named "${name}". Known: ${PROMPTS.map((p) => p.name).join(', ')}`,
    );
  }
  return found;
}
