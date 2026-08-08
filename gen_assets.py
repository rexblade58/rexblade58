#!/usr/bin/env python3
"""Generate Sharann-del-style section SVGs for rexblade58 profile.
Each SVG: mono font, animated draw-in rule line, section number,
dark/light adaptive via prefers-color-scheme CSS."""

import os

OUT = os.path.join(os.path.dirname(__file__), "assets", "dark")
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), "assets"), exist_ok=True)

HEADER_CSS = """<style>
    :root { --rule: #C0C0C0; --muted: #888888; --accent: #4DFF88; --ghost: #CCCCCC; --ink: #111111; --paper: #FFFFFF; }
    @media (prefers-color-scheme: dark) {
      :root { --rule: #444444; --muted: #777777; --accent: #4DFF88; --ghost: #2A2A2A; --ink: #EEEEEE; --paper: #0D1117; }
    }
    .mono { font-family: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace; }
    .draw { stroke: var(--rule); stroke-width: 1.5; stroke-dasharray: 760; stroke-dashoffset: 760; animation: d 1.3s cubic-bezier(.6,0,.2,1) .2s forwards; }
    @keyframes d { to { stroke-dashoffset: 0; } }
    .f { opacity: 0; animation: f .8s ease .1s forwards; }
    @keyframes f { to { opacity: 1; } }
    @media (prefers-reduced-motion: reduce) { .draw,.f { animation: none; } .draw { stroke-dashoffset: 0; } .f { opacity: 1; } }
</style>"""

def section_svg(num, label, title, y=92):
    return f"""<svg viewBox="0 0 1000 92" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">
{HEADER_CSS}
  <g class="f">
    <text class="mono" x="48" y="64" font-size="44" fill="var(--accent)">{num}</text>
    <text class="mono" x="112" y="64" font-size="26" fill="var(--ghost)" letter-spacing="4">{label}</text>
  </g>
  <line class="draw" x1="48" y1="{y-28}" x2="952" y2="{y-28}"/>
</svg>"""

# ---------- Header ----------
header = f"""<svg viewBox="0 0 1000 180" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Menard Rosal header">
{HEADER_CSS}
  <rect width="1000" height="180" fill="var(--paper)"/>
  <g class="f">
    <text class="mono" x="48" y="72" font-size="52" fill="var(--accent)">&gt;_</text>
    <text class="mono" x="110" y="72" font-size="46" fill="var(--ink)">Menard Rosal</text>
    <text class="mono" x="48" y="112" font-size="20" fill="var(--muted)">Software Engineer & Founder @ Letho AI</text>
    <text class="mono" x="48" y="140" font-size="16" fill="var(--ghost)">Southern Leyte, Philippines | Full-Stack | AI Agents | Multi-tenant SaaS</text>
  </g>
  <line class="draw" x1="48" y1="156" x2="952" y2="156"/>
</svg>"""

# ---------- Whoami ----------
whoami = f"""<svg viewBox="0 0 1000 240" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="whoami">
{HEADER_CSS}
  <g class="f">
    <text class="mono" x="48" y="56" font-size="18" fill="var(--accent)" letter-spacing="2">WHOAMI</text>
    <text class="mono" x="48" y="96" font-size="15" fill="var(--ink)">$ whoami</text>
    <text class="mono" x="48" y="126" font-size="15" fill="var(--muted)">Full-stack engineer. Founding lead of Bodego - a universal</text>
    <text class="mono" x="48" y="148" font-size="15" fill="var(--muted)">inventory management platform at Credo Tech.</text>
    <text class="mono" x="48" y="178" font-size="15" fill="var(--muted)">PhilNITS IP Passer. Dean's List, BS IT - Saint Joseph College.</text>
    <text class="mono" x="48" y="216" font-size="15" fill="var(--accent)">$ cat expertise.txt</text>
    <text class="mono" x="48" y="244" font-size="14" fill="var(--ghost)">react | node | python | postgres | rust | go | ai-agents</text>
  </g>
</svg>"""

# ---------- Ecosystem ----------
eco = f"""<svg viewBox="0 0 1000 300" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Project ecosystem">
{HEADER_CSS}
  <g class="f">
    <text class="mono" x="48" y="52" font-size="18" fill="var(--accent)" letter-spacing="2">PROJECT ECOSYSTEM</text>
    <circle cx="500" cy="160" r="42" fill="var(--paper)" stroke="var(--accent)" stroke-width="2"/>
    <text class="mono" x="500" y="166" font-size="13" fill="var(--accent)" text-anchor="middle">CORE</text>
  </g>
  <g class="draw">
    <line x1="500" y1="160" x2="200" y2="80"/>
    <line x1="500" y1="160" x2="180" y2="240"/>
    <line x1="500" y1="160" x2="500" y2="280"/>
    <line x1="500" y1="160" x2="800" y2="80"/>
    <line x1="500" y1="160" x2="820" y2="240"/>
  </g>
  <g class="f">
    <circle cx="200" cy="80" r="30" fill="var(--paper)" stroke="var(--ghost)" stroke-width="1.5"/>
    <text class="mono" x="200" y="85" font-size="12" fill="var(--ink)" text-anchor="middle">Bodego</text>
    <circle cx="180" cy="240" r="30" fill="var(--paper)" stroke="var(--ghost)" stroke-width="1.5"/>
    <text class="mono" x="180" y="245" font-size="12" fill="var(--ink)" text-anchor="middle">MAYKaya</text>
    <circle cx="500" cy="280" r="30" fill="var(--paper)" stroke="var(--ghost)" stroke-width="1.5"/>
    <text class="mono" x="500" y="285" font-size="12" fill="var(--ink)" text-anchor="middle">Letho AI</text>
    <circle cx="800" cy="80" r="30" fill="var(--paper)" stroke="var(--ghost)" stroke-width="1.5"/>
    <text class="mono" x="800" y="85" font-size="12" fill="var(--ink)" text-anchor="middle">Nexumi</text>
    <circle cx="820" cy="240" r="30" fill="var(--paper)" stroke="var(--ghost)" stroke-width="1.5"/>
    <text class="mono" x="820" y="245" font-size="12" fill="var(--ink)" text-anchor="middle">Kaetram</text>
  </g>
</svg>"""

# ---------- Stack ----------
stack_items = [
    ("LANG", "TypeScript, JavaScript, Python, Java, C#, Rust, Go"),
    ("FRONT", "React, Next.js, Vite, Tailwind, GSAP, Three.js"),
    ("BACK", "Node.js, Express, Django, PostgreSQL, Redis"),
    ("CLOUD", "Firebase, GCP, Netlify, Vercel, Docker"),
    ("AI", "OpenAI, Ollama, LangChain, MCP, AI Agents"),
]
rows = ""
y = 96
for k, v in stack_items:
    rows += f'<text class="mono" x="48" y="{y}" font-size="14" fill="var(--accent)">[{k}]</text>'
    rows += f'<text class="mono" x="160" y="{y}" font-size="14" fill="var(--ink)">{v}</text>'
    y += 34
stack = f"""<svg viewBox="0 0 1000 260" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Technical stack">
{HEADER_CSS}
  <g class="f">
    <text class="mono" x="48" y="52" font-size="18" fill="var(--accent)" letter-spacing="2">TECHNICAL STACK</text>
{rows}
  </g>
</svg>"""

# ---------- Stats ----------
stats = f"""<svg viewBox="0 0 1000 240" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Statistics">
{HEADER_CSS}
  <g class="f">
    <text class="mono" x="48" y="52" font-size="18" fill="var(--accent)" letter-spacing="2">TELEMETRY</text>
    <text class="mono" x="48" y="110" font-size="13" fill="var(--muted)">CONTRIBUTIONS 2026</text>
    <text class="mono" x="48" y="150" font-size="40" fill="var(--accent)">1,942</text>
    <text class="mono" x="290" y="110" font-size="13" fill="var(--muted)">ACTIVE DAYS</text>
    <text class="mono" x="290" y="150" font-size="40" fill="var(--ink)">221</text>
    <text class="mono" x="520" y="110" font-size="13" fill="var(--muted)">STREAK</text>
    <text class="mono" x="520" y="150" font-size="40" fill="var(--ink)">221d</text>
    <text class="mono" x="740" y="110" font-size="13" fill="var(--muted)">LANGUAGES</text>
    <text class="mono" x="740" y="150" font-size="40" fill="var(--ink)">11</text>
    <text class="mono" x="48" y="210" font-size="13" fill="var(--ghost)">2016 - 2026 | 10 years of building</text>
  </g>
</svg>"""

# ---------- Timeline ----------
years = ["2016-2018  Learning & games (Kaetram, Cataclysm)", "2019-2020  LMS, enrollment & queue systems", "2021-2023  College, Explore Maasin, E-Payslip", "2024-2025  Bodego platform, OMR, facial recognition", "2026  Letho AI, AI agents, MAYKaya"]
rows = ""
y = 96
for t in years:
    rows += f'<circle cx="48" cy="{y-5}" r="4" fill="var(--accent)"/>'
    rows += f'<text class="mono" x="70" y="{y}" font-size="14" fill="var(--ink)">{t}</text>'
    y += 32
timeline = f"""<svg viewBox="0 0 1000 250" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Timeline">
{HEADER_CSS}
  <g class="f">
    <text class="mono" x="48" y="52" font-size="18" fill="var(--accent)" letter-spacing="2">ROUTE MAP</text>
    <line x1="52" y1="76" x2="52" y2="232" stroke="var(--rule)" stroke-width="1.5"/>
{rows}
  </g>
</svg>"""

# ---------- Footer ----------
footer = f"""<svg viewBox="0 0 1000 80" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Footer">
{HEADER_CSS}
  <g class="f">
    <text class="mono" x="48" y="44" font-size="14" fill="var(--ghost)">status: OPEN_TO_WORK | building: letho-ai | stack: ts+py+rust</text>
    <line class="draw" x1="48" y1="58" x2="952" y2="58"/>
  </g>
</svg>"""

files = {
    "header-v1.svg": header,
    "s01.svg": section_svg("01", "WHOAMI", "whoami"),
    "s02.svg": section_svg("02", "ECOSYSTEM", "ecosystem"),
    "s03.svg": section_svg("03", "STACK", "stack"),
    "s04.svg": section_svg("04", "TELEMETRY", "telemetry"),
    "s05.svg": section_svg("05", "ROUTE", "timeline"),
    "whoami.svg": whoami,
    "ecosystem.svg": eco,
    "stack.svg": stack,
    "telemetry.svg": stats,
    "timeline.svg": timeline,
    "footer.svg": footer,
}

for name, svg in files.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  {name}")
print("Dark assets done")
