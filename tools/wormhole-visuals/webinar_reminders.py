"""Webinar "join us tomorrow" reminders in the approved Matt Drane reminder look (web20261103-final): a full-bleed
photo, a JOIN US TOMORROW banner, a dark title strip and a cream card with the speaker in a circle, name,
affiliation, date and time. Bigger text per docs/slide-rules.md; logo large in a green square.

Facts from https://webinar.soilfoodweb.com/reg-webinar-fall-webinars (checked 3 Nov): Juan de la Serna, Thu 12 Nov,
9:00am PT; Dr. Don M. Huber, Wed 18 Nov, 9:00am PT. Craig Kolodge, Wed 2 Dec, 9am PT is from Linnea (3 Nov) and is
not on the page yet. Headshots are cropped from the speaker graphics on that page.

  python3 tools/wormhole-visuals/webinar_reminders.py <dir with juan.png and huber.png>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageOps

from collage import Deck, cover
from nov_fill import BROWN, CREAM, DECKS, GREEN, INK, TILES, WHITE, box

W, H = 1080, 1350
PH = "/home/user/photos/new-2026-10"


def circle(img, d=300):
    im = cover(img, d, d, 0.5, 0.4).convert("RGBA")
    m = Image.new("L", (d * 2, d * 2), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d * 2 - 1, d * 2 - 1), fill=255)
    im.putalpha(m.resize((d, d), Image.LANCZOS))
    return im


def placeholder_circle(d=300):
    im = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.ellipse((0, 0, d - 1, d - 1), fill="#D9D4C8")
    return im


def big_logo(d, k, size=170):
    box(d, k, "Logo box", GREEN, W - 72 - size - 36, 72, size + 36, size + 36)
    lg = Image.open(WHITE).convert("RGBA")
    lg = lg.resize((size, round(lg.height * size / lg.width)), Image.LANCZOS)
    d.put(k, "SFW logo", lg, W - 72 - size - 18, 72 + 18 + (size - lg.height) // 2, shadowed=False, anchor="tl")


def reminder(pid, iso, slug, bg, fy, title, head, name, affil, when, time, credit):
    d = Deck(pid, 1, slug, iso)
    d.bg(0, cover(bg, W, H, 0.5, fy).convert("RGBA"), name="Photo")
    # banner
    box(d, 0, "Banner", GREEN, 0, 300, 940, 140)
    d.text(0, "Banner text", "JOIN US TOMORROW", 72, 324, 860, 100, 72, kind="montserrat-bold", italic=False,
           color=CREAM, lh=1.0, min_size=66)
    big_logo(d, 0)
    # title strip and card
    top = 690
    first = len(d.items)
    tb = d.text(0, "Talk title", title, 104, top + 30, 872, 200, 52, kind="montserrat-bold", italic=False,
                color=CREAM, lh=1.12, min_size=50)
    strip_h = round(tb) - top + 30
    box(d, 0, "Title strip", BROWN, 72, top, 936, strip_h)
    d.items.insert(first, d.items.pop())
    ct = top + strip_h
    box(d, 0, "Card", CREAM, 72, ct, 936, 1290 - ct)
    d.put(0, f"Photo: {name}", head, 102, ct + 40, shadowed=False, anchor="tl")
    y = d.text(0, "Name", name, 440, ct + 40, 540, 170, 66, kind="montserrat-bold", italic=False, color=BROWN,
               lh=1.05, min_size=66)
    y = d.text(0, "Affiliation", affil, 440, round(y) + 10, 540, 150, 42, kind="source-reg", italic=False,
               color=INK, lh=1.15, min_size=42)
    y = d.text(0, "Date", when, 440, round(y) + 22, 540, 70, 52, kind="montserrat-bold", italic=False, color=GREEN,
               lh=1.0, min_size=50)
    d.text(0, "Time", time, 440, round(y) + 8, 540, 70, 52, kind="source-reg", italic=False, color=INK, lh=1.0,
           min_size=50)
    d.text(0, "Credit", credit, 72, 1300, 936, 44, 42, kind="source-reg", italic=False, color=CREAM, lh=1.0,
           align="right", shade=True, min_size=42)
    return d


def head_from_graphic(path):
    """The speaker photo inside the webinar graphic (2000 x 2000): a square around the face."""
    return Image.open(path).convert("RGB").crop((470, 300, 1530, 1360))


if __name__ == "__main__":
    src = sys.argv[1]
    posts = [
        reminder("web20261111", "2026-11-11", "webinar-reminder-juan-de-la-serna-v1",
                 ImageOps.exif_transpose(Image.open(f"{PH}/community-field-walk-norfolk-jun-2025.jpg")).convert("RGB"),
                 0.5, "Johnson-Su compost on real farms", circle(head_from_graphic(f"{src}/juan.png")),
                 "Juan de la Serna", "Resoilutions", "Thu 12 Nov", "9am Pacific, free",
                 "Field walk, Norfolk, June 2025"),
        reminder("web20261117", "2026-11-17", "webinar-reminder-don-huber-v1",
                 ImageOps.exif_transpose(Image.open(f"{PH}/wild-ken-hill-group-in-field.jpg")).convert("RGB"),
                 0.5, "Agriculture beyond glyphosate", circle(head_from_graphic(f"{src}/huber.png")),
                 "Dr. Don M. Huber", "Emeritus Professor of Plant Pathology, Purdue University", "Wed 18 Nov",
                 "9am Pacific, free", "Wild Ken Hill, Norfolk"),
        reminder("web20261201", "2026-12-01", "webinar-reminder-craig-kolodge-v1",
                 ImageOps.exif_transpose(Image.open(f"{PH}/Bacterial-feeding nematode, 40x obj, Talbot Armstrong.jpg"))
                 .convert("RGB"), 0.5, "Why nematodes make great compost", placeholder_circle(),
                 "Dr. Craig Kolodge", "[affiliation]", "Wed 2 Dec", "9am Pacific, free",
                 "Bacterial-feeding nematode. Photo: Talbot Armstrong"),
    ]
    for d in posts:
        assert not os.path.exists(os.path.join(TILES, f"{d.id}-v1-1.jpg")), d.id
        print(d.save(TILES, DECKS)[0], d.pptx_name())
