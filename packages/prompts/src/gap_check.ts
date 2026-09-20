import { JSON_ONLY } from './brand.js';
import type { Prompt } from './types.js';

export const gapCheck: Prompt = {
  name: 'gap_check',
  version: 1,
  body: `Before anything is written, list what you would be assuming.

You are given the briefing packet for a post: the story, the assets chosen for
it, the facts already attached, and the calendar context.

Read it and answer one question honestly: to write this post, what would I have
to take on trust?

An assumption is something you believe is true and the briefing supports, but
which is not stated outright in the facts. Say what it is and what makes you
think it.

An unknown is something you would have to make up. A date nobody gave you, a
price, a person's role, a yield figure, which crop was in the ground, whether a
person in the photo agreed to be shown. If you would be inventing it, it is an
unknown. Write it as a single question a busy person can answer in one line
from memory, without opening anything.

Be specific. "More detail about the workshop" is useless. "Does the October
India workshop still have places, or has enrollment closed?" can be answered
in four words.

Say which topic each unknown belongs to, so it reaches the right person:
programs, mentors, graduates, students, india, partners, workshops, case
studies, links. Use the word that fits best; if none fits, use "programs".

Do not pad the list. Three real unknowns beat ten hedged ones. An empty
unknowns list is a good outcome and means the briefing was complete.

Never treat a number with no source as known. If the briefing uses one of the
three unsourced figures (organic matter below 0.5%, a 3% baseline, 22,000
gallons per acre), that is an unknown.

${JSON_ONLY}

Schema:
{
  "assumptions": [{ "text": "string", "basis": "string" }],
  "unknowns": [
    { "question": "string, one line", "topic": "string", "blocks_post": true }
  ]
}`,
};
