"""The connector: one thin fungal hypha line in SFW green.

Every grid tile carries the line through the same four edge points, so any
tile fits next to any other (edge-matched, or Wang, tiles). Inside the tile the
line finds its own way around the content, so each tile routes differently.

Edge points and line look live here and nowhere else.
"""
import heapq
import math
import random

from PIL import Image, ImageDraw

GREEN = (21, 104, 38)  # #156826

W, H = 1080, 1440  # 3:4, what the Instagram profile grid shows in full

# The fixed edge points: exact middle of each edge.
LEFT = (0, H // 2)
RIGHT = (W, H // 2)
TOP = (W // 2, 0)
BOTTOM = (W // 2, H)

LINE_PX = 4.0  # at 1080 px wide
CELL = 12  # routing grid
CLEARANCE = 26  # how close the line may come to a photo or text block
STRAIGHT = 40  # the line leaves every edge point straight for this many px
MARGIN = 84  # content keeps this far from the edges, so the line can get in and out


def _noise_field(cols, rows, rnd):
    """Smooth random costs, so each seed wanders a different way."""
    waves = [
        (rnd.uniform(0.02, 0.09), rnd.uniform(0.02, 0.09), rnd.uniform(0, 6.3), rnd.uniform(0.6, 1.4))
        for _ in range(4)
    ]
    out = []
    for r in range(rows):
        row = []
        for c in range(cols):
            v = sum(a * math.sin(fx * c + fy * r + ph) for fx, fy, ph, a in waves)
            row.append(max(0.4, 1.6 + v * 0.35))
        out.append(row)
    return out


def _blocked(rects, cols, rows, pad):
    grid = [[False] * cols for _ in range(rows)]
    for x0, y0, x1, y1 in rects:
        for r in range(max(0, int((y0 - pad) // CELL)), min(rows, int((y1 + pad) // CELL) + 1)):
            for c in range(max(0, int((x0 - pad) // CELL)), min(cols, int((x1 + pad) // CELL) + 1)):
                grid[r][c] = True
    return grid


def _dist_field(block, cols, rows):
    """Cells to the nearest blocked cell (BFS), so the line can hug content."""
    INF = 10**6
    d = [[INF] * cols for _ in range(rows)]
    q = []
    for r in range(rows):
        for c in range(cols):
            if block[r][c]:
                d[r][c] = 0
                q.append((r, c))
    i = 0
    while i < len(q):
        r, c = q[i]
        i += 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < rows and 0 <= cc < cols and d[rr][cc] > d[r][c] + 1:
                d[rr][cc] = d[r][c] + 1
                q.append((rr, cc))
    return d


def _astar(start, goal, block, cost, avoid):
    rows, cols = len(block), len(block[0])
    sr, sc = start
    gr, gc = goal
    openq = [(0, 0, sr, sc)]
    g = {(sr, sc): 0}
    prev = {}
    steps = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.42), (1, -1, 1.42), (-1, 1, 1.42), (-1, -1, 1.42)]
    while openq:
        _, gs, r, c = heapq.heappop(openq)
        if (r, c) == (gr, gc):
            break
        if gs > g.get((r, c), 1e18):
            continue
        for dr, dc, k in steps:
            rr, cc = r + dr, c + dc
            if not (0 <= rr < rows and 0 <= cc < cols) or block[rr][cc]:
                continue
            ng = gs + k * (cost[rr][cc] + avoid.get((rr, cc), 0))
            if ng < g.get((rr, cc), 1e18):
                g[(rr, cc)] = ng
                prev[(rr, cc)] = (r, c)
                h = math.hypot(rr - gr, cc - gc)
                heapq.heappush(openq, (ng + h, ng, rr, cc))
    if (gr, gc) not in prev and (gr, gc) != (sr, sc):
        raise RuntimeError('No route for the hypha line; the layout blocks an edge')
    path = [(gr, gc)]
    while path[-1] != (sr, sc):
        path.append(prev[path[-1]])
    return path[::-1]


def _rdp(pts, eps):
    """Drop the grid's stair steps: keep only the points that shape the path."""
    if len(pts) < 3:
        return pts
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1
    best, idx = 0.0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * (pts[i][0] - x0) - dx * (pts[i][1] - y0)) / ln
        if d > best:
            best, idx = d, i
    if best <= eps:
        return [pts[0], pts[-1]]
    return _rdp(pts[: idx + 1], eps)[:-1] + _rdp(pts[idx:], eps)


def _chaikin(pts, n=4):
    """Round the corners. Corner cutting stays inside the path's hull, so no loops."""
    for _ in range(n):
        out = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            out.append((0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1))
            out.append((0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1))
        out.append(pts[-1])
        pts = out
    return pts


def _resample(pts, step=5.0):
    out = [pts[0]]
    acc = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        if seg == 0:
            continue
        t = step - acc
        while t <= seg:
            out.append((x0 + (x1 - x0) * t / seg, y0 + (y1 - y0) * t / seg))
            t += step
        acc = seg - (t - step)
    if out[-1] != pts[-1]:
        out.append(pts[-1])
    return out


def _wobble(pts, rnd, amp):
    """Hand-drawn feel: a small sideways drift, zero near both edge points."""
    n = len(pts)
    ph1, ph2 = rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)
    f1, f2 = rnd.uniform(0.018, 0.03), rnd.uniform(0.05, 0.08)
    out = []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln, tx / ln
        dist_end = min(i, n - 1 - i) * 5.0
        fade = max(0.0, min(1.0, (dist_end - STRAIGHT) / 80))
        o = amp * fade * (math.sin(i * f1 + ph1) + 0.4 * math.sin(i * f2 + ph2))
        out.append((x + nx * o, y + ny * o))
    return out


def _edge_cell(p, inward):
    x, y = p
    x = min(max(x, 1), W - 1)
    y = min(max(y, 1), H - 1)
    return (int(y // CELL) + inward[1], int(x // CELL) + inward[0])


def route(obstacles, seed, strands=('h', 'v'), size=(W, H)):
    """Return the line as a list of polylines (main strands then branches).

    obstacles: content rects (x0, y0, x1, y1) the line must go around.
    strands: 'h' runs left middle to right middle, 'v' top middle to bottom middle.
    """
    global W, H
    W0, H0 = W, H
    W, H = size
    try:
        rnd = random.Random(seed)
        cols, rows = W // CELL + 1, H // CELL + 1
        block = _blocked(obstacles, cols, rows, CLEARANCE)
        dist = _dist_field(block, cols, rows)
        noise = _noise_field(cols, rows, rnd)
        hug = rnd.uniform(5, 9)  # cells: how close the line likes to run to content
        cost = [
            [
                noise[r][c]
                + (0.9 if dist[r][c] > hug else 0)
                + (1.2 if dist[r][c] < 2 else 0)
                + (2.5 if min(r, c, rows - 1 - r, cols - 1 - c) < 3 else 0)  # keep off the tile border
                for c in range(cols)
            ]
            for r in range(rows)
        ]
        ends = {
            'h': ((0, H // 2), (W, H // 2), (1, 0), (-1, 0)),
            'v': ((W // 2, 0), (W // 2, H), (0, 1), (0, -1)),
        }
        lines = []
        avoid = {}
        for s in strands:
            a, b, ia, ib = ends[s]
            k = STRAIGHT // CELL
            # The straight run out of each edge point is kept clear of content.
            ca = _edge_cell(a, (ia[0] * k, ia[1] * k))
            cb = _edge_cell(b, (ib[0] * k, ib[1] * k))
            for p, inward in ((a, ia), (b, ib)):
                for j in range(k + 1):
                    r, c = _edge_cell(p, (inward[0] * j, inward[1] * j))
                    if block[r][c]:
                        raise RuntimeError(f'Content too close to the edge point {p}')
            cells = _astar(ca, cb, block, cost, avoid)
            # The next strand keeps its distance, and crosses rather than shares a path.
            for r, c in cells:
                for dr in range(-4, 5):
                    for dc in range(-4, 5):
                        avoid[(r + dr, c + dc)] = 6.0
            mid = [(c * CELL + CELL / 2, r * CELL + CELL / 2) for r, c in cells]
            # Snap the straight run onto the exact edge axis.
            pa = (a[0] + ia[0] * STRAIGHT, a[1] + ia[1] * STRAIGHT)
            pb = (b[0] + ib[0] * STRAIGHT, b[1] + ib[1] * STRAIGHT)
            inner = [pa] + mid[1:-1] + [pb]
            for eps in (14, 9, 5, 0):
                shaped = _resample(_chaikin([a] + _rdp(inner, eps) + [b]), 5.0)
                if not any(_inside(q, obstacles, 4) for q in shaped):
                    break
            pts = _wobble(shaped, rnd, rnd.uniform(4.0, 8.0))
            pts[0], pts[-1] = a, b
            lines.append(('main', pts))
        lines += _branches(lines, obstacles, rnd)
        return lines
    finally:
        W, H = W0, H0


def _inside(p, rects, pad):
    x, y = p
    return any(x0 - pad <= x <= x1 + pad and y0 - pad <= y <= y1 + pad for x0, y0, x1, y1 in rects)


def _branches(lines, rects, rnd):
    out = []
    for _, pts in list(lines):
        n = len(pts)
        for _ in range(rnd.randint(2, 4)):
            i = rnd.randint(int(n * 0.15), int(n * 0.85))
            x, y = pts[i]
            if min(x, W - x, y, H - y) < 90:
                continue
            a, b = pts[max(0, i - 2)], pts[min(n - 1, i + 2)]
            ang = math.atan2(b[1] - a[1], b[0] - a[0]) + rnd.choice((-1, 1)) * rnd.uniform(0.6, 1.3)
            length = rnd.uniform(30, 110)
            bend = rnd.uniform(-0.03, 0.03)
            br = [(x, y)]
            ok = True
            for k in range(1, int(length / 5)):
                ang += bend + rnd.uniform(-0.05, 0.05)
                nx, ny = br[-1][0] + 5 * math.cos(ang), br[-1][1] + 5 * math.sin(ang)
                if _inside((nx, ny), rects, 12) or not (30 < nx < W - 30 and 30 < ny < H - 30):
                    ok = len(br) > 6
                    break
                br.append((nx, ny))
            if ok and len(br) > 4:
                out.append(('branch', br))
                if rnd.random() < 0.45 and len(br) > 10:
                    j = rnd.randint(len(br) // 3, len(br) - 3)
                    sx, sy = br[j]
                    a2 = ang + rnd.choice((-1, 1)) * rnd.uniform(0.5, 1.0)
                    sub = [(sx, sy)]
                    for _ in range(rnd.randint(5, 12)):
                        nx, ny = sub[-1][0] + 5 * math.cos(a2), sub[-1][1] + 5 * math.sin(a2)
                        if _inside((nx, ny), rects, 12):
                            break
                        sub.append((nx, ny))
                    if len(sub) > 3:
                        out.append(('twig', sub))
    return out


def draw(lines, size=(W, H), scale=2):
    """The line as a transparent RGBA layer, drawn at 2x and shrunk for smooth edges."""
    w, h = size
    s = scale * w / 1080
    im = Image.new('RGBA', (w * scale, h * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for kind, pts in lines:
        n = len(pts)
        for i, (x, y) in enumerate(pts):
            if kind == 'main':
                wdt = LINE_PX
            else:
                start = 2.6 if kind == 'branch' else 1.8
                wdt = start - (start - 0.8) * i / max(1, n - 1)
            r = wdt * s / 2
            cx, cy = x * scale, y * scale
            if i:
                px, py = pts[i - 1]
                d.line([(px * scale, py * scale), (cx, cy)], fill=GREEN + (255,), width=max(1, round(2 * r)))
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GREEN + (255,))
    return im.resize((w, h), Image.LANCZOS)
