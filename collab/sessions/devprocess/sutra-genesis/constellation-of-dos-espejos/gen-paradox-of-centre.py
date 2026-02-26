#!/usr/bin/env python3
"""
The Paradox of the Centre — illustration for The Constellation of Doridhar, Ch. VIII.

Four views of the same diamond. In each quadrant, the diamond is illuminated
from one direction: Measure (amber from left), Model (blue from above),
Manifest (terracotta from right), Evaluate (green from below). The centre
diamond — seen when no phase is active — is nearly invisible.

Usage:
    uv run --with matplotlib --with numpy python3 gen-paradox-of-centre.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path as FSPath

SLATE = "#12121e"
CHALK = "#e8e4d4"
CHALK_DIM = "#8a8678"

PHASES = {
    "measure":  {"colour": "#d4a574", "label": "MEASURE",  "angle": 180},
    "model":    {"colour": "#7eb8da", "label": "MODEL",    "angle": 90},
    "manifest": {"colour": "#c4836a", "label": "MANIFEST", "angle": 0},
    "evaluate": {"colour": "#a8d4a0", "label": "EVALUATE", "angle": 270},
}

rng = np.random.default_rng(42)


def hex_to_rgba(h, a=1.0):
    r, g, b = [int(h[i:i+2], 16) / 255.0 for i in (1, 3, 5)]
    return (r, g, b, a)


def draw_diamond(ax, cx, cy, r, highlight_angle=None, highlight_colour=None):
    """Draw a brilliant-cut diamond from above.

    highlight_angle: angle (degrees) of the illumination source.
        The facets facing that direction brighten; opposite facets dim.
    """
    table_r = r * 0.38
    star_r = r * 0.75
    kite_r = r * 1.2

    # 8 table vertices
    table = [(cx + table_r * np.cos(np.radians(22.5 + i*45)),
              cy + table_r * np.sin(np.radians(22.5 + i*45))) for i in range(8)]

    # 4 star tips at cardinals (right=0, up=90, left=180, down=270)
    star_angles = [0, 90, 180, 270]
    stars = [(cx + star_r * np.cos(np.radians(a)),
              cy + star_r * np.sin(np.radians(a))) for a in star_angles]

    # 4 kite tips at intercardinals
    kite_angles = [45, 135, 225, 315]
    kites = [(cx + kite_r * np.cos(np.radians(a)),
              cy + kite_r * np.sin(np.radians(a))) for a in kite_angles]

    # Draw table octagon
    if highlight_angle is None:
        table_alpha = 0.06
        table_col = CHALK
    else:
        table_alpha = 0.12
        table_col = highlight_colour or CHALK

    txs = [v[0] for v in table] + [table[0][0]]
    tys = [v[1] for v in table] + [table[0][1]]
    ax.fill(txs, tys, color=table_col, alpha=table_alpha * 0.8)
    ax.plot(txs, tys, color=table_col, lw=0.5, alpha=table_alpha * 1.5)

    # Each quadrant has 2 facets (star-adjacent and kite-adjacent)
    # Quadrants indexed by their star-tip angle: 0=right, 90=up, 180=left, 270=down
    quadrant_data = [
        (0,   stars[0], kites[0], kites[3], 7, 0, 1),   # right: T7, T0, S0, K0, K3
        (90,  stars[1], kites[0], kites[1], 1, 2, 3),   # up:    T1, T2, S1, K0, K1
        (180, stars[2], kites[1], kites[2], 3, 4, 5),   # left:  T3, T4, S2, K1, K2
        (270, stars[3], kites[2], kites[3], 5, 6, 7),   # down:  T5, T6, S3, K2, K3
    ]

    for q_angle, s, k_cw, k_ccw, t_a, t_b, t_c in quadrant_data:
        # How far is this quadrant from the highlight?
        if highlight_angle is not None:
            angle_diff = abs(((q_angle - highlight_angle) + 180) % 360 - 180)
            if angle_diff < 30:
                facet_alpha = 0.55
                edge_alpha = 0.7
            elif angle_diff < 100:
                facet_alpha = 0.25
                edge_alpha = 0.35
            else:
                facet_alpha = 0.08
                edge_alpha = 0.12
            col = highlight_colour
        else:
            facet_alpha = 0.04
            edge_alpha = 0.06
            col = CHALK

        # Facet A: star-adjacent (table[t_a], table[t_b], star-tip, kite_cw)
        fa = [table[t_a], table[t_b], s, k_cw]
        fax = [v[0] for v in fa]
        fay = [v[1] for v in fa]
        ax.fill(fax, fay, color=col, alpha=facet_alpha * 0.4)

        # Facet B: kite-adjacent (table[t_b], table[t_c], kite_ccw, star-tip)
        fb = [table[t_b], table[t_c], k_ccw, s]
        fbx = [v[0] for v in fb]
        fby = [v[1] for v in fb]
        ax.fill(fbx, fby, color=col, alpha=facet_alpha * 0.3)

        # Facet edges
        edges = [
            (table[t_a], s), (s, table[t_b]), (table[t_b], k_cw),
            (table[t_b], k_ccw), (k_ccw, table[t_c]), (s, table[t_c]),
            (table[t_a], k_cw), (k_ccw, s),
        ]
        for (x0, y0), (x1, y1) in edges:
            ax.plot([x0, x1], [y0, y1], color=col, lw=0.5, alpha=edge_alpha)

    # Ridge lines from center to star tips
    for s in stars:
        ridge_col = highlight_colour if highlight_angle is not None else CHALK
        ax.plot([cx, s[0]], [cy, s[1]], color=ridge_col,
                lw=0.4, alpha=0.15 if highlight_angle is None else 0.3)


# ---------------------------------------------------------------------------
# Figure: 2x2 grid plus central ghost
# ---------------------------------------------------------------------------

fig = plt.figure(figsize=(10, 10), dpi=200)
fig.patch.set_facecolor(SLATE)

# Central panel (ghost diamond — nearly invisible)
ax_centre = fig.add_axes([0.35, 0.35, 0.3, 0.3])
ax_centre.set_facecolor(SLATE)
ax_centre.set_xlim(-2, 2)
ax_centre.set_ylim(-2, 2)
ax_centre.set_aspect("equal")
ax_centre.axis("off")

# Chalk dust
n_dust = 200
ddx = rng.uniform(-1.8, 1.8, n_dust)
ddy = rng.uniform(-1.8, 1.8, n_dust)
dds = rng.uniform(0.1, 0.8, n_dust)
ax_centre.scatter(ddx, ddy, s=dds, c=CHALK, alpha=0.02, edgecolors="none")

draw_diamond(ax_centre, 0, 0, 1.0, highlight_angle=None)
ax_centre.text(0, -1.7, "no light", ha="center", va="center",
              fontsize=6, fontfamily="serif", fontstyle="italic",
              color=CHALK_DIM, alpha=0.25)

# Four quadrant panels
positions = [
    (0.02, 0.52, "measure"),   # top-left
    (0.52, 0.52, "model"),     # top-right
    (0.02, 0.02, "evaluate"),  # bottom-left
    (0.52, 0.02, "manifest"),  # bottom-right
]

for (px, py, phase) in positions:
    ax = fig.add_axes([px, py, 0.46, 0.46])
    ax.set_facecolor(SLATE)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")

    info = PHASES[phase]

    # Chalk dust
    ddx = rng.uniform(-2, 2, 300)
    ddy = rng.uniform(-2, 2, 300)
    dds = rng.uniform(0.1, 1.0, 300)
    ax.scatter(ddx, ddy, s=dds, c=CHALK, alpha=0.02, edgecolors="none")

    # Draw the illuminated diamond
    draw_diamond(ax, 0, 0, 1.0,
                 highlight_angle=info["angle"],
                 highlight_colour=info["colour"])

    # Light source indicator — small bright dot at the source direction
    src_x = 1.8 * np.cos(np.radians(info["angle"]))
    src_y = 1.8 * np.sin(np.radians(info["angle"]))
    for r_g in [0.25, 0.15, 0.08]:
        c = plt.Circle((src_x, src_y), r_g, color=info["colour"],
                       alpha=0.15, fill=True)
        ax.add_patch(c)
    ax.plot(src_x, src_y, "o", color=info["colour"],
            markersize=5, alpha=0.8, zorder=10)

    # Phase label
    ax.text(0, -2.0, info["label"], ha="center", va="center",
            fontsize=7, fontfamily="serif", color=info["colour"],
            alpha=0.5, fontweight="bold")

# Subtle frame separators
for y in [0.5]:
    line = plt.Line2D([0.04, 0.96], [y, y], transform=fig.transFigure,
                      color=CHALK_DIM, lw=0.3, alpha=0.1)
    fig.add_artist(line)
for x in [0.5]:
    line = plt.Line2D([x, x], [0.04, 0.96], transform=fig.transFigure,
                      color=CHALK_DIM, lw=0.3, alpha=0.1)
    fig.add_artist(line)

# Title
fig.text(0.5, 0.97, "The Paradox of the Centre", ha="center", va="top",
         fontsize=10, fontfamily="serif", color=CHALK, alpha=0.35,
         fontweight="bold")
fig.text(0.5, 0.945, "four lights, one diamond — visible only from a direction",
         ha="center", va="top", fontsize=7, fontfamily="serif",
         color=CHALK_DIM, alpha=0.25, fontstyle="italic")

# --- Save ---
out_dir = FSPath(__file__).parent
out = out_dir / "paradox-of-centre.png"
fig.savefig(out, bbox_inches="tight", dpi=200, facecolor=fig.get_facecolor(),
            pad_inches=0.1)
print(f"Saved: {out}")
plt.close(fig)
