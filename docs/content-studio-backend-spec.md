# Content Studio: Backend and Automations Spec

Technical companion to `content-studio-prd-v2.md`. Updated 19 Sep 2026.

---

## 1. Architecture

```
Browser (Next.js on Vercel)
   │  REST (API routes, server-side keys)
   ▼
Supabase Postgres ──── jobs table (queue) ──── Railway workers
   │  pgvector, RPC, triggers                    │ ingest, transcribe, clip, render,
   │                                             │ brief, write, critique, plan, scout,
   ▼                                             │ canva, results, learn
Cloudflare R2  ◄──────── read/write files ───────┘
  sfw-raw   (originals, video, Infrequent Access)
  sfw-media (thumbs, proxies, clips, renders, docs, Standard)

External APIs: Claude, Whisper, Canva Connect, RSS/web sources, Instagram/Later (results)
```

**Rules**
- The browser never holds service keys. All writes go through API routes.
- Every automation is a job row. Workers pull jobs; nothing calls a worker directly.
- Every job is idempotent: re-running it produces the same end state.
- Every AI output is stored with the prompt version, model, input IDs and cost.

---

## 2. Services

| Service | Host | Runtime | Role |
|---|---|---|---|
| `web` | Vercel | Next.js 14 | UI + API routes |
| `worker-light` | Railway | Node 20 | Claude calls, DB work, Canva, scout, planner. Concurrency 4 |
| `worker-media` | Railway | Node 20 + FFmpeg + Python (Whisper, face/speaker crop) | Proxies, transcripts, clip cuts, reframes. Concurrency 1, 4 GB RAM |
| `worker-render` | Railway | Node 20 + Remotion + Chromium | Reel renders. Concurrency 1 |
| `cron` | Railway cron | Node | Inserts scheduled jobs only |

Each worker declares which job types it claims via `claim_job(types[])`.

---

## 3. Storage layout (R2)

```
sfw-raw/
  originals/{asset_id}/{filename}
sfw-media/
  thumbs/{asset_id}.jpg            800px, JPEG q82
  proxies/{asset_id}.mp4           720p H.264, for browser playback
  audio/{asset_id}.m4a             for transcription
  clips/{clip_id}/{ratio}.mp4      9x16, 4x5, 1x1, 16x9
  clips/{clip_id}/captions.srt
  renders/{render_id}.mp4
  designs/{post_id}/{n}.png        built images and carousels
  docs/{doc_id}/{filename}         PDFs, reports
```

Presigned PUT for uploads (1 h), presigned GET for viewing (1 h). Buckets private. CORS: GET, PUT from the app domain.

---

## 4. Data model (Supabase)

### 4.1 Material
```sql
batches(id, drive_link, original_path, creator, workshop, uploaded_at)

assets(
  id uuid pk, batch_id fk, parent_id fk null,          -- clips point to their source video
  type text  -- photo|video|graphic|doc|clip|render|reference
  filename, bucket, r2_key, thumb_key, proxy_key, audio_key,
  width, height, duration_s, clip_start_s, clip_end_s,
  status  -- inbox|tagged|cleared|used|archived
  quality 1-5, hero_candidate bool,
  description text, notes text,
  drive_link, original_path, creator, credit_line,
  taken_at, camera, gps_lat, gps_lng,
  release_status  -- unknown|signed|missing
  embedding vector(1024),
  created_at, updated_at)

tags(id, name, facet)                          -- facet: workshop|subject|organism|pillar|people|place|platform_fit|format
asset_tags(asset_id, tag_id, source ai|human, confirmed bool, confidence real)

transcripts(asset_id pk, language, text, words jsonb)   -- words: [{w, start, end, speaker}]
people(id, name, role, org, email, release_status, notes)
asset_people(asset_id, person_id, source ai|human, confirmed)

smart_folders(id, name, section, filters jsonb, position)
```

### 4.2 Knowledge
```sql
sources(id, kind url|doc|transcript|human|post, ref, title, fetched_at, content_hash)
facts(
  id, subject, predicate, object,               -- "India workshop" | "runs" | "Oct 19 to 30 2026"
  text,                                         -- one plain sentence
  source_id fk, confidence real, status active|conflict|retired,
  confirmed_by text null, valid_from, valid_to,
  embedding vector(1024), created_at)
rules(id, scope all|instagram|linkedin|reel|caption|critic, text, origin edit|rejection|result|manual,
      evidence jsonb, active bool, applied_count int, created_at)
questions(id, text, asked_to person_id, context jsonb, status open|answered|dropped,
          answer text, answered_at)
```

### 4.3 Scout
```sql
feeds(id, name, url, kind rss|page|api, active)
news_items(id, feed_id, url unique, title, published_at, summary, relevance real,
           linked_facts int[], linked_assets uuid[], status new|drafted|dismissed, embedding)
```

### 4.4 Production
```sql
stories(id, origin asset|news|fact|manual, origin_ref, angle text, pillar,
        material_asset_ids uuid[], material_fact_ids int[], score real,
        status candidate|planned|used|dropped, created_at)

posts(
  id, story_id fk, slot_date date, slot_time time, platform, format feed|carousel|reel|story|linkedin|short,
  asset_ids uuid[], render_id fk null,
  hook, caption, hashtags text[], cta_text, cta_url, collaborators text[],
  status proposed|revising|in_review|approved|rejected|exported|published,
  reject_reason text null, experiment bool,
  critic_score real, critic_notes jsonb,
  published_url, published_at, created_at)

post_versions(id, post_id, version, author ai|human, caption, hook, hashtags, asset_ids,
              diff jsonb, prompt_version, created_at)

renders(id, template, input jsonb, bucket, r2_key, status, duration_s, cost_usd, created_at)
canva_links(id, post_id, canva_design_id, edit_url, exported_asset_id, status)
```

### 4.5 Results and learning
```sql
metrics(post_id, captured_at, reach, likes, comments, saves, shares, link_clicks, watch_time_s)
test_cases(id, name, kind good|bad, input jsonb, expected jsonb, notes)
eval_runs(id, prompt_version, passed int, failed int, details jsonb, created_at)
prompts(id, name, version, body text, active bool, created_at)
ai_calls(id, job_id, prompt_name, prompt_version, model, input_tokens, output_tokens,
         cost_usd, latency_ms, created_at)
```

### 4.6 Queue
```sql
jobs(id bigserial, type, payload jsonb, priority int default 5,
     status queued|running|done|failed|dead, attempts, max_attempts default 3,
     run_after timestamptz default now(), error, dedupe_key text unique null,
     created_at, updated_at)

claim_job(types text[]) → setof jobs     -- FOR UPDATE SKIP LOCKED, priority then created_at, run_after <= now()
```
Retry with backoff: `run_after = now() + 2^attempts minutes`. After `max_attempts`: status `dead`, shown in the app's Errors view.

---

## 5. Events and triggers

| Event | Source | Creates job(s) |
|---|---|---|
| Asset rows inserted | API `POST /assets` | `ingest` per asset |
| `ingest` done on video | worker | `proxy`, `transcribe` |
| `transcribe` done, duration > 180 s | worker | `find_clips` |
| Asset status → `tagged` | DB trigger | `embed` |
| Doc uploaded | API | `extract_doc` |
| Clip approved (Keep) | API | `cut_clip` for each ratio needed |
| Post approved | API | `build_post` (images/carousel) or `render_reel` |
| Post edited by human | API | `log_edit` |
| Post rejected with reason | API | `log_rejection` |
| Question answered | API (email reply webhook or UI) | `save_fact` |
| Post marked published | API | `link_asset_usage` |

### Cron (Railway, CET)
| Schedule | Job |
|---|---|
| Daily 06:00 | `scout_fetch` |
| Daily 06:30 | `scout_rank` |
| Mon 05:00 | `results_pull` |
| Mon 05:30 | `learn_weekly` |
| Mon 06:00 | `plan_week` |
| Mon 06:45 | `write_batch` for all planned posts |
| Mon 07:30 | `review_ready_notify` (email to Linnea) |
| Sun 04:00 | `eval_nightly` (run test set on active prompts) |
| Sun 04:30 | `web_refresh` (re-fetch source pages, detect changes) |
| Hourly | `questions_nudge` (one reminder after 48 h) |

---

## 6. Job catalogue

Each job: input → steps → output → failure handling.

### Material
**`ingest`** (light) · `{asset_id}`
1. Read EXIF if not set by browser. 2. Send thumbnail + tag vocabulary + batch context to Claude. 3. Save `description`, suggested tags (`source=ai, confirmed=false, confidence`). 4. If faces detected by Claude, suggest `people` matches from people table.
Output: tagged-in-inbox asset. Fail: retry; on dead, asset stays in inbox with "tagging failed" badge.

**`proxy`** (media) · `{asset_id}` · FFmpeg → 720p H.264 proxy + AAC audio to `sfw-media`.

**`transcribe`** (media) · `{asset_id}` · Whisper on audio, word timestamps, speaker diarization. Writes `transcripts`. Chunks audio > 25 MB.

**`embed`** (light) · `{asset_id}` · Text embedding of description + tags + transcript summary → `assets.embedding`.

**`extract_doc`** (light) · `{asset_id}` · PDF text → `sources` row → Claude extracts atomic facts with page refs → `facts` (status active if unambiguous, else conflict).

### Clips
**`find_clips`** (light) · `{asset_id}`
1. Load transcript + rules scope `reel` + top 5 past clips by saves.
2. Claude returns 12 to 15 candidates: `{start, end, hook, why, pillar, speaker, score 0-100}`. Constraints: 20 to 60 s, starts and ends on sentence boundaries, clears expertise bar.
3. Snap boundaries to word timestamps, pad 0.3 s.
4. Insert each as `assets(type=clip, parent_id, clip_start_s, clip_end_s, status=inbox)` + preview cut job.
Output: 12 to 15 clips in the Clips view.

**`cut_clip`** (media) · `{clip_id, ratio}`
1. FFmpeg seek-cut from original in `sfw-raw`. 2. Reframe: v1 center crop; v2 speaker-tracking crop (face detection every 0.5 s, smoothed). 3. Burn captions from word timestamps in SFW style (Montserrat 600, 2 lines max, highlight current word). 4. Loudness normalize to −14 LUFS.
Output: `clips/{id}/{ratio}.mp4` + `.srt`.

### Knowledge
**`brief`** (light, internal step, also callable) · `{story_id}` → briefing packet JSON:
```json
{ "story": {...}, "assets": [{id, description, credit_line, thumb_url}],
  "facts": [{id, text, source}], "rules": [...active rules for scope],
  "examples": [3 approved posts of same format, highest saves],
  "brand": "CLAUDE.md sections 2-5", "calendar_context": {...} }
```
Facts selected by: direct links from story + vector search top 15 + all facts about people in the assets.

**`gap_check`** (light) · `{post_id}`
Writer's first call returns `{assumptions:[], unknowns:[]}`. Each unknown → vector search facts. Found with confidence ≥ 0.8 → attach. Not found → `questions` row routed to person by topic map (programs → Stephanie, mentors/graduates → Carla, India/partners → Kavi, workshops → Loida). Post status `revising` until answered or 72 h pass, then goes to review flagged.

**`save_fact`** (light) · `{question_id}` → answer parsed into facts with `source.kind=human`.

**`web_refresh`** (light) · re-fetch every `sources.kind=url`. Content hash changed → re-extract facts → old facts with changed values set `retired`, new facts `active`, conflicts flagged.

### Scout
**`scout_fetch`** (light) · pull all active feeds → new `news_items` (dedupe by URL).
**`scout_rank`** (light) · per item: summary, relevance 0-1 vs SFW topics, link to facts and assets by vector search. Relevance ≥ 0.7 → `stories(origin=news)`.

### Planning and writing
**`plan_week`** (light)
Inputs: slots for next 7 days (cadence config: Mon/Wed/Fri feed, 3 to 4 Stories, 2 Shorts, 1 to 2 LinkedIn), events calendar (webinars, deadlines), story candidates, cleared unused assets and clips, `learn_weekly` weights.
Scoring: `score = relevance × freshness × material_strength × format_weight × pillar_balance`. 20% of slots chosen from exploration pool (formats or topics with < 3 data points).
Output: `posts(status=proposed)` linked to stories. Hard rule: a post needs ≥ 1 asset or ≥ 1 document; slots without material become `questions` or shot-list items.

**`write`** (light) · `{post_id}`
1. `brief` → 2. `gap_check` → 3. Claude writes with images attached (thumbnails of chosen assets) → hook, caption, hashtags, CTA, platform variant → `post_versions(author=ai)`.

**`critique`** (light) · `{post_id}`
Separate Claude call with a different prompt. Checklist from active `rules(scope=critic)` + claims ladder + image-text match (images attached). Returns `{score, issues[], must_fix[]}`. `must_fix` non-empty → back to `write` with issues (max 2 loops) → `in_review`.

**`write_batch`** · fans out `write` for all `proposed` posts.

### Production
**`build_post`** (media) · images resized/cropped to 4:5 or carousel slides with SFW frame template (Sharp) → `designs/`. If Canva enabled and template set → `canva_push`.
**`render_reel`** (render) · Remotion template + clip IDs + text → `renders/`.
**`canva_push`** (light) · upload assets to Canva folder, create design (Instagram post preset), store `edit_url`. When autofill approved: autofill brand template instead.
**`canva_pull`** (light) · export design PNG/MP4 → new asset `type=render`.

### Distribution
**`export_bundle`** (light) · approved posts → ZIP: media, `caption.txt`, `meta.json` (time, platform, hashtags, collaborators, UTM link). Later API path swaps in when access exists.
**`link_asset_usage`** · asset status → `used`, usage rows written.

### Results and learning
**`results_pull`** (light) · Instagram Graph API insights (Business account) or CSV import from Later → `metrics`.

**`log_edit`** (light) · diff of AI version vs human version → stored in `post_versions.diff`.

**`log_rejection`** (light) · reason code + post context stored.

**`learn_weekly`** (light)
1. Cluster last 4 weeks of edit diffs and rejection reasons. Claude proposes rules: `{text, scope, evidence: [post_ids]}`. Rules with ≥ 3 supporting edits → candidate.
2. Candidate rules run through `eval` against `test_cases`. Pass → `active`. Fail → discarded, logged.
3. Results: compute saves+shares per impression by format, pillar, asset type, speaker, hook style. Update `format_weight` and `pillar_balance` for the planner (moving average, capped change ±20% per week).
4. Promote top approved posts (edited ≤ 10%, top quartile saves) to `examples`.
5. Autonomy: post types with ≥ 90% approve-without-edit over 4 weeks flagged "light review".
6. Write a short "What it learned" note for the app.

**`eval_nightly`** (light) · run active prompts on `test_cases` (Pratik, Sandra = good; flagged posts = bad). Score with critic + string checks (banned phrases, negation patterns, em dashes, acronyms). Regression vs last run > 10% → alert + auto-rollback to previous `prompts.version`.

---

## 7. AI call contracts

All Claude calls: JSON-only responses, schema-validated (zod). Invalid → one repair retry → fail job.

| Call | Model | Input | Output schema |
|---|---|---|---|
| tag | sonnet | thumb, vocab, batch context | `{description, tags[], people_guess[]}` |
| find_clips | sonnet | transcript, rules, examples | `{clips:[{start,end,hook,why,pillar,speaker,score}]}` |
| extract_facts | sonnet | doc text chunk | `{facts:[{subject,predicate,object,text,page}]}` |
| gap_check | sonnet | briefing | `{assumptions[], unknowns[]}` |
| write | sonnet (opus for articles) | briefing + images | `{hook, caption, hashtags[], cta_text, cta_url, alt_text}` |
| critique | sonnet | draft + images + rules | `{score, issues[], must_fix[]}` |
| plan | sonnet | slots, candidates, weights | `{posts:[{slot, story_id, asset_ids, format, angle}]}` |
| learn | sonnet | diffs, reasons | `{rules:[{text, scope, evidence}]}` |
| scout_rank | haiku | news item | `{summary, relevance, topics[]}` |

Prompts live in `prompts` table, versioned. Workers load the active version at job start.

---

## 8. API routes (web)

```
POST /api/upload-url              presigned PUT for original + thumb
POST /api/assets                  create batch + assets, enqueue ingest
GET  /api/assets?filters          library query (facets, text, vector)
GET  /api/assets/:id              detail + presigned GET
PATCH /api/assets/:id             fields, tags, status, people
POST /api/assets/:id/find-clips   enqueue find_clips
POST /api/clips/:id/keep|cut|trim
GET  /api/week                    posts for current review
POST /api/posts/:id/approve|reject|edit
POST /api/posts/export            enqueue export_bundle
GET  /api/questions  POST /api/questions/:id/answer
GET  /api/scout
GET  /api/learned
POST /api/canva/auth  GET /api/canva/callback
POST /api/webhooks/email          inbound answers to questions
GET  /api/errors                  dead jobs
```

---

## 9. Security

- App behind Supabase Auth (magic link, allowlist: linnea@soilfoodweb.com). Basic-auth fallback in v1.
- Service role key and R2 keys only in Vercel and Railway env vars.
- R2 buckets private; all access via presigned URLs.
- Claude receives thumbnails, transcripts and text. Originals stay in R2.
- Canva OAuth tokens encrypted at rest (pgcrypto, key in env).
- Row Level Security on all tables; API routes use service role server-side only.
- No connection to SFW Google Drive.

---

## 10. Observability

- `ai_calls` for cost and latency per job and per prompt version.
- Errors view: dead jobs with retry button.
- Weekly cost line in the Monday email: storage, Claude, Whisper, Railway.
- Health: each worker writes a heartbeat row every 60 s; app shows red dot if > 5 min old.

---

## 11. Cost estimate (monthly, steady state)

| Item | Estimate |
|---|---|
| R2 storage 10 TB (mostly IA) | ~$75 |
| Supabase Pro | $25 |
| Railway (3 workers + cron) | $15 to $40 |
| Claude API (tagging 2k assets once, ~60 posts, ~50 clips, scout, learning) | $20 to $40 |
| Whisper (~20 h of video/month) | ~$7 |
| Vercel | $0 |
| **Total** | **~$140 to $190** |

Per clip: ~$0.10 to $0.30.

---

## 12. Environment variables

```
# shared
SUPABASE_URL  SUPABASE_SERVICE_ROLE_KEY
R2_ACCOUNT_ID  R2_ACCESS_KEY_ID  R2_SECRET_ACCESS_KEY  R2_BUCKET_MEDIA  R2_BUCKET_RAW
ANTHROPIC_API_KEY  OPENAI_API_KEY (Whisper)
# web
NEXT_PUBLIC_SUPABASE_URL  NEXT_PUBLIC_SUPABASE_ANON_KEY  APP_ALLOWLIST
CANVA_CLIENT_ID  CANVA_CLIENT_SECRET  CANVA_REDIRECT_URI  TOKEN_ENC_KEY
INBOUND_EMAIL_SECRET
# workers
WORKER_TYPES=ingest,embed,...   WORKER_CONCURRENCY
IG_BUSINESS_ACCOUNT_ID  IG_ACCESS_TOKEN (results)
NOTIFY_EMAIL=linnea@soilfoodweb.com
```

---

## 13. Build sequence

1. Queue + `ingest` + `embed` + library UI (done in `sfw-library` v1; migrate to this schema).
2. `proxy`, `transcribe`, `find_clips`, `cut_clip` (center crop) + Clips view. Run the contractor test.
3. `facts`, `extract_doc`, `brief`, `gap_check`, `write`, `critique` + review screen + questions.
4. `plan_week`, cron, `export_bundle`, `results_pull`.
5. `log_edit`, `log_rejection`, `learn_weekly`, `test_cases`, `eval_nightly`.
6. `render_reel` (2 templates), `canva_push/pull`.
7. `scout_fetch/rank`, speaker-tracking reframe, light editor.
