# Content Studio PRD v2

Owner: Linnea Moritz · Updated 19 Sep 2026 (rev 2) · Supersedes v1 (16 Sep)

## 1. What it is

Content Studio is SFW's content machine. It holds every photo, video, clip and document the Foundation owns, finds the stories inside that material, and produces finished posts, Reels and articles for human approval. It gets better every week from Linnea's edits and from post results.

It replaces three things: Drive-folder searching, spreadsheet content planning, and the outside video clipping contractor.

**Contractor baseline:** ~$1,000/month for 2 to 3 clips a week (~10 a month), about $100 per clip. **Content Studio target:** 8 to 10 clips a week at a few cents each in API costs.

## 2. Principles

1. **Material first.** A post exists only when its material exists: a photo, clip, transcript, report or verified fact. Missing material becomes a request to a named person.
2. **The agent looks things up.** Knowledge lives as small sourced facts. Each task gets a short briefing built for that task.
3. **Linnea's time is the scarcest resource.** Target: one 15-minute weekly review. Everything else runs on its own.
4. **Human approval before anything leaves.** The system ends at a ready-to-post bundle.
5. **Every correction teaches the system.** An edit made once gets applied everywhere after.
6. **Provenance on everything.** Every asset and fact knows where it came from.

## 3. Constraints

- SFW's Google Drive stays disconnected (Evan's security rule). Files enter by upload.
- Built privately. Evan wants output, no process involvement.
- Accounts under linnea@soilfoodweb.com.
- ~7.34 TB of footage today, growing to ~10 TB.
- Brand rules from the Messaging House, SOP and brand guide (CLAUDE.md).

## 4. Stack

| Layer | Tool | Cost |
|---|---|---|
| File storage | Cloudflare R2: `sfw-raw` (Infrequent Access), `sfw-media` (Standard) | ~$75/mo at 10 TB |
| Database, search, jobs | Supabase + pgvector | $0 to $25/mo |
| Workers and cron | Railway | ~$5 to $20/mo |
| App | Next.js on Vercel | $0 |
| Judgment and writing | Claude API | usage |
| Transcripts | Whisper | usage |
| Cutting, cropping, captions | FFmpeg (in Railway workers) | $0 |
| Reel rendering | Remotion | check license |
| Design finishing | Canva Connect API via Linnea's own SFW Canva account (Public integration in draft mode) | $0 extra |

## 5. Modules

### 5.1 Library
- One record per asset, stable ID. Faceted properties: type, workshop, subject, organism, people, place, date, status, pillar, platform fit.
- Smart folders are saved filters (Workshops, Asset types, Views, Saved). One asset appears in every folder it matches.
- Inside any folder: videos in their own row on top, photos and graphics below. Adjustable tile size.
- Provenance on every asset: Drive link (clickable), original path, creator, credit line, EXIF date, camera, GPS, release status.
- Batch upload: Drive link, path, creator and workshop entered once per batch.
- Drop-anything inbox: files, links, PDFs, screenshots, voice notes, reference Reels. Uncertain items land in an unsorted tray.
- Auto-description and suggested tags on upload. Linnea confirms in the inbox.
- Search by meaning ("steaming compost at sunrise") and "find similar".
- Statuses: inbox → tagged → cleared to post → used → archived.
- Built-in views: Unused, Untagged, Cleared to post.
- Reference assets: inspiration Reels and screenshots stored with a written breakdown of why they work.

### 5.2 Knowledge base
- Facts table: one sourced fact per row (programs, dates, prices, people, roles, organisms, partners, claims with evidence rung, naming rules).
- People table: name, role, face links in assets, media release status, contact for questions.
- Every task gets a briefing packet: relevant facts, images, source text, rules, three best past examples.
- Before writing, the agent lists its assumptions and unknowns. The system looks each one up. True unknowns become one-line questions emailed to the right person. Answers become permanent facts.
- Facts confirmed by two sources save automatically. Conflicts go to the weekly review.

### 5.3 Niche scout
- Daily scan of a fixed soil source list: research journals and alerts, soil policy (EU, US, India), partner news (Isha / Save Soil, permaculture network), regenerative ag press.
- Each item becomes a news card: summary, source, relevance score, links to related SFW facts and assets.
- Strong cards become draft LinkedIn posts, Instagram explainers, or blog articles. Drafts cite the source.

### 5.4 Clipping machine
- Trigger: a video over 3 minutes reaches "tagged", or Linnea presses "Find clips".
- Whisper transcript with word timestamps.
- Claude picks 5 to 10 moments of 20 to 60 seconds that clear the expertise bar (named organism, mechanism, number, person, place).
- FFmpeg cuts from the original, reframes to 9:16 following the speaker, burns in SFW-styled captions.
- Each clip becomes its own asset linked to its parent video with start and end times.
- Volume target: 8 to 10 approved clips a week. The machine proposes 12 to 15 so the weakest get cut.
- Distribution per week: best 2 to 3 to Instagram feed Reels, 3 to 4 to Stories and YouTube Shorts, 1 to 2 to LinkedIn (horizontal or 4:5), rest held in the library as "cleared" for later weeks.
- Each clip stores: parent video, start/end, transcript excerpt, hook line, pillar, platform fit, speaker, cost to produce.
- Success test ("contractor test"): take one workshop video the contractor already clipped. Run it through the machine. Show their clips next to ours with cost per clip under each. Pass = more usable clips, equal or better quality, lower cost.

### 5.5 Video editor (in-app, light)
- Trim start and end, split, reorder clips on a simple strip.
- Caption editor: fix transcript words, restyle, reposition.
- Reframe: adjust crop focus for 9:16, 4:5, 1:1, 16:9.
- Add music bed, logo, intro and end cards from templates.
- Re-render via worker. Heavy editing stays outside the app.

### 5.6 Reel maker
- Templates built in Remotion with SFW fonts, colours, logo and caption style: Field Notes, Workshop moment, Webinar promo, Science explainer, Quote card, Workshop recap.
- Input: clips and photos from the library plus caption text. Output: rendered MP4 saved as an asset.
- Hooks and on-screen text drafted by the Writer, checked by the Critic.

### 5.7 Caption and post generation
- Writer drafts while seeing the actual images and source material.
- Output in the planning-doc template: date, CTA, link, visual, caption, hashtags (5 to 8), collaborator tags.
- Platform versions: Instagram, Facebook, LinkedIn, YouTube Shorts.
- Critic checks: Messaging House pillar, claims ladder, copy rules, brand vocabulary, partner naming, image-text match, AI cadence. Weak drafts go back to the Writer automatically.
- Photo posts and carousels built in-app at 4:5.
- Canva: connected through Linnea's own SFW Canva account via a Public Connect API integration in draft mode (works for her own team, no paid plan needed). The app can send library assets into a Canva folder, create Instagram-sized designs from them, and pull finished designs back as PNG or MP4 into the library. Brand template autofill switches on once Canva approves the autofill access request.

### 5.8 Planner
- Weekly run, Monday 07:00 CET.
- Reads: open calendar slots, SOP cadence and pillar mix, upcoming events and deadlines, story candidates, unused cleared assets, last week's results.
- Proposes a full week, and can fill a full month on request.
- Keeps ~20% of slots for experiments.

### 5.9 Review
- One weekly screen: the week's posts shown in accurate Instagram, Facebook, LinkedIn and YouTube frames side by side, plus open questions and conflicts.
- One-tap approve, edit inline, or reject with a reason (too vague, wrong image, AI tone, fact wrong, off-brand).
- Approved posts export as a bundle for Later: media file, caption, hashtags, time, collaborator tags.

### 5.10 Results
- Weekly pull of saves, shares, comments, reach per post.
- Written onto each post and each asset used.
- Analyst summary feeds the Planner.

## 6. Agents

| Agent | Job | Reads |
|---|---|---|
| Scout | Finds story candidates in new material and niche news | Library, news cards, facts |
| Editor | Picks the week's stories for the calendar | Candidates, cadence, events, results |
| Writer | Drafts captions, hooks, articles | Briefing packet, images |
| Critic | Checks and returns weak drafts | Rules, facts, images, test set |
| Producer | Builds images, carousels, clips, Reels | Assets, templates |
| Analyst | Reads results, writes weekly learnings | Results, posts |

Each agent reads only what its job needs.

## 7. Self-improvement

1. **Edit learning.** Every edit stores before and after. Weekly, diffs become new rules, and the best approved versions become examples the Writer reads first.
2. **Rejection reasons.** Patterns in reasons update the Critic's checklist.
3. **Results steering.** Performance by format, topic, pillar and asset type reweights the Planner.
4. **Test set.** Best posts (Pratik vermicompost, Sandra) and worst posts are a fixed test. Any prompt or rule change must pass it before going live.
5. **Gap requests.** Stalled stories generate shot lists and asks to named people before events (India first).
6. **Autonomy ladder.** When a post type holds 90%+ approval for four weeks, it moves to lighter review.

## 8. Build phases

| Phase | Scope | Done when |
|---|---|---|
| 1 | Library + provenance + smart folders + auto-tagging worker | 30 Wild Ken Hill photos and 2 videos searchable with Drive links |
| 2 | Clipping machine (video editor comes later) | Passes the contractor test; 8 to 10 clips a week |
| 3 | Knowledge base + Writer + Critic + review screen | Ten posts approved with minimal edits |
| 4 | Planner + results sync + self-improvement loops | A full week proposed and approved in 15 minutes |
| 5 | Reel maker templates + Canva connection | Two templates live; Canva send and pull working |
| 7 | Light video editor | Trim, captions and reframe editable in-app |
| 6 | Niche scout + article drafts | Daily news cards, weekly LinkedIn drafts |

## 9. Success metrics

- Linnea's weekly time on content: ≤ 30 minutes.
- Approval rate of drafts without edits: rising month over month.
- Calendar slots filled: 100%.
- Clips: 8 to 10 approved per week (contractor: 2 to 3).
- Cost per clip: under $1 (contractor: ~$100).
- Saves and shares per post: rising.

## 10. Out of scope for v2

- Automatic publishing.
- Connection to SFW's Google Drive.
- AI-generated images of people, farms or soil.
- A full timeline editor.

## 11. Open questions

- Canva autofill access request: approved or pending.
- SFW's Later plan (API access).
- Remotion license terms for SFW.
- Contractor's turnaround time per clip.
