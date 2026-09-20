# SFW Content Studio

An asset library and content machine for the Soil Food Web Foundation. It takes
raw workshop footage, photos and documents, tags and transcribes them, cuts the
good moments out of long videos, drafts posts against the brand rules, critiques
its own drafts, asks a human when it does not know something, and learns from
every edit it gets.

## Read first

1. `CLAUDE.md` — brand, voice, copy rules, programs, people. Every AI prompt
   quotes it.
2. `docs/content-studio-prd-v2.md` — what the product does.
3. `docs/content-studio-backend-spec.md` — the technical source of truth: schema,
   jobs, triggers, cron, AI contracts, API routes, security. When the PRD and the
   spec disagree, the spec wins.

Choices made where both were silent are in `docs/DECISIONS.md`. What works right
now, and how to check it, is in `docs/PROGRESS.md`. Things that need a human with
an account login are in `docs/TODO-LINNEA.md`.

## Shape of the thing

```
apps/web          Next.js 14 on Vercel. The UI and every API route.
workers/light     Claude calls, DB work, Canva, scout, planner. Concurrency 4.
workers/media     FFmpeg and Whisper. Proxies, transcripts, clip cuts.
workers/render    Remotion. Reel renders.
workers/cron      Inserts scheduled jobs. Inserts only, never does work.
packages/*        Shared libraries. See packages/README.md.
supabase/         Migrations and seed data.
scripts/          Bulk upload and local eval runners.
tests/fixtures/   Sample photos, a 3-minute video, a sample PDF.
```

Nothing calls a worker directly. Every automation is a row in the `jobs` table,
workers claim jobs, and every job is idempotent.

## Getting started

```bash
cp .env.example .env.local     # fill in the keys, see docs/TODO-LINNEA.md
pnpm install
pnpm build
pnpm dev
```

`pnpm lint`, `pnpm typecheck` and `pnpm test` run across every workspace.

## Rules for changing this repo

- TypeScript everywhere. Small, readable code. No clever abstractions.
- Keys come from the environment. `.env.local` is never committed.
- Every AI call: JSON out, validated with zod, logged to `ai_calls`, prompt
  loaded from the `prompts` table by name and version.
- Every job: idempotent, retried with backoff, dead jobs visible in the app.
