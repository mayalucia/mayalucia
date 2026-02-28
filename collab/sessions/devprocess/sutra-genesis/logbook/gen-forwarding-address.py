#!/usr/bin/env python3
"""
The Forwarding Address — illustration for The Logbook of the Unnamed River, Ch. VIII.

The last cord in the old notation: addressed, statused, priority-marked.
Hung alone in an empty tray. The old post office closing.
Behind it, empty hooks where cords used to hang.

Usage:
    uv run --with matplotlib --with numpy python3 gen-forwarding-address.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.path import Path
import matplotlib.patches as mpatches
from pathlib import Path as FSPath

PARCHMENT = "#f4e8c1"
WOOD = "#a0804a"
WOOD_DARK = "#6b5030"
CORD_COLOR = "#3e2a1a"
rng = np.random.default_rng(2026)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def hand_line(x0, y0, x1, y1, n=60, jitter=0.003):
    t = np.linspace(0, 1, n)
    x = x0 + (x1 - x0) * t + rng.normal(0, jitter, n)
    y = y0 + (y1 - y0) * t + rng.normal(0, jitter, n)
    return x, y


def wavy_cord(ax, x0, y0, x1, y1, color, lw=2.0, alpha=1.0):
    dy = y1 - y0
    wobble = abs(dy) * 0.04
    cx1 = x0 + rng.uniform(-wobble, wobble)
    cy1 = y0 + dy * 0.33 + rng.uniform(-wobble * 0.5, wobble * 0.5)
    cx2 = x0 + rng.uniform(-wobble, wobble)
    cy2 = y0 + dy * 0.66 + rng.uniform(-wobble * 0.5, wobble * 0.5)
    verts = [(x0, y0), (cx1, cy1), (cx2, cy2), (x1, y1)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    path = Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor="none", edgecolor=color,
                               lw=lw, capstyle="round", alpha=alpha)
    ax.add_patch(patch)
    return verts


def point_on_bezier(verts, t):
    p0, p1, p2, p3 = [np.array(v) for v in verts]
    return ((1 - t)**3 * p0 + 3*(1 - t)**2 * t * p1 +
            3*(1 - t) * t**2 * p2 + t**3 * p3)


def draw_hook(ax, x, y, empty=True):
    """Small curved hook on the wall."""
    theta = np.linspace(0, np.pi * 0.8, 30)
    hx = x + 0.08 * np.cos(theta)
    hy = y - 0.12 * np.sin(theta)
    alpha = 0.25 if empty else 0.6
    ax.plot(hx, hy, color=WOOD_DARK, lw=1.2, alpha=alpha)
    if empty:
        # small dust mark below empty hook
        ax.plot(x, y - 0.18, ".", color="#8b7355", markersize=2, alpha=0.3)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 14), dpi=200)
fig.patch.set_facecolor(PARCHMENT)
ax.set_facecolor(PARCHMENT)
ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-14.5, 3.5)
ax.set_aspect("equal")
ax.axis("off")

# --- Title ---
ax.text(5.0, 3.0, "The Forwarding Address", ha="center", va="bottom",
        fontsize=15, fontfamily="serif", fontweight="bold", color="#3e2a1a")
ax.text(5.0, 2.4, "the last cord in the old notation",
        ha="center", va="bottom", fontsize=9, fontfamily="serif",
        fontstyle="italic", color="#6a5a4a")

# --- The Wall (background texture) ---
# Subtle stone/plaster texture
for _ in range(40):
    bx = rng.uniform(-0.5, 10.5)
    by = rng.uniform(-14, 3)
    br = rng.uniform(0.5, 2.0)
    circle = plt.Circle((bx, by), br, color="#b8a878",
                        alpha=rng.uniform(0.02, 0.06))
    ax.add_patch(circle)

# --- The Tray (wooden frame) ---
tray_left = 1.5
tray_right = 8.5
tray_top = 1.5
tray_bottom = -0.2

# Tray back
for i in range(5):
    gy = tray_top - i * 0.05
    gx, ggy = hand_line(tray_left, gy, tray_right, gy, n=100, jitter=0.005)
    ax.plot(gx, ggy, color=WOOD, lw=0.5, alpha=0.2)

# Tray edges
for (x0, y0, x1, y1) in [
    (tray_left, tray_top, tray_right, tray_top),      # top
    (tray_left, tray_bottom, tray_right, tray_bottom), # bottom
    (tray_left, tray_top, tray_left, tray_bottom),     # left
    (tray_right, tray_top, tray_right, tray_bottom),   # right
]:
    lx, ly = hand_line(x0, y0, x1, y1, n=60, jitter=0.004)
    ax.plot(lx, ly, color=WOOD_DARK, lw=1.8)

# Tray fill
ax.fill([tray_left, tray_right, tray_right, tray_left],
        [tray_top, tray_top, tray_bottom, tray_bottom],
        color=WOOD, alpha=0.12)

# Label on tray
ax.text((tray_left + tray_right) / 2, tray_bottom - 0.3,
        "INCOMING", ha="center", va="top",
        fontsize=6, fontfamily="serif", fontweight="bold",
        color=WOOD_DARK, alpha=0.5)

# --- Empty hooks on the wall above ---
hook_y = 2.0
for i, hx in enumerate(np.linspace(2.0, 8.0, 9)):
    draw_hook(ax, hx, hook_y, empty=True)

# Ghost labels for where cords used to hang
ghost_labels = ["#1", "#2", "#3", "", "#5", "", "#7", "", ""]
for i, hx in enumerate(np.linspace(2.0, 8.0, 9)):
    if ghost_labels[i]:
        ax.text(hx, hook_y + 0.15, ghost_labels[i],
                ha="center", va="bottom", fontsize=5,
                fontfamily="serif", color="#8b7355", alpha=0.25)

# --- The Single Cord — the forwarding address ---
# Prominent, alone in the tray, in old v0 format
cord_x = 5.0
cord_y_start = tray_top - 0.15
cord_length = 11.0
cord_y_end = cord_y_start - cord_length

verts = wavy_cord(ax, cord_x, cord_y_start,
                  cord_x + rng.uniform(-0.2, 0.2), cord_y_end,
                  CORD_COLOR, lw=2.8)

# --- v0 format knots on the cord ---
# 1. Address knot cluster (top) — "to: every workshop"
addr_frac = 0.06
addr_pt = point_on_bezier(verts, addr_frac)
# Multiple small knots = "every workshop"
for offset in [-0.12, -0.04, 0.04, 0.12]:
    ax.plot(addr_pt[0] + offset, addr_pt[1], "o", color="#2c3e6b",
            markersize=5, zorder=5)
ax.text(addr_pt[0] + 0.8, addr_pt[1],
        "to: every workshop",
        fontsize=7, fontfamily="serif", fontstyle="italic",
        color="#2c3e6b", ha="left", va="center")

# 2. Status knot — "pending" (tight overhand)
status_frac = 0.18
status_pt = point_on_bezier(verts, status_frac)
ax.plot(status_pt[0], status_pt[1], "o", color="#8b3a3a",
        markersize=9, zorder=5, markeredgewidth=1.2,
        markeredgecolor="#8b3a3a")
ax.text(status_pt[0] + 0.6, status_pt[1],
        "status: pending",
        fontsize=7, fontfamily="serif", fontstyle="italic",
        color="#8b3a3a", ha="left", va="center")

# 3. Priority knot — triple twist (the "read before weaving" mark)
priority_frac = 0.28
priority_pt = point_on_bezier(verts, priority_frac)
# Three tight twists
for dy_off in [-0.15, 0.0, 0.15]:
    twist_x = priority_pt[0]
    twist_y = priority_pt[1] + dy_off
    theta = np.linspace(0, 2 * np.pi, 30)
    tx = twist_x + 0.06 * np.cos(theta) + rng.normal(0, 0.002, 30)
    ty = twist_y + 0.06 * 0.5 * np.sin(theta) + rng.normal(0, 0.002, 30)
    ax.plot(tx, ty, color="#c4a35a", lw=1.4, zorder=5)
ax.text(priority_pt[0] + 0.6, priority_pt[1],
        "priority: read before weaving",
        fontsize=7, fontfamily="serif", fontstyle="italic",
        color="#c4a35a", ha="left", va="center")

# 4. The message body — content knots
body_start = 0.42
body_end = 0.85
n_body_knots = 12
for i in range(n_body_knots):
    frac = body_start + (body_end - body_start) * i / (n_body_knots - 1)
    pt = point_on_bezier(verts, frac)
    # Vary knot types
    if i % 3 == 0:
        # Long knot (ellipse)
        from matplotlib.patches import Ellipse as Ell
        e = Ell((pt[0], pt[1]), width=0.1, height=0.3,
                facecolor=CORD_COLOR, edgecolor=CORD_COLOR,
                lw=0.6, zorder=5, alpha=0.8)
        ax.add_patch(e)
    elif i % 3 == 1:
        # Overhand
        ax.plot(pt[0], pt[1], "o", color=CORD_COLOR, markersize=5, zorder=5)
    else:
        # Figure-8
        r = 0.05
        theta = np.linspace(0, 2 * np.pi, 40)
        denom = 1 + np.sin(theta)**2
        fx = r * 1.6 * np.cos(theta) / denom + pt[0]
        fy = r * 1.6 * np.cos(theta) * np.sin(theta) / denom + pt[1]
        ax.fill(fx, fy, color=CORD_COLOR, zorder=5, alpha=0.8)

# --- The message text (floating beside the cord, like a translation) ---
msg_x = 7.2
msg_y = point_on_bezier(verts, 0.50)[1]

msg_lines = [
    "The arrangement has changed.",
    "The trays are empty.",
    "The ledger is gone.",
    "",
    "There is a new archive,",
    "in a valley you have not visited,",
    "on a river you have not named.",
    "",
    "Ask the Thread Walker for the path.",
    "",
    "This is the last cord that will",
    "carry an address.",
]

for i, line in enumerate(msg_lines):
    ax.text(msg_x, msg_y - i * 0.42, line,
            fontsize=7.5, fontfamily="serif",
            fontstyle="italic" if line else "normal",
            color="#3e2a1a", ha="left", va="center",
            alpha=0.75 if line else 0)

# Connecting line from cord to message
mid_body_pt = point_on_bezier(verts, 0.55)
lx, ly = hand_line(mid_body_pt[0] + 0.15, mid_body_pt[1],
                   msg_x - 0.15, msg_y - 1.5,
                   n=40, jitter=0.008)
ax.plot(lx, ly, color="#6a5a4a", lw=0.5, alpha=0.3, linestyle="--")

# --- The crossed-out labels: old protocol artifacts ---
old_labels_y = -12.5
old_items = ["to:", "status:", "priority:"]
for i, label in enumerate(old_items):
    lx = 2.5 + i * 2.5
    ax.text(lx, old_labels_y, label, ha="center", va="center",
            fontsize=9, fontfamily="serif", color="#8b7355", alpha=0.35)
    # Strike-through
    slx, sly = hand_line(lx - 0.55, old_labels_y,
                         lx + 0.55, old_labels_y,
                         n=20, jitter=0.005)
    ax.plot(slx, sly, color="#8b3a3a", lw=1.5, alpha=0.45)

# Arrow from old to new
ax.annotate("", (8.5, old_labels_y), (7.8, old_labels_y),
            arrowprops=dict(arrowstyle="->", color="#5a7a5a",
                           lw=1.5, alpha=0.5))
ax.text(9.0, old_labels_y, "from:\ndate:\ntags:",
        ha="left", va="center", fontsize=8, fontfamily="serif",
        color="#5a7a5a", alpha=0.6, linespacing=1.5)

# --- Footnote ---
ax.text(5.0, -13.8,
        "The forwarding address on the door of the old post office,\n"
        "written in the old handwriting, in the old notation,\n"
        "by the last hand that would ever use it.",
        ha="center", va="top", fontsize=7.5, fontfamily="serif",
        fontstyle="italic", color="#6a5a4a", linespacing=1.6)

# --- Aging texture ---
n_specks = 500
spx = rng.uniform(-0.3, 10.3, n_specks)
spy = rng.uniform(-14.3, 3.3, n_specks)
sps = rng.uniform(0.2, 1.5, n_specks)
spa = rng.uniform(0.02, 0.08, n_specks)
ax.scatter(spx, spy, s=sps, c="#8b7355", alpha=spa, edgecolors="none")

# --- Save ---
out_dir = FSPath(__file__).parent
out = out_dir / "forwarding-address.png"
fig.savefig(out, bbox_inches="tight", dpi=200, facecolor=fig.get_facecolor(),
            pad_inches=0.15)
print(f"Saved: {out}")
plt.close(fig)
