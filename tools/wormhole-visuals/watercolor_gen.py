"""Watercolor illustrations from Replicate (FLUX 1.1 Pro), cached by name.

  python3 tools/wormhole-visuals/watercolor_gen.py [names...]   (all when none given)
    -> /home/user/wc/gen/<name>.png

Needs REPLICATE_API_TOKEN. Every prompt starts with the house prefix; no text in images.
Re-running a name that already has a file does nothing; delete the file to remake it.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

OUT = os.environ.get("WC_GEN", "/home/user/wc/gen")
PREFIX = ("Loose hand-painted watercolor illustration on white watercolor paper, soft muted earthy colours, "
          "thin grey ink outlines, educational science-book style, plain white background, no text.")
MODEL = "black-forest-labs/flux-1.1-pro"

PROMPTS = {
    # p11 Our new website is live
    "laptop-seedling": ("An open laptop seen from the front and slightly above, the screen is completely empty and plain white with nothing on it. "
                        "On the keyboard, in front of the screen, a small green seedling with two leaves grows out of a little mound of soil between the keys.", "4:5"),
    "spot-seedling": ("A small seedling sprouting from a little pile of dark crumbly soil.", "1:1"),
    "spot-globe": ("A small globe on a stand with a few green leaves growing around its base.", "1:1"),
    "spot-papers": ("A neat stack of old scientific papers tied with string, a small brass microscope beside it.", "1:1"),
    # p12 Leave the leaves
    "leaf-cutaway": ("Cross-section cut-away of the ground in autumn: a thick layer of fallen brown, orange and yellow leaves "
                     "on top of dark soil, fine white fungal threads spreading through the soil just under the leaves, an "
                     "earthworm pulling a leaf down into its burrow, a ladybird and a small beetle tucked under the leaves, "
                     "plant roots below. The cut-away block has clean edges on all sides.", "4:5"),
    "mower-leaves": ("A small red push lawn mower on a green lawn shredding fallen autumn leaves, the shredded leaves spread "
                     "as a mulch layer on a neighbouring vegetable garden bed with kale.", "4:5"),
    # p13 Dr. Elaine's flowers in our new logo
    "purple-vine": ("A botanical study of a slender green vine with round green leaves and small purple fan-shaped flowers.", "1:1"),
    "purple-sprig": ("A botanical study of a single small purple flower with a green stem, two leaves and a closed bud.", "1:1"),
    "purple-flower-open": ("A botanical study of one small purple flower seen from the front, petals spread like a fan, "
                           "with a short green stem.", "1:1"),
    # p05 What can I do right now to improve my soil?
    "bed-cutaway": ("Cut-away of a garden bed: straw mulch on top, small green seedlings, their roots going down into dark "
                    "soil, fine white fungal threads between the roots, an earthworm in the soil. Clean edges on all sides.", "4:5"),
    "cover-soil": ("A wide cut-away strip of garden soil divided into three clear sections from left to right: on the left a thick layer of "
                   "golden straw mulch, in the middle short green clover plants with round trefoil leaves, on the right a pile of fallen "
                   "brown and orange autumn leaves. Dark soil underneath all three. Nothing else, no table, no paper, no frame.", "4:5"),
    "compost-hand": ("A cupped hand holding dark crumbly compost, and next to it a round magnified circle like a microscope "
                     "view showing tiny rod-shaped bacteria, thin fungal hyphae threads, a round protozoan and a "
                     "nematode worm.", "4:5"),
    "spade-fungi": ("A garden spade pushed into the soil, a network of fine white fungal threads in the soil torn apart where "
                    "the blade cuts through, cut-away view of the soil.", "4:5"),
    "woodchips-fungi": ("A pile of wood chips on top of the soil with fine white fungal threads spreading down from the wood "
                        "chips into the dark soil below, cut-away view.", "4:5"),
    "hands-seedling": ("Two different people's hands, one coming from the left and one from the right, passing a small seedling with its ball of soil "
                       "from one pair of hands to the other.", "4:5"),
    # p14 Costa Rica
    "heliconia": ("A hanging heliconia (lobster claw) flower: a long zigzag chain of red bracts with yellow tips and green edges, "
                  "hanging down from a green stem, with one long paddle-shaped banana-like leaf. Painted directly on the white page, "
                  "no paper sheet, no card, no frame, no shadow.", "4:5"),
    "torch-ginger": ("A torch ginger flower (Etlingera elatior): a tall straight green stem topped by a large waxy pink cone-shaped flower head "
                     "made of many layered pink bracts, like a torch.", "4:5"),
    "banana-leaves": ("Two long green banana plant leaves, long and paddle shaped with a strong central rib, edges slightly torn in strips, no holes, "
                      "crossing each other.", "1:1"),
}


def run(name):
    path = os.path.join(OUT, f"{name}.png")
    if os.path.exists(path):
        return name, "cached"
    text, ratio = PROMPTS[name]
    body = json.dumps({"input": {"prompt": f"{PREFIX} {text}", "aspect_ratio": ratio, "output_format": "png",
                                 "safety_tolerance": 2, "prompt_upsampling": False}}).encode()
    req = urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=body, headers={
        "Authorization": f"Bearer {os.environ['REPLICATE_API_TOKEN']}", "Content-Type": "application/json",
        "Prefer": "wait"})
    for attempt in range(12):
        try:
            pred = json.load(urllib.request.urlopen(req, timeout=120))
            break
        except urllib.error.HTTPError as e:  # this account is rate-limited: wait and retry
            if e.code != 429 or attempt == 11:
                raise
            time.sleep(12)
    while pred.get("status") not in ("succeeded", "failed", "canceled"):
        time.sleep(2)
        pred = json.load(urllib.request.urlopen(urllib.request.Request(pred["urls"]["get"], headers={
            "Authorization": f"Bearer {os.environ['REPLICATE_API_TOKEN']}"}), timeout=60))
    if pred["status"] != "succeeded":
        return name, f"failed: {pred.get('error')}"
    url = pred["output"] if isinstance(pred["output"], str) else pred["output"][0]
    urllib.request.urlretrieve(url, path)
    return name, "ok"


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(PROMPTS)
    with ThreadPoolExecutor(1) as ex:
        for name, status in ex.map(run, names):
            print(name, status)
