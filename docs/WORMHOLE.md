# Wormhole

The team's preview of every planned post, at `/wormhole`, behind a shared password.

- **Views:** Instagram feed (swipeable carousels), Instagram grid (newest first), LinkedIn feed.
- **Editing:** "Edit" under any post. Changes save by themselves and show up on everyone else's screen within a few seconds. Every save is kept with who and when ("Show every saved version", then "Restore").
- **Images:** drop Canva exports onto a post's slides. Several pages at once fill the slides in order. Images are shrunk to 1440 px wide in the browser and stored in Postgres (`wormhole_images`).
- **Status:** Draft, Copy approved (Allison), Approved (Stephanie), Scheduled. Filter by status and week.
- **Doc export:** "Copy for the doc" puts the shown posts on the clipboard in Stephanie's planning-doc template, ready to paste into Google Docs. "Download" saves the same as an HTML file.

## Setup

- Tables: `supabase/migrations/0011_wormhole.sql` (RLS on, no policies; only the server reaches them through `DATABASE_URL`).
- Data: `pnpm wormhole:seed` loads `supabase/seed/wormhole-posts.json`. Posts that already exist are left alone.
- Env: `WORMHOLE_PASSWORD` (the shared password) and `WORMHOLE_SECRET` (signs the sign-in cookie; change it to sign everyone out).
- Voice rules for the agents in phase 2: `supabase/seed/wormhole-voice.md`.
