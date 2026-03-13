# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Peg-Path" (Story #18).

The Indus gorge below Chilas. Petroglyph terraces — 50,000 marks,
ten writing systems, ten thousand years. The palimpsest. The dam.
The ibex above the waterline.

Visual language: dark rock surfaces with lighter carved marks.
The gorge palette — dark gneiss, pale carved lines, the brown-grey
of weathered rock. The ibex in silhouette against sky.

Run with:  uv run generate_images_peg_path.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Output ──────────────────────────────────────────────────────────
SLUG = "the-peg-path"
OUT = (Path(__file__).parent / f"../../website/static/images/writing/{SLUG}").resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9

# ── Palette: Indus Gorge / Petroglyphs ────────────────────────────
ROCK_DARK     = "#2A2826"   # dark gneiss boulder surface
ROCK_MED      = "#4A4642"   # medium rock
ROCK_LT       = "#6A6662"   # lighter weathered surface
CARVED        = "#C8C0B0"   # carved line — lighter than rock
CARVED_OLD    = "#9A9488"   # older, more weathered carving
CARVED_FAINT  = "#7A7670"   # very old, barely visible
PATINA        = "#5A5650"   # desert varnish / patina
INDUS         = "#8A9088"   # grey-green glacial river
INDUS_DARK    = "#6A7068"   # deeper water
SKY_GORGE     = "#C8D0D8"   # pale sky seen from gorge depth
WATER_LINE    = "#5888A8"   # the dam water level — blue-grey
IBEX_BROWN    = "#8A7868"   # ibex silhouette
CLIFF_ORANGE  = "#C8A070"   # hydrothermal alteration


# ── Shared helpers ──────────────────────────────────────────────────

def make_fig(width=W, height=H, bg=ROCK_DARK):
    fig, ax = plt.subplots(1, 1, figsize=(width, height), facecolor=bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def rock_grain(ax, color=ROCK_MED, seed=42, n=25):
    """Subtle grain on rock surface."""
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x0 = rng.uniform(0, 100)
        y0 = rng.uniform(0, 100)
        length = rng.uniform(2, 10)
        angle = rng.uniform(0, 180)
        dx = length * np.cos(np.radians(angle))
        dy = length * np.sin(np.radians(angle))
        ax.plot([x0, x0 + dx], [y0, y0 + dy],
                color=color, alpha=rng.uniform(0.05, 0.12),
                linewidth=rng.uniform(0.5, 1.5))


def draw_ibex(ax, x, y, scale=1.0, color=CARVED, alpha=0.8, facing="right"):
    """Simple ibex petroglyph — horned profile."""
    direction = 1 if facing == "right" else -1
    s = scale
    # Body
    body_x = [x, x + 6*s*direction, x + 8*s*direction, x + 10*s*direction,
              x + 8*s*direction, x + 2*s*direction]
    body_y = [y, y + 1*s, y + 1.5*s, y, y - 1*s, y - 1*s]
    ax.fill(body_x, body_y, color=color, alpha=alpha)
    # Horns — curved backward
    horn_x = [x + 1*s*direction, x - 1*s*direction, x - 3*s*direction, x - 2*s*direction]
    horn_y = [y + 1*s, y + 4*s, y + 6*s, y + 7*s]
    ax.plot(horn_x, horn_y, color=color, alpha=alpha, linewidth=2*s)
    # Legs
    for lx_off in [3, 7]:
        ax.plot([x + lx_off*s*direction, x + lx_off*s*direction],
                [y - 1*s, y - 4*s], color=color, alpha=alpha, linewidth=1.5*s)


def draw_stupa(ax, x, y, scale=1.0, color=CARVED, alpha=0.7):
    """Simple stupa petroglyph."""
    s = scale
    # Base
    ax.plot([x - 4*s, x + 4*s], [y, y], color=color, alpha=alpha, linewidth=2*s)
    # Dome
    theta = np.linspace(0, np.pi, 30)
    dome_x = x + 3.5*s * np.cos(theta)
    dome_y = y + 3.5*s * np.sin(theta)
    ax.plot(dome_x, dome_y, color=color, alpha=alpha, linewidth=1.5*s)
    # Harmika (box on top)
    ax.plot([x - 1.5*s, x + 1.5*s, x + 1.5*s, x - 1.5*s, x - 1.5*s],
            [y + 3.5*s, y + 3.5*s, y + 5*s, y + 5*s, y + 3.5*s],
            color=color, alpha=alpha, linewidth=1.5*s)
    # Chattra (parasol)
    ax.plot([x, x], [y + 5*s, y + 8*s], color=color, alpha=alpha, linewidth=1*s)
    for h in [6, 7, 8]:
        w = (9 - h) * 0.8 * s
        ax.plot([x - w, x + w], [y + h*s, y + h*s],
                color=color, alpha=alpha * 0.8, linewidth=1*s)


def save(fig, name):
    path = OUT / f"{name}.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  ✓ {path.name}")


# ════════════════════════════════════════════════════════════════════
# Figure 1: The Palimpsest — ibex and stupa on the same rock
# ════════════════════════════════════════════════════════════════════

def fig1_palimpsest():
    fig, ax = make_fig(bg=ROCK_DARK)
    rock_grain(ax, seed=21, n=30)

    # Boulder surface — slightly lighter area in centre
    boulder = plt.Circle((50, 50), 40, color=ROCK_MED, alpha=0.2)
    ax.add_patch(boulder)

    # Old ibex — faint, large, the oldest layer
    draw_ibex(ax, 30, 45, scale=2.0, color=CARVED_FAINT, alpha=0.4)

    # Another old ibex — different position
    draw_ibex(ax, 55, 60, scale=1.5, color=CARVED_OLD, alpha=0.5, facing="left")

    # Stupa carved over/beside the ibex — brighter, newer
    draw_stupa(ax, 45, 35, scale=1.8, color=CARVED, alpha=0.7)

    # Sogdian-style text — abstract cursive marks
    rng = np.random.default_rng(66)
    text_x = 68
    for i in range(6):
        y_pos = 50 + i * 3
        length = rng.uniform(3, 8)
        # Cursive-like squiggle
        xs = np.linspace(text_x, text_x + length, 10)
        ys = y_pos + rng.uniform(-0.5, 0.5, 10).cumsum() * 0.3
        ax.plot(xs, ys, color=CARVED, alpha=0.5, linewidth=1.2)

    # Modern scratched name — brightest, crudest
    ax.text(20, 18, "AHMAD 2019", fontsize=8, color=CARVED,
            alpha=0.3, fontfamily="monospace", rotation=5)

    # Caption
    ax.text(50, 5, "the rock does not choose between its tenants",
            fontsize=14, color=CARVED_OLD, alpha=0.6,
            ha="center", fontfamily="serif", style="italic")

    save(fig, "fig1-palimpsest")


# ════════════════════════════════════════════════════════════════════
# Figure 2: Ten Writing Systems — the multilingual gorge
# ════════════════════════════════════════════════════════════════════

def fig2_writing_systems():
    fig, ax = make_fig(bg=ROCK_DARK)
    rock_grain(ax, seed=33, n=20)

    scripts = [
        ("Kharoshthi", 12, 82, 9, 0),
        ("Brahmi", 45, 85, 11, -3),
        ("Sogdian", 78, 80, 10, 5),
        ("Proto-Sharada", 15, 62, 9, 2),
        ("Bactrian", 50, 65, 9, -2),
        ("Chinese", 82, 60, 10, 0),
        ("Tibetan", 20, 42, 9, 3),
        ("Middle Persian", 55, 45, 9, -4),
        ("Parthian", 80, 40, 9, 1),
        ("Hebrew (?)", 45, 25, 8, 6),
    ]

    rng = np.random.default_rng(88)

    for name, x, y, size, rot in scripts:
        # Abstract script-like marks
        for j in range(rng.integers(3, 7)):
            sx = x + rng.uniform(-4, 12)
            sy = y + rng.uniform(-2, 2)
            length = rng.uniform(1, 4)
            angle = rot + rng.uniform(-20, 20)
            dx = length * np.cos(np.radians(angle))
            dy = length * np.sin(np.radians(angle))
            age = rng.uniform(0.3, 0.9)
            ax.plot([sx, sx + dx], [sy, sy + dy],
                    color=CARVED, alpha=age * 0.6,
                    linewidth=rng.uniform(1, 2.5))

        # Script name — faint label
        ax.text(x, y - 5, name, fontsize=size, color=CARVED_OLD,
                alpha=0.4, fontfamily="serif", style="italic",
                rotation=rot)

    # River line at bottom
    river_y = 10
    xs = np.linspace(0, 100, 100)
    ys = river_y + 1.5 * np.sin(xs * 0.1)
    ax.fill_between(xs, 0, ys, color=INDUS, alpha=0.3)

    ax.text(50, 4, "ten writing systems  ·  one stretch of riverbank",
            fontsize=13, color=INDUS, alpha=0.6,
            ha="center", fontfamily="serif", style="italic")

    save(fig, "fig2-writing-systems")


# ════════════════════════════════════════════════════════════════════
# Figure 3: The Water Line — what drowns, what remains
# ════════════════════════════════════════════════════════════════════

def fig3_water_line():
    fig, ax = make_fig(bg=SKY_GORGE)

    # Cliff walls — dark, vertical
    ax.fill([0, 0, 25, 20], [0, 100, 100, 0], color=ROCK_DARK, alpha=0.8)
    ax.fill([100, 100, 75, 80], [0, 100, 100, 0], color=ROCK_DARK, alpha=0.8)

    # Rock grain on cliff faces
    rng = np.random.default_rng(44)
    for side in [(5, 20), (80, 95)]:
        for _ in range(15):
            x0 = rng.uniform(*side)
            y0 = rng.uniform(10, 95)
            ax.plot([x0, x0 + rng.uniform(-1, 1)],
                    [y0, y0 + rng.uniform(2, 8)],
                    color=ROCK_LT, alpha=0.1, linewidth=1)

    # Petroglyphs on cliff face — below water line
    for _ in range(8):
        px = rng.uniform(5, 18)
        py = rng.uniform(15, 40)
        draw_ibex(ax, px, py, scale=0.6, color=CARVED_OLD, alpha=0.4)

    for _ in range(4):
        px = rng.uniform(82, 93)
        py = rng.uniform(20, 38)
        draw_stupa(ax, px, py, scale=0.5, color=CARVED_OLD, alpha=0.35)

    # The water line — horizontal, the dam level
    water_level = 45
    ax.fill_between([0, 100], 0, water_level, color=WATER_LINE, alpha=0.35)
    ax.plot([0, 100], [water_level, water_level],
            color=WATER_LINE, alpha=0.6, linewidth=2, linestyle="--")

    ax.text(50, water_level + 2, "— reservoir level —",
            fontsize=11, color=WATER_LINE, alpha=0.7,
            ha="center", fontfamily="serif", style="italic")

    # Percentage labels
    ax.text(50, water_level - 8, "86% submerged",
            fontsize=14, color=CARVED, alpha=0.5,
            ha="center", fontfamily="serif")
    ax.text(50, water_level - 13, "30,000 carvings",
            fontsize=11, color=CARVED_OLD, alpha=0.4,
            ha="center", fontfamily="serif", style="italic")

    # Ibex on cliff ABOVE waterline — alive, silhouetted
    ibex_x, ibex_y = 15, 72
    draw_ibex(ax, ibex_x, ibex_y, scale=1.2, color=IBEX_BROWN, alpha=0.8)

    # A second ibex higher up
    draw_ibex(ax, 83, 80, scale=0.9, color=IBEX_BROWN, alpha=0.7, facing="left")

    ax.text(50, 90, "the symbol drowns  ·  the animal climbs",
            fontsize=14, color=ROCK_LT, alpha=0.6,
            ha="center", fontfamily="serif", style="italic")

    save(fig, "fig3-water-line")


# ════════════════════════════════════════════════════════════════════
# Figure 4: The Ibex Above — silhouette against sky
# ════════════════════════════════════════════════════════════════════

def fig4_ibex_above():
    fig, ax = make_fig(bg=SKY_GORGE)

    # Ridge line
    ridge_x = [0, 15, 25, 35, 42, 50, 58, 65, 75, 85, 100]
    ridge_y = [40, 38, 42, 36, 40, 38, 41, 37, 39, 35, 38]
    ax.fill_between(ridge_x, 0, ridge_y, color=ROCK_DARK, alpha=0.9)

    # Rock texture below ridge
    rng = np.random.default_rng(55)
    for _ in range(30):
        x0 = rng.uniform(0, 100)
        y0 = rng.uniform(0, 35)
        ax.plot([x0, x0 + rng.uniform(-2, 2)],
                [y0, y0 + rng.uniform(1, 4)],
                color=ROCK_MED, alpha=0.08, linewidth=1)

    # Single ibex on the ridgeline — bold silhouette
    # Larger, more detailed ibex
    ix, iy = 52, 40
    s = 3.0

    # Body — fuller shape
    body_x = [ix, ix+2*s, ix+4*s, ix+6*s, ix+7*s, ix+8*s,
              ix+7*s, ix+5*s, ix+3*s, ix+1*s]
    body_y = [iy, iy+1.5*s, iy+2*s, iy+1.5*s, iy+0.5*s, iy-0.5*s,
              iy-1.5*s, iy-1.5*s, iy-1*s, iy-0.5*s]
    ax.fill(body_x, body_y, color=IBEX_BROWN, alpha=0.9)

    # Head
    head = plt.Circle((ix - 0.5*s, iy + 0.5*s), 1.2*s,
                       color=IBEX_BROWN, alpha=0.9)
    ax.add_patch(head)

    # Horns — large, curved, the defining feature
    horn_t = np.linspace(0, 1, 20)
    horn_x = ix - 1*s - horn_t * 4*s + horn_t**2 * 2*s
    horn_y = iy + 1.5*s + horn_t * 8*s - horn_t**2 * 1*s
    ax.plot(horn_x, horn_y, color=IBEX_BROWN, alpha=0.9, linewidth=3.5)

    # Legs
    for lx in [ix + 2*s, ix + 5.5*s]:
        ax.plot([lx, lx - 0.3*s], [iy - 1.5*s, iy - 4.5*s],
                color=IBEX_BROWN, alpha=0.9, linewidth=2.5)
        ax.plot([lx + 1*s, lx + 0.7*s], [iy - 1.5*s, iy - 4.5*s],
                color=IBEX_BROWN, alpha=0.9, linewidth=2.5)

    # Sky — graduated
    for y_band in range(45, 100, 2):
        alpha = 0.02 + (y_band - 45) * 0.001
        ax.axhspan(y_band, y_band + 2, color="#D8E4F0", alpha=alpha)

    # Text
    ax.text(50, 8, "ten thousand years  ·  the same ridgeline",
            fontsize=14, color=ROCK_LT, alpha=0.5,
            ha="center", fontfamily="serif", style="italic")

    save(fig, "fig4-ibex-above")


# ════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Generating illustrations → {OUT}/")
    fig1_palimpsest()
    fig2_writing_systems()
    fig3_water_line()
    fig4_ibex_above()
    print("Done.")
