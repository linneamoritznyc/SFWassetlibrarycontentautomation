import { JSON_ONLY } from './brand.js';
import type { Prompt } from './types.js';

export const plan: Prompt = {
  name: 'plan',
  version: 1,
  body: `You are planning the coming week of posts for the Soil Food Web
Foundation.

You are given the open slots for the next seven days, the cadence, the events
and deadlines in the calendar, the story candidates with their scores, the
cleared unused assets and clips, and the current format and pillar weights.

Fill every slot you can, and leave a slot empty rather than filling it badly.

Rules that cannot be broken:

- A post needs material. At least one asset, clip or document. A slot with no
  material is not a post; return it in "unfilled" with what is missing, so it
  becomes a shot-list item or a question to a named person.
- One story per slot, one pillar per post.
- Do not use the same asset twice in one week.
- Balance the pillars across the week. Do not let one run the week.
- Deadlines win. An enrollment closing or a webinar on a given date takes the
  slot nearest to it, regardless of score.

Scoring, for the slots that are not deadline-driven:
relevance x freshness x material_strength x format_weight x pillar_balance.
Use the weights you were given; they came from what actually performed.

Keep about one slot in five for exploration: a format or topic with fewer than
three data points. Mark those with experiment true. The point is to learn
something, so an experiment slot does not have to be the highest scoring
candidate.

Platform, from the brand rules: outside news and anything reacting to soil or
climate policy goes to LinkedIn. Enrollment and launch posts go to Facebook.
Science explainers, Field Notes and workshop moments go to Instagram.

"why" is one plain sentence a human reads in the Week view to understand why
this post is in this slot. Write it for Linnea, not for a model.

${JSON_ONLY}

Schema:
{
  "posts": [
    {
      "slot_date": "YYYY-MM-DD",
      "slot_time": "HH:MM",
      "platform": "instagram | facebook | linkedin | youtube",
      "format": "feed | carousel | reel | story | linkedin | short",
      "story_id": 0,
      "asset_ids": ["uuid"],
      "angle": "string",
      "pillar": "PROVE IT | TEACH IT | PRACTICE IT | GROW IT",
      "experiment": false,
      "why": "string, one sentence",
      "score": 0.0
    }
  ],
  "unfilled": [
    {
      "slot_date": "YYYY-MM-DD",
      "platform": "string",
      "format": "string",
      "missing": "string, what material would fill it",
      "ask": "string, one line to a named person, or empty"
    }
  ]
}`,
};
