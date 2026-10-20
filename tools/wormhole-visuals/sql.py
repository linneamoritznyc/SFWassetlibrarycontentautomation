import json, sys
m = json.load(open('out/manifest.json'))
ids = sys.argv[1:] or list(m)
parts = []
for pid in ids:
    e = m[pid]
    slides = [dict(text=t, image=i) for t, i in zip(e['texts'], e['slides'])]
    parts.append(f"update wormhole_posts set slides = $j${json.dumps(slides, ensure_ascii=False)}$j$::jsonb, updated_by = 'Claude (visuals)', updated_at = now() where id = '{pid}';")
print("\n".join(parts))
