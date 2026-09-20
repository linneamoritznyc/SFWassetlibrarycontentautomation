/**
 * One file per prompt. The seed script upserts every prompt here into the
 * `prompts` table; workers load the active version from the table at job start
 * and never read these files at runtime.
 *
 * Changing a body means bumping `version`. Seeding a new version does not
 * activate it: `eval_nightly` and the local eval script decide that, so a
 * prompt change cannot reach production without passing the test set.
 */
export type Prompt = {
  name: string;
  version: number;
  body: string;
};
