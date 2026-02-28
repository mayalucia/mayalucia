#!/usr/bin/env python3
"""
The Glass Plate — illustration for The Constellation of Doridhar, Ch. II-IV.

A dark glass plate showing the constellation: four phase crystals at cardinal
positions (Platonic solid wireframes), provinces as blended-colour points of
light with connecting threads, the ghostly diamond at centre, all on a
chalk-dust ground.

Usage:
    uv run --with matplotlib --with numpy python3 gen-glass-plate.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, RegularPolygon, Circle
from matplotlib.path import Path
import matplotlib.patches as mpatches
from pathlib import Path as FSPath

# ---------------------------------------------------------------------------
# Palette (from the actual constellation browser)
# ---------------------------------------------------------------------------
SLATE = "#12121e"
CHALK = "#e8e4d4"
CHALK_DIM = "#8a8678"

PHASE_COLOURS = {
    "measure":  "#d4a574",   # warm amber
    "model":    "#7eb8da",   # cool blue
    "manifest": "#c4836a",   # terracotta
    "evaluate": "#a8d4a0",   # sage green
}

PROVINCE_COLOURS = {
    "observatory":    "#c4a06a",   # mostly amber + blue tint
    "lantern":        "#c48a72",   # mostly terracotta + blue tint
    "menagerie":      "#9aaa8a",   # blue-green blend
    "loom":           "#b0a87a",   # amber-blue blend
    "watershed":      "#bca87a",   # amber-gold
    "scriptorium":    "#dac87e",   # gold
    "thread":         "#c4c4c4",   # silver
    "constellation":  "#d4a0c4",   # mauve
}

rng = np.random.default_rng(2026)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def hex_to_rgb(h):
    return [int(h[i:i+2], 16) / 255.0 for i in (1, 3, 5)]

def draw_wireframe_octahedron(ax, cx, cy, r, color, alpha=0.7):
    """Octahedron projected to 2D — 6 vertices, 12 edges."""
    # Top, bottom, and 4 equatorial vertices
    verts = [
        (cx, cy + r),          # top
        (cx, cy - r),          # bottom
        (cx + r*0.7, cy),      # right
        (cx - r*0.7, cy),      # left
        (cx + r*0.25, cy + r*0.15),  # front-right (depth)
        (cx - r*0.25, cy - r*0.15),  # back-left (depth)
    ]
    edges = [(0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(1,5),
             (2,4),(4,3),(3,5),(5,2)]
    for i, j in edges:
        x = [verts[i][0], verts[j][0]]
        y = [verts[i][1], verts[j][1]]
        # Add slight jitter for hand-drawn feel
        x = np.array(x) + rng.normal(0, r*0.01, 2)
        y = np.array(y) + rng.normal(0, r*0.01, 2)
        ax.plot(x, y, color=color, lw=0.8, alpha=alpha * 0.7)
    # Glow at vertices
    for v in verts:
        ax.plot(v[0], v[1], "o", color=color, markersize=2, alpha=alpha)

def draw_wireframe_cube(ax, cx, cy, r, color, alpha=0.7):
    """Cube projected to 2D with slight perspective."""
    s = r * 0.6
    d = r * 0.3  # depth offset
    front = [(cx-s, cy-s), (cx+s, cy-s), (cx+s, cy+s), (cx-s, cy+s)]
    back = [(cx-s+d, cy-s+d), (cx+s+d, cy-s+d), (cx+s+d, cy+s+d), (cx-s+d, cy+s+d)]
    # Front face
    for i in range(4):
        j = (i+1) % 4
        ax.plot([front[i][0], front[j][0]], [front[i][1], front[j][1]],
                color=color, lw=0.8, alpha=alpha * 0.7)
    # Back face
    for i in range(4):
        j = (i+1) % 4
        ax.plot([back[i][0], back[j][0]], [back[i][1], back[j][1]],
                color=color, lw=0.5, alpha=alpha * 0.4)
    # Connecting edges
    for i in range(4):
        ax.plot([front[i][0], back[i][0]], [front[i][1], back[i][1]],
                color=color, lw=0.5, alpha=alpha * 0.5)
    for v in front:
        ax.plot(v[0], v[1], "o", color=color, markersize=2, alpha=alpha)

def draw_wireframe_dodecahedron(ax, cx, cy, r, color, alpha=0.7):
    """Simplified dodecahedron — two nested pentagons with connecting edges."""
    n = 5
    outer_r = r * 0.8
    inner_r = r * 0.45
    rot = -np.pi/2
    outer = [(cx + outer_r * np.cos(2*np.pi*i/n + rot),
              cy + outer_r * np.sin(2*np.pi*i/n + rot)) for i in range(n)]
    inner = [(cx + inner_r * np.cos(2*np.pi*i/n + rot + np.pi/n),
              cy + inner_r * np.sin(2*np.pi*i/n + rot + np.pi/n)) for i in range(n)]
    # Outer pentagon
    for i in range(n):
        j = (i+1) % n
        ax.plot([outer[i][0], outer[j][0]], [outer[i][1], outer[j][1]],
                color=color, lw=0.8, alpha=alpha * 0.7)
    # Inner pentagon
    for i in range(n):
        j = (i+1) % n
        ax.plot([inner[i][0], inner[j][0]], [inner[i][1], inner[j][1]],
                color=color, lw=0.6, alpha=alpha * 0.5)
    # Spokes
    for i in range(n):
        ax.plot([outer[i][0], inner[i][0]], [outer[i][1], inner[i][1]],
                color=color, lw=0.5, alpha=alpha * 0.5)
        ax.plot([outer[i][0], inner[(i-1)%n][0]], [outer[i][1], inner[(i-1)%n][1]],
                color=color, lw=0.5, alpha=alpha * 0.4)
    for v in outer + inner:
        ax.plot(v[0], v[1], "o", color=color, markersize=1.5, alpha=alpha)

def draw_wireframe_icosahedron(ax, cx, cy, r, color, alpha=0.7):
    """Simplified icosahedron — top cap, equatorial ring, bottom cap."""
    n = 5
    eq_r = r * 0.7
    cap_r = r * 0.35
    rot = -np.pi/2
    equator = [(cx + eq_r * np.cos(2*np.pi*i/n + rot),
                cy + eq_r * np.sin(2*np.pi*i/n + rot)) for i in range(n)]
    top = (cx, cy + r * 0.5)
    bottom = (cx, cy - r * 0.5)
    # Equatorial ring
    for i in range(n):
        j = (i+1) % n
        ax.plot([equator[i][0], equator[j][0]], [equator[i][1], equator[j][1]],
                color=color, lw=0.7, alpha=alpha * 0.6)
    # Top fan
    for i in range(n):
        ax.plot([top[0], equator[i][0]], [top[1], equator[i][1]],
                color=color, lw=0.5, alpha=alpha * 0.5)
    # Bottom fan
    for i in range(n):
        ax.plot([bottom[0], equator[i][0]], [bottom[1], equator[i][1]],
                color=color, lw=0.5, alpha=alpha * 0.5)
    ax.plot(top[0], top[1], "o", color=color, markersize=2.5, alpha=alpha)
    ax.plot(bottom[0], bottom[1], "o", color=color, markersize=2.5, alpha=alpha)
    for v in equator:
        ax.plot(v[0], v[1], "o", color=color, markersize=1.5, alpha=alpha)

def draw_diamond(ax, cx, cy, r, alpha=0.12):
    """Central brilliant-cut diamond — ghostly octagonal table + 8 crown facets."""
    # Table octagon
    n = 8
    table_r = r * 0.38
    star_r = r * 0.75
    kite_r = r * 1.4

    table_verts = [(cx + table_r * np.cos(np.radians(22.5 + i*45)),
                    cy + table_r * np.sin(np.radians(22.5 + i*45))) for i in range(n)]
    # Star tips at cardinals
    stars = {
        "right":  (cx + star_r, cy),
        "up":     (cx, cy + star_r),
        "left":   (cx - star_r, cy),
        "down":   (cx, cy - star_r),
    }
    # Kite tips at intercardinals
    kites = {
        "ur": (cx + kite_r * np.cos(np.radians(45)),  cy + kite_r * np.sin(np.radians(45))),
        "ul": (cx + kite_r * np.cos(np.radians(135)), cy + kite_r * np.sin(np.radians(135))),
        "dl": (cx + kite_r * np.cos(np.radians(225)), cy + kite_r * np.sin(np.radians(225))),
        "dr": (cx + kite_r * np.cos(np.radians(315)), cy + kite_r * np.sin(np.radians(315))),
    }

    # Draw table
    table_xs = [v[0] for v in table_verts] + [table_verts[0][0]]
    table_ys = [v[1] for v in table_verts] + [table_verts[0][1]]
    ax.fill(table_xs, table_ys, color=CHALK, alpha=alpha * 0.6)
    ax.plot(table_xs, table_ys, color=CHALK, lw=0.4, alpha=alpha)

    # Draw crown facet edges — lines from table vertices to star/kite tips
    phase_colors = [
        PHASE_COLOURS["manifest"],  # right
        PHASE_COLOURS["evaluate"],  # down
        PHASE_COLOURS["measure"],   # left
        PHASE_COLOURS["model"],     # up
    ]
    star_keys = ["right", "down", "left", "up"]
    kite_pairs = [("ur", "dr"), ("dr", "dl"), ("dl", "ul"), ("ul", "ur")]

    for qi in range(4):
        t0 = table_verts[(qi*2 + 7) % 8]
        t1 = table_verts[(qi*2) % 8]
        t2 = table_verts[(qi*2 + 1) % 8]
        s = stars[star_keys[qi]]
        k1 = kites[kite_pairs[qi][0]]
        k2 = kites[kite_pairs[qi][1]]
        col = phase_colors[qi]

        # Star-adjacent facet
        for edge in [(t0, s), (s, t1), (t0, k1), (t1, k2)]:
            ax.plot([edge[0][0], edge[1][0]], [edge[0][1], edge[1][1]],
                    color=col, lw=0.4, alpha=alpha * 1.5)
        # Kite-adjacent facet
        for edge in [(t1, k2), (t2, k2), (s, t1)]:
            ax.plot([edge[0][0], edge[1][0]], [edge[0][1], edge[1][1]],
                    color=col, lw=0.3, alpha=alpha * 1.0)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 12), dpi=200)
fig.patch.set_facecolor(SLATE)
ax.set_facecolor(SLATE)
ax.set_xlim(-7, 7)
ax.set_ylim(-7, 7)
ax.set_aspect("equal")
ax.axis("off")

# --- Chalk dust background ---
n_dust = 3000
dx = rng.uniform(-6.8, 6.8, n_dust)
dy = rng.uniform(-6.8, 6.8, n_dust)
ds = rng.uniform(0.1, 1.5, n_dust)
da = rng.uniform(0.01, 0.06, n_dust)
# Cluster dust more densely toward centre
dist = np.sqrt(dx**2 + dy**2)
da *= np.clip(1.0 - dist / 8.0, 0.3, 1.0)
ax.scatter(dx, dy, s=ds, c=CHALK, alpha=da, edgecolors="none")

# --- Central diamond (ghostly) ---
draw_diamond(ax, 0, 0, 2.0, alpha=0.14)

# --- Ambient glow at centre ---
for r_glow in np.linspace(0.2, 2.5, 12):
    circle = plt.Circle((0, 0), r_glow, color=CHALK,
                        alpha=0.015 * (1.0 - r_glow/2.5), fill=True)
    ax.add_patch(circle)

# --- Phase crystals at cardinal positions ---
crystal_r = 0.7
# Measure — left — octahedron
draw_wireframe_octahedron(ax, -5.0, 0, crystal_r, PHASE_COLOURS["measure"])
ax.text(-5.0, -crystal_r - 0.35, "MEASURE", ha="center", va="top",
        fontsize=6, fontfamily="serif", color=PHASE_COLOURS["measure"],
        alpha=0.6, fontweight="bold")

# Model — top — cube
draw_wireframe_cube(ax, 0, 4.5, crystal_r, PHASE_COLOURS["model"])
ax.text(0, 4.5 - crystal_r - 0.35, "MODEL", ha="center", va="top",
        fontsize=6, fontfamily="serif", color=PHASE_COLOURS["model"],
        alpha=0.6, fontweight="bold")

# Manifest — right — dodecahedron
draw_wireframe_dodecahedron(ax, 5.0, 0, crystal_r, PHASE_COLOURS["manifest"])
ax.text(5.0, -crystal_r - 0.35, "MANIFEST", ha="center", va="top",
        fontsize=6, fontfamily="serif", color=PHASE_COLOURS["manifest"],
        alpha=0.6, fontweight="bold")

# Evaluate — bottom — icosahedron
draw_wireframe_icosahedron(ax, 0, -4.5, crystal_r, PHASE_COLOURS["evaluate"])
ax.text(0, -4.5 - crystal_r - 0.35, "EVALUATE", ha="center", va="top",
        fontsize=6, fontfamily="serif", color=PHASE_COLOURS["evaluate"],
        alpha=0.6, fontweight="bold")

# --- Sight lines from diamond to phase crystals ---
for (px, py), col in [
    ((-5.0, 0), PHASE_COLOURS["measure"]),
    ((0, 4.5), PHASE_COLOURS["model"]),
    ((5.0, 0), PHASE_COLOURS["manifest"]),
    ((0, -4.5), PHASE_COLOURS["evaluate"]),
]:
    # Dashed ray from near centre to near crystal
    t_vals = np.linspace(0.25, 0.72, 40)
    ray_x = t_vals * px
    ray_y = t_vals * py
    ax.plot(ray_x, ray_y, color=col, lw=0.5, alpha=0.15,
            linestyle=(0, (5, 8)))

# --- Province nodes ---
provinces = [
    {"name": "Observatory", "glyph": "\u22A5", "x": -3.8, "y": -1.5,
     "color": PROVINCE_COLOURS["observatory"], "size": 10},
    {"name": "Lantern", "glyph": "\u25C8", "x": 3.5, "y": -1.2,
     "color": PROVINCE_COLOURS["lantern"], "size": 10},
    {"name": "Menagerie", "glyph": "\u25C7", "x": 2.0, "y": 2.5,
     "color": PROVINCE_COLOURS["menagerie"], "size": 9},
    {"name": "Loom", "glyph": "\u2042", "x": -2.5, "y": 2.0,
     "color": PROVINCE_COLOURS["loom"], "size": 9},
    {"name": "Watershed", "glyph": "\u25B3", "x": -1.8, "y": -3.0,
     "color": PROVINCE_COLOURS["watershed"], "size": 9},
    {"name": "Scriptorium", "glyph": "\u2605", "x": 1.5, "y": -3.5,
     "color": PROVINCE_COLOURS["scriptorium"], "size": 7},
    {"name": "Thread", "glyph": "\u2261", "x": -0.5, "y": 1.5,
     "color": PROVINCE_COLOURS["thread"], "size": 7},
    {"name": "Constellation", "glyph": "\u2726", "x": 3.2, "y": 3.0,
     "color": PROVINCE_COLOURS["constellation"], "size": 7},
]

for p in provinces:
    # Glow halo
    for r_h in [0.4, 0.25, 0.12]:
        c = plt.Circle((p["x"], p["y"]), r_h,
                       color=p["color"], alpha=0.05, fill=True)
        ax.add_patch(c)
    # Node dot
    ax.plot(p["x"], p["y"], "o", color=p["color"],
            markersize=p["size"], zorder=10,
            markeredgecolor=p["color"], markeredgewidth=0.5)
    # Glyph
    ax.text(p["x"], p["y"], p["glyph"], ha="center", va="center",
            fontsize=7, color=SLATE, fontweight="bold", zorder=11)
    # Label
    ax.text(p["x"], p["y"] - 0.5, p["name"], ha="center", va="top",
            fontsize=5.5, fontfamily="serif", color=p["color"],
            alpha=0.7, zorder=10)

# --- Connecting threads ---
edges = [
    ("Observatory", "Loom", 0.08),
    ("Observatory", "Watershed", 0.06),
    ("Lantern", "Menagerie", 0.08),
    ("Loom", "Menagerie", 0.06),
    ("Loom", "Watershed", 0.05),
    ("Thread", "Scriptorium", 0.05),
    ("Constellation", "Lantern", 0.06),
    ("Lantern", "Watershed", 0.05),
    ("Menagerie", "Thread", 0.04),
]

prov_by_name = {p["name"]: p for p in provinces}
for src_name, tgt_name, alpha in edges:
    src = prov_by_name[src_name]
    tgt = prov_by_name[tgt_name]
    n_pts = 40
    t = np.linspace(0, 1, n_pts)
    # Slight curve via midpoint offset
    mid_x = (src["x"] + tgt["x"]) / 2 + rng.uniform(-0.3, 0.3)
    mid_y = (src["y"] + tgt["y"]) / 2 + rng.uniform(-0.3, 0.3)
    ex = src["x"] * (1-t)**2 + 2 * mid_x * t * (1-t) + tgt["x"] * t**2
    ey = src["y"] * (1-t)**2 + 2 * mid_y * t * (1-t) + tgt["y"] * t**2
    ex += rng.normal(0, 0.02, n_pts)
    ey += rng.normal(0, 0.02, n_pts)
    # Blend colours
    src_rgb = np.array(hex_to_rgb(src["color"]))
    tgt_rgb = np.array(hex_to_rgb(tgt["color"]))
    for i in range(n_pts - 1):
        frac = i / (n_pts - 1)
        seg_rgb = src_rgb * (1 - frac) + tgt_rgb * frac
        seg_color = "#{:02x}{:02x}{:02x}".format(
            int(seg_rgb[0]*255), int(seg_rgb[1]*255), int(seg_rgb[2]*255))
        ax.plot(ex[i:i+2], ey[i:i+2], color=seg_color,
                lw=0.6, alpha=alpha)

# --- Title (subtle, at top) ---
ax.text(0, 6.5, "The Glass Plate", ha="center", va="center",
        fontsize=11, fontfamily="serif", color=CHALK, alpha=0.35,
        fontweight="bold")
ax.text(0, 6.0, "the constellation as seen from above, in the first building",
        ha="center", va="center", fontsize=7, fontfamily="serif",
        color=CHALK_DIM, alpha=0.3, fontstyle="italic")

# --- Edge vignette (dark fade at borders) ---
for margin in np.linspace(0.0, 0.5, 15):
    alpha_v = 0.08 * (1.0 - margin / 0.5)
    rect = plt.Rectangle((-7 + margin, -7 + margin),
                         14 - 2*margin, 14 - 2*margin,
                         fill=False, edgecolor=SLATE, lw=8,
                         alpha=alpha_v)
    ax.add_patch(rect)

# --- Save ---
out_dir = FSPath(__file__).parent
out = out_dir / "glass-plate.png"
fig.savefig(out, bbox_inches="tight", dpi=200, facecolor=fig.get_facecolor(),
            pad_inches=0.1)
print(f"Saved: {out}")
plt.close(fig)
