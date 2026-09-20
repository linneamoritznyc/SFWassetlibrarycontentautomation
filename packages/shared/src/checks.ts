/**
 * The string checks. `eval_nightly` and the local eval script run these over
 * every draft a prompt produces, alongside the critic. They are deliberately
 * mechanical: a regular expression cannot be talked round, and these are the
 * failures that came back again and again in Linnea's edits.
 *
 * Each check returns the offending text so a failure report can quote it.
 */

export type CheckHit = { check: string; quote: string; note: string };

/** Phrases CLAUDE.md sections 3 and 4 retire outright. */
export const BANNED_PHRASES: { phrase: string; note: string }[] = [
  { phrase: 'reverse climate change', note: 'Say: sequester carbon and build climate resilience' },
  {
    phrase: 'eliminates the need for fertilizer',
    note: 'Say: dramatically reduce dependence on chemical inputs',
  },
  {
    phrase: "world's foremost soil biologist",
    note: 'Say: four decades of research, now being opened and replicated',
  },
  { phrase: 'proven on 5 million acres', note: 'Say: applied on millions of acres worldwide' },
  { phrase: 'miracle', note: 'Say: measurable, teachable, repeatable' },
  { phrase: 'revolutionary', note: 'Say: measurable, teachable, repeatable' },
  { phrase: 'game-changer', note: 'Say: measurable, teachable, repeatable' },
  { phrase: 'game changer', note: 'Say: measurable, teachable, repeatable' },
  { phrase: 'sign up + save', note: 'Retired. Sales pages only' },
  { phrase: 's.o.s. save our soils', note: 'Retired' },
  { phrase: 'skip the bag', note: 'The example of a slogan that fails' },
  { phrase: "here's the thing", note: 'AI cadence' },
  { phrase: 'let that sink in', note: 'AI cadence' },
  { phrase: 'the results speak for themselves', note: 'AI cadence' },
];

/** Internal acronyms that must never appear in public copy. */
export const INTERNAL_ACRONYMS = ['FC', 'AP', 'PDC', 'AW', 'CTP'];

/** "This isn't X, it's Y" and its relatives. */
export const NEGATION_PATTERNS: RegExp[] = [
  /\b(?:this|that|it)\s+(?:is|'s)\s*n[o']t\s+[^.!?]{1,60}?,\s*(?:it|that|this)\s*(?:'s|\s+is)\b/i,
  /\bnot\s+(?:just|only)\s+[^.!?]{1,60}?,\s*but\b/i,
  /\bthat'?s\s+not\s+[^.!?]{1,40}\.\s*that'?s\b/i,
];

const EM_DASH = /[—–]/;

/** A number with no nearby named case, place or season. */
const UNSOURCED_NUMBER = /\b\d{1,3}(?:[.,]\d+)?\s*%|\b\d{2,}\s*(?:gallons|acres|tons|tonnes)\b/i;

/** The three figures CLAUDE.md section 3 flags as having no source on file. */
export const UNSOURCED_FIGURES = ['0.5%', '3% healthy baseline', '22,000 gallons'];

export function runStringChecks(text: string): CheckHit[] {
  const hits: CheckHit[] = [];
  const lower = text.toLowerCase();

  for (const { phrase, note } of BANNED_PHRASES) {
    if (lower.includes(phrase.toLowerCase())) {
      hits.push({ check: 'banned_phrase', quote: phrase, note });
    }
  }

  for (const pattern of NEGATION_PATTERNS) {
    const m = pattern.exec(text);
    if (m) {
      hits.push({
        check: 'negation_framing',
        quote: m[0],
        note: 'No "this isn\'t X, it\'s Y". Say the thing plainly',
      });
    }
  }

  const dash = EM_DASH.exec(text);
  if (dash) {
    hits.push({
      check: 'em_dash',
      quote: dash[0],
      note: 'No em dashes. Use a full stop or a comma',
    });
  }

  for (const acronym of INTERNAL_ACRONYMS) {
    // Word boundary, and not inside a longer capitalised word.
    if (new RegExp(`(?<![A-Za-z])${acronym}(?![A-Za-z])`).test(text)) {
      hits.push({
        check: 'internal_acronym',
        quote: acronym,
        note: 'Internal acronyms stay out of public captions. Write the name in full',
      });
    }
  }

  for (const figure of UNSOURCED_FIGURES) {
    if (lower.includes(figure.toLowerCase())) {
      hits.push({
        check: 'unsourced_figure',
        quote: figure,
        note: 'This figure has no source on file (CLAUDE.md section 3). Find one or drop it',
      });
    }
  }

  return hits;
}

/**
 * True when the text names something concrete: an organism, a number with a
 * unit, a person, or a place. The expertise bar is more than this, but a draft
 * that fails it certainly does not clear the bar.
 */
export function hasConcreteDetail(text: string, organisms: string[]): boolean {
  if (organisms.some((o) => text.toLowerCase().includes(o.toLowerCase()))) return true;
  return UNSOURCED_NUMBER.test(text);
}
