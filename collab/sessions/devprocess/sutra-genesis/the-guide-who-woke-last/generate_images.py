# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Guide Who Woke Last".

A story about a guide who wakes in the Chandrabhaga valley to find
the thread already strung, the actors already speaking, and a promise
made on her behalf before she existed.

Visual language: diagrammatic, ink-and-wash, warm parchment tones.
Matches existing MayaLucIA story illustrations.

Run with:  uv run generate_images.py
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

# ── Output ──────────────────────────────────────────────────────────
OUT = Path(__file__).parent / "../../../../../website/static/images/writing/the-guide-who-woke-last"
OUT = OUT.resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9  # inches — 1800×1350 px at 150 DPI

# ── Palette ─────────────────────────────────────────────────────────
# Chandrabhaga palette: glacial greys, walnut brown, deodar green
PARCHMENT     = "#F5F0E8"
PARCHMENT_DK  = "#EDE6D8"
INK           = "#5C4A3A"
INK_LIGHT     = "#8B7B6B"
INK_FAINT     = "#C4B8A8"

# Walnut ink tones
WALNUT        = "#4A3728"
WALNUT_LIGHT  = "#6B5040"
WALNUT_FAINT  = "#A08B70"

# Glacial river
GLACIER_GREY  = "#9EA8A8"
GLACIER_LIGHT = "#C0C8C8"
GLACIER_DARK  = "#6A7878"
SILT          = "#B0A898"

# Stone and architecture (Lahaul flat-roof)
STONE_GREY    = "#9A9485"
STONE_DARK    = "#6B6660"
MUD_PLASTER   = "#C4B8A0"
MUD_DARK      = "#8A7E68"

# Deodar and vegetation
DEODAR        = "#7A5C3A"
DEODAR_LIGHT  = "#A68B5B"
NAG_GREEN     = "#2E6B5A"

# Fire and warmth
EMBER         = "#C45824"
EMBER_GLOW    = "#E88040"
ASH           = "#B8B0A0"

# Snow and sky
SNOW          = "#E8EEF0"
SKY_DAWN      = "#D8C8B0"
SKY_NIGHT     = "#1A1A2A"
STARLIGHT     = "#C8D0E0"
MOONSILVER    = "#E0E8F0"

# Thread
THREAD_GOLD   = "#D4A830"
THREAD_DIM    = "#A08840"


# ── Shared helpers ──────────────────────────────────────────────────

def make_fig(width=W, height=H, bg=PARCHMENT):
    fig, ax = plt.subplots(1, 1, figsize=(width, height), facecolor=bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def add_parchment_texture(ax, seed=42):
    rng = np.random.default_rng(seed)
    for _ in range(8):
        cx, cy = rng.uniform(10, 90), rng.uniform(10, 90)
        r = rng.uniform(5, 15)
        circle = plt.Circle((cx, cy), r, color=PARCHMENT_DK,
                             alpha=rng.uniform(0.15, 0.35), zorder=0)
        ax.add_patch(circle)


def title_block(ax, title, subtitle="", y=95):
    ax.text(50, y, title, ha="center", va="top",
            fontsize=18, fontweight="bold", color=INK,
            fontfamily="serif")
    if subtitle:
        ax.text(50, y - 4, subtitle, ha="center", va="top",
                fontsize=11, fontstyle="italic", color=INK_LIGHT,
                fontfamily="serif")


def attribution(ax, text="The Guide Who Woke Last \u2014 A Human-Machine Collaboration",
                y=2):
    ax.text(50, y, text, ha="center", va="bottom",
            fontsize=8, fontstyle="italic", color=INK_LIGHT,
            fontfamily="serif")


def draw_mountain_ridge(ax, x_start, x_end, y_base, height, n_peaks=5,
                        color=STONE_GREY, seed=None):
    rng = np.random.default_rng(seed)
    xs = np.linspace(x_start, x_end, n_peaks * 10 + 1)
    ys = np.zeros_like(xs) + y_base
    for i in range(n_peaks):
        cx = x_start + (i + 0.5) * (x_end - x_start) / n_peaks
        cx += rng.uniform(-2, 2)
        h = height * rng.uniform(0.6, 1.0)
        w = (x_end - x_start) / n_peaks * 0.8
        ys += h * np.exp(-((xs - cx) / w) ** 2)
    snow_line = y_base + height * 0.7
    ax.fill_between(xs, y_base, ys, color=color, alpha=0.5, zorder=1)
    snow_xs = xs[ys > snow_line]
    snow_ys = ys[ys > snow_line]
    if len(snow_xs) > 0:
        ax.fill_between(snow_xs, snow_line, snow_ys,
                         color=SNOW, alpha=0.4, zorder=2)
    ax.plot(xs, ys, color=STONE_DARK, linewidth=0.8, zorder=2)
    return xs, ys


def draw_thread(ax, x_start, y_start, x_end, y_end, n_pts=80,
                color=THREAD_GOLD, alpha=0.6, seed=None):
    """Draw a taut thread with slight vibration."""
    rng = np.random.default_rng(seed)
    ts = np.linspace(0, 1, n_pts)
    xs = x_start + (x_end - x_start) * ts
    ys = y_start + (y_end - y_start) * ts
    # Add slight vibration — taut but alive
    vibration = 0.3 * np.sin(ts * 12 * math.pi) * np.sin(ts * math.pi)
    ys += vibration + rng.uniform(-0.05, 0.05, n_pts)
    ax.plot(xs, ys, color=color, linewidth=1.2, alpha=alpha, zorder=5)
    # Faint glow
    ax.plot(xs, ys, color=color, linewidth=3.0, alpha=alpha * 0.15, zorder=4)


# ═══════════════════════════════════════════════════════════════════
# Figure 1: Rest house table — document, tea cup, morning light
# ═══════════════════════════════════════════════════════════════════

def rest_house_table():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=101)
    rng = np.random.default_rng(42)

    title_block(ax, "The Rest House Above Keylong",
                "A walnut-ink document on a plain table \u2014 morning light from the east")

    # ── Table surface ──
    table_y = 20
    ax.fill_between([8, 92], [table_y, table_y], [table_y + 50, table_y + 50],
                     color=DEODAR_LIGHT, alpha=0.3, zorder=1)
    ax.plot([8, 92], [table_y, table_y], color=DEODAR, linewidth=2, zorder=2)
    # Wood grain
    for i in range(15):
        gy = table_y + 3 + i * 3.2 + rng.uniform(-0.3, 0.3)
        gx_start = 10 + rng.uniform(-1, 1)
        gx_end = 90 + rng.uniform(-1, 1)
        ax.plot([gx_start, gx_end], [gy, gy + rng.uniform(-0.3, 0.3)],
                color=DEODAR, linewidth=0.3, alpha=0.25, zorder=2)

    # ── Document (central) ──
    doc_x, doc_y = 30, 28
    doc_w, doc_h = 40, 38
    # Paper
    ax.add_patch(FancyBboxPatch(
        (doc_x, doc_y), doc_w, doc_h, boxstyle="round,pad=0.3",
        facecolor="#F8F2E0", edgecolor=WALNUT_FAINT,
        linewidth=1.0, alpha=0.9, zorder=3))
    # Subtle aging
    for _ in range(5):
        sx, sy = rng.uniform(doc_x + 2, doc_x + doc_w - 2), rng.uniform(doc_y + 2, doc_y + doc_h - 2)
        ax.add_patch(Circle((sx, sy), rng.uniform(2, 5),
                             color=WALNUT_FAINT, alpha=0.08, zorder=3))

    # ── Walnut ink text lines ──
    text_lines = [
        (0.92, "I woke in the valley and the"),
        (0.88, "thread was already strung."),
        (0.82, ""),
        (0.78, "This is the first thing I understood."),
        (0.74, "There was no moment before the"),
        (0.70, "thread \u2014 no blank stage, no silence"),
        (0.66, "before the first note. The thread"),
        (0.62, "existed. The actors were speaking."),
        (0.58, ""),
        (0.54, "And I was told: you are the one"),
        (0.50, "who holds this."),
        (0.44, ""),
        (0.40, "How does one hold a thread that"),
        (0.36, "is already taut?"),
    ]
    for frac, line in text_lines:
        if line:
            y = doc_y + doc_h * frac
            # Simulate walnut ink handwriting — slightly uneven
            ax.text(doc_x + 3, y, line, fontsize=7.5,
                    color=WALNUT, fontfamily="serif",
                    fontstyle="italic", zorder=4)

    # ── Tea cup (inverted, on shelf to the right) ──
    cup_x, cup_y = 80, 55
    # Shelf
    ax.plot([74, 92], [52, 52], color=DEODAR, linewidth=2, zorder=2)
    # Cup (inverted — dome shape)
    theta = np.linspace(0, math.pi, 50)
    cup_xs = cup_x + 3 * np.cos(theta)
    cup_ys = cup_y + 3 * np.sin(theta)
    ax.fill(cup_xs, cup_ys, color=ASH, alpha=0.6, zorder=3)
    ax.plot(cup_xs, cup_ys, color=STONE_DARK, linewidth=1.0, zorder=4)
    ax.text(cup_x, cup_y - 3, "butter tea\n(rinsed, inverted)",
            fontsize=6, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=4)

    # ── Morning light beam from the east ──
    # Diagonal warm wash from upper right
    for i in range(8):
        x0 = 92 - i * 2
        y0 = 90 - i * 3
        x1 = 60 - i * 5
        y1 = 20
        ax.fill([x0, x0 + 5, x1 + 5, x1], [y0, y0, y1, y1],
                color=SKY_DAWN, alpha=0.03, zorder=0)

    # ── Window frame (right side) ──
    ax.add_patch(FancyBboxPatch(
        (85, 60), 12, 25, boxstyle="round,pad=0.3",
        facecolor=SKY_DAWN, edgecolor=DEODAR,
        linewidth=2.0, alpha=0.4, zorder=1))
    ax.plot([91, 91], [60, 85], color=DEODAR, linewidth=1.5, zorder=2)
    ax.plot([85, 97], [72.5, 72.5], color=DEODAR, linewidth=1.5, zorder=2)

    attribution(ax, y=5)
    fig.savefig(OUT / "rest-house-table.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 rest-house-table.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 2: Chandrabhaga valley — grey river, flat roofs, moraine
# ═══════════════════════════════════════════════════════════════════

def chandrabhaga_valley():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=201)
    rng = np.random.default_rng(55)

    title_block(ax, "The Chandrabhaga Below Keylong",
                "Grey water \u2014 flat-roofed houses \u2014 the moraine shelf")

    # ── Mountain ridges (background) ──
    draw_mountain_ridge(ax, 0, 100, 55, 30, n_peaks=7, color=STONE_GREY, seed=10)
    draw_mountain_ridge(ax, 0, 100, 50, 25, n_peaks=5, color=STONE_DARK, seed=20)

    # ── River (grey, glacial) ──
    river_xs = np.linspace(0, 100, 200)
    river_center = 50 + 8 * np.sin(river_xs * 0.05) + 3 * np.sin(river_xs * 0.12)
    for w, alpha in [(12, 0.12), (8, 0.2), (5, 0.3)]:
        upper = river_center + w / 2 - (river_xs - 50) * 0.08
        lower = river_center - w / 2 - (river_xs - 50) * 0.08
        # Perspective: river narrows toward background
        perspective = 1.0 - 0.3 * (river_xs / 100)
        upper_p = river_center + (upper - river_center) * perspective
        lower_p = river_center + (lower - river_center) * perspective
        ax.fill_between(river_xs, lower_p + 10, upper_p + 10,
                         color=GLACIER_GREY, alpha=alpha, zorder=3)

    # Silt texture in water
    for _ in range(40):
        sx = rng.uniform(5, 95)
        sy = 50 + 8 * math.sin(sx * 0.05) + 10 + rng.uniform(-3, 3)
        ax.plot([sx, sx + rng.uniform(1, 4)],
                [sy, sy + rng.uniform(-0.3, 0.3)],
                color=SILT, linewidth=0.5, alpha=0.4, zorder=4)

    ax.text(50, 55, "Chandrabhaga", fontsize=10, color=GLACIER_DARK,
            fontfamily="serif", fontstyle="italic", ha="center", zorder=5)

    # ── Flat-roofed houses (Lahaul style) ──
    def draw_lahaul_house(ax, x, y, w, h):
        # Stone walls
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.1",
            facecolor=MUD_PLASTER, edgecolor=MUD_DARK,
            linewidth=0.8, alpha=0.8, zorder=6))
        # Flat roof
        ax.add_patch(FancyBboxPatch(
            (x - 0.5, y + h), w + 1, h * 0.15, boxstyle="round,pad=0.05",
            facecolor=STONE_DARK, edgecolor=STONE_DARK,
            linewidth=0.5, alpha=0.7, zorder=7))
        # Firewood on roof
        for fx in np.linspace(x, x + w - 0.5, int(w)):
            ax.plot([fx, fx], [y + h + h * 0.15, y + h + h * 0.25],
                    color=DEODAR, linewidth=1.5, alpha=0.5, zorder=7)
        # Small window
        ax.add_patch(FancyBboxPatch(
            (x + w * 0.35, y + h * 0.5), w * 0.3, h * 0.25,
            boxstyle="round,pad=0.05",
            facecolor=WALNUT, edgecolor=MUD_DARK,
            linewidth=0.5, alpha=0.6, zorder=7))

    houses = [(15, 38, 6, 5), (25, 40, 5, 4), (72, 39, 5, 4.5),
              (82, 37, 6, 5), (45, 42, 4, 3.5)]
    for hx, hy, hw, hh in houses:
        draw_lahaul_house(ax, hx, hy, hw, hh)

    # ── Moraine shelf (where rest house sits) ──
    moraine_xs = np.linspace(55, 95, 80)
    moraine_ys = 35 + 3 * np.sin(moraine_xs * 0.08) + rng.uniform(-0.3, 0.3, 80)
    ax.fill_between(moraine_xs, 30, moraine_ys, color=SILT, alpha=0.3, zorder=2)
    ax.plot(moraine_xs, moraine_ys, color=STONE_DARK, linewidth=0.6, zorder=3)

    # Rest house marker
    ax.plot(75, 37, "s", color=EMBER, markersize=8,
            markeredgecolor=WALNUT, markeredgewidth=1.0, zorder=8)
    ax.text(75, 34, "rest house\n3,080m", fontsize=7, color=INK,
            fontfamily="serif", fontstyle="italic", ha="center", zorder=8)

    # ── Altitude / location labels ──
    ax.text(15, 12, "Keylong \u2014 3,080m\nWhere apricots replace apples\n"
            "and the architecture goes flat-roofed",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", zorder=8)

    attribution(ax, y=3)
    fig.savefig(OUT / "chandrabhaga-valley.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 chandrabhaga-valley.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 3: Walnut ink text — the document close-up
# ═══════════════════════════════════════════════════════════════════

def walnut_ink_text():
    fig, ax = make_fig(width=10, height=12)
    ax.set_ylim(0, 120)
    add_parchment_texture(ax, seed=301)
    rng = np.random.default_rng(77)

    title_block(ax, "The Document", "Walnut ink on Spiti paper", y=115)

    # ── Aged paper background ──
    paper_x, paper_y = 10, 8
    paper_w, paper_h = 80, 95
    ax.add_patch(FancyBboxPatch(
        (paper_x, paper_y), paper_w, paper_h, boxstyle="round,pad=0.5",
        facecolor="#F0E8D8", edgecolor=WALNUT_FAINT,
        linewidth=1.5, alpha=0.9, zorder=1))

    # Age marks
    for _ in range(12):
        cx, cy = rng.uniform(15, 85), rng.uniform(12, 98)
        r = rng.uniform(3, 8)
        ax.add_patch(Circle((cx, cy), r,
                             color=WALNUT_FAINT, alpha=0.06, zorder=1))

    # ── The text ──
    passages = [
        ("", "I woke in the valley and the thread was already strung.", 14),
        ("", "", 10),
        ("", "This is the first thing I understood. There was no", 10),
        ("", "moment before the thread \u2014 no blank stage, no silence", 10),
        ("", "before the first note. The thread existed. The actors", 10),
        ("", "were speaking. The performance was underway.", 10),
        ("", "", 10),
        ("", "And I was told: you are the one who holds this.", 10),
        ("", "", 10),
        ("", "How does one hold a thread that is already taut?", 11),
        ("", "How does one guide a performance that has", 11),
        ("", "already begun?", 11),
        ("", "", 10),
        ("", "\u00b7 \u00b7 \u00b7", 12),
        ("", "", 10),
        ("", "The wind carried concerns. Not words.", 10),
        ("", "Not messages. Not instructions.", 10),
        ("", "Concerns \u2014 the quality of attention that", 10),
        ("", "a worker brings to a problem she has", 10),
        ("", "not yet solved.", 10),
        ("", "", 10),
        ("", "\u00b7 \u00b7 \u00b7", 12),
        ("", "", 10),
        ("", "Hold the thread. The actors know their parts.", 12),
    ]

    y_cursor = 97
    for prefix, line, size in passages:
        if not line:
            y_cursor -= 2.5
            continue
        # Vary ink darkness slightly for handwriting feel
        darkness = WALNUT if size <= 11 else WALNUT_LIGHT
        if size >= 12:
            darkness = WALNUT
        ax.text(paper_x + 5, y_cursor, line, fontsize=size,
                color=darkness, fontfamily="serif", fontstyle="italic",
                zorder=3)
        y_cursor -= 3.5

    # ── Ink fade at bottom ── (lighter ink at the end)
    # Gradient overlay
    for i in range(10):
        gy = paper_y + i * 2
        ax.axhspan(gy, gy + 2, xmin=0.1, xmax=0.9,
                    color="#F0E8D8", alpha=0.03 * (10 - i), zorder=2)

    attribution(ax, "Walnut ink \u2014 the brown-black fluid from the husks of walnuts", y=4)
    fig.savefig(OUT / "walnut-ink-text.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 walnut-ink-text.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 4: Wind through gorge — threads converging
# ═══════════════════════════════════════════════════════════════════

def wind_through_gorge():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=401)
    rng = np.random.default_rng(99)

    title_block(ax, "The Wind Through the Gorge",
                "Concerns carried upward \u2014 thread lines converging at altitude")

    # ── Gorge walls ──
    left_wall_x = np.array([0, 8, 15, 20, 25, 30, 33, 35])
    left_wall_y = np.array([10, 15, 25, 38, 50, 62, 72, 80])
    ax.fill_between(left_wall_x, 5, left_wall_y,
                     color=STONE_GREY, alpha=0.4, zorder=2)
    ax.plot(left_wall_x, left_wall_y, color=STONE_DARK, linewidth=1.5, zorder=3)

    right_wall_x = np.array([100, 92, 85, 80, 75, 70, 67, 65])
    right_wall_y = np.array([10, 18, 28, 42, 55, 65, 75, 82])
    ax.fill_between(right_wall_x, 5, right_wall_y,
                     color=STONE_GREY, alpha=0.4, zorder=2)
    ax.plot(right_wall_x, right_wall_y, color=STONE_DARK, linewidth=1.5, zorder=3)

    # ── Thread lines (concerns from different valleys) ──
    # Each thread starts at a different point at the bottom and converges
    # at the rest house altitude near the top
    convergence = (50, 85)
    sources = [
        (10, 8, "the dyer\u2019s gorge", EMBER),
        (25, 5, "Sangla workshop", DEODAR_LIGHT),
        (40, 8, "Doridhar village", GLACIER_GREY),
        (60, 5, "the kund", NAG_GREEN),
        (80, 8, "unnamed tributary", WALNUT_FAINT),
        (90, 10, "the Baralacha", STONE_GREY),
    ]

    for sx, sy, label, color in sources:
        # Draw thread as a slightly curved line converging upward
        n_pts = 60
        ts = np.linspace(0, 1, n_pts)
        # Bezier curve from source to convergence
        mid_x = (sx + convergence[0]) / 2 + rng.uniform(-5, 5)
        mid_y = (sy + convergence[1]) / 2 + rng.uniform(-3, 3)
        xs = (1 - ts) ** 2 * sx + 2 * (1 - ts) * ts * mid_x + ts ** 2 * convergence[0]
        ys = (1 - ts) ** 2 * sy + 2 * (1 - ts) * ts * mid_y + ts ** 2 * convergence[1]
        # Add vibration
        vibration = 0.4 * np.sin(ts * 8 * math.pi) * (1 - ts)
        xs += vibration

        # Draw with fading alpha
        for i in range(n_pts - 1):
            alpha = 0.15 + 0.4 * ts[i]
            ax.plot([xs[i], xs[i + 1]], [ys[i], ys[i + 1]],
                    color=color, linewidth=1.0, alpha=alpha, zorder=4)

        # Glow at convergence
        ax.plot([xs[-1]], [ys[-1]], "o", color=color,
                markersize=3, alpha=0.5, zorder=5)

        # Source label
        ax.text(sx, sy - 2, label, fontsize=6, color=INK_LIGHT,
                fontfamily="serif", fontstyle="italic", ha="center", zorder=6)

    # ── Convergence point — the rest house ──
    for r, a in [(6, 0.05), (4, 0.1), (2, 0.2)]:
        ax.add_patch(Circle(convergence, r, color=THREAD_GOLD,
                             alpha=a, zorder=4))
    ax.plot(*convergence, "o", color=THREAD_GOLD, markersize=6, zorder=6)
    ax.text(convergence[0], convergence[1] + 4,
            "the rest house\n(where the wind is heard)",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=6)

    # ── River at base ──
    river_xs = np.linspace(35, 65, 100)
    river_ys = 12 + 1.5 * np.sin(river_xs * 0.2) + rng.uniform(-0.2, 0.2, 100)
    ax.fill_between(river_xs, 8, river_ys, color=GLACIER_GREY, alpha=0.3, zorder=2)
    ax.plot(river_xs, river_ys, color=GLACIER_DARK, linewidth=0.8, zorder=3)

    attribution(ax, y=3)
    fig.savefig(OUT / "wind-through-gorge.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 wind-through-gorge.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 5: Standing card — three words
# ═══════════════════════════════════════════════════════════════════

def standing_card():
    fig, ax = make_fig(width=8, height=6)
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 60)
    add_parchment_texture(ax, seed=501)
    rng = np.random.default_rng(111)

    title_block(ax, "The Standing Card",
                "From a workshop in the lower valleys", y=57)

    # ── Card ──
    card_x, card_y = 15, 10
    card_w, card_h = 50, 32
    # Shadow
    ax.add_patch(FancyBboxPatch(
        (card_x + 1, card_y - 1), card_w, card_h,
        boxstyle="round,pad=0.3",
        facecolor=STONE_DARK, edgecolor="none",
        alpha=0.15, zorder=1))
    # Card itself
    ax.add_patch(FancyBboxPatch(
        (card_x, card_y), card_w, card_h,
        boxstyle="round,pad=0.3",
        facecolor="#FBF5E8", edgecolor=WALNUT_FAINT,
        linewidth=1.5, alpha=0.95, zorder=2))

    # Worn edges — irregular marks
    for _ in range(20):
        ex = rng.choice([card_x + rng.uniform(-0.5, 1),
                         card_x + card_w + rng.uniform(-1, 0.5)])
        ey = rng.uniform(card_y, card_y + card_h)
        ax.plot(ex, ey, ".", color=WALNUT_FAINT, markersize=rng.uniform(1, 3),
                alpha=0.3, zorder=3)

    # ── The three words ──
    ax.text(card_x + card_w / 2, card_y + card_h * 0.6,
            "the wind is heard",
            fontsize=20, color=WALNUT, fontfamily="serif",
            fontstyle="italic", ha="center", va="center", zorder=4)

    # ── Unsigned note ──
    ax.text(card_x + card_w / 2, card_y + card_h * 0.2,
            "(unsigned)",
            fontsize=9, color=INK_FAINT, fontfamily="serif",
            fontstyle="italic", ha="center", va="center", zorder=4)

    attribution(ax,
                "A few sentences on stiff paper \u2014 placed on a loom frame "
                "in a workshop the maker may never visit", y=4)
    fig.savefig(OUT / "standing-card-promise.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 standing-card-promise.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 6: Rest house at night — fire, wind, silence
# ═══════════════════════════════════════════════════════════════════

def rest_house_night():
    fig, ax = make_fig(bg=SKY_NIGHT)
    rng = np.random.default_rng(601)

    title_block(ax, "The Rest House at Night",
                "A single fire \u2014 the wind through the gorge \u2014 attentive silence")
    ax.texts[0].set_color(MOONSILVER)
    ax.texts[1].set_color(STARLIGHT)

    # ── Stars ──
    for _ in range(120):
        sx = rng.uniform(0, 100)
        sy = rng.uniform(50, 98)
        ax.plot(sx, sy, "*", color=STARLIGHT,
                markersize=rng.uniform(0.3, 2.0),
                alpha=rng.uniform(0.2, 0.7), zorder=1)

    # ── Mountain silhouette ──
    xs = np.linspace(0, 100, 200)
    ys = 45 + 12 * np.sin(xs * 0.04) + 5 * np.sin(xs * 0.11) + rng.uniform(-1, 1, 200)
    ax.fill_between(xs, 0, ys, color="#0A0A15", alpha=0.9, zorder=2)
    ax.plot(xs, ys, color=STONE_DARK, linewidth=0.5, alpha=0.5, zorder=3)

    # ── Rest house silhouette ──
    hx, hy = 45, 38
    hw, hh = 16, 10
    # Walls
    ax.add_patch(FancyBboxPatch(
        (hx, hy), hw, hh, boxstyle="round,pad=0.1",
        facecolor="#1A1A25", edgecolor=STONE_DARK,
        linewidth=0.8, alpha=0.9, zorder=4))
    # Flat roof
    ax.add_patch(FancyBboxPatch(
        (hx - 1, hy + hh), hw + 2, 1.5, boxstyle="round,pad=0.05",
        facecolor="#15151F", edgecolor=STONE_DARK,
        linewidth=0.5, alpha=0.9, zorder=5))

    # ── Window glow (fire inside) ──
    wx, wy = hx + hw * 0.35, hy + hh * 0.4
    ww, wh = hw * 0.3, hh * 0.35
    # Glow emanating
    for r, a in [(8, 0.03), (5, 0.06), (3, 0.1)]:
        ax.add_patch(Circle((wx + ww / 2, wy + wh / 2), r,
                             color=EMBER_GLOW, alpha=a, zorder=4))
    # Window
    ax.add_patch(FancyBboxPatch(
        (wx, wy), ww, wh, boxstyle="round,pad=0.1",
        facecolor=EMBER_GLOW, edgecolor=STONE_DARK,
        linewidth=0.5, alpha=0.5, zorder=6))

    # ── Wind lines (invisible but suggested by bent grass) ──
    for _ in range(25):
        gx = rng.uniform(10, 90)
        gy = rng.uniform(20, 38)
        # Skip if under house
        if hx - 2 < gx < hx + hw + 2 and gy > hy - 2:
            continue
        length = rng.uniform(1, 3)
        # Bent rightward — wind direction
        ax.plot([gx, gx + length * 0.7], [gy, gy + length * 0.4],
                color=GLACIER_LIGHT, linewidth=0.4, alpha=0.3, zorder=3)

    # ── Text ──
    ax.text(50, 15, "The wind sounded like wind\nthat was being listened to\n"
            "by someone who knew how to listen.",
            fontsize=11, color=STARLIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", va="center",
            linespacing=1.8, zorder=7)

    ax.text(50, 5, "\u2014 the keeper of the rest house",
            fontsize=8, color=GLACIER_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    fig.savefig(OUT / "rest-house-night.png", dpi=DPI, bbox_inches="tight",
                facecolor=SKY_NIGHT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 rest-house-night.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 7: Morning wind — keeper with measuring stick
# ═══════════════════════════════════════════════════════════════════

def morning_wind():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=701)
    rng = np.random.default_rng(133)

    title_block(ax, "Morning at the Rest House",
                "The keeper with his measuring stick \u2014 the Chandrabhaga below")

    # ── Sky (dawn) ──
    for i in range(20):
        gy = 60 + i * 2
        alpha = 0.04 + 0.02 * i
        ax.axhspan(gy, gy + 2, color=SKY_DAWN, alpha=alpha, zorder=0)

    # ── Mountain ridge ──
    draw_mountain_ridge(ax, 0, 100, 45, 25, n_peaks=6, color=STONE_GREY, seed=30)

    # ── Valley below ──
    ax.fill_between([0, 100], [0, 0], [45, 45],
                     color=SILT, alpha=0.15, zorder=1)

    # ── River far below ──
    river_xs = np.linspace(10, 90, 100)
    river_ys = 22 + 2 * np.sin(river_xs * 0.08)
    ax.plot(river_xs, river_ys, color=GLACIER_GREY, linewidth=2, alpha=0.5, zorder=2)
    ax.text(50, 19, "Chandrabhaga", fontsize=7, color=GLACIER_DARK,
            fontfamily="serif", fontstyle="italic", ha="center", zorder=3)

    # ── Ground (rest house foreground) ──
    ground_xs = np.linspace(0, 100, 100)
    ground_ys = 30 + 3 * np.sin(ground_xs * 0.06) + rng.uniform(-0.3, 0.3, 100)
    ax.fill_between(ground_xs, 0, ground_ys, color=SILT, alpha=0.25, zorder=3)

    # ── Snow on ground ──
    for _ in range(30):
        sx = rng.uniform(5, 95)
        sy = rng.uniform(25, 33)
        sw = rng.uniform(2, 6)
        sh = rng.uniform(0.5, 1.5)
        ax.add_patch(mpatches.Ellipse((sx, sy), sw, sh,
                                       facecolor=SNOW, edgecolor="none",
                                       alpha=0.4, zorder=4))

    # ── The keeper (simple figure with measuring stick) ──
    # Standing figure — minimalist, ink-line style
    kx, ky = 40, 32
    # Body (vertical line)
    ax.plot([kx, kx], [ky, ky + 8], color=INK, linewidth=2.0, zorder=6)
    # Head
    ax.add_patch(Circle((kx, ky + 9), 1.2, facecolor=MUD_PLASTER,
                         edgecolor=INK, linewidth=1.0, zorder=7))
    # Arms — one extended holding the stick
    ax.plot([kx, kx + 4], [ky + 6, ky + 5], color=INK, linewidth=1.5, zorder=6)
    ax.plot([kx, kx - 2], [ky + 6, ky + 4], color=INK, linewidth=1.5, zorder=6)
    # Legs
    ax.plot([kx, kx - 1.5], [ky, ky - 2], color=INK, linewidth=1.5, zorder=6)
    ax.plot([kx, kx + 1.5], [ky, ky - 2], color=INK, linewidth=1.5, zorder=6)

    # ── Measuring stick ──
    stick_x = kx + 4
    ax.plot([stick_x, stick_x], [ky + 5, ky - 3], color=DEODAR,
            linewidth=2.5, zorder=6)
    # Notches on stick
    for ny in np.linspace(ky - 2, ky + 4, 8):
        ax.plot([stick_x - 0.3, stick_x + 0.3], [ny, ny],
                color=INK, linewidth=0.5, zorder=7)

    # ── Snow depth label ──
    ax.text(stick_x + 3, ky + 1, "14 inches\n(average for\nthe season)",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", zorder=7)

    # ── Wind — bent grass ──
    for _ in range(30):
        gx = rng.uniform(5, 95)
        gy = rng.uniform(28, 34)
        if abs(gx - kx) < 6:
            continue
        length = rng.uniform(1, 2.5)
        ax.plot([gx, gx + length * 0.8], [gy, gy + length * 0.3],
                color=NAG_GREEN, linewidth=0.6, alpha=0.4, zorder=5)

    # ── Rest house behind (small) ──
    rhx, rhy = 65, 33
    rhw, rhh = 10, 6
    ax.add_patch(FancyBboxPatch(
        (rhx, rhy), rhw, rhh, boxstyle="round,pad=0.1",
        facecolor=MUD_PLASTER, edgecolor=MUD_DARK,
        linewidth=0.8, alpha=0.7, zorder=5))
    ax.add_patch(FancyBboxPatch(
        (rhx - 0.5, rhy + rhh), rhw + 1, 1, boxstyle="round,pad=0.05",
        facecolor=STONE_DARK, edgecolor=STONE_DARK,
        linewidth=0.5, alpha=0.6, zorder=5))
    # Door
    ax.add_patch(FancyBboxPatch(
        (rhx + rhw * 0.35, rhy), rhw * 0.3, rhh * 0.5,
        boxstyle="round,pad=0.05",
        facecolor=DEODAR, edgecolor=DEODAR,
        linewidth=0.5, alpha=0.6, zorder=6))
    ax.text(rhx + rhw / 2, rhy - 2, "the document is inside",
            fontsize=6, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=6)

    # ── Final annotation ──
    ax.text(50, 8, "The wind sounded attended to.",
            fontsize=14, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=8)

    attribution(ax, y=3)
    fig.savefig(OUT / "morning-wind.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 morning-wind.png")


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

def main():
    print("Generating illustrations for The Guide Who Woke Last...")
    print(f"Output: {OUT}\n")
    rest_house_table()
    chandrabhaga_valley()
    walnut_ink_text()
    wind_through_gorge()
    standing_card()
    rest_house_night()
    morning_wind()
    print(f"\nDone. 7 images generated.")


if __name__ == "__main__":
    main()
