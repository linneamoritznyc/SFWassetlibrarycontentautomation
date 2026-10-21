"""Append "new slides" entries for built posts to apps/web/lib/wormhole-changes.ts.

  python3 tools/wormhole-visuals/add_slide_changes.py <date-key> <id> [id...]

Wormhole applies each entry once, on the next load, through the normal edit path.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TS = os.path.join(REPO, "apps", "web", "lib", "wormhole-changes.ts")

day, ids = sys.argv[1], sys.argv[2:]
m = json.load(open(os.path.join(HERE, "out", "manifest.json")))
src = open(TS).read()
entries = []
for pid in ids:
    e = m[pid]
    key = f"{day} {pid} slides"
    if f"'{key}'" in src:
        continue
    slides = [dict(text=t, image=i) for t, i in zip(e["texts"], e["slides"])]
    entries.append(
        "  {\n"
        f"    key: '{key}',\n"
        f"    post: '{pid}',\n"
        f"    set: {{ slides: {json.dumps(slides, ensure_ascii=False)} }},\n"
        f"    reason: {json.dumps('New slides (' + day + ') in the earthworm-cover style. Deck: ' + e['pptx'] + '.', ensure_ascii=False)},\n"
        "  },\n"
    )
marker = "];\n\nconst editorOf"
src = src.replace(marker, "".join(entries) + marker, 1)
open(TS, "w").write(src)
print(len(entries), "entries added")
