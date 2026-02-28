"""
The Mathematicians — five modes of mathematical cognition.

Usage:
    uv run --with matplotlib --with numpy python3 gen-mode-mathematicians.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
from matplotlib.collections import LineCollection
from pathlib import Path

rng = np.random.default_rng(42)

fig, axes = plt.subplots(1, 5, figsize=(18, 5), dpi=200)
SLATE = "#1a1a2e"
CHALK = "#e8e4d4"
CHALK_DIM = "#8a8678"
GOLD = "#dac87e"
GOLD_DIM = "#8a7a3e"

fig.patch.set_facecolor(SLATE)

for ax in axes:
    ax.set_facecolor(SLATE)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    # chalk dust
    ax.scatter(rng.uniform(-2.4, 2.4, 400),
               rng.uniform(-2.4, 2.4, 400),
               s=rng.uniform(0.1, 0.3, 400),
               c=CHALK, alpha=rng.uniform(0.01, 0.03, 400),
               edgecolors="none")

# ===================================================================
# Panel 1: Gauss — computational patience (number grid with pattern)
# ===================================================================
ax1 = axes[0]

# Grid of primes / composites — pattern emerging
primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
grid_size = 7
for row in range(grid_size):
    for col in range(grid_size):
        n = row * grid_size + col + 1
        x = -1.8 + col * 0.6
        y = 1.8 - row * 0.55
        is_prime = n in primes
        col_n = GOLD if is_prime else CHALK_DIM
        alpha = 0.9 if is_prime else 0.35
        ax1.text(x, y, str(n), fontsize=7, fontfamily="monospace",
                color=col_n, ha="center", va="center", alpha=alpha)

# Highlight pattern
ax1.text(0, -2.0, "GAUSS", fontsize=9, fontfamily="serif",
         fontweight="bold", color=GOLD, ha="center")
ax1.text(0, -2.3, "computational\npatience", fontsize=6,
         fontfamily="serif", fontstyle="italic", color=CHALK_DIM,
         ha="center", linespacing=1.1)

# ===================================================================
# Panel 2: Riemann — curved surface (saddle/hyperbolic)
# ===================================================================
ax2 = axes[1]

# Hyperbolic-like curves suggesting a saddle surface
thetas = np.linspace(0, 2 * np.pi, 100)
for r in np.linspace(0.3, 2.0, 8):
    x = r * np.cos(thetas) * (1 + 0.15 * np.sin(2 * thetas))
    y = r * np.sin(thetas) * (1 - 0.15 * np.sin(2 * thetas))
    x += rng.normal(0, 0.01, len(x))
    y += rng.normal(0, 0.01, len(y))
    ax2.plot(x, y, color=GOLD, lw=0.5, alpha=0.3 + 0.05 * r)

# Geodesics
for angle in np.linspace(0, np.pi, 6):
    t = np.linspace(-2, 2, 80)
    gx = t * np.cos(angle) + 0.1 * np.sin(t * 2) * np.sin(angle)
    gy = t * np.sin(angle) - 0.1 * np.sin(t * 2) * np.cos(angle)
    mask = gx**2 + gy**2 < 5
    ax2.plot(gx[mask], gy[mask], color=CHALK, lw=0.4, alpha=0.4)

ax2.text(0, -2.0, "RIEMANN", fontsize=9, fontfamily="serif",
         fontweight="bold", color=GOLD, ha="center")
ax2.text(0, -2.3, "conceptual\narchitecture", fontsize=6,
         fontfamily="serif", fontstyle="italic", color=CHALK_DIM,
         ha="center", linespacing=1.1)

# ===================================================================
# Panel 3: Erdős — network graph
# ===================================================================
ax3 = axes[2]

# Random network
n_nodes = 25
positions = rng.uniform(-1.8, 1.8, (n_nodes, 2))
# edges: connect nearby nodes
edges = []
for i in range(n_nodes):
    for j in range(i + 1, n_nodes):
        dist = np.sqrt((positions[i, 0] - positions[j, 0])**2 +
                       (positions[i, 1] - positions[j, 1])**2)
        if dist < 1.2 and rng.random() < 0.4:
            edges.append((i, j))

for i, j in edges:
    x1, y1 = positions[i]
    x2, y2 = positions[j]
    n_pts = 20
    t = np.linspace(0, 1, n_pts)
    lx = x1 + (x2 - x1) * t + rng.normal(0, 0.01, n_pts)
    ly = y1 + (y2 - y1) * t + rng.normal(0, 0.01, n_pts)
    ax3.plot(lx, ly, color=GOLD, lw=0.4, alpha=0.3)

# Central node (Erdős)
centre = np.array([0.0, 0.0])
for i in range(n_nodes):
    if np.sqrt(positions[i, 0]**2 + positions[i, 1]**2) < 1.5:
        ax3.plot([0, positions[i, 0]], [0, positions[i, 1]],
                color=CHALK, lw=0.5, alpha=0.3)

for i in range(n_nodes):
    col_n = CHALK if rng.random() > 0.5 else GOLD
    ax3.add_patch(Circle(positions[i], 0.08, facecolor=col_n,
                         edgecolor=CHALK, lw=0.3, alpha=0.6, zorder=5))

# Central node highlighted
ax3.add_patch(Circle((0, 0), 0.15, facecolor=GOLD,
                     edgecolor=CHALK, lw=0.8, alpha=0.9, zorder=6))

ax3.text(0, -2.0, "ERDŐS", fontsize=9, fontfamily="serif",
         fontweight="bold", color=GOLD, ha="center")
ax3.text(0, -2.3, "itinerant\nconnection", fontsize=6,
         fontfamily="serif", fontstyle="italic", color=CHALK_DIM,
         ha="center", linespacing=1.1)

# ===================================================================
# Panel 4: Tao — strategy tree / decision branches
# ===================================================================
ax4 = axes[3]

# Binary tree representing strategic choices
def draw_tree(ax, x, y, dx, dy, depth, max_depth):
    if depth >= max_depth:
        return
    # left branch
    x_l = x - dx
    y_l = y + dy
    n_pts = 15
    t = np.linspace(0, 1, n_pts)
    lx = x + (x_l - x) * t + rng.normal(0, 0.008, n_pts)
    ly = y + (y_l - y) * t + rng.normal(0, 0.008, n_pts)
    alpha = 0.7 - depth * 0.12
    ax.plot(lx, ly, color=GOLD, lw=max(0.4, 1.2 - depth * 0.2), alpha=alpha)
    # right branch
    x_r = x + dx
    y_r = y + dy
    lx = x + (x_r - x) * t + rng.normal(0, 0.008, n_pts)
    ly = y + (y_r - y) * t + rng.normal(0, 0.008, n_pts)
    ax.plot(lx, ly, color=GOLD, lw=max(0.4, 1.2 - depth * 0.2), alpha=alpha)

    # nodes
    for nx, ny in [(x_l, y_l), (x_r, y_r)]:
        s = max(0.03, 0.08 - depth * 0.012)
        ax.add_patch(Circle((nx, ny), s, facecolor=GOLD,
                           edgecolor=CHALK, lw=0.3, alpha=alpha, zorder=5))

    draw_tree(ax, x_l, y_l, dx * 0.55, dy * 0.7, depth + 1, max_depth)
    draw_tree(ax, x_r, y_r, dx * 0.55, dy * 0.7, depth + 1, max_depth)

# Root
ax4.add_patch(Circle((0, -1.5), 0.12, facecolor=CHALK,
                     edgecolor=GOLD, lw=0.8, alpha=0.9, zorder=6))
draw_tree(ax4, 0, -1.5, 1.2, 0.7, 0, 4)

# Labels on early branches
ax4.text(-0.85, -0.5, "try X?", fontsize=5, fontfamily="serif",
         fontstyle="italic", color=CHALK_DIM, ha="center", alpha=0.5)
ax4.text(0.85, -0.5, "try Y?", fontsize=5, fontfamily="serif",
         fontstyle="italic", color=CHALK_DIM, ha="center", alpha=0.5)

ax4.text(0, -2.0, "TAO", fontsize=9, fontfamily="serif",
         fontweight="bold", color=GOLD, ha="center")
ax4.text(0, -2.3, "strategic\nmetacognition", fontsize=6,
         fontfamily="serif", fontstyle="italic", color=CHALK_DIM,
         ha="center", linespacing=1.1)

# ===================================================================
# Panel 5: Thurston — hyperbolic tiling (Poincaré disk)
# ===================================================================
ax5 = axes[4]

# Poincaré disk boundary
theta = np.linspace(0, 2 * np.pi, 200)
ax5.plot(2.0 * np.cos(theta), 2.0 * np.sin(theta),
         color=CHALK, lw=0.8, alpha=0.4)

# Hyperbolic geodesics (arcs within the disk)
n_geo = 20
for _ in range(n_geo):
    a1 = rng.uniform(0, 2 * np.pi)
    a2 = a1 + rng.uniform(0.5, 2.5)
    # points on boundary
    p1 = 2.0 * np.array([np.cos(a1), np.sin(a1)])
    p2 = 2.0 * np.array([np.cos(a2), np.sin(a2)])
    # geodesic approximation: circular arc through p1, p2
    # orthogonal to boundary
    mid = (p1 + p2) / 2
    perp = np.array([-(p2[1] - p1[1]), p2[0] - p1[0]])
    perp_len = np.sqrt(perp[0]**2 + perp[1]**2)
    if perp_len < 0.01:
        continue
    perp = perp / perp_len
    # parametric arc
    t = np.linspace(0, 1, 40)
    # simple quadratic Bezier arc
    ctrl = mid + perp * rng.uniform(-1.5, 1.5)
    gx = (1 - t)**2 * p1[0] + 2 * (1 - t) * t * ctrl[0] + t**2 * p2[0]
    gy = (1 - t)**2 * p1[1] + 2 * (1 - t) * t * ctrl[1] + t**2 * p2[1]
    # clip to disk
    r = np.sqrt(gx**2 + gy**2)
    mask = r < 1.95
    gx += rng.normal(0, 0.008, len(gx))
    gy += rng.normal(0, 0.008, len(gy))
    ax5.plot(gx[mask], gy[mask], color=GOLD, lw=0.4, alpha=0.35)

# Scattered vertices
n_v = 40
v_r = rng.uniform(0, 1.8, n_v)
v_a = rng.uniform(0, 2 * np.pi, n_v)
vx = v_r * np.cos(v_a)
vy = v_r * np.sin(v_a)
ax5.scatter(vx, vy, s=rng.uniform(2, 8, n_v), c=GOLD,
            alpha=0.4, edgecolors="none", zorder=5)

ax5.text(0, -2.0, "THURSTON", fontsize=9, fontfamily="serif",
         fontweight="bold", color=GOLD, ha="center")
ax5.text(0, -2.3, "embodied\ngeometry", fontsize=6,
         fontfamily="serif", fontstyle="italic", color=CHALK_DIM,
         ha="center", linespacing=1.1)

# --- Suptitle ---
fig.suptitle("THE MATHEMATICIANS", fontsize=16, fontfamily="serif",
             fontweight="bold", color=GOLD, y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.95])

# --- Save ---
out_dir = Path(__file__).parent
for ext in ("png",):
    out = out_dir / f"mode-mathematicians.{ext}"
    fig.savefig(out, bbox_inches="tight", dpi=200,
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    print(f"Saved: {out}")
plt.close()
