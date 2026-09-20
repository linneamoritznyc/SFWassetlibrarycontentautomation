# Paste intake

The main way material gets into Content Studio by hand: paste a screenshot, a
link, or a block of text, and the machine spins up a story and a draft from it.

Added 20 Sep 2026 at Linnea's request. It replaces the idea of connecting to
Google Drive, Google Chat or Monday.com. Nothing here reads another system. The
screenshot is the interface.

## What triggers it

Anything dropped on `/inbox` or pasted with Cmd-V anywhere in the app:

| Pasted | What happens |
| --- | --- |
| A screenshot (a Google Chat message, an email, an Instagram post, an article) | Read it with Claude vision, pull out the sender, the message, and any URLs |
| A bare URL | Skip straight to fetching the page |
| Plain text | Treat it as a note from a named person and extract facts directly |

The worked example: a Google Chat screenshot of Evan posting a Walton Family
Foundation story with "More good news to share!".

## The chain

```
paste            → assets(type=reference)            stored in sfw-media
  ↓
paste_intake     → Claude vision reads the image     {sender, message, urls[], ...}
  ↓
web_fetch        → per URL: sources(kind=url) row    content hash stored
  ↓
extract_facts    → facts, each with its source       page/section refs
  ↓
propose_story    → stories(origin=news)              angle + pillar + material
  ↓
write → gap_check → critique                         a draft in the Week view
```

Each step is an ordinary job row, so a pasted screenshot at 1am is a critiqued
draft waiting on Monday morning.

## What `paste_intake` returns

Claude reads the screenshot and returns this, validated with zod:

```json
{
  "kind": "chat",
  "sender": "Evan Buckman",
  "sent_at": "1:43 AM",
  "message_text": "More good news to share!",
  "urls": ["https://www.waltonfamilyfoundation.org/stories/environment/..."],
  "link_preview_title": "Investing in Water and Nature to Build Climate Resilience",
  "image_description": "Aerial photo of a river through dense mixed forest",
  "is_sfw_material": false
}
```

`is_sfw_material` is the important one. A screenshot of a chat window is not a
post visual, and neither is a third-party foundation's photo. Both fail the
brand rule in CLAUDE.md section 5: real SFW images only, no stock, no borrowed
photography. So the reference asset is stored as provenance, never as the visual.

## Where the angle comes from

`propose_story` gets the brand rules as its briefing, not a blank page. It picks:

- **The pillar.** Four to choose from, and the choice drives everything after it.
  Third-party climate and water research is usually PROVE IT.
- **The platform.** CLAUDE.md section 4 is explicit: LinkedIn is where SFW reacts
  to real niche news in soil, ag policy and climate, and restating org facts
  performs badly there. Outside news lands on LinkedIn first, with a real
  question at the end. Instagram gets it only when there is a science explainer
  in it and an SFW image to carry it.
- **The evidence rung.** Someone else's research is theirs, not ours. Section 3
  allows "documented" language only for a named case with data. A foundation's
  press story is cited, never absorbed into an SFW claim.
- **The visual.** Vector search over the library for a cleared, unused SFW asset
  that matches the angle. Found: attach it. Not found: the story stalls and
  raises a shot-list item or a question, because PRD principle 1 says a post
  exists only when its material exists.

## The hard rule this makes visible

A pasted link on its own cannot become a post. It has the fact but not the
picture. So `propose_story` ends one of two ways, and both are useful:

1. A draft with an SFW image attached, ready for the Week view.
2. A story marked `candidate` plus a one-line ask: "Which workshop photo should
   carry this? None in the library matches water and climate resilience." That
   ask goes to the Questions view, and by the routing map in CLAUDE.md section
   10 an item about partners and outside news goes to Kavi.

Never a post built on someone else's photograph.

## Build order

- Capture, storage and the vision read land in **Phase 2**, alongside the rest of
  the inbox.
- `propose_story` and the spin-up into `write` and `critique` land in **Phase 4**,
  once the knowledge base and the writer exist.
- Until Phase 4, a paste produces a reference asset, a source, and facts. That is
  already worth having: the facts are in the knowledge base for anything else
  written that week.
