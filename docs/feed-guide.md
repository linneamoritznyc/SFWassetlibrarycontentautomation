# SFW feed visual guide

The Instagram grid should look like one beautiful, varied feed. Every post is on
brand, and the posts next to each other look different from each other. A run of
posts in one style looks like a template, and Linnea never wants that: never five
posts in a row in the smell-of-rain style, or five in the cutout-flower style.

Read this before building any visual. Colours, fonts and logo rules are in
docs/brand.md; this guide is about variety across the grid.

## The rule

- **Never one template across a batch.** Plan every post's family before building any of them. The photo-and-tag
  look (photo with a coloured box heading) is at most 1 in any 9 grid posts; Linnea hates seeing it everywhere.
- **One photo, one post.** No photo appears on two posts anywhere in the feed. Check every photo with
  `python3 tools/wormhole-visuals/photo_check.py photo.jpg` before using it.
- **Every grid post has a family written in its visual note.** grid_check.py counts a missing family as a break.
- **Neighbours never share a style family.** The post before and the post after must
  use different families from the list below.
- **No family more than twice in any 6 feed posts in a row** (two rows of the grid).
- **At least 5 different families in any 9 feed posts in a row** (three rows).
- **The ground colour changes between neighbours.** Rotate cream, deep green, soil
  brown, tan, light green, blue and real photos edge to edge.
- Feed posts and Reels both count, because both show in the grid. Stories do not, and
  LinkedIn-only posts do not (Wormhole keeps them off the Instagram grid).
- Inside one carousel the slides keep one family, and the layout still changes from
  slide to slide.

## Before building a visual

1. Open Wormhole's Instagram grid and look at the 4 posts on each side of the date.
   Or run `python3 tools/wormhole-visuals/grid_check.py`, which lists the feed in
   order with each post's family.
2. Pick a family none of the nearest neighbours use, and one the last 9 posts use at
   most once.
3. Write it at the start of the post's visual note: `Family: B, big number.`
4. After building, look at the grid again (or rerun grid_check.py) with the new post in it.

## Style families

| | Family | What makes it this family | Example |
|---|---|---|---|
| A | Brand boxes | Flat full-colour boxes with hard edges overlapping a real photo, a green band running across slide edges | d26, the smell of rain (boxes.py, d26_rain.py) |
| B | Big number | One huge number in EB Garamond on cream, one short line under it, one real microscope photo in a circle | Soil in numbers: 440 quintillion nematodes |
| C | Article repost card | Cream card on a Food Web Green ground: the article photo with an outlet tab, a Soil Brown headline beside a green bar, Read More and the source link. Landscape 1200 x 627 for LinkedIn. | Save Soil shoutouts (savesoil.py) |
| D | Full-bleed photo | One strong photo edge to edge, one solid colour strip at the bottom with the heading | Costa Rica, a day at the workshop |
| E | Botanical | Large real plant or flower cutouts on a flat brand colour, with an upright heading | Holiday and seasonal posts |
| F | Specimen | Deep ground colour, one microscope specimen in a circle, its name as a label | Halloween, the vampire amoeba |
| G | Type only | One statement or quote set big on a flat brand colour, no photo | Myth vs mechanism openers, quotes from mentors |
| H | Diagram | A simple drawn diagram on a flat brand colour: layers, a cycle, a cross-section | Soil aggregates explained twice |
| I | Portrait | A person's photo large, with their name, country or role | New consultants, mentor spotlight, graduates |
| J | Numbered steps | A big step number, one short instruction and a square photo, on a flat colour | Do this weekend posts |
| K | Framed photo | One real photo in a clean straight frame on a flat brand colour, heading above or below | Thanksgiving pumpkins (Linnea: 10/10), jan_varied.py |
| L | Photo grid | Three real photos, straight, even gutters, heading under them | Costa Rica one week to go (jan_varied.py) |
| M | Event card | A cream card on a brand colour with a date block and Link in bio | New Year webinar series (jan_varied.py) |
| N | Field notebook | Ruled cream page, margin line, FIELD NOTES label, photo space | Field Notes #3 |

New families are welcome when they follow the brand rules below. Add them to this
table, and to `FAMILIES` in grid_check.py.

## Brand rules that hold in every family

- **Colours:** Soil Brown `#4F3433`, Food Web Green `#156826`, deep green `#22371F`,
  Organic Cream `#F4F1EA`, Education Blue `#3780B8`, Natural Tan `#C89B7B`, Light
  Green `#59A66C`, Purple `#6B4C7A` (Dr. Elaine content only), body text `#333130`.
- **Fonts:** Montserrat, Source Sans 3 and EB Garamond, all upright. Pathway Gothic
  One (from the brand guide) for short condensed labels. Fredoka and other fonts are
  off brand.
- **Real photos only:** our own, the SFW microscope library, or openly licensed with a
  credit.
- **Banned:** gold (except a donate button, per CLAUDE.md), gradients, photo fades,
  glow, vignettes, film grain, tape strips, tilted photos, italic type, small cutouts
  on plain white, hand-drawn sketchy frames, slide counters, date or "Day 1" tags on
  slides, stock photos.
