# Scout: the soil news scraper

Scout reads 31 soil, farming and research sources and lists the fresh stories
that sit closest to the soil food web.

## In Wormhole (the everyday way)

Open the **Soil news** tab on https://wormholelinnea.vercel.app. It reads every
source live when you open it. Each source is cached for three hours, so it
costs nothing to open again.

- Stories are scored on the words they use: mycorrhizal fungi, nematodes,
  protozoa, compost and soil carbon count for much more than "farm" or "crop".
  Anything below the cut-off (`MIN_SCORE` in `apps/web/lib/scout.ts`) is left
  out. "Mentions" on each card shows why a story made the list.
- **Add to the plan** makes a draft post with no date. The story's link is in
  Sources, the caption has the caption-shape prompts, and the visual note says
  where Scout found it. Give it a date in Edit.
- **Not for us** hides a story on that device only.
- The line under the filters says how many sources answered; tap it to see each
  one and why any are failing.

## The source list

`packages/shared/src/feeds.ts`. Where an organisation has no working RSS, the
URL is a Google News search limited to its site (for example `site:cgiar.org`).
`fallback` is tried when the main URL fails. Checked 23 October 2026: all 31
answer from the server.

## From a terminal

```bash
python3 tools/scout/fetch_feeds.py --days 10
```

This writes `tools/scout/out/candidates.json` (every fresh story, newest first,
not scored) and `feed-health.json`. A Claude Code session can read these to
pick stories and build slides with `news_posts.py`.

## Rules for any post Scout starts

- Read the study, not just the press release. The headline is a lead, not a
  source.
- Every number needs its source in the notes (CLAUDE.md, section 3).
- Match the claim to the evidence: a pot trial is "early results suggest",
  not "proven".
