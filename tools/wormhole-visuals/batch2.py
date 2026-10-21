"""22 to 26 October in the earthworm-cover style: d27, p10, p11, p12, p13, p14.

  python3 tools/wormhole-visuals/batch2.py [ids...]
"""
import sys

from PIL import Image

from collage import GREEN, H, W, flower, lens, phone, print_photo, round_photo, soil
from mentors import CORAL, PEACH, SAGE, SKY, SUN, headline, line, scene
from p08_earthworm import DEEP, SOIL_TOP, logo_full
from posts import MICRO, N, build, post

PAST = "/home/user/photos/past-workshop-images"
PICKS = "/home/user/photos/past-workshop-picks/img"
SHOTS = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/site"
PHOTO = "/home/user/SFW-SocialMedia/assets/photo"
AUTUMN = [(0, "#F2B27A"), (0.35, "#F7CFA2"), (0.6, "#FAE2C6"), (1, "#F1D6B4")]
LAVENDER = [(0, "#CDBFE0"), (0.35, "#E0D6EC"), (0.6, "#EFE9F5"), (1, "#E4DDEE")]


def split(t):
    head, _, rest = t.partition(": ")
    return (head + ".", rest) if rest else (t, "")


@post("d27", "2026-10-22", "smell-is-a-lab-result", 7)
def d27(d):
    scene(d, 7, SAGE, [("clover", 140), ("norfolk-cornflower", 180), ("clover", 150), ("tamil-nadu-marigold", 170)], 27)
    texts = [
        ("Smell is a lab result.", "What your compost pile is telling you."),
        ("Ammonia.", "Nitrogen is leaving the pile as gas. Too much nitrogen, or pH too high."),
        ("Rotten eggs.", "Hydrogen sulfide from sulfate-reducing bacteria. Zero oxygen."),
        ("Vinegar or vomit.", "Acetic and butyric acid, fermentation products. Both are toxic to roots."),
        ("Earthy.", "Geosmin from actinomycetes. An aerobic pile."),
        ("Under the microscope, ciliates confirm it.", "They indicate anaerobic conditions."),
        ("The fix: structure and oxygen.", "Keep the pile at 55 to 68°C and turn it when it goes above 68°C."),
    ]
    for k, (h, l) in enumerate(texts):
        headline(d, k, h, size=104 if len(h) < 24 else 80)
        line(d, k, l, size=42)
    d.put(0, "compost-pile", soil("compost-white-fungal-threads", w=420), 760, SOIL_TOP - 90)
    d.put(1, "dark-soil", soil("dark-soil-clump", w=300), 780, SOIL_TOP - 60)
    d.put(2, "earthworm", soil("earthworm", h=260), 700, 1110, rot=30)
    d.put(3, "dry-leaves", soil("dry-leaves-twigs", w=280), 780, SOIL_TOP - 60)
    d.put(4, "moss", soil("moss-clump", w=300), 780, SOIL_TOP - 60)
    d.put(5, "micrograph-ciliate", lens(N("Ciliate, 60x obj, Patricia J Coppola.jpg"), 360), 790, 1060)
    d.put(6, "wood-chips", soil("wood-chips-pile", w=300), 780, SOIL_TOP - 60)


@post("p10", "2026-10-22", "christina-olivero", 4)
def p10(d):
    scene(d, 4, PEACH, [("clover", 150), ("norfolk-cornflower", 180), ("santa-fe-globemallow", 200), ("clover", 140)], 10)
    line(d, 0, "Soil Regenerators in the wild", 150, size=44)
    headline(d, 0, "From advertising to a soil business.", size=100, y=210, w=760)
    headline(d, 1, "Christina Olivero, Alter Eco Farms, Chattanooga.", size=88)
    d.put(1, "dark-soil", soil("dark-soil-clump", w=300), 780, SOIL_TOP - 60)
    headline(d, 2, "It started with one free webinar on protozoa.", size=88)
    d.put(2, "micrograph-amoeba", lens(N("Naked amoeba (stellate), flagellate, 40x obj, Jimena Fuentes.jpg"), 360), 790, 1060)
    headline(d, 3, "Today she runs workshops, sells biological amendments and runs soil tests.", size=74)
    d.put(3, "compost", soil("compost-white-fungal-threads", w=300), 780, SOIL_TOP - 60)
    d.notes.append("add photo of Christina Olivero")


@post("p11", "2026-10-23", "our-new-website-is-live", 6)
def p11(d):
    scene(d, 6, SKY, [("clover", 150), ("norfolk-common-poppy", 200), ("clover", 140), ("tamil-nadu-marigold", 170)], 11)
    texts = ["Our new home is live!", "Every course, in one learning path.", "Every workshop, past and upcoming.",
             "Find a soil consultant near you.", "Dr. Elaine's papers in one library.", "soilfoodweb.com"]
    shots = ["home-1-top.png", "programs-overview-1-top.png", "workshops-1-top.png", "find-a-professional-1-top.png",
             "publications-1-top.png", "home-2-section.png"]
    for k, (t, s) in enumerate(zip(texts, shots)):
        headline(d, k, t, size=96 if k in (0, 5) else 84, w=620)
        ph = phone(f"{SHOTS}/{s}", w=330)
        d.put(k, "phone-screenshot", ph, 820, SOIL_TOP + 120 - ph.height // 2 + 40, off=(12, 14))


@post("p12", "2026-10-24", "leave-the-leaves", 6)
def p12(d):
    scene(d, 6, AUTUMN, [("clover", 140), ("tamil-nadu-marigold", 180), ("santa-fe-chamisa", 190), ("clover", 150)], 12)
    texts = ["Myth: fall leaves need to be cleaned up.", "Leaf litter is rich in carbon and lignin.",
             "Fungi are the main decomposers of lignin.", "That feeds the fungal soils trees and shrubs prefer.",
             "A litter layer shields the soil over winter.", "On lawns, shred the leaves and move them to your beds."]
    for k, t in enumerate(texts):
        headline(d, k, t, size=84)
        for j, (x, r) in enumerate([(260, -12), (560, 8), (840, -4)][: 1 + k % 3]):
            d.put(k, f"leaves-{j + 1}", soil("dry-leaves-twigs", w=230), x, SOIL_TOP - 40, rot=r)
    d.put(2, "micrograph-fungal-hypha", lens(N("Fungal hypha, 100x obj, Marco Trevisan.jpg"), 330), 790, 1080)
    d.put(3, "mushrooms", soil("mushrooms", w=240), 760, 1150)


@post("p13", "2026-10-25", "dr-elaine-flowers-in-our-logo", 3)
def p13(d):
    # Memorial content: purple is allowed here.
    scene(d, 3, LAVENDER, [("clover", 150), ("norfolk-sea-lavender", 200), ("clover", 140), ("norfolk-foxglove", 230)], 13)
    headline(d, 0, "Look closely at our new logo.", size=100, w=620)
    big = Image.open("/home/user/sfwlib/img/sfwlogo-240.png").convert("RGBA").resize((420, 364), Image.LANCZOS)
    d.put(0, "logo-big", big, 780, 560, off=(6, 8), blur=8, alpha=0.25)
    headline(d, 1, "Purple flowers, in honor of Dr. Elaine Ingham.", size=84, w=620)
    line(d, 1, "Purple was her favorite color.", size=44)
    d.put(1, "photo-elaine", round_photo(f"{PHOTO}/elaine-flower-shirt-microscope.png", 360, ring=14, fy=0.3), 820, 1050)
    headline(d, 2, "soilfoodweb.com", size=100)
    line(d, 2, "See it on our new website. Link in bio.", size=44)


@post("p14", "2026-10-26", "costa-rica-where-it-began", 5)
def p14(d):
    scene(d, 5, SUN, [("costa-rica-hibiscus", 160), ("clover", 140), ("costa-rica-heliconia", 220), ("costa-rica-torch-ginger", 190)], 14)
    a = f"{PAST}/accelerator-workshop-august-2023/accelerator-workshop-august-2023-"
    headline(d, 0, "Where it began.", size=110)
    line(d, 0, "Costa Rica, August 2023", size=44)
    d.put(0, "photo-high-five", print_photo(f"{PICKS}/accelerator-workshop-august-2023-card.jpg", 520, 390), 640, 610)
    for k, f in ((1, "03-laughing-at-compost-cage"), (2, "04-students-holding-buckets"), (3, "01-graduates-with-certificates")):
        d.put(k, "photo", print_photo(f"{a}{f}.jpg", 880, 600), W // 2, 470, rot=0)
    headline(d, 4, "Accelerator Workshop, Costa Rica", size=88)
    line(d, 4, "18 to 29 January 2027. Join the interest list, link in bio.", size=44)


if __name__ == "__main__":
    for pid in sys.argv[1:] or ["d27", "p10", "p11", "p12", "p13", "p14"]:
        build(pid)
        print(pid, "built")
