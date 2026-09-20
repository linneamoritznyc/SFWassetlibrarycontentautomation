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

Phase 8. Not written yet.

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
