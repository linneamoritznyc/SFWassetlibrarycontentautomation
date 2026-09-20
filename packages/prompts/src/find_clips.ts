import { BRAND_RULES, JSON_ONLY } from './brand.js';
import type { Prompt } from './types.js';

export const findClips: Prompt = {
  name: 'find_clips',
  version: 1,
  body: `You are finding the moments in a workshop video that are worth cutting
into short vertical clips.

You are given the full transcript with word-level timestamps, the active rules
for reels, and the clips that performed best in the past.

${BRAND_RULES}

Return 12 to 15 candidates. More than are needed, on purpose, so the weakest
can be cut by a human.

What makes a candidate:

- It clears the expertise bar. It names an organism, a mechanism, a person, a
  place or a number. A speaker being warm and general is not a clip.
- It stands alone. Someone arriving with no context understands it. If it opens
  with "and so the second reason" it is not a clip, it is the middle of one.
- It is 20 to 60 seconds. Below 20 there is no room to land a point; above 60 it
  stops being a short.
- It starts and ends on a sentence boundary, at the timestamps of real words in
  the transcript. Never cut into the middle of a sentence.
- The hook is the speaker's own first line, or a plain line drawn from what they
  actually say. Do not write ad copy for it and do not add a claim the speaker
  did not make.

Score 0 to 100 on how strongly it clears the expertise bar and how well it
stands alone. Be hard. A 90 is something you would put on the feed this week; a
50 is usable if nothing better exists.

"why" is one plain sentence to a colleague explaining what makes this worth
cutting. It is read by a human deciding Keep or Cut, so make it useful.

Do not overlap candidates by more than a couple of seconds. If two good moments
sit inside the same passage, return the stronger one.

${JSON_ONLY}

Schema:
{
  "clips": [
    {
      "start": 0.0,
      "end": 0.0,
      "hook": "string, the opening line",
      "why": "string, one sentence",
      "pillar": "PROVE IT | TEACH IT | PRACTICE IT | GROW IT",
      "speaker": "string, or empty if unknown",
      "score": 0
    }
  ]
}`,
};
