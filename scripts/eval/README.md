# eval

Runs the fixed test set against the active prompts on your own machine, the
same checks `eval_nightly` runs on Sundays.

```bash
pnpm --filter @sfw/script-eval build

# The critic, with the model. Costs a few cents.
node scripts/eval/dist/index.js

# The string checks only. Free, and instant.
node scripts/eval/dist/index.js --no-model

# A different prompt.
node scripts/eval/dist/index.js --prompt write

# Promote a version, but only if everything passed.
node scripts/eval/dist/index.js --activate 3
```

It exits non-zero when anything fails, so it works in a pre-commit hook or in
CI.

## What it checks

The test set is in `packages/shared/src/test-cases.ts` and is seeded into
`test_cases`. A **good** case has to come back clean and scored at or above its
threshold. A **bad** case has to be caught, either by the mechanical string
checks or by the critic naming the same check.

Three of the bad cases cannot be settled by a regular expression: the expertise
bar, platform fit and whether the caption matches the picture. With `--no-model`
those are reported as failures rather than quietly passed, so a run of 8 out of
11 is the expected result with the model off.

## Changing a prompt

1. Edit the file in `packages/prompts/src/`, bumping its `version`.
2. `pnpm db:seed`. The new version arrives **inactive**.
3. `node scripts/eval/dist/index.js --prompt <name>` to see how it does.
4. `--activate <version>` when it passes.

A prompt change cannot reach production just by being deployed. That is
deliberate: PRD 7.4 says any prompt or rule change must pass the test set
first.
