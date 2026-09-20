# Decisions

Every choice made where the PRD and the backend spec were silent or disagreed.
Newest last. Format: date, decision, why.

## Phase 0

**2026-09-20 — The spec wins over the PRD.**
Standing rule from the build prompt, written here so it is visible from the code
side too. Two places it already bites:

- PRD 5.4 says Claude picks 5 to 10 clip moments; spec section 6 `find_clips`
  says 12 to 15 candidates. Using 12 to 15. The PRD's own "propose 12 to 15 so
  the weakest get cut" later in the same section agrees with the spec.
- PRD 8 numbers the build phases differently from spec 13 and from the build
  prompt (its Reel phase is 5, its scout phase 6, its editor 7). The build
  prompt's Phase 0 to 8 numbering is what `docs/PROGRESS.md` tracks.

**2026-09-20 — Model ids live in env, not in code.**
The build prompt names `claude-sonnet-4-6` as the default and haiku for scout
ranking. Those are the defaults in `.env.example`, but every call reads its id
from `ANTHROPIC_MODEL_DEFAULT` / `_CHEAP` / `_LONGFORM`, so swapping a model is a
config change and never a code change. Note for Linnea: newer Claude models
exist (the Claude 5 family). The pinned ids are what the build prompt asked for,
not a recommendation.

**2026-09-20 — Turborepo 2 task syntax.**
`turbo.json` uses the `tasks` key (Turborepo 2.x), not the `pipeline` key from
1.x. No version was pinned, so this is the current one.

**2026-09-20 — ESLint flat config, one file at the root.**
A single `eslint.config.js` covers every workspace rather than one config per
package. Less to keep in sync, and the rule set is identical everywhere anyway.

**2026-09-20 — Embedding dimension 1024 comes from an OpenAI model.**
The spec fixes `vector(1024)` but names no embedding provider. Using OpenAI
`text-embedding-3-small` with `dimensions: 1024`, because the OpenAI key is
already required for Whisper and Anthropic ships no embedding endpoint.

**2026-09-20 — Transactional email is Resend.**
Spec section 6 needs to email questions to named people and take their replies
back through `POST /api/webhooks/email`, and spec section 5 needs the Monday
notice, but neither document names a provider. Resend: cheap, has inbound
parsing, one env var. `RESEND_API_KEY` is added to `.env.example` even though it
is not in spec section 12, since section 12 lists no mail variable at all.

**2026-09-20 — `.env.example` carries a few variables spec 12 omits.**
`NEXT_PUBLIC_APP_URL` (magic-link redirects and the Monday email's link),
`OPENAI_WHISPER_MODEL`, and the three model ids above. Everything in spec 12 is
present and unchanged.

## Requirement change, 20 Sep 2026

**2026-09-20 — No Drive, no Google Chat, no Monday.com. Paste is the interface.**
Linnea's call. The spec already ruled out Google Drive (section 9, and PRD
constraint 3); this extends it to Google Chat and Monday.com, which were never
in either document but are the obvious next things someone would wire up. The
replacement is a paste intake: drop a screenshot, a link or text into the inbox
and the machine reads it, fetches what it links to, turns it into sourced facts,
and proposes a story with an angle. Designed in `docs/paste-intake.md`. Capture
and the vision read go in Phase 2, the story and draft spin-up in Phase 4.

Three things follow from it, and each one is a rule in code rather than a note:

- A pasted screenshot is `assets(type=reference)`: provenance, never a post
  visual. CLAUDE.md section 5 allows real SFW images only.
- Outside news goes to LinkedIn first with a real question at the end, per
  CLAUDE.md section 4, not to Instagram by default.
- Someone else's research keeps its own evidence rung. It is cited, never
  restated as an SFW claim.

**2026-09-20 — `paste_intake` and `propose_story` are new job types.**
Neither is in spec section 6. They are additions, not replacements, and they
reuse `sources`, `facts`, `stories` and `assets(type=reference)` exactly as the
schema already defines them, so no table changes. `web_fetch` is the single-URL
version of the spec's `web_refresh`.

## Phase 1

**2026-09-20 — Workers connect to Postgres directly; the web app uses supabase-js.**
The queue is a polling loop, and routing `claim_job` through PostgREST would be
an HTTP round trip per tick for what is one `update ... returning`. So
`packages/queue` and `packages/db` take a `DATABASE_URL` (the connection string
from the Supabase dashboard, pooled, port 6543) and `apps/web` keeps supabase-js
for auth and the query builder. `DATABASE_URL` is not in spec section 12; it is
added to `.env.example` with the rest.

**2026-09-20 — RLS on every table, with no policies at all.**
Spec section 9 says "Row Level Security on all tables; API routes use service
role server-side only". The simplest thing that means is: enable RLS, write zero
policies, and revoke the grants from `anon` and `authenticated` as well. Only a
role with `bypassrls`, which is what Supabase's service_role has, gets through.
A key that ever leaks into a browser can then read nothing. Also `force row
level security`, so the table owner is not an exception either.

**2026-09-20 — `dedupe_key` is unique only among live jobs.**
The spec writes it as `dedupe_key text unique null`, which would mean a key could
be used once in the lifetime of the database: after the first `embed:<asset_id>`
finished, that asset could never be re-embedded. Instead there is a partial
unique index over `status in ('queued','running')`. A duplicate is blocked while
the work is pending and the key frees up when it finishes, which is what makes
"re-tag this asset" and the Errors view's retry button work at all.

**2026-09-20 — `claim_job` takes an optional second argument.**
`claim_job(types text[], lim integer default 1)`. The spec's one-argument call
still works. A worker at concurrency 4 with four free slots should claim four
jobs in one round trip rather than four.

**2026-09-20 — Seven additions to the schema, all of them things a spec job needs.**
Each one exists because a job in spec section 6 or a screen in section 8 has
nowhere else to put its state:

- `asset_usage` — `link_asset_usage` says "usage rows written"; the library's
  "used in" list and the Unused view read it.
- `planner_weights` — `learn_weekly` updates `format_weight` and
  `pillar_balance` and the planner reads them back.
- `settings` — the cadence config and the feature flags, editable from the
  Settings view.
- `worker_heartbeats` — spec section 10's red dot after 5 minutes.
- `posts.is_example` — `learn_weekly` step 4 promotes posts to examples and
  `brief` reads back the three best of a format.
- `questions.created_at` and `nudged_at` — the hourly nudge at 48 h and the
  `gap_check` timeout at 72 h both need to know when the question was asked.
- `people.topics` — this *is* the question-routing map. Rather than a separate
  table, each person carries the topics they answer for, so routing is one
  query and adding a topic is editing a person.

**2026-09-20 — Three rules enforced by the database, not only by code.**
`post_has_material` (a post past `proposed` has at least one asset or a render,
which is PRD principle 1), `rejection_has_reason`, and `clip_has_range`. A check
constraint cannot be forgotten by a future job, and the first of these is the
rule the whole product rests on.

**2026-09-20 — Seed data lives in TypeScript, not in SQL.**
The tag vocabulary, cadence and people are read at runtime by the workers as
well as written once by the seeder. Keeping them in `@sfw/shared` and seeding
from there means one source of truth; a `supabase/seed.sql` would drift from the
copy the tagger actually offers Claude. `supabase/migrations` stays pure SQL.

**2026-09-20 — A new prompt version is seeded inactive.**
Seeding activates a prompt only when its name has no active version at all,
which is the first run. After that, a new version arrives dormant and something
has to run the test set and promote it. That is what makes PRD 7.4 true in
practice: a prompt change cannot reach production just by being deployed.

**2026-09-20 — The two good test cases are reconstructed, and say so.**
The real Pratik and Sandra captions are not in any of the source documents. The
seeded versions are built from the details CLAUDE.md records (moisture range,
aggregates, air channels, no foul smell; Van, Texas, butternut squash on fallow
clay and sand) and each one's `notes` field says it is a reconstruction. They
test the shape and the discipline. Swap in the real text when you have it:
`docs/TODO-LINNEA.md`.

**2026-09-20 — `tsconfig.json` for typechecking, `tsconfig.build.json` for building.**
Tests are typechecked but do not end up in `dist`.

## Phase 2

**2026-09-20 — Supabase for who you are, Postgres for everything else.**
A refinement of the Phase 1 decision. `apps/web` uses supabase-js only for
magic-link auth and the session cookie; every data read and write in the API
routes goes through the same `pg` pool the workers use. The library query is
joins, aggregated tag arrays, facet counts and a vector ordering, and the
PostgREST query builder would fight all four. One query language across the
whole codebase is also one fewer thing to learn.

**2026-09-20 — The allowlist is enforced in middleware, once.**
Not per page and not per route. An empty or missing `APP_ALLOWLIST` means
nobody gets in, not everybody: failing closed is the only safe reading of a
variable that has gone missing in production. Someone signed in but not on the
list is told so rather than bounced in a loop.

**2026-09-20 — Thumbnails are made in the browser.**
800px JPEG at quality 0.82, from a canvas; for video, a frame at two seconds.
It means a 4 GB original never has to be read by a server just to get a preview
out of it, and the upload is one presigned PUT for the file and one for the
thumbnail. A codec the browser cannot decode is not an error: the asset uploads
without a thumbnail and the media worker makes one in Phase 3.

**2026-09-20 — `ingest` moves an asset to `tagged`, and the Inbox shows both.**
The spec calls the output of `ingest` a "tagged-in-inbox asset", and the DB
trigger that creates the `embed` job fires on `status = 'tagged'`. So ingest
sets `tagged`, which is what makes an asset searchable, and the Inbox view
filters `status in ('inbox', 'tagged')` so it is still sitting there waiting for
a human to confirm the tags. Clearing or archiving is what takes it out.

**2026-09-20 — Confirming a tag keeps `source = 'ai'`; rejecting deletes the row.**
Confirming only flips `confirmed`, so the library still knows the AI suggested
it and `learn_weekly` can measure how often its guesses survive. Rejecting
removes the row outright, because `ingest` clears only its own unconfirmed rows
on a re-run and a rejected suggestion coming straight back would be the most
annoying possible behaviour.

**2026-09-20 — A pasted screenshot is uploaded through the API route.**
Everything else gets a presigned PUT straight to R2, but a screenshot is a
couple of megabytes and the two-step presign dance would put a visible pause
between pasting and anything happening. Capped at 12 MB; anything bigger is an
upload, not a paste.

**2026-09-20 — Plain `<img>`, not `next/image`.**
Every thumbnail is a presigned R2 URL whose host and query string change every
hour. `next/image` cannot cache that and would only proxy it.

**2026-09-20 — Relative imports in `apps/web` carry no `.js` extension.**
The packages are ESM under NodeNext and need the extension; Next uses bundler
resolution and its webpack build fails with it. The two conventions sit either
side of the workspace boundary.

## Phase 3

**2026-09-20 — Whisper does not do speaker diarization, so `speaker` comes back null.**
Spec section 6 asks `transcribe` for "word timestamps, speaker diarization".
Word timestamps it does; diarization it does not, and nothing in the OpenAI API
does. Real diarization means pyannote, a Hugging Face token and a GPU-ish
workload, which is a bigger dependency than this phase can justify. So every
word carries `speaker: null`, and `find_clips` fills in the speaker from what
is being said and who the transcript names. Proper diarization sits with the
speaker-tracking crop in Phase 8, where the same face detection would feed it.

**2026-09-20 — Captions are ASS, not SRT.**
SRT cannot colour part of a line, and the spec wants the word being spoken
picked out. The burner emits one ASS dialogue event per word, each showing the
same one or two lines with a different word highlighted, which produces the
word-by-word effect with no animation and nothing to go out of sync. The `.srt`
the spec stores next to each clip is still written, for anything that wants
plain captions.

**2026-09-20 — Audio is split by time, not by size.**
Whisper refuses anything over 25 MB. Splitting into ten-minute pieces of 64k
mono keeps each one well under, and shifting the word timestamps back is then
multiplication rather than bookkeeping.

**2026-09-20 — Clips are cut from the original, never from the proxy.**
The proxy is 720p. A 9:16 crop out of it would be soft on a phone. The cut uses
`-ss` before `-i` so seeking a multi-gigabyte file is fast, and because the
video is re-encoded anyway the cut still lands on the exact frame.

**2026-09-20 — Only 9:16 is cut up front; the other ratios wait for Keep.**
Fifteen candidates times four ratios is sixty encodes, and twelve of the
candidates get thrown away. The preview is 9:16 because that is what most
clips go out as; pressing Keep cuts the rest.

**2026-09-20 — A candidate that snaps outside 20 to 60 seconds is dropped, not trimmed.**
Trimming it back into range would cut mid-sentence, which is the exact thing
the snapping exists to prevent. The model is asked for 12 to 15 candidates so
losing one or two to this costs nothing.

**2026-09-20 — `find_clips` clears only untouched candidates on a re-run.**
A clip somebody kept, trimmed or archived is theirs. Re-running replaces the
ones still sitting at `inbox` and never used.

**2026-09-20 — Montserrat is downloaded at image build, with a fallback.**
It is not in the Debian archive. The `workers/media` image fetches it from
Google Fonts under the Open Font License; if that fails the build still
succeeds and fontconfig falls back to DejaVu Sans Bold, which is legible but
off brand. Logged in `docs/TODO-LINNEA.md` as something to check after the
first deploy.

## Phase 4

**2026-09-20 — `gap_check` needs both similarity and confidence before it answers itself.**
An unknown is only treated as answered when the nearest fact is close in
meaning (similarity above 0.55) *and* the fact itself is confident (0.8, which
is the spec's number). Either alone is not enough: a confident fact about
something else is worse than no fact, because it produces a post that is wrong
rather than a post that is late.

**2026-09-20 — The mechanical checks run inside the critic and cap the score.**
`runStringChecks` runs before the Claude call and its hits are added to
`must_fix`. A regular expression cannot be talked out of an em dash, and a
draft that trips one is capped at 55 however well the critic rated the rest.

**2026-09-20 — The rewrite loop stops at two, and the post goes to review anyway.**
With the critic's notes attached. A loop that never terminates is worse than a
draft a human has to fix, and by the third pass the model is usually arguing
rather than improving.

**2026-09-20 — The gap check runs on the first pass only.**
A rewrite is answering the critic, not re-asking the same questions. Running it
every loop would re-ask a person who has not had time to reply.

**2026-09-20 — `propose_story` may only pick a visual from the assets it was handed.**
The returned ids are filtered against what was offered. A hallucinated id would
otherwise become a post with a picture nobody chose. When nothing fits, the
story is created without a visual and a question goes out asking for one,
rather than the post borrowing the linked page's photograph.

**2026-09-20 — Replies are parsed for the question id in three places.**
The reply-to address (`questions+42@`), then `[#42]` in the subject, then a
marker in the body. Providers and mail clients mangle different ones. The
quoted original is stripped before anything is stored, or answering "it closes
on the 21st" would file the question itself as a fact.

**2026-09-20 — An answered question is worth more than a web page.**
Facts from `save_fact` get a confidence floor of 0.85 and carry the person's
name in `confirmed_by`. A named colleague saying so outranks a page that might
be a year out of date.

## Phase 5

**2026-09-20 — The cron service runs two ways.**
`node dist/index.js plan_week` enqueues one job and exits, which is what a
Railway cron trigger calls. With no argument it stays up and fires on its own
schedule, which is what local development and any host without a scheduler
needs. Both use the same dedupe key, so running both at once is harmless rather
than double work.

**2026-09-20 — The slots come from code, the choices come from the model.**
How many posts a week is a decision, not a judgement: the cadence produces the
slots and marks a fifth of them as exploration before the planner sees them.
What goes in each slot is the judgement, and every candidate arrives
pre-scored, so Claude is arguing against arithmetic rather than inventing it.

**2026-09-20 — Freshness halves every three weeks.**
Nothing in the spec fixes the decay. Three weeks means a month-old story has to
be about twice as good as a new one to take a slot, which matches a cadence of
three feed posts a week.

**2026-09-20 — The planner filters the asset ids it is given back.**
Only ids that exist and are cleared or tagged survive. A hallucinated id would
otherwise become a post with a picture nobody chose. A slot whose assets all
fail becomes a shot-list question instead.

**2026-09-20 — `write_batch` spreads the writes over a few minutes.**
Each post is two or three Claude calls. A dozen starting at once is a rate
limit, not a fast week.

**2026-09-20 — Email falls back to the console.**
Without `RESEND_API_KEY` the Monday notice and the question nudges are logged
instead of sent, and the whole system still works: the Week and Questions views
are the other way in. It means Linnea can use this before she has a mail
provider.

**2026-09-20 — One nudge, tracked by `nudged_at`.**
The hourly job only picks up questions that have never been nudged. A second
reminder is nagging, and nagging is how people start ignoring the first one.

**2026-09-20 — `build_post` crops towards the subject and stays plain.**
Sharp's attention crop rather than a centre crop, so a photo of a person does
not lose their head to a 4:5 frame. No type is drawn on: CLAUDE.md section 5
says graphics are built on the existing Canva templates with real photos
swapped in, so anything with words on it goes through Canva in Phase 7.

**2026-09-20 — The Later CSV is matched by what a header contains.**
Later's column names have changed more than once and differ by plan. The
importer matches loosely, understands "12,480" and "2.1k", and reports which
columns it could not find rather than quietly importing zeros.

**2026-09-20 — Export writes a ZIP to R2 rather than streaming it.**
A week of posts with video in it is too big to hold in a serverless response,
and the bundle is worth keeping: it is the record of exactly what was handed
over. A missing file becomes a `MISSING.txt` inside the bundle rather than
losing the whole export.

## Phase 6

**2026-09-20 — The edit diff is word-level and order-insensitive.**
"vermicompost" becoming "worm castings" is one change, not eleven characters,
and moving a sentence is not an edit in any sense that matters. So it is a
multiset difference over words rather than a character edit distance. A true
Levenshtein over a caption is a lot of work to answer a question that "which
words are gone" already answers.

Underscores are kept when splitting words, because `@visionary_permaculture` is
one token and splitting it would read as an edit on every post carrying the
collab tag.

**2026-09-20 — A candidate rule is tested by handing it to the critic.**
The whole test set is run with the candidate added to the active rules, and the
rule only goes live if nothing that used to pass now fails. A rule that makes
the critic flag the Pratik post is a bad rule however sensible it reads. Rules
that fail are still written to the table, inactive, so the "What it learned"
screen can show what was proposed and rejected.

**2026-09-20 — The eval is an eval of the critic.**
The test cases are captions to be judged, so running them means asking the
critic to judge them: a good caption must come back clean and well scored, a
bad one must be caught. That is what makes the nightly rollback meaningful.
Running with `--no-model` exercises the mechanical half for free, and honestly
fails the three cases that need judgement rather than passing them.

**2026-09-20 — A bad case caught for the wrong reason still counts as caught.**
The post does not go out either way. The report says which check actually fired
so a drift in the critic's reasoning is visible, but it is not a failure.

**2026-09-20 — Weights move by a capped moving average, and only with three data points.**
The cap is the spec's ±20% a week; the moving average is the midpoint between
the current weight and the capped target, so a weight drifts rather than jumps.
A format with fewer than three posts behind it is left alone, which is what
makes the exploration slots worth having: an untried format is not penalised
for being untried.

**2026-09-20 — A rejected post's story goes back in the pool.**
The angle may have been fine and the execution wrong. The story returns to
`candidate` rather than dying with the post.

**2026-09-20 — Rejections are stored as version rows.**
Same table as edits, with `diff.rejected = true` and the reason, so
`learn_weekly` reads corrections from one place instead of joining two.

## Phase 7

**2026-09-20 — The Remotion bundler is told to resolve `.js` to `.tsx`.**
The package's own `index.ts` and `schema.ts` are compiled by tsc and loaded by
the render worker as Node ESM, which needs the `.js` extension on relative
imports. Remotion bundles with webpack, which resolves like a bundler and looks
for a literal `.js` file. Rather than run two import conventions in one folder,
the bundler is given `extensionAlias: { '.js': ['.js', '.ts', '.tsx'] }`.

**2026-09-20 — `@sfw/remotion` exports its own `package.json`.**
The render worker resolves the bundler entry point from the installed package
rather than guessing a relative path, so it works the same in the Docker image
as from the repository root. That needs `./package.json` in the exports map.

**2026-09-20 — Clips are handed to the renderer as presigned URLs.**
Remotion fetches them itself while rendering. Downloading three clips first
would mean a few hundred megabytes on disk before anything starts.

**2026-09-20 — A composition works out its own length.**
`calculateMetadata` sums the clips plus the two cards, so a render is never
padded with black or cut short. The job hands over clips; the composition is
exactly as long as they are.

**2026-09-20 — Canva helpers live in `@sfw/shared/canva`, a server-only subpath.**
Both the web app's OAuth routes and the worker's push and pull jobs need them.
They use `node:crypto`, so exporting them from the main entry point pulled that
into the client bundle and broke the Next build. A separate subpath keeps the
main entry point safe for components.

The pool-dependent functions take a minimal `Queryable` interface rather than
importing `@sfw/db`, so `@sfw/shared` still has no database dependency.

**2026-09-20 — Canva tokens are stored in `settings`, not a table.**
There is exactly one Canva account. A table for one row is a table that will
be wrong about something later. They are AES-256-GCM encrypted with a fresh IV
each time, so two encryptions of the same token do not look alike.

**2026-09-20 — The OAuth flow uses PKCE even though the exchange is server-side.**
The browser does the redirect, so an intercepted code is otherwise usable. The
verifier never leaves the server, and the state cookie is httpOnly, scoped to
`/api/canva` and expires in ten minutes.

**2026-09-20 — Connecting Canva switches it on.**
The callback sets `canva_enabled`. Going through an OAuth flow is a clear
enough statement of intent; making someone then find a toggle would be
pointless. Autofill stays behind its own flag until Canva approves that scope.

## Phase 8

**2026-09-20 — A feed that fails is reported, not thrown.**
One dead URL out of fourteen should not stop the other thirteen. `scout_fetch`
collects the failures and logs them together, and the Settings view shows a
feed with no items so a dead URL is visible rather than silent.

**2026-09-20 — The feed list could not be verified from the build sandbox.**
Every outbound request to a feed was refused by the sandbox proxy, so the URLs
in `packages/shared/src/feeds.ts` are plausible rather than confirmed. The
parser is tested against fixtures of the four shapes real feeds come in (RSS
2.0, Atom with the link in an attribute, RDF, and a single non-array item),
which is the part worth testing anyway. Checking the feeds is in
`docs/TODO-LINNEA.md`.

**2026-09-20 — `scout_rank` works in batches and re-queues itself.**
Forty items a run. A hundred items in one job is a job that runs for ten
minutes and loses everything if it dies at minute nine.

**2026-09-20 — OpenCV is pinned below 5.**
OpenCV 5 dropped the bundled Haar cascades, and its DNN replacement needs a
model file fetched at runtime, which is a network dependency inside a container
that should not need one.

**2026-09-20 — The speaker crop drifts rather than chases.**
Three passes over the detections: carry the last known position through frames
with no face, average over a window, then limit the speed to a quarter of the
frame a second with a deadzone. A crop that snaps to every detection is
unwatchable and worse than the centre crop it replaced. Half of workshop
footage is someone's hands in compost, so holding position through a gap
matters more than reacting quickly.

**2026-09-20 — The crop expression steps rather than interpolates.**
An ffmpeg expression with interpolation between a dozen keypoints is
unreadable, and a step every half second under a deadzone is not visible.
Points where nothing changed are dropped, so a static shot compiles to a
constant.

**2026-09-20 — Trim, split and reorder are one list of segments.**
They are three verbs for the same operation. The editor offers three buttons
and `edit_clip` implements one thing, which is also why a round of changes is
one re-render rather than four.

**2026-09-20 — Prompts are read-only in Settings.**
Editing one in a text box would let a change reach production without passing
the test set, which is the one rule the self-improvement loop rests on. The
screen shows which version is live; changing it goes through the eval.

**2026-09-20 — The worker health endpoint checks the database, not the process.**
"The process is running" is not the question worth asking: a worker that cannot
reach Postgres is up and useless. It answers 200 only when a query succeeds,
and it only listens when `PORT` is set, because a worker otherwise needs no
socket.

**2026-09-20 — There are no down migrations.**
An automatic reverse of a destructive change is a way to lose data twice. To
undo a migration, write a new one that undoes it, so the history stays
forwards-only and readable. Supabase's point-in-time recovery is the right tool
when data is actually lost.

**2026-09-20 — The scout source list is global, and non-English feeds are welcome.**
A source list that is all English-language North American press would keep
handing the planner the same five stories, and the Foundation has graduates in
over 100 countries. The list now reaches the UN bodies, the research networks
and the regional programmes: FAO Global Soil Partnership, UNCCD, IPBES, CGIAR,
WRI, the African Union, AGRA, Regeneration International, Embrapa, IICA, Soils
For Life, APCNF, ICRISAT, the EU Soil Observatory, and the rest. Twenty-seven
feeds across seven regions.

**2026-09-20 — `scout_rank` summarises in English and keeps the source's own words.**
Everything downstream reads `summary`: the planner, the writer, the critique.
So it is always English, whatever the item was published in. For a non-English
item the original title and the feed's own description are stored beside it and
shown on the card, because the English summary is ours, not the source's, and a
reader who does speak the language has to be able to check us.

**2026-09-20 — Feed health is recorded on the feed row, not hoped about.**
None of the feed URLs could be reached from the sandbox this was built in: its
egress proxy refuses every host not on its allowlist. Rather than claim they
work, `scout_fetch` records `last_ok_at`, `last_error`, `last_checked_at` and
`consecutive_failures` on every feed, and Settings shows the failures at the
top of the Feeds panel with the actual error. `pnpm feeds:check` tests all of
them from a machine with a normal internet connection and prints a table.

**2026-09-20 — A feed that answers 200 with nothing parseable has failed.**
A redirect to a landing page, a cookie wall, or a feed that quietly moved are
the most common ways a feed dies, and all three return 200. Treating them as a
quiet day would mean a feed stops working and nobody ever hears about it.

**2026-09-20 — A feed switches itself off after five failures in a row.**
A URL that has been dead for a week will still be dead tomorrow. Switching it
off stops the pointless request and puts it in front of a human in Settings,
which is where someone decides what to replace it with. Coming back clears the
count.

**2026-09-20 — A new prompt version is activated by switching the old one off first.**
`prompts_one_active_idx` allows exactly one active version per prompt name, so
activating a new version while the old one is still active either violates the
index or silently does nothing. The seed now does both updates on one
connection in one transaction, old off then new on, so a crash in between
cannot leave a prompt with no active version at all.
