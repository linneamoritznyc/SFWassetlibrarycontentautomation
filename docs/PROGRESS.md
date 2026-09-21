# Progress

What works, and how to check it. Updated at the end of every phase.

| Phase | Name | State |
| --- | --- | --- |
| 0 | Repo and folders | done |
| 1 | Database and queue | done |
| 2 | Library (web) + ingest | done, except uploading the fixtures, which needs your keys |
| 3 | Clipping machine | done, except the contractor test, which needs a real video |
| 4 | Knowledge, writing and review | done, except a live end-to-end run, which needs keys |
| 5 | Planner, cron, export, results | done, except a live dry-run Monday, which needs keys |
| 6 | Self-improvement | done |
| 7 | Reels and Canva | done, except a live Canva round trip, which needs the integration |
| 8 | Scout, then polish | done, except deploying, which needs your accounts |

Paste intake (`docs/paste-intake.md`) is threaded through Phase 2 (capture and
the vision read) and Phase 4 (story and draft spin-up). No Drive, Google Chat or
Monday.com connection, by decision of 20 Sep 2026.

**Checked on 21 Sep 2026** against a local Postgres 16 with pgvector, which the
earlier sandbox did not have: `pnpm build`, `lint`, `typecheck` and
`format:check` clean; all 219 tests pass, including the 53 that need a
database; `pnpm db:setup` twice on an empty database applies ten migrations
then reports "No new migrations" and seeds the same counts; the eval CLI with
the model off scores 8 of 11; the cron one-shot queues `plan_week` once and
dedupes the second call. ffmpeg was installed and a caption burned: libass
now picks the brand face (see Phase 3 below and item 10 of the TODO).

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

- Ten migrations in `supabase/migrations`, covering every table in backend spec
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
# Applied: 0001_extensions.sql ... 0010_scout_global.sql
# Seeded: tags 88, smart_folders 16, people 12, settings 2,
#         planner_weights 10, prompts 11, test_cases 11, sources 6, feeds 27
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

**Font**

Captions burn in Montserrat SemiBold from
`packages/brand/fonts/Montserrat-SemiBold.ttf`, which the `ass` filter is
pointed at directly, so this holds on a laptop with nothing installed as well
as in the container. Verified 21 Sep 2026 by burning a caption with ffmpeg and
reading libass's own font selection line.

**Known gap**

Whisper does not do speaker diarization, so every word has `speaker: null` and
the speaker on a clip is whatever Claude infers from the transcript. Real
diarization goes with the speaker-tracking crop in Phase 8.

---

## Phase 4: Knowledge, writing and review

**What works**

- `brief` builds the briefing packet from spec section 6. Facts come from three
  places: linked to the story outright, the closest fifteen by meaning against
  the angle, and everything known about whoever is in the chosen images. It
  also carries the active rules for that platform, the three best past posts of
  the same shape, the brand rules and the calendar.
- `gap_check` lists what the writer would be assuming, looks each unknown up in
  the knowledge base, and only asks a person when it genuinely cannot answer
  itself. Questions are routed by topic through `people.topics`: programs to
  Stephanie, mentors and graduates to Carla, India and partners to Kavi,
  workshops to Loida, and anything unmatched to Stephanie. A blocking unknown
  holds the post at `revising` for 72 hours, then it goes to review flagged.
- `write` drafts with the chosen thumbnails attached, so the caption describes
  what is actually in the picture. Every run appends a `post_versions` row.
- `critique` is a separate call with a different prompt and the same images.
  The mechanical checks run first and cap the score at 55 if any fire.
  `must_fix` sends the draft back at most twice.
- `save_fact` turns an answer into permanent facts with the person's name on
  them and releases the post that was waiting.
- `web_refresh` re-queues every source page weekly, spread out so a burst of
  fetches does not look like an attack. `propose_story` decides whether a
  pasted link has a post in it, and which pillar, platform and visual.
- The six SFW pages from CLAUDE.md section 9 are seeded as sources.
- Week view: every post in a real phone frame at the right ratio, with the
  profile header and the caption truncated where Instagram truncates it. Why
  this post, the critic score and its must-fix list, and any question still
  unanswered behind it. Approve, edit inline, or reject with one of the five
  reason codes.
- Questions view: answer in one line, or drop it. Answering does the same thing
  as replying to the email.
- `POST /api/webhooks/email` takes replies. The signature is checked before
  anything is written, the question id is found in the address, the subject or
  the body, and the quoted original is stripped.

**How to test**

```bash
TEST_DATABASE_URL=postgres://postgres@127.0.0.1:5433/postgres pnpm test
```

98 tests. The 18 new ones cover the reply parsing (Gmail and Outlook quoting,
phone signatures, the three places a question id hides, signature verification
including the wrong-length case that would otherwise throw) and rule scoping.

With keys, the acceptance run from the build prompt:

1. Make a story by hand against a fixture asset, or paste a link and let
   `propose_story` make one.
2. A post on that story gets written and critiqued. Watch `/errors`.
3. If it needed something it did not know, `/questions` has a one-line question
   against a named person.
4. Answer it. The answer becomes facts, and the post is rewritten using them.
5. `/week` shows the draft in a real phone frame with the critic's score.

**Known gaps**

`build_post`, `render_reel`, `log_edit` and `log_rejection` are queued by the
approve, reject and edit buttons but their handlers arrive in Phases 5 to 7.
Until then those jobs sit in the queue, which is what should happen.

---

## Phase 5: Planner, cron, export and results

**What works**

- `workers/cron` with every schedule from spec section 5, in CET. It inserts
  job rows and does nothing else. One-shot mode for Railway cron triggers,
  long-running mode for anywhere else, both deduped so running both is safe.
- `plan_week`: slots from the cadence, a fifth held for experiments and spread
  so two never land next to each other, candidates scored with the spec's
  formula (relevance x freshness x material strength x format weight x pillar
  balance), and pillar balance computed from what actually ran in the last four
  weeks. Slots with no material become shot-list questions rather than empty
  posts.
- `write_batch` fans out the writing, spread over a few minutes.
- `review_ready_notify`: the Monday email with the link, the count, the open
  questions and what the week cost in AI. `questions_nudge` sends one reminder
  after 48 hours and only one.
- `build_post`: Sharp, 4:5 for feed and carousel, 9:16 for Stories and Reels,
  cropped towards the subject.
- `export_bundle`: a ZIP per run with one folder per post holding the media,
  `caption.txt` ready to paste, and `meta.json` with the time, platform,
  hashtags, collaborators and the UTM-tagged link. Exported posts then have
  their assets marked used.
- `results_pull` from the Instagram Graph API when both tokens are set, and a
  Later CSV import screen in Settings when they are not.

**How to test**

```bash
TEST_DATABASE_URL=postgres://postgres@127.0.0.1:5433/postgres pnpm test
```

133 tests. The 35 new ones cover slot generation against the cadence, the
exploration spread, the scoring formula and its decay, pillar balance, UTM
tagging, Instagram permalink parsing, and the Later CSV reader including quoted
cells with commas and newlines, thousands separators and the abbreviated "2.1k"
form.

The cron service was run for real against a local database: it queued a job,
deduped an immediate second call to the same row, and rejected an unknown job
name. Sharp was run against a real frame and produced 1080x1350 and 1080x1920.

With keys, the dry-run Monday:

```bash
node workers/cron/dist/index.js plan_week
node workers/cron/dist/index.js write_batch
node workers/cron/dist/index.js review_ready_notify
```

Then `/week` has the proposed week, each post critiqued, and an "Export
approved" button that writes the ZIP to `sfw-media` under `docs/exports/`.

---

## Phase 6: Self-improvement

**What works**

- `log_edit` measures what a human changed: a word-level diff that ignores
  punctuation, case and sentence order, plus the sentences dropped and added
  and the hashtags changed. The ratio is what the autonomy ladder reads.
- `log_rejection` stores the reason with enough of the post to see the pattern
  later, and puts the story back in the pool, since the angle may have been
  fine and the execution wrong.
- `learn_weekly` does six things in order: read four weeks of edits and
  rejections, propose rules that at least three separate posts argue for, test
  each candidate by handing it to the critic and re-running the whole test set,
  reweight the planner from saves and shares per impression with the spec's
  ±20% cap, promote barely-edited top-quartile posts to examples, and flag post
  types approved without edits nine times in ten. Then it writes one sentence a
  person can read.
- `eval_nightly` runs the test set, records the run, and rolls the active
  prompt back to its previous version if the pass rate dropped by more than ten
  points, emailing what failed.
- `scripts/eval` runs the same thing locally, with `--no-model` for the free
  half and `--activate` to promote a version that passed.
- "What it learned": rules in force with their evidence and origin, rules that
  were proposed and discarded for making the test set worse, the planner
  weights with how many data points are behind each, and the eval history with
  the failures named.

**How to test**

```bash
TEST_DATABASE_URL=postgres://postgres@127.0.0.1:5433/postgres pnpm test
```

151 tests. The 18 new ones cover the diff (zero when nothing changed, small for
a tweak, large for a rewrite, unchanged by reordering, handles for
`@visionary_permaculture` kept whole, empty drafts without dividing by zero)
and the evaluator running against the real seeded test set.

The eval CLI was run against a live database:

```
8 of 11 (73%)
```

with the model off, failing exactly the three cases that need judgement, which
is the honest answer rather than a pass.

**How to use it**

Changing a prompt is: edit `packages/prompts/src/`, bump the version, seed,
run the eval, activate. A new version is seeded inactive, so a prompt change
cannot reach production just by being deployed.

---

## Phase 7: Reels and Canva

**What works**

- `packages/remotion` with the two templates the build prompt named. **Field
  Notes** carries the series convention from CLAUDE.md section 7: the eyebrow
  number and a subtitle with the named person, place and season. **Workshop
  moment** leads with the speaker's own line and names who said it and where.
  Both have the intro card, the clips, the end card with the CTA, and the
  wordmark, in the brand greens and cream with cream used as a shape.
- Each composition works out its own length from the clips it is given, so a
  render is never padded or cut short.
- `render_reel` in `workers/render`: bundles once per process, hands the clips
  over as presigned URLs, renders at 1080x1920 H.264, uploads to
  `renders/{id}.mp4` and points the post at the render row.
- Canva Connect: the PKCE OAuth flow at `/api/canva/auth` and its callback,
  tokens encrypted with AES-256-GCM before they touch the database,
  `canva_push` (upload by URL into a folder, create an Instagram-sized design,
  save the edit URL on the post) and `canva_pull` (export the finished design
  and bring it back as a `render` asset the post then points at).
- Autofill is behind its own flag, off until Canva approves that scope.
- A Connect Canva button in Settings.

**How to test**

```bash
TEST_DATABASE_URL=postgres://postgres@127.0.0.1:5433/postgres pnpm test
```

163 tests. The 12 new ones cover the token encryption: a round trip, a
different ciphertext each time, refusing a tampered ciphertext and the wrong
key, a key of the wrong length, and the authorize URL asking for every scope
the jobs need with PKCE set to S256.

A Reel was rendered end to end during the build: the templates bundled, a
headless Chromium rendered 1080x1920 H.264, and the output was 11.05 seconds
for a 2.5s intro, a 6s clip and a 2.5s end card. The intro card came out on
brand: deep green, the hook in a cream block, the attribution under it, the
wordmark bottom left.

With the integration connected, the round trip is: approve a photo post, which
queues `build_post` and then `canva_push`; open the edit URL on the post;
finish it on the existing SFW templates; then run `canva_pull` to bring it back
into the library as the asset the post goes out with.

**Needs you**

`TOKEN_ENC_KEY` has to be generated before Canva can connect, and the Remotion
licence is worth checking. Both are in `docs/TODO-LINNEA.md`, items 11 and 12.

---

## Phase 8: Scout, then polish

**What works**

- `scout_fetch` reads fourteen seeded feeds across soil research, policy in the
  EU, US and India, the partners, the permaculture network and the regenerative
  agriculture press. A feed that fails is reported and skipped rather than
  taking the run down with it.
- `scout_rank` summarises each item with Haiku, scores its relevance, links it
  to the nearest facts and assets by meaning, and turns anything at 0.7 or
  above into a story candidate. It works in batches of forty and re-queues
  itself.
- Scout view: cards sorted by relevance with what the Foundation already knows
  that touches them and whether the library has anything to carry them. Make a
  story, or dismiss.
- Speaker-tracking crop in `cut_clip`, behind its flag: OpenCV finds the
  largest face twice a second, and the track is filled, averaged and
  speed-limited before it becomes an ffmpeg crop expression. It drifts rather
  than chases.
- The light editor: trim, split and reorder as one list of segments, caption
  fixes applied to the words before they are burned in, crop focus, and a music
  bed mixed under the speech. One save, one re-render.
- Settings: the cadence, who answers what with editable emails, the feeds with
  on/off switches, the live prompt versions read-only, a thirty-day cost table
  by prompt and model, the Canva connect button, the Later CSV import, and
  worker heartbeats.
- Deploy: `vercel.json` for the web app, a `railway.json` per worker, and a
  health endpoint on each worker that answers 200 only when the database is
  actually reachable.

**How to test**

```bash
TEST_DATABASE_URL=postgres://postgres@127.0.0.1:5433/postgres pnpm test
```

193 tests. The 30 new ones cover the RSS parser against fixtures of all four
shapes real feeds come in, the speaker-track smoothing (holding position
through frames with no face, never cropping outside the frame, drifting rather
than chasing, ignoring jitter), the crop expression, and the caption
corrections.

The moving crop and the multi-segment edit were both run through real ffmpeg
during the build: two segments in reverse order concatenated to exactly 4.00s
with a music bed mixed under, at the right dimensions and codecs.

**Known gap**

The sandbox this was built in could not reach the open internet, so the feed
URLs are plausible rather than confirmed. See `docs/TODO-LINNEA.md` item 13.

---

# Everything, and how to check it

The final checklist. Each row is something the system does and the quickest way
to see it doing it.

## Before any of it works

`docs/TODO-LINNEA.md` has thirteen things only you can do: the Supabase
project, the two R2 buckets, the API keys, the Canva integration, the token
encryption key, the team's email addresses. Until the first four are done,
`pnpm dev` shows a page telling you so.

```bash
cp .env.example .env.local     # fill it in
pnpm install && pnpm db:setup  # ten migrations, then the seed
pnpm dev                       # web on :3000
```

Workers, in other terminals:

```bash
node workers/light/dist/index.js     # claims everything it can do
WORKER_TYPES=proxy,transcribe,cut_clip,build_post,edit_clip \
  node workers/media/dist/index.js
WORKER_TYPES=render_reel node workers/render/dist/index.js
node workers/cron/dist/index.js      # or one-shot: ... dist/index.js plan_week
```

## Library

| It does | Check it by |
| --- | --- |
| Signs you in by magic link, allowlist only | Sign in. Try an address not in `APP_ALLOWLIST`: it is turned away. |
| Batch upload with provenance entered once | Library, Upload. Fill in workshop, creator, Drive link. Drop 30 photos. |
| Thumbnails and EXIF in the browser | They appear immediately, with the date and camera on the detail panel. |
| Uploads straight to R2 | Network tab: the PUTs go to `r2.cloudflarestorage.com`, not to the app. |
| Describes and tags each asset | Within a minute each has a description and suggested tags. |
| Meaning search | Toggle to Meaning, search "steaming compost at sunrise". |
| Find similar | Open an asset, Find similar. |
| Smart folders as saved filters | Click a workshop in the sidebar. Filter, then Save current filters as folder. |
| Videos in their own row | Any folder with a video in it. |
| Drive link and credit line | Detail panel, Open original in Drive, Copy credit line. |
| Inbox on the keyboard | `/inbox`: arrows, 1 to 5, A, C, X, H. No mouse. |
| Dead jobs with retry | `/errors`. |

## Paste

| It does | Check it by |
| --- | --- |
| Reads a pasted screenshot | Cmd-V a screenshot of a chat message on `/library`. |
| Pulls out sender, message and links | The reference asset's description, within a minute. |
| Fetches each link and extracts facts | `/errors` shows `web_fetch` then `propose_story`. |
| Refuses to use the screenshot as a visual | The asset is `reference` and its notes say so. |
| Sends outside news to LinkedIn | The proposed story's platform. |

## Clips

| It does | Check it by |
| --- | --- |
| Proxy and transcript on upload | Upload a video. It gets a 720p proxy and a transcript. |
| Finds clips over three minutes | `find_clips` runs on its own; or press Find clips. |
| 12 to 15 candidates on word boundaries | `/clips`. Each has a hook, why, pillar, speaker and score. |
| Cuts at four ratios with captions | Keep one. The other three ratios are cut. |
| Loudness at -14 LUFS | `ffmpeg -i clip.mp4 -af ebur128 -f null -` |
| Captions in Montserrat, not DejaVu | Run the cut with `-loglevel debug`: libass logs `fontselect: (Montserrat SemiBold, 700, 0) -> Montserrat-SemiBold`. |
| Cost per kept clip | The header on `/clips`. |
| Trim, split, reorder, caption fixes, music | Edit on any clip. |
| Follows the speaker | Turn on `speaker_tracking_crop` in the `flags` setting. |

## Writing and review

| It does | Check it by |
| --- | --- |
| Builds a briefing from facts, images and rules | Any post's write job. |
| Asks a person what it does not know | `/questions`. |
| Turns an answer into facts and rewrites | Answer one. The post is rewritten using it. |
| Refuses a post with no material | Try approving one. The database refuses it. |
| Critiques with the images attached | The critic score and must-fix list on `/week`. |
| Catches em dashes, acronyms and AI cadence | They cap the score at 55. |
| Shows posts in real phone frames | `/week`: the caption truncates where Instagram truncates. |
| Approve, edit inline, reject with a reason | The buttons on each post. |
| Answers by email reply | Reply to a question email. |

## The week

| It does | Check it by |
| --- | --- |
| Plans a week from the cadence | `node workers/cron/dist/index.js plan_week` |
| Holds a fifth of slots for experiments | Posts marked experiment on `/week`. |
| Turns a slot with no material into an ask | `/questions`. |
| Writes and critiques everything | `write_batch`, then `/week`. |
| Monday email with link, count, questions, cost | `review_ready_notify` |
| Exports a ZIP for Later | Export approved on `/week`. Look in `sfw-media/docs/exports/`. |
| Pulls results, or takes a CSV | `results_pull`, or Settings, Import results. |

## Learning

| It does | Check it by |
| --- | --- |
| Measures what you changed | Edit a post. The diff lands on the version row. |
| Proposes rules from three or more edits | `learn_weekly` |
| Tests a rule before switching it on | `/learned` shows rules proposed and discarded. |
| Reweights the planner, capped at 20% | `/learned`, the weights table. |
| Promotes barely-edited top posts to examples | They appear in the next briefing. |
| Flags what could go to lighter review | `/learned`, top of the page. |
| Rolls a prompt back on a regression | `eval_nightly`, or `scripts/eval` locally. |

## Reels and Canva

| It does | Check it by |
| --- | --- |
| Renders Field Notes and Workshop moment | Approve a reel post. |
| Works out its own length | The MP4 is intro plus clips plus end card, exactly. |
| Sends a post into Canva | Settings, Connect Canva, then approve a photo post. |
| Brings the finished design back | `canva_pull`. The post points at the new asset. |

## Scout

| It does | Check it by |
| --- | --- |
| Reads 27 feeds daily, across 7 regions | `node workers/cron/dist/index.js scout_fetch` |
| Ranks and links to what we know | `/scout` |
| Promotes anything at 0.7 or above | It becomes a story candidate. |
| Summarises a non-English item in English | The card shows the English summary, the source's own title under it, and a language badge. |
| Shows which region a story came from | The badge on each Scout card. |
| Notices a feed that stopped working | Settings, Feeds panel. Failures sit at the top with the actual error. |
| Switches a feed off after 5 failures | Settings shows it as switched off automatically. |
| Tests every feed URL in one go | `pnpm feeds:check` |

## What it costs

Settings has a thirty-day table by prompt and model. The spec estimated $140 to
$190 a month all in, of which $20 to $40 is Claude. The rest is storage,
Supabase, Railway and Whisper, billed by those providers.
