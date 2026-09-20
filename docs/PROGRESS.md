# Progress

What works, and how to check it. Updated at the end of every phase.

| Phase | Name | State |
| --- | --- | --- |
| 0 | Repo and folders | done |
| 1 | Database and queue | done |
| 2 | Library (web) + ingest | in progress: storage, AI and the worker jobs done; the web app is next |
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

---

## Phase 2 so far: storage, AI and the ingest jobs

The web app is not built yet. Everything the jobs need is.

**What works**

- `packages/storage`: the R2 layout from spec section 3 built in one place,
  presigned PUT and GET at one hour, and a filename sanitiser so nothing can
  escape its folder. Video originals go to `sfw-raw`, everything else to
  `sfw-media`.
- `packages/ai`: one Claude call path used by every job. It loads the active
  prompt from the table, constrains the reply to a zod schema server-side,
  validates it again on the way back, retries once with the failure quoted if
  it still does not match, and logs tokens, latency and cost to `ai_calls`
  whether the call succeeded or not.
- `packages/ai`: a zod schema per AI contract, and embeddings at 1024
  dimensions to match the `vector(1024)` columns.
- `workers/light` with five jobs: `ingest`, `embed`, `extract_doc`,
  `paste_intake` and `web_fetch`. It claims what `WORKER_TYPES` names, runs at
  concurrency 4, heartbeats every 60 seconds and shuts down gracefully.

**The paste flow, end to end in the queue**

`paste_intake` reads the screenshot with Claude vision, pulls out the sender,
the message and the links, and enqueues `web_fetch` for each link. `web_fetch`
fetches the page, hashes it, and turns it into sourced facts, retiring the
facts from any previous read of the same URL. It then enqueues `propose_story`,
whose handler arrives in Phase 4; until then those jobs sit in the queue, which
is exactly what should happen.

**How to test**

The jobs need real keys (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, the four R2
variables) and a Supabase project, so they are not covered by the automated
tests. What is covered without keys:

```bash
pnpm test
```

10 tests over the R2 key layout and the cost calculation, on top of the 29 from
Phase 1.

**Still to do in Phase 2**

Auth with the allowlist, the upload form and presigned PUT, `POST /api/assets`
and the rest of the routes, the library UI, the inbox with its keyboard
shortcuts, the errors view, and the bulk-upload script.
