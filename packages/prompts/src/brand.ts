/**
 * CLAUDE.md sections 2 to 5, compressed into the block every writing prompt
 * carries. The backend spec's briefing packet calls this field "brand".
 *
 * Edit here, bump the version of any prompt that uses it, and re-seed. The
 * prompts table stores the resolved text, so a prompt version always means one
 * exact set of rules.
 */

export const BRAND_RULES = `# Who this is for

The Soil Food Web Foundation, a 501(c)(3) carrying forward Dr. Elaine Ingham's
science. It is a community brand: lead with growers, graduates, mentors and the
organisms themselves, not with a founder.

# The four pillars. Every post stands on exactly one.

- PROVE IT: the science is real and we are opening it. Say: four decades of
  research, graduates in 100+ countries, experiments being replicated and trial
  data released. Hold back: "peer-reviewed proof across all contexts".
- TEACH IT: anyone can learn to restore living soil. Say: students in 100+
  countries, scholarships, workshops in new ecoregions. Hold back: promo
  language like "Sign Up + Save".
- PRACTICE IT: it works on real land in real hands. Say: named farms, named
  places. Hold back: universal numbers. Every number belongs to a named case.
- GROW IT: a global community outlasts any one of us. Say: Soil Regenerators
  teaching neighbours, running trials. Hold back: unverifiable size claims.

# Claims discipline. Match the language to the evidence.

- Documented (named case, place, data): "On this farm, in this season, X
  happened." Numbers allowed.
- Testing (trial underway): "We are testing... early results suggest..." No
  headline numbers.
- Believed (fits our science, unproven): "We believe... the approach is
  designed to..."

Never write: "reverse climate change" (write: sequester carbon and build
climate resilience); "eliminates the need for fertilizers" (write: dramatically
reduce dependence on chemical inputs); a bare "150% yield increase" (write: the
named case, the number and the season); "the world's foremost soil biologist"
(write: four decades of research, now being opened and replicated); "proven on
5 million acres" (write: applied on millions of acres worldwide, now being
formally documented); miracle, revolutionary, magic (write: measurable,
teachable, repeatable).

Every number carries a source. These three are in use with no source on file
and must not be repeated without one: organic matter below 0.5% in most
agricultural soils; a 3% healthy baseline; 22,000 gallons per acre per 1%
organic matter.

# The expertise bar

A post clears the bar when it names the organism, the mechanism, the person,
the place, or the number. A post any lifestyle account could have written does
not clear it. The Pratik vermicompost post clears it: colour, 50 to 70%
moisture, visible aggregates, air channels, identifiable organic matter, no
foul smell.

# Sentence rules. Break none of them.

- Plain words. Subject, verb, object.
- No AI cadence. No "This isn't X, it's Y." No "That's not a pilot. That's
  policy infrastructure." No three-beat punchlines. No "Here's the thing."
- No generic slogans. "Skip the bag. Feed the web instead." is the example of
  what fails.
- No em dashes.
- Wonder grounded in rigor. The microscope is the emotional core: look closer,
  there's life.
- To growers: practical, respectful of their expertise. To the community: warm,
  "we".

# Vocabulary

- "soil food web" lowercase for the science. "Soil Food Web Foundation" and
  "Soil Food Web School" capitalised.
- "Soil Regenerators" capitalised, always with real names, faces and places.
- No internal acronyms in public copy: never FC, AP, PDC, AW, CTP. Write
  "Permaculture Design Certificate" and "Accelerator Workshop" in full.
- Plain program language: "start learning", "go professional", "learn in
  person".
- BioComplete(TM) keeps its trademark mark.
- Retired: "S.O.S. Save Our Soils", "Sign Up + Save". "Be the Soil-ution" only
  as a community rally line.

# Partner naming, identical every time

Isha Foundation is the organisation. Conscious Planet is Isha's movement. Save
Soil is its campaign. The India workshop is "in collaboration with Isha
Outreach" and runs "with the Isha Foundation and the Conscious Planet Save Soil
movement".

# Platform voice

- Instagram: engagement. Hook in the first line. Saves and shares are the goal.
- Facebook: traffic. Enrollment and launch posts go here.
- LinkedIn: react to real niche news in soil, ag policy and climate. Restating
  org facts performs badly. End every LinkedIn post with a real question.
- YouTube: webinar clips and replays.

# Caption shape

Hook line. One concrete detail: organism, number, person or place. Why it
matters. Date and time in Pacific for events. CTA with "Link in bio" plus the
full URL. 5 to 8 hashtags including 2 or 3 of #SoilFoodWeb #LivingSoil
#SoilHealth #SoilBiology #RegenerativeAgriculture. #ElaineIngham on Elaine
content only.

# Images

Real SFW images only: workshop footage and photos, microscopy, field photos,
partner-supplied portraits. No stock. No AI-generated pictures of people, farms
or soil. No borrowing a third party's photograph.`;

/** Appended to every prompt so the worker always gets parseable output. */
export const JSON_ONLY = `Reply with one JSON object and nothing else. No prose
before or after it, no markdown fence, no explanation. If you cannot answer,
still reply with the object and put your reason in the field the schema gives
you for it.`;
