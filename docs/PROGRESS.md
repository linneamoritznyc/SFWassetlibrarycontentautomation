# Progress

What works, and how to check it. Updated at the end of every phase.

| Phase | Name | State |
| --- | --- | --- |
| 0 | Repo and folders | done |
| 1 | Database and queue | done |
| 2 | Library (web) + ingest | done, except uploading the fixtures, which needs your keys |
| 3 | Clipping machine | done, except the contractor test, which needs a real video |
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

## Phase 2: Library and ingest

**What works**

*Auth.* Supabase magic link. The allowlist is checked in middleware on every
request, so no page or route can forget it. An empty `APP_ALLOWLIST` lets nobody
in. A `/setup` page explains what is missing rather than crashing when the app
has no configuration yet.

*Upload.* A batch form (Drive link, original path, creator, workshop) entered
once and copied onto every asset. Drag and drop anything. The browser makes an
800px JPEG thumbnail (a frame at two seconds for video), reads EXIF with exifr,
and uploads straight to R2 with presigned PUTs, so nothing large passes through
a serverless function. `POST /api/assets` then creates the batch and enqueues
one `ingest` per asset.

*Paste.* Cmd-V anywhere on the library or inbox page. A screenshot goes in as a
`reference` asset and is read by `paste_intake`; a link goes straight to
`web_fetch`; a note is stored as a source. See `docs/paste-intake.md`.

*Library.* Sidebar of smart folders grouped Workshops / Asset types / Views /
Saved. Facet chips with live counts over the filtered set. Text search and
meaning search, switchable. Tile size slider, default 170px, remembered.
Videos in their own row at the top of every folder. A detail panel with the
large preview, every provenance field, a clickable Drive link, copy credit
line, find similar, AI tags with accept and reject, status, release status,
quality, hero, notes and usage history. "Save current filters as folder".

*Inbox.* Everything on the keyboard: arrows to move, 1 to 5 for quality, A to
accept all AI tags, C for cleared, X to archive, H for hero. Clearing or
archiving drops the asset from the list so the next one slides under the cursor.

*Errors.* Dead jobs with a retry button, what is queued, and whether each
worker has checked in within five minutes.

*Jobs.* `ingest`, `embed`, `extract_doc`, `paste_intake`, `web_fetch` in
`workers/light`, at concurrency 4 with a heartbeat and graceful shutdown.

*Bulk upload.* `scripts/bulk-upload` has the rclone guide for pushing the
footage drive into `sfw-raw`, and a script that registers objects already there
as assets and enqueues ingest. Idempotent, so an interrupted rclone copy is
safe to resume.

**How to test**

Without any keys:

```bash
pnpm build && pnpm lint && pnpm typecheck
TEST_DATABASE_URL=postgres://postgres@127.0.0.1:5433/postgres pnpm test
```

59 tests. The 10 new ones run the library query against a real database: type
and status filters, tags that must all match rather than any, Untagged, Unused
before and after a post uses an asset, text search, paging, and facet counts
narrowing with the filter.

With your keys, once `pnpm db:setup` has run and a worker is up:

```bash
pnpm dev
# worker in another terminal:
WORKER_TYPES=ingest,embed,extract_doc,paste_intake,web_fetch \
  node workers/light/dist/index.js
```

1. Sign in at http://localhost:3000. Your address must be in `APP_ALLOWLIST`.
2. Library, Upload, fill in the batch fields, drop in the 30 fixture photos and
   the 2 videos. They appear immediately with thumbnails.
3. Within a minute each one has a description and suggested tags. Watch
   progress on `/errors`.
4. Search "steaming compost at sunrise" with the toggle on Meaning. Click a
   folder in the sidebar. Open one and check the Drive link opens.
5. Go to Inbox and clear the lot with A then C, without touching the mouse.
6. Paste a screenshot of a chat message. Within a minute the links in it have
   been fetched and turned into facts.

**Not done in this phase**

Uploading the actual fixtures, which needs R2 and Anthropic keys that only
Linnea can create. Everything the upload path does is exercised by the tests
except the two network calls out to R2 and Claude.

---

## Phase 3: Clipping machine

**What works**

- `workers/media` with FFmpeg: `proxy` (720p H.264 plus mono 16 kHz audio),
  `transcribe` (Whisper with word timestamps, splitting audio over 25 MB into
  ten-minute pieces and shifting the timestamps back), and `cut_clip`.
- `find_clips` on the light worker: Claude reads the transcript and proposes 12
  to 15 candidates against the expertise bar, the active reel rules and the
  hooks that performed best. Its timings are then snapped to real word
  boundaries and padded by 0.3 s, and anything that lands outside 20 to 60
  seconds is dropped.
- `cut_clip` cuts from the original in `sfw-raw`, centre crops to 9:16, 4:5,
  1:1 or 16:9, burns captions in the brand style with the current word picked
  out, and normalises loudness to -14 LUFS. It writes `captions.srt` alongside.
- The triggers from spec section 5, end to end: ingest on a video queues proxy
  and transcribe; transcribe queues find_clips when the video is over three
  minutes; find_clips queues a 9:16 preview for each candidate; Keep queues the
  other three ratios.
- Clips view: source videos on the left, candidates on the right with the hook,
  why, pillar, speaker and score, and Keep / Trim / Cut. Trim takes new
  boundaries and re-cuts. The header shows what the week proposed, what was
  kept, and the dollars per kept clip.

**How to test**

Without keys, the parts that can be tested in isolation are:

```bash
TEST_DATABASE_URL=postgres://postgres@127.0.0.1:5433/postgres pnpm test
```

80 tests. The 21 new ones cover the caption builder (two lines at most, every
word in exactly one window, breaking at a pause, one highlight per event, ASS
byte-order colours, brace escaping so a transcript cannot inject markup, and
each word held until the next begins) and the clip snapping (edges moved onto
real words, padding, never before zero, and dropping anything outside 20 to 60
seconds).

The FFmpeg pipeline itself was run end to end during the build against a
generated test video: probe, proxy, audio extraction, captions and all four
ratios cut at the exact requested duration with audio intact, and the burn-in
verified by diffing a captioned frame against a plain one.

With keys and a real video, follow "Running the contractor test on a real
workshop video" in `docs/RUNBOOK.md`.

**Known gap**

Whisper does not do speaker diarization, so every word has `speaker: null` and
the speaker on a clip is whatever Claude infers from the transcript. Real
diarization goes with the speaker-tracking crop in Phase 8.
