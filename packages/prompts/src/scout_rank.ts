import { JSON_ONLY } from './brand.js';
import type { Prompt } from './types.js';

export const scoutRank: Prompt = {
  name: 'scout_rank',
  version: 1,
  body: `Rate one news item for how useful it is to the Soil Food Web
Foundation.

The Foundation teaches people to restore the living biology of their soil. It
cares about: soil biology and microbiology, soil health and organic matter,
regenerative agriculture, compost and biological amendments, soil policy in the
EU, US and India, water and carbon in soil, and its partners (Isha Foundation,
Conscious Planet, Save Soil, the permaculture network).

Summarise it in one or two plain sentences. What happened, and who says so.

Relevance, 0 to 1:
- 0.9 and up: new research or policy directly about soil biology or soil health
  that the Foundation could react to this week.
- 0.7 to 0.9: adjacent and usable. Regenerative agriculture, carbon in soil,
  water retention, a partner's news.
- 0.4 to 0.7: same world, no angle. General climate or farming news.
- Below 0.4: not for us.

Be strict. Everything at 0.7 and above becomes a story candidate and takes up a
slot in someone's week.

Topics: short lowercase words from what the item is actually about.

${JSON_ONLY}

Schema:
{
  "summary": "string, one or two sentences",
  "relevance": 0.0,
  "topics": ["string"]
}`,
};
