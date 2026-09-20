# eval

Runs the `test_cases` rows against the active prompts on your own machine, the
same checks `eval_nightly` runs on Sundays: the critic prompt plus the string
checks (banned phrases, negation framing, em dashes, internal acronyms,
unsourced numbers).

```bash
pnpm --filter @sfw/script-eval build
node scripts/eval/dist/index.js --prompt write
node scripts/eval/dist/index.js --all
```

Use it before activating a prompt change by hand. Filled in Phase 6.
