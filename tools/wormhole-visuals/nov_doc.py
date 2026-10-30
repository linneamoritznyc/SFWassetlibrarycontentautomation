"""Visuals for the 12 posts in the November 2026 planning doc (Stephanie and Allison, 30 Oct: these first).

  python3 tools/wormhole-visuals/nov_doc.py [ids...]
    crinfo20261105  Costa Rica info session reminder, event card on a real Costa Rica class photo
    x20261108       Diwali, one watercolor (watercolor_gen.py "diwali-diya") on warm white paper
"""
import sys

from PIL import ImageEnhance, ImageOps, Image

from collage import cover
from jan_varied import (BROWN, CREAM, FWG, INK, LGREEN, band, body, credit, eyebrow, head, logo)
from novdec import REG, W, build, post
from watercolor_posts import wc

CR_CLASS = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/crphotos/PXL_20251024_162714282.jpg"
PAPER = "#FBF9F4"


@post("crinfo20261105", "2026-11-05", "costa-rica-info-session-v1", 1, FWG)
def info_session(p):
    """M, event card: the class listening in the shed at Armonía, a cream card with the date block."""
    im = ImageOps.exif_transpose(Image.open(CR_CLASS)).convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(1.35)
    p.put(0, "photo", cover(im, W, 640, 0.5, 0.55).convert("RGBA"), 0, 0)
    band(p, 0, CREAM, 560, 690, x=60, w=960, name="card")
    band(p, 0, LGREEN, 560, 14, x=60, w=960, name="card-top")
    eyebrow(p, 0, "FREE LIVE INFO SESSION", CREAM, y=610, x=110)
    head(p, 0, "Costa Rica Accelerator Workshop", CREAM, y=665, x=110, w=860, size=66, h=170)
    band(p, 0, BROWN, 860, 220, x=110, w=330, name="date-block")
    p.d.text(0, "day", "FRI 6 NOV", 120, 885, 310, 70, 58, kind="pathway", italic=False, color=CREAM, lh=1.0,
             align="center", track=2)
    p.d.text(0, "time", "12pm Pacific", 120, 965, 310, 70, 44, kind="montserrat-bold", italic=False, color=CREAM,
             lh=1.0, align="center")
    p.d.text(0, "how", "Live on Zoom. Meet the team, ask your questions. Recorded for anyone who can't join live.",
             480, 870, 500, 220, 34, kind="source-reg", italic=False, color=INK, lh=1.3, min_size=26)
    p.d.text(0, "cta", "LINK IN BIO", 110, 1130, 600, 60, 48, kind="pathway", italic=False, color=FWG, lh=1.0,
             track=3)
    credit(p, 0, "Photo: Soil Food Web Foundation (Costa Rica, October 2025)", FWG, y=1290, x=60, w=700)
    logo(p, 0, FWG, size=110)


@post("x20261108", "2026-11-08", "happy-diwali-v6", 1, PAPER)
def diwali(p):
    """W, watercolor: a clay diya on living soil with marigolds, greeting above in brand type."""
    eyebrow(p, 0, "8 NOVEMBER", PAPER, y=110, color=FWG)
    head(p, 0, "Happy Diwali", PAPER, y=170, size=120, h=160, color=BROWN)
    body(p, 0, "To our students, mentors and partners in India, and to everyone celebrating around the world.",
         PAPER, 330, size=40, w=900, color=INK)
    art = wc("diwali-diya", w=1000)
    p.put(0, "watercolor", art, (W - art.width) // 2, p.h - 40 - art.height)
    logo(p, 0, PAPER, size=140)


FAMILY = {"crinfo20261105": "M, event card", "x20261108": "W, watercolor"}

if __name__ == "__main__":
    for pid in sys.argv[1:] or list(FAMILY):
        print(pid, build(pid)["tiles"])
