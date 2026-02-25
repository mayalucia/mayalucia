#!/usr/bin/env python3
"""
The Stone on the Grooved Board — illustration for The Logbook of the Unnamed River, Ch. VI.

A grooved board representing the archive timeline. A stone (the read cursor / HEAD)
marks where the last weaver stopped reading. Cords before the stone are faded (already
absorbed). Cords after the stone are vivid (unread, new water). A river flows beneath.

Usage:
    uv run --with matplotlib --with numpy python3 gen-stone-on-board.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Circle
from matplotlib.path import Path
import matplotlib.patches as mpatches
from pathlib import Path as FSPath

PARCHMENT = "#f4e8c1"
rng = np.random.default_rng(2026)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def hand_line(x0, y0, x1, y1, n=60, jitter=0.003):
    t = np.linspace(0, 1, n)
    x = x0 + (x1 - x0) * t + rng.normal(0, jitter, n)
    y = y0 + (y1 - y0) * t + rng.normal(0, jitter, n)
    return x, y


def hand_curve(pts, n=120, jitter=0.002):
    pts = np.array(pts)
    total = len(pts) - 1
    per_seg = max(n // total, 2)
    xs, ys = [], []
    for i in range(total):
        t = np.linspace(0, 1, per_seg, endpoint=(i == total - 1))
        xs.append(pts[i, 0] + (pts[i + 1, 0] - pts[i, 0]) * t)
        ys.append(pts[i, 1] + (pts[i + 1, 1] - pts[i, 1]) * t)
    x = np.concatenate(xs) + rng.normal(0, jitter, sum(len(a) for a in xs))
    y = np.concatenate(ys) + rng.normal(0, jitter, sum(len(a) for a in ys))
    return x, y


def wavy_cord_simple(ax, x0, y0, length, color, lw=1.5, alpha=1.0):
    """A short vertical cord hanging from a point, with a knot or two."""
    y1 = y0 - length
    wobble = length * 0.04
    cx1 = x0 + rng.uniform(-wobble, wobble)
    cy1 = y0 + (y1 - y0) * 0.33
    cx2 = x0 + rng.uniform(-wobble, wobble)
    cy2 = y0 + (y1 - y0) * 0.66
    verts = [(x0, y0), (cx1, cy1), (cx2, cy2), (x0 + rng.uniform(-0.05, 0.05), y1)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    path = Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor="none", edgecolor=color,
                               lw=lw, capstyle="round", alpha=alpha)
    ax.add_patch(patch)
    # Add 1-2 knots
    for frac in rng.uniform(0.3, 0.8, rng.integers(1, 3)):
        p = np.array(verts[0]) * (1 - frac)**3 + \
            3 * np.array(verts[1]) * (1 - frac)**2 * frac + \
            3 * np.array(verts[2]) * (1 - frac) * frac**2 + \
            np.array(verts[3]) * frac**3
        ax.plot(p[0], p[1], "o", color=color, markersize=3 * lw / 1.5,
                zorder=5, alpha=alpha)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 10), dpi=200)
fig.patch.set_facecolor(PARCHMENT)
ax.set_facecolor(PARCHMENT)
ax.set_xlim(-0.5, 14.5)
ax.set_ylim(-7.5, 4.0)
ax.set_aspect("equal")
ax.axis("off")

# --- Title ---
ax.text(7.0, 3.4, "The Stone on the Grooved Board", ha="center", va="bottom",
        fontsize=14, fontfamily="serif", fontweight="bold", color="#3e2a1a")
ax.text(7.0, 2.9, "the read cursor", ha="center", va="bottom",
        fontsize=9, fontfamily="serif", fontstyle="italic", color="#6a5a4a")

# --- The grooved board (shelf) ---
board_y = 1.8
board_x0 = 1.0
board_x1 = 13.0
board_width = 0.35

# Wood grain effect
for i in range(8):
    grain_y = board_y - board_width * 0.1 + i * (board_width / 8)
    gx, gy = hand_line(board_x0, grain_y, board_x1, grain_y,
                       n=200, jitter=0.008)
    ax.plot(gx, gy, color="#8b6914", lw=0.4, alpha=0.25)

# Board edges
bx_top, by_top = hand_line(board_x0, board_y, board_x1, board_y,
                           n=100, jitter=0.004)
bx_bot, by_bot = hand_line(board_x0, board_y - board_width,
                           board_x1, board_y - board_width,
                           n=100, jitter=0.004)
ax.plot(bx_top, by_top, color="#5c4a2f", lw=1.5)
ax.plot(bx_bot, by_bot, color="#5c4a2f", lw=1.5)

# Board fill
ax.fill_between(bx_top, by_top, board_y - board_width,
                color="#c9a050", alpha=0.35)

# Groove (darker line through center of board)
groove_y = board_y - board_width * 0.5
gx, gy = hand_line(board_x0 + 0.3, groove_y, board_x1 - 0.3, groove_y,
                   n=200, jitter=0.003)
ax.plot(gx, gy, color="#6b4a14", lw=2.0, alpha=0.5)
# Groove shadow
ax.plot(gx, gy - 0.02, color="#4a3010", lw=0.8, alpha=0.2)

# --- Notch marks along the groove ---
n_notches = 22
notch_xs = np.linspace(board_x0 + 0.6, board_x1 - 0.6, n_notches)
stone_position = 15  # stone is at notch 15 (0-indexed)

for i, nx in enumerate(notch_xs):
    ny = groove_y
    # Small tick mark
    tick_top = ny + 0.08
    tick_bot = ny - 0.08
    tx, ty = hand_line(nx, tick_top, nx, tick_bot, n=8, jitter=0.002)
    alpha = 0.3 if i < stone_position else 0.6
    ax.plot(tx, ty, color="#5c4a2f", lw=0.7, alpha=alpha)

# --- The Stone (at position 15) ---
stone_x = notch_xs[stone_position]
stone_y = groove_y + 0.02
# Draw as a rounded, slightly irregular oval
theta = np.linspace(0, 2 * np.pi, 80)
stone_rx = 0.22
stone_ry = 0.18
# Slight irregularity
sx = stone_x + stone_rx * np.cos(theta) * (1 + 0.08 * np.sin(3 * theta))
sy = stone_y + stone_ry * np.sin(theta) * (1 + 0.05 * np.cos(2 * theta))
ax.fill(sx, sy, color="#5a5a6a", alpha=0.85, zorder=8)
ax.plot(sx, sy, color="#3a3a4a", lw=1.0, zorder=8)
# Highlight
ax.plot(sx[:20], sy[:20] + 0.02, color="#8a8a9a", lw=0.6, alpha=0.5, zorder=9)
# Shadow
shadow_sx = stone_x + stone_rx * 1.05 * np.cos(theta)
shadow_sy = stone_y - 0.04 + stone_ry * 0.7 * np.sin(theta)
ax.fill(shadow_sx, shadow_sy, color="#3a3010", alpha=0.12, zorder=7)

# --- Label the stone ---
ax.annotate("HEAD", (stone_x, stone_y + stone_ry + 0.05),
            (stone_x, stone_y + 0.65),
            fontsize=8, fontfamily="serif", fontweight="bold",
            color="#3a3a4a", ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", color="#3a3a4a", lw=0.8),
            zorder=10)

# --- Cords hanging from the board ---
# Before stone: faded (already read)
# After stone: vivid (unread / new water)

cord_colors_read = ["#2c3e6b", "#8b3a3a", "#5a7a5a", "#c4a35a",
                    "#2c3e6b", "#8b3a3a", "#5a7a5a", "#2c3e6b",
                    "#c4a35a", "#8b3a3a", "#5a7a5a", "#2c3e6b",
                    "#8b3a3a", "#c4a35a", "#5a7a5a"]
cord_colors_unread = ["#2c3e6b", "#8b3a3a", "#5a7a5a", "#c4a35a",
                      "#2c3e6b", "#8b3a3a", "#5a7a5a"]

for i, nx in enumerate(notch_xs):
    if i >= len(cord_colors_read) + len(cord_colors_unread):
        break

    is_read = i < stone_position
    if is_read and i < len(cord_colors_read):
        color = cord_colors_read[i]
        alpha = 0.2 + 0.05 * (i / stone_position)  # fade older ones more
        lw = 1.0
        cord_len = rng.uniform(2.0, 3.5)
    elif not is_read:
        idx = i - stone_position
        if idx < len(cord_colors_unread):
            color = cord_colors_unread[idx]
        else:
            color = "#2c3e6b"
        alpha = 0.85
        lw = 1.6
        cord_len = rng.uniform(2.5, 4.0)
    else:
        continue

    cord_top = board_y - board_width
    wavy_cord_simple(ax, nx, cord_top, cord_len, color, lw=lw, alpha=alpha)

# --- "already absorbed" / "new water" labels ---
mid_read = (notch_xs[0] + notch_xs[stone_position - 1]) / 2
mid_unread = (notch_xs[stone_position] + notch_xs[min(stone_position + 6, n_notches - 1)]) / 2

ax.text(mid_read, -4.8, "already absorbed\ninto the archive",
        ha="center", va="top", fontsize=7, fontfamily="serif",
        fontstyle="italic", color="#6a5a4a", alpha=0.5, linespacing=1.4)

ax.text(mid_unread, -4.8, "new water\nsince you were last here",
        ha="center", va="top", fontsize=7, fontfamily="serif",
        fontstyle="italic", color="#3e2a1a", linespacing=1.4)

# --- The River (flowing beneath) ---
river_y = -6.0
river_color = "#3b5998"

# Multiple braided channels
for channel_offset in [-0.3, 0.0, 0.25]:
    pts = []
    x_start = -0.5
    for seg in range(12):
        px = x_start + seg * 1.3
        py = river_y + channel_offset + rng.uniform(-0.15, 0.15)
        pts.append((px, py))
    rx, ry = hand_curve(pts, n=200, jitter=0.008)
    alpha = 0.3 if abs(channel_offset) > 0.1 else 0.45
    ax.plot(rx, ry, color=river_color, lw=1.2 if channel_offset == 0 else 0.7,
            alpha=alpha)

# River label
ax.text(7.0, river_y - 0.6, "\u015aatadru \u2014 the hundred-channelled one",
        ha="center", va="top", fontsize=7, fontfamily="serif",
        fontstyle="italic", color=river_color, alpha=0.5)

# --- Footnote ---
ax.text(7.0, -7.2,
        "The stone remembers for them.",
        ha="center", va="top", fontsize=8, fontfamily="serif",
        fontstyle="italic", color="#6a5a4a")

# --- Aging texture ---
n_specks = 500
spx = rng.uniform(-0.3, 14.3, n_specks)
spy = rng.uniform(-7.3, 3.8, n_specks)
sps = rng.uniform(0.2, 1.5, n_specks)
spa = rng.uniform(0.02, 0.08, n_specks)
ax.scatter(spx, spy, s=sps, c="#8b7355", alpha=spa, edgecolors="none")

# --- Save ---
out_dir = FSPath(__file__).parent
out = out_dir / "stone-on-board.png"
fig.savefig(out, bbox_inches="tight", dpi=200, facecolor=fig.get_facecolor(),
            pad_inches=0.15)
print(f"Saved: {out}")
plt.close(fig)
