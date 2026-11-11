import json, os, sys, time, urllib.request
TOKEN = os.environ["PF"]; STORE = "19049727"
S = "/tmp/claude-0/-home-user/aa85d233-831d-5e12-bf14-2ae561c4274c/scratchpad/pf"
OUT = "/home/user/sfwlib/social/merch/printful"
RAW = "https://raw.githubusercontent.com/linneamoritznyc/SFWassetlibrarycontentautomation/claude/zealous-shannon-g3u56z/apps/web/public/wormhole/merch/"
def api(path, body=None):
    req = urllib.request.Request("https://api.printful.com" + path, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": "Bearer " + TOKEN, "X-PF-Store-Id": STORE,
                                          "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        return json.loads(e.read())
# (name, product, variants, file, placement, width fraction, top fraction)
JOBS = [
    ("tee", 71, [4012, 8452, 22051], None, "front", 0.78, 0.04),
    ("hoodie", 146, [20571, 12998], None, "front", 0.72, 0.02),
    ("crewneck", 145, [16877, 18764], None, "front", 0.78, 0.04),
    ("tote", 367, [10458], "mycelium-green-ink.png", "front", 0.86, 0.06),
    ("mug", 19, [1320], "mycelium-green-ink.png", "default", None, None),
    ("poster", 1, [6239], "mycelium-poster-square.png", "default", 1.0, 0.0),
    ("sticker", 358, [10164], "mycelium-sticker-circle.png", "default", 1.0, 0.0),
]
INK = {4012: "green", 8452: "light", 22051: "green", 20571: "light", 12998: "green", 16877: "green", 18764: "light"}
only = sys.argv[1:]
for name, pid, variants, file, place, wf, tf in JOBS:
    if only and name not in only:
        continue
    pfr = json.load(open(f"{S}/f{pid}.json"))["result"]
    pfs = {x["printfile_id"]: x for x in pfr["printfiles"]}
    groups = {}
    for v in variants:
        f = file or ("mycelium-light-ink.png" if INK[v] == "light" else "mycelium-green-ink.png")
        groups.setdefault(f, []).append(v)
    for f, vs in groups.items():
        vp = next(x for x in pfr["variant_printfiles"] if x["variant_id"] == vs[0])
        pf = pfs[vp["placements"][place]]
        AW, AH = pf["width"], pf["height"]
        if name == "mug":
            h = AH; w = h; pos = dict(area_width=AW, area_height=AH, width=w, height=h, top=0, left=(AW - w) // 2)
        elif name in ("poster", "sticker"):
            s = min(AW, AH); pos = dict(area_width=AW, area_height=AH, width=s, height=s, top=(AH - s) // 2, left=(AW - s) // 2)
        else:
            w = round(AW * wf); pos = dict(area_width=AW, area_height=AH, width=w, height=w, top=round(AH * tf), left=(AW - w) // 2)
        body = {"variant_ids": vs, "format": "jpg", "files": [{"placement": place, "image_url": RAW + f, "position": pos}]}
        import re
        for _try in range(8):
            r = api(f"/mockup-generator/create-task/{pid}?store_id={STORE}", body)
            if r.get("code") == 429:
                m = re.search(r"after (\d+) seconds", str(r.get("result")))
                time.sleep((int(m.group(1)) if m else 60) + 3)
                continue
            break
        if "result" not in r or not isinstance(r["result"], dict):
            print(name, "create failed", str(r)[:300]); continue
        key = r["result"]["task_key"]
        for _ in range(60):
            time.sleep(5)
            t = api(f"/mockup-generator/task?task_key={key}&store_id={STORE}")["result"]
            if t["status"] != "pending":
                break
        if t["status"] != "completed":
            print(name, t["status"], str(t)[:300]); continue
        for i, m in enumerate(t["mockups"]):
            urls = [m["mockup_url"]] + [x["url"] for x in m.get("extra", [])][:3]
            for j, u in enumerate(urls):
                fn = f"{OUT}/{name}-{'-'.join(map(str, m['variant_ids']))}-{j}.jpg"
                urllib.request.urlretrieve(u, fn)
                print("saved", fn, m.get("placement"), m["variant_ids"])
        time.sleep(15)
