/**
 * The tag vocabulary, drawn from CLAUDE.md. The `ingest` job is given this list
 * and may only choose from it, so the library stays filterable instead of
 * drifting into a thousand near-duplicate tags. Adding a tag is a code change
 * and a re-seed, on purpose.
 */

export const TAG_FACETS = [
  'workshop',
  'subject',
  'organism',
  'pillar',
  'people',
  'place',
  'platform_fit',
  'format',
] as const;

export type TagFacet = (typeof TAG_FACETS)[number];

export type TagSeed = { name: string; facet: TagFacet };

const facet = (f: TagFacet, names: string[]): TagSeed[] =>
  names.map((name) => ({ name, facet: f }));

export const TAG_VOCABULARY: TagSeed[] = [
  // Where the material was shot. CLAUDE.md section 5 names the workshops SFW
  // actually has footage from.
  ...facet('workshop', [
    'New Mexico compost workshop',
    'Wild Ken Hill',
    'Cyprus 2025',
    'India Accelerator Workshop 2026',
    'Life in the Soils seminar',
  ]),

  // What is happening in the frame.
  ...facet('subject', [
    'compost',
    'vermicompost',
    'thermophilic pile',
    'turning a pile',
    'compost extract',
    'compost tea',
    'protozoan infusion',
    'nematode extraction',
    'microscopy',
    'soil sampling',
    'field assessment',
    'field application',
    'experiment design',
    'field trial',
    'restoration',
    'vineyard',
    'cover crop',
    'water retention',
    'carbon',
    'organic matter',
    'aggregates',
    'roots',
    'teaching',
    'group work',
    'portrait',
    'landscape',
  ]),

  // The organisms. Naming one is half of how a post clears the expertise bar
  // in CLAUDE.md section 4.
  ...facet('organism', [
    'bacteria',
    'fungi',
    'mycorrhizal fungi',
    'protozoa',
    'flagellates',
    'amoebae',
    'ciliates',
    'nematodes',
    'bacterial-feeding nematode',
    'fungal-feeding nematode',
    'predatory nematode',
    'root-feeding nematode',
    'micro-arthropods',
    'earthworms',
  ]),

  // The Messaging House. Every post stands on exactly one.
  ...facet('pillar', ['PROVE IT', 'TEACH IT', 'PRACTICE IT', 'GROW IT']),

  // Seeded from CLAUDE.md section 10. The people table is the real record;
  // these exist so an asset can be filtered by who is in it.
  ...facet('people', [
    'Dr. Elaine Ingham',
    'Evan Buckman',
    'Stephanie McDaniel',
    'Loida Vasquez',
    'Gerald Ramirez',
    'Carla Portugal',
    'Kavi Reddy',
    'Wes Sander',
    'Brian Daubenspeck',
    'Delvin Solkinson',
    'Sandra Niggemeyer',
    'Josh Cheng',
    'Pratik',
  ]),

  ...facet('place', [
    'Coimbatore, Tamil Nadu',
    'Isha Yoga Center',
    'Save Soil Regenerative Revolution Farm',
    'Portland, Oregon',
    'Van, Texas',
    'Anhui Province, China',
    'Cyprus',
    'New Mexico',
    'Wild Ken Hill, Norfolk',
  ]),

  // Which surface the material suits. Ratios come from CLAUDE.md section 5.
  ...facet('platform_fit', [
    'instagram-feed',
    'instagram-reel',
    'instagram-story',
    'facebook',
    'linkedin',
    'youtube-short',
  ]),

  // Which shape of post it could carry. The named series come from CLAUDE.md
  // section 7 and PRD 5.6.
  ...facet('format', [
    'feed',
    'carousel',
    'reel',
    'story',
    'short',
    'field-notes',
    'science-explainer',
    'workshop-moment',
    'workshop-recap',
    'webinar-promo',
    'quote-card',
  ]),
];

export const TAG_NAMES_BY_FACET: Record<TagFacet, string[]> = TAG_FACETS.reduce(
  (acc, f) => {
    acc[f] = TAG_VOCABULARY.filter((t) => t.facet === f).map((t) => t.name);
    return acc;
  },
  {} as Record<TagFacet, string[]>,
);
