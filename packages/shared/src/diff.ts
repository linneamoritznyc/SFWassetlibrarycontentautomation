/**
 * Measuring what a human changed about a draft.
 *
 * This is the input to the whole self-improvement loop: `log_edit` stores the
 * diff, `learn_weekly` clusters them into rules, and the autonomy ladder uses
 * "edited by 10% or less" to decide what can move to lighter review. So it
 * needs to be a number that means something, not a character count.
 *
 * Word-level rather than character-level, because "vermicompost" becoming
 * "worm castings" is one change, not eleven.
 */

export type Change = { kind: 'added' | 'removed'; text: string };

export type EditDiff = {
  /** 0 when nothing changed, 1 when nothing survived. */
  ratio: number;
  changes: Change[];
  addedWords: number;
  removedWords: number;
  /** Whole sentences the human dropped, which is the strongest signal. */
  removedSentences: string[];
  /** Whole sentences the human wrote, which is the next strongest. */
  addedSentences: string[];
};

export function words(text: string): string[] {
  return (
    text
      .toLowerCase()
      // Underscores stay: Instagram handles have them, and @visionary_permaculture
      // splitting into two words would read as an edit every time.
      .replace(/[^\p{L}\p{N}\s#@_'-]/gu, ' ')
      .split(/\s+/)
      .filter(Boolean)
  );
}

export function sentences(text: string): string[] {
  return text
    .split(/(?<=[.!?])\s+|\n+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

/**
 * How much of the draft survived, as a share of the larger of the two.
 *
 * Uses a multiset difference rather than a true edit distance: moving a
 * sentence is not an edit in any sense that matters here, and an O(n*m) Levenshtein
 * over a caption is a lot of work to answer a question that "which words are
 * gone" already answers.
 */
export function diffCaption(before: string, after: string): EditDiff {
  const beforeWords = words(before);
  const afterWords = words(after);

  const counts = new Map<string, number>();
  for (const word of beforeWords) counts.set(word, (counts.get(word) ?? 0) + 1);

  const added: string[] = [];
  for (const word of afterWords) {
    const left = counts.get(word) ?? 0;
    if (left > 0) counts.set(word, left - 1);
    else added.push(word);
  }

  const removed: string[] = [];
  for (const [word, left] of counts) {
    for (let i = 0; i < left; i += 1) removed.push(word);
  }

  const largest = Math.max(beforeWords.length, afterWords.length, 1);
  const ratio = Math.min(1, (added.length + removed.length) / (largest * 2));

  const beforeSentences = sentences(before);
  const afterSentences = sentences(after);
  const normalise = (s: string) => words(s).join(' ');
  const afterSet = new Set(afterSentences.map(normalise));
  const beforeSet = new Set(beforeSentences.map(normalise));

  return {
    ratio,
    changes: [
      ...removed.map((text) => ({ kind: 'removed' as const, text })),
      ...added.map((text) => ({ kind: 'added' as const, text })),
    ],
    addedWords: added.length,
    removedWords: removed.length,
    removedSentences: beforeSentences.filter((s) => !afterSet.has(normalise(s))),
    addedSentences: afterSentences.filter((s) => !beforeSet.has(normalise(s))),
  };
}

/** The autonomy ladder's threshold: a post barely touched. */
export function barelyEdited(diff: EditDiff): boolean {
  return diff.ratio <= 0.1;
}
