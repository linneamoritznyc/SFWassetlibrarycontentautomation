# packages

Shared libraries. Every one is plain TypeScript compiled to `dist/`.

- `db` — Supabase client, generated types, query helpers.
- `queue` — enqueue, claim, complete, fail, backoff, heartbeat.
- `storage` — R2 client, presigned URLs, key builders for the layout in backend
  spec section 3.
- `ai` — Claude and Whisper clients, zod schemas for every AI contract, the
  prompt loader, cost logging into `ai_calls`.
- `prompts` — the seed text of every prompt, one file per prompt, versioned.
  These are loaded into the `prompts` table by the seed script; workers read the
  table, not these files.
- `brand` — tokens from `CLAUDE.md`: colours, fonts, caption style.
- `remotion` — Reel templates.
- `shared` — types, constants, the tag vocabulary, cadence config.
