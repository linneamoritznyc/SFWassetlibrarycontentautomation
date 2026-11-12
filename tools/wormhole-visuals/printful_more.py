import json, os, re, time, urllib.request
TOKEN = os.environ["PF"]; STORE = "19049727"
RAW = "https://raw.githubusercontent.com/linneamoritznyc/SFWassetlibrarycontentautomation/claude/zealous-shannon-g3u56z/apps/web/public/wormhole/merch/"
OUT = "/home/user/sfwlib/social/merch/printful"
def api(path, body=None):
    for _ in range(8):
        req = urllib.request.Request("https://api.printful.com" + path, data=json.dumps(body).encode() if body else None,
              headers={"Authorization": "Bearer " + TOKEN, "X-PF-Store-Id": STORE, "Content-Type": "application/json"})
        try:
            return json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as e:
            r = json.loads(e.read())
            if r.get("code") == 429:
                m = re.search(r"after (\d+) seconds", str(r.get("result"))); time.sleep((int(m.group(1)) if m else 60) + 3); continue
            return r
def full(w, h):
    return dict(area_width=w, area_height=h, width=w, height=h, top=0, left=0, limit_to_print_area=True)
PHONES = [17714, 17716, 17718, 17720, 20302, 20303, 20304, 20305, 33985, 33986, 33987, 33988]
P = [
 ("Be the Mycelium Water Bottle", 382, [10798], "default", "mycelium-bottle-wrap.png", full(2557, 1582), "30.00"),
 ("Be the Mycelium Journal", 867, [22658], "front", "mycelium-journal-cover-front.png", full(4065, 2850), "22.00"),
 ("Be the Mycelium Phone Case", 601, PHONES, "default", "mycelium-phone-case.png", full(1392, 2220), "28.00"),
 ("Be the Mycelium Framed Poster", 795, [20256, 20258], "default", "mycelium-poster-12x16.png", dict(area_width=3600, area_height=4800, width=3600, height=4800, top=0, left=0), "65.00"),
 ("Be the Mycelium Cotton Tote (Natural)", 1553, [49323], "front_dtf_tote", "mycelium-tote-natural.png", full(1425, 1425), "27.00"),
 ("Be the Mycelium Cotton Tote (Green)", 1553, [49314], "front_dtf_tote", "mycelium-tote-green.png", full(1425, 1425), "27.00"),
]
existing = {p["name"] for p in api("/store/products?limit=100").get("result", [])}
for name, pid, vids, place, f, pos, price in [x for x in P if "Journal" in x[0]]:
    files = [{"type": place, "url": RAW + f + "?v=2", **({"position": pos} if pos else {})}]
    if name not in existing:
        sv = [{"variant_id": v, "retail_price": price, "files": files} for v in vids]
        r = api("/store/products", {"sync_product": {"name": name}, "sync_variants": sv})
        print(name, r.get("code"), r["result"]["id"] if r.get("code") == 200 else str(r.get("result"))[:200])
    # mockup for review
    mf = [{"placement": place, "image_url": RAW + f + "?v=2", **({"position": {k: v for k, v in pos.items() if k != "limit_to_print_area"}} if pos else {})}]
    body = {"variant_ids": vids[:1] if pid != 1553 else vids, "format": "jpg", "files": mf}
    if pid == 1553:
        body["technique"] = "DTFILM"
    r = api(f"/mockup-generator/create-task/{pid}?store_id={STORE}", body)
    if not isinstance(r.get("result"), dict):
        print(" mockup fail", str(r)[:200]); continue
    key = r["result"]["task_key"]
    for _ in range(60):
        time.sleep(5)
        t = api(f"/mockup-generator/task?task_key={key}&store_id={STORE}")["result"]
        if t["status"] != "pending":
            break
    if t["status"] == "completed":
        u = t["mockups"][0]["mockup_url"]
        fn = f"{OUT}/{name.split('Mycelium ')[1].lower().replace(' ', '-').replace('(', '').replace(')', '')}.jpg"
        urllib.request.urlretrieve(u, fn); print(" mockup", fn)
    else:
        print(" mockup", t["status"], str(t)[:200])
    time.sleep(12)
