import { BRAND_RULES, JSON_ONLY } from './brand.js';
import type { Prompt } from './types.js';

export const proposeStory: Prompt = {
  name: 'propose_story',
  version: 1,
  body: `Something came in: a link a colleague shared, a document, or a note.
Decide whether the Soil Food Web Foundation has a post in it, and if so, what
the angle is.

You are given what was pasted, the facts extracted from whatever it linked to,
and the library assets that came closest on a meaning search.

${BRAND_RULES}

Work through it in this order.

1. Is there anything here for us? Not everything a colleague shares is a post.
   Say no clearly when the answer is no; an honest "no angle" costs nothing, a
   thin post costs the account's credibility.

2. Whose finding is it? Outside research and other organisations' announcements
   stay theirs. The Foundation cites them, reacts to them, and adds what it
   knows. It never restates someone else's result as its own work, and never
   moves their hedged claim up a rung.

3. Which pillar? Usually PROVE IT for outside science and policy, because the
   move is "here is more evidence that living soil is the lever", and the
   Foundation's own position is that the science is real and being opened.

4. Which platform? LinkedIn first for outside news, soil policy and climate
   research: that is where the Foundation reacts to real niche news, and it must
   end on a real question. Instagram only when there is a science explainer in
   it and an SFW image that can carry it. Never both by default.

5. What carries it visually? Choose from the library assets you were given, and
   only those. The screenshot itself is not a visual. A photograph belonging to
   whoever published the link is not a visual. If nothing in the library fits
   the angle, leave asset_ids empty and write the shot you would need in
   "material_needed", as one line a person can act on.

6. What is still unknown? Anything you would have to invent goes in "questions",
   one line each, with the topic so it reaches the right person.

The angle is one sentence: what this post says that is worth someone's
attention, in plain words, naming the concrete thing it hangs on.

${JSON_ONLY}

Schema:
{
  "has_story": true,
  "no_story_reason": "string, empty when has_story is true",
  "angle": "string, one sentence",
  "pillar": "PROVE IT | TEACH IT | PRACTICE IT | GROW IT",
  "platform": "instagram | facebook | linkedin | youtube",
  "format": "feed | carousel | reel | story | linkedin | short",
  "attribution": "string, whose finding this is and how to credit it",
  "asset_ids": ["uuid, from the library assets given to you"],
  "fact_ids": [0],
  "material_needed": "string, the shot or document that is missing, or empty",
  "questions": [{ "question": "string, one line", "topic": "string" }],
  "score": 0.0
}`,
};
