#!/usr/bin/env python3
"""
Correction Letter No. 1 — Lahaul to All Workshops
A knotted cord diagram in the notation of the Guild of Thread Walkers.

Generates a museum-style illustration of a khipu-inspired correction letter
encoding seventeen corrections as pendant cords hung from a primary cord.

Usage:
    uv run --with matplotlib --with numpy python3 cord-correction-letter.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse
from matplotlib.path import Path
import matplotlib.patches as mpatches
from pathlib import Path as FSPath

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PARCHMENT = "#f4e8c1"
PRIMARY_CORD_COLOR = "#3e2a1a"
COLORS = {
    "pattern":  "#2c3e6b",   # dark indigo
    "dye":      "#8b3a3a",   # madder red
    "filing":   "#c4a35a",   # ochre
    "weight":   "#5a7a5a",   # sage green
}

# Category assignment for each of the 17 pendant cords (0-indexed internally)
CATEGORIES = [
    "pattern", "dye",    "pattern", "filing",  "weight", "pattern",   # 1-6
    "dye",    "filing",  "pattern", "weight",  "dye",    "pattern",   # 7-12
    "filing", "weight",  "pattern", "dye",     "filing",              # 13-17
]

# Pendant cord lengths (visual complexity proxy)
LENGTHS = [
    3.2, 2.4, 3.8, 2.0, 2.6, 3.0,
    2.8, 2.2, 5.0, 2.6, 3.4, 3.6,
    2.2, 2.8, 3.0, 2.4, 2.0,
]

# Knot specifications per cord: list of (relative_position, knot_type)
#   relative_position in [0, 1] along the cord length
#   knot_type: "overhand" | "long" | "figure8"
KNOTS = [
    [(0.25, "overhand"), (0.55, "long")],
    [(0.3, "overhand"), (0.7, "overhand")],
    [(0.2, "figure8"), (0.5, "overhand"), (0.8, "long")],
    [(0.4, "overhand")],
    [(0.3, "long"), (0.65, "overhand")],
    [(0.2, "overhand"), (0.5, "figure8")],
    [(0.35, "long"), (0.7, "overhand")],
    [(0.4, "overhand")],
    [(0.15, "figure8"), (0.35, "long"), (0.52, "overhand"),           # cord 9 — complex
     (0.68, "figure8"), (0.85, "long")],
    [(0.3, "overhand"), (0.6, "long")],
    [(0.2, "overhand"), (0.5, "overhand"), (0.75, "long")],
    [(0.2, "figure8"), (0.45, "long"), (0.7, "overhand")],
    [(0.4, "overhand")],
    [(0.25, "long"), (0.6, "overhand")],
    [(0.2, "overhand"), (0.5, "figure8"), (0.8, "overhand")],
    [(0.35, "overhand"), (0.65, "long")],
    [(0.4, "overhand")],
]

# Which cords have subsidiary (difficulty) cords: (attach_frac, sub_length)
SUBSIDIARIES = {
    2:  (0.40, 1.0),
    5:  (0.35, 0.8),
    8:  (0.30, 1.4),   # cord 9 — extra annotation
    11: (0.50, 0.9),
    14: (0.45, 0.7),
}

rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def wavy_cord(ax, x0, y0, x1, y1, color, lw=2.0, alpha=1.0):
    """Draw an organic, slightly wavy cord between two points using a cubic Bezier."""
    dx = x1 - x0
    dy = y1 - y0
    length = np.hypot(dx, dy)
    # lateral wobble proportional to length
    wobble = length * 0.04
    mid_y = (y0 + y1) / 2.0
    ctrl1_x = x0 + rng.uniform(-wobble, wobble)
    ctrl1_y = y0 + (y1 - y0) * 0.33 + rng.uniform(-wobble * 0.5, wobble * 0.5)
    ctrl2_x = x0 + rng.uniform(-wobble, wobble)
    ctrl2_y = y0 + (y1 - y0) * 0.66 + rng.uniform(-wobble * 0.5, wobble * 0.5)
    verts = [(x0, y0), (ctrl1_x, ctrl1_y), (ctrl2_x, ctrl2_y), (x1, y1)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    path = Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor="none", edgecolor=color,
                               lw=lw, capstyle="round", alpha=alpha)
    ax.add_patch(patch)
    return verts


def point_on_bezier(verts, t):
    """Evaluate a cubic Bezier at parameter t in [0,1]."""
    p0, p1, p2, p3 = [np.array(v) for v in verts]
    return ((1 - t)**3 * p0 + 3*(1 - t)**2 * t * p1 +
            3*(1 - t) * t**2 * p2 + t**3 * p3)


def draw_overhand_knot(ax, x, y, color):
    """Small filled circle — simple overhand knot."""
    ax.plot(x, y, "o", color=color, markersize=5.5, zorder=5,
            markeredgecolor=color, markeredgewidth=0.5)


def draw_long_knot(ax, x, y, color):
    """Elongated bump — an ellipse along the cord."""
    e = Ellipse((x, y), width=0.12, height=0.28, angle=0,
                facecolor=color, edgecolor=color, lw=0.8, zorder=5, alpha=0.9)
    ax.add_patch(e)


def draw_figure8_knot(ax, x, y, color):
    """Small figure-eight / infinity shape."""
    r = 0.07
    theta = np.linspace(0, 2 * np.pi, 60)
    # lemniscate of Bernoulli (figure-8 curve), scaled
    denom = 1 + np.sin(theta)**2
    fx = r * 1.6 * np.cos(theta) / denom + x
    fy = r * 1.6 * np.cos(theta) * np.sin(theta) / denom + y
    ax.fill(fx, fy, color=color, zorder=5, alpha=0.9)
    ax.plot(fx, fy, color=color, lw=0.7, zorder=6)


KNOT_DRAWERS = {
    "overhand": draw_overhand_knot,
    "long":     draw_long_knot,
    "figure8":  draw_figure8_knot,
}


# ---------------------------------------------------------------------------
# Main figure
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 9))
fig.set_facecolor(PARCHMENT)
ax.set_facecolor(PARCHMENT)
ax.set_xlim(-0.5, 14.5)
ax.set_ylim(-8.5, 2.0)
ax.set_aspect("equal")
ax.axis("off")

# --- Primary cord ---
primary_y = 0.5
# Draw it as a thick wavy line across the top
n_seg = 80
px = np.linspace(0.2, 13.8, n_seg)
py = primary_y + 0.06 * np.sin(np.linspace(0, 4 * np.pi, n_seg))
ax.plot(px, py, color=PRIMARY_CORD_COLOR, lw=5.5, solid_capstyle="round", zorder=3)
# A thinner highlight to suggest twist
ax.plot(px, py + 0.03, color="#5a4030", lw=1.2, solid_capstyle="round",
        alpha=0.4, zorder=4)

# --- Pendant cord positions (with grouping gaps) ---
def pendant_x_positions(n=17):
    """Compute x positions for n pendant cords with gaps between groups 1-6, 7-12, 13-17."""
    positions = []
    spacing = 0.65
    gap = 0.45
    x = 1.0
    for i in range(n):
        positions.append(x)
        x += spacing
        if i == 5 or i == 11:   # after cord 6, after cord 12
            x += gap
    return positions

x_positions = pendant_x_positions()

# --- Draw pendant cords, knots, labels ---
for i in range(17):
    x0 = x_positions[i]
    y0 = np.interp(x0, px, py)  # attach to primary cord
    cat = CATEGORIES[i]
    color = COLORS[cat]
    length = LENGTHS[i]
    y1 = y0 - length

    # slight sway — offset bottom x
    sway = rng.uniform(-0.12, 0.12)
    x1 = x0 + sway

    # draw pendant cord
    verts = wavy_cord(ax, x0, y0, x1, y1, color, lw=1.8)

    # cord number label above
    ax.text(x0, y0 + 0.25, str(i + 1), ha="center", va="bottom",
            fontsize=6.5, fontfamily="serif", color="#4a3a2a", zorder=7)

    # knots
    for (frac, ktype) in KNOTS[i]:
        pt = point_on_bezier(verts, frac)
        KNOT_DRAWERS[ktype](ax, pt[0], pt[1], color)

    # subsidiary cord
    if i in SUBSIDIARIES:
        attach_frac, sub_len = SUBSIDIARIES[i]
        attach_pt = point_on_bezier(verts, attach_frac)
        sub_x1 = attach_pt[0] + rng.uniform(0.25, 0.45)
        sub_y1 = attach_pt[1] - sub_len
        sub_color = "#7a6a5a"   # muted brown for difficulty annotation
        wavy_cord(ax, attach_pt[0], attach_pt[1], sub_x1, sub_y1,
                  sub_color, lw=0.9, alpha=0.7)
        # small terminal knot on subsidiary
        ax.plot(sub_x1, sub_y1, "o", color=sub_color, markersize=2.5,
                zorder=5, alpha=0.7)

    # special annotation for cord 9
    if i == 8:
        bottom_pt = point_on_bezier(verts, 0.97)
        ax.text(bottom_pt[0] + 0.15, bottom_pt[1] - 0.15, r"$\S 9$",
                ha="left", va="top", fontsize=7.5, fontfamily="serif",
                fontstyle="italic", color="#2c3e6b", zorder=7)

# --- Title and subtitle ---
ax.text(7.0, 1.65, "Correction Letter No. 1 \u2014 Lahaul to All Workshops",
        ha="center", va="bottom", fontsize=13, fontfamily="serif",
        fontweight="bold", color="#3e2a1a")
ax.text(7.0, 1.28, "seventeen corrections, ordered by dependency",
        ha="center", va="bottom", fontsize=9, fontfamily="serif",
        fontstyle="italic", color="#6a5a4a")

# --- Footnote ---
footnote = ("Cord 6 depends on Cord 3.  Cord 12 depends on Cord 6.  "
            "Cord 9 requires derivation from the thread-weight conversion table.")
ax.text(7.0, -8.1, footnote, ha="center", va="top", fontsize=6.5,
        fontfamily="serif", color="#6a5a4a", fontstyle="italic")

# --- Legend (bottom right) ---
legend_x, legend_y = 11.2, -5.4
# background box
legend_bg = FancyBboxPatch((legend_x - 0.3, legend_y - 2.55), 3.2, 2.7,
                           boxstyle="round,pad=0.15", facecolor=PARCHMENT,
                           edgecolor="#a09080", lw=0.8, zorder=6)
ax.add_patch(legend_bg)

ax.text(legend_x + 1.3, legend_y - 0.05, "Legend", ha="center", va="bottom",
        fontsize=8, fontfamily="serif", fontweight="bold", color="#3e2a1a", zorder=7)

# Cord colour legend
dy = -0.38
colour_items = [
    ("Pattern records",         COLORS["pattern"]),
    ("Dye records",             COLORS["dye"]),
    ("Classification / filing", COLORS["filing"]),
    ("Thread-weight standards", COLORS["weight"]),
]
for j, (label, col) in enumerate(colour_items):
    yy = legend_y + dy * (j + 1) - 0.1
    ax.plot([legend_x, legend_x + 0.45], [yy, yy], color=col, lw=2.2, zorder=7)
    ax.text(legend_x + 0.6, yy, label, va="center", fontsize=6,
            fontfamily="serif", color="#3e2a1a", zorder=7)

# Knot type legend
knot_label_y = legend_y + dy * 5 - 0.25
knot_items = [
    ("overhand", "Quantity",    draw_overhand_knot),
    ("long",     "Reference",   draw_long_knot),
    ("figure8",  "Instruction", draw_figure8_knot),
]
for j, (ktype, label, drawer) in enumerate(knot_items):
    yy = knot_label_y + dy * j
    drawer(ax, legend_x + 0.15, yy, "#4a3a2a")
    ax.text(legend_x + 0.6, yy, label, va="center", fontsize=6,
            fontfamily="serif", color="#3e2a1a", zorder=7)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_dir = FSPath(__file__).parent
for ext in ("pdf", "png"):
    out = out_dir / f"cord-correction-letter.{ext}"
    fig.savefig(out, bbox_inches="tight", dpi=200, facecolor=fig.get_facecolor())
    print(f"Saved: {out}")
plt.close(fig)
