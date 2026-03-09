# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Six Tri-Junctions".

Six chapters, six places where three valleys / traditions / languages
converge. The Thread Walker moves from the Parvati headwall to the
Karakoram. Visual register shifts as she moves north: warm monsoon
tones (green-brown) for chapters I-III, mineral Karakoram tones
(grey-orange-blue) for chapters IV-VI.

Ten figures total:
  Ch I:   the-rain-wall.png, three-climates.png
  Ch II:  two-processions.png
  Ch III: three-flocks.png
  Ch IV:  the-petroglyphs.png, the-palimpsest.png
  Ch V:   three-faces.png, the-gorge.png
  Ch VI:  three-languages.png, the-bitan.png

Run with:  uv run generate_images.py
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
SLUG = Path(__file__).parent.name
OUT = (Path(__file__).parent / "../../website/static/images/writing" / SLUG).resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9  # inches — 1800×1350 px at 150 DPI

# ── Palette ─────────────────────────────────────────────────────────
# Monsoon palette (chapters I-III)
PARCHMENT     = "#F5F0E8"
PARCHMENT_DK  = "#EDE6D8"
INK           = "#5C4A3A"
INK_LIGHT     = "#8B7B6B"
INK_FAINT     = "#C4B8A8"

# Slate palette (shared)
SLATE         = "#3A3A38"
SLATE_LT      = "#5A5A58"
CHALK         = "#E8E4D8"
CHALK_DK      = "#D0C8B8"
CHALK_DIM     = "#9A9890"

# Geography colours
DEODAR_GREEN  = "#3A6B4A"
DEODAR_DK     = "#2A4A32"
JUNIPER_GREY  = "#7A8B7A"
MUD_BROWN     = "#8B7B5A"
SNOW_WHITE    = "#F0EEE8"
GLACIER_BLUE  = "#8AAAB8"
GLACIER_DK    = "#6A8A98"

# Karakoram palette (chapters IV-VI)
GNEISS_GREY   = "#6A6A68"
GNEISS_DK     = "#4A4A48"
HYDROTHERMAL  = "#C4886B"   # orange alteration
MELTWATER     = "#5A8BA0"
MINERAL_LIGHT = "#D8D0C4"

# Accent colours
MAROON        = "#6B2A2A"
SAFFRON       = "#C89030"
COPPER        = "#C4886B"
WALNUT        = "#4A3728"

# Petroglyph colours
ROCK_SURFACE  = "#8A8478"
ROCK_DK       = "#5A5448"
CARVING       = "#C8C0B0"
CARVING_DK    = "#A8A090"

# Script colours (three unrelated language families)
SHINA_INK     = "#5A4A38"      # Indo-Aryan — warm brown
BURUSHASKI_INK = "#3A5A6A"     # isolate — cool blue-grey
WAKHI_INK     = "#6A3A3A"      # Iranian — deep red-brown


# ── Shared helpers ──────────────────────────────────────────────────

def make_fig(width=W, height=H, bg=PARCHMENT):
    fig, ax = plt.subplots(1, 1, figsize=(width, height), facecolor=bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def jitter(arr, rng, scale=0.3):
    """Add hand-drawn wobble."""
    return arr + rng.normal(0, scale, len(arr))


def draw_mountain_ridge(ax, xs, ys, colour, lw=1.5, rng=None, seed=42):
    """Draw a mountain ridge with hand-drawn wobble."""
    if rng is None:
        rng = np.random.default_rng(seed)
    ax.plot(jitter(xs, rng, 0.2), jitter(ys, rng, 0.3), color=colour,
            linewidth=lw, solid_capstyle="round")


def draw_peak(ax, cx, cy, width, height, colour, rng=None, fill=None, lw=1.5):
    """Draw a single mountain peak."""
    if rng is None:
        rng = np.random.default_rng(42)
    xs = np.array([cx - width/2, cx, cx + width/2])
    ys = np.array([cy, cy + height, cy])
    ax.plot(jitter(xs, rng, 0.3), jitter(ys, rng, 0.3), color=colour,
            linewidth=lw, solid_capstyle="round")
    if fill:
        ax.fill(xs, ys, color=fill, alpha=0.3)


def draw_pass(ax, cx, cy, width, colour, rng=None, lw=1.0):
    """Draw a pass as a dip between two peaks."""
    if rng is None:
        rng = np.random.default_rng(42)
    xs = np.array([cx - width/2, cx - width/4, cx, cx + width/4, cx + width/2])
    ys = np.array([cy + 3, cy + 1.5, cy, cy + 1.5, cy + 3])
    ax.plot(jitter(xs, rng, 0.2), jitter(ys, rng, 0.2), color=colour,
            linewidth=lw, solid_capstyle="round")


def draw_river(ax, xs, ys, colour, lw=1.0, rng=None):
    """Draw a river with flowing wobble."""
    if rng is None:
        rng = np.random.default_rng(42)
    ax.plot(jitter(xs, rng, 0.4), jitter(ys, rng, 0.2), color=colour,
            linewidth=lw, solid_capstyle="round")


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  saved {path.name}")


# ════════════════════════════════════════════════════════════════════
# CHAPTER I — The Rain Wall
# ════════════════════════════════════════════════════════════════════

def fig_rain_wall():
    """Fig 1: The headwall — three passes fanning from Mantalai Lake."""
    fig, ax = make_fig(bg=PARCHMENT)

    rng = np.random.default_rng(101)

    # Background wash — pale blue-grey sky
    sky = mpatches.FancyBboxPatch((0, 55), 100, 45, boxstyle="square,pad=0",
                                   facecolor="#D8E0E8", alpha=0.3)
    ax.add_patch(sky)

    # Draw the three ridges converging at the headwall
    # Left ridge (toward Spiti — Pin Parvati)
    xs_l = np.linspace(5, 50, 30)
    ys_l = 40 + 25 * np.exp(-((xs_l - 25)**2) / 200) + 5 * np.sin(xs_l * 0.3)
    draw_mountain_ridge(ax, xs_l, ys_l, GNEISS_GREY, lw=2, rng=rng)
    ax.fill_between(xs_l, ys_l, 30, color=GNEISS_GREY, alpha=0.15)

    # Right ridge (toward Lahaul)
    xs_r = np.linspace(50, 95, 30)
    ys_r = 40 + 22 * np.exp(-((xs_r - 75)**2) / 200) + 4 * np.sin(xs_r * 0.35)
    draw_mountain_ridge(ax, xs_r, ys_r, GNEISS_GREY, lw=2, rng=rng)
    ax.fill_between(xs_r, ys_r, 30, color=GNEISS_GREY, alpha=0.15)

    # Central ridge (toward Tos glacier)
    xs_c = np.linspace(35, 65, 20)
    ys_c = 50 + 20 * np.exp(-((xs_c - 50)**2) / 100)
    draw_mountain_ridge(ax, xs_c, ys_c, GNEISS_DK, lw=2, rng=rng)

    # Snow caps
    for cx, cy in [(25, 66), (50, 70), (75, 63)]:
        snow_x = np.array([cx-4, cx-2, cx, cx+2, cx+4])
        snow_y = np.array([cy-1, cy+1, cy+2, cy+1, cy-1])
        ax.fill(snow_x, snow_y, color=SNOW_WHITE, alpha=0.8)

    # Three passes — dips in the ridges
    draw_pass(ax, 35, 52, 8, COPPER, rng=rng, lw=1.5)
    draw_pass(ax, 55, 54, 7, COPPER, rng=rng, lw=1.5)
    draw_pass(ax, 42, 48, 6, COPPER, rng=rng, lw=1.5)

    # Lake at base
    lake_x = np.array([38, 42, 50, 58, 62, 58, 50, 42, 38])
    lake_y = np.array([32, 30, 29, 30, 32, 34, 35, 34, 32])
    ax.fill(lake_x, lake_y, color=GLACIER_BLUE, alpha=0.5)
    ax.plot(jitter(lake_x, rng, 0.2), jitter(lake_y, rng, 0.2),
            color=GLACIER_DK, linewidth=1, solid_capstyle="round")

    # Three arrows from lake to passes
    for px, py, label, ha in [(30, 55, "Pin Parvati\n→ Spiti", "right"),
                               (55, 57, "Kulti col\n→ Lahaul", "left"),
                               (45, 50, "Tos col", "center")]:
        ax.annotate("", xy=(px, py), xytext=(50, 33),
                    arrowprops=dict(arrowstyle="->", color=COPPER, lw=1.2))
        ax.text(px, py + 2, label, fontsize=8, color=INK, ha=ha,
                fontstyle="italic")

    # Lake label
    ax.text(50, 26, "Mantalai Lake", fontsize=10, color=INK_LIGHT,
            ha="center", fontstyle="italic")

    # River flowing south from lake
    river_x = np.array([50, 49, 48, 47, 46, 45, 44, 43])
    river_y = np.array([29, 24, 20, 16, 12, 8, 5, 2])
    draw_river(ax, river_x, river_y, MELTWATER, lw=1.5, rng=rng)
    ax.text(42, 6, "Parvati →", fontsize=8, color=MELTWATER, ha="center",
            fontstyle="italic")

    # Title
    ax.text(50, 95, "The Headwall", fontsize=14, color=INK, ha="center",
            fontweight="bold")
    ax.text(50, 91, "Three passes from one lake — three countries",
            fontsize=9, color=INK_LIGHT, ha="center", fontstyle="italic")

    save(fig, "the-rain-wall.png")


def fig_three_climates():
    """Fig 2: Three climate panels — deodar / juniper / mud-brick."""
    fig, axes = plt.subplots(1, 3, figsize=(W, H//1.2), facecolor=PARCHMENT)

    rng = np.random.default_rng(102)

    panels = [
        ("Parvati face", "1,200 mm", DEODAR_GREEN, DEODAR_DK, "deodar"),
        ("Spiti face", "200 mm", JUNIPER_GREY, GNEISS_GREY, "juniper"),
        ("Lahaul face", "300 mm", MUD_BROWN, GNEISS_DK, "mud-brick"),
    ]

    for ax, (title, precip, col1, col2, veg) in zip(axes, panels):
        ax.set_facecolor(PARCHMENT)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_aspect("equal")
        ax.axis("off")

        # Ground
        ax.fill_between([0, 100], [0, 0], [30, 30], color=col2, alpha=0.15)

        # Mountain slope
        xs = np.linspace(0, 100, 30)
        ys = 30 + 40 * (1 - np.abs(xs - 50) / 50) + rng.normal(0, 2, 30)
        ax.plot(xs, ys, color=col2, linewidth=1.5)
        ax.fill_between(xs, ys, 30, color=col1, alpha=0.2)

        # Vegetation marks
        if veg == "deodar":
            # Conifer triangles
            for _ in range(25):
                tx = rng.uniform(10, 90)
                ty = rng.uniform(32, 55)
                size = rng.uniform(1.5, 3)
                tree_x = [tx, tx - size*0.4, tx + size*0.4]
                tree_y = [ty + size, ty, ty]
                ax.fill(tree_x, tree_y, color=DEODAR_GREEN, alpha=0.6)
        elif veg == "juniper":
            # Sparse low shrubs
            for _ in range(12):
                tx = rng.uniform(15, 85)
                ty = rng.uniform(32, 45)
                ax.plot([tx-1, tx, tx+1], [ty, ty+1, ty],
                        color=JUNIPER_GREY, linewidth=1.5)
        else:
            # Mud-brick rectangles
            for _ in range(6):
                tx = rng.uniform(25, 75)
                ty = rng.uniform(32, 42)
                rect = mpatches.Rectangle((tx, ty), 3, 2,
                                          facecolor=MUD_BROWN, edgecolor=col2,
                                          linewidth=0.8, alpha=0.6)
                ax.add_patch(rect)

        # Rain indication — density
        n_drops = {"deodar": 60, "juniper": 8, "mud-brick": 15}[veg]
        for _ in range(n_drops):
            rx = rng.uniform(5, 95)
            ry = rng.uniform(65, 95)
            ax.plot([rx, rx], [ry, ry - 2], color=MELTWATER, alpha=0.3,
                    linewidth=0.5)

        # Labels
        ax.text(50, 92, title, fontsize=11, color=INK, ha="center",
                fontweight="bold")
        ax.text(50, 86, precip, fontsize=9, color=INK_LIGHT, ha="center",
                fontstyle="italic")

    fig.suptitle("Three climates from one ridge", fontsize=13, color=INK,
                 y=0.98, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save(fig, "three-climates.png")


# ════════════════════════════════════════════════════════════════════
# CHAPTER II — The Statue with Two Names
# ════════════════════════════════════════════════════════════════════

def fig_two_processions():
    """Fig 3: Trilokinath — two processions arriving at one temple."""
    fig, ax = make_fig(bg=PARCHMENT_DK)

    rng = np.random.default_rng(201)

    # Temple — pagoda silhouette at center
    # Base
    temple_base = mpatches.Rectangle((40, 35), 20, 12,
                                      facecolor=MINERAL_LIGHT, edgecolor=INK,
                                      linewidth=1.5)
    ax.add_patch(temple_base)

    # Tiered roof
    tiers = [(38, 47, 24, 6), (40, 53, 20, 5), (42, 58, 16, 4), (44, 62, 12, 3)]
    for tx, ty, tw, th in tiers:
        roof_x = [tx, tx + tw/2, tx + tw]
        roof_y = [ty, ty + th, ty]
        ax.fill(roof_x, roof_y, color=WALNUT, alpha=0.6)
        ax.plot(roof_x, roof_y, color=INK, linewidth=1)

    # Finial
    ax.plot([50, 50], [65, 70], color=SAFFRON, linewidth=2)
    ax.plot(50, 71, "o", color=SAFFRON, markersize=4)

    # Gate
    gate = mpatches.FancyBboxPatch((46, 35), 8, 10,
                                    boxstyle="round,pad=0.5",
                                    facecolor=WALNUT, edgecolor=INK,
                                    linewidth=1, alpha=0.5)
    ax.add_patch(gate)

    # Hindu procession from the south (left)
    proc_h_x = np.array([5, 12, 18, 24, 30, 36, 42, 46])
    proc_h_y = np.array([15, 18, 22, 25, 28, 30, 33, 35])
    draw_river(ax, proc_h_x, proc_h_y, SAFFRON, lw=2, rng=rng)

    # Hindu figures — small marks along the path
    for i in range(6):
        fx = proc_h_x[i] + rng.uniform(-1, 1)
        fy = proc_h_y[i] + rng.uniform(0, 2)
        ax.plot(fx, fy, "o", color=SAFFRON, markersize=3, alpha=0.7)
        # Small garland mark
        ax.plot([fx - 0.5, fx, fx + 0.5], [fy + 1, fy + 1.5, fy + 1],
                color=SAFFRON, linewidth=0.8, alpha=0.6)

    # Buddhist procession from the east (right)
    proc_b_x = np.array([95, 88, 82, 76, 70, 64, 58, 54])
    proc_b_y = np.array([20, 22, 25, 27, 29, 31, 33, 35])
    draw_river(ax, proc_b_x, proc_b_y, MAROON, lw=2, rng=rng)

    # Buddhist figures
    for i in range(6):
        fx = proc_b_x[i] + rng.uniform(-1, 1)
        fy = proc_b_y[i] + rng.uniform(0, 2)
        ax.plot(fx, fy, "s", color=MAROON, markersize=3, alpha=0.7)

    # Prayer flags from temple
    for i in range(5):
        flag_x = 54 + i * 5
        flag_y = 55 + rng.uniform(-2, 2)
        cols = [SAFFRON, "#FFFFFF", MAROON, DEODAR_GREEN, MELTWATER]
        ax.plot([54, flag_x], [60, flag_y], color=cols[i % 5],
                linewidth=0.6, alpha=0.5)

    # Labels
    ax.text(15, 10, "Hindu procession\nfrom the south", fontsize=8,
            color=SAFFRON, fontstyle="italic", ha="center")
    ax.text(85, 15, "Buddhist procession\nfrom the east", fontsize=8,
            color=MAROON, fontstyle="italic", ha="center")

    # Mountain backdrop
    for cx, cy, w, h in [(20, 75, 25, 18), (50, 80, 20, 15), (80, 73, 22, 16)]:
        draw_peak(ax, cx, cy, w, h, INK_FAINT, rng=rng, fill=INK_FAINT)

    # Title
    ax.text(50, 95, "Trilokinath", fontsize=14, color=INK, ha="center",
            fontweight="bold")
    ax.text(50, 91, "One temple, two names, one stone", fontsize=9,
            color=INK_LIGHT, ha="center", fontstyle="italic")

    save(fig, "two-processions.png")


# ════════════════════════════════════════════════════════════════════
# CHAPTER III — The Meadow Where Three Flocks Arrive
# ════════════════════════════════════════════════════════════════════

def fig_three_flocks():
    """Fig 4: Three trails converging on a meadow above Bara Bhangal."""
    fig, ax = make_fig(bg=PARCHMENT)

    rng = np.random.default_rng(301)

    # Green meadow at centre
    meadow_x = np.array([30, 35, 45, 55, 65, 70, 65, 55, 45, 35, 30])
    meadow_y = np.array([40, 35, 33, 33, 35, 40, 48, 50, 50, 48, 40])
    ax.fill(meadow_x, meadow_y, color=DEODAR_GREEN, alpha=0.15)
    ax.plot(jitter(meadow_x, rng, 0.3), jitter(meadow_y, rng, 0.3),
            color=DEODAR_GREEN, linewidth=1, alpha=0.5)

    # Surrounding ridges
    ridge_x = np.linspace(0, 100, 40)
    ridge_y = 55 + 15 * np.sin(ridge_x * 0.08) + rng.normal(0, 1.5, 40)
    draw_mountain_ridge(ax, ridge_x, ridge_y, GNEISS_GREY, lw=1.5, rng=rng)
    ax.fill_between(ridge_x, ridge_y, 100, color="#D8E0E8", alpha=0.2)

    # Three trails converging
    # Trail from east (Kullu) — straight line
    trail_e_x = np.array([95, 85, 78, 72, 68, 65])
    trail_e_y = np.array([42, 41, 40, 40, 40, 40])
    ax.plot(trail_e_x, trail_e_y, color=COPPER, linewidth=1.5, linestyle="--")

    # Trail from south (Kangra) — curved
    trail_s_x = np.array([50, 50, 50, 50, 50, 50])
    trail_s_y = np.array([5, 12, 18, 24, 28, 33])
    ax.plot(trail_s_x, trail_s_y, color=SAFFRON, linewidth=1.5, linestyle="--")

    # Trail from northwest (Chamba) — following water
    trail_nw_x = np.array([8, 15, 22, 28, 33, 35])
    trail_nw_y = np.array([60, 55, 50, 46, 43, 40])
    ax.plot(trail_nw_x, trail_nw_y, color=MAROON, linewidth=1.5, linestyle="--")

    # Flock marks — small dots along each trail
    # Kullu flock — linear pattern
    for i in range(8):
        fx = 70 + i * 2.5 + rng.uniform(-0.5, 0.5)
        fy = 40 + rng.uniform(-1, 1)
        ax.plot(fx, fy, ".", color=COPPER, markersize=4)

    # Kangra flock — circular pattern
    for angle in np.linspace(0, 2 * np.pi, 10):
        fx = 50 + 4 * np.cos(angle) + rng.uniform(-0.5, 0.5)
        fy = 25 + 3 * np.sin(angle) + rng.uniform(-0.5, 0.5)
        ax.plot(fx, fy, ".", color=SAFFRON, markersize=4)

    # Chamba flock — scattered, following terrain
    for i in range(8):
        fx = 15 + i * 3 + rng.uniform(-1, 1)
        fy = 55 - i * 2 + rng.uniform(-1, 1)
        ax.plot(fx, fy, ".", color=MAROON, markersize=4)

    # Labels
    ax.text(90, 45, "Kullu\n(east)", fontsize=8, color=COPPER,
            ha="center", fontstyle="italic")
    ax.text(50, 2, "Kangra (south)", fontsize=8, color=SAFFRON,
            ha="center", fontstyle="italic")
    ax.text(8, 65, "Chamba\n(northwest)", fontsize=8, color=MAROON,
            ha="center", fontstyle="italic")

    # Meadow label
    ax.text(50, 42, "Bara Bhangal", fontsize=10, color=DEODAR_DK,
            ha="center", fontstyle="italic")

    # Title
    ax.text(50, 95, "The Meadow", fontsize=14, color=INK, ha="center",
            fontweight="bold")
    ax.text(50, 91, "Three trails, three flocks, one grass", fontsize=9,
            color=INK_LIGHT, ha="center", fontstyle="italic")

    save(fig, "three-flocks.png")


# ════════════════════════════════════════════════════════════════════
# CHAPTER IV — The Fossilised Corridor
# ════════════════════════════════════════════════════════════════════

def fig_petroglyphs():
    """Fig 5: Rock terraces at Chilas — boulders covered in marks."""
    fig, ax = make_fig(bg=SLATE)

    rng = np.random.default_rng(401)

    # Rock face texture
    for _ in range(30):
        rx = rng.uniform(0, 100)
        ry = rng.uniform(0, 100)
        rw = rng.uniform(5, 15)
        rh = rng.uniform(3, 8)
        rect = mpatches.Rectangle((rx, ry), rw, rh,
                                   facecolor=ROCK_SURFACE, edgecolor=ROCK_DK,
                                   linewidth=0.3, alpha=rng.uniform(0.1, 0.25))
        ax.add_patch(rect)

    # Large boulder surfaces — three main rocks
    boulders = [(15, 25, 25, 35), (42, 15, 22, 45), (70, 20, 25, 40)]
    for bx, by, bw, bh in boulders:
        # Boulder outline
        b_xs = np.array([bx, bx + bw*0.2, bx + bw*0.5, bx + bw*0.8, bx + bw,
                         bx + bw, bx, bx])
        b_ys = np.array([by, by - 2, by - 3, by - 2, by,
                         by + bh, by + bh, by])
        ax.fill(jitter(b_xs, rng, 0.3), jitter(b_ys, rng, 0.3),
                color=ROCK_SURFACE, alpha=0.6)
        ax.plot(jitter(b_xs, rng, 0.2), jitter(b_ys, rng, 0.2),
                color=ROCK_DK, linewidth=1)

    # Ibex carvings — oldest layer, deepest
    def draw_ibex(ax, cx, cy, size, alpha=0.7):
        # Body
        body_x = np.array([cx, cx + size, cx + size*1.2, cx + size*0.8, cx - size*0.2])
        body_y = np.array([cy, cy + size*0.3, cy, cy - size*0.3, cy - size*0.1])
        ax.plot(jitter(body_x, rng, 0.1), jitter(body_y, rng, 0.1),
                color=CARVING, linewidth=1.2, alpha=alpha)
        # Horns — curved backward
        horn_x = np.array([cx + size*0.1, cx - size*0.3, cx - size*0.6])
        horn_y = np.array([cy + size*0.3, cy + size*0.6, cy + size*0.4])
        ax.plot(jitter(horn_x, rng, 0.1), jitter(horn_y, rng, 0.1),
                color=CARVING, linewidth=1, alpha=alpha)
        # Legs
        for lx in [cx + size*0.2, cx + size*0.6]:
            ax.plot([lx, lx], [cy - size*0.3, cy - size*0.7],
                    color=CARVING, linewidth=0.8, alpha=alpha)

    # Scatter ibex across boulders
    draw_ibex(ax, 18, 45, 4, alpha=0.5)
    draw_ibex(ax, 25, 38, 3, alpha=0.4)
    draw_ibex(ax, 48, 42, 5, alpha=0.6)
    draw_ibex(ax, 72, 45, 4, alpha=0.5)
    draw_ibex(ax, 80, 35, 3, alpha=0.4)

    # Stupa carvings — Buddhist layer
    def draw_stupa(ax, cx, cy, size):
        # Base platform
        ax.plot([cx - size, cx + size], [cy, cy], color=CHALK, linewidth=1, alpha=0.6)
        # Dome
        theta = np.linspace(0, np.pi, 20)
        dome_x = cx + size * 0.7 * np.cos(theta)
        dome_y = cy + size * 0.7 * np.sin(theta)
        ax.plot(dome_x, dome_y, color=CHALK, linewidth=1, alpha=0.6)
        # Spire
        ax.plot([cx, cx], [cy + size*0.7, cy + size*1.2],
                color=CHALK, linewidth=0.8, alpha=0.6)
        # Umbrella tiers
        for i in range(3):
            tier_y = cy + size * (0.8 + i * 0.15)
            tier_w = size * (0.3 - i * 0.08)
            ax.plot([cx - tier_w, cx + tier_w], [tier_y, tier_y],
                    color=CHALK, linewidth=0.6, alpha=0.5)

    draw_stupa(ax, 22, 30, 3)
    draw_stupa(ax, 50, 25, 4)
    draw_stupa(ax, 78, 28, 3)

    # Script marks — scattered text-like marks
    scripts = [
        (30, 55, "Kharoṣṭhī", CHALK_DIM),
        (55, 55, "Brāhmī", CHALK),
        (80, 55, "Sogdian", CHALK_DK),
    ]
    for sx, sy, label, col in scripts:
        # Squiggly marks suggesting script
        for i in range(4):
            mx = sx + i * 2 + rng.uniform(-0.5, 0.5)
            my = sy + rng.uniform(-1, 1)
            # Small script-like marks
            ax.plot([mx, mx + 1.5], [my, my + rng.uniform(-0.5, 0.5)],
                    color=col, linewidth=0.8, alpha=0.6)
            ax.plot([mx + 0.5, mx + 0.5], [my - 0.5, my + 0.5],
                    color=col, linewidth=0.6, alpha=0.5)
        ax.text(sx + 3, sy - 4, label, fontsize=7, color=col,
                ha="center", fontstyle="italic", alpha=0.7)

    # Title
    ax.text(50, 95, "The Rock Terraces", fontsize=14, color=CHALK, ha="center",
            fontweight="bold")
    ax.text(50, 91, "Ten thousand years of marks on stone", fontsize=9,
            color=CHALK_DIM, ha="center", fontstyle="italic")

    # River at bottom
    river_x = np.linspace(0, 100, 30)
    river_y = 8 + 2 * np.sin(river_x * 0.1) + rng.normal(0, 0.3, 30)
    ax.fill_between(river_x, river_y, 0, color=MELTWATER, alpha=0.2)
    ax.plot(river_x, river_y, color=MELTWATER, linewidth=1, alpha=0.5)
    ax.text(50, 3, "Indus", fontsize=9, color=MELTWATER, ha="center",
            fontstyle="italic", alpha=0.7)

    save(fig, "the-petroglyphs.png")


def fig_palimpsest():
    """Fig 6: The palimpsest — ibex beneath stupa beneath script."""
    fig, ax = make_fig(bg=ROCK_SURFACE)

    rng = np.random.default_rng(402)

    # Single rock face — close-up
    # Subtle texture
    for _ in range(50):
        rx = rng.uniform(0, 100)
        ry = rng.uniform(0, 100)
        ax.plot(rx, ry, ".", color=ROCK_DK, markersize=rng.uniform(1, 3),
                alpha=rng.uniform(0.05, 0.15))

    # Layer 1 (deepest): Large ibex — faded
    # Body
    ibex_body_x = np.array([25, 35, 45, 55, 65, 70, 65, 55, 45, 35, 25])
    ibex_body_y = np.array([40, 45, 48, 48, 45, 40, 35, 32, 32, 35, 40])
    ax.plot(jitter(ibex_body_x, rng, 0.3), jitter(ibex_body_y, rng, 0.3),
            color=CARVING_DK, linewidth=2, alpha=0.4)
    # Horns — large curved
    horn_x = np.array([28, 20, 15, 18, 25])
    horn_y = np.array([48, 55, 62, 68, 65])
    ax.plot(jitter(horn_x, rng, 0.3), jitter(horn_y, rng, 0.3),
            color=CARVING_DK, linewidth=2.5, alpha=0.35)
    horn2_x = np.array([25, 22, 23])
    horn2_y = np.array([65, 58, 52])
    ax.plot(jitter(horn2_x, rng, 0.2), jitter(horn2_y, rng, 0.2),
            color=CARVING_DK, linewidth=1.5, alpha=0.3)
    # Legs
    for lx, ly in [(35, 32), (55, 32), (40, 32), (60, 32)]:
        ax.plot([lx, lx + rng.uniform(-1, 1)], [ly, ly - 10],
                color=CARVING_DK, linewidth=1.5, alpha=0.35)
    # Beard
    ax.plot([65, 68, 66], [42, 38, 35], color=CARVING_DK,
            linewidth=1, alpha=0.3)

    # Layer 2 (middle): Stupa — carved on top of ibex
    # Dome overlapping ibex body
    theta = np.linspace(0, np.pi, 30)
    dome_x = 48 + 12 * np.cos(theta)
    dome_y = 40 + 12 * np.sin(theta)
    ax.plot(dome_x, dome_y, color=CARVING, linewidth=2, alpha=0.6)
    # Platform
    ax.plot([36, 60], [40, 40], color=CARVING, linewidth=1.5, alpha=0.6)
    ax.plot([38, 58], [38, 38], color=CARVING, linewidth=1, alpha=0.5)
    # Spire
    ax.plot([48, 48], [52, 62], color=CARVING, linewidth=1.5, alpha=0.6)
    # Umbrellas
    for uy in [54, 57, 60]:
        uw = 7 - (uy - 54)
        ax.plot([48 - uw, 48 + uw], [uy, uy], color=CARVING,
                linewidth=1, alpha=0.5)

    # Layer 3 (top): Sogdian script — squeezed into remaining space
    # Script marks around the edges
    for sx, sy in [(12, 70), (14, 66), (16, 62), (75, 65), (77, 60),
                    (79, 55), (10, 30), (12, 25), (75, 30), (77, 25)]:
        for i in range(3):
            mx = sx + i * 2
            my = sy + rng.uniform(-0.5, 0.5)
            ax.plot([mx, mx + 1.8], [my, my + rng.uniform(-0.8, 0.8)],
                    color=CHALK, linewidth=1, alpha=0.7)

    # Layer labels — timeline on right margin
    labels = [
        (92, 25, "~8,000 BCE\nibex", CARVING_DK, 0.5),
        (92, 45, "1st–7th c.\nstūpa", CARVING, 0.7),
        (92, 65, "3rd–7th c.\nSogdian", CHALK, 0.8),
    ]
    for lx, ly, text, col, alpha in labels:
        ax.text(lx, ly, text, fontsize=7, color=col, ha="center",
                fontstyle="italic", alpha=alpha)
        ax.plot([86, 88], [ly, ly], color=col, linewidth=0.8, alpha=alpha)

    # "Horns through the halo" annotation
    ax.annotate("horns through\nthe halo", xy=(22, 60), xytext=(8, 78),
                fontsize=7, color=CHALK_DIM, fontstyle="italic",
                arrowprops=dict(arrowstyle="->", color=CHALK_DIM, lw=0.8))

    # Title
    ax.text(50, 95, "The Palimpsest", fontsize=14, color=CHALK, ha="center",
            fontweight="bold")
    ax.text(50, 91, "Ibex first, stūpa beside, Sogdian on top", fontsize=9,
            color=CHALK_DIM, ha="center", fontstyle="italic")

    save(fig, "the-palimpsest.png")


# ════════════════════════════════════════════════════════════════════
# CHAPTER V — The Mountain That Cannot Be Seen Whole
# ════════════════════════════════════════════════════════════════════

def fig_three_faces():
    """Fig 7: Three faces of Nanga Parbat — three sightlines."""
    fig, ax = make_fig(bg="#D0D8E0")  # high-altitude grey-blue sky

    rng = np.random.default_rng(501)

    # Central peak — massive, dominating
    peak_x = np.array([20, 30, 38, 45, 50, 55, 62, 70, 80])
    peak_y = np.array([30, 45, 58, 72, 85, 72, 58, 45, 30])
    ax.fill(peak_x, peak_y, color=GNEISS_GREY, alpha=0.4)
    ax.plot(jitter(peak_x, rng, 0.3), jitter(peak_y, rng, 0.4),
            color=GNEISS_DK, linewidth=2)

    # Snow on upper portion
    snow_x = np.array([35, 40, 45, 50, 55, 60, 65])
    snow_y = np.array([55, 65, 75, 85, 75, 65, 55])
    ax.fill(snow_x, snow_y, color=SNOW_WHITE, alpha=0.6)

    # Three face labels with sightline arrows
    faces = [
        (12, 25, "Rakhiot\n(north)", "→ ice", GLACIER_BLUE, (20, 35)),
        (88, 25, "Rupal\n(south)", "→ time", HYDROTHERMAL, (80, 35)),
        (15, 55, "Diamir\n(west)", "→ rock", GNEISS_DK, (25, 55)),
    ]
    for lx, ly, name, reading, col, arrow_to in faces:
        ax.text(lx, ly, name, fontsize=9, color=col, ha="center",
                fontweight="bold")
        ax.text(lx, ly - 5, reading, fontsize=7, color=col, ha="center",
                fontstyle="italic")
        ax.annotate("", xy=arrow_to, xytext=(lx, ly + 2),
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.2,
                                    linestyle="dashed"))

    # Glaciers
    # Rakhiot glacier (north, left)
    gl_x = np.array([22, 25, 30, 35, 38])
    gl_y = np.array([20, 25, 28, 30, 33])
    ax.fill_between(gl_x, gl_y, gl_y - 3, color=GLACIER_BLUE, alpha=0.3)
    ax.plot(gl_x, gl_y, color=GLACIER_DK, linewidth=1)

    # Rupal face shading (south, right) — vertical striations
    for i in range(8):
        sx = 62 + i * 2.5
        sy_top = 55 - i * 2
        sy_bot = 30
        ax.plot([sx, sx + rng.uniform(-0.5, 0.5)], [sy_top, sy_bot],
                color=GNEISS_DK, linewidth=0.5, alpha=0.3)

    # Summit marker
    ax.plot(50, 85, "*", color=SNOW_WHITE, markersize=10)
    ax.text(50, 88, "8,126 m", fontsize=8, color=GNEISS_DK, ha="center",
            fontstyle="italic")

    # "No point on earth..." text
    ax.text(50, 8, "No point on earth from which all three are visible at once",
            fontsize=9, color=GNEISS_DK, ha="center", fontstyle="italic")

    # Valley floor
    ax.fill_between([0, 100], [0, 0], [18, 18], color=MUD_BROWN, alpha=0.1)

    # Title
    ax.text(50, 95, "The Three Faces", fontsize=14, color=GNEISS_DK,
            ha="center", fontweight="bold")

    save(fig, "three-faces.png")


def fig_gorge():
    """Fig 8: The Indus gorge — seven thousand metres of relief."""
    fig, ax = make_fig(bg=SLATE)

    rng = np.random.default_rng(502)

    # Left gorge wall
    left_x = np.array([0, 5, 10, 15, 20, 25, 30, 35, 38, 40])
    left_y = np.array([95, 90, 82, 70, 60, 50, 42, 35, 25, 15])
    ax.fill_betweenx(left_y, 0, left_x, color=GNEISS_GREY, alpha=0.4)
    ax.plot(left_x, left_y, color=GNEISS_DK, linewidth=2)

    # Right gorge wall
    right_x = np.array([100, 95, 90, 85, 80, 75, 70, 65, 62, 60])
    right_y = np.array([95, 88, 78, 65, 55, 45, 38, 30, 20, 10])
    ax.fill_betweenx(right_y, 100, right_x, color=GNEISS_GREY, alpha=0.4)
    ax.plot(right_x, right_y, color=GNEISS_DK, linewidth=2)

    # Rock striations on walls
    for _ in range(20):
        wx = rng.uniform(5, 35)
        wy = rng.uniform(20, 90)
        ax.plot([wx, wx + rng.uniform(1, 5)],
                [wy, wy + rng.uniform(-2, 2)],
                color=ROCK_DK, linewidth=0.5, alpha=0.3)
    for _ in range(20):
        wx = rng.uniform(65, 95)
        wy = rng.uniform(15, 85)
        ax.plot([wx, wx + rng.uniform(1, 5)],
                [wy, wy + rng.uniform(-2, 2)],
                color=ROCK_DK, linewidth=0.5, alpha=0.3)

    # River at bottom
    river_x = np.linspace(40, 60, 20)
    river_y = 8 + 3 * np.sin(river_x * 0.2) + rng.normal(0, 0.3, 20)
    ax.fill_between(river_x, river_y, 3, color=MELTWATER, alpha=0.4)
    ax.plot(river_x, river_y, color=MELTWATER, linewidth=1.5, alpha=0.7)

    # Elevation markers on left wall
    elevations = [
        (8, 85, "8,126 m — summit"),
        (18, 60, "3,300 m — Fairy Meadows"),
        (38, 15, "1,100 m — Indus"),
    ]
    for ex, ey, label in elevations:
        ax.text(ex, ey, label, fontsize=7, color=CHALK_DIM, ha="left",
                fontstyle="italic")
        ax.plot([ex + 15, 40], [ey, ey], color=CHALK_DIM, linewidth=0.5,
                linestyle=":", alpha=0.5)

    # Snow caps at top
    for cx in [15, 50, 85]:
        ax.plot([cx - 5, cx, cx + 5], [95, 98, 95], color=SNOW_WHITE,
                linewidth=2, alpha=0.6)

    # "7,000 m" vertical arrow
    ax.annotate("", xy=(50, 85), xytext=(50, 12),
                arrowprops=dict(arrowstyle="<->", color=CHALK, lw=1.5))
    ax.text(52, 48, "7,000 m\nrelief", fontsize=9, color=CHALK,
            fontstyle="italic")

    # Title
    ax.text(50, 3, "The Indus", fontsize=10, color=MELTWATER, ha="center",
            fontstyle="italic")

    save(fig, "the-gorge.png")


# ════════════════════════════════════════════════════════════════════
# CHAPTER VI — The Language the Spirit Brings
# ════════════════════════════════════════════════════════════════════

def fig_three_languages():
    """Fig 9: Three languages, no common ancestor — three scripts."""
    fig, ax = make_fig(bg=PARCHMENT_DK)

    rng = np.random.default_rng(601)

    # Three panels suggesting different scripts
    # Each panel is a "wall section" — market wall in Karimabad
    wall_y_base = 25
    wall_height = 50
    panel_width = 28

    # Wall texture
    wall = mpatches.Rectangle((5, wall_y_base), 90, wall_height,
                               facecolor=MINERAL_LIGHT, edgecolor=INK_FAINT,
                               linewidth=1)
    ax.add_patch(wall)

    # Panel dividers
    for dx in [35, 65]:
        ax.plot([dx, dx], [wall_y_base, wall_y_base + wall_height],
                color=INK_FAINT, linewidth=0.8, linestyle="--")

    # Panel 1: Burushaski (isolate) — invented script-like marks
    # (Burushaski has no traditional script; written in modified Arabic/Latin)
    bx, by = 12, 45
    ax.text(20, 70, "Burushaski", fontsize=10, color=BURUSHASKI_INK,
            ha="center", fontweight="bold")
    ax.text(20, 65, "(isolate)", fontsize=7, color=BURUSHASKI_INK,
            ha="center", fontstyle="italic")
    # Script-like marks — angular, unique
    for i in range(5):
        for j in range(3):
            mx = bx + i * 4 + rng.uniform(-0.3, 0.3)
            my = by + j * 5 + rng.uniform(-0.3, 0.3)
            # Angular marks suggesting unfamiliar script
            pts = rng.uniform(-1.5, 1.5, (4, 2))
            pts[:, 0] += mx
            pts[:, 1] += my
            ax.plot(pts[:, 0], pts[:, 1], color=BURUSHASKI_INK,
                    linewidth=1.2, alpha=0.7)

    # Panel 2: Shina (Indo-Aryan) — Devanagari-like marks
    sx_base, sy_base = 42, 45
    ax.text(50, 70, "Shina", fontsize=10, color=SHINA_INK,
            ha="center", fontweight="bold")
    ax.text(50, 65, "(Indo-Aryan)", fontsize=7, color=SHINA_INK,
            ha="center", fontstyle="italic")
    # Devanagari headline + hanging characters
    for i in range(5):
        mx = sx_base + i * 4
        # Headline bar
        ax.plot([mx, mx + 3], [sy_base + 12, sy_base + 12],
                color=SHINA_INK, linewidth=1.5, alpha=0.7)
        # Vertical stems
        ax.plot([mx + 1.5, mx + 1.5], [sy_base + 12, sy_base + 7],
                color=SHINA_INK, linewidth=1, alpha=0.6)
        # Curves suggesting characters
        curve_x = np.array([mx + 0.5, mx + 1.5, mx + 2.5])
        curve_y = np.array([sy_base + 8, sy_base + 6, sy_base + 8])
        ax.plot(curve_x, curve_y, color=SHINA_INK, linewidth=0.8, alpha=0.6)
    # Second line
    for i in range(5):
        mx = sx_base + i * 4
        ax.plot([mx, mx + 3], [sy_base + 2, sy_base + 2],
                color=SHINA_INK, linewidth=1.5, alpha=0.6)
        ax.plot([mx + 1, mx + 1], [sy_base + 2, sy_base - 2],
                color=SHINA_INK, linewidth=0.8, alpha=0.5)

    # Panel 3: Wakhi (Iranian) — Arabic-like marks
    wx_base, wy_base = 72, 45
    ax.text(80, 70, "Wakhi", fontsize=10, color=WAKHI_INK,
            ha="center", fontweight="bold")
    ax.text(80, 65, "(Iranian)", fontsize=7, color=WAKHI_INK,
            ha="center", fontstyle="italic")
    # Arabic-like flowing script (right-to-left suggestion)
    for j in range(3):
        baseline = wy_base + j * 5
        # Flowing connected line
        flow_x = np.linspace(wx_base + 18, wx_base, 20)
        flow_y = baseline + 1.5 * np.sin(flow_x * 0.5) + rng.normal(0, 0.2, 20)
        ax.plot(flow_x, flow_y, color=WAKHI_INK, linewidth=1, alpha=0.6)
        # Dots above/below
        for _ in range(3):
            dx = rng.uniform(wx_base, wx_base + 18)
            dy = baseline + rng.choice([-2, 2]) + rng.uniform(-0.3, 0.3)
            ax.plot(dx, dy, ".", color=WAKHI_INK, markersize=3, alpha=0.5)

    # Annotation below wall
    ax.text(50, 18, "No common ancestor", fontsize=11, color=INK,
            ha="center", fontstyle="italic")

    # Three family tree stubs — disconnected
    for cx, label in [(20, "?"), (50, "Indo-European"), (80, "Indo-European")]:
        ax.plot([cx, cx], [12, 15], color=INK_LIGHT, linewidth=0.8)
        if cx == 20:
            ax.text(cx, 10, "no known\nfamily", fontsize=6, color=BURUSHASKI_INK,
                    ha="center", fontstyle="italic")
        elif cx == 50:
            ax.text(cx, 10, "Indo-Aryan\nbranch", fontsize=6, color=SHINA_INK,
                    ha="center", fontstyle="italic")
        else:
            ax.text(cx, 10, "Iranian\nbranch", fontsize=6, color=WAKHI_INK,
                    ha="center", fontstyle="italic")

    # Mountain backdrop
    for cx, cy, w, h in [(15, 82, 20, 12), (50, 85, 18, 10), (85, 80, 22, 14)]:
        draw_peak(ax, cx, cy, w, h, INK_FAINT, rng=rng, fill=INK_FAINT)

    # Title
    ax.text(50, 95, "Three Languages", fontsize=14, color=INK, ha="center",
            fontweight="bold")

    save(fig, "three-languages.png")


def fig_bitan():
    """Fig 10: The bitan in trance — juniper smoke, drum, passage."""
    fig, ax = make_fig(bg=SLATE)

    rng = np.random.default_rng(602)

    # Subtle texture
    for _ in range(40):
        rx = rng.uniform(0, 100)
        ry = rng.uniform(0, 100)
        ax.plot(rx, ry, ".", color=SLATE_LT, markersize=rng.uniform(1, 2),
                alpha=rng.uniform(0.1, 0.2))

    # Central figure — the bitan, suggested rather than drawn
    # Vertical form
    body_x = np.array([48, 47, 46, 47, 50, 53, 54, 53, 52])
    body_y = np.array([25, 35, 45, 55, 65, 55, 45, 35, 25])
    ax.plot(jitter(body_x, rng, 0.3), jitter(body_y, rng, 0.4),
            color=CHALK, linewidth=2, alpha=0.7)

    # Head
    theta = np.linspace(0, 2 * np.pi, 20)
    head_x = 50 + 3 * np.cos(theta)
    head_y = 68 + 3 * np.sin(theta)
    ax.plot(head_x, head_y, color=CHALK, linewidth=1.5, alpha=0.7)

    # Iron bangle — the kau
    kau_x = 42 + 2 * np.cos(theta)
    kau_y = 50 + 1.5 * np.sin(theta)
    ax.plot(kau_x, kau_y, color=HYDROTHERMAL, linewidth=2, alpha=0.8)
    ax.text(36, 50, "kau", fontsize=7, color=HYDROTHERMAL, ha="center",
            fontstyle="italic")

    # Arms raised
    ax.plot([47, 38, 32], [55, 62, 68], color=CHALK, linewidth=1.5, alpha=0.6)
    ax.plot([53, 62, 68], [55, 62, 68], color=CHALK, linewidth=1.5, alpha=0.6)

    # Juniper smoke — rising wisps from left
    for i in range(6):
        smoke_x = 25 + i * 1.5 + 8 * np.sin(np.linspace(0, 3, 20) + i)
        smoke_y = np.linspace(20 + i * 5, 50 + i * 8, 20)
        ax.plot(smoke_x, smoke_y, color=JUNIPER_GREY, linewidth=0.8,
                alpha=0.3 - i * 0.03)

    # Juniper branch at base
    ax.plot([22, 25, 28], [20, 22, 20], color=JUNIPER_GREY, linewidth=1.5,
            alpha=0.6)
    ax.text(25, 16, "juniper", fontsize=7, color=JUNIPER_GREY, ha="center",
            fontstyle="italic", alpha=0.7)

    # Drum on right — dadang
    drum_x = 72 + 5 * np.cos(theta)
    drum_y = 40 + 3 * np.sin(theta)
    ax.plot(drum_x, drum_y, color=COPPER, linewidth=1.5, alpha=0.7)
    # Drum sticks
    ax.plot([72, 68], [43, 50], color=COPPER, linewidth=1, alpha=0.6)
    ax.plot([72, 76], [43, 50], color=COPPER, linewidth=1, alpha=0.6)
    ax.text(72, 34, "dadang", fontsize=7, color=COPPER, ha="center",
            fontstyle="italic", alpha=0.7)

    # Sound waves from drum
    for r in range(3):
        wave_x = 72 + (8 + r * 4) * np.cos(np.linspace(-0.5, 0.5, 10))
        wave_y = 40 + (5 + r * 3) * np.sin(np.linspace(-0.5, 0.5, 10))
        ax.plot(wave_x, wave_y, color=COPPER, linewidth=0.5,
                alpha=0.4 - r * 0.1)

    # The two languages — emerging from the figure
    # Burushaski (waking) — below, grounded
    ax.text(50, 15, "Burushaski", fontsize=10, color=BURUSHASKI_INK,
            ha="center", fontstyle="italic", alpha=0.6)
    ax.text(50, 11, "(the waking tongue)", fontsize=7, color=BURUSHASKI_INK,
            ha="center", alpha=0.5)

    # Shina (trance) — above, floating
    ax.text(50, 82, "S h i n a", fontsize=14, color=CHALK,
            ha="center", fontweight="bold", alpha=0.8,
            fontfamily="serif")
    ax.text(50, 77, "(the spirit's tongue)", fontsize=8, color=CHALK_DIM,
            ha="center", fontstyle="italic")

    # Passage arrows — Burushaski → body → Shina
    ax.annotate("", xy=(50, 22), xytext=(50, 18),
                arrowprops=dict(arrowstyle="->", color=BURUSHASKI_INK,
                                lw=1, linestyle="dashed"))
    ax.annotate("", xy=(50, 75), xytext=(50, 72),
                arrowprops=dict(arrowstyle="->", color=CHALK,
                                lw=1, linestyle="dashed"))

    # Title
    ax.text(50, 95, "The Bitan", fontsize=14, color=CHALK, ha="center",
            fontweight="bold")
    ax.text(50, 91, "The spirit brings its own language", fontsize=9,
            color=CHALK_DIM, ha="center", fontstyle="italic")

    save(fig, "the-bitan.png")


# ════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Generating illustrations for '{SLUG}'...")
    print(f"Output: {OUT}\n")

    # Chapter I
    print("Chapter I — The Rain Wall")
    fig_rain_wall()
    fig_three_climates()

    # Chapter II
    print("\nChapter II — The Statue with Two Names")
    fig_two_processions()

    # Chapter III
    print("\nChapter III — The Meadow Where Three Flocks Arrive")
    fig_three_flocks()

    # Chapter IV
    print("\nChapter IV — The Fossilised Corridor")
    fig_petroglyphs()
    fig_palimpsest()

    # Chapter V
    print("\nChapter V — The Mountain That Cannot Be Seen Whole")
    fig_three_faces()
    fig_gorge()

    # Chapter VI
    print("\nChapter VI — The Language the Spirit Brings")
    fig_three_languages()
    fig_bitan()

    print(f"\nDone — {len(list(OUT.glob('*.png')))} images in {OUT}")
