# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Glacier's Dowry" (Story #17).

The Rakhiot valley below Nanga Parbat's north face. Two waters —
glacial melt and hot spring — from one massif. The gender of glaciers.
The marriage protocol. The seven-fold acceleration. The dowry.

Visual language: mineral palette. Grey gneiss, orange hydrothermal
alteration, white/blue ice, warm earth tones. No forest canopy —
this is above treeline, scarcity not abundance.

Run with:  uv run generate_images_glaciers_dowry.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ── Output ──────────────────────────────────────────────────────────
SLUG = "the-glaciers-dowry"
OUT = (Path(__file__).parent / f"../../website/static/images/writing/{SLUG}").resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9  # inches — 1800×1350 px at 150 DPI

# ── Palette: Mineral / Rakhiot Valley ─────────────────────────────
GNEISS        = "#4A4845"   # dark grey metamorphic rock
GNEISS_LT     = "#6A6865"   # lighter gneiss
MORAINE       = "#8A8580"   # rubble grey
ICE_WHITE     = "#E8EDF2"   # female glacier — bright, clean
ICE_GREY      = "#9A9B98"   # male glacier — debris-covered
ICE_BLUE      = "#B8D0E8"   # blue ice revealed in crevasse
MELT_WATER    = "#C8DDE8"   # glacial meltwater — pale blue-grey
HOT_SPRING    = "#E8A060"   # orange hydrothermal alteration
HOT_STEAM     = "#F0E8E0"   # white steam against dark rock
BARLEY_HAY    = "#D8C898"   # golden — the insulation material
WILLOW        = "#A8B888"   # green-brown of willow weave
CHARCOAL      = "#3A3838"   # seal material
EARTH         = "#C8A878"   # warm earth, mud
SKY_HIGH      = "#D8E0E8"   # pale high-altitude sky
ALPENGLOW     = "#E8A8A0"   # pink light on ice at sunset
SNOW          = "#F0F0F0"   # fresh snow


# ── Shared helpers ──────────────────────────────────────────────────

def make_fig(width=W, height=H, bg=GNEISS):
    fig, ax = plt.subplots(1, 1, figsize=(width, height), facecolor=bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def rock_texture(ax, color=GNEISS_LT, seed=42, n=20):
    """Subtle gneiss foliation lines."""
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x0 = rng.uniform(0, 100)
        y0 = rng.uniform(0, 100)
        length = rng.uniform(5, 25)
        angle = rng.uniform(-15, 15)  # roughly horizontal foliation
        dx = length * np.cos(np.radians(angle))
        dy = length * np.sin(np.radians(angle))
        ax.plot([x0, x0 + dx], [y0, y0 + dy],
                color=color, alpha=rng.uniform(0.05, 0.15),
                linewidth=rng.uniform(0.5, 2.0))


def mountain_profile(ax, peaks, base_y=30, color=GNEISS_LT, alpha=0.3):
    """Draw a mountain ridge profile."""
    xs = [0]
    ys = [base_y]
    for px, py in peaks:
        xs.append(px)
        ys.append(py)
    xs.append(100)
    ys.append(base_y)
    ax.fill(xs, ys, color=color, alpha=alpha)
    ax.plot(xs, ys, color=color, alpha=alpha + 0.2, linewidth=1.0)


def save(fig, name):
    path = OUT / f"{name}.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  ✓ {path.name}")


# ════════════════════════════════════════════════════════════════════
# Figure 1: The Two Waters
# ════════════════════════════════════════════════════════════════════

def fig1_two_waters():
    fig, ax = make_fig(bg=GNEISS)
    rock_texture(ax, seed=11)

    # Mountain backdrop — Nanga Parbat north face
    mountain_profile(ax, [(15, 55), (30, 72), (45, 88), (55, 85),
                          (65, 70), (80, 58)],
                     base_y=35, color=GNEISS_LT, alpha=0.25)

    # Snow and ice on upper slopes
    snow_xs = [25, 35, 45, 55, 50, 40, 30]
    snow_ys = [65, 78, 88, 85, 80, 72, 62]
    ax.fill(snow_xs, snow_ys, color=SNOW, alpha=0.3)

    # Glacier tongue descending
    glacier_xs = [38, 42, 48, 52, 50, 46, 40, 36]
    glacier_ys = [70, 75, 72, 65, 50, 42, 45, 55]
    ax.fill(glacier_xs, glacier_ys, color=ICE_WHITE, alpha=0.4)
    ax.fill(glacier_xs, glacier_ys, color=ICE_BLUE, alpha=0.15)

    # Meltwater stream — cold, left side
    stream_x = [44, 43, 41, 40, 38, 36, 35, 33]
    stream_y = [42, 38, 34, 30, 26, 22, 18, 14]
    ax.plot(stream_x, stream_y, color=MELT_WATER, linewidth=3, alpha=0.7)
    ax.plot(stream_x, stream_y, color=ICE_BLUE, linewidth=1.5, alpha=0.4)

    # Temperature label — cold
    ax.text(30, 16, "0°C", fontsize=14, color=MELT_WATER, alpha=0.8,
            fontfamily="serif", style="italic")

    # Hot spring — right side, orange glow
    spring_x, spring_y = 62, 22
    for r in range(8, 0, -1):
        circle = plt.Circle((spring_x, spring_y), r,
                            color=HOT_SPRING, alpha=0.04 * (9 - r))
        ax.add_patch(circle)

    # Steam rising
    rng = np.random.default_rng(33)
    for i in range(12):
        sx = spring_x + rng.uniform(-3, 3)
        sy = spring_y + rng.uniform(2, 20)
        ax.plot([sx, sx + rng.uniform(-1, 1)],
                [sy, sy + rng.uniform(2, 5)],
                color=HOT_STEAM, alpha=rng.uniform(0.15, 0.35),
                linewidth=rng.uniform(1, 3))

    # Temperature label — hot
    ax.text(68, 24, "92°C", fontsize=14, color=HOT_SPRING, alpha=0.9,
            fontfamily="serif", style="italic")

    # Caption text
    ax.text(50, 5, "Two waters from one source",
            fontsize=16, color=HOT_STEAM, alpha=0.7,
            ha="center", fontfamily="serif", style="italic")

    save(fig, "fig1-two-waters")


# ════════════════════════════════════════════════════════════════════
# Figure 2: Male and Female Glacier
# ════════════════════════════════════════════════════════════════════

def fig2_gender_of_ice():
    fig, ax = make_fig(width=14, height=8, bg=SKY_HIGH)

    # Split composition: male glacier (left), female glacier (right)

    # Male glacier — po gang — grey, debris-covered
    male_xs = [5, 10, 18, 25, 30, 35, 38, 35, 28, 20, 12, 5]
    male_ys = [30, 50, 62, 68, 65, 55, 35, 28, 25, 22, 24, 30]
    ax.fill(male_xs, male_ys, color=ICE_GREY, alpha=0.8)

    # Debris on male glacier surface
    rng = np.random.default_rng(44)
    for _ in range(40):
        rx = rng.uniform(8, 33)
        ry = rng.uniform(26, 60)
        # Check roughly inside polygon
        if ry < 25 or ry > 65:
            continue
        size = rng.uniform(0.3, 1.2)
        ax.plot(rx, ry, 'o', color=MORAINE, markersize=size * 3,
                alpha=rng.uniform(0.3, 0.7))

    ax.text(20, 16, "po gang", fontsize=18, color=GNEISS,
            ha="center", fontfamily="serif", style="italic")
    ax.text(20, 10, "grey  ·  debris-covered  ·  slow  ·  yields little water",
            fontsize=10, color=GNEISS, ha="center", fontfamily="serif", alpha=0.7)

    # Female glacier — mo gang — white/blue, clean, bright
    female_xs = [62, 67, 75, 82, 88, 93, 95, 92, 85, 78, 70, 62]
    female_ys = [30, 52, 65, 70, 67, 58, 35, 28, 24, 22, 24, 30]
    ax.fill(female_xs, female_ys, color=ICE_WHITE, alpha=0.9)
    ax.fill(female_xs, female_ys, color=ICE_BLUE, alpha=0.2)

    # Blue veins in female ice
    for _ in range(8):
        vx = rng.uniform(65, 90)
        vy = rng.uniform(30, 60)
        vlen = rng.uniform(3, 8)
        angle = rng.uniform(60, 120)
        dx = vlen * np.cos(np.radians(angle))
        dy = vlen * np.sin(np.radians(angle))
        ax.plot([vx, vx + dx], [vy, vy + dy],
                color=ICE_BLUE, alpha=rng.uniform(0.2, 0.5),
                linewidth=rng.uniform(1, 2.5))

    ax.text(78, 16, "mo gang", fontsize=18, color=ICE_BLUE,
            ha="center", fontfamily="serif", style="italic")
    ax.text(78, 10, "white  ·  clean  ·  growing  ·  gives water freely",
            fontsize=10, color=GNEISS_LT, ha="center", fontfamily="serif", alpha=0.7)

    # Dividing line
    ax.plot([50, 50], [5, 80], color=GNEISS_LT, alpha=0.2,
            linewidth=0.5, linestyle="--")

    # Meltwater streams
    # Male — thin trickle
    ax.plot([20, 19, 18], [24, 20, 16], color=MELT_WATER,
            linewidth=1.5, alpha=0.5)
    # Female — stronger flow
    ax.plot([78, 77, 75, 74], [24, 19, 15, 12], color=MELT_WATER,
            linewidth=3, alpha=0.7)
    ax.plot([78, 77, 75, 74], [24, 19, 15, 12], color=ICE_BLUE,
            linewidth=1.5, alpha=0.3)

    save(fig, "fig2-gender-of-ice")


# ════════════════════════════════════════════════════════════════════
# Figure 3: The Marriage Protocol — a sequence
# ════════════════════════════════════════════════════════════════════

def fig3_marriage_protocol():
    fig, axes = plt.subplots(1, 5, figsize=(18, 7), facecolor=GNEISS)

    steps = [
        ("male + female\nice", ICE_GREY, ICE_WHITE),
        ("coal +\nbarley hay", CHARCOAL, BARLEY_HAY),
        ("willow\nchorong", WILLOW, EARTH),
        ("north-facing\ncave, sealed", GNEISS_LT, CHARCOAL),
        ("twelve\nyears", SNOW, ICE_BLUE),
    ]

    labels = ["harvest", "insulate", "carry", "seal", "wait"]

    for i, (ax, (desc, c1, c2), label) in enumerate(zip(axes, steps, labels)):
        ax.set_facecolor(GNEISS)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_aspect("equal")
        ax.axis("off")

        # Central circle — two halves
        theta1 = np.linspace(0, np.pi, 50)
        theta2 = np.linspace(np.pi, 2 * np.pi, 50)
        r = 28

        # Top half
        x1 = 50 + r * np.cos(theta1)
        y1 = 55 + r * np.sin(theta1)
        ax.fill(np.append(x1, x1[0]), np.append(y1, y1[0]),
                color=c1, alpha=0.7)

        # Bottom half
        x2 = 50 + r * np.cos(theta2)
        y2 = 55 + r * np.sin(theta2)
        ax.fill(np.append(x2, x2[0]), np.append(y2, y2[0]),
                color=c2, alpha=0.7)

        # Ring outline
        theta_full = np.linspace(0, 2 * np.pi, 100)
        ax.plot(50 + r * np.cos(theta_full), 55 + r * np.sin(theta_full),
                color=HOT_STEAM, alpha=0.3, linewidth=1)

        # Step number
        ax.text(50, 92, str(i + 1), fontsize=20, color=HOT_STEAM,
                alpha=0.5, ha="center", fontfamily="serif")

        # Description
        ax.text(50, 50, desc, fontsize=11, color=HOT_STEAM,
                ha="center", va="center", fontfamily="serif",
                style="italic", alpha=0.9, linespacing=1.4)

        # Label below
        ax.text(50, 12, label, fontsize=13, color=BARLEY_HAY,
                ha="center", fontfamily="serif", alpha=0.7)

        # Arrow to next (except last)
        if i < 4:
            ax.annotate("", xy=(98, 55), xytext=(88, 55),
                       arrowprops=dict(arrowstyle="->", color=HOT_STEAM,
                                      lw=1, alpha=0.3))

    fig.subplots_adjust(wspace=0.05)
    save(fig, "fig3-marriage-protocol")


# ════════════════════════════════════════════════════════════════════
# Figure 4: The Dowry — basket, mountain, twelve years
# ════════════════════════════════════════════════════════════════════

def fig4_the_dowry():
    fig, ax = make_fig(bg=GNEISS)
    rock_texture(ax, seed=77)

    # Mountain — massive, filling upper half
    mountain_profile(ax, [(10, 50), (25, 68), (40, 82), (50, 90),
                          (60, 86), (75, 70), (90, 52)],
                     base_y=35, color=GNEISS_LT, alpha=0.2)

    # Snow cap
    snow_xs = [35, 42, 50, 58, 55, 48, 40]
    snow_ys = [75, 85, 90, 86, 82, 80, 72]
    ax.fill(snow_xs, snow_ys, color=SNOW, alpha=0.25)

    # Alpenglow on summit
    for r in range(12, 0, -1):
        circle = plt.Circle((50, 88), r * 1.5,
                            color=ALPENGLOW, alpha=0.02 * (13 - r))
        ax.add_patch(circle)

    # The chorong (basket) — small, at the base
    basket_x, basket_y = 50, 20
    # Conical shape — narrow base, wide rim
    bx = [basket_x - 3, basket_x - 8, basket_x + 8, basket_x + 3]
    by = [basket_y - 5, basket_y + 5, basket_y + 5, basket_y - 5]
    ax.fill(bx, by, color=WILLOW, alpha=0.6)

    # Weave pattern on basket
    rng = np.random.default_rng(55)
    for j in range(6):
        y_line = basket_y - 4 + j * 1.8
        width = 3 + (j / 5) * 5
        ax.plot([basket_x - width, basket_x + width], [y_line, y_line],
                color=EARTH, alpha=0.3, linewidth=0.8)

    # Ice pieces visible inside basket
    ax.plot(basket_x - 2, basket_y + 1, 's', color=ICE_GREY,
            markersize=6, alpha=0.6)
    ax.plot(basket_x + 2, basket_y + 1, 's', color=ICE_WHITE,
            markersize=6, alpha=0.8)

    # Text: "we carry the dowry"
    ax.text(50, 9, "we carry the dowry",
            fontsize=16, color=BARLEY_HAY, alpha=0.7,
            ha="center", fontfamily="serif", style="italic")

    # Text: "the mountain provides the house"
    ax.text(50, 42, "the mountain provides the house",
            fontsize=14, color=HOT_STEAM, alpha=0.5,
            ha="center", fontfamily="serif", style="italic")

    # Twelve-year arc — dotted semicircle connecting basket to mountain
    theta = np.linspace(0.2, np.pi - 0.2, 50)
    arc_r = 25
    arc_x = 50 + arc_r * np.cos(theta)
    arc_y = 30 + arc_r * np.sin(theta) * 0.8
    ax.plot(arc_x, arc_y, color=BARLEY_HAY, alpha=0.25,
            linewidth=1.5, linestyle=":")

    # "12 years" along the arc
    ax.text(50, 52, "12 years", fontsize=11, color=BARLEY_HAY,
            alpha=0.4, ha="center", fontfamily="serif", style="italic",
            rotation=0)

    save(fig, "fig4-the-dowry")


# ════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Generating illustrations → {OUT}/")
    fig1_two_waters()
    fig2_gender_of_ice()
    fig3_marriage_protocol()
    fig4_the_dowry()
    print("Done.")
