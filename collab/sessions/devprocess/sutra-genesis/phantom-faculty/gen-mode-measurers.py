"""
The Measurers — triptych of three empirical modes.

Usage:
    uv run --with matplotlib --with numpy python3 gen-mode-measurers.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
from pathlib import Path

rng = np.random.default_rng(42)

fig, axes = plt.subplots(1, 3, figsize=(16, 6), dpi=200)
SLATE = "#1a1a2e"
CHALK = "#e8e4d4"
CHALK_DIM = "#8a8678"
OCHRE = "#d4a574"
OCHRE_DIM = "#8a6a44"

fig.patch.set_facecolor(SLATE)

for ax in axes:
    ax.set_facecolor(SLATE)
    ax.set_aspect("equal")
    ax.axis("off")

# ===================================================================
# Panel 1: Faraday — iron filings / field lines
# ===================================================================
ax1 = axes[0]
ax1.set_xlim(-3, 3)
ax1.set_ylim(-3, 3)

# Chalk dust
ax1.scatter(rng.uniform(-2.9, 2.9, 800),
            rng.uniform(-2.9, 2.9, 800),
            s=rng.uniform(0.1, 0.4, 800),
            c=CHALK, alpha=rng.uniform(0.01, 0.03, 800),
            edgecolors="none")

# Dipole field lines
# B = (mu/4pi) * (3(m.r)r/r^5 - m/r^3), simplified to 2D dipole
n_lines = 16
for angle in np.linspace(0.15, np.pi - 0.15, n_lines // 2):
    # field line of a dipole: r = r0 sin^2(theta)
    theta = np.linspace(angle, np.pi - angle + np.pi, 200)
    r0 = 2.5 * np.sin(angle)**2
    r = r0 * np.sin(theta)**2
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    mask = (np.abs(x) < 2.8) & (np.abs(y) < 2.8) & (r > 0.35)
    # add jitter for hand-drawn feel
    x_j = x + rng.normal(0, 0.015, len(x))
    y_j = y + rng.normal(0, 0.015, len(y))
    ax1.plot(x_j[mask], y_j[mask], color=OCHRE, lw=0.7, alpha=0.6)

# Magnet at centre
ax1.add_patch(Rectangle((-0.15, -0.5), 0.3, 1.0,
              facecolor="#8b3a3a", edgecolor=CHALK, lw=0.5, zorder=5))
ax1.text(0, 0.25, "N", fontsize=7, color=CHALK, ha="center",
         va="center", fontweight="bold", zorder=6)
ax1.text(0, -0.25, "S", fontsize=7, color=CHALK, ha="center",
         va="center", fontweight="bold", zorder=6)

# Iron filings (scatter along field lines)
n_filings = 400
f_angles = rng.uniform(0, 2 * np.pi, n_filings)
f_r = rng.uniform(0.5, 2.5, n_filings)
f_x = f_r * np.cos(f_angles)
f_y = f_r * np.sin(f_angles)
# orient filings along field direction
for i in range(n_filings):
    if f_r[i] < 0.4:
        continue
    r3 = f_r[i]**3
    bx = 3 * f_x[i] * f_y[i] / (f_r[i]**5)
    by = (3 * f_y[i]**2 / (f_r[i]**5) - 1 / r3)
    b_mag = np.sqrt(bx**2 + by**2)
    if b_mag > 0:
        dx = 0.06 * bx / b_mag
        dy = 0.06 * by / b_mag
        ax1.plot([f_x[i] - dx, f_x[i] + dx],
                [f_y[i] - dy, f_y[i] + dy],
                color=OCHRE, lw=0.3, alpha=0.4)

ax1.text(0, -2.7, "FARADAY", fontsize=10, fontfamily="serif",
         fontweight="bold", color=OCHRE, ha="center", va="center")
ax1.text(0, -2.95, "active measurement", fontsize=7, fontfamily="serif",
         fontstyle="italic", color=CHALK_DIM, ha="center")

# ===================================================================
# Panel 2: Humboldt — Naturgemälde (altitude cross-section)
# ===================================================================
ax2 = axes[1]
ax2.set_xlim(-3, 3)
ax2.set_ylim(-3, 3)

# Chalk dust
ax2.scatter(rng.uniform(-2.9, 2.9, 800),
            rng.uniform(-2.9, 2.9, 800),
            s=rng.uniform(0.1, 0.4, 800),
            c=CHALK, alpha=rng.uniform(0.01, 0.03, 800),
            edgecolors="none")

# Mountain profile
n_prof = 200
mx = np.linspace(-2.5, 2.5, n_prof)
# asymmetric peak
my = -1.5 + 3.8 * np.exp(-0.5 * ((mx - 0.2) / 1.2)**2)
my += 0.3 * np.sin(mx * 3) * np.exp(-0.5 * ((mx) / 2)**2)
my_jitter = my + rng.normal(0, 0.02, n_prof)
ax2.plot(mx, my_jitter, color=CHALK, lw=1.2, alpha=0.7)
ax2.fill_between(mx, -3, my_jitter, color=CHALK, alpha=0.04)

# Vegetation zones (horizontal bands with labels)
zones = [
    (-1.5, -0.5, "tropical forest",  "#2d5a27"),
    (-0.5,  0.5, "cloud forest",     "#3a7a33"),
    ( 0.5,  1.2, "páramo",           "#6a8a44"),
    ( 1.2,  1.8, "alpine tundra",    "#8a8a5a"),
    ( 1.8,  2.3, "eternal snow",     "#c4c4c4"),
]
for y_lo, y_hi, label, col in zones:
    ax2.axhspan(y_lo, y_hi, color=col, alpha=0.08, zorder=0)
    ax2.text(2.6, (y_lo + y_hi) / 2, label, fontsize=5,
             fontfamily="serif", fontstyle="italic", color=col,
             ha="left", va="center", alpha=0.7)

# Data channels on right margin
channels = [
    (2.3, "T °C",     "#d44a4a"),
    (1.5, "P hPa",    "#4a7ad4"),
    (0.7, "B incl.",   OCHRE),
    (-0.1, "species", "#4ad47a"),
    (-0.9, "soil",    "#8a6a44"),
]
for y, label, col in channels:
    ax2.plot([-2.8, -2.4], [y, y], color=col, lw=1.5, alpha=0.5)
    ax2.text(-2.85, y, label, fontsize=5, fontfamily="serif",
             color=col, ha="right", va="center", alpha=0.7)

# Integration arrows (converging to mountain)
for y, _, col in channels:
    ax2.annotate("", xy=(-1.8, y * 0.7), xytext=(-2.3, y),
                arrowprops=dict(arrowstyle="->", color=col,
                               lw=0.5, alpha=0.3))

ax2.text(0, -2.7, "HUMBOLDT", fontsize=10, fontfamily="serif",
         fontweight="bold", color=OCHRE, ha="center", va="center")
ax2.text(0, -2.95, "passive observation", fontsize=7, fontfamily="serif",
         fontstyle="italic", color=CHALK_DIM, ha="center")

# ===================================================================
# Panel 3: Helmholtz — coil + equation
# ===================================================================
ax3 = axes[2]
ax3.set_xlim(-3, 3)
ax3.set_ylim(-3, 3)

# Chalk dust
ax3.scatter(rng.uniform(-2.9, 2.9, 800),
            rng.uniform(-2.9, 2.9, 800),
            s=rng.uniform(0.1, 0.4, 800),
            c=CHALK, alpha=rng.uniform(0.01, 0.03, 800),
            edgecolors="none")

# Helmholtz coils (two circles, side view as ellipses)
from matplotlib.patches import Ellipse
coil_col = OCHRE
for y_c in [-0.7, 0.7]:
    e = Ellipse((0, y_c), 3.6, 0.4, facecolor="none",
                edgecolor=coil_col, lw=1.8, alpha=0.7)
    ax3.add_patch(e)

# Uniform field lines between coils
for x_f in np.linspace(-1.5, 1.5, 12):
    n_pts = 30
    t = np.linspace(0, 1, n_pts)
    ly = -0.5 + 1.0 * t + rng.normal(0, 0.008, n_pts)
    lx = x_f + rng.normal(0, 0.008, n_pts)
    ax3.plot(lx, ly, color=OCHRE, lw=0.5, alpha=0.4)
    # arrowhead at midpoint
    if abs(x_f) < 1.2:
        ax3.annotate("", xy=(x_f, 0.05), xytext=(x_f, -0.05),
                    arrowprops=dict(arrowstyle="->", color=OCHRE,
                                   lw=0.5, alpha=0.4))

# Equation overlaid
ax3.text(0, -1.6,
         r"$B = \frac{8\mu_0 N I}{5\sqrt{5}\, R}$",
         fontsize=14, fontfamily="serif", color=CHALK,
         ha="center", va="center", alpha=0.85)

# Bidirectional arrow between coil and equation
ax3.annotate("", xy=(0, -1.1), xytext=(0, -0.4),
            arrowprops=dict(arrowstyle="<->", color=CHALK,
                           lw=0.8, alpha=0.5))
ax3.text(0.3, -0.75, "implies", fontsize=6, fontfamily="serif",
         fontstyle="italic", color=CHALK_DIM, ha="left",
         va="center", alpha=0.5)

# Labels
ax3.text(0, 1.8, "theory", fontsize=7, fontfamily="serif",
         fontstyle="italic", color=CHALK_DIM, ha="center", alpha=0.5)
ax3.text(0, -2.1, "instrument", fontsize=7, fontfamily="serif",
         fontstyle="italic", color=CHALK_DIM, ha="center", alpha=0.5)

ax3.text(0, -2.7, "HELMHOLTZ", fontsize=10, fontfamily="serif",
         fontweight="bold", color=OCHRE, ha="center", va="center")
ax3.text(0, -2.95, "instrument-theory unity", fontsize=7,
         fontfamily="serif", fontstyle="italic", color=CHALK_DIM,
         ha="center")

# --- Suptitle ---
fig.suptitle("THE MEASURERS", fontsize=16, fontfamily="serif",
             fontweight="bold", color=OCHRE, y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.95])

# --- Save ---
out_dir = Path(__file__).parent
for ext in ("png",):
    out = out_dir / f"mode-measurers.{ext}"
    fig.savefig(out, bbox_inches="tight", dpi=200,
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    print(f"Saved: {out}")
plt.close()
