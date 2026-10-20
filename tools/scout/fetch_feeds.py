"""Scout, step 1: read every feed in packages/shared/src/feeds.ts and list fresh stories.

  python3 tools/scout/fetch_feeds.py [--days 10]
    -> tools/scout/out/candidates.json  (newest first, one entry per story)
    -> tools/scout/out/feed-health.json (which feeds answered, which failed)

No API key and no database: a Claude Code session reads candidates.json, picks
and writes the posts (see tools/scout/RUN.md).
"""
import argparse
import email.utils
import html
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
UA = "SFWContentStudio/0.1 (+https://soilfoodweb.com)"


def feeds():
    src = open(os.path.join(REPO, "packages", "shared", "src", "feeds.ts")).read()
    out = []
    for block in re.findall(r"\{[^{}]*?url:\s*'[^']+'[^{}]*?\}", src, re.S):
        get = lambda k: (re.search(rf"{k}:\s*'([^']*)'", block) or [None, None])[1]
        out.append(dict(name=get("name"), url=get("url"), kind=get("kind") or "rss", region=get("region")))
    return out


def text(el):
    if el is None:
        return ""
    t = "".join(el.itertext()) if len(el) else (el.text or "")
    t = re.sub(r"<[^>]+>", " ", html.unescape(t))
    return re.sub(r"\s+", " ", t).strip()


def when(s):
    if not s:
        return None
    try:
        return email.utils.parsedate_to_datetime(s).astimezone(timezone.utc)
    except Exception:
        pass
    try:
        return datetime.fromisoformat(s.strip().replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def parse(xml):
    root = ET.fromstring(xml)
    items = []
    for it in root.iter():
        tag = it.tag.split("}")[-1]
        if tag not in ("item", "entry"):
            continue
        f = {c.tag.split("}")[-1]: c for c in it}
        link = f.get("link")
        url = (link.get("href") if link is not None and link.get("href") else text(link)) if link is not None else ""
        date = when(text(f.get("pubDate")) or text(f.get("published")) or text(f.get("updated")) or text(f.get("date")))
        summary = text(f.get("description")) or text(f.get("summary")) or text(f.get("content"))
        items.append(dict(title=text(f.get("title")), url=url.strip(), published=date.isoformat() if date else None,
                          summary=summary[:900]))
    return items


def fetch(feed):
    try:
        req = urllib.request.Request(feed["url"], headers={
            "user-agent": UA,
            "accept": "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.5"})
        with urllib.request.urlopen(req, timeout=25) as r:
            items = parse(r.read())
        return feed, items, None if items else "answered, but no items could be parsed"
    except Exception as e:
        return feed, [], str(e)[:200]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=10)
    a = ap.parse_args()
    cutoff = datetime.now(timezone.utc) - timedelta(days=a.days)
    os.makedirs(OUT, exist_ok=True)
    rss = [f for f in feeds() if f["kind"] == "rss"]
    seen, cands, health = set(), [], []
    with ThreadPoolExecutor(8) as ex:
        for feed, items, err in ex.map(fetch, rss):
            fresh = 0
            for it in items:
                if not it["url"] or it["url"] in seen:
                    continue
                if it["published"] and datetime.fromisoformat(it["published"]) < cutoff:
                    continue
                seen.add(it["url"])
                cands.append(dict(feed=feed["name"], region=feed["region"], **it))
                fresh += 1
            health.append(dict(feed=feed["name"], url=feed["url"], ok=err is None, error=err, items=len(items), fresh=fresh))
    cands.sort(key=lambda c: c["published"] or "", reverse=True)
    json.dump(cands, open(os.path.join(OUT, "candidates.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(health, open(os.path.join(OUT, "feed-health.json"), "w"), indent=1)
    ok = sum(h["ok"] for h in health)
    print(f"{ok}/{len(health)} feeds answered, {len(cands)} stories from the last {a.days} days")
    for h in health:
        if not h["ok"]:
            print("  failed:", h["feed"], "-", h["error"])


if __name__ == "__main__":
    main()
