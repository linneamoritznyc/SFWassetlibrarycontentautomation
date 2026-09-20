import { describe, expect, it } from 'vitest';
import { runStringChecks } from './checks.js';
import { TEST_CASES } from './test-cases.js';

/**
 * These run with no database, so they are the checks CI can always do. They are
 * the mechanical half of eval_nightly: the half a regular expression can settle.
 */
describe('string checks', () => {
  const checksFor = (text: string) => runStringChecks(text).map((h) => h.check);

  it('catches "this isn\'t X, it\'s Y"', () => {
    expect(checksFor("This isn't a compost pile, it's a living system.")).toContain(
      'negation_framing',
    );
  });

  it('catches "not just X, but Y"', () => {
    expect(checksFor('Compost is not just an amendment, but an ecosystem.')).toContain(
      'negation_framing',
    );
  });

  it('catches em dashes', () => {
    expect(checksFor('Living soil holds water — more than you think.')).toContain('em_dash');
  });

  it('catches internal acronyms without catching ordinary words', () => {
    expect(checksFor('Finish the PDC before October.')).toContain('internal_acronym');
    expect(checksFor('The compost was applied across the field.')).not.toContain(
      'internal_acronym',
    );
  });

  it('catches the three figures with no source on file', () => {
    expect(checksFor('Most soils sit below 0.5% organic matter.')).toContain('unsourced_figure');
    expect(checksFor('That is 22,000 gallons per acre.')).toContain('unsourced_figure');
  });

  it('catches retired and overreaching claims', () => {
    expect(checksFor('This revolutionary method can reverse climate change.')).toContain(
      'banned_phrase',
    );
  });

  it('leaves a caption that clears the expertise bar alone', () => {
    const clean =
      'Pratik checks the pile at 55 percent moisture and looks for visible aggregates and ' +
      'air channels before he calls it finished.';
    expect(runStringChecks(clean)).toEqual([]);
  });
});

describe('the eval test set', () => {
  it('has the two good cases the PRD names', () => {
    const good = TEST_CASES.filter((t) => t.kind === 'good').map((t) => t.name);
    expect(good.some((n) => n.includes('Pratik'))).toBe(true);
    expect(good.some((n) => n.includes('Sandra'))).toBe(true);
  });

  it('every good case passes the string checks', () => {
    for (const t of TEST_CASES.filter((c) => c.kind === 'good')) {
      expect(runStringChecks(t.input.caption), `${t.name} should be clean`).toEqual([]);
    }
  });

  it('every mechanical bad case is caught by the check it names', () => {
    const mechanical = [
      'negation_framing',
      'em_dash',
      'internal_acronym',
      'unsourced_figure',
      'banned_phrase',
    ];

    for (const t of TEST_CASES.filter((c) => c.kind === 'bad')) {
      const wants = (t.expected.catches ?? []).filter((c) => mechanical.includes(c));
      if (wants.length === 0) continue; // left to the critic, not to a regex

      const hits = runStringChecks(t.input.caption).map((h) => h.check);
      for (const want of wants) {
        expect(hits, `${t.name} should trip ${want}`).toContain(want);
      }
    }
  });

  it('leaves judgement calls to the critic rather than to a regex', () => {
    const judgement = TEST_CASES.filter((t) =>
      (t.expected.catches ?? []).some((c) =>
        ['expertise_bar', 'platform_fit', 'image_text_match'].includes(c),
      ),
    );
    expect(judgement.length).toBeGreaterThanOrEqual(3);
  });
});
