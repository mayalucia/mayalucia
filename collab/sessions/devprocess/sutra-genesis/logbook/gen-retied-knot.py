#!/usr/bin/env python3
"""
The Retied Knot — illustration for The Logbook of the Unnamed River, Ch. I.

Two hands have retied the same status knot on a cord. The image shows a single
pendant cord with two overlapping overhand knots at the same position — one in
warm brown (first weaver's hand), one in cooler umber (second weaver's hand).
The fiber tension is visibly different around the contested knot.

Usage:
    uv run --with matplotlib --with numpy python3 gen-retied-knot.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse
from matplotlib.path import Path
import matplotlib.patches as mpatches
from pathlib import Path as FSPath

PARCHMENT = "#f4e8c1"
rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# Helpers (from Thread Walkers family)
# ---------------------------------------------------------------------------

def hand_line(ax, x0, y0, x1, y1, n=60, jitter=0.003, **kwargs):
    t = np.linspace(0, 1, n)
    x = x0 + (x1 - x0) * t + rng.normal(0, jitter, n)
    y = y0 + (y1 - y0) * t + rng.normal(0, jitter, n)
    ax.plot(x, y, **kwargs)
    return x, y


def wavy_cord(ax, x0, y0, x1, y1, color, lw=2.0, alpha=1.0):
    dx = x1 - x0
    dy = y1 - y0
    length = np.hypot(dx, dy)
    wobble = length * 0.035
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
    p0, p1, p2, p3 = [np.array(v) for v in verts]
    return ((1 - t)**3 * p0 + 3*(1 - t)**2 * t * p1 +
            3*(1 - t) * t**2 * p2 + t**3 * p3)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 14), dpi=200)
fig.patch.set_facecolor(PARCHMENT)
ax.set_facecolor(PARCHMENT)
ax.set_xlim(-1, 11)
ax.set_ylim(-16, 3)
ax.set_aspect("equal")
ax.axis("off")

# --- Title ---
ax.text(5.0, 2.2, "The Retied Knot", ha="center", va="bottom",
        fontsize=16, fontfamily="serif", fontweight="bold", color="#3e2a1a")
ax.text(5.0, 1.6, "two hands on the same cord", ha="center", va="bottom",
        fontsize=10, fontfamily="serif", fontstyle="italic", color="#6a5a4a")

# --- Primary cord (horizontal, top) ---
n_seg = 80
px = np.linspace(0.5, 9.5, n_seg)
py = 0.8 + 0.04 * np.sin(np.linspace(0, 3 * np.pi, n_seg))
ax.plot(px, py, color="#3e2a1a", lw=5.0, solid_capstyle="round", zorder=3)
ax.plot(px, py + 0.025, color="#5a4030", lw=1.0, alpha=0.35, zorder=4)

# --- Three cords hanging ---
# Left cord: "pending" status knot — untouched reference
# Center cord: the retied knot — the problem
# Right cord: a clean "done" knot — what it should look like

cord_specs = [
    {"x": 2.5, "label": "untouched\n(pending)", "kind": "clean_pending"},
    {"x": 5.0, "label": "retied\n(contested)", "kind": "retied"},
    {"x": 7.5, "label": "fresh done\n(authoritative)", "kind": "clean_done"},
]

WARM_HAND = "#6b3a1a"    # first weaver — warm sienna
COOL_HAND = "#3a4a5a"    # second weaver — cool umber
CORD_COLOR = "#4a3520"
STATUS_PENDING = "#2c3e6b"    # indigo
STATUS_DONE = "#5a7a5a"       # sage

for spec in cord_specs:
    x0 = spec["x"]
    y0 = np.interp(x0, px, py)
    length = 12.0
    sway = rng.uniform(-0.15, 0.15)
    x1 = x0 + sway
    y1 = y0 - length

    # Draw main cord
    verts = wavy_cord(ax, x0, y0, x1, y1, CORD_COLOR, lw=2.2)

    # Address knot near top (small, all cords have one)
    addr_pt = point_on_bezier(verts, 0.08)
    ax.plot(addr_pt[0], addr_pt[1], "o", color="#2c3e6b", markersize=4.5, zorder=5)

    if spec["kind"] == "clean_pending":
        # Single tight overhand knot — status: pending
        knot_pt = point_on_bezier(verts, 0.45)
        ax.plot(knot_pt[0], knot_pt[1], "o", color=STATUS_PENDING,
                markersize=7, zorder=5, markeredgewidth=0.8,
                markeredgecolor=STATUS_PENDING)
        # Label
        ax.text(knot_pt[0] - 0.6, knot_pt[1], "pending",
                fontsize=6, fontfamily="serif", fontstyle="italic",
                color="#6a5a4a", ha="right", va="center")

    elif spec["kind"] == "retied":
        # THE CONTESTED KNOT — two overlapping knots, different tension
        knot_y_frac = 0.45
        knot_pt = point_on_bezier(verts, knot_y_frac)

        # First weaver's knot — slightly above, warm
        k1x = knot_pt[0] - 0.08
        k1y = knot_pt[1] + 0.12
        ax.plot(k1x, k1y, "o", color=WARM_HAND, markersize=8, zorder=5,
                markeredgewidth=1.0, markeredgecolor=WARM_HAND)
        # Tension lines radiating from first knot (tight, even)
        for angle in np.linspace(-30, 30, 5):
            rad = np.radians(angle - 90)
            dx = 0.35 * np.cos(rad)
            dy = 0.35 * np.sin(rad)
            hand_line(ax, k1x, k1y, k1x + dx, k1y + dy, n=20,
                     jitter=0.008, color=WARM_HAND, lw=0.4, alpha=0.3)

        # Second weaver's knot — slightly below, cool, overlapping
        k2x = knot_pt[0] + 0.08
        k2y = knot_pt[1] - 0.12
        ax.plot(k2x, k2y, "o", color=COOL_HAND, markersize=8, zorder=6,
                markeredgewidth=1.0, markeredgecolor=COOL_HAND)
        # Tension lines from second knot (looser, uneven)
        for angle in np.linspace(-40, 40, 5):
            rad = np.radians(angle - 90)
            dx = 0.4 * np.cos(rad) * rng.uniform(0.7, 1.3)
            dy = 0.4 * np.sin(rad) * rng.uniform(0.7, 1.3)
            hand_line(ax, k2x, k2y, k2x + dx, k2y + dy, n=20,
                     jitter=0.012, color=COOL_HAND, lw=0.4, alpha=0.3)

        # Bracket showing contested zone
        brace_y_top = k1y + 0.3
        brace_y_bot = k2y - 0.3
        brace_x = knot_pt[0] + 0.8
        hand_line(ax, brace_x, brace_y_top, brace_x, brace_y_bot,
                 n=30, jitter=0.005, color="#6a5a4a", lw=0.8, alpha=0.5)
        hand_line(ax, brace_x - 0.1, brace_y_top, brace_x, brace_y_top,
                 n=8, jitter=0.002, color="#6a5a4a", lw=0.8, alpha=0.5)
        hand_line(ax, brace_x - 0.1, brace_y_bot, brace_x, brace_y_bot,
                 n=8, jitter=0.002, color="#6a5a4a", lw=0.8, alpha=0.5)

        # Annotation
        ax.text(brace_x + 0.15, (brace_y_top + brace_y_bot) / 2,
                "two hands\nsame cord",
                fontsize=6.5, fontfamily="serif", fontstyle="italic",
                color="#6a5a4a", ha="left", va="center")

        # "done" labels in both hands
        ax.text(k1x - 0.4, k1y, "done",
                fontsize=5.5, fontfamily="serif", color=WARM_HAND,
                ha="right", va="center", fontstyle="italic")
        ax.text(k2x + 0.4, k2y, "done",
                fontsize=5.5, fontfamily="serif", color=COOL_HAND,
                ha="left", va="center", fontstyle="italic")

    elif spec["kind"] == "clean_done":
        # Single bowline released to slack — status: done
        knot_pt = point_on_bezier(verts, 0.45)
        # Looser, open loop shape
        theta = np.linspace(0, 1.8 * np.pi, 40)
        loop_r = 0.15
        lx = knot_pt[0] + loop_r * np.cos(theta) + rng.normal(0, 0.005, 40)
        ly = knot_pt[1] + loop_r * 0.6 * np.sin(theta) + rng.normal(0, 0.005, 40)
        ax.plot(lx, ly, color=STATUS_DONE, lw=1.8, alpha=0.85, zorder=5)
        ax.plot(knot_pt[0], knot_pt[1], "o", color=STATUS_DONE,
                markersize=5, zorder=6)
        ax.text(knot_pt[0] + 0.6, knot_pt[1], "done",
                fontsize=6, fontfamily="serif", fontstyle="italic",
                color="#6a5a4a", ha="left", va="center")

    # Content knots below status position
    for frac in [0.62, 0.75, 0.88]:
        pt = point_on_bezier(verts, frac)
        e = Ellipse((pt[0], pt[1]), width=0.09, height=0.22,
                    facecolor=CORD_COLOR, edgecolor=CORD_COLOR,
                    lw=0.6, zorder=5, alpha=0.7)
        ax.add_patch(e)

    # Label below cord
    bottom_pt = point_on_bezier(verts, 0.98)
    ax.text(bottom_pt[0], bottom_pt[1] - 0.5, spec["label"],
            ha="center", va="top", fontsize=7, fontfamily="serif",
            color="#4a3a2a", fontstyle="italic", linespacing=1.4)

# --- Legend for hand colors ---
legend_x, legend_y = 7.8, -13.5
legend_bg = FancyBboxPatch((legend_x - 0.3, legend_y - 1.2), 3.0, 1.8,
                           boxstyle="round,pad=0.12", facecolor=PARCHMENT,
                           edgecolor="#a09080", lw=0.7, zorder=6)
ax.add_patch(legend_bg)
ax.text(legend_x + 1.2, legend_y + 0.45, "Hands", ha="center", va="bottom",
        fontsize=7.5, fontfamily="serif", fontweight="bold", color="#3e2a1a",
        zorder=7)
for j, (label, col) in enumerate([("first weaver (monsoon)", WARM_HAND),
                                    ("second weaver (autumn)", COOL_HAND)]):
    yy = legend_y + 0.05 - 0.42 * j
    ax.plot([legend_x, legend_x + 0.35], [yy, yy], color=col, lw=2.5, zorder=7)
    ax.text(legend_x + 0.5, yy, label, va="center", fontsize=5.5,
            fontfamily="serif", color="#3e2a1a", zorder=7)

# --- Footnote ---
ax.text(5.0, -15.2,
        "A retied knot is not the same knot. The fibre remembers the tension.",
        ha="center", va="top", fontsize=7, fontfamily="serif",
        fontstyle="italic", color="#6a5a4a")

# --- Aging texture ---
n_specks = 400
sx = rng.uniform(-0.5, 10.5, n_specks)
sy = rng.uniform(-15.5, 2.5, n_specks)
ss = rng.uniform(0.2, 1.5, n_specks)
sa = rng.uniform(0.02, 0.08, n_specks)
ax.scatter(sx, sy, s=ss, c="#8b7355", alpha=sa, edgecolors="none")

# --- Save ---
out_dir = FSPath(__file__).parent
for ext in ("png",):
    out = out_dir / f"retied-knot.{ext}"
    fig.savefig(out, bbox_inches="tight", dpi=200, facecolor=fig.get_facecolor(),
                pad_inches=0.15)
    print(f"Saved: {out}")
plt.close(fig)
