"""
Generate a hand-drawn manuscript-style map of high Himalayan valleys and passes
for "The Thread Walkers" literary fiction.

Usage:
    uv run --with matplotlib --with numpy python3 map-of-passes.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path as FSPath

# --- Reproducible randomness ---
rng = np.random.default_rng(42)

# --- Canvas ---
fig, ax = plt.subplots(figsize=(11, 14), dpi=200)
fig.patch.set_facecolor("#f4e8c1")
ax.set_facecolor("#f4e8c1")
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.35)
ax.set_aspect("equal")
ax.axis("off")


# --- Helper: hand-drawn line ---
def hand_line(x0, y0, x1, y1, n=60, jitter=0.003):
    """Return wobbly line coordinates between two points."""
    t = np.linspace(0, 1, n)
    x = x0 + (x1 - x0) * t + rng.normal(0, jitter, n)
    y = y0 + (y1 - y0) * t + rng.normal(0, jitter, n)
    return x, y


def hand_curve(pts, n=120, jitter=0.002):
    """Spline-ish hand-drawn curve through a sequence of (x,y) waypoints."""
    pts = np.array(pts)
    # linear interpolation along segments, then jitter
    total = len(pts) - 1
    per_seg = n // total
    xs, ys = [], []
    for i in range(total):
        t = np.linspace(0, 1, per_seg, endpoint=(i == total - 1))
        xs.append(pts[i, 0] + (pts[i + 1, 0] - pts[i, 0]) * t)
        ys.append(pts[i, 1] + (pts[i + 1, 1] - pts[i, 1]) * t)
    x = np.concatenate(xs) + rng.normal(0, jitter, sum(len(a) for a in xs))
    y = np.concatenate(ys) + rng.normal(0, jitter, sum(len(a) for a in ys))
    return x, y


# --- Helper: mountain cluster ---
def draw_mountains(cx, cy, count=5, spread=0.04, size=0.018):
    """Draw a cluster of inverted-V mountain marks."""
    for _ in range(count):
        mx = cx + rng.uniform(-spread, spread)
        my = cy + rng.uniform(-spread * 0.5, spread * 0.5)
        s = size * rng.uniform(0.7, 1.3)
        lx, ly = hand_line(mx - s * 0.6, my, mx, my + s, n=15, jitter=0.001)
        rx, ry = hand_line(mx, my + s, mx + s * 0.6, my, n=15, jitter=0.001)
        ax.plot(lx, ly, color="#5c4a2f", lw=0.7, alpha=0.75)
        ax.plot(rx, ry, color="#5c4a2f", lw=0.7, alpha=0.75)


# --- Helper: pass chevron symbol ---
def draw_pass(cx, cy, label, label_offset=(0, -0.025)):
    s = 0.008
    # double chevron
    for dy in [0, s * 0.6]:
        ax.plot([cx - s, cx, cx + s], [cy + s + dy, cy + dy, cy + s + dy],
                color="#5c4a2f", lw=1.2, solid_capstyle="round")
    ax.text(cx + label_offset[0], cy + label_offset[1], label,
            fontsize=6.5, fontstyle="italic", fontfamily="serif",
            color="#5c4a2f", ha="center", va="top")


# --- Helper: loom glyph (workshop) ---
def draw_loom(cx, cy, label, label_offset=(0.025, 0)):
    """Two vertical posts with three horizontal bars — a tiny loom."""
    h = 0.016
    w = 0.008
    # posts
    for dx in [-w / 2, w / 2]:
        lx, ly = hand_line(cx + dx, cy, cx + dx, cy + h, n=12, jitter=0.0005)
        ax.plot(lx, ly, color="#5c4a2f", lw=1.0)
    # bars
    for frac in [0.25, 0.5, 0.75]:
        bx, by = hand_line(cx - w / 2, cy + h * frac,
                           cx + w / 2, cy + h * frac, n=10, jitter=0.0004)
        ax.plot(bx, by, color="#5c4a2f", lw=0.8)
    ax.text(cx + label_offset[0], cy + label_offset[1], label,
            fontsize=5.5, fontfamily="serif", color="#5c4a2f",
            ha="left", va="center")


# --- Elevation shading (subtle ochre blobs) ---
for _ in range(80):
    ex = rng.uniform(0.05, 0.95)
    ey = rng.uniform(0.1, 1.2)
    er = rng.uniform(0.03, 0.09)
    circle = plt.Circle((ex, ey), er, color="#c9a84c", alpha=rng.uniform(0.03, 0.08))
    ax.add_patch(circle)


# --- Mountain ranges ---
# Great Himalaya spine
for cx in np.linspace(0.1, 0.9, 12):
    draw_mountains(cx, 0.55 + 0.08 * np.sin(cx * 5), count=rng.integers(3, 7),
                   spread=0.03, size=0.02)
# Pir Panjal / southern range
for cx in np.linspace(0.05, 0.5, 6):
    draw_mountains(cx, 0.35 + 0.04 * np.sin(cx * 7), count=rng.integers(2, 5),
                   spread=0.025, size=0.015)
# Karakoram (northern, fading)
for cx in np.linspace(0.3, 0.95, 8):
    draw_mountains(cx, 0.95 + 0.06 * np.sin(cx * 4), count=rng.integers(3, 6),
                   spread=0.035, size=0.022)
# Zanskar range (middle)
for cx in np.linspace(0.15, 0.65, 5):
    draw_mountains(cx, 0.72 + 0.03 * np.sin(cx * 6), count=rng.integers(2, 4),
                   spread=0.02, size=0.016)


# --- Rivers (faded indigo) ---
river_color = "#3b5998"
river_alpha = 0.45
river_lw = 1.1

# Chandra river — through Lahaul
rx, ry = hand_curve([(0.05, 0.48), (0.15, 0.45), (0.25, 0.43),
                      (0.32, 0.44), (0.38, 0.48)], jitter=0.003)
ax.plot(rx, ry, color=river_color, lw=river_lw, alpha=river_alpha)
ax.text(0.18, 0.44, "Chandra", fontsize=5, fontfamily="serif",
        fontstyle="italic", color=river_color, alpha=0.6, rotation=-5)

# Bhaga river
rx, ry = hand_curve([(0.15, 0.55), (0.22, 0.50), (0.30, 0.47),
                      (0.32, 0.44)], jitter=0.003)
ax.plot(rx, ry, color=river_color, lw=river_lw, alpha=river_alpha)
ax.text(0.17, 0.52, "Bhaga", fontsize=5, fontfamily="serif",
        fontstyle="italic", color=river_color, alpha=0.6, rotation=-25)

# Spiti river
rx, ry = hand_curve([(0.45, 0.62), (0.50, 0.55), (0.55, 0.48),
                      (0.58, 0.40), (0.55, 0.32)], jitter=0.003)
ax.plot(rx, ry, color=river_color, lw=river_lw, alpha=river_alpha)
ax.text(0.53, 0.50, "Spiti", fontsize=5, fontfamily="serif",
        fontstyle="italic", color=river_color, alpha=0.6, rotation=-60)

# Shyok river (far north)
rx, ry = hand_curve([(0.55, 1.10), (0.62, 1.02), (0.70, 0.95),
                      (0.78, 0.90), (0.88, 0.88)], jitter=0.004)
ax.plot(rx, ry, color=river_color, lw=1.3, alpha=river_alpha * 0.8)
ax.text(0.68, 0.99, "Shyok", fontsize=5, fontfamily="serif",
        fontstyle="italic", color=river_color, alpha=0.5, rotation=-18)


# --- Valleys (labels) ---
valley_style = dict(fontsize=9, fontfamily="serif", color="#5c4a2f",
                    fontweight="bold", ha="center")
ax.text(0.25, 0.40, "L A H A U L", **valley_style)
ax.text(0.28, 0.375, "(Keylong)", fontsize=6, fontfamily="serif",
        fontstyle="italic", color="#7a6a4f", ha="center")

ax.text(0.52, 0.42, "S P I T I", **valley_style)
ax.text(0.52, 0.395, "(Kaza)", fontsize=6, fontfamily="serif",
        fontstyle="italic", color="#7a6a4f", ha="center")

ax.text(0.72, 0.35, "K I N N A U R", **valley_style)

ax.text(0.65, 0.85, "N U B R A", **valley_style)
ax.text(0.65, 0.825, "V A L L E Y", fontsize=7, fontfamily="serif",
        color="#7a6a4f", ha="center")

# "Beyond the Karakoram" — fading
ax.text(0.55, 1.18, "beyond  the  Karakoram . . .",
        fontsize=8, fontfamily="serif", fontstyle="italic",
        color="#7a6a4f", alpha=0.4, ha="center")


# --- Passes ---
draw_pass(0.18, 0.50, "Rohtang La")
draw_pass(0.40, 0.52, "Kunzum La")
draw_pass(0.30, 0.62, "Baralacha La")
draw_pass(0.58, 0.78, "Khardung La", label_offset=(0.04, 0.005))
draw_pass(0.70, 1.05, "Karakoram\nPass", label_offset=(0.0, -0.03))


# --- Workshops (loom glyphs) ---
draw_loom(0.22, 0.42, "weaving house", label_offset=(0.018, 0.008))
draw_loom(0.50, 0.44, "thread-hall", label_offset=(0.018, 0.008))
draw_loom(0.62, 0.87, "the high loom", label_offset=(0.018, 0.008))
draw_loom(0.35, 0.58, "dye-works", label_offset=(0.018, 0.008))


# --- Disputed borders (dashed, fading) ---
border_pts = [(0.02, 0.90), (0.15, 0.88), (0.30, 0.92), (0.45, 0.98),
              (0.60, 1.05), (0.75, 1.10), (0.90, 1.12), (1.02, 1.15)]
bx, by = hand_curve(border_pts, n=200, jitter=0.005)
# fade alpha along the line
n_pts = len(bx)
seg_len = 4
for i in range(0, n_pts - seg_len, seg_len):
    fade = 0.35 * (1.0 - 0.4 * abs(i / n_pts - 0.5))
    ax.plot(bx[i:i + seg_len + 1], by[i:i + seg_len + 1],
            color="#5c4a2f", lw=0.8, alpha=fade,
            linestyle=(0, (3, 4)), solid_capstyle="round")

ax.text(0.45, 1.01, "— disputed —", fontsize=5, fontfamily="serif",
        fontstyle="italic", color="#7a6a4f", alpha=0.45, ha="center",
        rotation=8)


# --- Compass rose (upper-left) ---
cx_c, cy_c = 0.10, 1.15
arm = 0.035
# N-S
for dx, dy, label in [(0, arm, "N"), (0, -arm, "S"),
                       (arm, 0, "E"), (-arm, 0, "W")]:
    lx, ly = hand_line(cx_c, cy_c, cx_c + dx, cy_c + dy, n=15, jitter=0.001)
    ax.plot(lx, ly, color="#5c4a2f", lw=1.0, alpha=0.7)
    ax.text(cx_c + dx * 1.5, cy_c + dy * 1.5, label,
            fontsize=6, fontfamily="serif", fontweight="bold",
            color="#5c4a2f", ha="center", va="center", alpha=0.7)
# diamond at center
diamond_x = [cx_c, cx_c + 0.006, cx_c, cx_c - 0.006, cx_c]
diamond_y = [cy_c + 0.008, cy_c, cy_c - 0.008, cy_c, cy_c + 0.008]
ax.fill(diamond_x, diamond_y, color="#5c4a2f", alpha=0.5)


# --- Title cartouche ---
# Decorative border
cart_x, cart_y = 0.50, 1.28
cart_w, cart_h = 0.34, 0.055
rect = FancyBboxPatch((cart_x - cart_w, cart_y - cart_h), cart_w * 2, cart_h * 2,
                       boxstyle="round,pad=0.008", linewidth=1.0,
                       edgecolor="#5c4a2f", facecolor="#f4e8c1", alpha=0.9)
ax.add_patch(rect)

ax.text(cart_x, cart_y + 0.015, "The Disputed Passes",
        fontsize=13, fontfamily="serif", fontweight="bold",
        color="#3d2e1a", ha="center", va="center")
ax.text(cart_x, cart_y - 0.022, "from the Thread Walker\u2019s notebooks",
        fontsize=7.5, fontfamily="serif", fontstyle="italic",
        color="#7a6a4f", ha="center", va="center")


# --- Edge vignette (radial fade) ---
# Overlay transparent-to-background rectangles around edges
for side_alpha in np.linspace(0.0, 0.55, 20):
    margin = side_alpha * 0.06
    edge_rect = plt.Rectangle((-0.05 + margin, -0.05 + margin),
                               1.10 - 2 * margin, 1.40 - 2 * margin,
                               fill=False, edgecolor="#f4e8c1",
                               lw=6, alpha=side_alpha * 0.8)
    ax.add_patch(edge_rect)

# Stronger fade at very edges
for thickness, alpha in [(0.04, 0.7), (0.03, 0.5), (0.02, 0.3)]:
    for (x, y, w, h) in [
        (-0.05, -0.05, 1.10, thickness),           # bottom
        (-0.05, 1.35 - thickness, 1.10, thickness), # top
        (-0.05, -0.05, thickness, 1.40),            # left
        (1.05 - thickness, -0.05, thickness, 1.40), # right
    ]:
        ax.add_patch(plt.Rectangle((x, y), w, h,
                     facecolor="#f4e8c1", alpha=alpha, edgecolor="none"))


# --- Speckle / aging texture ---
n_specks = 600
sx = rng.uniform(-0.02, 1.02, n_specks)
sy = rng.uniform(-0.02, 1.32, n_specks)
ss = rng.uniform(0.2, 1.5, n_specks)
sa = rng.uniform(0.02, 0.10, n_specks)
ax.scatter(sx, sy, s=ss, c="#8b7355", alpha=sa, edgecolors="none")


# --- Save ---
out_dir = FSPath(__file__).parent
for ext in ("pdf", "png"):
    out_path = out_dir / f"map-of-passes.{ext}"
    fig.savefig(out_path, bbox_inches="tight", facecolor=fig.get_facecolor(),
                pad_inches=0.15, dpi=200)
    print(f"Saved: {out_path}")
plt.close()
