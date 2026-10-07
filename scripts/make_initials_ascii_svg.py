#!/usr/bin/env python3
"""
Monochrome initials ASCII portrait (no photo required).

Inspired by AVIVASHISHTA29/terminal README pattern — replace with a real portrait via:
  python scripts/prep_photo.py your-photo.png
  python scripts/make_ascii_svg.py

    python scripts/make_initials_ascii_svg.py [output.svg]
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "profile-ascii.svg")

# block-letter "BJB" + subtle frame (monospace art)
ART = [
    "      ██████╗       ██╗ ██████╗       ██████╗ ",
    "      ██╔══██╗      ██║ ██╔══██╗      ██╔══██╗",
    "      ██████╔╝      ██║ ██████╔╝      ██████╔╝",
    "      ██╔══██╗ ██   ██║ ██╔══██╗      ██╔══██╗",
    "      ██████╔╝ ╚█████╔╝ ██████╔╝      ██████╔╝",
    "      ╚═════╝   ╚════╝  ╚═════╝       ╚═════╝ ",
    "                                              ",
    "         ·  AI / ML  ·  NLP  ·  retrieval  · ",
    "              Tezpur University · 2026       ",
]

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#c9d1d9"
CURSOR = "#c9d1d9"
ACCENT = "#22d3ee"

W, H = 840, 880  # match info-card.svg for side-by-side README layout
CELL_W = 5.0
CELL_H = 9.0
COLS = max(len(line) for line in ART)
ROWS = len(ART)
PAD = 20
TITLEBAR_H = 30
STATUS_H = 30
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W, CANVAS_H = W, H
art_left = (CANVAS_W - ART_W) / 2

ROW_DUR = 5.8 / ROWS
STAGGER = ROW_DUR
art_top = TITLEBAR_H + PAD * 0.35
font_size = CELL_H * 0.86

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, '
    f'Menlo, Consolas, monospace">',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
    f'fill="none" stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(
    f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
    f'text-anchor="middle">bjb0@github: ~$ ./portrait.sh --initials</text>'
)

for ry, line in enumerate(ART):
    y = art_top + ry * CELL_H + CELL_H * 0.74
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER
    fill = ACCENT if ry < 6 else INK
    safe = html.escape(line)
    text = (
        f'<text xml:space="preserve" x="{art_left:.1f}" y="{y:.1f}" fill="{fill}" '
        f'font-size="{font_size:.1f}">{safe}</text>'
    )
    parts.append(
        f'<clipPath id="r{ry}"><rect x="{art_left:.1f}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')

status_line_y = TITLEBAR_H + ART_H + PAD * 0.35 + 40
status_y = status_line_y + 19
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
parts.append(
    f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
    f'bjb0@github:~$ whoami <tspan fill="{INK}">Bhargab Jyoti Bhuyan</tspan></text>'
)
parts.append("</svg>")

svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", CANVAS_W, "x", CANVAS_H)
