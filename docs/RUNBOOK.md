# Runbook

Operating the system. Filled in as phases land.

## Local development

```bash
cp .env.example .env.local     # then fill in the keys
pnpm install
pnpm build
pnpm dev                       # web on http://localhost:3000, workers polling
```

## Database

```bash
pnpm db:setup      # apply migrations, then seed. Safe to re-run.
pnpm db:migrate    # migrations only
pnpm db:seed       # seed only
```

Migrations are recorded in `schema_migrations` and each runs once, inside a
transaction. The seed upserts by natural key and never deletes, so a tag added
by hand and an email filled in by hand both survive a re-seed.

A prompt is activated by the seed only the first time its name is seen. A new
version of an existing prompt arrives inactive and has to pass the test set
before it goes live.

## Running the tests with a database

The schema and queue tests build their own throwaway databases. They need a
Postgres with `vector` and `pgcrypto`, and a user that can create databases.

```bash
# Ubuntu
apt-get install -y postgresql-16 postgresql-16-pgvector

TEST_DATABASE_URL=postgres://postgres@127.0.0.1:5432/postgres pnpm test
```

Without `TEST_DATABASE_URL` those tests skip and the rest still run.

## Running the workers

Each worker claims the job types named in `WORKER_TYPES`, so one image can run
as several workers.

```bash
# Claude calls, tagging, facts, the clip finder.
WORKER_TYPES=ingest,embed,extract_doc,paste_intake,web_fetch,find_clips \
  WORKER_CONCURRENCY=4 node workers/light/dist/index.js

# FFmpeg and Whisper. One at a time: two ffmpeg runs on one box finish later
# than two in a row.
WORKER_TYPES=proxy,transcribe,cut_clip \
  WORKER_CONCURRENCY=1 node workers/media/dist/index.js
```

Both need `DATABASE_URL`, the four R2 variables, and the API keys. They write a
heartbeat every 60 seconds, which the Errors view shows as a red dot after five
minutes of silence.

FFmpeg has to be on the PATH for `worker-media`, or set `FFMPEG_PATH` and
`FFPROBE_PATH`.

## Deploy

Five services. The web app on Vercel, three workers and the cron on Railway.
All of them read the same `DATABASE_URL` and the same R2 and API keys.

### Vercel, for apps/web

1. https://vercel.com/new, import the repository.
2. **Root Directory**: `apps/web`. Vercel reads `apps/web/vercel.json`, which
   builds from the monorepo root so the workspace packages come along.
3. Environment variables, in **Settings, Environment Variables**, for Production
   and Preview both:
   `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `APP_ALLOWLIST`,
   `DATABASE_URL`, `NEXT_PUBLIC_APP_URL`, the four `R2_*`, `ANTHROPIC_API_KEY`,
   `OPENAI_API_KEY`, `TOKEN_ENC_KEY`, `INBOUND_EMAIL_SECRET`, the three
   `CANVA_*`.
4. Deploy. Then set `NEXT_PUBLIC_APP_URL` and `CANVA_REDIRECT_URI` to the real
   domain and redeploy, because magic links and the Canva callback both come
   back to whatever those say.
5. Add the Vercel domain to both R2 buckets' CORS policy (TODO-LINNEA item 2).

### Railway, for the workers

One service per worker, all from the same repository.

| Service | Dockerfile | `WORKER_TYPES` |
| --- | --- | --- |
| worker-light | `workers/light/Dockerfile` | leave unset: it claims everything it can do |
| worker-media | `workers/media/Dockerfile` | `proxy,transcribe,cut_clip,build_post,edit_clip` |
| worker-render | `workers/render/Dockerfile` | `render_reel` |
| cron | `workers/cron/Dockerfile` | not applicable |

1. https://railway.app, New Project, Deploy from GitHub repo.
2. For each service: **Settings, Build**, set the Dockerfile path from the
   table. Each folder also has a `railway.json` with the start command, the
   health check and the restart policy.
3. **Variables**, shared across all four: `DATABASE_URL`, the four `R2_*`,
   `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `NOTIFY_EMAIL`, `RESEND_API_KEY`,
   `NEXT_PUBLIC_APP_URL`. worker-light also wants `TOKEN_ENC_KEY` and the
   `CANVA_*` ones; cron wants `CRON_TIMEZONE=Europe/Berlin`.
4. Sizes: worker-media needs **4 GB** (spec section 2) and worker-render at
   least 4 GB, because Chromium and ffmpeg are both memory hungry. worker-light
   and cron are happy at 512 MB.
5. Set `PORT` on the three workers so Railway's health check has something to
   poll. The endpoint answers 200 only when the database is reachable, so a
   worker that is up but cut off is reported as unhealthy rather than fine.

### Is it working

- `/errors` in the app shows a heartbeat per worker. A red dot means nothing
  has been heard for five minutes.
- `/api/health` on the web app.
- `curl https://<worker>.up.railway.app/` returns the worker's name and the
  job types it claims.

## Rollback

**The web app.** Vercel keeps every deployment. Open the one that worked,
**Promote to Production**. It is instant and changes no data.

**A worker.** Railway keeps the previous image. Open the service, **Deployments**,
find the last good one, **Redeploy**. Jobs in flight fail and are retried, which
is what the backoff is for.

**A prompt.** Nothing needs deploying. `eval_nightly` rolls back automatically
on a regression of more than ten points. By hand:

```bash
node scripts/eval/dist/index.js --prompt write            # see where it stands
node scripts/eval/dist/index.js --prompt write --activate 2
```

**A migration.** There is no down migration, on purpose: an automatic reverse
of a destructive change is a way to lose data twice. To undo one, write a new
migration that undoes it and apply that, so the history stays forwards-only and
readable. Supabase also has point-in-time recovery on the Pro plan, which is
the right tool if data is actually lost.

**Everything at once.** The database is the system. The services are
disposable: redeploy them from any commit and they pick up where they left off,
because all the state is in Postgres and R2.

## Adding a workshop

A workshop is a tag, a smart folder and a batch of material.

1. Add it to `WORKSHOPS` in `packages/shared/src/folders.ts` and to the
   `workshop` facet in `packages/shared/src/tags.ts`.
2. `pnpm db:seed`. The tag and the folder appear; nothing else changes.
3. Upload the material through Library, Upload, with the workshop name in the
   batch form. It is copied onto every asset in the batch.
4. For the footage drive, use `scripts/bulk-upload` instead: rclone it into
   `sfw-raw`, then run the register script with `--workshop "<name>"`.
5. Anything over three minutes gets transcribed and clipped on its own.

If the workshop has a course page, add it to `SOURCE_PAGES` in
`packages/shared/src/sources.ts` too. It is then re-read weekly, and its dates
and prices become facts the writer can cite.

## Rollback

Phase 8. Not written yet.

## Adding a workshop

Phase 8. Not written yet.

## Running the contractor test on a real workshop video

The point of the clipping machine is to replace roughly $1,000 a month of
outside clipping. The test is a side-by-side on a video the contractor has
already done, so the comparison is on the same material.

**What you need:** one workshop video the contractor clipped, and their clips.

1. Upload the source video through Library, Upload. Give the batch the workshop
   name and the creator.
2. It gets a 720p proxy and a transcript automatically. A video over three
   minutes then queues `find_clips` on its own. Watch `/errors` for progress;
   an hour of video is a few minutes of transcription.
3. Open `/clips` and pick the video. You should see 12 to 15 candidates, each
   with the hook the speaker actually said, why it was chosen, its pillar and a
   score out of 100.
4. Work through them. Keep the ones you would post, Trim the ones whose edges
   are wrong, Cut the rest. Keeping one cuts all four ratios.
5. Read the cost line at the top of the page: proposed, kept, and dollars per
   kept clip.

**What passing looks like,** from PRD 5.4: more usable clips than the
contractor produced from the same video, quality as good or better, at a lower
cost per clip. The PRD's target is 8 to 10 kept clips a week at under $1 each,
against 2 to 3 at about $100.

**Write down**, for the comparison:

- how many candidates the machine proposed, and how many you kept
- how many the contractor delivered from the same video
- dollars per kept clip from the header, against about $100
- how long you spent deciding, which is the number that decides whether this
  is worth running every week

If the candidates are weak, the fix is the `find_clips` prompt rather than the
code: the constraints (20 to 60 seconds, sentence boundaries, the expertise
bar) are all in the prompt body. Bump its version, seed it, and run the eval
before activating it.
