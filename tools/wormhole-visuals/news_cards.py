"""Every news post in the news card format (Linnea, 31 Oct: "they all have to follow the news sharing template").

The format is savesoil.py / the 39% study v5 (nov_fill.news_card): Food Web Green grain, logo disc top left, one
cream card with the article image, outlet tab, credit, green bar + headline and blurb, then Read More and the source
under the card. Fact slides: one cream card, green bar, headline and detail. Roundups (Fun Soil News) get one full
news card per story. Text at docs/slide-rules.md sizes: headlines 84 px, small text 52 px, floor 42.

Article images are cropped from each post's own earlier visual, so no photo moves between posts.
LinkedIn-only posts get the 1200 x 627 card from savesoil.linkedin, drawn here with the same fonts.

  python3 tools/wormhole-visuals/news_cards.py [post ids]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from collage import Deck, cover
from nov_fill import BROWN, CREAM, GREEN, INK, LGREEN, box, grain
from regen_news import arrow_disc, logo_disc

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TILES = os.path.join(REPO, "apps", "web", "public", "wormhole", "tiles")
DECKS = os.path.join(REPO, "apps", "web", "public", "wormhole", "decks")
FONTS = "/root/.fonts"
W, H = 1080, 1350
BODY = "#6E5452"
VERSION = "nc1"  # tiles <id>-nc1-<n>.jpg


def tile(name, box_=None):
    im = Image.open(os.path.join(TILES, name)).convert("RGB")
    return im.crop(box_) if box_ else im


def placeholder(w, h, label="ARTICLE IMAGE"):
    im = Image.new("RGB", (w, h), "#D9D4C8")
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(os.path.join(FONTS, "PathwayGothicOne-Regular.ttf"), 56)
    tw = d.textlength(label, font=f)
    d.text(((w - tw) / 2, h / 2 - 34), label, font=f, fill="#7C7468")
    return im


def tab_width(text, size=50):
    f = ImageFont.truetype(os.path.join(FONTS, "SourceSans3-Italic.ttf"), size)
    return round(ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(text, font=f)) + 44


# ------------------------------------------------------------------ Instagram 4:5
CX, CW = 72, 936
PX, PW, PH = CX + 28, CW - 56, 400


def card(d, k, img, tab, credit, headline, blurb, source):
    """One full news card on slide k."""
    top = 150
    box(d, k, "Card", CREAM, CX, top, CW, 980)
    py = top + 28
    im = img if img is not None else placeholder(PW, PH)
    d.put(k, f"Article image: {credit or 'to add'}", cover(im, PW, PH, 0.5, 0.5).convert("RGBA"), PX, py,
          shadowed=False, anchor="tl")
    tw = min(tab_width(tab), PW)
    box(d, k, "Tab", GREEN, PX, py + PH - 70, tw, 70)  # the outlet's name, italic, as on the pinned NYT card
    d.text(k, "Tab text", tab, PX + 22, py + PH - 64, tw - 30, 62, 50, kind="source-reg", italic=True, color=CREAM,
           lh=1.0, min_size=42)
    if credit:
        d.text(k, "Credit", credit, PX, py + PH + 10, PW, 50, 42, kind="source-reg", italic=False, color=BODY, lh=1.0,
               align="right", min_size=42)
    hy = py + PH + 72
    bottom = d.text(k, "Headline", headline, PX + 34, hy, PW - 50, 290, 84, kind="montserrat-bold", italic=False,
                    color=BROWN, lh=1.05, min_size=84)
    box(d, k, "Bar", LGREEN, PX, hy + 8, 10, round(bottom) - hy - 14)
    d.text(k, "Details", blurb, PX + 34, round(bottom) + 22, PW - 50, top + 980 - round(bottom) - 40, 52,
           kind="source-reg", italic=False, color=INK, lh=1.2, min_size=50)
    y = top + 980 + 26
    d.text(k, "Read More", "Read More", CX + 4, y + 4, 300, 64, 52, kind="mont-medium", italic=False, color=CREAM,
           lh=1.0, min_size=50)
    d.put(k, "Arrow", arrow_disc().resize((48, 48), Image.LANCZOS), CX + 318, y + 10, shadowed=False, anchor="tl")
    d.text(k, "Source", "Source:\n" + source, CX + 400, y, CW - 400, H - y - 12, 42, kind="source-reg", italic=False,
           color=CREAM, lh=1.12, align="right", min_size=42)


def fact(d, k, headline, detail):
    y_h = d.text(k, "Headline", headline, 166, 0, 790, 460, 84, kind="montserrat-bold", italic=False, color=BROWN,
                 lh=1.05, min_size=84)
    h_item = d.items[-1]
    y_d = d.text(k, "Details", detail, 166, round(y_h) + 32, 790, 420, 52, kind="source-reg", italic=False,
                 color=INK, lh=1.22, min_size=50)
    d_item = d.items[-1]
    card_h = round(y_d) + 2 * 80
    top = (H - card_h) // 2
    h_item["y"] += top + 80
    d_item["y"] += top + 80
    box(d, k, "Card", CREAM, CX, top, CW, card_h)
    box(d, k, "Bar", LGREEN, 124, top + 90, 10, round(y_h) - 14)


def instagram(pid, iso, slug, cards, facts=(), seed=339):
    n = len(cards) + len(facts)
    d = Deck(pid, n, f"{slug}-{VERSION}" if VERSION.startswith("v") else f"{slug}-v{VERSION}", iso)
    d.bg(None, grain(W * n, H, seed).convert("RGBA"), name="Background")
    for k in range(n):
        d.put(k, "Logo", logo_disc(110), 40, 36, shadowed=False, anchor="tl")
    for k, c in enumerate(cards):
        card(d, k, *c)
    for k, (h, det) in enumerate(facts, start=len(cards)):
        fact(d, k, h, det)
    return d


# ------------------------------------------------------------------ LinkedIn 1200 x 627
def linkedin(pid, img, tab, credit, headline, blurb, source, seed=341):
    LW, LH = 1200, 627
    out = grain(LW, LH, seed).convert("RGB")
    d = ImageDraw.Draw(out)
    F = lambda name, s: ImageFont.truetype(os.path.join(FONTS, name), s)  # noqa: E731
    cx0, cy0, cx1, cy1 = 40, 40, 1160, 530
    d.rectangle((cx0, cy0, cx1, cy1), fill=CREAM)
    px0, py0, px1, py1 = cx0 + 22, cy0 + 22, cx0 + 22 + 470, cy1 - 22
    out.paste(cover(img, px1 - px0, py1 - py0, 0.5, 0.45).convert("RGB"), (px0, py0))
    tf = F("SourceSans3-Italic.ttf", 36)
    tw = d.textlength(tab, font=tf)
    d.rectangle((px0, py1 - 54, px0 + tw + 36, py1), fill=GREEN)
    d.text((px0 + 18, py1 - 49), tab, font=tf, fill=CREAM)

    def wrap(text, f, width):
        lines, cur = [], ""
        for w in text.split():
            t = f"{cur} {w}".strip()
            if d.textlength(t, font=f) <= width:
                cur = t
            else:
                lines.append(cur)
                cur = w
        return lines + [cur]

    tx, tw_ = px1 + 40, cx1 - px1 - 40 - 40
    hf = F("Montserrat-Bold.ttf", 54)
    hl = wrap(headline, hf, tw_ - 34)
    if len(hl) > 4:
        raise SystemExit(f"{pid}: LinkedIn headline too long, cut words")
    y = cy0 + 40
    d.rectangle((tx, y + 6, tx + 8, y + len(hl) * 62 - 6), fill=LGREEN)
    for ln in hl:
        d.text((tx + 34, y), ln, font=hf, fill=BROWN)
        y += 62
    bf = F("SourceSans3-Regular.ttf", 32)
    bl = wrap(blurb, bf, tw_ - 34)
    y += 16
    if y + len(bl) * 40 > cy1 - 50:
        raise SystemExit(f"{pid}: LinkedIn blurb too long, cut words")
    for ln in bl:
        d.text((tx + 34, y), ln, font=bf, fill=INK)
        y += 40
    cf = F("SourceSans3-Regular.ttf", 22)
    d.text((cx1 - 22 - d.textlength(credit, font=cf), cy1 - 36), credit, font=cf, fill=BODY)
    rf = F("Montserrat-SemiBold.ttf", 30)
    d.text((cx0 + 4, cy1 + 30), "Read More", font=rf, fill=CREAM)
    ax = cx0 + 4 + d.textlength("Read More", font=rf) + 14
    out.paste(arrow_disc().resize((34, 34), Image.LANCZOS), (round(ax), cy1 + 33), arrow_disc().resize((34, 34)))
    sf = F("SourceSans3-Regular.ttf", 26)
    s = "Source: " + source
    d.text((cx1 - d.textlength(s, font=sf), cy1 + 34), s, font=sf, fill=CREAM)
    name = f"{pid}-{VERSION}-1.jpg"
    path = os.path.join(TILES, name)
    if os.path.exists(path):
        raise SystemExit(f"exists, not overwriting: {path}")
    out.save(path, quality=90, optimize=True, progressive=True)
    return [name]


# ------------------------------------------------------------------ the posts
SHEFF = "doi.org/10.1016/j.cub.2026.09.061"
FLIND = "doi.org/10.1111/mec.70552"
OWN = "Illustration: Soil Food Web Foundation"
MAPS = "Map: Natural Earth (public domain)"


def fun_template(pid, iso, slug, month, n):
    cards = [(None, "Fun Soil News", None, f"Fun Soil News: {month}",
              f"{n} good stories from the soil this month.", "in the caption")]
    cards += [(None, "Outlet name", "Photo credit", f"Story {i}: short headline here",
               "One sentence: what happened, where.", "the article link") for i in range(1, n + 1)]
    return instagram(pid, iso, slug, cards)


POSTS = {
    "n20261023a": lambda: instagram(
        "n20261023a", "2026-10-27", "mustard-plant-fungus-news",
        [(tile("n20261023a-1.jpg", (0, 640, 1000, 1095)), "University of Sheffield", OWN,
          "A plant said to skip fungi traded food with one",
          "University of Sheffield, Current Biology, 15 Oct 2026.", SHEFF)],
        [("The plant: Arabidopsis", "A small mustard plant. Its family lost the genes most plants use to welcome "
                                    "fungal partners."),
         ("The fungus", "A Mucoromycotina fine root endophyte, from an ancient group of soil fungi."),
         ("Nitrogen and phosphorus in", "The fungus carried both from the soil into the plant's shoots. The plant "
                                        "grew normally."),
         ("260% more carbon out", "In return, the fungus received more than 260% more of the plant's carbon."),
         ("Next: cabbage and canola", "Same plant family. The team wants to learn what this means for crops."),
         ("Read the study", "University of Sheffield, led by Professor Katie Field. Current Biology, October 2026. "
                            "Link in bio.")], seed=401),
    "n20261024a": lambda: instagram(
        "n20261024a", "2026-10-28", "restored-land-soil-fungi-news",
        [(tile("n20261024a-1.jpg", (0, 890, 900, 1299)), "Flinders University", OWN,
          "Soil fungi lag behind replanted land",
          "Flinders University, Molecular Ecology, October 2026.", FLIND)],
        [("Six years later", "A team led by Professor Martin Breed sampled the soil fungi in replanted farmland "
                             "again."),
         ("The work came back", "What the fungi do in the soil, cycling nutrients and breaking down organic matter, "
                                "kept recovering."),
         ("The community lagged", "The mix of fungal species changed very little."),
         ("A likely brake", "The farming history: soils still rich in leftover nutrients."),
         ("Measure below ground", "Trees are the part of restoration we can see. The soil food web runs on its own "
                                  "timeline."),
         ("Read the study", "Flinders University, Molecular Ecology, October 2026. Link in bio.")], seed=402),
    "k20261030": lambda: instagram(
        "k20261030", "2026-10-30", "mycorrhizal-cotton-news",
        [(tile("k20261030-v1-1.jpg", (80, 520, 1020, 947)), "European Journal of Soil Biology", OWN,
          "Fungi reach 15 times more soil than cotton roots",
          "A pick from our mentor Dr. Carla Portugal.",
          "doi.org/10.1016/j.ejsobi.2018.12.002")],
        [("About 30 mm out", "Mycorrhizal hyphae took up phosphorus and moved it to the plant from up to 3 cm "
                             "beyond the root."),
         ("Less soluble P, more hyphae", "Low soluble phosphorus promoted hyphal growth. High soluble phosphorus "
                                         "held it back."),
         ("A moderate rate won", "Cotton took up the most phosphorus at 150 kg P2O5 per hectare."),
         ("Carla's caveat", "One crop, one field, fungi and soil chemistry only. The rest of the soil food web was "
                            "not measured."),
         ("Read the paper", "Mai et al. 2019, European Journal of Soil Biology 90: 31-35. Link in bio.")], seed=403),
    "ev-02": lambda: instagram(
        "ev-02", "2026-11-18", "beopen-earth-news",
        [(tile("ev-02-v2-1.jpg", (0, 200, 1080, 691)), "BeOpen", "Soil bacteria. Photo: Gerri Gassert",
          "An open atlas of soil life from 100,000 samples",
          "By Biome Makers: soil life from over 90 countries.", "beopen.earth/atlas")],
        [("One protocol, 90+ countries", "Every sample is collected, sequenced and analysed the same way, so "
                                         "continents can be compared."),
         ("Open data", "Researchers get raw reads and processed data for free."),
         ("200+ research partners", "And 3,000 datasets so far. Labs can join as contributors."),
         ("Explore the atlas", "beopen.earth/atlas. Link in bio.")], seed=404),
    "p17": lambda: instagram(
        "p17", "2026-10-31", "fun-soil-news-october-news",
        [(tile("p17-f1-1.jpg", (0, 560, 1040, 1033)), "Fun Soil News", "Maps: Natural Earth (public domain)",
          "Three soil stories from October", "A giant fungus, plastic-eating bacteria, returning fungi.",
          "in the caption"),
         (tile("p17-f1-2.jpg", (0, 380, 1000, 835)), "Frontiers in Fungal Biology", MAPS,
          "A giant fungus grows up to 50 cm tall",
          "Dianjunus rex, from oak roots in Yunnan, China.",
          "doi.org/10.3389/ffunb.2026.1940464"),
         (tile("p17-f1-3.jpg", (20, 520, 980, 956)), "The ISME Journal", OWN,
          "Forest soil bacteria ate bioplastic",
          "Films gone in 250 to 330 days. Konstanz, Germany.",
          "doi.org/10.1093/ismejo/wrag203"),
         (tile("p17-f1-4.jpg", (40, 450, 1000, 886)), "Molecular Ecology", MAPS,
          "Soil fungi back at work after replanting",
          "Six years of recovery in South Australia.", FLIND)], seed=405),
    "pl20261127": lambda: fun_template("pl20261127", "2026-11-27", "fun-soil-news-november-news", "November 2026", 5),
    "pl20261218": lambda: fun_template("pl20261218", "2026-12-18", "fun-soil-news-december-news", "December 2026", 5),
    "j20270130": lambda: fun_template("j20270130", "2027-01-30", "fun-soil-news-january-news", "January 2027", 3),
}

TOI_IMG = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/toi/f63.jpg"
POSTS["toi20261031"] = lambda: Deck_toi()


def Deck_toi():
    """Times of India, 30 Oct 2026, on the India Accelerator Workshop. Frame at 63 s of sfw-india-aw-film-draft.mp4
    (Linnea's Drive): the group under the shed at the Save Soil farm."""
    global VERSION
    VERSION = "v1"
    return instagram(
        "toi20261031", "2026-10-31", "times-of-india-coimbatore-workshop",
        [(Image.open(TOI_IMG).convert("RGB"), "The Times of India", "Photo: Soil Food Web Foundation, Coimbatore",
          "The Times of India covered our India workshop", "Coimbatore, Tamil Nadu. 30 October 2026.",
          "timesofindia.indiatimes.com/\narticleshow/135370094.cms")],
        [("46 participants, 10 countries", "Farmers, soil scientists, microbiologists and consultants, from seven "
                                           "Indian states and abroad."),
         ("At the Save Soil model farm", "Ten days at Sadhguru's Save Soil Regenerative Revolution farm, in "
                                         "collaboration with Isha Outreach."),
         ("Compost to microscope", "BioComplete™ compost, compost extracts and teas, soil sampling and microscopy "
                                   "sessions."),
         ("61 more at the seminar", "The two-day Life in the Soil Seminar came first, on 16 and 17 October."),
         ("Read the article", "The Times of India, 30 October 2026. Link in bio.")], seed=406)


LINKEDIN = {
    "j20270109b": lambda: linkedin(
        "j20270109b", tile("j20270109b-v2-1.jpg", (60, 0, 560, 350)), "Save Soil", "Photo: Soil Food Web Foundation",
        "10 billion microorganisms in one gram of soil",
        "Save Soil's article \"What's Missing? Life.\" by Lu Yu, citing Dr. Elaine Ingham.",
        "consciousplanet.org/save-soil/news"),
    "j20270123a": lambda: linkedin(
        "j20270123a", tile("j20270123a-v2-1.jpg", (100, 0, 700, 405)), "Save Soil", "Photo: Soil Food Web Foundation",
        "33 million fertility trees in West Africa",
        "Save Soil's interview with Dr. Nathalie Benziwa Johnson on APAF's agroforestry.",
        "consciousplanet.org/save-soil/news", seed=342),
}

if __name__ == "__main__" and sys.argv[1:] != ["toi-options"]:
    for pid in sys.argv[1:] or list(POSTS) + list(LINKEDIN):
        if pid in LINKEDIN:
            print(pid, LINKEDIN[pid]())
            continue
        d = POSTS[pid]()
        for k in range(1, d.n + 1):
            p = os.path.join(TILES, f"{pid}-{VERSION}-{k}.jpg")
            if os.path.exists(p):
                raise SystemExit(f"exists, not overwriting: {p}")
        names, _ = d.save(TILES, DECKS)
        print(pid, names, d.pptx_name())


# ------------------------------------------------------------------ Times of India options (Linnea, 31 Oct)
TOI_DIR = os.path.dirname(TOI_IMG)


def frame(name):
    return Image.open(os.path.join(TOI_DIR, name + ".jpg")).convert("RGB")


def photo_fact(d, k, img, headline, detail):
    """A fact card with a workshop photo on top: same card, bar and type as the news card."""
    top = 150
    box(d, k, "Card", CREAM, CX, top, CW, 1050)
    d.put(k, "Photo", cover(img, PW, 470, 0.5, 0.5).convert("RGBA"), PX, top + 28, shadowed=False, anchor="tl")
    hy = top + 28 + 470 + 44
    bottom = d.text(k, "Headline", headline, PX + 34, hy, PW - 50, 200, 84, kind="montserrat-bold", italic=False,
                    color=BROWN, lh=1.05, min_size=84)
    box(d, k, "Bar", LGREEN, PX, hy + 8, 10, round(bottom) - hy - 14)
    d.text(k, "Details", detail, PX + 34, round(bottom) + 22, PW - 50, top + 1050 - round(bottom) - 40, 52,
           kind="source-reg", italic=False, color=INK, lh=1.2, min_size=50)


TOI_SRC = "timesofindia.indiatimes.com/\narticleshow/135370094.cms"
TOI_CREDIT = "Photo: Soil Food Web Foundation, Coimbatore"


def toi_b():
    n = 5
    d = Deck("toi20261031", n, "times-of-india-coimbatore-workshop-v2", "2026-10-31")
    d.bg(None, grain(W * n, H, 407).convert("RGBA"), name="Background")
    for k in range(n):
        d.put(k, "Logo", logo_disc(110), 40, 36, shadowed=False, anchor="tl")
    card(d, 0, frame("f51"), "The Times of India", TOI_CREDIT, "We made the Times of India",
         "46 people from 10 countries learned with us in Coimbatore.", TOI_SRC)
    photo_fact(d, 1, frame("f63"), "46 participants, 10 countries", "Farmers, soil scientists, microbiologists "
               "and consultants.")
    photo_fact(d, 2, frame("f45"), "The Save Soil model farm", "Ten days at Sadhguru's Save Soil Regenerative "
               "Revolution farm.")
    photo_fact(d, 3, frame("f69"), "Compost to microscope", "BioComplete™ compost, extracts, teas and soil "
               "sampling.")
    fact(d, 4, "Read the article", "The Times of India, 30 October 2026. In collaboration with Isha Outreach. "
         "Link in bio.")
    return d


def toi_c():
    n = 5
    d = Deck("toi20261031", n, "times-of-india-coimbatore-workshop-v3", "2026-10-31")
    d.bg(None, grain(W * n, H, 408).convert("RGBA"), name="Background")
    for k in range(n):
        d.put(k, "Logo", logo_disc(110), 40, 36, shadowed=False, anchor="tl")
    card(d, 0, frame("f81"), "The Times of India", TOI_CREDIT, "From 10 countries to one farm in Coimbatore",
         "Our India Accelerator Workshop, in the news.", TOI_SRC)
    fact(d, 1, "46 participants", "From seven Indian states, the Netherlands, Australia, Iran, the United States "
         "and Costa Rica.")
    fact(d, 2, "10 days on a working farm", "At Sadhguru's Save Soil Regenerative Revolution farm, in "
         "collaboration with Isha Outreach.")
    fact(d, 3, "61 at the seminar first", "The two-day Life in the Soil Seminar ran on 16 and 17 October.")
    fact(d, 4, "Read the article", "The Times of India, 30 October 2026. Link in bio.")
    return d


if __name__ == "__main__" and sys.argv[1:] == ["toi-options"]:
    for fn in (toi_b, toi_c):
        d = fn()
        print(d.save(TILES, DECKS)[0], d.pptx_name())
