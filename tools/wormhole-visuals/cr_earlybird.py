"""Costa Rica Accelerator Workshop, Early Nematode Discount ends 4 November (post cr20261103, 3 Nov 2026).

Six 1080 x 1350 slides in the trifold look: real Costa Rica workshop photos, flat full-colour boxes with hard
edges overlapping them, short large text inside the boxes. The Food Web Green box on slide 1 runs off the
right edge and comes back as the full-height band on slide 2, so the carousel reads as one strip.
Colours and fonts from the new website (final-sfwsite-linnea css/site.css): Montserrat headings, Source Sans 3.

  python3 tools/wormhole-visuals/cr_earlybird.py <photo dir> [preview.png]
    -> apps/web/public/wormhole/decks/03-11-2026-costa-rica-early-bird.pptx (editable: every photo, box,
       text and the logo its own layer; the photo file for each slide in the speaker notes)
"""
import io
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageStat
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except ImportError:  # only needed for the .HEIC on slide 1
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DECK = os.path.join(REPO, "apps", "web", "public", "wormhole", "decks", "03-11-2026-costa-rica-early-bird.pptx")
LOGO = "/home/user/sfwlib/img/sfwlogo-240.png"
FONTS = os.environ.get("SFW_FONTS", "/root/.fonts")

W, H = 1080, 1350
EMU = 9525  # per pixel at 96 dpi
GREEN, SOIL, CREAM, INK, BLUE = "#156826", "#4F3433", "#F4F1EA", "#333130", "#3780B8"
HEAD, BODY = ("Montserrat", "Montserrat-Bold.ttf"), ("Source Sans 3", "SourceSans3-SemiBold.ttf")

SLIDES = [
    # (photo file, catalog note)
    ("IMG_4534.HEIC", "Costa Rica Oct 2025, Armonía: laughing around the wire mesh bin with a thermometer"),
    ("PXL_20251022_151710920.MP.jpg", "Costa Rica Oct 2025, Armonía: wide view of the shed, several teams building at once"),
    ("PXL_20240716_224324982_HandsInSoil.jpg", "Costa Rica Jul 2024, Armonía: hands in woody compost (HandsInSoil)"),
    ("PXL_20251020_222404850.jpg + Compost_Tea_Prep.jpg",
     "Costa Rica Oct 2025: frothy brew in the blue tub (top); Costa Rica Jul 2024: Compost Tea Prep bucket brewer (bottom)"),
    ("PXL_20251023_191907277.jpg", "Costa Rica Oct 2025, Armonía: class watching live microscopy on screen (Drive ID 1YTuACdcqtVqv99HAArkRDlBUYdnCP8KZ), brightened"),
    ("PXL_20251022_172210012.jpg", "Costa Rica Oct 2025, Armonía: the class under the big tree in the forest"),
]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def photo(path, w, h, fx=0.5, fy=0.5, lift=None):
    """Crop to w x h around (fx, fy); lift the brightness of a dark shot so it reads on a phone."""
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(im.width * fx - w / 2)), im.width - w)
    y = min(max(0, round(im.height * fy - h / 2)), im.height - h)
    im = im.crop((x, y, x + w, y + h))
    mean = ImageStat.Stat(im.convert("L")).mean[0]
    if lift is None:
        lift = 1.0 if mean > 118 else min(1.35, 128 / max(mean, 1))
    if lift != 1.0:
        im = ImageEnhance.Brightness(im).enhance(lift)
        im = ImageEnhance.Contrast(im).enhance(1.04)
    return im


class Strip:
    """Every layer of the six slides in strip coordinates (slide k starts at x = k * W)."""

    def __init__(self, src):
        self.src = src
        self.layers = []

    def pic(self, k, name, im, x, y):
        self.layers.append(("pic", k, name, im, x, y))

    def box(self, name, color, x0, y0, x1, y1):
        self.layers.append(("box", None, name, color, (x0, y0, x1, y1)))

    def text(self, k, name, s, x, y, w, h, size, font, color, align="left", anchor="top"):
        self.layers.append(("text", k, name, s, (x, y, w, h), size, font, color, align, anchor))


def build(src):
    st = Strip(src)
    P = lambda f: os.path.join(src, f)  # noqa: E731

    # 1. Hook: full-bleed photo, green box in the lower third running off the right edge
    st.pic(0, "photo IMG_4534", photo(P("IMG_4534.HEIC"), W, H, 0.5, 0.42), 0, 0)
    st.box("green band (continues into slide 2)", GREEN, 60, 830, W + 400, 1230)  # into slide 2
    st.box("green band slide 2", GREEN, W, 0, W + 400, H)
    st.text(0, "headline", "Early Nematode Discount ends tomorrow", 110, 870, 930, 200, 64, HEAD, CREAM)
    st.text(0, "small line", "Accelerator Workshop · Costa Rica", 112, 1150, 900, 50, 38, BODY, CREAM)

    # 2. Ten days: the band from slide 1 on the left, the shed on the right two thirds
    st.pic(1, "photo PXL_20251022_151710920", photo(P("PXL_20251022_151710920.MP.jpg"), W - 400, H, 0.55, 0.55),
           W + 400, 0)
    st.text(1, "headline", "Ten days of hands‑on training", W + 40, 300, 340, 520, 58, HEAD, CREAM)

    # 3. Compost: photo top 60%, Soil Brown box overlapping it at the bottom
    k = 2 * W
    st.pic(2, "photo HandsInSoil", photo(P("PXL_20240716_224324982_HandsInSoil.jpg"), W, 830, 0.5, 0.55), k, 0)
    st.box("soil brown box", SOIL, k, 760, k + W, H)
    st.text(2, "headline", "Build BioComplete™ compost with your team", k + 80, 860, 900, 380, 72, HEAD, CREAM)

    # 4. Extracts and teas: two photos stacked, a cream box across the seam
    k = 3 * W
    st.pic(3, "photo PXL_20251020_222404850", photo(P("PXL_20251020_222404850.jpg"), W, 675, 0.5, 0.45), k, 0)
    st.pic(3, "photo Compost Tea Prep", photo(P("Compost_Tea_Prep.jpg"), W, 675, 0.5, 0.38), k, 675)
    st.box("cream box", CREAM, k + 140, 545, k + W, 805)
    st.text(3, "headline", "Brew extracts and teas", k + 200, 545, 840, 260, 74, HEAD, SOIL, anchor="middle")

    # 5. Microscope: the classroom, brightened, Education Blue box top left
    k = 4 * W
    st.pic(4, "photo PXL_20251023_191907277", photo(P("PXL_20251023_191907277.jpg"), W, H, 0.5, 0.5, lift=1.32),
           k, 0)
    st.box("education blue box", BLUE, k, 0, k + 760, 470)
    st.text(4, "headline", "Read the biology, with a mentor beside you", k + 70, 90, 640, 340, 66, HEAD, CREAM)

    # 6. Close: the class under the big tree, green box centre bottom with the logo
    k = 5 * W
    st.pic(5, "photo PXL_20251022_172210012", photo(P("PXL_20251022_172210012.jpg"), W, H, 0.5, 0.42), k, 0)
    st.box("green box", GREEN, k + 90, 740, k + 990, 1280)
    st.text(5, "title", "Accelerator Workshop", k + 150, 790, 800, 80, 58, HEAD, CREAM)
    st.text(5, "place", "Heredia, Costa Rica", k + 152, 895, 760, 60, 44, BODY, CREAM)
    st.text(5, "dates", "January 18–29, 2027", k + 152, 955, 760, 60, 44, BODY, CREAM)
    st.text(5, "cta", "Register, link in bio", k + 150, 1105, 580, 70, 48, HEAD, CREAM)
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((130, round(logo.height * 130 / logo.width)), Image.LANCZOS)
    disc = Image.new("RGBA", (170, 170), (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse((0, 0, 169, 169), fill=rgb(CREAM) + (255,))
    disc.alpha_composite(logo, (20, (170 - logo.height) // 2))
    st.pic(5, "logo", disc, k + 790, 1080)
    return st


# ------------------------------------------------------------------ PowerPoint
def pptx(st, path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(W * EMU), Emu(H * EMU)
    slides = [prs.slides.add_slide(prs.slide_layouts[6]) for _ in range(6)]
    for i, sl in enumerate(slides):
        f, note = SLIDES[i]
        sl.notes_slide.notes_text_frame.text = f"Photo: {f}\n{note}"
    order = {"pic": 0, "box": 1, "text": 2}
    for lay in sorted(st.layers, key=lambda L: order[L[0]] if not (L[0] == "pic" and L[2] == "logo") else 3):
        if lay[0] == "pic":
            _, k, name, im, x, y = lay
            buf = io.BytesIO()
            (im.save(buf, "PNG") if im.mode == "RGBA" else im.save(buf, "JPEG", quality=90))
            buf.seek(0)
            p = slides[k].shapes.add_picture(buf, Emu((x - k * W) * EMU), Emu(y * EMU), Emu(im.width * EMU),
                                            Emu(im.height * EMU))
            p.name = name
        elif lay[0] == "box":
            _, _, name, color, (x0, y0, x1, y1) = lay
            for k in range(6):  # a box that crosses a slide edge becomes one piece on each slide
                a, b = max(x0, k * W), min(x1, (k + 1) * W)
                if b <= a:
                    continue
                s = slides[k].shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu((a - k * W) * EMU), Emu(y0 * EMU),
                                               Emu((b - a) * EMU), Emu((y1 - y0) * EMU))
                s.name = name
                s.fill.solid()
                s.fill.fore_color.rgb = RGBColor(*rgb(color))
                s.line.fill.background()
                s.shadow.inherit = False
        else:
            _, k, name, s, (x, y, w, h), size, font, color, align, anchor = lay
            tb = slides[k].shapes.add_textbox(Emu((x - k * W) * EMU), Emu(y * EMU), Emu(w * EMU), Emu(h * EMU))
            tb.name = name
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE if anchor == "middle" else MSO_ANCHOR.TOP
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if align == "center" else PP_ALIGN.LEFT
            p.line_spacing = 1.05
            r = p.add_run()
            r.text = s
            r.font.name = font[0]
            r.font.size = Pt(size * 0.75)
            r.font.bold = font is HEAD
            r.font.color.rgb = RGBColor(*rgb(color))
    prs.save(path)


if __name__ == "__main__":
    st = build(sys.argv[1])
    pptx(st, DECK)
    print(DECK)
