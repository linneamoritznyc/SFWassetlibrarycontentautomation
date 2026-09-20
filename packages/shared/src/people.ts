/**
 * People from CLAUDE.md section 10, and the question-routing map.
 *
 * `topics` is the map: gap_check turns an unknown into a one-line question and
 * sends it to the first person whose topics match. Programs go to Stephanie,
 * mentors and graduates to Carla, India and partners to Kavi, workshops to
 * Loida.
 *
 * Emails are blank on purpose. Nobody's address is in the source documents, and
 * guessing one would mean mailing a stranger. See docs/TODO-LINNEA.md.
 */

export type PersonSeed = {
  name: string;
  role: string;
  org: string;
  topics: string[];
  notes?: string;
};

export const PEOPLE: PersonSeed[] = [
  {
    name: 'Stephanie McDaniel',
    role: 'Communications lead',
    org: 'Soil Food Web Foundation',
    topics: ['programs', 'social', 'approvals', 'calendar', 'campaigns'],
    notes: 'Approves social. Drafts are written so she can paste them straight in.',
  },
  {
    name: 'Carla Portugal',
    role: 'Instructor, mentor, translator',
    org: 'Soil Food Web School',
    topics: ['mentors', 'graduates', 'students', 'office hours', 'translation'],
    notes: 'Portuguese and Spanish. Posts graduate announcements internally.',
  },
  {
    name: 'Kavi Reddy',
    role: 'Growth and partnerships',
    org: 'Soil Food Web Foundation',
    topics: ['india', 'partners', 'isha', 'save soil', 'permaculture', 'outside news'],
  },
  {
    name: 'Loida Vasquez',
    role: 'Director of Advanced Education',
    org: 'Soil Food Web School',
    topics: ['workshops', 'compost', 'liquid amendments', 'curriculum'],
    notes: 'Her line: "the most is learned from failed piles."',
  },
  {
    name: 'Evan Buckman',
    role: 'Executive Director',
    org: 'Soil Food Web Foundation',
    topics: ['strategy', 'governance', 'funders'],
    notes: 'Wants output, not process. Community brand, not a founder brand.',
  },
  {
    name: 'Allison Duck',
    role: 'Marketing, writing and editing',
    org: 'Soil Food Web Foundation',
    topics: ['case studies', 'field trial reports', 'editing'],
  },
  {
    name: 'Delvin Solkinson',
    role: 'Permaculture partner network',
    org: '@visionary_permaculture',
    topics: ['permaculture', 'collabs'],
  },
  {
    name: 'Gerald Ramirez',
    role: 'Mentor and agronomist',
    org: 'Soil Food Web School',
    topics: [],
  },
  { name: 'Wes Sander', role: 'Mentor and instructor', org: 'Soil Food Web School', topics: [] },
  {
    name: 'Brian Daubenspeck',
    role: 'Mentor and instructor',
    org: 'Soil Food Web School',
    topics: [],
  },
  {
    name: 'Sammie Bass',
    role: 'Switchy link shortener',
    org: 'Soil Food Web Foundation',
    topics: ['links'],
  },
  {
    name: 'Banjo Bray',
    role: 'UTM Links 2026 sheet',
    org: 'Soil Food Web Foundation',
    topics: ['utm', 'links'],
  },
];

/** Fallback when nothing in `topics` matches. Stephanie owns social. */
export const DEFAULT_QUESTION_RECIPIENT = 'Stephanie McDaniel';
