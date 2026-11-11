import json, os, time, urllib.request, re
TOKEN = os.environ["PF"]; STORE = "19049727"
S = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/pf"
RAW = "https://raw.githubusercontent.com/linneamoritznyc/SFWassetlibrarycontentautomation/claude/zealous-shannon-g3u56z/apps/web/public/wormhole/merch/"
def api(path, body=None, method=None):
    req = urllib.request.Request("https://api.printful.com" + path, data=json.dumps(body).encode() if body else None,
                                 method=method, headers={"Authorization": "Bearer " + TOKEN, "X-PF-Store-Id": STORE,
                                                          "Content-Type": "application/json"})
    for _ in range(6):
        try:
            return json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as e:
            r = json.loads(e.read())
            if r.get("code") == 429:
                m = re.search(r"after (\d+) seconds", str(r.get("result"))); time.sleep((int(m.group(1)) if m else 60) + 3); continue
            return r
SIZES = ["S", "M", "L", "XL", "2XL", "One size"]
# name, product, colours->ink, placement, price, width frac, top frac, thumbnail
P = [
    ("Be the Mycelium Tee", 71, {"White": "green", "Forest": "light", "Sage": "green"}, "front", "32.00", 0.78, 0.04, "tee-8452-0.jpg"),
    ("Be the Mycelium Hoodie", 146, {"Forest Green": "light", "Sand": "green"}, "front", "55.00", 0.72, 0.02, "hoodie-20571-0.jpg"),
    ("Be the Mycelium Crewneck", 145, {"Forest Green": "light", "Sand": "green"}, "front", "48.00", 0.78, 0.04, "crewneck-18764-0.jpg"),
    ("Be the Mycelium Tote", 367, {"Oyster": "green"}, "front", "25.00", 0.86, 0.06, "tote-10458-0.jpg"),
    ("Be the Mycelium Mug", 19, None, "default", "18.00", None, None, "mug-1320-2.jpg"),
    ("Be the Mycelium Poster", 1, None, "default", "25.00", 1.0, 0.0, "poster-6239-0.jpg"),
    ("Be the Mycelium Sticker", 358, None, "default", "5.00", 1.0, 0.0, "sticker-10164-0.jpg"),
]
ONLY = {19: [1320], 1: [6239], 358: [10164]}
FILE = {19: "mycelium-green-ink.png", 1: "mycelium-poster-square.png", 358: "mycelium-sticker-circle.png"}
THUMB = "https://raw.githubusercontent.com/linneamoritznyc/SFWassetlibrarycontentautomation/claude/zealous-shannon-g3u56z/apps/web/public/wormhole/merch/mockups/"
existing = {p["name"] for p in api("/store/products?limit=100").get("result", [])}
for name, pid, cols, place, price, wf, tf, thumb in P:
    if name in existing:
        print("exists", name); continue
    pv = json.load(open(f"{S}/p{pid}.json"))["result"]["variants"]
    pfr = json.load(open(f"{S}/f{pid}.json"))["result"]
    pfs = {x["printfile_id"]: x for x in pfr["printfiles"]}
    sv = []
    if cols:
        vs = [(v["id"], cols[v["color"]]) for v in pv if v["color"] in cols and v["size"] in SIZES]
    else:
        vs = [(i, None) for i in ONLY[pid]]
    for vid, ink in vs:
        f = FILE.get(pid) or ("mycelium-light-ink.png" if ink == "light" else "mycelium-green-ink.png")
        vp = next(x for x in pfr["variant_printfiles"] if x["variant_id"] == vid)
        pf = pfs[vp["placements"][place]]
        AW, AH = pf["width"], pf["height"]
        if pid == 19:
            pos = dict(area_width=AW, area_height=AH, width=AH, height=AH, top=0, left=(AW - AH) // 2)
        elif pid in (1, 358):
            s = min(AW, AH); pos = dict(area_width=AW, area_height=AH, width=s, height=s, top=(AH - s) // 2, left=(AW - s) // 2)
        else:
            w = round(AW * wf); pos = dict(area_width=AW, area_height=AH, width=w, height=w, top=round(AH * tf), left=(AW - w) // 2)
        pos["limit_to_print_area"] = True
        sv.append({"variant_id": vid, "retail_price": price,
                   "files": [{"type": place, "url": RAW + f, "position": pos}]})
    body = {"sync_product": {"name": name, "thumbnail": THUMB + thumb}, "sync_variants": sv}
    r = api("/store/products", body)
    print(name, len(sv), "variants ->", r.get("code"), str(r.get("result"))[:200] if r.get("code") != 200 else r["result"]["id"])
    time.sleep(4)
