#!/usr/bin/env python3
"""
The Traveller's Window — inspiration piece for The Constellation of Doridhar.

A moonlit night in the high Himalaya. A central peak silhouetted against the
Milky Way. The Parvati descends from the peak — a river carving its valley
downward like a careless but elegant goddess. Moonlight floods the scene,
catching snow, water, and the quartz in cliff faces.

Usage:
    uv run --with matplotlib --with numpy --with scipy python3 gen-travellers-window.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.ndimage import gaussian_filter, zoom
from pathlib import Path as FSPath

rng = np.random.default_rng(2026)

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
DEEP_SKY = "#06081a"
MID_SKY = "#0c1030"
MOONLIT_BLUE = "#1a2248"
SNOW = "#d0d8e8"
MOONLIGHT = "#c0c8e0"
ICE_BLUE = "#90a8c8"
GLACIER = "#7888a0"
DARK_ROCK = "#161618"
MID_ROCK = "#302828"
LIGHT_ROCK = "#403430"
WARM_ROCK = "#5a3828"
FOREST_DARK = "#081008"
FOREST_MID = "#0c160e"
FOREST_NEAR = "#101c14"
RIVER_JADE = "#2a5848"
MIST = "#283050"

def hex_rgb(h):
    return np.array([int(h[i:i+2], 16)/255. for i in (1, 3, 5)])


# ---------------------------------------------------------------------------
# Fractal noise for Milky Way
# ---------------------------------------------------------------------------
def fractal_noise_2d(shape, octaves=6, persistence=0.5, lacunarity=2.0, seed=0):
    local_rng = np.random.default_rng(seed)
    noise = np.zeros(shape, dtype=float)
    amplitude = 1.0
    frequency = 1.0
    for _ in range(octaves):
        small = (max(2, int(shape[0] / frequency)),
                 max(2, int(shape[1] / frequency)))
        raw = local_rng.standard_normal(small)
        scaled = zoom(raw, (shape[0] / small[0], shape[1] / small[1]), order=3)
        scaled = scaled[:shape[0], :shape[1]]
        noise += amplitude * scaled
        amplitude *= persistence
        frequency *= lacunarity
    noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-10)
    return noise


# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------
W, H = 2400, 3200
fig, ax = plt.subplots(figsize=(12, 16), dpi=200)
fig.patch.set_facecolor(DEEP_SKY)
ax.set_facecolor(DEEP_SKY)
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.axis("off")

# ---------------------------------------------------------------------------
# SKY gradient
# ---------------------------------------------------------------------------
sky_top = hex_rgb(DEEP_SKY)
sky_mid = hex_rgb(MID_SKY)
sky_horizon = hex_rgb(MOONLIT_BLUE)

for i, y in enumerate(np.linspace(H * 0.35, H, 500)):
    t = i / 500
    if t > 0.5:
        s = (t - 0.5) / 0.5
        colour = sky_mid * (1 - s) + sky_top * s
    else:
        s = t / 0.5
        colour = sky_horizon * (1 - s) + sky_mid * s
    ax.plot([0, W], [y, y], color=colour, lw=3.0, zorder=0)

# ---------------------------------------------------------------------------
# MILKY WAY — rasterized fractal noise, axis-aligned, composited via imshow
# ---------------------------------------------------------------------------
# The MW band runs diagonally. We'll build the noise in screen space,
# shaping it with a rotated Gaussian envelope + dark rift.

mw_pix_h = 800   # resolution of the noise field
mw_pix_w = 600
mw_noise = fractal_noise_2d((mw_pix_h, mw_pix_w), octaves=7,
                             persistence=0.55, seed=42)
# Boost clumpy structure
mw_noise = mw_noise ** 0.6

# Build the band envelope in screen coordinates
# The MW spans from lower-right to upper-left across the sky portion
# In noise-field coords: y = row (0=top of sky, mw_pix_h=bottom of sky zone)
#                        x = col (0=left, mw_pix_w=right)
ys_n = np.arange(mw_pix_h)
xs_n = np.arange(mw_pix_w)
XX, YY = np.meshgrid(xs_n, ys_n)

# Band center goes diagonally
band_angle = 25  # degrees from vertical
band_cx = mw_pix_w * 0.55  # center column
band_cy = mw_pix_h * 0.50
rad = np.radians(band_angle)
# Distance from band axis (rotated)
along = (XX - band_cx) * np.cos(rad) + (YY - band_cy) * np.sin(rad)
across = -(XX - band_cx) * np.sin(rad) + (YY - band_cy) * np.cos(rad)

band_sigma = mw_pix_w * 0.18
envelope = np.exp(-(across ** 2) / (2 * band_sigma ** 2))

# Dark rift — sinuous lane
rift_shift = 15 * np.sin(along * 2 * np.pi / mw_pix_h * 1.5)
rift_width = band_sigma * 0.22
rift = 1.0 - 0.65 * np.exp(-((across - rift_shift) ** 2) / (2 * rift_width ** 2))

# Star clouds — local density enhancements
cloud1 = 0.3 * np.exp(-((along - mw_pix_h*0.15)**2 + across**2) / (2 * (band_sigma*0.5)**2))
cloud2 = 0.2 * np.exp(-((along + mw_pix_h*0.2)**2 + (across - band_sigma*0.2)**2) / (2 * (band_sigma*0.4)**2))

mw_field = mw_noise * (envelope * rift + cloud1 + cloud2)
mw_field = np.clip(mw_field, 0, 1)

# Smooth slightly for nebulous glow
mw_field = gaussian_filter(mw_field, sigma=2.0)

# Build RGBA — warm blue-white colour
mw_rgba = np.zeros((mw_pix_h, mw_pix_w, 4))
mw_col = hex_rgb("#c8d0e4")
mw_rgba[:, :, 0] = mw_col[0]
mw_rgba[:, :, 1] = mw_col[1]
mw_rgba[:, :, 2] = mw_col[2]
mw_rgba[:, :, 3] = mw_field * 0.45  # visible but moonlit

# Moon washout — reduce alpha near the moon
# Moon in image coords: (moon_x_frac * mw_pix_w, (1 - moon_y_frac) * mw_pix_h)
# moon is at (0.35*W, 0.83*H), sky zone is H*0.35 to H
moon_col = int(0.35 * mw_pix_w)
moon_row = int((1.0 - (0.83 - 0.35) / 0.65) * mw_pix_h)
moon_dist = np.sqrt((XX - moon_col)**2 + (YY - moon_row)**2)
moon_fade = np.clip(moon_dist / 120 - 0.5, 0.15, 1.0)
mw_rgba[:, :, 3] *= moon_fade

# Display — covers the sky zone (y from H*0.35 to H), no rotation needed
# imshow origin='lower' means row 0 is at the bottom
ax.imshow(mw_rgba[::-1], extent=[0, W, H * 0.35, H],
          aspect="auto", interpolation="bilinear", zorder=1)

# ---------------------------------------------------------------------------
# MOON
# ---------------------------------------------------------------------------
moon_x, moon_y = W * 0.35, H * 0.83
moon_r = 50

for r_glow, a_glow in [(500, 0.008), (300, 0.015), (180, 0.025),
                         (100, 0.05), (65, 0.08)]:
    c = plt.Circle((moon_x, moon_y), r_glow, color=MOONLIGHT,
                   alpha=a_glow, fill=True, zorder=2)
    ax.add_patch(c)

c = plt.Circle((moon_x, moon_y), moon_r, color="#dce0f0",
               alpha=0.95, fill=True, zorder=3)
ax.add_patch(c)
for mx, my, mr, ma in [(moon_x-12, moon_y+8, 16, 0.25),
                         (moon_x+7, moon_y-4, 11, 0.2),
                         (moon_x-4, moon_y-12, 9, 0.2),
                         (moon_x+18, moon_y+10, 7, 0.15)]:
    c = plt.Circle((mx, my), mr, color="#b0b4c8", alpha=ma, fill=True, zorder=3)
    ax.add_patch(c)

# ---------------------------------------------------------------------------
# STARS — point stars over the MW (brighter ones only, moonlit sky)
# ---------------------------------------------------------------------------
n_stars = 800
sx = rng.uniform(30, W - 30, n_stars)
sy = rng.uniform(H * 0.40, H - 30, n_stars)
ss = rng.exponential(1.0, n_stars)
ss = np.clip(ss, 0.2, 6.0)

dist_moon = np.sqrt((sx - moon_x)**2 + (sy - moon_y)**2)
moon_wash = np.clip(dist_moon / 300 - 0.2, 0.08, 1.0)
s_alpha = np.clip(ss / 6.0 * 0.7 * moon_wash, 0.03, 0.75)

s_colors = []
for _ in range(n_stars):
    roll = rng.random()
    if roll < 0.55: s_colors.append("#dddcd4")
    elif roll < 0.75: s_colors.append(ICE_BLUE)
    elif roll < 0.88: s_colors.append("#d4a574")
    else: s_colors.append("#e8c8a0")

ax.scatter(sx, sy, s=ss * 2.5, c=s_colors, alpha=s_alpha,
           edgecolors="none", zorder=2)

# Bright stars with glow
for _ in range(12):
    bx = rng.uniform(80, W - 80)
    by = rng.uniform(H * 0.50, H - 60)
    d = np.sqrt((bx - moon_x)**2 + (by - moon_y)**2)
    if d < 180: continue
    bc = ["#e0dcd0", "#d4a574", ICE_BLUE][rng.integers(3)]
    for r in [5.0, 2.5, 1.0]:
        c = plt.Circle((bx, by), r, color=bc, alpha=0.05, fill=True, zorder=2)
        ax.add_patch(c)
    spike_l = rng.uniform(8, 16)
    for dx, dy in [(1, 0), (0, 1)]:
        ax.plot([bx - dx*spike_l, bx + dx*spike_l],
                [by - dy*spike_l, by + dy*spike_l],
                color=bc, lw=0.3, alpha=0.12, zorder=2)
    ax.plot(bx, by, "o", color=bc, markersize=rng.uniform(2, 3.5),
            alpha=0.85, zorder=3)

# ---------------------------------------------------------------------------
# TERRAIN HELPERS
# ---------------------------------------------------------------------------
x = np.arange(W)

def ridgeline(x, base, peaks, roughness_seed=0, roughness_amp=30):
    y = np.full_like(x, base, dtype=float)
    for cx, h, sigma in peaks:
        y += h * np.exp(-((x - cx) / sigma) ** 2)
    local_rng = np.random.default_rng(roughness_seed)
    for oct in range(8):
        freq = (oct + 1) * 2.5
        phase = local_rng.uniform(0, 2 * np.pi)
        amp = roughness_amp / (oct + 1) ** 1.2
        y += amp * np.sin(freq * x / W * 2 * np.pi + phase)
    y += local_rng.normal(0, 3, len(x))
    return y


# ---------------------------------------------------------------------------
# DISTANT PEAKS — atmospheric, snowy
# ---------------------------------------------------------------------------
dist_ridge = ridgeline(x, H * 0.50, [
    (W * 0.18, H * 0.13, W * 0.08),
    (W * 0.78, H * 0.11, W * 0.09),
    (W * 0.45, H * 0.06, W * 0.12),
], roughness_seed=100)

atm_col = hex_rgb(MOONLIT_BLUE) * 0.6 + hex_rgb(GLACIER) * 0.4
ax.fill_between(x, 0, dist_ridge, color=atm_col, alpha=0.35, zorder=4)
ax.fill_between(x, dist_ridge - 35, dist_ridge, color=SNOW, alpha=0.15, zorder=4)

# Mid-distance ridge
mid_ridge = ridgeline(x, H * 0.44, [
    (W * 0.12, H * 0.10, W * 0.10),
    (W * 0.82, H * 0.09, W * 0.09),
    (W * 0.48, H * 0.04, W * 0.14),
], roughness_seed=200)
ax.fill_between(x, 0, mid_ridge, color=hex_rgb("#1a2a22"), alpha=0.7, zorder=4)

# ---------------------------------------------------------------------------
# CENTRAL PEAK — bare rock above treeline, massive
# ---------------------------------------------------------------------------
peak_profile = ridgeline(x, H * 0.38, [
    (W * 0.48, H * 0.28, W * 0.060),   # Main spire — slightly left of center
    (W * 0.53, H * 0.22, W * 0.050),   # Secondary summit — right
    (W * 0.42, H * 0.16, W * 0.050),   # Left shoulder
    (W * 0.60, H * 0.17, W * 0.055),   # Right shoulder
    (W * 0.35, H * 0.08, W * 0.070),   # Far left buttress
    (W * 0.67, H * 0.07, W * 0.065),   # Far right buttress
    (W * 0.46, H * 0.05, W * 0.030),   # Rocky spur left
], roughness_seed=300, roughness_amp=80)

# Extra high-frequency crag detail on the peak — serrated skyline
crag_rng = np.random.default_rng(777)
for oct in range(8, 14):
    freq = oct * 3.5
    phase = crag_rng.uniform(0, 2 * np.pi)
    amp = 18 / (oct - 6) ** 1.0
    # Only apply where the peak is above treeline (rock zone)
    crag = amp * np.sin(freq * x / W * 2 * np.pi + phase)
    peak_profile += crag * np.clip((peak_profile - H * 0.44) / (H * 0.10), 0, 1)

# Treeline — below this, forest; above, bare rock
# Real treeline undulates — higher in sheltered gullies, lower on exposed ridges
treeline_base = H * 0.44
treeline_noise = 20 * np.sin(x / W * 12 * np.pi) + 15 * np.sin(x / W * 5 * np.pi)
treeline_noise += gaussian_filter(rng.normal(0, 8, W), sigma=12)
treeline = treeline_base + treeline_noise

# Rock mass above treeline
rock_profile = np.copy(peak_profile)
rock_profile = np.maximum(rock_profile, treeline)

# Fill bare rock — base dark, with moonlit faces
ax.fill_between(x, treeline, rock_profile,
                where=(rock_profile > treeline),
                color=DARK_ROCK, alpha=1.0, zorder=6)

# Moonlit rock — gradient from bright (left face) to dark (right face)
# Use the peak's own slope to determine where the ridge crest is:
# the crest is where slope changes from positive to negative (local maxima)
# For simplicity, use a smooth sigmoid centered on the peak summit x
peak_summit_x = x[np.argmax(peak_profile)]
# Moonlight factor: wide sigmoid, 1.0 on far left, 0.0 on far right
moon_factor = 1.0 / (1.0 + np.exp((x - peak_summit_x) / (W * 0.05)))

# Three overlapping fills to create gradient — lower alphas to avoid overbrightening
for alpha_mult, factor_thresh in [(0.18, 0.7), (0.12, 0.35), (0.06, 0.10)]:
    mask = (rock_profile > treeline) & (moon_factor > factor_thresh)
    ax.fill_between(x, treeline, rock_profile,
                    where=mask,
                    color=MID_ROCK, alpha=alpha_mult, zorder=6)

# Warm reddish tinge on the lit rock face — ochre/terracotta
# Warm reddish tinge — only on rock well above treeline, on moonlit face
exposed_rock = peak_profile > (treeline + 30)
warm_rock_mask = exposed_rock & (moon_factor > 0.4)
ax.fill_between(x, treeline + 30, peak_profile,
                where=warm_rock_mask,
                color=WARM_ROCK, alpha=0.15, zorder=6)
# Stronger warmth in the mid-zone between treeline and snow line
warm_mid_mask = exposed_rock & (moon_factor > 0.55) & (peak_profile > treeline + 50) & (peak_profile < H * 0.58)
ax.fill_between(x, treeline + 50, np.minimum(peak_profile, H * 0.58),
                where=warm_mid_mask,
                color="#6a4030", alpha=0.12, zorder=6)

# Rock strata — subtle horizontal bands
for band_y in np.arange(treeline_base + 40, H * 0.70, 60):
    for xi in range(0, W, 4):
        if peak_profile[xi] > band_y and band_y > treeline[xi]:
            ax.plot([xi, xi + 4], [band_y, band_y + rng.uniform(-2, 2)],
                    color=LIGHT_ROCK, lw=0.3, alpha=0.08, zorder=6)

# ---------------------------------------------------------------------------
# SNOW — on the upper peak, using fill_between for smooth coverage
# ---------------------------------------------------------------------------
snow_line = H * 0.56

# Snow is patchy — use noise to break it up
snow_noise = np.array([rng.uniform(-25, 25) for _ in range(W)])
snow_noise = gaussian_filter(snow_noise, sigma=15)
snow_boundary = snow_line + snow_noise

# Snow fill — base layer (shadow side, muted)
snow_mask = peak_profile > snow_boundary
ax.fill_between(x, snow_boundary, peak_profile,
                where=snow_mask,
                color=GLACIER, alpha=0.40, zorder=7)

# Moonlit snow — gradient using same sigmoid as rock
for alpha_val, factor_thresh in [(0.22, 0.7), (0.14, 0.35), (0.06, 0.10)]:
    mask = snow_mask & (moon_factor > factor_thresh)
    ax.fill_between(x, snow_boundary, peak_profile,
                    where=mask,
                    color=SNOW, alpha=alpha_val, zorder=7)

# Moonlit edge — bright rim on the left skyline of the peak
for xi in range(int(W * 0.36), int(W * 0.52)):
    if peak_profile[xi] > H * 0.52:
        slope = peak_profile[xi] - peak_profile[max(0, xi - 4)]
        if slope > 1.5:
            ax.plot(xi, peak_profile[xi], ".", color=MOONLIGHT,
                    markersize=1.0, alpha=0.3, zorder=8)

# ---------------------------------------------------------------------------
# VALLEY: multiple overlapping forested ridgelines + descending stream
# ---------------------------------------------------------------------------

# Cover the peak base below treeline with forest
peak_base_forest = np.minimum(peak_profile, treeline)
ax.fill_between(x, 0, peak_base_forest,
                where=(peak_base_forest > H * 0.10),
                color=FOREST_DARK, alpha=1.0, zorder=7)

# Deodar silhouette helper
def draw_deodar(ax, tx, ty, height, width, color="#050c06", alpha=0.9, zorder=12):
    n_tiers = rng.integers(3, 6)
    pts = [(tx, ty)]
    for i in range(n_tiers):
        t_frac = (i + 1) / n_tiers
        tw = width * (1 - t_frac * 0.65) * (0.7 + 0.5 * rng.random())
        th = ty + height * t_frac
        pts.append((tx - tw/2, ty + height * (t_frac - 0.4/n_tiers)))
        pts.append((tx, th))
        if i < n_tiers - 1:
            pts.append((tx + tw/2, ty + height * (t_frac - 0.4/n_tiers)))
    tree = Polygon(pts, closed=True, facecolor=color, edgecolor="none", alpha=alpha)
    ax.add_patch(tree)

# --- THE DESCENDING STREAM ---
# A single continuous torrent from peak base, meandering leftward,
# disappearing into thick forest about halfway down.

stream_n = 400
stream_t = np.linspace(0, 1, stream_n)
# y: from peak base (H*0.34) to roughly mid-valley (H*0.22) where it vanishes
stream_y = H * 0.34 * (1 - stream_t) + H * 0.22 * stream_t
# x: meanders leftward from center
stream_rng = np.random.default_rng(999)
meander_walk = np.cumsum(stream_rng.normal(0, 2.0, stream_n))
meander_walk = gaussian_filter(meander_walk, sigma=15)
meander_walk *= 150 / (np.abs(meander_walk).max() + 1e-6)
stream_x = (W * 0.50
            - 200 * stream_t ** 0.7
            + meander_walk
            + 80 * np.sin(stream_t * 2.5 * np.pi))
stream_x = np.clip(stream_x, 20, W - 20)
stream_width = 3 + 20 * stream_t ** 0.6
# Fade out toward the end — stream disappears into forest
stream_alpha = 0.85 * (1 - stream_t ** 1.5)

jade = hex_rgb(RIVER_JADE)
moon_c = hex_rgb(MOONLIGHT)

# --- OVERLAPPING FORESTED RIDGELINES ---
# Each ridge is a full-width (or partial) forested spur crossing the valley.
# They're drawn from back (high y, near treeline) to front (low y, near river),
# progressively obscuring the stream.

ridge_specs = [
    # (base_y, peaks, x_range, seed, colour, n_trees, zorder)
    # Ridge 1: high, full width — just below treeline
    (H * 0.36, [(W*0.25, 50, W*0.15), (W*0.70, 45, W*0.12)],
     (0, W), 500, FOREST_DARK, 50, 9),
    # Ridge 2: spur from the right, only goes halfway
    (H * 0.30, [(W*0.75, 55, W*0.18), (W*0.55, 35, W*0.10)],
     (int(W*0.40), W), 510, FOREST_MID, 35, 10),
    # Ridge 3: spur from the left, goes 2/3 across
    (H * 0.26, [(W*0.20, 50, W*0.14), (W*0.45, 40, W*0.12)],
     (0, int(W*0.65)), 520, FOREST_DARK, 40, 11),
    # Ridge 4: full width, lower
    (H * 0.21, [(W*0.35, 40, W*0.15), (W*0.65, 35, W*0.13), (W*0.50, 25, W*0.08)],
     (0, W), 530, FOREST_MID, 45, 12),
    # Ridge 5: spur from right, low
    (H * 0.17, [(W*0.60, 45, W*0.16), (W*0.80, 35, W*0.10)],
     (int(W*0.30), W), 540, FOREST_NEAR, 30, 13),
    # Ridge 6: final spur from left, just above the big river
    (H * 0.14, [(W*0.15, 35, W*0.12), (W*0.40, 30, W*0.10)],
     (0, int(W*0.55)), 550, FOREST_DARK, 25, 13),
]

# Collect ridge profiles for stream visibility testing
ridge_profiles = []  # list of (rx_array, ry_array, zorder)

for base_y, peaks, (x_start, x_end), seed, col, n_trees, zord in ridge_specs:
    rx = np.arange(x_start, x_end)
    ry = ridgeline(rx, base_y, peaks, roughness_seed=seed, roughness_amp=25)

    # Taper the ridge at its ends so it doesn't have a hard vertical cut
    taper_len = min(150, len(rx) // 4)
    if x_start > 0:
        # Taper left end down
        taper = np.linspace(0, 1, taper_len)
        ry[:taper_len] = ry[:taper_len] * taper + H * 0.05 * (1 - taper)
    if x_end < W:
        # Taper right end down
        taper = np.linspace(1, 0, taper_len)
        ry[-taper_len:] = ry[-taper_len:] * taper + H * 0.05 * (1 - taper)

    ridge_profiles.append((rx, ry, zord))

    # Fill the ridge
    ax.fill_between(rx, 0, ry, color=col, alpha=0.97, zorder=zord)

    # Deodar silhouettes along the top
    for _ in range(n_trees):
        tx = rng.uniform(x_start + 20, x_end - 20)
        ty = np.interp(tx, rx, ry) - 5
        if ty < H * 0.06:
            continue
        h = rng.uniform(15, 45)
        w = rng.uniform(7, 16)
        draw_deodar(ax, tx, ty, h, w, col, alpha=0.95, zorder=zord)

    # Moonlit tree tips on the ridge top (left-facing = moon-lit)
    for _ in range(n_trees // 3):
        tx = rng.uniform(x_start + 30, min(x_end - 30, W * 0.50))
        ty = np.interp(tx, rx, ry) + rng.uniform(0, 15)
        if ty < H * 0.06:
            continue
        ax.plot(tx, ty, ".", color=MOONLIGHT, markersize=rng.uniform(0.3, 1.0),
                alpha=rng.uniform(0.03, 0.08), zorder=zord)

# ---------------------------------------------------------------------------
# DRAW THE DESCENDING STREAM — simple, continuous, fading into forest
# ---------------------------------------------------------------------------
for i in range(stream_n):
    sx, sy, sw = stream_x[i], stream_y[i], stream_width[i]
    sa = stream_alpha[i]
    if sa < 0.02:
        continue
    moon_dist = np.sqrt((sx - moon_x)**2 + (sy - moon_y)**2)
    moon_reflect = np.clip(0.25 * np.exp(-moon_dist / 800), 0, 0.25)
    col = jade * (1 - moon_reflect) + moon_c * moon_reflect

    ax.plot([sx - sw/2, sx + sw/2], [sy, sy],
            color=col, lw=3.5, alpha=sa, zorder=13.5)
    # Moonlight center
    ax.plot([sx - sw*0.15, sx + sw*0.15], [sy, sy],
            color=MOONLIGHT, lw=1.2, alpha=sa * 0.15, zorder=13.5)
    if stream_rng.random() < 0.10:
        fx = sx + stream_rng.uniform(-sw * 0.3, sw * 0.3)
        ax.plot(fx, sy, ".", color=MOONLIGHT,
                markersize=stream_rng.uniform(1.0, 3.5),
                alpha=sa * 0.4, zorder=13.5)

# ---------------------------------------------------------------------------
# THE BIG RIVER — Parvati reappears as a torrent, flowing left to right
# ---------------------------------------------------------------------------
# Define the river path as upper and lower banks
big_x = np.arange(W)
# River center — gentle S-curve across the frame
big_cy = (H * 0.08
          + 20 * np.sin(big_x / W * 2.0 * np.pi + 0.5)
          + 8 * np.sin(big_x / W * 5.0 * np.pi)
          + 5 * np.sin(big_x / W * 9.0 * np.pi + 1.0))
# Width: powerful, undulating
big_hw = (30 + 12 * np.sin(big_x / W * 3 * np.pi)
          + 8 * np.exp(-((big_x / W - 0.5) / 0.25) ** 2) * 10)
big_upper = big_cy + big_hw
big_lower = big_cy - big_hw

# Solid river body — deep jade
ax.fill_between(big_x, big_lower, big_upper,
                color="#1a3830", alpha=0.90, zorder=14)
# Lighter jade layer in the center
ax.fill_between(big_x, big_cy - big_hw * 0.5, big_cy + big_hw * 0.5,
                color=RIVER_JADE, alpha=0.35, zorder=14)

# Moonlight reflection — bright band on the water surface
refl_w = big_hw * 0.35
ax.fill_between(big_x, big_cy - refl_w * 0.5, big_cy + refl_w * 0.5,
                color=MOONLIGHT, alpha=0.10, zorder=15)
# Second broader, dimmer reflection
ax.fill_between(big_x, big_cy - big_hw * 0.6, big_cy + big_hw * 0.6,
                color=ICE_BLUE, alpha=0.04, zorder=15)

# Rapids and foam — scattered bright flecks
for _ in range(500):
    fx = rng.uniform(0, W)
    fi = int(np.clip(fx, 0, W - 1))
    fy = rng.uniform(big_lower[fi], big_upper[fi])
    ax.plot(fx, fy, ".", color=MOONLIGHT,
            markersize=rng.uniform(0.3, 3.0),
            alpha=rng.uniform(0.05, 0.30), zorder=15)

# Bank edges — foam line
for _ in range(300):
    fx = rng.uniform(0, W)
    fi = int(np.clip(fx, 0, W - 1))
    side = rng.choice([-1, 1])
    if side == 1:
        fy = big_upper[fi] + rng.uniform(-2, 4)
    else:
        fy = big_lower[fi] + rng.uniform(-4, 2)
    ax.plot(fx, fy, ".", color="#4a7868",
            markersize=rng.uniform(0.3, 1.5),
            alpha=rng.uniform(0.06, 0.18), zorder=15)

# ---------------------------------------------------------------------------
# MIST in the valley
# ---------------------------------------------------------------------------
for y_band, a_base in [(H*0.15, 0.04), (H*0.22, 0.05),
                        (H*0.28, 0.04), (H*0.34, 0.03)]:
    ax.axhspan(y_band - 25, y_band + 25, color=MIST, alpha=a_base, zorder=13)
    c = plt.Circle((W * 0.50, y_band), W * 0.18, color=MOONLIGHT,
                   alpha=a_base * 0.2, fill=True, zorder=13)
    ax.add_patch(c)

# ---------------------------------------------------------------------------
# FOREGROUND — banks around the river
# ---------------------------------------------------------------------------
fg_x = np.arange(W)

# Lower bank — below the river (nearest to viewer)
fg_y_low = big_lower - 5 + 6 * np.sin(fg_x / W * 4 * np.pi) + rng.normal(0, 2, W)
ax.fill_between(fg_x, 0, fg_y_low, color="#050606", alpha=1.0, zorder=16)

# Upper bank — above the river, forested
fg_y_up = big_upper + 15 + 8 * np.sin(fg_x / W * 5 * np.pi) + rng.normal(0, 3, W)
ax.fill_between(fg_x, big_upper + 2, fg_y_up,
                color=FOREST_DARK, alpha=0.90, zorder=16)

# Large boulders in the big river — dark rock breaking the torrent
boulder_rng = np.random.default_rng(777)
for _ in range(25):
    bx = boulder_rng.uniform(50, W - 50)
    fi = int(np.clip(bx, 0, W - 1))
    # Most boulders mid-river, some near banks
    roll = boulder_rng.random()
    if roll < 0.6:
        by = big_cy[fi] + boulder_rng.uniform(-big_hw[fi]*0.4, big_hw[fi]*0.4)
    elif roll < 0.8:
        by = big_upper[fi] - boulder_rng.uniform(3, 15)
    else:
        by = big_lower[fi] + boulder_rng.uniform(3, 15)
    # Large boulders — some truly massive
    bw = boulder_rng.uniform(50, 160)
    bh = boulder_rng.uniform(18, 55)
    # Irregular shape — 5-6 vertices for a craggy outline
    n_verts = boulder_rng.integers(5, 8)
    angles = np.sort(boulder_rng.uniform(0, 2*np.pi, n_verts))
    radii = np.array([boulder_rng.uniform(0.6, 1.0) for _ in range(n_verts)])
    verts = [(bx + bw/2 * r * np.cos(a), by + bh/2 * r * np.sin(a))
             for a, r in zip(angles, radii)]
    boulder = Polygon(verts, closed=True,
                       facecolor=DARK_ROCK, edgecolor="none", alpha=0.92)
    boulder.set_zorder(15.5)
    ax.add_patch(boulder)
    # Moonlit top edge — bright highlight on the upstream face
    top_idx = np.argmax([v[1] for v in verts])
    tx, ty_top = verts[top_idx]
    prev_v = verts[(top_idx - 1) % n_verts]
    ax.plot([prev_v[0], tx], [prev_v[1], ty_top],
            color=MOONLIGHT, lw=1.2, alpha=0.15, zorder=15.6)
    # Foam wake — white flecks downstream (below) the boulder
    for _ in range(boulder_rng.integers(3, 10)):
        fx = bx + boulder_rng.uniform(-bw*0.4, bw*0.4)
        fy = by - boulder_rng.uniform(2, bh * 0.8)
        ax.plot(fx, fy, ".", color=MOONLIGHT,
                markersize=boulder_rng.uniform(1.5, 5.0),
                alpha=boulder_rng.uniform(0.15, 0.45), zorder=15.6)
    # Water ripple V-wake
    wake_len = boulder_rng.uniform(15, 40)
    ax.plot([bx - bw*0.2, bx, bx + bw*0.2],
            [by - wake_len, by - bh*0.3, by - wake_len],
            color=MOONLIGHT, lw=0.6, alpha=0.08, zorder=15.6)

# ---------------------------------------------------------------------------
# QUARTZ specks scattered in the forest zone
# ---------------------------------------------------------------------------
for _ in range(200):
    qx = rng.uniform(30, W - 30)
    qy = rng.uniform(H * 0.12, treeline_base)
    ax.plot(qx, qy, ".", color=MOONLIGHT, markersize=rng.uniform(0.3, 1.5),
            alpha=rng.uniform(0.01, 0.05), zorder=13)

# ---------------------------------------------------------------------------
# TITLE
# ---------------------------------------------------------------------------
ax.text(W / 2, H * 0.015, "The Traveller\u2019s Window", ha="center", va="bottom",
        fontsize=9, fontfamily="serif", color=MOONLIGHT, alpha=0.18,
        fontweight="bold", zorder=20)
ax.text(W / 2, H * 0.005,
        "the Parvati descends \u2014 careless, elegant, powerful",
        ha="center", va="bottom", fontsize=6, fontfamily="serif",
        color=GLACIER, alpha=0.12, fontstyle="italic", zorder=20)

# ---------------------------------------------------------------------------
# SAVE
# ---------------------------------------------------------------------------
out_dir = FSPath(__file__).parent
out = out_dir / "travellers-window.png"
fig.savefig(out, bbox_inches="tight", dpi=200, facecolor=fig.get_facecolor(),
            pad_inches=0.1)
print(f"Saved: {out}")
plt.close(fig)
