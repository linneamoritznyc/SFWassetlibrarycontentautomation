"""Checks the Instagram grid against docs/feed-guide.md.

  WORMHOLE_PASSWORD=... python3 tools/wormhole-visuals/grid_check.py [--from 2026-11-01] [--to 2026-12-31]

Reads the live posts, keeps what shows in the Instagram grid (dated feed posts and
Reels; no Stories, no LinkedIn-only posts), reads each post's family from the start
of its visual note ("Family: B, big number."), and prints the feed in order with
every break of the variety rules:

  - neighbours share a family
  - a family more than twice in any 6 posts in a row
  - fewer than 5 families in any 9 posts in a row
  - posts with no family written yet
"""
import argparse
import http.cookiejar
import json
import os
import re
import urllib.request

BASE = "https://wormholelinnea.vercel.app"
FAMILIES = {
    "A": "brand boxes", "B": "big number", "C": "article repost card", "D": "full-bleed photo",
    "E": "botanical", "F": "specimen", "G": "type only", "H": "diagram", "I": "portrait",
    "J": "numbered steps", "K": "framed photo", "L": "photo grid", "M": "event card", "N": "field notebook",
}


def posts():
    jar = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    body = json.dumps({"password": os.environ["WORMHOLE_PASSWORD"], "name": "grid check"}).encode()
    op.open(urllib.request.Request(BASE + "/api/wormhole/login", body, {"content-type": "application/json"}))
    return json.load(op.open(BASE + "/api/wormhole/posts"))["posts"]


def in_grid(p):
    plat = p["platform"]
    story = "stories" in plat.lower() or re.search(r"\bstory\b", p["topic"], re.I)
    return not p["date_tbd"] and not story and (not plat.strip() or "instagram" in plat.lower())


def family(p):
    m = re.match(r"\s*Family:\s*([A-Z])\b", p.get("visual_note") or "")
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="")
    ap.add_argument("--to", dest="end", default="9999")
    a = ap.parse_args()
    feed = sorted((p for p in posts() if in_grid(p)), key=lambda p: (p["iso_date"], p["id"]))
    feed = [p for p in feed if a.start <= p["iso_date"] <= a.end]
    fam = [family(p) for p in feed]
    problems = []
    for i, p in enumerate(feed):
        if not fam[i]:
            problems.append(f"{p['id']} ({p['iso_date']}): no family in the visual note")
        if i and fam[i] and fam[i] == fam[i - 1]:
            problems.append(f"{feed[i - 1]['id']} and {p['id']}: neighbours share family {fam[i]}")
    for i in range(len(feed) - 5):
        win = [f for f in fam[i:i + 6] if f]
        for f in set(win):
            if win.count(f) > 2:
                problems.append(f"{feed[i]['id']} to {feed[i + 5]['id']}: family {f} {win.count(f)} times in 6 posts")
    for i in range(len(feed) - 8):
        win = {f for f in fam[i:i + 9] if f}
        if all(fam[i:i + 9]) and len(win) < 5:
            problems.append(f"{feed[i]['id']} to {feed[i + 8]['id']}: only {len(win)} families in 9 posts")
    for p, f in zip(feed, fam):
        print(f"{p['iso_date']}  {f or '?'}  {FAMILIES.get(f, 'no family yet'):20}  {p['id']:14}  {p['topic'][:60]}")
    print()
    print("\n".join(dict.fromkeys(problems)) or "No breaks of the variety rules.")


if __name__ == "__main__":
    main()
