#!/usr/bin/env python3
"""
The Borderlands Map — a night survey of the Doridhar valley.

A fictional cartographic illustration in the style of mountain survey maps
drawn by starlight. Landscape orientation — the river flows left (high) to
right (low). Contour ridgelines, named settlements with glyphs, tributaries
descending from top and bottom edges.

Usage:
    uv run --with matplotlib --with numpy --with scipy python3 gen-borderlands-map.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib.collections import LineCollection
from scipy.ndimage import gaussian_filter
from pathlib import Path as FSPath

rng = np.random.default_rng(2026)

# ---------------------------------------------------------------------------
# Canvas — landscape
# ---------------------------------------------------------------------------
W, H = 3200, 2000
DPI = 150

# ---------------------------------------------------------------------------
# Palette — earth tones: sepia ink on aged parchment
# ---------------------------------------------------------------------------
PAPER      = "#1a1610"   # deep umber — aged leather
INK_FAINT  = "#2e2820"   # ghostly contours
INK_MID    = "#4a3e30"   # mid contours — warm sepia
INK_BRIGHT = "#6a5840"   # prominent ridges — strong sepia
RIVER_BLUE = "#2a4838"   # slate-green river (mountain water)
RIVER_GLOW = "#3a6850"   # river highlight — jade green
SNOW_WHITE = "#c8c0b0"   # snow/ice — warm white
CHALK      = "#d4c8a8"   # settlement names — parchment gold
AMBER      = "#c89048"   # observatory markers — bright amber
TERRACOTTA = "#b86848"   # forge markers — kiln red
SAGE       = "#6a9860"   # court markers — mountain meadow
COOL_BLUE  = "#5888a0"   # workshop markers — grey-blue
ARCHIVE_OCHRE = "#a88850" # archive markers — old gold
GRID_LINE  = "#221e18"   # faint grid — barely there
PATH_GOLD  = "#8a6830"   # pilgrim paths — dusty gold

def hex_rgb(h):
    return np.array([int(h[i:i+2], 16)/255. for i in (1, 3, 5)])


# ---------------------------------------------------------------------------
# Terrain — contours now run roughly vertical (N-S ridges flanking the valley)
# with V-deflections where the river cuts through
# ---------------------------------------------------------------------------
def make_contour(x_base_frac, amplitude, n_bumps, seed):
    """A roughly vertical contour line (top to bottom of map)."""
    local_rng = np.random.default_rng(seed)
    y_arr = np.linspace(0, H, 500)
    x = np.full_like(y_arr, x_base_frac * W)
    for _ in range(n_bumps):
        cy = local_rng.uniform(0, H)
        sigma = local_rng.uniform(H * 0.08, H * 0.30)
        dx = local_rng.uniform(-amplitude, amplitude)
        x += dx * np.exp(-0.5 * ((y_arr - cy) / sigma) ** 2)
    noise = local_rng.normal(0, amplitude * 0.04, len(y_arr))
    noise = gaussian_filter(noise, sigma=4)
    x += noise
    return x, y_arr


# ---------------------------------------------------------------------------
# Gazetteer — x_frac: 0=left (high/west), 1=right (low/east)
#              y_frac: 0=top (north), 1=bottom (south)
# ---------------------------------------------------------------------------
PLACES = [
    # High places — observatories, left side near snowline
    (0.08, 0.28, "Khardung",   "observatory", "Highest point. Stellar survey station."),
    (0.14, 0.72, "Chhimkha",   "observatory", "Wind-scoured ridge. Transit instrument."),

    # The pass — far left
    (0.04, 0.50, "Rhotang La", "pass",        "The crossing to the western valleys."),

    # Mid-valley — workshops and the village
    (0.38, 0.45, "Doridhar",   "village",     "The cartographers' village. Thread-ridge."),
    (0.32, 0.62, "Thangspa",   "workshop",    "River terrace. Model-building workshop."),
    (0.42, 0.28, "Dramtse",    "workshop",    "Monastery-workshop. Instrument repair."),

    # Archives — in cliff faces
    (0.52, 0.18, "Takphu",     "archive",     "Rock cave. The plate archive."),
    (0.48, 0.78, "Barphu",     "archive",     "Overhang cave. Older collection."),

    # Forges — near confluences
    (0.62, 0.48, "Gorsem",     "forge",       "River junction. Glass and metal work."),
    (0.58, 0.72, "Koksar",     "forge",       "Side-valley confluence. Copper work."),

    # Courts — meadows
    (0.74, 0.38, "Dulchi",     "court",       "Alpine meadow. Seasonal evaluation court."),
    (0.70, 0.65, "Tseram",     "court",       "Moraine camp. Summer assemblies."),

    # Lower valley — gorge exit, far right
    (0.88, 0.52, "Phirtse",    "village",     "Gorge mouth. Last settlement before plains."),

    # Side passes
    (0.22, 0.12, "Changla",    "pass",        "Northern pass to Spiti."),
    (0.20, 0.88, "Lingkhor",   "village",     "Circuit-path settlement. Pilgrims rest."),
]

GLYPH_COLOURS = {
    "observatory": AMBER,
    "workshop":    COOL_BLUE,
    "forge":       TERRACOTTA,
    "court":       SAGE,
    "archive":     ARCHIVE_OCHRE,
    "village":     CHALK,
    "pass":        SNOW_WHITE,
}


# ---------------------------------------------------------------------------
# River — flows left to right with meander
# ---------------------------------------------------------------------------
def make_river(n=800):
    t = np.linspace(0, 1, n)
    x = W * (0.04 + 0.90 * t)
    meander_rng = np.random.default_rng(42)
    walk = np.cumsum(meander_rng.normal(0, 1.8, n))
    walk = gaussian_filter(walk, sigma=25)
    walk *= 100 / (np.abs(walk).max() + 1e-6)
    y = H * (0.50 + 0.03 * np.sin(t * 4 * np.pi)) + walk
    return x, y


def make_tributary(sx, sy, ex, ey, n=300, seed=100):
    """A mountain tributary — jagged random walk in both axes."""
    t = np.linspace(0, 1, n)
    local_rng = np.random.default_rng(seed)

    # Distance determines meander scale
    dist = np.hypot(ex - sx, ey - sy)
    amp = dist * 0.12  # meander amplitude ~12% of length

    # Random walk perpendicular to the flow direction
    # (applied to both x and y via the perpendicular vector)
    dx, dy = ex - sx, ey - sy
    length = np.hypot(dx, dy) + 1e-6
    perp_x, perp_y = -dy / length, dx / length  # perpendicular unit vector

    # Multi-scale meander: coarse wander + fine jitter
    walk_coarse = np.cumsum(local_rng.normal(0, 2.5, n))
    walk_coarse = gaussian_filter(walk_coarse, sigma=18)
    walk_coarse -= np.linspace(walk_coarse[0], walk_coarse[-1], n)  # pin endpoints
    walk_coarse *= amp / (np.abs(walk_coarse).max() + 1e-6)

    walk_fine = np.cumsum(local_rng.normal(0, 1.2, n))
    walk_fine = gaussian_filter(walk_fine, sigma=5)
    walk_fine -= np.linspace(walk_fine[0], walk_fine[-1], n)
    walk_fine *= (amp * 0.3) / (np.abs(walk_fine).max() + 1e-6)

    meander = walk_coarse + walk_fine

    # Along-flow jitter (streams don't descend at constant speed)
    along_jitter = np.cumsum(local_rng.normal(0, 0.5, n))
    along_jitter = gaussian_filter(along_jitter, sigma=12)
    along_jitter -= np.linspace(along_jitter[0], along_jitter[-1], n)
    along_jitter *= (amp * 0.15) / (np.abs(along_jitter).max() + 1e-6)

    x = sx + dx * t + perp_x * meander + (dx / length) * along_jitter
    y = sy + dy * t + perp_y * meander + (dy / length) * along_jitter
    return x, y


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
ROUTES = [
    ("Rhotang La", "Doridhar", "pilgrim"),
    ("Doridhar", "Thangspa", "trail"),
    ("Doridhar", "Dramtse", "trail"),
    ("Doridhar", "Takphu", "trail"),
    ("Thangspa", "Barphu", "trail"),
    ("Doridhar", "Gorsem", "pilgrim"),
    ("Gorsem", "Dulchi", "trail"),
    ("Gorsem", "Koksar", "trail"),
    ("Dulchi", "Phirtse", "pilgrim"),
    ("Tseram", "Koksar", "trail"),
    ("Chhimkha", "Lingkhor", "trail"),
    ("Lingkhor", "Doridhar", "pilgrim"),
    ("Khardung", "Changla", "trail"),
    ("Khardung", "Dramtse", "trail"),
    ("Chhimkha", "Rhotang La", "trail"),
]


# ---------------------------------------------------------------------------
# Draw
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(W / DPI, H / DPI), dpi=DPI)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.invert_yaxis()
ax.set_aspect("equal")
ax.axis("off")

# --- Faint grid ---
for gx in np.linspace(W * 0.03, W * 0.97, 16):
    ax.axvline(gx, color=GRID_LINE, linewidth=0.3, zorder=1)
for gy in np.linspace(H * 0.05, H * 0.95, 10):
    ax.axhline(gy, color=GRID_LINE, linewidth=0.3, zorder=1)

# --- Ridge shading — tonal gradient bands from river to edges ---
# North ridge: darker bands from river (y~0.44) toward top edge (y=0)
RIDGE_DARK  = "#201a14"   # slightly lighter than paper
RIDGE_MID   = "#2a2218"   # mid-altitude — warm brown
RIDGE_HIGH  = "#342a1e"   # high altitude — dark umber
n_bands = 10
y_arr_fill = np.linspace(0, W, 600)  # x-positions for fill

for i in range(n_bands):
    band_frac = i / n_bands  # 0 = near river, 1 = near edge
    # North ridge bands: from H*0.42 upward
    y_inner = H * (0.42 - 0.42 * band_frac)
    y_outer = H * (0.42 - 0.42 * (band_frac + 1.0 / n_bands))
    band_alpha = 0.06 + 0.12 * band_frac  # stronger toward edges
    rgb = hex_rgb(RIDGE_HIGH)
    ax.fill_between([0, W], [y_outer, y_outer], [y_inner, y_inner],
                    color=RIDGE_HIGH, alpha=band_alpha, zorder=1.5)
    # South ridge bands: from H*0.58 downward
    y_inner_s = H * (0.58 + 0.42 * band_frac)
    y_outer_s = H * (0.58 + 0.42 * (band_frac + 1.0 / n_bands))
    ax.fill_between([0, W], [y_inner_s, y_inner_s], [y_outer_s, y_outer_s],
                    color=RIDGE_HIGH, alpha=band_alpha, zorder=1.5)

# --- Contour lines (roughly vertical, flanking the river) ---
n_contours = 25  # denser

for i in range(n_contours):
    frac = i / n_contours
    x_base = 0.05 + 0.90 * frac
    amp = W * 0.028 * (1.0 + 0.8 * (1 - abs(frac - 0.15)))

    # Colour ramp: high ground bright, low ground faint
    if frac < 0.12:
        colour = INK_BRIGHT
    elif frac < 0.40:
        colour = INK_MID
    else:
        colour = INK_FAINT
    lw = 0.6 + 1.0 * (1 - frac)
    alpha = 0.30 + 0.50 * (1 - frac)

    # North ridge contour
    cx_top, cy_top = make_contour(x_base, amp, n_bumps=6, seed=3000 + i * 7)
    # Draw only above river corridor, fade near river
    for j in range(len(cy_top) - 1):
        if cy_top[j] > H * 0.44:
            continue
        if cy_top[j] > H * 0.32:
            alpha_j = alpha * max(0, (H * 0.44 - cy_top[j]) / (H * 0.12))
        else:
            alpha_j = alpha
        ax.plot(cx_top[j:j+2], cy_top[j:j+2], color=colour,
                linewidth=lw, alpha=alpha_j, zorder=2)

    # South ridge contour
    cx_bot, cy_bot = make_contour(x_base, amp, n_bumps=6, seed=4000 + i * 7)
    for j in range(len(cy_bot) - 1):
        if cy_bot[j] < H * 0.56:
            continue
        if cy_bot[j] < H * 0.68:
            alpha_j = alpha * max(0, (cy_bot[j] - H * 0.56) / (H * 0.12))
        else:
            alpha_j = alpha
        ax.plot(cx_bot[j:j+2], cy_bot[j:j+2], color=colour,
                linewidth=lw, alpha=alpha_j, zorder=2)

# --- Snow fields on the left (high ground) ---
for i in range(4):
    snow_y = np.linspace(0, H, 400)
    x_base = W * (0.06 - 0.012 * i)
    noise = rng.normal(0, W * 0.008, len(snow_y))
    noise = gaussian_filter(noise, sigma=10)
    snow_x = x_base + noise
    ax.fill_betweenx(snow_y, np.zeros_like(snow_y), snow_x,
                     color=SNOW_WHITE, alpha=0.04 - 0.008 * i, zorder=3)

# --- River — wide braided bed ---
rx, ry = make_river()
n_riv = len(rx)
t_riv = np.linspace(0, 1, n_riv)

# River bed half-width: narrow at source (left), wide downstream (right)
bed_half = 15 + 65 * t_riv ** 0.4   # 15px at source, ~80px at exit

# River bed fill — the gravel/sand corridor
bed_rng = np.random.default_rng(777)
# Irregular bed edges (north and south bank)
bank_noise_n = np.cumsum(bed_rng.normal(0, 0.8, n_riv))
bank_noise_n = gaussian_filter(bank_noise_n, sigma=15)
bank_noise_n *= 12 / (np.abs(bank_noise_n).max() + 1e-6)
bank_noise_s = np.cumsum(bed_rng.normal(0, 0.8, n_riv))
bank_noise_s = gaussian_filter(bank_noise_s, sigma=15)
bank_noise_s *= 12 / (np.abs(bank_noise_s).max() + 1e-6)

bed_north_y = ry - bed_half + bank_noise_n
bed_south_y = ry + bed_half + bank_noise_s

# Fill the bed — wet gravel tone, distinctly different from paper
RIVERBED = "#1a2820"   # dark moss — wet river gravel
ax.fill_between(rx, bed_north_y, bed_south_y,
                color=RIVERBED, alpha=0.7, zorder=4)
# Second layer — slightly warmer near the banks (dry gravel)
BANK_TONE = "#242018"   # dry gravel — sandy brown
bank_inner_n = ry - bed_half * 0.3 + bank_noise_n
bank_inner_s = ry + bed_half * 0.3 + bank_noise_s
ax.fill_between(rx, bed_north_y, bank_inner_n,
                color=BANK_TONE, alpha=0.3, zorder=4.2)
ax.fill_between(rx, bank_inner_s, bed_south_y,
                color=BANK_TONE, alpha=0.3, zorder=4.2)
# Bed edge lines (bank markers)
ax.plot(rx, bed_north_y, color=INK_BRIGHT, linewidth=0.7, alpha=0.40, zorder=4.5)
ax.plot(rx, bed_south_y, color=INK_BRIGHT, linewidth=0.7, alpha=0.40, zorder=4.5)

# Main channel — slightly off-centre, wandering within the bed
chan_offset = np.cumsum(bed_rng.normal(0, 0.6, n_riv))
chan_offset = gaussian_filter(chan_offset, sigma=20)
chan_offset *= 15 / (np.abs(chan_offset).max() + 1e-6)
chan_y = ry + chan_offset

# Main channel glow
ax.plot(rx, chan_y, color=RIVER_GLOW, linewidth=7, alpha=0.08, zorder=5)
ax.plot(rx, chan_y, color=RIVER_GLOW, linewidth=4, alpha=0.12, zorder=5)

# Main channel core (varying width)
widths = 1.5 + 3.5 * t_riv ** 0.5
points = np.array([rx, chan_y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
river_rgb = hex_rgb(RIVER_BLUE)
lc = LineCollection(segments, linewidths=widths[:-1],
                    colors=[(river_rgb[0], river_rgb[1], river_rgb[2],
                             0.50 + 0.35 * t)
                            for t in np.linspace(0, 1, len(segments))],
                    zorder=6)
ax.add_collection(lc)

# Secondary braids — thinner channels that split and rejoin
for braid_i in range(3):
    braid_seed = 800 + braid_i
    braid_rng = np.random.default_rng(braid_seed)
    b_offset = np.cumsum(braid_rng.normal(0, 1.0, n_riv))
    b_offset = gaussian_filter(b_offset, sigma=12)
    b_offset *= (bed_half * 0.6) / (np.abs(b_offset).max() + 1e-6)
    b_y = ry + b_offset
    # Only draw in downstream half where the bed is wide enough to braid
    start_idx = int(n_riv * (0.25 + 0.15 * braid_i))
    bx = rx[start_idx:]
    by = b_y[start_idx:]
    b_alpha = 0.18 + 0.08 * braid_i
    ax.plot(bx, by, color=RIVER_BLUE, linewidth=0.6, alpha=b_alpha, zorder=5.5)

# Gravel bars — small irregular shapes scattered in the bed
n_bars = 30
for _ in range(n_bars):
    bar_t = bed_rng.uniform(0.15, 0.95)
    bar_idx = int(bar_t * (n_riv - 1))
    bar_cx = rx[bar_idx] + bed_rng.uniform(-15, 15)
    bar_cy = ry[bar_idx] + bed_rng.uniform(-bed_half[bar_idx]*0.6,
                                            bed_half[bar_idx]*0.6)
    bar_w = bed_rng.uniform(4, 18) * (0.5 + bar_t)
    bar_h = bar_w * bed_rng.uniform(0.3, 0.7)
    n_verts = bed_rng.integers(5, 9)
    angles = np.sort(bed_rng.uniform(0, 2*np.pi, n_verts))
    bar_verts = [(bar_cx + bar_w * np.cos(a) * bed_rng.uniform(0.6, 1.0),
                  bar_cy + bar_h * np.sin(a) * bed_rng.uniform(0.6, 1.0))
                 for a in angles]
    ax.add_patch(Polygon(bar_verts, closed=True, fill=True,
                         facecolor="#2a2418", edgecolor=INK_FAINT,
                         linewidth=0.3, alpha=0.5, zorder=5.8))

# --- Tributaries (from top and bottom edges into river) ---
place_dict = {p[2]: (p[0] * W, p[1] * H) for p in PLACES}

# Tributaries — each flows from the map edge, past a settlement, to the river.
# (edge_x, edge_y, via_x, via_y, t_join_on_river, seed, name_for_debug)
# The "via" point is near the settlement the stream serves.
tribs = [
    # North-side streams (from top edge down to river)
    (W*0.10, 0,  W*0.08, H*0.28,  0.06,  301, "Khardung stream"),
    (W*0.22, 0,  W*0.22, H*0.12,  0.18,  302, "Changla stream"),
    (W*0.44, 0,  W*0.42, H*0.28,  0.40,  303, "Dramtse stream"),
    (W*0.54, 0,  W*0.52, H*0.18,  0.50,  304, "Takphu stream"),
    (W*0.72, 0,  W*0.74, H*0.38,  0.72,  305, "Dulchi stream"),
    # South-side streams (from bottom edge up to river)
    (W*0.16, H,  W*0.14, H*0.72,  0.12,  401, "Chhimkha stream"),
    (W*0.22, H,  W*0.20, H*0.88,  0.20,  402, "Lingkhor stream"),
    (W*0.50, H,  W*0.48, H*0.78,  0.48,  403, "Barphu stream"),
    (W*0.60, H,  W*0.58, H*0.72,  0.58,  404, "Koksar stream"),
    (W*0.72, H,  W*0.70, H*0.65,  0.70,  405, "Tseram stream"),
]
for edge_x, edge_y, via_x, via_y, t_join, seed, _name in tribs:
    idx = int(t_join * (len(rx) - 1))
    river_x, river_y = rx[idx], ry[idx]
    # Two-segment tributary: edge → via (settlement), via → river
    tx1, ty1 = make_tributary(edge_x, edge_y, via_x, via_y, n=180, seed=seed)
    tx2, ty2 = make_tributary(via_x, via_y, river_x, river_y, n=150, seed=seed+50)
    # Stitch them together
    tx = np.concatenate([tx1, tx2[1:]])
    ty = np.concatenate([ty1, ty2[1:]])
    # glow
    ax.plot(tx, ty, color=RIVER_GLOW, linewidth=2.5, alpha=0.06, zorder=4.5)
    # core
    ax.plot(tx, ty, color=RIVER_BLUE, linewidth=1.1, alpha=0.40, zorder=5)

# --- Paths / Routes ---
for from_name, to_name, style in ROUTES:
    if from_name not in place_dict or to_name not in place_dict:
        continue
    x0, y0 = place_dict[from_name]
    x1, y1 = place_dict[to_name]
    mid_x = (x0 + x1) / 2 + rng.uniform(-25, 25)
    mid_y = (y0 + y1) / 2 + rng.uniform(-25, 25)
    t = np.linspace(0, 1, 100)
    px = (1 - t)**2 * x0 + 2 * (1 - t) * t * mid_x + t**2 * x1
    py = (1 - t)**2 * y0 + 2 * (1 - t) * t * mid_y + t**2 * y1
    if style == "pilgrim":
        ax.plot(px, py, color=PATH_GOLD, linewidth=1.0, alpha=0.35,
                linestyle=(0, (8, 4)), zorder=7)
    else:
        ax.plot(px, py, color=INK_MID, linewidth=0.6, alpha=0.28,
                linestyle=(0, (3, 5)), zorder=7)

# --- Place markers ---
for xf, yf, name, ptype, desc in PLACES:
    px, py = xf * W, yf * H
    colour = GLYPH_COLOURS.get(ptype, CHALK)

    if ptype == "observatory":
        size = 14
        verts = [(px, py - size), (px + size * 0.7, py),
                 (px, py + size), (px - size * 0.7, py)]
        ax.add_patch(Polygon(verts, closed=True, fill=False,
                             edgecolor=colour, linewidth=1.4, alpha=0.85, zorder=10))
        ax.plot(px, py, 'o', color=colour, markersize=3, alpha=0.9, zorder=10)

    elif ptype == "workshop":
        size = 10
        verts = [(px - size, py - size), (px + size, py - size),
                 (px + size, py + size), (px - size, py + size)]
        ax.add_patch(Polygon(verts, closed=True, fill=False,
                             edgecolor=colour, linewidth=1.1, alpha=0.75, zorder=10))

    elif ptype == "forge":
        size = 12
        verts = [(px, py - size), (px + size * 0.87, py + size * 0.5),
                 (px - size * 0.87, py + size * 0.5)]
        ax.add_patch(Polygon(verts, closed=True, fill=False,
                             edgecolor=colour, linewidth=1.2, alpha=0.80, zorder=10))

    elif ptype == "court":
        ax.add_patch(Circle((px, py), 11, fill=False,
                            edgecolor=colour, linewidth=1.1, alpha=0.75, zorder=10))

    elif ptype == "archive":
        ax.add_patch(plt.Rectangle((px - 14, py - 6), 28, 12, fill=False,
                                   edgecolor=colour, linewidth=1.1,
                                   alpha=0.75, zorder=10))

    elif ptype == "pass":
        size = 12
        ax.plot([px - size, px, px + size],
                [py + size * 0.5, py - size * 0.5, py + size * 0.5],
                color=colour, linewidth=1.5, alpha=0.85, zorder=10)

    else:  # village
        ax.plot(px, py, 'o', color=colour, markersize=6, alpha=0.85, zorder=10)

    # Label — place to the right unless too far right
    if xf > 0.80:
        ha, lx = "right", px - 20
    else:
        ha, lx = "left", px + 20
    ly = py - 8 if yf > 0.15 else py + 16

    ax.text(lx, ly, name,
            fontsize=8, color=colour, alpha=0.85,
            fontfamily="serif", fontstyle="italic",
            ha=ha, va="center", zorder=11)

# --- Title cartouche (bottom-centre) ---
cart_y = H * 0.92
ax.plot([W * 0.30, W * 0.70], [cart_y - 18, cart_y - 18],
        color=INK_MID, linewidth=0.5, alpha=0.4, zorder=12)
ax.plot([W * 0.30, W * 0.70], [cart_y + 42, cart_y + 42],
        color=INK_MID, linewidth=0.5, alpha=0.4, zorder=12)

ax.text(W * 0.50, cart_y,
        "T H E   V A L L E Y   O F   D O R I D H A R",
        fontsize=13, color=CHALK, alpha=0.8,
        fontfamily="serif", fontweight="bold",
        ha="center", va="bottom", zorder=12)
ax.text(W * 0.50, cart_y + 26,
        "A Night Survey  \u00b7  From the Archive at Takphu",
        fontsize=8.5, color=INK_BRIGHT, alpha=0.65,
        fontfamily="serif", fontstyle="italic",
        ha="center", va="bottom", zorder=12)

# --- Legend (bottom-right) ---
leg_x = W * 0.85
leg_y = H * 0.90
legend_items = [
    ("Observatory", AMBER),
    ("Workshop",    COOL_BLUE),
    ("Forge",       TERRACOTTA),
    ("Court",       SAGE),
    ("Archive",     ARCHIVE_OCHRE),
]
for i, (label, colour) in enumerate(legend_items):
    ly = leg_y + i * 20
    ax.plot(leg_x, ly, 's', color=colour, markersize=4.5, alpha=0.75, zorder=12)
    ax.text(leg_x + 16, ly, label,
            fontsize=6.5, color=colour, alpha=0.65,
            fontfamily="serif", va="center", zorder=12)

# --- Compass rose (top-right) ---
cx, cy = W * 0.94, H * 0.08
arm = 28
ax.annotate("", xy=(cx, cy - arm), xytext=(cx, cy + arm),
            arrowprops=dict(arrowstyle="-|>", color=SNOW_WHITE,
                           lw=0.8, mutation_scale=8),
            zorder=12)
ax.text(cx, cy - arm - 10, "N", fontsize=7.5, color=SNOW_WHITE, alpha=0.7,
        ha="center", va="bottom", fontfamily="serif", zorder=12)

# --- Stars in the margins (less sky visible in landscape, so fewer) ---
n_stars = 120
star_x = rng.uniform(0, W, n_stars)
star_y = np.concatenate([rng.uniform(0, H * 0.12, n_stars // 2),
                         rng.uniform(H * 0.88, H, n_stars // 2)])
star_sizes = rng.uniform(0.2, 1.5, n_stars)
star_alpha = rng.uniform(0.1, 0.45, n_stars)
for sx, sy, ss, sa in zip(star_x, star_y, star_sizes, star_alpha):
    ax.plot(sx, sy, '.', color=SNOW_WHITE, markersize=ss, alpha=sa, zorder=1)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out = FSPath(__file__).parent / "borderlands-map.png"
fig.savefig(out, dpi=DPI, bbox_inches="tight",
            facecolor=PAPER, edgecolor="none", pad_inches=0.1)
plt.close(fig)
print(f"Saved \u2192 {out}  ({out.stat().st_size / 1024:.0f} KB)")
