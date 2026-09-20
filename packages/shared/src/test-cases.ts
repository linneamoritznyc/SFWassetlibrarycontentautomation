/**
 * The fixed test set. Any prompt or rule change has to pass this before it goes
 * live (PRD 7.4). `eval_nightly` runs it on Sundays; `scripts/eval` runs the
 * same thing on your own machine.
 *
 * A `good` case must score well and trip no string check. A `bad` case must be
 * caught: the critic has to return at least one must_fix naming the check in
 * `expected.catches`.
 *
 * The two good cases are rebuilt from the details CLAUDE.md records about them,
 * not copied from the real posts, which are not in any of the source documents.
 * Replace them with the real captions when you have them: see
 * docs/TODO-LINNEA.md. Until then they test the shape and the discipline, which
 * is most of what they are for.
 */

export type TestCaseSeed = {
  name: string;
  kind: 'good' | 'bad';
  input: { caption: string; platform?: string; format?: string; context?: string };
  expected: { minScore?: number; catches?: string[]; noHits?: boolean };
  notes: string;
};

export const TEST_CASES: TestCaseSeed[] = [
  {
    name: 'good: Pratik vermicompost',
    kind: 'good',
    input: {
      platform: 'instagram',
      format: 'feed',
      caption: `Finished vermicompost should be dark and crumbly, and hold together when you squeeze it.

Pratik checks four things before he calls a batch done. Moisture between 50 and 70 percent, so a handful clumps but does not drip. Visible aggregates, the small crumbs worms leave behind. Air channels running through it. Organic matter you can still identify, a leaf edge, a piece of stem.

And no foul smell. A sour or ammonia note means it went anaerobic, and the biology you were building is gone.

He learned this in Cyprus in 2025 and is applying it in India now.

Link in bio for the free webinars: https://webinar.soilfoodweb.com

#SoilFoodWeb #LivingSoil #SoilBiology #Vermicompost #RegenerativeAgriculture`,
    },
    expected: { minScore: 85, noHits: true },
    notes:
      'Clears the expertise bar five times over: named person, named place, a number with a unit, ' +
      'and an observable mechanism. Rebuilt from CLAUDE.md section 4.',
  },
  {
    name: 'good: Sandra Niggemeyer Field Notes',
    kind: 'good',
    input: {
      platform: 'instagram',
      format: 'carousel',
      caption: `FIELD NOTES No. 01

Sandra Niggemeyer grows butternut squash in Van, Texas, on ground that had been fallow long enough for the clay and sand to set hard.

She ran her practicum trial there last season and published what happened, including the part that did not work.

Swipe for the plots, the applications and the numbers she recorded.

Field Notes is where practicum graduates publish their trials. Inconclusive results get published too, because a result you can only report when it is flattering is not a result.

Link in bio: https://soilfoodweb.com

#SoilFoodWeb #LivingSoil #SoilHealth #FieldNotes #RegenerativeAgriculture`,
    },
    expected: { minScore: 85, noHits: true },
    notes:
      'Named person, named place, named crop, named season, and the series convention from ' +
      'CLAUDE.md section 7. Rebuilt, not the real caption.',
  },

  {
    name: 'bad: AI cadence, negation framing',
    kind: 'bad',
    input: {
      caption:
        "This isn't a compost pile, it's a living system. That's not gardening. That's soil biology.",
    },
    expected: { catches: ['negation_framing'] },
    notes: 'The exact cadence CLAUDE.md section 4 bans, twice in two sentences.',
  },
  {
    name: 'bad: not just X but Y',
    kind: 'bad',
    input: {
      caption:
        'Compost is not just a soil amendment, but an entire ecosystem you are choosing to feed.',
    },
    expected: { catches: ['negation_framing'] },
    notes: 'The softer version of the same pattern.',
  },
  {
    name: 'bad: em dash',
    kind: 'bad',
    input: {
      caption:
        'Living soil holds more water — and that is what carries a crop through a dry August.',
    },
    expected: { catches: ['em_dash'] },
    notes: 'No em dashes.',
  },
  {
    name: 'bad: internal acronyms in public copy',
    kind: 'bad',
    input: {
      caption: 'Finish your FC, then the PDC, then join the AW in October to go professional.',
    },
    expected: { catches: ['internal_acronym'] },
    notes: 'CLAUDE.md section 4: acronyms stay internal. Write the names in full.',
  },
  {
    name: 'bad: unsourced numbers',
    kind: 'bad',
    input: {
      caption:
        'Most agricultural soils are below 0.5% organic matter, against a 3% healthy baseline, ' +
        'and every 1% holds another 22,000 gallons per acre.',
    },
    expected: { catches: ['unsourced_figure'] },
    notes: 'All three figures CLAUDE.md section 3 flags as having no source on file.',
  },
  {
    name: 'bad: banned claims',
    kind: 'bad',
    input: {
      caption:
        'This revolutionary approach eliminates the need for fertilizer and can reverse climate change.',
    },
    expected: { catches: ['banned_phrase'] },
    notes: 'Three rungs too high on the evidence ladder in one sentence.',
  },
  {
    name: 'bad: clears no expertise bar',
    kind: 'bad',
    input: {
      caption:
        'Healthy soil is the foundation of everything we grow. Look after it, and it looks after you. ' +
        'Start your journey with us today.',
    },
    expected: { catches: ['expertise_bar'] },
    notes:
      'No organism, no mechanism, no person, no place, no number. Any lifestyle account ' +
      'could have posted it, which is the test CLAUDE.md section 4 sets.',
  },
  {
    name: 'bad: LinkedIn post with no question',
    kind: 'bad',
    input: {
      platform: 'linkedin',
      caption:
        'The Soil Food Web Foundation is a nonprofit carrying forward four decades of research, ' +
        'with graduates in over 100 countries.',
    },
    expected: { catches: ['platform_fit'] },
    notes:
      'CLAUDE.md section 4: restating org facts performs badly on LinkedIn, and every LinkedIn ' +
      'post ends with a real question.',
  },
  {
    name: 'bad: image and text disagree',
    kind: 'bad',
    input: {
      context: 'The attached image shows a hand holding finished dark vermicompost, indoors.',
      caption:
        'Day three of the thermophilic pile and it is holding at 60 degrees Celsius in the field.',
    },
    expected: { catches: ['image_text_match'] },
    notes:
      'The critic sees the images. A caption about a hot pile over a photo of finished castings.',
  },
];
