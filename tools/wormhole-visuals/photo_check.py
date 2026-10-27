"""One photo, one post: finds photos already used in Wormhole, even cropped or resized.

  WORMHOLE_PASSWORD=... python3 tools/wormhole-visuals/photo_check.py photo.jpg [more.jpg ...]
      -> for each photo, the live posts and slides that already show it
  WORMHOLE_PASSWORD=... python3 tools/wormhole-visuals/photo_check.py --dupes [--from 2026-11-01]
      -> pairs of different posts that share a photo

Downloads every live slide image once into out/photo-cache, then matches ORB features
(RANSAC homography inliers), so a crop, a resize or a coloured box over part of the photo
still matches. Needs opencv-python-headless.
"""
import argparse
import http.cookiejar
import json
import os
import urllib.request

import cv2
import numpy as np

BASE = "https://wormholelinnea.vercel.app"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "photo-cache")
MIN_INLIERS = 40
orb = cv2.ORB_create(1500)
bf = cv2.BFMatcher(cv2.NORM_HAMMING)


def posts():
    jar = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    body = json.dumps({"password": os.environ["WORMHOLE_PASSWORD"], "name": "photo check"}).encode()
    op.open(urllib.request.Request(BASE + "/api/wormhole/login", body, {"content-type": "application/json"}))
    return json.load(op.open(BASE + "/api/wormhole/posts"))["posts"]


def features(path):
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if im is None:
        return None
    s = 700 / max(im.shape)
    im = cv2.resize(im, None, fx=s, fy=s) if s < 1 else im
    return orb.detectAndCompute(im, None)


def inliers(a, b):
    (ka, da), (kb, db) = a, b
    if da is None or db is None or len(ka) < 10 or len(kb) < 10:
        return 0
    good = [m for m, n in (p for p in bf.knnMatch(da, db, k=2) if len(p) == 2) if m.distance < 0.75 * n.distance]
    if len(good) < 12:
        return 0
    src = np.float32([ka[m.queryIdx].pt for m in good])
    dst = np.float32([kb[m.trainIdx].pt for m in good])
    _, mask = cv2.findHomography(src, dst, cv2.RANSAC, 6.0)
    return int(mask.sum()) if mask is not None else 0


def index(start=""):
    os.makedirs(CACHE, exist_ok=True)
    out = []
    for p in posts():
        if p["iso_date"] < start:
            continue
        for i, s in enumerate(p["slides"]):
            if not s.get("image"):
                continue
            fn = os.path.join(CACHE, s["image"].strip("/").replace("/", "_"))
            if not os.path.exists(fn):
                try:
                    urllib.request.urlretrieve(BASE + s["image"], fn)
                except Exception:
                    continue
            f = features(fn)
            if f is not None:
                out.append((p["id"], i + 1, s["image"], f))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photos", nargs="*")
    ap.add_argument("--dupes", action="store_true")
    ap.add_argument("--from", dest="start", default="")
    a = ap.parse_args()
    idx = index(a.start)
    if a.dupes:
        seen = set()
        for i in range(len(idx)):
            for j in range(i + 1, len(idx)):
                if idx[i][0] == idx[j][0]:
                    continue
                n = inliers(idx[i][3], idx[j][3])
                if n >= MIN_INLIERS and (idx[i][0], idx[j][0]) not in seen:
                    seen.add((idx[i][0], idx[j][0]))
                    print(f"{idx[i][0]} slide {idx[i][1]}  =  {idx[j][0]} slide {idx[j][1]}  ({n})")
        return
    for ph in a.photos:
        f = features(ph)
        hits = [(pid, k, n) for pid, k, _, g in idx if (n := inliers(f, g)) >= MIN_INLIERS]
        print(ph, "->", ", ".join(f"{pid} slide {k} ({n})" for pid, k, n in hits) or "unused")


if __name__ == "__main__":
    main()
