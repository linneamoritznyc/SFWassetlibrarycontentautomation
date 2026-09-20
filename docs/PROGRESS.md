# Progress

What works, and how to check it. Updated at the end of every phase.

| Phase | Name | State |
| --- | --- | --- |
| 0 | Repo and folders | done |
| 1 | Database and queue | done |
| 2 | Library (web) + ingest | not started |
| 3 | Clipping machine | not started |
| 4 | Knowledge, writing and review | not started |
| 5 | Planner, cron, export, results | not started |
| 6 | Self-improvement | not started |
| 7 | Reels and Canva | not started |
| 8 | Scout, then polish | not started |

Paste intake (`docs/paste-intake.md`) is threaded through Phase 2 (capture and
the vision read) and Phase 4 (story and draft spin-up). No Drive, Google Chat or
Monday.com connection, by decision of 20 Sep 2026.

---

## Phase 0: Repo and folders

**What works**

- pnpm workspaces over `apps/*`, `workers/*`, `packages/*`, `scripts/*`.
- Turborepo tasks: `dev`, `build`, `lint`, `typecheck`, `test`.
- ESLint 9 flat config, Prettier, Vitest, one shared `tsconfig.base.json`.
- Every folder in the spec's tree exists, each top-level one with a README
  saying what lives there.
- `.env.example` carries every variable from backend spec section 12.
- `CLAUDE.md` at the root and in `docs/`.
- Dockerfiles for the three workers, each with what that worker actually needs
  (FFmpeg and Python for media, Chromium for render, nothing extra for light).

**How to test**

```bash
pnpm install
pnpm build        # builds every package, worker and the web app
pnpm lint
pnpm typecheck
pnpm test
```

All five must pass on the empty skeleton. Nothing here talks to Supabase, R2 or
Anthropic yet, so no keys are needed.

`pnpm format:check` also passes. Markdown is excluded from Prettier so the three
supplied source documents stay byte-for-byte as you wrote them.

Every screen in the spec exists as a route with a placeholder saying which phase
fills it: `/library`, `/inbox`, `/clips`, `/week`, `/scout`, `/learned`,
`/questions`, `/errors`, `/settings`, plus `GET /api/health`.

---

## Phase 1: Database and queue

**What works**

- Nine migrations in `supabase/migrations`, covering every table in backend spec
  section 4: 29 tables with foreign keys, check constraints and indexes,
  including HNSW vector indexes on `assets`, `facts` and `news_items`.
- Row Level Security on all 29, with no policies and the grants revoked from
  `anon` and `authenticated`. Only the service role gets through.
- `claim_job` (FOR UPDATE SKIP LOCKED, priority then age, only jobs that are
  due), `complete_job`, `fail_job` (backoff of 2^attempts minutes, `dead` after
  `max_attempts`), `retry_job` and `enqueue_job`.
- The database trigger from spec section 5: an asset moving to `tagged`
  enqueues `embed`, once, whatever happens to its status afterwards.
- Three rules the database itself enforces: a post past `proposed` must have
  material, a rejection must have a reason, a clip must have a parent and a
  range.
- `packages/queue`: typed `enqueue` with dedupe keys, `claim`, `complete`,
  `fail`, `retry`, a claim loop with configurable concurrency and graceful
  shutdown on SIGTERM, and a heartbeat every 60 seconds.
- `packages/shared`: the tag vocabulary (88 tags across 8 facets), smart
  folders, people with their question-routing topics, the cadence, and the
  mechanical string checks (banned phrases, negation framing, em dashes,
  internal acronyms, the three unsourced figures).
- `packages/prompts`: 11 prompts, one file each, versioned. The nine from spec
  section 7 plus `paste_intake` and `propose_story`.
- `packages/db`: connection pool, migration runner, idempotent seeder, and a
  test-database helper.
- The eval test set: 2 good cases and 9 bad ones, each naming the check that
  should catch it.

**How to test**

Against your Supabase project, once `DATABASE_URL` is set:

```bash
pnpm db:setup
# Applied: 0001_extensions.sql ... 0009_rls.sql
# Seeded: tags 88, smart_folders 16, people 12, settings 2,
#         planner_weights 10, prompts 11, test_cases 11
```

Run it twice. The second run says "No new migrations" and seeds the same counts
without creating duplicates.

The automated tests need a Postgres with the `vector` and `pgcrypto` extensions
that the test user can create databases on. Each test file builds its own
throwaway database and applies the migrations to it from scratch, so this is
also the check that the migrations apply cleanly to an empty project:

```bash
TEST_DATABASE_URL=postgres://postgres@127.0.0.1:5433/postgres pnpm test
```

39 tests: 11 string checks with no database, 16 on the schema and seed, 12 on
the queue. Without `TEST_DATABASE_URL` the 28 database tests skip and the rest
still run, so `pnpm test` passes on a machine with no Postgres.

The queue tests cover the Phase 1 acceptance case directly: enqueue, claim,
fail, retry with backoff, and complete. They also check that two workers racing
for the same job get one each, that a job waiting on its backoff is not
claimable, that priority beats age, and that a dedupe key blocks a duplicate
while the job is live and frees up when it finishes.
