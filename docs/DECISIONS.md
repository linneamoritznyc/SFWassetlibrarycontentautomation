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
