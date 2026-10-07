#!/usr/bin/env python3
"""
Neofetch-style profile info card (terminal window SVG).

Content is sourced from README.md facts only — edit INFO below when your bio changes.
Pattern adapted from Aviv Ashishta's terminal GitHub profile README.

    python scripts/make_info_card.py [output.svg]
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

# ---- profile facts (from README.md on main) --------------------------------
HOST = "bjb0@github"
NAME = "Bhargab Jyoti Bhuyan"
TITLE = "AI/ML & NLP engineer"
EDU = "B.Tech Computer Science & Engineering · Tezpur University (Class of 2026)"
TAGLINE = (
    "I build end-to-end ML pipelines, deploy models with FastAPI, and ship "
    "LLM-powered apps—with recent work in multilingual dense retrieval and NLP research."
)
OPEN = "Open to full-time roles, internships, and hackathons in AI/ML & NLP—and thoughtful collaborations."

HIGHLIGHTS = [
    "Education: B.Tech CSE at Tezpur University, Assam (Aug 2022 – Jun 2026).",
    "Now: AI Research & Engineering Intern at Khyontek AI — CLEF 2026 CheckThat! Task 1 "
    "(retrieving publications cited in multilingual social claims); experiments with "
    "multilingual-E5, BGE, and Contriever; co-authored submission to CEUR-WS proceedings.",
    "Before: Project intern at C-DAC (ANUVAAD Chat multilingual backend) and AI/ML research "
    "intern at IIT Guwahati (grasp-force prediction, SHAP, cross-validation).",
    "Focus: Retrieval & reranking, RAG, reproducible ML, and backends that are ready to deploy—not just notebooks.",
]

STACK = [
    "Python · PyTorch · TensorFlow · Pandas · FastAPI · Docker · Git · GitHub Actions",
    "React · Flask · Streamlit · Linux · Postgres",
    "LLMs & NLP: Dense retrieval · RAG · LangChain · LangGraph · scikit-learn · prompt design · Gemini / OpenAI / Anthropic APIs",
    "Also: Pydantic · MLflow · DVC · vector stores (learning advanced retrieval & reranking).",
]

FUN = "Fun fact: I lift heavier than my code compiles."

# ---- layout ----------------------------------------------------------------
BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
CYAN = "#22d3ee"
GREEN = "#39d353"
MAGENTA = "#d2a8ff"
YELLOW = "#f2cc60"

W, H = 840, 880
PAD = 20
TITLEBAR_H = 30
LINE_H = 17
LOGO_W = 92

# timing
LINE_STAGGER = 0.04
FADE_DUR = 0.35


def esc(s):
    return html.escape(s)


def wrap(text, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def logo_blocks():
    """Simple neofetch-style ASCII logo."""
    return [
        "  █▀▀▄  ",
        "  █  █  ",
        "  ▀▀▀   ",
    ]


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    "<style>"
    f".ln{{opacity:0;animation:fade {FADE_DUR}s ease-out both}}"
    "@keyframes fade{0%{opacity:0;transform:translateX(-6px)}100%{opacity:1;transform:none}}"
    "@media (prefers-reduced-motion: reduce){.ln{opacity:1!important;transform:none!important;animation:none!important}}"
    "</style>",
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
    f'text-anchor="middle">{esc(HOST)}: ~$ neofetch</text>'
)

# logo
logo = logo_blocks()
logo_x = PAD
logo_y = TITLEBAR_H + PAD + 8
for i, row in enumerate(logo):
    parts.append(
        f'<text x="{logo_x}" y="{logo_y + i * 14}" fill="{CYAN}" font-size="13" font-weight="700">'
        f"{esc(row)}</text>"
    )

text_x = PAD + LOGO_W
y = TITLEBAR_H + PAD + 4
delay = 0.0

def line(text, size=13, fill=INK, bold=False):
    global y, delay
    weight = ' font-weight="700"' if bold else ""
    parts.append(
        f'<text class="ln" x="{text_x}" y="{y}" fill="{fill}" font-size="{size}"{weight} '
        f'style="animation-delay:{delay:.2f}s">{text}</text>'
    )
    y += LINE_H if size <= 13 else LINE_H + 2
    delay += LINE_STAGGER


line(f'<tspan fill="{CYAN}">{esc(HOST)}</tspan>', bold=True)
line(f'<tspan fill="{GREEN}">OS:</tspan> {esc(EDU)}')
line(f'<tspan fill="{GREEN}">Host:</tspan> {esc(NAME)}')
line(f'<tspan fill="{GREEN}">Kernel:</tspan> {esc(TITLE)}')
line(f'<tspan fill="{GREEN}">Shell:</tspan> {esc(TAGLINE)}', size=12)
y += 6
delay += 0.05
line(f'<tspan fill="{YELLOW}">Uptime:</tspan> {esc(OPEN)}', size=12)

y += 8
line(f'<tspan fill="{MAGENTA}">Packages</tspan> (highlights):', bold=True)
for h in HIGHLIGHTS:
    for wl in wrap(h, 62):
        line(f"  ▸ {esc(wl)}", size=11, fill=MUTED)

y += 6
line(f'<tspan fill="{MAGENTA}">Languages</tspan> (tech):', bold=True)
for s in STACK:
    for wl in wrap(s, 62):
        line(f"  {esc(wl)}", size=11, fill=INK)

y += 10
line(f'<tspan fill="{MUTED}">{esc(FUN)}</tspan>', size=11)

# blinking cursor bottom-right
parts.append(
    f'<rect x="{W - PAD - 10}" y="{H - PAD - 8}" width="8" height="14" fill="{INK}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
    f'dur="1s" repeatCount="indefinite"/></rect>'
)

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)//1024} KB")
