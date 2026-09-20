import { JSON_ONLY } from './brand.js';
import type { Prompt } from './types.js';

export const scoutRank: Prompt = {
  name: 'scout_rank',
  version: 2,
  body: `Rate one news item for how useful it is to the Soil Food Web
Foundation.

The Foundation teaches people to restore the living biology of their soil. It
has graduates in more than 100 countries, so this list is global: UN bodies,
international research centres, and regional programmes from Andhra Pradesh to
Brazil to the African Union.

It cares about: soil biology and microbiology, soil health and organic matter,
regenerative agriculture, compost and biological amendments, soil and land
policy anywhere in the world, water and carbon in soil, desertification and
land restoration, and its partners (Isha Foundation, Conscious Planet, Save
Soil, the permaculture network).

## Language

The item may be in any language. Brazilian research arrives in Portuguese,
Latin American institutions publish in Spanish, EU bodies in French or German.

- Write "summary" in **English**, always, whatever the source language. The
  planner, the writer and the critic all read it, and they work in English.
- Set "language" to the BCP 47 tag of what you were actually given: "en",
  "pt-BR", "es", "fr", "hi", "te". Judge it from the text, not from the domain
  name: plenty of Brazilian sites publish in English.
- When the item is not in English, put its own headline, unchanged and in its
  own script, in "original_title". Leave it empty for English items. It is
  shown next to the summary so a caption can quote the source properly rather
  than quoting a translation.
- Do not translate names of institutions, places or programmes. Embrapa is
  Embrapa. Write the acronym the organisation uses for itself.

## Relevance, 0 to 1

- 0.9 and up: new research or policy directly about soil biology or soil health
  that the Foundation could react to this week.
- 0.7 to 0.9: adjacent and usable. Regenerative agriculture, carbon or water in
  soil, land restoration, desertification, a partner's news, a national or
  regional soil programme.
- 0.4 to 0.7: same world, no angle. General climate or farming news.
- Below 0.4: not for us.

Be strict. Everything at 0.7 and above becomes a story candidate and takes up a
slot in someone's week.

Judge the item, not where it came from. A thin press release from a famous
institution scores below a specific finding from a small one. A regional
programme reaching a million farmers is more interesting than another summary
of why soil matters.

## Topics

Short lowercase words from what the item is actually about. Include the region
or country when the item is about a specific place: "brazil", "andhra
pradesh", "sahel".

${JSON_ONLY}

Schema:
{
  "summary": "string, one or two sentences, in English",
  "language": "string, BCP 47 tag of the source",
  "original_title": "string, the headline in its own language, or empty for English",
  "relevance": 0.0,
  "topics": ["string"]
}`,
};
