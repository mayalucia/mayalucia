# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Weaver's Loom".

A story about a weaver in Nahin — above Gushaini, above Pekhri, at the
end of a trail with no road — who discovers the difference between sitting
beside a loom and weaving. The three preparations (eye, thread, deposit),
the bees in the Kath-Kuni walls, the serpentine Tirthan viewed from above.

Visual language: parchment/walnut base. Loom palette — indigo weft,
slate-grey warp, deodar wood, Kath-Kuni stone courses, wild honey gold,
bee clay. Hand-drawn jitter throughout.

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
OUT = Path(__file__).parent / "../../../../../website/static/images/writing/the-weavers-loom"
OUT = OUT.resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9  # inches — 1800×1350 px at 150 DPI

# ── Palette ─────────────────────────────────────────────────────────
PARCHMENT     = "#F5F0E8"
PARCHMENT_DK  = "#EDE6D8"
INK           = "#5C4A3A"
INK_LIGHT     = "#8B7B6B"
INK_FAINT     = "#C4B8A8"

WALNUT        = "#4A3728"
WALNUT_LIGHT  = "#6B5040"

# Deodar / forest
DEODAR        = "#4A6B48"
DEODAR_DK     = "#2E4A2C"
DEODAR_LT     = "#6B8B68"

# Kath-Kuni stone and timber
STONE         = "#9A9080"
STONE_DK      = "#6B6658"
STONE_LT      = "#B8B0A0"
TIMBER        = "#8B6B4A"
TIMBER_DK     = "#6B4A30"

# Loom / textile
WARP_GREY     = "#A0A098"
INDIGO        = "#3A4A6B"
INDIGO_LT     = "#5A6A8B"

# Water
WATER_WHITE   = "#E8EEF0"
WATER_EMERALD = "#4A8B6B"
WATER_EMERALD_LT = "#70AB8B"

# Mountain
MOUNTAIN      = "#7A7068"
MOUNTAIN_DK   = "#5A5248"
SNOW          = "#E8EEF0"

# Sky
SKY_WARM      = "#D8C8B0"

# Bee / honey
HONEY         = "#D4A840"
HONEY_LT      = "#E8C060"
BEE_CLAY      = "#C4A878"

# Brass
BRASS         = "#C4A830"
BRASS_LT      = "#D8C060"

# Charcoal (for slate marks)
CHARCOAL      = "#4A4A48"
CHARCOAL_LT   = "#6A6A68"
SLATE_BG      = "#7A7A78"
SLATE_LT      = "#9A9A98"

# Flour
FLOUR         = "#F0EAE0"


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


def attribution(ax, text="The Weaver\u2019s Loom \u2014 A Human-Machine Collaboration",
                y=2):
    ax.text(50, y, text, ha="center", va="bottom",
            fontsize=8, fontstyle="italic", color=INK_LIGHT,
            fontfamily="serif")


def wobbly_line(ax, x0, y0, x1, y1, rng, lw=1.5, color=WALNUT,
                alpha=0.7, n=30, zorder=4):
    xs = np.linspace(x0, x1, n)
    ys = np.linspace(y0, y1, n)
    xs += rng.uniform(-0.25, 0.25, n)
    ys += rng.uniform(-0.25, 0.25, n)
    ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha, zorder=zorder)


def wobbly_circle(ax, cx, cy, r, rng, color=WALNUT, fill_color=None,
                  lw=1.2, alpha=0.7, zorder=4):
    theta = np.linspace(0, 2 * np.pi, 40)
    xs = cx + r * np.cos(theta) + rng.uniform(-0.15, 0.15, 40)
    ys = cy + r * np.sin(theta) + rng.uniform(-0.15, 0.15, 40)
    ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha, zorder=zorder)
    if fill_color:
        ax.fill(xs, ys, color=fill_color, alpha=0.3, zorder=zorder - 1)


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


def draw_kath_kuni_wall(ax, bx, by, bw, bh, n_courses=8, zorder=4):
    """Draw alternating stone and timber courses."""
    for i in range(n_courses):
        cy = by + i * (bh / n_courses)
        ch = bh / n_courses
        color = STONE if i % 2 == 0 else TIMBER
        alpha = 0.7 if i % 2 == 0 else 0.5
        ax.add_patch(FancyBboxPatch(
            (bx, cy), bw, ch, boxstyle="square,pad=0",
            facecolor=color, edgecolor=INK_FAINT,
            linewidth=0.3, alpha=alpha, zorder=zorder))


# ═══════════════════════════════════════════════════════════════════
# Figure 1: The serpentine Tirthan from above
# White rapids, emerald pools, side-streams, road scars
# ═══════════════════════════════════════════════════════════════════

def serpentine_tirthan():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=401)
    rng = np.random.default_rng(42)

    title_block(ax, "The Tirthan from Above Nahin",
                "White where the gradient is steep, emerald where the water holds still")

    # ── Sky wash ──
    for i in range(8):
        gy = 75 + i * 3
        ax.axhspan(gy, gy + 3, color=SKY_WARM, alpha=0.02 + 0.008 * i, zorder=0)

    # ── Mountains (distant) ──
    draw_mountain_ridge(ax, 0, 100, 72, 20, n_peaks=6, color=MOUNTAIN, seed=40)

    # ── Hillside (green, sloping) ──
    hill_xs = np.linspace(0, 100, 200)
    hill_ys = 70 - 0.15 * hill_xs + 2 * np.sin(hill_xs * 0.05)
    ax.fill_between(hill_xs, 8, hill_ys, color=DEODAR_LT, alpha=0.15, zorder=1)

    # ── Deodar forest (sparse) ──
    for _ in range(35):
        tx = rng.uniform(3, 97)
        ty = rng.uniform(25, 65)
        th = rng.uniform(3, 7)
        tw = rng.uniform(1.2, 2.5)
        xs_t = [tx - tw / 2, tx, tx + tw / 2]
        ys_t = [ty, ty + th, ty]
        ax.fill(xs_t, ys_t, color=DEODAR, alpha=rng.uniform(0.15, 0.35), zorder=2)

    # ── The serpentine river ──
    # Main channel: S-curve from upper-right to lower-left
    t = np.linspace(0, 1, 300)
    river_x = 80 - 55 * t + 12 * np.sin(t * 5.5 * np.pi)
    river_y = 70 - 55 * t + 4 * np.cos(t * 3.7 * np.pi)

    # River width varies — wider at pools, narrower at rapids
    widths = 1.2 + 0.8 * np.sin(t * 8 * np.pi) ** 2

    # Draw river with alternating white/emerald
    for i in range(len(t) - 1):
        x0, y0 = river_x[i], river_y[i]
        x1, y1 = river_x[i + 1], river_y[i + 1]
        w = widths[i]

        # Gradient steepness → color
        dy = abs(river_y[i] - river_y[min(i + 5, len(t) - 1)])
        if dy > 1.2:
            color = WATER_WHITE
            alpha = 0.8
        else:
            color = WATER_EMERALD
            alpha = 0.7

        # Draw as thick line segment
        dx = x1 - x0
        dy_seg = y1 - y0
        length = max(np.sqrt(dx**2 + dy_seg**2), 0.01)
        nx, ny = -dy_seg / length, dx / length

        xs = [x0 - nx * w, x0 + nx * w, x1 + nx * w, x1 - nx * w]
        ys = [y0 - ny * w, y0 + ny * w, y1 + ny * w, y1 - ny * w]
        ax.fill(xs, ys, color=color, alpha=alpha, zorder=3)

    # River outline
    ax.plot(river_x, river_y, color=INK_FAINT, linewidth=0.4, alpha=0.5, zorder=4)

    # ── Side tributaries (smaller serpents) ──
    for (start_x, start_y, join_idx, seed_t) in [
        (92, 50, 60, 101), (10, 55, 150, 102), (85, 35, 120, 103),
        (8, 38, 200, 104),
    ]:
        join_x, join_y = river_x[join_idx], river_y[join_idx]
        tt = np.linspace(0, 1, 50)
        tx = start_x + (join_x - start_x) * tt + 3 * np.sin(tt * 3 * np.pi)
        ty = start_y + (join_y - start_y) * tt + 2 * np.cos(tt * 2.5 * np.pi)
        ax.plot(tx, ty, color=WATER_EMERALD_LT, linewidth=1.2,
                alpha=0.5, zorder=3)

    # ── Road scars (white marks on eastern ridge) ──
    for _ in range(6):
        sx = rng.uniform(75, 92)
        sy = rng.uniform(40, 60)
        sl = rng.uniform(2, 5)
        sa = rng.uniform(-0.3, 0.3)
        ax.plot([sx, sx + sl * np.cos(sa)], [sy, sy + sl * np.sin(sa)],
                color=PARCHMENT, linewidth=2.5, alpha=0.6, zorder=4)

    ax.text(88, 62, "road\nscars", fontsize=7, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", ha="center", zorder=7)

    # ── Nahin (small cluster, high) ──
    for dx in [-1.5, 0, 1.8]:
        bx = 30 + dx * 3
        by = 60 + rng.uniform(-1, 1)
        draw_kath_kuni_wall(ax, bx, by, 3, 3, n_courses=4, zorder=5)
    ax.text(30, 57, "Nahin", fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # ── Gushaini (lower) ──
    ax.text(25, 18, "Gushaini", fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # ── Trail (dotted path uphill) ──
    trail_t = np.linspace(0, 1, 80)
    trail_x = 25 + 5 * trail_t + 2 * np.sin(trail_t * 4 * np.pi)
    trail_y = 20 + 38 * trail_t
    ax.plot(trail_x, trail_y, color=WALNUT_LIGHT, linewidth=0.8,
            linestyle=(0, (3, 4)), alpha=0.5, zorder=4)

    # ── Toward Hans Kund label ──
    ax.text(70, 72, "\u2192 Hans Kund", fontsize=7, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", zorder=7)

    attribution(ax, y=3)
    fig.savefig(OUT / "serpentine-tirthan.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 serpentine-tirthan.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 2: Kath-Kuni house with bee-houses in the wall
# Alternating stone and timber, clay cavities, bees returning
# ═══════════════════════════════════════════════════════════════════

def kath_kuni_bees():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=402)
    rng = np.random.default_rng(55)

    title_block(ax, "The Bees in the Wall",
                "Clay houses within the Kath-Kuni \u2014 the bees return each spring")

    # ── The house (large, detailed Kath-Kuni) ──
    bx, by, bw, bh = 25, 15, 50, 50

    for i in range(12):
        cy = by + i * (bh / 12)
        ch = bh / 12
        is_stone = i % 2 == 0
        color = STONE if is_stone else TIMBER
        alpha = 0.65 if is_stone else 0.5
        ax.add_patch(FancyBboxPatch(
            (bx, cy), bw, ch, boxstyle="square,pad=0",
            facecolor=color, edgecolor=INK_FAINT,
            linewidth=0.4, alpha=alpha, zorder=4))

        # Clay bee-houses in the timber courses (every other timber course)
        if not is_stone and i % 4 == 1:
            for j in range(4):
                bee_x = bx + 5 + j * (bw - 10) / 3.5
                bee_y = cy + ch * 0.2
                bee_w = 3
                bee_h = ch * 0.6
                ax.add_patch(FancyBboxPatch(
                    (bee_x, bee_y), bee_w, bee_h,
                    boxstyle="round,pad=0.15",
                    facecolor=BEE_CLAY, edgecolor=WALNUT_LIGHT,
                    linewidth=0.5, alpha=0.7, zorder=5))
                # Bee entry hole
                ax.add_patch(Circle((bee_x + bee_w / 2, bee_y + bee_h / 2),
                                     0.3, color=WALNUT, alpha=0.6, zorder=6))

    # ── Roof ──
    roof_xs = [bx - 3, bx + bw / 2, bx + bw + 3]
    roof_ys = [by + bh, by + bh + 10, by + bh]
    ax.fill(roof_xs, roof_ys, color=STONE_DK, alpha=0.6, zorder=5)
    ax.plot(roof_xs, roof_ys, color=INK, linewidth=0.8, zorder=5)

    # Firewood on roof
    for _ in range(8):
        fx = rng.uniform(bx + 5, bx + bw - 5)
        fy = by + bh + rng.uniform(0.5, 4)
        fl = rng.uniform(2, 4)
        ax.plot([fx, fx + fl], [fy, fy + rng.uniform(-0.3, 0.3)],
                color=TIMBER_DK, linewidth=1.5, alpha=0.4, zorder=6)

    # ── Window (east-facing, light coming through) ──
    win_x, win_y = bx + bw / 2 - 3, by + bh * 0.6
    ax.add_patch(FancyBboxPatch(
        (win_x, win_y), 6, 5, boxstyle="round,pad=0.2",
        facecolor=SKY_WARM, edgecolor=INK_FAINT,
        linewidth=0.8, alpha=0.6, zorder=6))
    # Light rays from window
    for i in range(5):
        angle = -0.4 + i * 0.2
        lx = win_x + 3 + 8 * np.cos(angle)
        ly = win_y + 2.5 + 8 * np.sin(angle)
        ax.plot([win_x + 3, lx], [win_y + 2.5, ly],
                color=HONEY_LT, linewidth=0.5, alpha=0.15, zorder=3)

    # ── Bees (small marks returning to the wall) ──
    for _ in range(20):
        bx_b = rng.uniform(30, 70)
        by_b = rng.uniform(by + 10, by + bh - 5)
        # Flight path (slight curve)
        path_len = rng.uniform(5, 15)
        angle = rng.uniform(-np.pi, np.pi)
        bx_start = bx_b + path_len * np.cos(angle)
        by_start = by_b + path_len * np.sin(angle)
        t = np.linspace(0, 1, 15)
        fx = bx_start + (bx_b - bx_start) * t
        fy = by_start + (by_b - by_start) * t + 1.5 * np.sin(t * 3 * np.pi)
        ax.plot(fx, fy, color=HONEY, linewidth=0.3, alpha=0.3, zorder=7)
        # Bee body (tiny dot at end)
        ax.add_patch(Circle((bx_b, by_b), 0.25, color=HONEY,
                             alpha=0.5, zorder=7))

    # ── Labels ──
    ax.text(bx - 5, by + bh * 0.35, "clay\nbee-\nhouses",
            fontsize=8, color=INK, fontfamily="serif",
            fontstyle="italic", ha="right", zorder=7)

    # Arrow to bee-house
    ax.annotate("", xy=(bx + 2, by + bh * 0.28), xytext=(bx - 3, by + bh * 0.32),
                arrowprops=dict(arrowstyle="->", color=INK_FAINT,
                                linewidth=0.6), zorder=7)

    ax.text(50, 10, "they come when the apple blossom opens\n"
            "the honey tells you what kind of year the mountain had",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    attribution(ax, y=3)
    fig.savefig(OUT / "kath-kuni-bees.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 kath-kuni-bees.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 3: The idle loom
# Strung warp, shuttle resting, weaver sitting beside (not at) it
# ═══════════════════════════════════════════════════════════════════

def idle_loom():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=403)
    rng = np.random.default_rng(66)

    title_block(ax, "The Idle Loom",
                "Strung but not woven \u2014 the weaver sits beside, not at")

    # ── Loom frame (vertical, deodar wood) ──
    loom_x, loom_y = 45, 18
    loom_w, loom_h = 22, 55

    # Vertical posts
    for dx in [0, loom_w]:
        ax.add_patch(FancyBboxPatch(
            (loom_x + dx - 0.8, loom_y), 1.6, loom_h,
            boxstyle="square,pad=0",
            facecolor=TIMBER, edgecolor=INK_FAINT,
            linewidth=0.5, alpha=0.6, zorder=4))

    # Top and bottom beams
    for dy in [0, loom_h - 1.5]:
        ax.add_patch(FancyBboxPatch(
            (loom_x - 1, loom_y + dy), loom_w + 2, 1.5,
            boxstyle="square,pad=0",
            facecolor=TIMBER_DK, edgecolor=INK_FAINT,
            linewidth=0.5, alpha=0.6, zorder=5))

    # ── Warp threads (vertical, evenly spaced) ──
    n_threads = 16
    for i in range(n_threads):
        tx = loom_x + 2 + i * (loom_w - 4) / (n_threads - 1)
        # Slight irregularity in position
        tx += rng.uniform(-0.15, 0.15)
        ax.plot([tx, tx], [loom_y + 2, loom_y + loom_h - 2],
                color=WARP_GREY, linewidth=0.8,
                alpha=0.6, zorder=4)

    # Stone weights at bottom
    for i in range(n_threads):
        tx = loom_x + 2 + i * (loom_w - 4) / (n_threads - 1)
        ax.add_patch(Circle((tx, loom_y - 1), 0.6,
                             color=STONE, alpha=0.5, zorder=4))

    # ── Shuttle resting on bench (not in loom) ──
    bench_x, bench_y = loom_x + loom_w + 4, loom_y + 5
    ax.add_patch(FancyBboxPatch(
        (bench_x, bench_y), 8, 3, boxstyle="round,pad=0.2",
        facecolor=TIMBER, edgecolor=INK_FAINT,
        linewidth=0.5, alpha=0.4, zorder=3))
    # Shuttle (walnut stick with indigo yarn)
    ax.add_patch(FancyBboxPatch(
        (bench_x + 1, bench_y + 0.8), 6, 1.2,
        boxstyle="round,pad=0.2",
        facecolor=WALNUT_LIGHT, edgecolor=INK_FAINT,
        linewidth=0.4, alpha=0.7, zorder=5))
    # Yarn wound around shuttle
    for j in range(8):
        yy = bench_x + 1.5 + j * 0.6
        ax.plot([yy, yy], [bench_y + 0.9, bench_y + 1.9],
                color=INDIGO, linewidth=0.8, alpha=0.5, zorder=6)

    ax.text(bench_x + 4, bench_y - 1.5, "shuttle\n(resting)",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # ── Window behind loom (light through warp) ──
    win_x, win_y = loom_x + 3, loom_y + loom_h + 2
    ax.add_patch(FancyBboxPatch(
        (win_x, win_y), loom_w - 6, 8, boxstyle="round,pad=0.3",
        facecolor=SKY_WARM, edgecolor=INK_FAINT,
        linewidth=0.8, alpha=0.4, zorder=2))
    ax.text(loom_x + loom_w / 2, win_y + 4, "east window",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # Light shadows on floor from warp
    for i in range(n_threads):
        tx = loom_x + 2 + i * (loom_w - 4) / (n_threads - 1)
        ax.plot([tx, tx - 1.5], [loom_y + 2, loom_y - 3],
                color=INK_FAINT, linewidth=0.5, alpha=0.3, zorder=2)

    # ── Weaver sitting BESIDE the loom (not at it) ──
    weaver_x = loom_x - 10
    weaver_y = loom_y + 15
    # Simple seated figure
    ax.add_patch(Circle((weaver_x, weaver_y + 4), 1.8,
                         color=WALNUT, alpha=0.5, zorder=5))
    ax.add_patch(mpatches.Ellipse((weaver_x, weaver_y + 1), 3.5, 4,
                                   color=WALNUT_LIGHT, alpha=0.4, zorder=5))
    # Cold tea cup
    ax.add_patch(FancyBboxPatch(
        (weaver_x + 2.5, weaver_y), 1.5, 1.2,
        boxstyle="round,pad=0.1",
        facecolor=STONE_LT, edgecolor=INK_FAINT,
        linewidth=0.3, alpha=0.5, zorder=6))

    # Annotations
    ax.text(weaver_x, weaver_y - 3, "the weaver\n(beside, not at)",
            fontsize=8, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # No cloth on loom — emphasized
    ax.text(loom_x + loom_w / 2, loom_y + loom_h / 2,
            "no cloth\nno weft\nonly warp",
            fontsize=10, color=INK_FAINT, fontfamily="serif",
            fontstyle="italic", ha="center", va="center",
            alpha=0.6, zorder=6)

    attribution(ax, y=3)
    fig.savefig(OUT / "idle-loom.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 idle-loom.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 4: The three preparations — charcoal on slate
# Three circles: eye, thread, deposit
# ═══════════════════════════════════════════════════════════════════

def three_preparations():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=404)
    rng = np.random.default_rng(77)

    title_block(ax, "The Three Preparations",
                "Charcoal on slate \u2014 eye, thread, deposit")

    # ── Slate background ──
    ax.add_patch(FancyBboxPatch(
        (10, 15), 80, 65, boxstyle="round,pad=0.5",
        facecolor=SLATE_BG, edgecolor=STONE_DK,
        linewidth=1.5, alpha=0.25, zorder=1))

    # ── Three circles in charcoal ──
    circles = [
        (28, 55, "eye", "perceive",
         "attend to what the\nloom is showing you"),
        (50, 55, "thread", "hold",
         "awareness of where\nyou are in the cloth"),
        (72, 55, "deposit", "lay down",
         "what you have understood\nin a form that can be read"),
    ]

    for (cx, cy, label_top, label_mid, desc) in circles:
        # Charcoal circle (rough)
        wobbly_circle(ax, cx, cy, 8, rng, color=CHARCOAL,
                      fill_color=SLATE_LT, lw=2.0, alpha=0.6)

        # Pahari-style label inside (simulated with serif italic)
        ax.text(cx, cy + 2, label_top, fontsize=14, color=CHARCOAL,
                fontfamily="serif", fontweight="bold",
                ha="center", va="center", zorder=7)
        ax.text(cx, cy - 2, label_mid, fontsize=10, color=CHARCOAL_LT,
                fontfamily="serif", fontstyle="italic",
                ha="center", va="center", zorder=7)

        # Description below circle
        ax.text(cx, cy - 12, desc, fontsize=8, color=INK,
                fontfamily="serif", fontstyle="italic",
                ha="center", va="top", zorder=7)

    # ── Connecting line (dashed) ──
    wobbly_line(ax, 36, 55, 42, 55, rng, lw=1.0, color=CHARCOAL_LT, alpha=0.4)
    wobbly_line(ax, 58, 55, 64, 55, rng, lw=1.0, color=CHARCOAL_LT, alpha=0.4)

    # ── Key insight ──
    ax.text(50, 22, "not instructions to the hands\n"
            "instructions to the mind",
            fontsize=11, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", va="center", zorder=7,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=PARCHMENT,
                      edgecolor=INK_FAINT, alpha=0.7))

    attribution(ax, y=3)
    fig.savefig(OUT / "three-preparations.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 three-preparations.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 5: The room arranged for perception
# Brass cup on window ledge, stone on flour, observation cord
# ═══════════════════════════════════════════════════════════════════

def room_perception():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=405)
    rng = np.random.default_rng(88)

    title_block(ax, "The Room Arranged for Perception",
                "Cup for light \u2014 stone for tension \u2014 cord for observation")

    # ── Room outline (subtle) ──
    ax.add_patch(FancyBboxPatch(
        (8, 10), 84, 72, boxstyle="round,pad=0.5",
        facecolor=PARCHMENT_DK, edgecolor=INK_FAINT,
        linewidth=0.5, alpha=0.2, zorder=1))

    # ── Loom (simplified, center-right) ──
    lx, ly = 55, 15
    lw_l, lh = 18, 50
    # Frame only
    for dx in [0, lw_l]:
        ax.plot([lx + dx, lx + dx], [ly, ly + lh],
                color=TIMBER, linewidth=2, alpha=0.5, zorder=3)
    ax.plot([lx, lx + lw_l], [ly, ly], color=TIMBER_DK,
            linewidth=2.5, alpha=0.5, zorder=3)
    ax.plot([lx, lx + lw_l], [ly + lh, ly + lh], color=TIMBER_DK,
            linewidth=2.5, alpha=0.5, zorder=3)
    # Warp threads
    for i in range(12):
        tx = lx + 2 + i * (lw_l - 4) / 11
        ax.plot([tx, tx], [ly + 2, ly + lh - 2],
                color=WARP_GREY, linewidth=0.6, alpha=0.5, zorder=3)

    # ── 1. Brass cup on window ledge ──
    cup_x, cup_y = 15, 62
    # Window
    ax.add_patch(FancyBboxPatch(
        (12, 58), 10, 12, boxstyle="round,pad=0.3",
        facecolor=SKY_WARM, edgecolor=INK_FAINT,
        linewidth=0.8, alpha=0.5, zorder=2))
    ax.text(17, 71, "east window", fontsize=7, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", ha="center", zorder=7)
    # Cup
    ax.add_patch(FancyBboxPatch(
        (cup_x - 1, cup_y - 0.5), 2.5, 1.8,
        boxstyle="round,pad=0.15",
        facecolor=BRASS, edgecolor=BRASS_LT,
        linewidth=0.8, alpha=0.7, zorder=6))
    # Water surface (reflective)
    ax.add_patch(mpatches.Ellipse((cup_x + 0.25, cup_y + 1), 2, 0.6,
                                   color=WATER_EMERALD_LT, alpha=0.4, zorder=7))
    # Reflected light spot on opposite wall
    spot_x, spot_y = 82, 55
    for r, a in [(4, 0.05), (2.5, 0.1), (1.2, 0.2)]:
        ax.add_patch(Circle((spot_x, spot_y), r,
                             color=HONEY_LT, alpha=a, zorder=2))
    # Light beam (very faint)
    ax.plot([cup_x + 1, spot_x], [cup_y + 1, spot_y],
            color=HONEY_LT, linewidth=0.4, alpha=0.15,
            linestyle="--", zorder=2)

    ax.text(cup_x, cup_y - 3, "brass cup\n(catches light)",
            fontsize=8, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # ── 2. Stone on flour-dusted slate ──
    stone_x, stone_y = 60, 12
    # Slate piece
    ax.add_patch(FancyBboxPatch(
        (stone_x - 5, stone_y - 2), 10, 5,
        boxstyle="round,pad=0.2",
        facecolor=SLATE_BG, edgecolor=STONE_DK,
        linewidth=0.8, alpha=0.3, zorder=4))
    # Flour dusting
    for _ in range(30):
        fx = stone_x + rng.uniform(-4, 4)
        fy = stone_y + rng.uniform(-1.5, 2)
        ax.add_patch(Circle((fx, fy), rng.uniform(0.1, 0.3),
                             color=FLOUR, alpha=rng.uniform(0.2, 0.5), zorder=5))
    # Stone
    ax.add_patch(Circle((stone_x, stone_y + 0.5), 0.8,
                         color=STONE_DK, alpha=0.7, zorder=6))
    # Track in flour (arc)
    track_t = np.linspace(-0.5, 0.5, 30)
    track_x = stone_x + 2 * track_t
    track_y = stone_y + 0.5 + 0.8 * np.sin(track_t * 3)
    ax.plot(track_x, track_y, color=SLATE_LT, linewidth=1.5,
            alpha=0.5, zorder=5)
    # Thread from loom frame to stone
    ax.plot([lx, stone_x], [ly + 3, stone_y + 0.5],
            color=WARP_GREY, linewidth=0.5, alpha=0.4,
            linestyle="--", zorder=3)

    ax.text(stone_x, stone_y - 4.5, "stone on flour\n(reads tension)",
            fontsize=8, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # ── 3. Observation cord on wall ──
    cord_x, cord_y = 85, 30
    # Cord hanging (vertical, with knots)
    cord_top = 65
    cord_bot = 20
    cord_xs = cord_x + 0.5 * np.sin(np.linspace(0, 2 * np.pi, 50))
    cord_ys = np.linspace(cord_top, cord_bot, 50)
    ax.plot(cord_xs, cord_ys, color=WALNUT, linewidth=1.2,
            alpha=0.6, zorder=5)
    # Knots at irregular intervals
    knot_ys = [62, 55, 48, 43, 36, 28, 23]
    for ky in knot_ys:
        ax.add_patch(Circle((cord_x, ky), 0.6,
                             color=WALNUT, alpha=0.7, zorder=6))

    ax.text(cord_x, cord_top + 3, "observation\ncord",
            fontsize=8, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)
    ax.text(cord_x, cord_bot - 3, "each knot =\na seeing",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # ── Key insight ──
    ax.text(35, 10, "the room\u2019s body delivers\nthe weaver\u2019s mind interprets",
            fontsize=10, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=PARCHMENT,
                      edgecolor=INK_FAINT, alpha=0.7))

    attribution(ax, y=3)
    fig.savefig(OUT / "room-perception.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 room-perception.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 6: Mountains beyond mountains — the weaver's notation
# Nested ridgelines on slate — the deposit
# ═══════════════════════════════════════════════════════════════════

def mountains_beyond_mountains():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=406)
    rng = np.random.default_rng(99)

    title_block(ax, "Mountains Beyond Mountains",
                "The weaver\u2019s notation \u2014 the structure of understanding laid down")

    # ── Slate background ──
    ax.add_patch(FancyBboxPatch(
        (10, 10), 80, 72, boxstyle="round,pad=0.5",
        facecolor=SLATE_BG, edgecolor=STONE_DK,
        linewidth=1.5, alpha=0.25, zorder=1))

    # ── Charcoal scratch marks (texture) ──
    for _ in range(15):
        sx = rng.uniform(15, 85)
        sy = rng.uniform(13, 78)
        sl = rng.uniform(1, 4)
        sa = rng.uniform(0, np.pi)
        ax.plot([sx, sx + sl * np.cos(sa)], [sy, sy + sl * np.sin(sa)],
                color=CHARCOAL_LT, linewidth=0.3, alpha=0.15, zorder=2)

    # ── Helper: draw a wobbly mountain ridgeline (charcoal on slate) ──
    def charcoal_ridge(ax, x_start, x_end, y_base, heights, rng,
                       lw=2.0, color=CHARCOAL, alpha=0.7, fill_color=None,
                       fill_alpha=0.12, zorder=4):
        """Draw a hand-scratched mountain ridgeline with given peak heights.
        heights: list of peak heights (one per peak)."""
        n_peaks = len(heights)
        n_pts = n_peaks * 20 + 1
        xs = np.linspace(x_start, x_end, n_pts)
        ys = np.zeros_like(xs) + y_base
        for i, h in enumerate(heights):
            cx = x_start + (i + 0.5) * (x_end - x_start) / n_peaks
            cx += rng.uniform(-1.5, 1.5)
            w = (x_end - x_start) / n_peaks * 0.7
            ys += h * np.exp(-((xs - cx) / w) ** 2)
        # Add hand-drawn wobble
        ys += rng.uniform(-0.3, 0.3, n_pts)
        xs += rng.uniform(-0.15, 0.15, n_pts)
        if fill_color:
            ax.fill_between(xs, y_base, ys, color=fill_color,
                             alpha=fill_alpha, zorder=zorder - 1)
        ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha, zorder=zorder)
        return xs, ys

    # ── The outermost ridge: the whole understanding ──
    # Broad, high, encompassing — like the view from Nahin
    charcoal_ridge(ax, 15, 85, 25, [18, 28, 22, 26, 15], rng,
                   lw=2.5, color=CHARCOAL, alpha=0.7,
                   fill_color=SLATE_LT, fill_alpha=0.15, zorder=3)

    # ── Second ridge (nearer, lower, inside the first) ──
    # Four peaks: the four aspects of the weaving state
    charcoal_ridge(ax, 20, 80, 25, [10, 18, 14, 12], rng,
                   lw=2.0, color=CHARCOAL, alpha=0.6,
                   fill_color=SLATE_LT, fill_alpha=0.12, zorder=4)

    # ── Third ridge (nearest, smallest peaks inside the second) ──
    # Finer detail — the specific state within each aspect
    charcoal_ridge(ax, 25, 75, 25, [6, 10, 8, 11, 7, 5], rng,
                   lw=1.5, color=CHARCOAL, alpha=0.5,
                   fill_color=SLATE_LT, fill_alpha=0.10, zorder=5)

    # ── Innermost marks: small peaks, almost symbols ──
    # The weaver's specific understanding — "mine, not secret, just specific"
    charcoal_ridge(ax, 32, 68, 25, [3, 5, 4, 6, 3, 4, 2], rng,
                   lw=1.0, color=CHARCOAL_LT, alpha=0.5,
                   fill_color=None, zorder=6)

    # ── Small relational marks between inner peaks ──
    # Dots and short scratches — the symbols within the innermost mountains
    inner_xs = np.linspace(35, 65, 9)
    for ix in inner_xs:
        iy = 26 + rng.uniform(0, 2)
        mark_type = rng.integers(0, 3)
        if mark_type == 0:
            # Small dot
            ax.add_patch(Circle((ix, iy), 0.4,
                                 color=CHARCOAL, alpha=0.4, zorder=7))
        elif mark_type == 1:
            # Short vertical scratch
            ax.plot([ix, ix + rng.uniform(-0.2, 0.2)],
                    [iy - 0.8, iy + 0.8],
                    color=CHARCOAL, linewidth=0.8, alpha=0.4, zorder=7)
        else:
            # Small chevron (tiny mountain mark)
            ax.plot([ix - 0.6, ix, ix + 0.6],
                    [iy, iy + 1, iy],
                    color=CHARCOAL, linewidth=0.7, alpha=0.4, zorder=7)

    # ── Valley floor: the baseline from which all ridges rise ──
    wobbly_line(ax, 15, 25, 85, 25, rng, lw=1.0, color=CHARCOAL_LT,
                alpha=0.3, zorder=3)

    # ── Labels (scratched alongside, like the weaver's hand) ──
    # Outer ridge
    ax.text(86, 48, "the whole\ncloth",
            fontsize=8, color=CHARCOAL, fontfamily="serif",
            fontstyle="italic", ha="left", zorder=7, alpha=0.6)
    wobbly_line(ax, 84, 45, 86, 48, rng, lw=0.5, color=CHARCOAL_LT,
                alpha=0.3, zorder=7)

    # Inner ridges
    ax.text(14, 38, "tension",
            fontsize=7, color=CHARCOAL_LT, fontfamily="serif",
            fontstyle="italic", ha="right", zorder=7, alpha=0.6)
    ax.text(14, 32, "row",
            fontsize=7, color=CHARCOAL_LT, fontfamily="serif",
            fontstyle="italic", ha="right", zorder=7, alpha=0.6)

    # ── The weaver's words ──
    ax.text(50, 16, "the large thing contains the smaller things",
            fontsize=10, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=PARCHMENT,
                      edgecolor=INK_FAINT, alpha=0.7))

    # ── Annotation: view from the window ──
    ax.text(50, 76, "the view from the window \u2014 mountains inside mountains",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    attribution(ax, y=3)
    fig.savefig(OUT / "mountains-beyond-mountains.png", dpi=DPI,
                bbox_inches="tight", facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 mountains-beyond-mountains.png")


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating illustrations for The Weaver\u2019s Loom...")
    serpentine_tirthan()
    kath_kuni_bees()
    idle_loom()
    three_preparations()
    room_perception()
    mountains_beyond_mountains()
    print(f"\nDone. Output: {OUT}")
