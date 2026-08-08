#!/usr/bin/env python3
"""Render the contribution grid as a playable-looking Snake game.

The snake walks the grid one cell at a time, orthogonally, hunting the days
that have contributions. Target choice is randomised among the nearest few
pellets, so the route wanders instead of sweeping in reading order. A cell
switches to the empty colour on the frame the head reaches it.

Animation is pure CSS: one @keyframes for the route, shared by every body
segment at a different negative animation-delay, plus one small keyframes
per eat-time bucket. No script, no SMIL, so it animates inside the <img>
that GitHub renders the README with.
"""

import json
import os
import random
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "github-snake-dark.svg")

# CELL+GAP and PAD are chosen so every cell centre lands on a whole pixel --
# keeps the route keyframes short.
CELL, GAP, PAD = 12, 2, 10
PITCH = CELL + GAP
COLS, ROWS = 53, 7

EMPTY = "#161b22"
LEVELS = ["#0e4429", "#006d32", "#26a641", "#39d353"]
# Mint-to-teal so the snake never reads as just another bright contribution
# square, plus a background-coloured outline to separate it from the cells it
# passes over.
HEAD = "#e9fff4"
BODY = ["#8affc0", "#4dff88", "#2fe875", "#1fc964", "#16a085", "#127f68"]
OUTLINE = "#0d1117"

SEGMENTS = len(BODY) + 1          # head + body
STEP_SECONDS = 0.055              # wall time the head spends on one cell
TAIL_PAUSE = 1.6                  # beat at the end before the loop restarts

random.seed(20260809)


def load_grid():
    """Sunday-first columns, same shape GitHub draws."""
    path = os.path.join(HERE, "contrib2026.json")
    raw = json.load(open(path, encoding="utf-8-sig"))
    counts = {d["date"]: d["count"] for d in raw}

    start, end = date(2026, 1, 1), date(2026, 12, 31)
    days, cur = [], start - timedelta(days=(start.weekday() + 1) % 7)
    while cur <= end:
        days.append((cur, counts.get(cur.isoformat(), 0) if cur >= start else 0))
        cur += timedelta(days=1)

    grid = {}
    for i, (day, count) in enumerate(days):
        col, row = i // 7, i % 7
        if col < COLS:
            grid[(col, row)] = count
    return grid


def level(count):
    if count <= 0:
        return -1
    if count <= 3:
        return 0
    if count <= 8:
        return 1
    if count <= 20:
        return 2
    return 3


def plan_route(food):
    """Greedy tour with a wobble: pick one of the three closest pellets, then
    walk to it a cell at a time, alternating axes so the line reads as a snake
    rather than an L. Anything edible under the head en route is eaten early."""
    remaining = set(food)
    pos = (0, 3)
    route = [pos]
    eaten = {}

    if pos in remaining:
        eaten[pos] = 0
        remaining.discard(pos)

    while remaining:
        ranked = sorted(remaining,
                        key=lambda c: abs(c[0] - pos[0]) + abs(c[1] - pos[1]))
        target = random.choice(ranked[:3])

        while pos != target:
            dx = target[0] - pos[0]
            dy = target[1] - pos[1]
            # Bias toward the longer axis, but leave room to zigzag.
            if dx and dy:
                horizontal = random.random() < (abs(dx) / (abs(dx) + abs(dy)))
            else:
                horizontal = bool(dx)
            if horizontal:
                pos = (pos[0] + (1 if dx > 0 else -1), pos[1])
            else:
                pos = (pos[0], pos[1] + (1 if dy > 0 else -1))

            route.append(pos)
            if pos in remaining:
                eaten[pos] = len(route) - 1
                remaining.discard(pos)

    # Slide off the right edge to close the loop cleanly.
    while pos[0] < COLS + 1:
        pos = (pos[0] + 1, pos[1])
        route.append(pos)

    return route, eaten


def cx(col):
    return PAD + col * PITCH + CELL // 2


def cy(row):
    return PAD + row * PITCH + CELL // 2


def build():
    grid = load_grid()
    food = [c for c, n in grid.items() if n > 0]
    route, eaten = plan_route(food)

    steps = len(route) - 1
    travel = steps * STEP_SECONDS
    total = travel + TAIL_PAUSE
    lead = (SEGMENTS - 1) * STEP_SECONDS      # head runs ahead of the tail

    width = PAD * 2 + COLS * PITCH - GAP
    height = PAD * 2 + ROWS * PITCH - GAP

    # ---- route keyframes: one block, every segment replays it time-shifted
    frames = []
    for i, (col, row) in enumerate(route):
        pct = i / steps * (travel / total) * 100
        frames.append(f"{pct:.3f}%{{transform:translate({cx(col)}px,{cy(row)}px)}}")
    # Hold at the exit point through the pause so the loop does not snap back.
    frames.append(f"100%{{transform:translate({cx(route[-1][0])}px,{cy(route[-1][1])}px)}}")

    # ---- eat keyframes, bucketed so cells eaten at the same moment share one
    buckets, cell_bucket = {}, {}
    for cell, idx in eaten.items():
        when = max(0.0, (idx * STEP_SECONDS - lead)) / total * 100
        key = round(when, 1)
        if key not in buckets:
            buckets[key] = f"k{len(buckets)}"
        cell_bucket[cell] = buckets[key]

    eat_css = []
    for when, name in sorted(buckets.items(), key=lambda kv: kv[0]):
        stop = min(100.0, when + 0.3)
        # The class binds the animation; the at-rule only declares it.
        eat_css.append(f".{name}{{animation-name:{name}}}")
        eat_css.append(
            f"@keyframes {name}{{0%,{when:.1f}%{{fill:var(--a);rx:2px}}"
            f"{stop:.1f}%,100%{{fill:{EMPTY};rx:6px}}}}"
        )

    css = [
        # Geometry in CSS keeps every <rect> down to a class and two coords.
        f"rect{{width:{CELL}px;height:{CELL}px;rx:2px}}",
        f".e{{fill:{EMPTY}}}",
        f"@keyframes route{{{''.join(frames)}}}",
        f".seg{{animation:route {total:.2f}s linear infinite}}",
        f".seg rect{{transform:translate(-{CELL // 2}px,-{CELL // 2}px);"
        f"stroke:{OUTLINE};stroke-width:1}}",
        f".c{{animation-duration:{total:.2f}s;animation-timing-function:linear;"
        "animation-iteration-count:infinite}",
        "@media (prefers-reduced-motion:reduce){.seg,.c{animation:none}"
        ".seg{visibility:hidden}}",
    ]
    for i, colour in enumerate(LEVELS):
        css.append(f".l{i}{{fill:{colour};--a:{colour}}}")
    for i in range(SEGMENTS):
        css.append(f".s{i}{{animation-delay:-{(SEGMENTS - 1 - i) * STEP_SECONDS:.3f}s}}")
    css += eat_css

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Snake eating the 2026 contribution graph">',
        "<style>" + "".join(css) + "</style>",
    ]

    # ---- grid
    out.append("<g>")
    for (col, row), count in sorted(grid.items()):
        lv = level(count)
        x, y = PAD + col * PITCH, PAD + row * PITCH
        if lv < 0:
            out.append(f'<rect class="e" x="{x}" y="{y}"/>')
        else:
            out.append(f'<rect class="c l{lv} {cell_bucket[(col, row)]}" '
                       f'x="{x}" y="{y}"/>')
    out.append("</g>")

    # ---- snake, tail first so the head paints on top
    for i in range(SEGMENTS - 1, -1, -1):
        fill = HEAD if i == 0 else BODY[i - 1]
        out.append(f'<g class="seg s{i}"><rect rx="3" fill="{fill}"/></g>')

    out.append("</svg>")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))

    size_kb = os.path.getsize(OUT) / 1024
    print(f"{OUT}")
    print(f"  {width}x{height}px | {len(food)} pellets | {steps} steps | "
          f"{total:.1f}s loop | {len(buckets)} eat buckets | {size_kb:.1f} KB")


if __name__ == "__main__":
    build()
