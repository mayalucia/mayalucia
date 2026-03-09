# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Cartographer's Slab".

A story about a retired Survey of India cartographer who draws the
Western Himalaya's relationships — not its contours — on a slate slab
with chalk. Rivers as connections, ridges as seams, passes as openings.
The background drawn faintly. The whole thing washes clean each monsoon.

Visual language: parchment base, chalk-on-slate for the slab drawings,
walnut ink for framing. Hand-drawn jitter throughout.

Run with:  uv run generate_images.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ── Output ──────────────────────────────────────────────────────────
OUT = Path(__file__).parent / "../../website/static/images/writing/the-cartographers-slab"
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

DEODAR        = "#4A6B48"
DEODAR_DK     = "#2E4A2C"

STONE         = "#9A9080"
STONE_DK      = "#6B6658"
TIMBER        = "#8B6B4A"

WATER_EMERALD = "#4A8B6B"
WATER_COPPER  = "#C4886B"

MOUNTAIN      = "#7A7068"
MOUNTAIN_DK   = "#5A5248"
SNOW          = "#E8EEF0"

SKY_WARM      = "#D8C8B0"
SKY_COPPER    = "#D4A878"
SKY_DUSK      = "#B8886B"

SLATE         = "#3A3A38"
SLATE_LT      = "#5A5A58"
CHALK         = "#E8E4D8"
CHALK_DK      = "#D0C8B8"
CHALK_DIM     = "#9A9890"

MAGNETITE     = "#3A3838"
MAGNETITE_LT  = "#5A5858"

COPPER        = "#C4886B"
COPPER_LT     = "#D8A888"

TRAIL_OCHRE   = "#C4A868"

CHARCOAL      = "#4A4A48"

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


def attribution(ax, text="The Cartographer\u2019s Slab \u2014 A Human-Machine Collaboration",
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


def wobbly_curve(ax, points, rng, lw=1.5, color=CHALK, alpha=0.8,
                 n_per_seg=15, zorder=4):
    """Draw a smooth wobbly curve through a list of (x,y) points."""
    all_xs, all_ys = [], []
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        xs = np.linspace(x0, x1, n_per_seg)
        ys = np.linspace(y0, y1, n_per_seg)
        xs += rng.uniform(-0.3, 0.3, n_per_seg)
        ys += rng.uniform(-0.3, 0.3, n_per_seg)
        all_xs.extend(xs)
        all_ys.extend(ys)
    ax.plot(all_xs, all_ys, color=color, linewidth=lw, alpha=alpha,
            zorder=zorder)


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
    for i in range(n_courses):
        cy = by + i * (bh / n_courses)
        ch = bh / n_courses
        color = STONE if i % 2 == 0 else TIMBER
        alpha = 0.7 if i % 2 == 0 else 0.5
        ax.add_patch(FancyBboxPatch(
            (bx, cy), bw, ch, boxstyle="square,pad=0",
            facecolor=color, edgecolor=INK_FAINT,
            linewidth=0.3, alpha=alpha, zorder=zorder))


# ════════════════════════════════════════════════════════════════════
# Figure 1: The Rest House Above the Gorge
# ════════════════════════════════════════════════════════════════════

def fig1_rest_house():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=100)
    rng = np.random.default_rng(101)

    title_block(ax, "The Forest Rest House",
                "A shelf above the Tirthan gorge, the cartographer at his slab")

    # Sky gradient
    for i in range(20):
        y = 88 - i * 0.8
        ax.axhspan(y, y + 0.8, color=SKY_WARM, alpha=0.15 - i * 0.005,
                   zorder=0)

    # Far mountains
    draw_mountain_ridge(ax, 0, 100, 65, 22, n_peaks=7, color=MOUNTAIN, seed=102)

    # Deodar forest on slopes
    for _ in range(40):
        tx = rng.uniform(5, 95)
        ty = rng.uniform(45, 68)
        ts = rng.uniform(1.5, 3.5)
        ax.plot([tx, tx], [ty, ty + ts], color=DEODAR_DK,
                linewidth=0.5, alpha=0.4, zorder=3)
        # Simple triangle canopy
        tri_xs = [tx - ts * 0.4, tx, tx + ts * 0.4]
        tri_ys = [ty + ts * 0.3, ty + ts, ty + ts * 0.3]
        ax.fill(tri_xs, tri_ys, color=DEODAR, alpha=0.3, zorder=3)

    # Gorge walls — magnetite narrows
    gorge_left_x = np.array([35, 37, 38, 39, 40, 42])
    gorge_left_y = np.array([10, 25, 35, 42, 48, 55])
    gorge_right_x = np.array([58, 60, 61, 62, 63, 65])
    gorge_right_y = np.array([10, 25, 35, 42, 48, 55])

    ax.fill_betweenx(gorge_left_y, gorge_left_x - 5, gorge_left_x,
                      color=MAGNETITE, alpha=0.6, zorder=2)
    ax.fill_betweenx(gorge_right_y, gorge_right_x, gorge_right_x + 5,
                      color=MAGNETITE, alpha=0.6, zorder=2)

    # River through the gorge
    river_xs = [42, 44, 48, 52, 55, 58]
    river_ys = [10, 20, 30, 38, 45, 52]
    wobbly_curve(ax, list(zip(river_xs, river_ys)), rng,
                 lw=3, color=WATER_EMERALD, alpha=0.5, zorder=3)

    # The shelf / terrace where the rest house sits
    shelf_xs = [15, 25, 40, 55, 70, 85]
    shelf_ys = [48, 50, 52, 52, 50, 47]
    ax.fill_between(shelf_xs, [45] * 6, shelf_ys,
                    color=TRAIL_OCHRE, alpha=0.3, zorder=4)

    # Rest house — PWD style, simple rectangle with pitched roof
    bx, by, bw, bh = 20, 50, 18, 8
    draw_kath_kuni_wall(ax, bx, by, bw, bh, n_courses=6, zorder=5)
    # Roof
    roof_xs = [bx - 1, bx + bw / 2, bx + bw + 1]
    roof_ys = [by + bh, by + bh + 5, by + bh]
    ax.fill(roof_xs, roof_ys, color=STONE_DK, alpha=0.6, zorder=6)
    ax.plot(roof_xs + [roof_xs[0]], roof_ys + [roof_ys[0]],
            color=INK, linewidth=0.8, alpha=0.5, zorder=6)

    # PWD letters on gatepost
    ax.text(bx - 2, by + 2, "P.W.D.", fontsize=5, color=INK_LIGHT,
            fontfamily="serif", alpha=0.4, rotation=90, zorder=6)

    # Veranda
    ax.add_patch(FancyBboxPatch(
        (bx + bw, by), 6, bh * 0.7, boxstyle="square,pad=0",
        facecolor=TIMBER, edgecolor=INK_FAINT,
        linewidth=0.3, alpha=0.35, zorder=5))

    # The slab on the veranda — tilted rectangle
    slab_x, slab_y = bx + bw + 1.5, by + 2
    ax.add_patch(FancyBboxPatch(
        (slab_x, slab_y), 3.5, 4, boxstyle="round,pad=0.1",
        facecolor=SLATE, edgecolor=SLATE_LT,
        linewidth=0.8, alpha=0.8, zorder=7))
    # Chalk marks on slab (tiny)
    for _ in range(8):
        lx = slab_x + rng.uniform(0.3, 3.2)
        ly = slab_y + rng.uniform(0.3, 3.7)
        ax.plot([lx, lx + rng.uniform(-0.5, 0.5)],
                [ly, ly + rng.uniform(-0.3, 0.3)],
                color=CHALK, linewidth=0.4, alpha=0.6, zorder=8)

    # Cartographer figure (simple, seated)
    cx, cy = bx + bw + 4.5, by + 2
    # Body
    ax.plot([cx, cx], [cy, cy + 3], color=INK, linewidth=1.2,
            alpha=0.5, zorder=7)
    # Head
    ax.add_patch(plt.Circle((cx, cy + 3.5), 0.7, color=INK,
                              alpha=0.35, zorder=7))
    # Arms toward slab
    ax.plot([cx, cx - 1.5], [cy + 2, cy + 2.5], color=INK,
            linewidth=0.8, alpha=0.4, zorder=7)

    # Dusk light — copper wash on gorge
    for i in range(10):
        ax.axhspan(10 + i * 3, 13 + i * 3,
                   xmin=0.35, xmax=0.65,
                   color=COPPER, alpha=0.03, zorder=3)

    attribution(ax)
    fig.savefig(OUT / "rest-house.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ rest-house.png")


# ════════════════════════════════════════════════════════════════════
# Figure 2: The Bounding Box Problem
# ════════════════════════════════════════════════════════════════════

def fig2_bounding_box():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=200)
    rng = np.random.default_rng(201)

    title_block(ax, "The Problem of the Bounding Box",
                "Sheet 53F/4 — the frame that cuts the ridge")

    # Draw a Survey sheet frame
    frame_x, frame_y, frame_w, frame_h = 15, 15, 70, 65
    ax.add_patch(FancyBboxPatch(
        (frame_x, frame_y), frame_w, frame_h, boxstyle="square,pad=0",
        facecolor=PARCHMENT_DK, edgecolor=INK,
        linewidth=1.5, alpha=0.5, zorder=2))

    # Sheet designation
    ax.text(frame_x + 2, frame_y + frame_h - 2, "53F/4",
            fontsize=10, fontfamily="serif", color=INK_LIGHT,
            alpha=0.6, zorder=4)

    # Ridge running diagonally across the sheet and BEYOND the frame
    ridge_points_full = [
        (5, 30), (20, 40), (35, 52), (50, 58),
        (65, 55), (80, 48), (95, 42)
    ]
    # The ridge extends beyond the bounding box
    xs_full = [p[0] for p in ridge_points_full]
    ys_full = [p[1] for p in ridge_points_full]

    # Draw full ridge faintly (what exists in reality)
    wobbly_curve(ax, ridge_points_full, rng, lw=2.5, color=MOUNTAIN,
                 alpha=0.2, zorder=3)

    # Draw the portion inside the frame more strongly
    ridge_inside = [(x, y) for x, y in ridge_points_full
                    if frame_x <= x <= frame_x + frame_w]
    if len(ridge_inside) >= 2:
        wobbly_curve(ax, ridge_inside, rng, lw=2.5, color=MOUNTAIN_DK,
                     alpha=0.6, zorder=4)

    # Label the ridge
    ax.text(50, 62, "The ridge continues\u2026", fontsize=9,
            fontfamily="serif", fontstyle="italic", color=INK_LIGHT,
            ha="center", alpha=0.6, zorder=5)

    # Tirthan valley (east side of ridge) — inside the frame
    tirthan_pts = [(55, 20), (58, 30), (60, 40), (58, 50)]
    wobbly_curve(ax, tirthan_pts, rng, lw=2, color=WATER_EMERALD,
                 alpha=0.5, zorder=4)
    ax.text(62, 35, "Tirthan", fontsize=9, fontfamily="serif",
            color=WATER_EMERALD, alpha=0.6, zorder=5, fontstyle="italic")

    # Parvati valley (west side of ridge) — partially outside
    parvati_pts = [(30, 18), (28, 28), (25, 38), (22, 48)]
    wobbly_curve(ax, parvati_pts, rng, lw=2, color=WATER_EMERALD,
                 alpha=0.3, zorder=4)
    ax.text(22, 25, "Parvati", fontsize=9, fontfamily="serif",
            color=WATER_EMERALD, alpha=0.4, zorder=5, fontstyle="italic")

    # The relationship arrow crossing the ridge — cut by the frame
    ax.annotate("", xy=(30, 38), xytext=(60, 40),
                arrowprops=dict(arrowstyle="<->", color=COPPER,
                               lw=1.5, alpha=0.4),
                zorder=5)
    ax.text(45, 44, "relationship", fontsize=8, fontfamily="serif",
            fontstyle="italic", color=COPPER, ha="center", alpha=0.5,
            zorder=5)

    # "Gupta's territory" label outside the frame
    ax.text(8, 42, "Gupta\u2019s\nterritory\n(53F/3)", fontsize=8,
            fontfamily="serif", color=INK_LIGHT, ha="center",
            alpha=0.5, zorder=3, fontstyle="italic")

    # Dashed lines at frame edges showing the cut
    for yy in np.linspace(frame_y, frame_y + frame_h, 30):
        ax.plot([frame_x, frame_x], [yy, yy + 1],
                color=INK, linewidth=0.3, alpha=0.3, zorder=3)

    # Jalori pass on the ridge
    ax.plot(50, 58, 'x', color=INK, markersize=8, alpha=0.5, zorder=5)
    ax.text(50, 55, "Jalori", fontsize=8, fontfamily="serif",
            color=INK_LIGHT, ha="center", alpha=0.5, zorder=5)

    # Quote
    ax.text(50, 8, "\u201cA boundary belongs to no one.\u201d",
            fontsize=11, fontfamily="serif", fontstyle="italic",
            color=INK, ha="center", alpha=0.5, zorder=5)

    attribution(ax)
    fig.savefig(OUT / "bounding-box.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ bounding-box.png")


# ════════════════════════════════════════════════════════════════════
# Figure 3: The Slab — chalk diagram of connections
# ════════════════════════════════════════════════════════════════════

def fig3_the_slab():
    fig, ax = make_fig(bg=SLATE)
    rng = np.random.default_rng(300)

    # Slate texture — subtle lighter patches
    for _ in range(12):
        cx, cy = rng.uniform(10, 90), rng.uniform(10, 90)
        r = rng.uniform(5, 12)
        circle = plt.Circle((cx, cy), r, color=SLATE_LT,
                             alpha=rng.uniform(0.05, 0.12), zorder=0)
        ax.add_patch(circle)

    ax.text(50, 96, "The Slab", ha="center", va="top",
            fontsize=18, fontweight="bold", color=CHALK,
            fontfamily="serif", alpha=0.8)
    ax.text(50, 92, "What things do to each other",
            ha="center", va="top", fontsize=11,
            fontstyle="italic", color=CHALK_DIM, fontfamily="serif")

    # ── Towns as junction nodes ──
    towns = {
        "Kullu":   (50, 45),
        "Manali":  (45, 65),
        "Shimla":  (55, 15),
        "Keylong": (30, 75),
        "Banjar":  (60, 38),
        "Kasol":   (35, 50),
        "Mandi":   (58, 25),
        "Sangla":  (75, 55),
        "Rampur":  (68, 30),
    }

    # ── Rivers as connection lines (heavy chalk) ──
    rivers = [
        # (name, points)
        ("Beas", [(45, 65), (48, 55), (50, 45), (53, 35), (58, 25)]),
        ("Parvati", [(25, 60), (30, 55), (35, 50), (45, 47), (50, 45)]),
        ("Tirthan", [(55, 55), (58, 48), (60, 42), (60, 38)]),
        ("Sainj", [(65, 52), (62, 45), (60, 38)]),
        ("Sutlej", [(75, 55), (72, 45), (68, 35), (68, 30), (62, 22), (55, 15)]),
        ("Chandrabhaga", [(15, 80), (22, 75), (30, 75), (35, 70)]),
    ]

    for name, pts in rivers:
        wobbly_curve(ax, pts, rng, lw=2, color=CHALK, alpha=0.7, zorder=4)
        # Label at midpoint
        mid = pts[len(pts) // 2]
        ax.text(mid[0] + rng.uniform(-2, 2), mid[1] + 2.5,
                name, fontsize=7, fontfamily="serif", fontstyle="italic",
                color=CHALK_DIM, alpha=0.6, ha="center", zorder=5)

    # ── Ridges as dashed seams ──
    ridges = [
        ("GHR", [(20, 58), (35, 60), (50, 62), (65, 58), (80, 52)]),
        ("Pir Panjal", [(15, 72), (30, 68), (45, 65)]),
        ("Dhauladhar", [(55, 70), (68, 65), (80, 60)]),
    ]

    for name, pts in ridges:
        xs, ys = [], []
        for i in range(len(pts) - 1):
            seg_xs = np.linspace(pts[i][0], pts[i+1][0], 20)
            seg_ys = np.linspace(pts[i][1], pts[i+1][1], 20)
            seg_xs += rng.uniform(-0.3, 0.3, 20)
            seg_ys += rng.uniform(-0.3, 0.3, 20)
            xs.extend(seg_xs)
            ys.extend(seg_ys)
        ax.plot(xs, ys, color=CHALK_DK, linewidth=1, alpha=0.4,
                linestyle=(0, (4, 3)), zorder=3)
        mid = pts[len(pts) // 2]
        ax.text(mid[0], mid[1] + 3, name, fontsize=6,
                fontfamily="serif", fontstyle="italic",
                color=CHALK_DIM, alpha=0.4, ha="center", zorder=5)

    # ── Passes as openings (× marks) ──
    passes = {
        "Rohtang":      (40, 70),
        "Jalori":       (57, 58),
        "Chandrakhani": (42, 57),
        "Pin Parvati":  (28, 65),
    }

    for name, (px, py) in passes.items():
        s = 1.2
        ax.plot([px - s, px + s], [py - s, py + s], color=CHALK,
                linewidth=1, alpha=0.5, zorder=5)
        ax.plot([px + s, px - s], [py - s, py + s], color=CHALK,
                linewidth=1, alpha=0.5, zorder=5)
        ax.text(px, py - 2.5, name, fontsize=6, fontfamily="serif",
                color=CHALK_DIM, alpha=0.5, ha="center", zorder=5)

    # ── Towns as dots with names ──
    for name, (tx, ty) in towns.items():
        ax.plot(tx, ty, 'o', color=CHALK, markersize=5, alpha=0.6,
                zorder=6)
        ax.text(tx + 2, ty - 1.5, name, fontsize=7, fontfamily="serif",
                color=CHALK, alpha=0.5, zorder=6)

    # Attribution
    ax.text(50, 2, "The Cartographer\u2019s Slab \u2014 A Human-Machine Collaboration",
            ha="center", va="bottom", fontsize=8, fontstyle="italic",
            color=CHALK_DIM, fontfamily="serif", alpha=0.5)

    fig.savefig(OUT / "the-slab.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ the-slab.png")


# ════════════════════════════════════════════════════════════════════
# Figure 4: The Background — faint geography behind heavy connections
# ════════════════════════════════════════════════════════════════════

def fig4_the_background():
    fig, ax = make_fig(bg=SLATE)
    rng = np.random.default_rng(400)

    # Slate texture
    for _ in range(12):
        cx, cy = rng.uniform(10, 90), rng.uniform(10, 90)
        r = rng.uniform(5, 12)
        circle = plt.Circle((cx, cy), r, color=SLATE_LT,
                             alpha=rng.uniform(0.05, 0.10), zorder=0)
        ax.add_patch(circle)

    ax.text(50, 96, "The Background", ha="center", va="top",
            fontsize=18, fontweight="bold", color=CHALK,
            fontfamily="serif", alpha=0.8)
    ax.text(50, 92, "The discipline of faintness",
            ha="center", va="top", fontsize=11,
            fontstyle="italic", color=CHALK_DIM, fontfamily="serif")

    # ── Background layer: faint geographic detail ──

    # Faint river courses (the actual winding paths, not schematic)
    bg_rivers = [
        # Tirthan through gorge
        [(55, 55), (56, 52), (57, 48), (57.5, 45), (58, 42),
         (59, 40), (60, 38), (60, 35)],
        # Beas main course
        [(44, 68), (45, 63), (46, 58), (48, 52), (49, 48),
         (50, 45), (51, 40), (53, 35), (55, 30), (57, 25)],
        # Parvati
        [(22, 62), (25, 58), (28, 55), (31, 52), (35, 50),
         (40, 48), (45, 47), (50, 45)],
        # Side streams (very faint)
        [(58, 50), (57, 47), (56, 44)],
        [(62, 48), (61, 44), (60, 40)],
    ]

    for pts in bg_rivers:
        wobbly_curve(ax, pts, rng, lw=0.8, color=CHALK_DIM,
                     alpha=0.15, zorder=2)

    # Faint ridge profiles
    for y_base, seed in [(60, 410), (68, 411), (53, 412)]:
        xs = np.linspace(10, 90, 80)
        ys = y_base + np.zeros_like(xs)
        rng2 = np.random.default_rng(seed)
        for _ in range(4):
            cx = rng2.uniform(20, 80)
            h = rng2.uniform(2, 5)
            w = rng2.uniform(8, 15)
            ys += h * np.exp(-((xs - cx) / w) ** 2)
        xs += rng2.uniform(-0.2, 0.2, len(xs))
        ax.plot(xs, ys, color=CHALK_DIM, linewidth=0.5, alpha=0.08,
                linestyle=(0, (3, 4)), zorder=1)

    # Faint town dots
    bg_towns = [(50, 45), (45, 65), (35, 50), (60, 38),
                (58, 25), (75, 55)]
    for tx, ty in bg_towns:
        ax.plot(tx, ty, 'o', color=CHALK_DIM, markersize=2,
                alpha=0.12, zorder=2)

    # ── Foreground layer: heavy chalk connections ──

    # Main river connections (heavy)
    fg_rivers = [
        ("Beas", [(45, 65), (50, 45), (58, 25)]),
        ("Parvati", [(25, 60), (35, 50), (50, 45)]),
        ("Tirthan", [(55, 55), (60, 38)]),
        ("Sutlej", [(75, 55), (68, 30), (55, 15)]),
    ]

    for name, pts in fg_rivers:
        wobbly_curve(ax, pts, rng, lw=2.5, color=CHALK, alpha=0.7,
                     zorder=5)
        mid = pts[len(pts) // 2]
        ax.text(mid[0] + 2, mid[1] + 2, name, fontsize=8,
                fontfamily="serif", fontstyle="italic",
                color=CHALK, alpha=0.5, ha="center", zorder=6)

    # Main ridge seams (medium chalk)
    ridge_pts = [(20, 58), (35, 60), (50, 62), (65, 58), (80, 52)]
    xs, ys = [], []
    for i in range(len(ridge_pts) - 1):
        seg_xs = np.linspace(ridge_pts[i][0], ridge_pts[i+1][0], 20)
        seg_ys = np.linspace(ridge_pts[i][1], ridge_pts[i+1][1], 20)
        seg_xs += rng.uniform(-0.3, 0.3, 20)
        seg_ys += rng.uniform(-0.3, 0.3, 20)
        xs.extend(seg_xs)
        ys.extend(seg_ys)
    ax.plot(xs, ys, color=CHALK_DK, linewidth=1.5, alpha=0.35,
            linestyle=(0, (5, 3)), zorder=4)

    # Pass openings
    for px, py, name in [(57, 58, "Jalori"), (40, 70, "Rohtang")]:
        s = 1.5
        ax.plot([px - s, px + s], [py - s, py + s], color=CHALK,
                linewidth=1.2, alpha=0.5, zorder=6)
        ax.plot([px + s, px - s], [py - s, py + s], color=CHALK,
                linewidth=1.2, alpha=0.5, zorder=6)
        ax.text(px, py - 3, name, fontsize=7, fontfamily="serif",
                color=CHALK, alpha=0.4, ha="center", zorder=6)

    # Town nodes
    for tx, ty, name in [(50, 45, "Kullu"), (45, 65, "Manali"),
                          (35, 50, "Kasol"), (60, 38, "Banjar")]:
        ax.plot(tx, ty, 'o', color=CHALK, markersize=6, alpha=0.7,
                zorder=7)
        ax.text(tx + 2.5, ty - 1.5, name, fontsize=8,
                fontfamily="serif", color=CHALK, alpha=0.5, zorder=7)

    # The key insight — annotation
    ax.text(50, 7, "\u201cIf the background is absent, the connections float in nothing.\u201d",
            ha="center", fontsize=10, fontfamily="serif",
            fontstyle="italic", color=CHALK_DK, alpha=0.4, zorder=8)

    # Attribution
    ax.text(50, 2, "The Cartographer\u2019s Slab \u2014 A Human-Machine Collaboration",
            ha="center", va="bottom", fontsize=8, fontstyle="italic",
            color=CHALK_DIM, fontfamily="serif", alpha=0.5)

    fig.savefig(OUT / "the-background.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ the-background.png")


# ════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating illustrations for The Cartographer's Slab...")
    fig1_rest_house()
    fig2_bounding_box()
    fig3_the_slab()
    fig4_the_background()
    print(f"\nAll images written to {OUT}")
