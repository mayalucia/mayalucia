"""
The Landau Mode — a derivation chain on a chalkboard.

Usage:
    uv run --with matplotlib --with numpy python3 gen-mode-landau.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from pathlib import Path

rng = np.random.default_rng(42)

fig, ax = plt.subplots(figsize=(10, 12), dpi=200)
SLATE = "#1a1a2e"
CHALK = "#e8e4d4"
CHALK_DIM = "#8a8678"
BLUE = "#7eb8da"
GOLD = "#dac87e"

fig.patch.set_facecolor(SLATE)
ax.set_facecolor(SLATE)
ax.set_xlim(-5, 5)
ax.set_ylim(-6.5, 6.5)
ax.set_aspect("equal")
ax.axis("off")

# --- Chalk dust ---
n_dust = 2000
ax.scatter(rng.uniform(-4.9, 4.9, n_dust),
           rng.uniform(-6.4, 6.4, n_dust),
           s=rng.uniform(0.1, 0.5, n_dust),
           c=CHALK, alpha=rng.uniform(0.01, 0.03, n_dust),
           edgecolors="none")

# --- Derivation steps ---
steps = [
    (r"$\mathbf{M}$ = magnetic moment of spin ensemble",
     "Definition"),
    (r"$\boldsymbol{\tau} = \gamma\, \mathbf{M} \times \mathbf{B}$",
     "Torque on magnetic\nmoment in field $\\mathbf{B}$"),
    (r"$\frac{d\mathbf{M}}{dt} = \gamma\, \mathbf{M} \times \mathbf{B}$",
     "Newton's second\nlaw for angular\nmomentum"),
    (r"$\dot{M}_x = \gamma (M_y B_z - M_z B_y)$",
     "Component form\n($x$-component)"),
    (r"$|\mathbf{M}|$ is conserved  $\Leftarrow$  $\mathbf{M} \cdot \dot{\mathbf{M}} = 0$",
     "Cross product is\northogonal to $\\mathbf{M}$"),
    (r"$\omega_L = \gamma |\mathbf{B}|$   :   Larmor frequency",
     "The measurement\nequation"),
]

n_steps = len(steps)
y_top = 5.5
y_bot = -4.5
y_positions = np.linspace(y_top, y_bot, n_steps)

for i, ((eq, premise), y) in enumerate(zip(steps, y_positions)):
    # Premise label (left margin)
    ax.text(-4.5, y, premise, fontsize=7, fontfamily="serif",
            fontstyle="italic", color=CHALK_DIM, ha="left",
            va="center", linespacing=1.2, alpha=0.6)

    # Step number
    ax.text(-1.8, y + 0.25, f"({i+1})", fontsize=7, fontfamily="serif",
            color=BLUE, ha="center", va="center", alpha=0.7)

    # Equation
    text_col = GOLD if i == n_steps - 1 else CHALK
    text_size = 13 if i == n_steps - 1 else 11
    text_alpha = 1.0 if i == n_steps - 1 else 0.85
    ax.text(1.0, y, eq, fontsize=text_size, fontfamily="serif",
            color=text_col, ha="center", va="center",
            alpha=text_alpha)

    # Connecting arrow
    if i < n_steps - 1:
        y_next = y_positions[i + 1]
        mid_y = (y + y_next) / 2
        # hand-drawn arrow
        n_pts = 20
        t = np.linspace(0, 1, n_pts)
        arr_x = -1.8 + rng.normal(0, 0.015, n_pts)
        arr_y = y - 0.4 + (y_next + 0.4 - (y - 0.4)) * t + rng.normal(0, 0.01, n_pts)
        ax.plot(arr_x, arr_y, color=BLUE, lw=0.8, alpha=0.5)
        # arrowhead
        ax.annotate("", xy=(-1.8, y_next + 0.35),
                    xytext=(-1.8, y_next + 0.6),
                    arrowprops=dict(arrowstyle="->", color=BLUE,
                                   lw=0.8, mutation_scale=10),
                    alpha=0.5)

# --- Final result highlight ---
y_final = y_positions[-1]
highlight = FancyBboxPatch((-2.5, y_final - 0.45), 7.0, 0.9,
                           boxstyle="round,pad=0.15",
                           facecolor=GOLD, alpha=0.08,
                           edgecolor=GOLD, linewidth=0.8)
ax.add_patch(highlight)

# --- Title ---
ax.text(0, 6.3, "THE LANDAU MODE",
        fontsize=16, fontfamily="serif", fontweight="bold",
        color=BLUE, ha="center", va="center")
ax.text(0, 5.9, "every result derived  \u00b7  no equation falls from the sky",
        fontsize=8, fontfamily="serif", fontstyle="italic",
        color=CHALK_DIM, ha="center", va="center")

# --- Bottom quote ---
ax.text(0, -5.8,
        '"Can you reproduce this derivation on a blank page?"',
        fontsize=8, fontfamily="serif", fontstyle="italic",
        color=CHALK_DIM, ha="center", va="center", alpha=0.6)

# --- Left margin label ---
ax.text(-4.5, 6.0, "PREMISES", fontsize=7, fontfamily="serif",
        fontweight="bold", color=CHALK_DIM, ha="left", va="center",
        alpha=0.4, rotation=0)

# --- Save ---
out_dir = Path(__file__).parent
for ext in ("png",):
    out = out_dir / f"mode-landau.{ext}"
    fig.savefig(out, bbox_inches="tight", dpi=200,
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    print(f"Saved: {out}")
plt.close()
