# workers

Long-running Node processes on Railway. Each one claims job types from the `jobs`
table with `claim_job(types[])` and does the work. Nothing ever calls a worker
directly over HTTP.

- `light` — Claude calls, database work, Canva, scout, the planner. Concurrency 4.
- `media` — FFmpeg and Python (Whisper, face crop). Proxies, transcripts, clip
  cuts, reframes. Concurrency 1, 4 GB RAM.
- `render` — Remotion and Chromium. Reel renders. Concurrency 1.
- `cron` — Railway cron. Inserts scheduled job rows and nothing else.

Which types a process claims is set by `WORKER_TYPES`, so one image can run as
several different workers.
