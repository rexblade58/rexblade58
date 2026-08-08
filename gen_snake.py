#!/usr/bin/env python3
"""Generate an ANIMATED github-snake-dark.svg matching Platane/snk style.
The snake is made of a dashed path animated with CSS keyframes, plus a
contribution grid beneath it."""

import json
import os
from datetime import date, timedelta

DATA = json.load(open(os.path.join(os.path.dirname(__file__), "contrib2026.json"), "r", encoding="utf-8-sig"))
counts = {d["date"]: d["count"] for d in DATA}

start = date(2026, 1, 1)
end = date(2026, 12, 31)
all_days = []
cur = start
while cur <= end:
    iso = cur.isoformat()
    all_days.append({"date": iso, "count": counts.get(iso, 0)})
    cur += timedelta(days=1)

# Pad to Sunday-start weeks
first_sunday = start - timedelta(days=start.weekday() + 1)
padded = []
c = first_sunday
while c < start:
    padded.append({"date": c.isoformat(), "count": 0})
    c += timedelta(days=1)
padded.extend(all_days)
while len(padded) % 7 != 0:
    padded.append({"date": "", "count": 0})

weeks = [padded[i:i + 7] for i in range(0, len(padded), 7)]

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def intensity(count):
    if count <= 0: return 0
    if count <= 3: return 1
    if count <= 6: return 2
    if count <= 9: return 3
    return 4

CELL = 11
GAP = 3
PAD = 16
HEADER = 40
cols = len(weeks)
SW = PAD * 2 + cols * CELL + (cols - 1) * GAP
SH = HEADER + PAD * 2 + 7 * CELL + 6 * GAP + 80

out = []
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}">')
out.append('<defs>')
out.append('<style>')
out.append('  .bg { fill: #0d1117; }')
out.append('  .label { font-family: -apple-system, Arial, sans-serif; font-size: 13px; fill: #8b949e; }')
out.append('  @keyframes dash { to { stroke-dashoffset: 0; } }')
out.append('  @keyframes glow { 0%,100% { opacity: 0.35; } 50% { opacity: 1; } }')
out.append('  .snake-path { stroke-dasharray: 40 600; stroke-dashoffset: 640; animation: dash 4s linear infinite; }')
out.append('  .snake-head { animation: glow 1.2s ease-in-out infinite; }')
out.append('</style>')
out.append('</defs>')
out.append(f'<rect class="bg" width="100%" height="100%"/>')
out.append(f'<text class="label" x="{PAD}" y="24">GitHub contributions - rexblade58 - 2026</text>')

# Grid
for wi, week in enumerate(weeks):
    for di, day in enumerate(week):
        if not day["date"]:
            continue
        x = PAD + wi * (CELL + GAP)
        y = HEADER + PAD + di * (CELL + GAP)
        lvl = intensity(day["count"])
        out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{PALETTE[lvl]}"/>')

# Snake path: serpentine across the grid
snake_y_base = HEADER + PAD + 3 * (CELL + GAP) + 6
path = f'M {PAD} {snake_y_base} '
for wi in range(cols):
    x = PAD + wi * (CELL + GAP) + CELL / 2
    # serpentine: alternate up/down every 4 columns
    band = (wi // 4) % 2
    y = snake_y_base + band * 40
    path += f'L {x} {y} '
out.append(f'<path class="snake-path" d="{path}" fill="none" stroke="#39d353" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
out.append(f'<circle class="snake-head" cx="{PAD + (cols-1)*(CELL+GAP) + CELL/2}" cy="{snake_y_base + ((cols-1)//4 % 2) * 40}" r="6" fill="#39d353"/>')

# Food pellets along the path
out.append(f'<text class="label" x="{PAD}" y="{SH-14}">Generated from real contribution data - {sum(d["count"] for d in all_days)} total in 2026</text>')
out.append('</svg>')

with open("github-snake-dark.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"Animated snake written: {SW}x{SH}, {cols} weeks")
