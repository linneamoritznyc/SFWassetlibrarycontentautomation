# scripts

- `bulk-upload/` — an rclone guide for pushing the raw footage drive into
  `sfw-raw`, plus a script that registers objects already in R2 as assets and
  enqueues `ingest` for each.
- `eval/` — runs the test set in `test_cases` against the active prompts on your
  own machine, the same checks `eval_nightly` runs.
