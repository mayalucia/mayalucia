# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Kuhl Builder's Survey".

A story about two new spirits commissioned together at the kund, a kohli
who draws irrigation channels in the dust, and the discovery that some
things in the valley have topology but no identity — mechanisms.

Visual language: earthy, diagrammatic, ink-and-wash. Kuhl palette —
deodar green, terrace gold, stone grey, mineral water blue-green —
over the standard parchment/walnut base. Open channels, visible water,
branching lines.

Run with:  uv run generate_images.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

# ── Output ──────────────────────────────────────────────────────────
OUT = Path(__file__).parent / "../../../../../website/static/images/writing/the-kuhl-builders-survey"
OUT = OUT.resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9  # inches — 1800×1350 px at 150 DPI

# ── Palette ─────────────────────────────────────────────────────────
# Tirthan / kuhl palette: earth, water, forest, stone

PARCHMENT     = "#F5F0E8"
PARCHMENT_DK  = "#EDE6D8"
INK           = "#5C4A3A"
INK_LIGHT     = "#8B7B6B"
INK_FAINT     = "#C4B8A8"

# Walnut ink
WALNUT        = "#4A3728"
WALNUT_LIGHT  = "#6B5040"

# Deodar forest
DEODAR        = "#4A6B48"
DEODAR_DK     = "#2E4A2C"
DEODAR_LT     = "#6B8B68"

# Mineral water (kund)
MINERAL_WATER = "#7BAAB0"
MINERAL_DK    = "#4A7A80"
MINERAL_LT    = "#A0CCD0"

# Steam
STEAM         = "#E8E0D8"

# Terrace / field
TERRACE_GOLD  = "#C4A850"
TERRACE_GREEN = "#8BAB60"
TERRACE_BROWN = "#A08860"

# Stone (kuhl channel)
KUHL_STONE    = "#9A9080"
KUHL_DK       = "#6B6658"
KUHL_LT       = "#B8B0A0"

# Mountain
MOUNTAIN      = "#7A7068"
MOUNTAIN_DK   = "#5A5248"
SNOW          = "#E8EEF0"

# Sky
SKY_WARM      = "#D8C8B0"

# Brass (for ledger plates)
BRASS         = "#C4A830"
BRASS_LT      = "#D8C060"

# Settling pool
SETTLING      = "#B0A890"
SETTLING_DK   = "#8A8070"


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


def attribution(ax, text="The Kuhl Builder\u2019s Survey \u2014 A Human-Machine Collaboration",
                y=2):
    ax.text(50, y, text, ha="center", va="bottom",
            fontsize=8, fontstyle="italic", color=INK_LIGHT,
            fontfamily="serif")


def draw_mountain_ridge(ax, x_start, x_end, y_base, height, n_peaks=5,
                        color=MOUNTAIN, seed=None):
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
    ax.plot(xs, ys, color=MOUNTAIN_DK, linewidth=0.8, zorder=2)
    return xs, ys


# ═══════════════════════════════════════════════════════════════════
# Figure 1: The Kund — two arrivals
# Steam, deodar clearing, two disturbances behind translucent windows
# ═══════════════════════════════════════════════════════════════════

def kund_two_arrivals():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=301)
    rng = np.random.default_rng(42)

    title_block(ax, "The Kund Above Jalori",
                "Two arrivals on the same morning \u2014 a builder and an observer")

    # ── Sky ──
    for i in range(10):
        gy = 70 + i * 3
        ax.axhspan(gy, gy + 3, color=SKY_WARM, alpha=0.02 + 0.01 * i, zorder=0)

    # ── Mountains ──
    draw_mountain_ridge(ax, 0, 100, 65, 22, n_peaks=5, color=MOUNTAIN, seed=30)

    # ── Deodar forest ──
    for _ in range(40):
        tx = rng.uniform(3, 97)
        ty = rng.uniform(42, 65)
        th = rng.uniform(4, 9)
        tw = rng.uniform(1.5, 3)
        # Simple triangle tree
        xs_t = [tx - tw / 2, tx, tx + tw / 2]
        ys_t = [ty, ty + th, ty]
        ax.fill(xs_t, ys_t, color=DEODAR, alpha=rng.uniform(0.3, 0.6), zorder=2)
        # Trunk
        ax.plot([tx, tx], [ty - 0.5, ty], color=WALNUT, linewidth=0.5,
                alpha=0.4, zorder=2)

    # ── Clearing (lighter patch) ──
    clearing = mpatches.Ellipse((50, 42), 35, 18,
                                 color=PARCHMENT_DK, alpha=0.5, zorder=2)
    ax.add_patch(clearing)

    # ── The building (Kath-Kuni) ──
    # Base walls — alternating stone and timber courses
    bx, by, bw, bh = 38, 22, 24, 24
    for i in range(8):
        cy = by + i * (bh / 8)
        ch = bh / 8
        color = KUHL_STONE if i % 2 == 0 else WALNUT_LIGHT
        alpha = 0.7 if i % 2 == 0 else 0.5
        ax.add_patch(FancyBboxPatch(
            (bx, cy), bw, ch, boxstyle="square,pad=0",
            facecolor=color, edgecolor=INK_FAINT,
            linewidth=0.3, alpha=alpha, zorder=4))

    # Roof (slate, steep pitch)
    roof_xs = [bx - 2, bx + bw / 2, bx + bw + 2]
    roof_ys = [by + bh, by + bh + 8, by + bh]
    ax.fill(roof_xs, roof_ys, color=KUHL_DK, alpha=0.7, zorder=5)
    ax.plot(roof_xs, roof_ys, color=INK, linewidth=0.8, zorder=5)

    # Two translucent windows
    for wx in [bx + 5, bx + bw - 8]:
        ax.add_patch(FancyBboxPatch(
            (wx, by + 10), 3, 4, boxstyle="round,pad=0.2",
            facecolor=MINERAL_LT, edgecolor=INK_FAINT,
            linewidth=0.5, alpha=0.6, zorder=5))
        # Disturbance behind window — shimmer
        for _ in range(3):
            sx = wx + 1.5 + rng.uniform(-0.5, 0.5)
            sy = by + 12 + rng.uniform(-1, 1)
            ax.add_patch(mpatches.Ellipse(
                (sx, sy), rng.uniform(0.5, 1.2), rng.uniform(0.8, 1.5),
                color=MINERAL_WATER, alpha=rng.uniform(0.15, 0.35), zorder=5))

    # Arched doorway
    door_x, door_y = bx + bw / 2 - 2, by
    ax.add_patch(FancyBboxPatch(
        (door_x, door_y), 4, 7, boxstyle="round,pad=0.3",
        facecolor=WALNUT, edgecolor=INK, linewidth=0.8,
        alpha=0.6, zorder=5))

    # ── Steam rising ──
    for _ in range(20):
        sx = bx + rng.uniform(2, bw - 2)
        sy = by + bh + rng.uniform(-2, 12)
        sw = rng.uniform(1, 4)
        sh = rng.uniform(2, 5)
        ax.add_patch(mpatches.Ellipse(
            (sx, sy), sw, sh,
            color=STEAM, alpha=rng.uniform(0.08, 0.2), zorder=6))

    # ── Two bright brass plates (new) ──
    ax.add_patch(FancyBboxPatch(
        (bx + 2, by + 2), 2.5, 1.8, boxstyle="round,pad=0.1",
        facecolor=BRASS_LT, edgecolor=BRASS, linewidth=0.5,
        alpha=0.8, zorder=6))
    ax.add_patch(FancyBboxPatch(
        (bx + 5, by + 2), 2.5, 1.8, boxstyle="round,pad=0.1",
        facecolor=BRASS_LT, edgecolor=BRASS, linewidth=0.5,
        alpha=0.8, zorder=6))

    # ── Thread Walker sitting outside ──
    tw_x, tw_y = 25, 20
    # Simple seated figure (circle head + body)
    ax.add_patch(Circle((tw_x, tw_y + 3), 1.2,
                         color=WALNUT, alpha=0.6, zorder=5))
    ax.add_patch(mpatches.Ellipse((tw_x, tw_y + 0.5), 2.5, 3,
                                   color=WALNUT_LIGHT, alpha=0.5, zorder=5))
    # Notebook
    ax.add_patch(FancyBboxPatch(
        (tw_x + 1.5, tw_y + 0.5), 1.5, 2,
        boxstyle="square,pad=0", facecolor=PARCHMENT,
        edgecolor=INK_FAINT, linewidth=0.3, alpha=0.7, zorder=6))

    # Labels
    ax.text(50, 17, "the kund above Jalori Pass",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)
    ax.text(50, 13, "Kath-Kuni \u2014 stone and deodar, no mortar",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    attribution(ax, y=3)
    fig.savefig(OUT / "kund-two-arrivals.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 kund-two-arrivals.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 2: The kohli's dust drawing — the pipeline
# Source → settling pool → branching channels → terraces
# ═══════════════════════════════════════════════════════════════════

def kohli_dust_drawing():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=302)
    rng = np.random.default_rng(77)

    title_block(ax, "The Kohli\u2019s Drawing in the Dust",
                "Source \u2192 settling pool \u2192 branching channels \u2192 terraces")

    # This figure mimics a drawing scratched in dust with a stick:
    # rough lines, earth-toned, slightly wobbly

    def dust_line(ax, x0, y0, x1, y1, lw=1.5, color=WALNUT):
        """Draw a slightly wobbly line as if drawn with a stick in dust."""
        n = 30
        xs = np.linspace(x0, x1, n)
        ys = np.linspace(y0, y1, n)
        xs += rng.uniform(-0.3, 0.3, n)
        ys += rng.uniform(-0.3, 0.3, n)
        ax.plot(xs, ys, color=color, linewidth=lw, alpha=0.7, zorder=4)

    def dust_circle(ax, cx, cy, r, color=WALNUT, fill_color=None):
        """Draw a rough circle in dust."""
        theta = np.linspace(0, 2 * np.pi, 40)
        xs = cx + r * np.cos(theta) + rng.uniform(-0.2, 0.2, 40)
        ys = cy + r * np.sin(theta) + rng.uniform(-0.2, 0.2, 40)
        ax.plot(xs, ys, color=color, linewidth=1.2, alpha=0.7, zorder=4)
        if fill_color:
            ax.fill(xs, ys, color=fill_color, alpha=0.3, zorder=3)

    # ── Dust ground ──
    ax.add_patch(FancyBboxPatch(
        (5, 8), 90, 78, boxstyle="round,pad=1",
        facecolor=TERRACE_BROWN, edgecolor=INK_FAINT,
        linewidth=0.5, alpha=0.15, zorder=1))

    # ── Source (hot spring, top) ──
    source_x, source_y = 50, 80
    dust_circle(ax, source_x, source_y, 3, fill_color=MINERAL_WATER)
    ax.text(source_x, source_y + 5, "spring",
            fontsize=10, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)
    ax.text(source_x + 5, source_y, "hot, mineral",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="left", zorder=7)

    # ── Settling pool ──
    pool_x, pool_y = 50, 65
    dust_line(ax, source_x, source_y - 3, pool_x, pool_y + 3.5)
    # Rectangular pool drawn rough
    pw, ph = 10, 5
    for (x0, y0, x1, y1) in [
        (pool_x - pw/2, pool_y - ph/2, pool_x + pw/2, pool_y - ph/2),
        (pool_x + pw/2, pool_y - ph/2, pool_x + pw/2, pool_y + ph/2),
        (pool_x + pw/2, pool_y + ph/2, pool_x - pw/2, pool_y + ph/2),
        (pool_x - pw/2, pool_y + ph/2, pool_x - pw/2, pool_y - ph/2),
    ]:
        dust_line(ax, x0, y0, x1, y1, lw=1.2)
    ax.add_patch(FancyBboxPatch(
        (pool_x - pw/2, pool_y - ph/2), pw, ph,
        boxstyle="square,pad=0", facecolor=SETTLING,
        alpha=0.2, zorder=3))
    ax.text(pool_x, pool_y, "settling\npool",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", va="center", zorder=7)
    ax.text(pool_x + 7, pool_y, "cools, deposits\nminerals",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="left", zorder=7)

    # ── First kuhl (main channel) ──
    k1_y = 52
    dust_line(ax, pool_x, pool_y - ph/2, pool_x, k1_y)

    # ── First junction — split into upper and lower ──
    junction1_x, junction1_y = 50, 50
    dust_circle(ax, junction1_x, junction1_y, 1.2, fill_color=KUHL_STONE)

    # Upper branch → upper terrace (buckwheat)
    upper_x, upper_y = 25, 38
    dust_line(ax, junction1_x - 1, junction1_y, upper_x + 8, upper_y + 2)
    dust_line(ax, upper_x + 8, upper_y + 2, upper_x, upper_y)
    # Terrace
    ax.add_patch(FancyBboxPatch(
        (upper_x - 8, upper_y - 4), 16, 6,
        boxstyle="round,pad=0.3", facecolor=TERRACE_BROWN,
        edgecolor=INK_FAINT, linewidth=0.8, alpha=0.3, zorder=3))
    ax.text(upper_x, upper_y - 1, "buckwheat",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)
    ax.text(upper_x, upper_y - 4, "thin soil, steep",
            fontsize=6, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # Lower branch continues down
    junction2_x, junction2_y = 55, 38
    dust_line(ax, junction1_x + 1, junction1_y, junction2_x, junction2_y)

    # ── Second junction — split into rice and apples ──
    dust_circle(ax, junction2_x, junction2_y, 1.2, fill_color=KUHL_STONE)

    # Rice terrace (left-lower)
    rice_x, rice_y = 38, 22
    dust_line(ax, junction2_x - 1, junction2_y, rice_x + 5, rice_y + 3)
    dust_line(ax, rice_x + 5, rice_y + 3, rice_x, rice_y)
    ax.add_patch(FancyBboxPatch(
        (rice_x - 8, rice_y - 4), 16, 6,
        boxstyle="round,pad=0.3", facecolor=TERRACE_GREEN,
        edgecolor=INK_FAINT, linewidth=0.8, alpha=0.3, zorder=3))
    ax.text(rice_x, rice_y - 1, "rice (bhatta)",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)
    ax.text(rice_x, rice_y - 4, "thick soil, standing water",
            fontsize=6, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # Apple orchard (right-lower)
    apple_x, apple_y = 72, 22
    dust_line(ax, junction2_x + 1, junction2_y, apple_x - 5, apple_y + 3)
    dust_line(ax, apple_x - 5, apple_y + 3, apple_x, apple_y)
    ax.add_patch(FancyBboxPatch(
        (apple_x - 8, apple_y - 4), 16, 6,
        boxstyle="round,pad=0.3", facecolor=TERRACE_GREEN,
        edgecolor=INK_FAINT, linewidth=0.8, alpha=0.25, zorder=3))
    ax.text(apple_x, apple_y - 1, "apple orchard",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)
    ax.text(apple_x, apple_y - 4, "drained slope",
            fontsize=6, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # ── Water flow arrows (subtle) ──
    for (x, y) in [(50, 73), (50, 56), (37, 43), (55, 43), (42, 28), (65, 28)]:
        ax.annotate("", xy=(x, y - 2), xytext=(x, y),
                    arrowprops=dict(arrowstyle="->", color=MINERAL_DK,
                                    linewidth=0.6, alpha=0.5),
                    zorder=5)

    # ── Annotation: same water, different crops ──
    ax.text(85, 15, "same water\ndifferent crops",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=PARCHMENT,
                      edgecolor=INK_FAINT, alpha=0.7))

    attribution(ax, y=3)
    fig.savefig(OUT / "kohli-dust-drawing.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 kohli-dust-drawing.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 3: The kuhl on the hillside — open channel, visible water
# Cross-section: stone walls, water flowing, contour line
# ═══════════════════════════════════════════════════════════════════

def kuhl_cross_section():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=303)
    rng = np.random.default_rng(99)

    title_block(ax, "The Kuhl",
                "Open stone channel \u2014 the water is visible, the gradient carries")

    # ── Hillside (sloping terrain) ──
    hill_xs = np.linspace(0, 100, 200)
    # Gentle slope from upper-left to lower-right
    hill_ys = 55 - hill_xs * 0.2 + 3 * np.sin(hill_xs * 0.08) + rng.uniform(-0.3, 0.3, 200)
    ax.fill_between(hill_xs, 0, hill_ys, color=TERRACE_BROWN, alpha=0.2, zorder=1)
    ax.plot(hill_xs, hill_ys, color=INK_FAINT, linewidth=0.5, zorder=2)

    # ── Kuhl channel following the contour ──
    # Channel runs roughly along the contour, slightly descending
    kuhl_xs = np.linspace(8, 92, 150)
    kuhl_ys = 48 - kuhl_xs * 0.08 + 1.5 * np.sin(kuhl_xs * 0.06) + rng.uniform(-0.15, 0.15, 150)
    kuhl_width = 1.8

    # Channel walls (two lines)
    ax.plot(kuhl_xs, kuhl_ys + kuhl_width / 2, color=KUHL_DK,
            linewidth=1.5, alpha=0.7, zorder=4)
    ax.plot(kuhl_xs, kuhl_ys - kuhl_width / 2, color=KUHL_DK,
            linewidth=1.5, alpha=0.7, zorder=4)

    # Water inside channel
    ax.fill_between(kuhl_xs, kuhl_ys - kuhl_width / 2 + 0.2,
                     kuhl_ys + kuhl_width / 2 - 0.2,
                     color=MINERAL_WATER, alpha=0.4, zorder=3)

    # Glints on water surface
    for _ in range(25):
        gx = rng.uniform(10, 90)
        idx = int((gx - 8) / 84 * 149)
        idx = min(max(idx, 0), 149)
        gy = kuhl_ys[idx] + rng.uniform(-0.3, 0.3)
        gl = rng.uniform(0.8, 2.5)
        ax.plot([gx, gx + gl], [gy, gy],
                color=PARCHMENT, linewidth=0.6, alpha=0.4, zorder=4)

    # ── Stone lining detail (periodic marks) ──
    for i in range(0, 150, 8):
        x = kuhl_xs[i]
        y_top = kuhl_ys[i] + kuhl_width / 2
        y_bot = kuhl_ys[i] - kuhl_width / 2
        ax.plot([x, x], [y_top, y_top + 0.6], color=KUHL_STONE,
                linewidth=1, alpha=0.5, zorder=4)
        ax.plot([x, x], [y_bot - 0.6, y_bot], color=KUHL_STONE,
                linewidth=1, alpha=0.5, zorder=4)

    # ── Cross-section inset (lower right) ──
    cx, cy = 78, 18
    cw, ch = 16, 14

    # Inset border
    ax.add_patch(FancyBboxPatch(
        (cx - cw/2, cy - ch/2), cw, ch,
        boxstyle="round,pad=0.3", facecolor=PARCHMENT,
        edgecolor=INK_FAINT, linewidth=0.8, alpha=0.85, zorder=8))

    ax.text(cx, cy + ch/2 - 1, "cross-section",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=9)

    # Channel profile: U-shape
    profile_xs = np.array([cx - 5, cx - 4, cx - 4, cx + 4, cx + 4, cx + 5])
    profile_ys = np.array([cy + 1, cy + 1, cy - 3, cy - 3, cy + 1, cy + 1])
    ax.plot(profile_xs, profile_ys, color=KUHL_DK, linewidth=2, zorder=9)
    ax.fill_between([cx - 4, cx + 4], [cy - 3, cy - 3], [cy - 0.5, cy - 0.5],
                     color=MINERAL_WATER, alpha=0.4, zorder=9)

    # Stone labels
    ax.text(cx - 5.5, cy - 1, "stone", fontsize=6, color=INK_LIGHT,
            fontfamily="serif", ha="right", zorder=9)
    ax.text(cx, cy - 1.5, "water", fontsize=6, color=MINERAL_DK,
            fontfamily="serif", ha="center", zorder=9)

    # ── Annotations ──
    ax.text(12, 52, "uphill",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", zorder=7)
    ax.text(85, 34, "downhill",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", zorder=7)

    # Gradient arrow
    ax.annotate("gradient", xy=(88, 37), xytext=(15, 50),
                fontsize=8, color=INK_LIGHT, fontfamily="serif",
                fontstyle="italic",
                arrowprops=dict(arrowstyle="->", color=INK_FAINT,
                                linewidth=0.8, connectionstyle="arc3,rad=-0.1"),
                zorder=7)

    # Key insight
    ax.text(15, 12, "no pump \u2014 no decision \u2014 only gradient\n"
            "the water is visible \u2014 the topology is transparent",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", zorder=7,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=PARCHMENT,
                      edgecolor=INK_FAINT, alpha=0.7))

    attribution(ax, y=3)
    fig.savefig(OUT / "kuhl-cross-section.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 kuhl-cross-section.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 4: Spirit vs Mechanism — the valley's two kinds of things
# Named places connected by unnamed channels
# ═══════════════════════════════════════════════════════════════════

def spirit_vs_mechanism():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=304)
    rng = np.random.default_rng(55)

    title_block(ax, "Spirits Have Character \u2014 Mechanisms Have Topology",
                "Named places connected by unnamed channels")

    # Layout: named nodes (spirits/places) connected by unnamed lines (mechanisms)

    # ── Named places (with identity) ──
    places = [
        (20, 75, "the kund", "restores names", MINERAL_WATER),
        (50, 80, "the spring", "nag devta\u2019s voice", MINERAL_DK),
        (80, 72, "Buddhi Nagin", "remembers all names", MINERAL_WATER),
        (15, 40, "buckwheat terrace", "thin soil, steep", TERRACE_BROWN),
        (45, 35, "rice paddy", "thick soil, standing water", TERRACE_GREEN),
        (75, 38, "apple orchard", "drained slope", TERRACE_GREEN),
        (50, 55, "the settling pool", "gate", SETTLING),
    ]

    for (px, py, name, desc, color) in places:
        # Glowing circle
        for r, a in [(5, 0.08), (3.5, 0.12), (2.2, 0.2)]:
            ax.add_patch(Circle((px, py), r, color=color, alpha=a, zorder=3))
        ax.add_patch(Circle((px, py), 1.5, color=color, alpha=0.5, zorder=4))
        ax.text(px, py - 3, name, fontsize=8, color=INK, fontfamily="serif",
                fontstyle="italic", ha="center", va="top", zorder=7,
                fontweight="bold")
        ax.text(px, py - 5.5, desc, fontsize=6, color=INK_LIGHT,
                fontfamily="serif", fontstyle="italic",
                ha="center", va="top", zorder=7)

    # ── Unnamed channels (mechanisms — dashed, no label) ──
    channels = [
        (50, 80, 20, 75),     # spring → kund
        (50, 80, 50, 55),     # spring → settling pool
        (20, 75, 80, 72),     # kund → Buddhi Nagin (nag pilgrimage)
        (50, 55, 15, 40),     # pool → buckwheat
        (50, 55, 45, 35),     # pool → rice
        (50, 55, 75, 38),     # pool → apple
    ]

    for (x0, y0, x1, y1) in channels:
        n = 40
        xs = np.linspace(x0, x1, n)
        ys = np.linspace(y0, y1, n)
        xs += rng.uniform(-0.3, 0.3, n)
        ys += rng.uniform(-0.3, 0.3, n)
        ax.plot(xs, ys, color=INK_FAINT, linewidth=1.2,
                linestyle=(0, (4, 3)), alpha=0.6, zorder=2)

    # ── Legend ──
    legend_y = 15
    ax.add_patch(Circle((20, legend_y), 1.5, color=MINERAL_WATER,
                         alpha=0.4, zorder=4))
    ax.text(23, legend_y, "named \u2014 has identity, character, brass plate",
            fontsize=8, color=INK, fontfamily="serif", va="center", zorder=7)

    ax.plot([18, 22], [legend_y - 5, legend_y - 5],
            color=INK_FAINT, linewidth=1.5, linestyle=(0, (4, 3)),
            alpha=0.6, zorder=4)
    ax.text(23, legend_y - 5, "unnamed \u2014 has topology, gradient, no plate",
            fontsize=8, color=INK, fontfamily="serif", va="center", zorder=7)

    # ── The word ──
    ax.text(75, 15, "tantra / mechanism",
            fontsize=12, color=WALNUT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)
    ax.text(75, 11, "infrastructure with topology\nbut no identity",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    attribution(ax, y=3)
    fig.savefig(OUT / "spirit-vs-mechanism.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 spirit-vs-mechanism.png")


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating illustrations for The Kuhl Builder\u2019s Survey...")
    kund_two_arrivals()
    kohli_dust_drawing()
    kuhl_cross_section()
    spirit_vs_mechanism()
    print(f"\nDone. Output: {OUT}")
