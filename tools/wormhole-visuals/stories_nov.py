"""November Stories (Linnea, 4 Nov: "just make some visuals"): Costa Rica info session, webinar "live today" frames,
Fall Enrollment Special countdown, and the 13 Nov Costa Rica Reel cover. 1080 x 1920 news-card look on Food Web Green,
white logo straight on the background (no box). Text kept out of the top 250 and bottom 300 px.

  python3 tools/wormhole-visuals/stories_nov.py
"""
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

import collage
import news_cards as nc
from collage import Deck, cover
from nov_fill import BROWN, CREAM, GREEN, INK, LGREEN, WHITE, box, grain
from regen_news import arrow_disc

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except ImportError:
    pass

SCR = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad"
PW = "/home/user/photos/past-workshop-images/accelerator-workshop-march-2025"


def img(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def head(path):
    return Image.open(path).convert("RGB").crop((470, 300, 1530, 1360))


def placeholder(w=880, h=620):
    im = Image.new("RGB", (w, h), "#D9D4C8")
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(os.path.join(nc.FONTS, "PathwayGothicOne-Regular.ttf"), 64)
    t = "PHOTO: CRAIG KOLODGE"
    d.text(((w - d.textlength(t, font=f)) / 2, h / 2 - 36), t, font=f, fill="#7C7468")
    return im


def story(pid, slug, iso, photo, tab, headline, details, sticker, seed, fx=0.5, fy=0.5):
    collage.H = 1920
    try:
        d = Deck(pid, 1, slug, iso)
        d.bg(0, grain(1080, 1920, seed).convert("RGBA"), name="Background")
        lg = Image.open(WHITE).convert("RGBA")
        lg = lg.resize((200, round(lg.height * 200 / lg.width)), Image.LANCZOS)
        d.put(0, "SFW logo", lg, 72, 60, shadowed=False, anchor="tl")
        cx, cw, top = 72, 936, 300
        px, pw, ph = cx + 28, cw - 56, 620
        first = len(d.items)
        d.put(0, "Photo", cover(photo, pw, ph, fx, fy).convert("RGBA"), px, top + 28, shadowed=False, anchor="tl")
        tw = nc.tab_width(tab)
        box(d, 0, "Tab", GREEN, px, top + 28 + ph - 70, tw, 70)
        d.text(0, "Tab text", tab, px + 22, top + 28 + ph - 64, tw - 30, 62, 50, kind="source-reg", italic=True,
               color=CREAM, lh=1.0, min_size=42)
        hy = top + 28 + ph + 50
        bottom = d.text(0, "Headline", headline, px + 34, hy, pw - 50, 290, 86, kind="montserrat-bold",
                        italic=False, color=BROWN, lh=1.05, min_size=84)
        box(d, 0, "Bar", LGREEN, px, hy + 8, 10, round(bottom) - hy - 14)
        end = round(d.text(0, "Details", details, px + 34, round(bottom) + 22, pw - 50, 260, 52,
                           kind="source-reg", italic=False, color=INK, lh=1.2, min_size=50)) + 50
        if end + (110 if sticker else 0) > 1920 - 300:
            raise SystemExit(f"{pid}: too tall, cut words")
        box(d, 0, "Card", CREAM, cx, top, cw, end - top)
        d.items.insert(first, d.items.pop())
        if sticker:
            d.text(0, "Sticker note", sticker, cx + 4, end + 36, 700, 70, 54, kind="mont-medium", italic=False,
                   color=CREAM, lh=1.0, min_size=50)
            f = ImageFont.truetype(os.path.join(nc.FONTS, "Montserrat-SemiBold.ttf"), 54)
            w = ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(sticker, font=f)
            d.put(0, "Arrow", arrow_disc().resize((56, 56), Image.LANCZOS), cx + 4 + round(w) + 24, end + 42,
                  shadowed=False, anchor="tl")
        p = os.path.join(nc.TILES, f"{pid}-{slug.rsplit('-', 1)[1]}-1.jpg")
        if os.path.exists(p):
            raise SystemExit(f"exists, not overwriting: {p}")
        names, _ = d.save(nc.TILES, nc.DECKS)
        return names[0], d.pptx_name()
    finally:
        collage.H = 1350


STORIES = [
    ("st20261105cr", "costa-rica-info-session-story-v1", "2026-11-05",
     lambda: img(f"{PW}/accelerator-workshop-march-2025-05-group-around-compost-pile.jpg"), "Costa Rica",
     "Info session tomorrow", "Fri 6 Nov, 12pm Pacific, on Zoom. Free, and recorded.", "Sign up", 501),
    ("st20261104web", "webinar-live-today-matt-drane-v1", "2026-11-04", lambda: head(f"{SCR}/web/matt.png"),
     "Free webinar", "Live today, 9am Pacific", "Matt Drane: 15 years of regenerative corn and soy.", "Register", 502),
    ("st20261112web", "webinar-live-today-juan-de-la-serna-v1", "2026-11-12", lambda: head(f"{SCR}/web/juan.png"),
     "Free webinar", "Live today, 9am Pacific", "Juan de la Serna: Johnson-Su compost on real farms.", "Register",
     503),
    ("st20261118web", "webinar-live-today-don-huber-v1", "2026-11-18", lambda: head(f"{SCR}/web/huber.png"),
     "Free webinar", "Live today, 9am Pacific", "Dr. Don M. Huber: agriculture beyond glyphosate.", "Register", 504),
    ("st20261202web", "webinar-live-today-craig-kolodge-v1", "2026-12-02", placeholder, "Free webinar",
     "Live today, 9am Pacific", "Dr. Craig Kolodge: why nematodes make great compost.", "Register", 505),
    ("st20261125bun", "fall-enrollment-one-week-left-v1", "2026-11-25",
     lambda: img(f"{PW}/accelerator-workshop-march-2025-06-staff-and-mentors.jpg"), "Fall Enrollment Special",
     "1 week left", "All four Foundation Courses and a 2027 Compost Intensive seat, in one bundle.", "Enroll", 506),
    ("st20261129bun", "fall-enrollment-three-days-left-v1", "2026-11-29",
     lambda: img(f"{PW}/accelerator-workshop-march-2025-03-feedstock-sacks.jpg"), "Fall Enrollment Special",
     "3 days left", "All four Foundation Courses and a 2027 Compost Intensive seat.", "Enroll", 507),
    ("st20261202bun", "fall-enrollment-last-day-v1", "2026-12-02",
     lambda: img(f"{SCR}/india/raw/03acc3e2-6fc9-43c7-8c8e-ceb00c5a7101(1).jpg"), "Fall Enrollment Special",
     "Last day", "The bundle closes tonight. All four Foundation Courses, one price.", "Enroll", 508),
    ("reel20261113", "costa-rica-reel-cover-v1", "2026-11-13",
     lambda: img(f"{SCR}/crphotos/PXL_20251022_151806888.MP.jpg"), "Costa Rica",
     "Finished the Foundation Courses?", "Your next step: our Accelerator Workshop, 18 to 29 January 2027.", "", 509),
]

if __name__ == "__main__":
    for pid, slug, iso, ph, tab, h, det, st, seed in STORIES:
        print(story(pid, slug, iso, ph(), tab, h, det, st, seed))
