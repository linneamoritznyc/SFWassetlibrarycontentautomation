"""Write apps/web/lib/wormhole-designs.json: designed slides, real Instagram tiles, and the
Instagram posts that are not in the database yet. Wormhole shows these on load (lib/wormhole-designs.ts).
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
m = json.load(open(os.path.join(HERE, "out", "manifest.json")))
designs = {pid: [dict(text=t, image=i) for t, i in zip(e["texts"], e["slides"])] for pid, e in m.items()}
UNKNOWN = "Date unknown, posted. Image cropped from the profile screenshot of 18 October 2026."
# posted posts already in the database: their real tile becomes slide 1
posted = {"p01": "p01", "d09": "d09", "d08": "d08", "d07": "d07", "d04": "d04", "d03": "d03", "d01": "d01"}
virtual = []
def v(id, iso, topic, img, pinned=None, note=UNKNOWN, reel=False):
    virtual.append(dict(id=id, iso_date=iso, date_tbd=False, topic=topic, platform="Instagram", caption="",
                        slides=[dict(text="", image=f"/wormhole/ig/{img}.jpg")], cta="", link="", sources=[],
                        visual_note="Reel" if reel else "", note=note, status="scheduled", pinned=pinned))
v("ig-pin1", "2026-09-01", "Pinned: New York Times, Elaine Ingham, who taught that soil is alive", "pin1-nyt", 1)
v("ig-pin2", "2026-09-01", "Pinned: drawn portrait of Dr. Elaine Ingham", "pin2-portrait", 2)
v("ig-pin3", "2026-09-01", "Pinned: The Soil Foodweb, Dr. Elaine in a field", "pin3-soil-foodweb", 3)
v("d04a", "2026-10-07", "Hyderabad panel: Voices of Regeneration poster", "d04a", note="Posted 7 October 2026 next to d04 (Tangy illustration).")
v("ig-wild-ones", "2026-10-02", "Wild Ones repost: Our soil is living infrastructure", "ig-wild-ones")
for i, (img, topic, reel) in enumerate([
    ("ig-pov-reel", "POV: you're scrolling through your phone (Reel)", True),
    ("ig-blue-reel", "Blue Reel with leaf line drawings", True),
    ("ig-soil-reel", "Soil close-up (Reel)", True),
    ("ig-green-reel", "Green Reel with vegetable line drawings", True),
    ("ig-brown-reel", "Brown Reel with flower line drawings", True),
    ("ig-sifting-reel", "Man sifting compost (Reel)", True),
    ("ig-woman-chin", "Woman in a white shirt, chin on her hand", False),
    ("ig-leaves", "White tile with leaf drawings", False),
    ("ig-house-drawing", "Line drawing of a house and garden", False),
    ("ig-woman-dog", "Woman in a garden with a white dog", False),
    ("ig-webinar-series", "Webinar Series: Designing the Regeneration, Rewilding & Restoring", False),
    ("ig-geoff-lawton", "Geoff Lawton, live now, discussing permaculture design", False),
    ("ig-black-reel", "Black Reel", True)]):
    v(img, f"2026-09-{30 - i:02d}", topic, img, reel=reel)
out = dict(designs=designs, posted={k: f"/wormhole/ig/{f}.jpg" for k, f in posted.items()}, virtual=virtual)
json.dump(out, open(os.path.join(REPO, "apps", "web", "lib", "wormhole-designs.json"), "w"), indent=1, ensure_ascii=False)
print(len(designs), "designed,", len(virtual), "virtual")
