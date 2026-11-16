# Year-end campaign 2026: builders, assets and design rules

Everything Claude built for the SFW year-end campaign 2026 lives here, so another chat can pick it up.

## Where things are
- Builders and assets: `tools/wormhole-visuals/year-end-2026/`
  - `natlib.py`: python-pptx helpers (`Deck(W, H)` in px, `text()`, `P()`, `measure()`, `rect()`, `png()`, `pic()`). Every paragraph group becomes its own text box.
  - `ig.py`: the 9 social decks (feed 1080x1350, Stories 1080x1920, LinkedIn 1200x1200). Run from this folder: `mkdir -p out/ig && python3 ig.py`.
  - `variants.py`, `fund1.py`, `fund2.py`, `fund2p.py`: the donor documents. Run `python3 variants.py final`, `python3 fund1.py`, `python3 fund2p.py`.
  - `ig/`: 1440 px web copies of the 22 Oct India photos used in the social posts. `ph/`: photos used in the donor documents. Do not reuse `ph/` photos in social posts.
  - `logo.png`, `logo-white.png`, `brandq-green.png` (quote mark), `qr-white.png`, `hay-top.png` (hay strip for Stories and Funding page 1), `el-*.png` elements.
  - `fonts/`: EB Garamond, Source Sans 3, Montserrat. Copy them to `~/.fonts` before rendering with LibreOffice.
- Finished files: `apps/web/public/wormhole/decks/year-end-2026/`
  - `social/`: the 9 PPTX drafts, a preview PDF for each, the contact sheet and the captions draft.
  - `donor-docs/`: the 4 approved donor documents (Case for Support, Donor Overview, Funding the Vision Ahead 1 page and 2 pages) with preview PDFs.

## Check after every build
Run `soffice --headless --convert-to pdf`, then `pdftoppm -r 40 -png`, then look at every page. Check crops (no cut heads or feet), text overflow and margins before you send anything.

## Status on 16 Nov
Linnea saw the social drafts as a contact sheet. The December plan changes two photos:
- CHN_0720 (walking under the palms) moves to Giving Tuesday, so World Soil Day needs a new photo.
- CHN_0804 (three men laughing) moves to Kisan Diwas, so countdown story 1 needs a new photo.

## Conflict to settle with Linnea
The repo CLAUDE.md (12 Nov) says social posts use only Montserrat, Source Sans 3 and Pathway Gothic One, and no Garamond. These campaign drafts use EB Garamond because she asked for them to match the donor documents, which use EB Garamond. Ask her which rule wins for the campaign posts before you finalize them. The repo rules on variety, text sizes (docs/slide-rules.md), photo_check.py and grid_check.py also apply to anything that goes in the feed.

## Linnea's hard rules (all from her feedback)
- Never crop heads or feet. Check every crop at full size.
- Never reuse a photo. Each photo appears in one post or document only. Avoid HKS_0130 (the tarp group under the shed); it is in Funding the Vision Ahead.
- Brand colours only. Whole-number font sizes. No letter-spacing.
- Logo bottom right, on a calm area. White logo on dark, colour logo on light.
- No mycelium texture on rectangular designs (posts and pages are rectangles).
- No "Link in bio". Write the URL: soilfoodweb.com/donations.
- Real quotes only, word for word. Use [brackets] for any missing name, quote or number. Never invent a quote or a fact about a person.
- Headers are never wider than the body text below them. Stack things on one left edge.
- Every line of text in its own text box. Group multi-line columns. Every element separate and movable, so the PPTX imports cleanly into Canva.
- Do not connect to the SFW Canva account or the SFW Workspace Drive. Use only Linnea's own Drive.
- Send a preview PDF or contact sheet first. Send the PPTX only after she is happy with the preview, or when she asks for PPTX directly.
- When she rejects an element, remove it everywhere.
- Captions: plain, warm, proud, inviting. Subject-verb-object. No em dashes. No flowery biology metaphors.

## Brand tokens
- Soil Food Web Green #156826 (labels, attributions, accent lines)
- Deep green #22371F (bottom bands, Stories background, quote text)
- Light olive #A2AE77 (progress bar fill, small labels on dark)
- Pale sage #DCE3CC (small text on deep green)
- Olive #5F6A3C, Ink #333130 (body text on white)
- Fonts: EB Garamond (headlines, quotes, CTA lines), Source Sans 3 (body, attributions, URLs), Montserrat bold (small labels)
- Font size in PPTX: pt = px x 0.75, rounded. Use px values that give whole pt: 28, 32, 36, 40, 44, 48, 52, 56, 64, 72, 96, 120.

## The campaign post layout (approved look, matches the 4 donor documents)
Feed post 1080 x 1350, margin 72 px. See `curve_photo()`, `band()` and `quote_block()` in `ig.py`.
1. Photo across the top, about 560 to 640 px tall. Its bottom edge is a concave curve (Linnea picked "B": the edge rises in the middle). Curve: y(x) = PH - 6 - 26 x (1 - ((2x / W) - 1)^2). Bake the curve into a PNG mask with PIL, then add a thin Soil Food Web Green freeform line (5 px) along the same curve.
2. White middle area. Content block centred vertically between the curve and the band:
   - small Montserrat bold green label (28 px), such as "Scholar story" or "Giving Tuesday, December 1"
   - green quote mark image beside the quote
   - quote in EB Garamond, deep green, 52 to 56 px, line height 1.18
   - attribution in Source Sans 3 bold green, 32 px: "Name, scholarship student, Country"
3. Deep green band at the bottom, 150 to 200 px. EB Garamond white CTA line (44 to 48 px), a pale sage Source Sans line under it (32 px) with the URL, white logo 96 px tall on the right, vertically centred.

Variants:
- Headline posts (Giving Tuesday, Thank you, LinkedIn): label + EB Garamond headline 72 to 96 px in deep green, then a smaller quote or body line.
- Stories 1080 x 1920 (Giving Tuesday live progress): deep green background, the hay strip across the top with a concave green edge, everything centred: label in light olive, "[AMOUNT RAISED]" in EB Garamond 96 px white (on one line), "raised of our $300,000 goal" 56 px pale sage, a progress bar (track #34532F, fill #A2AE77, 36 px tall, $0 and $300,000 under the ends), the message line 64 px white, the URL 40 px, white logo centred near the bottom. Three versions: morning about 20%, afternoon about 55%, last hours about 85%. A small version note sits in the corner and is deleted before posting.
- LinkedIn board images 1200 x 1200: same system, photo 560 px tall.
- Missing photo: a pale sage block (#E4E9DA) with "[Photo: ...]" centred in olive.

## Photo plan for December (22nd Oct folder in Linnea's Drive, edited "-e" files)
- Giving Tuesday Dec 1: 20261022_CHN_0720-e.jpg, group walking toward the fields under the palms.
- Gerald's reel cover: 20261022_CHN_0245-e.jpg, Gerald with the pitchfork at the compost bin.
- Kisan Diwas Dec 23: 20261022_CHN_0804-e.jpg, three men laughing.
- Already in the campaign kit draft: building-pile (countdown 2, Martin Kihara), bucket-chain (alumni story, Norman Higgins), cert-group (thank you), group-bin, CHN_0545 filling-bin, microscopy-class (3 LinkedIn images). student-microscope is free now.
- Linnea copied 0862, 0864, 0896 and 0959 into a new folder on 16 Nov (folder id 18ajAa47GvAr9U5DL_Dg6CqWsbDdew7oi). Ask her if these are her picks before you use them.

## Real quotes on hand (Testimonials_for_new_website sheet in Linnea's Drive)
- Zoë Unruh, Canada, scholarship: "I just wanted to say thank you so much for allowing me to participate in a class that otherwise would have never been accessible to me."
- Martin Kihara, Kenya, scholarship: "My goal is to turn this knowledge into living topsoil, restored yields, and climate resilience across Kenya."
- Boubacar Tidiane Diallo, Guinea, scholarship: "Through this training, I will strengthen my knowledge of soil biology and share it with farmers, youth, and rural communities across Guinea."
- Anusha Fatima, Pakistan, scholarship: "I want to help repair broken food systems by rebuilding life in the soil."
- Norman Higgins, New Zealand, certified SFW lab tech: "I am so excited to continue this amazing journey as I unlearn 30 years of agrochemical farming and move down the regenerative path to biological understanding."
- Adam Queen, US, lab tech: "This class has opened my eyes and mind up to the microbial world and how it operates. I don't see the world the same now."
- Dr. Elaine Ingham: "Let me teach you so that you can do this for yourself."
- From Evan's campaign doc: "Both founders of TrashIt in Pakistan trained with us, and TrashIt now offers microbial soil testing to farmers." "$5,000 funds a full scholarship." Living Soil Circle: monthly donors whose steady support funds scholarships all year.
- Stephanie: the match amount is unclear, so say "every gift is doubled". Avoid the anniversary angle.

## Wormhole rows for the week of Nov 30 (checked 16 Nov)
- nmw10rs7jfer, Dec 1 "Fundraising campaign (TBD)": delete (plan).
- x20261201, Dec 1 GivingTuesday: caption has placeholders, no visual yet. Replace with the plan version.
- web20261201, Dec 1 webinar reminder: wrong title. Correct: "Monetizing Healthy Soil Creation: Is It Possible", Dr. Craig Kolodge, Wed Dec 2, 9am PT / 17:00 UTC.
- fes20261130, Dec 2 Fall Enrollment last day: caption still says "link in bio".
- x20261203, Dec 3 Costa Rica six weeks to go: visual note says no visual yet; the plan says visual v2 exists. Check.
- Outside the 3-a-week plan on these dates: k20261201, x20261202, p09 (Dora Tkalec), x20261204, pl20261205 (old World Soil Day carousel), pl20261206, w20261206. Ask Linnea which to delete or move.
