#!/usr/bin/env python3
"""
The Descent — illustration for The Constellation of Doridhar, Ch. V.

Two views of the constellation connected by a visual fold: the outer cosmos
(all provinces) fading, and the inner cosmos of the Observatory emerging.
A breadcrumb trail shows the path of descent.

Usage:
    uv run --with matplotlib --with numpy python3 gen-descent.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from pathlib import Path as FSPath

SLATE = "#12121e"
CHALK = "#e8e4d4"
CHALK_DIM = "#8a8678"
AMBER = "#d4a574"
BLUE = "#7eb8da"
TERRACOTTA = "#c4836a"
GREEN = "#a8d4a0"

rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# Figure — two panels side by side, connected by a fold
# ---------------------------------------------------------------------------

fig = plt.figure(figsize=(14, 7), dpi=200)
fig.patch.set_facecolor(SLATE)

# Left panel: outer constellation (fading)
ax_left = fig.add_axes([0.02, 0.05, 0.42, 0.88])
ax_left.set_facecolor(SLATE)
ax_left.set_xlim(-6, 6)
ax_left.set_ylim(-5.5, 5.5)
ax_left.set_aspect("equal")
ax_left.axis("off")

# Right panel: inner constellation (emerging)
ax_right = fig.add_axes([0.56, 0.05, 0.42, 0.88])
ax_right.set_facecolor(SLATE)
ax_right.set_xlim(-5, 5)
ax_right.set_ylim(-4.5, 4.5)
ax_right.set_aspect("equal")
ax_right.axis("off")

# --- Left panel: outer cosmos, fading ---

# Chalk dust (sparse, faded)
n_dust = 800
dx = rng.uniform(-5.5, 5.5, n_dust)
dy = rng.uniform(-5, 5, n_dust)
ds = rng.uniform(0.1, 1.0, n_dust)
ax_left.scatter(dx, dy, s=ds, c=CHALK, alpha=0.02, edgecolors="none")

# Phase crystal positions (faded)
phases = [
    (-4.5, 0, AMBER, "M\u2081"),
    (0, 3.8, BLUE, "M\u2082"),
    (4.5, 0, TERRACOTTA, "M\u2083"),
    (0, -3.8, GREEN, "E"),
]
for px, py, col, glyph in phases:
    ax_left.plot(px, py, "o", color=col, markersize=8, alpha=0.15)
    ax_left.text(px, py, glyph, ha="center", va="center",
                fontsize=6, color=SLATE, alpha=0.3, fontweight="bold")

# Province nodes (most faded, Observatory highlighted)
outer_nodes = [
    ("Observatory", -3.5, -1.2, "#c4a06a", True),
    ("Lantern", 3.2, -1.0, "#c48a72", False),
    ("Menagerie", 1.8, 2.2, "#9aaa8a", False),
    ("Loom", -2.2, 1.8, "#b0a87a", False),
    ("Watershed", -1.5, -2.8, "#bca87a", False),
    ("Scriptorium", 1.2, -3.0, "#dac87e", False),
    ("Thread", -0.4, 1.2, "#c4c4c4", False),
]

for name, nx, ny, col, highlight in outer_nodes:
    if highlight:
        # The selected node — brighter, with expanding ring
        for r_h in [0.8, 0.5, 0.25]:
            c = plt.Circle((nx, ny), r_h, color=col,
                          alpha=0.08, fill=True)
            ax_left.add_patch(c)
        ax_left.plot(nx, ny, "o", color=col, markersize=12,
                    alpha=0.85, zorder=10)
        ax_left.text(nx, ny - 0.65, name, ha="center", va="top",
                    fontsize=6, fontfamily="serif", color=col,
                    alpha=0.9, fontweight="bold")
    else:
        # Fading nodes
        ax_left.plot(nx, ny, "o", color=col, markersize=5, alpha=0.12)
        ax_left.text(nx, ny - 0.45, name, ha="center", va="top",
                    fontsize=4.5, fontfamily="serif", color=col, alpha=0.12)

# Fading edges
fade_edges = [
    (-3.5, -1.2, -2.2, 1.8),
    (-3.5, -1.2, -1.5, -2.8),
    (3.2, -1.0, 1.8, 2.2),
    (-2.2, 1.8, 1.8, 2.2),
]
for x0, y0, x1, y1 in fade_edges:
    ax_left.plot([x0, x1], [y0, y1], color=CHALK_DIM, lw=0.4, alpha=0.06)

# Label
ax_left.text(0, 5.0, "the outer cosmos", ha="center", va="center",
            fontsize=8, fontfamily="serif", fontstyle="italic",
            color=CHALK_DIM, alpha=0.35)

# --- Connecting fold (between panels, in figure coords) ---
# Draw a swooping arrow/fold in figure coordinates
ax_fold = fig.add_axes([0.43, 0.3, 0.14, 0.4])
ax_fold.set_facecolor(SLATE)
ax_fold.set_xlim(0, 1)
ax_fold.set_ylim(0, 1)
ax_fold.axis("off")

# Curved arrow suggesting descent / unfold
t = np.linspace(0, 1, 80)
fold_x = 0.2 + 0.6 * t
fold_y = 0.7 - 0.4 * np.sin(t * np.pi)
fold_x += rng.normal(0, 0.005, 80)
fold_y += rng.normal(0, 0.005, 80)
ax_fold.plot(fold_x, fold_y, color=AMBER, lw=1.0, alpha=0.35)
# Arrowhead
ax_fold.annotate("", xy=(fold_x[-1], fold_y[-1]),
                xytext=(fold_x[-5], fold_y[-5]),
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.0,
                               mutation_scale=12),
                alpha=0.4)

# Breadcrumb text
ax_fold.text(0.5, 0.15, "The Archive \u203A The Observatory",
            ha="center", va="center", fontsize=6.5,
            fontfamily="serif", color=CHALK, alpha=0.4)

# --- Right panel: inner cosmos of the Observatory ---

# Denser chalk dust (this is a new space)
n_dust2 = 1200
dx2 = rng.uniform(-4.5, 4.5, n_dust2)
dy2 = rng.uniform(-4, 4, n_dust2)
ds2 = rng.uniform(0.1, 1.2, n_dust2)
ax_right.scatter(dx2, dy2, s=ds2, c=CHALK, alpha=0.03, edgecolors="none")

# Inner nodes of the Observatory
inner_nodes = [
    ("Equations", "\u2202", -2.0, -1.5, BLUE, 10),
    ("Notebooks", "\u03C0", -2.5, 1.5, AMBER, 9),
    ("Specification", "\u03BB", 0.5, -3.0, BLUE, 9),
    ("Engine", "\u2295", 2.8, -0.8, TERRACOTTA, 9),
    ("Demonstration", "\u25C9", 2.0, 2.5, TERRACOTTA, 8),
]

for name, glyph, nx, ny, col, size in inner_nodes:
    # Glow
    for r_h in [0.5, 0.3, 0.15]:
        c = plt.Circle((nx, ny), r_h, color=col,
                       alpha=0.06, fill=True)
        ax_right.add_patch(c)
    ax_right.plot(nx, ny, "o", color=col, markersize=size,
                 alpha=0.85, zorder=10)
    ax_right.text(nx, ny, glyph, ha="center", va="center",
                 fontsize=7, color=SLATE, fontweight="bold", zorder=11)
    ax_right.text(nx, ny - 0.55, name, ha="center", va="top",
                 fontsize=5.5, fontfamily="serif", color=col, alpha=0.75)

# Inner edges
inner_edges = [
    ("Equations", "Notebooks"),
    ("Equations", "Specification"),
    ("Equations", "Engine"),
    ("Engine", "Demonstration"),
    ("Notebooks", "Demonstration"),
]

node_pos = {n[0]: (n[2], n[3]) for n in inner_nodes}
for src_name, tgt_name in inner_edges:
    sx, sy = node_pos[src_name]
    tx, ty = node_pos[tgt_name]
    n_pts = 30
    t = np.linspace(0, 1, n_pts)
    mx = (sx + tx) / 2 + rng.uniform(-0.2, 0.2)
    my = (sy + ty) / 2 + rng.uniform(-0.2, 0.2)
    ex = sx * (1-t)**2 + 2 * mx * t * (1-t) + tx * t**2
    ey = sy * (1-t)**2 + 2 * my * t * (1-t) + ty * t**2
    ax_right.plot(ex, ey, color=CHALK_DIM, lw=0.6, alpha=0.15)

# Cluster labels
ax_right.text(0, -3.8, "PHYSICS", ha="center", va="center",
             fontsize=5, fontfamily="serif", color=BLUE,
             alpha=0.3, fontweight="bold")
ax_right.text(0, 3.5, "IMPLEMENTATION", ha="center", va="center",
             fontsize=5, fontfamily="serif", color=AMBER,
             alpha=0.3, fontweight="bold")

ax_right.text(0, 4.0, "the inner cosmos", ha="center", va="center",
             fontsize=8, fontfamily="serif", fontstyle="italic",
             color=CHALK_DIM, alpha=0.35)

# --- Save ---
out_dir = FSPath(__file__).parent
out = out_dir / "the-descent.png"
fig.savefig(out, bbox_inches="tight", dpi=200, facecolor=fig.get_facecolor(),
            pad_inches=0.1)
print(f"Saved: {out}")
plt.close(fig)
