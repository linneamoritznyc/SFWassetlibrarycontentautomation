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
