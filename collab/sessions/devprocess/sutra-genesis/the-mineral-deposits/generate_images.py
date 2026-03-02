# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Mineral Deposits".

A story about a spirit at Tattapani who reads mineral deposits in the
dam wall that match its own chemistry — the handwriting is familiar,
the hand is not. Agent generations as geological strata.

Visual language: diagrammatic, ink-and-wash, warm parchment tones.
Mineral palette — iron oxide reds, manganese darks, sulphur yellows,
reservoir blues — layered over the standard parchment/walnut base.

Run with:  uv run generate_images.py
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

# ── Output ──────────────────────────────────────────────────────────
OUT = Path(__file__).parent / "../../../../../website/static/images/writing/the-mineral-deposits"
OUT = OUT.resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9  # inches — 1800×1350 px at 150 DPI

# ── Palette ─────────────────────────────────────────────────────────
# Tattapani palette: mineral, thermal, reservoir
PARCHMENT     = "#F5F0E8"
PARCHMENT_DK  = "#EDE6D8"
INK           = "#5C4A3A"
INK_LIGHT     = "#8B7B6B"
INK_FAINT     = "#C4B8A8"

# Walnut ink
WALNUT        = "#4A3728"
WALNUT_LIGHT  = "#6B5040"
WALNUT_FAINT  = "#A08B70"

# Mineral deposits
MANGANESE     = "#3A2520"    # dark, first-layer
IRON_OXIDE    = "#8B3A1A"    # rust red banding
CALCIUM       = "#E8DCC8"    # pale carbonate
SILICA        = "#D8D0C0"    # translucent white
SULPHUR       = "#C4A830"    # yellow thermal
SULPHUR_PALE  = "#E0D080"

# Reservoir water
RESERVOIR     = "#5A7888"
RESERVOIR_LT  = "#8AAAB8"
RESERVOIR_DK  = "#3A5868"
RESERVOIR_DEEP= "#1A3040"

# Thermal / hot spring
THERMAL       = "#C85828"
THERMAL_GLOW  = "#E88848"
STEAM         = "#E8E0D8"

# Stone / dam
STONE_GREY    = "#9A9485"
STONE_DARK    = "#6B6660"
CONCRETE      = "#A8A098"
CONCRETE_DK   = "#787068"

# Mountain
MOUNTAIN      = "#7A7068"
MOUNTAIN_DK   = "#5A5248"
SNOW          = "#E8EEF0"

# Sky
SKY_WARM      = "#D8C8B0"
SKY_BLUE      = "#B0C8D8"

# Thread (gold)
THREAD_GOLD   = "#D4A830"


# ── Shared helpers ──────────────────────────────────────────────────

def make_fig(width=W, height=H, bg=PARCHMENT):
    fig, ax = plt.subplots(1, 1, figsize=(width, height), facecolor=bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def add_parchment_texture(ax, seed=42):
    rng = np.random.default_rng(seed)
    for _ in range(8):
        cx, cy = rng.uniform(10, 90), rng.uniform(10, 90)
        r = rng.uniform(5, 15)
        circle = plt.Circle((cx, cy), r, color=PARCHMENT_DK,
                             alpha=rng.uniform(0.15, 0.35), zorder=0)
        ax.add_patch(circle)


def title_block(ax, title, subtitle="", y=95):
    ax.text(50, y, title, ha="center", va="top",
            fontsize=18, fontweight="bold", color=INK,
            fontfamily="serif")
    if subtitle:
        ax.text(50, y - 4, subtitle, ha="center", va="top",
                fontsize=11, fontstyle="italic", color=INK_LIGHT,
                fontfamily="serif")


def attribution(ax, text="The Mineral Deposits \u2014 A Human-Machine Collaboration",
                y=2):
    ax.text(50, y, text, ha="center", va="bottom",
            fontsize=8, fontstyle="italic", color=INK_LIGHT,
            fontfamily="serif")


def draw_mountain_ridge(ax, x_start, x_end, y_base, height, n_peaks=5,
                        color=MOUNTAIN, seed=None):
    rng = np.random.default_rng(seed)
    xs = np.linspace(x_start, x_end, n_peaks * 10 + 1)
    ys = np.zeros_like(xs) + y_base
    for i in range(n_peaks):
        cx = x_start + (i + 0.5) * (x_end - x_start) / n_peaks
        cx += rng.uniform(-2, 2)
        h = height * rng.uniform(0.6, 1.0)
        w = (x_end - x_start) / n_peaks * 0.8
        ys += h * np.exp(-((xs - cx) / w) ** 2)
    snow_line = y_base + height * 0.7
    ax.fill_between(xs, y_base, ys, color=color, alpha=0.5, zorder=1)
    snow_xs = xs[ys > snow_line]
    snow_ys = ys[ys > snow_line]
    if len(snow_xs) > 0:
        ax.fill_between(snow_xs, snow_line, snow_ys,
                         color=SNOW, alpha=0.4, zorder=2)
    ax.plot(xs, ys, color=MOUNTAIN_DK, linewidth=0.8, zorder=2)
    return xs, ys


def draw_mineral_layer(ax, x_start, x_end, y, thickness, color,
                       alpha=0.8, wobble_seed=None):
    """Draw a single mineral deposit layer with slight irregularity."""
    rng = np.random.default_rng(wobble_seed)
    xs = np.linspace(x_start, x_end, 80)
    top = y + thickness + rng.uniform(-thickness * 0.15, thickness * 0.15, 80)
    bot = np.full_like(xs, y)
    ax.fill_between(xs, bot, top, color=color, alpha=alpha, zorder=3)
    ax.plot(xs, top, color=INK, linewidth=0.3, alpha=0.4, zorder=4)


# ═══════════════════════════════════════════════════════════════════
# Figure 1: Sutlej reservoir — surface, dam wall, springs below
# ═══════════════════════════════════════════════════════════════════

def sutlej_reservoir():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=101)
    rng = np.random.default_rng(42)

    title_block(ax, "The Sutlej Above Tattapani",
                "Reservoir surface \u2014 dam wall to the south \u2014 springs below")

    # ── Sky ──
    for i in range(15):
        gy = 70 + i * 2
        ax.axhspan(gy, gy + 2, color=SKY_WARM, alpha=0.03 + 0.015 * i, zorder=0)

    # ── Mountains (background) ──
    draw_mountain_ridge(ax, 0, 100, 60, 25, n_peaks=6, color=MOUNTAIN, seed=10)
    draw_mountain_ridge(ax, 0, 100, 55, 20, n_peaks=4, color=MOUNTAIN_DK, seed=20)

    # ── Dam wall (right side) ──
    dam_x = 75
    dam_top = 55
    dam_bot = 15
    dam_w = 8
    # Concrete face
    ax.add_patch(FancyBboxPatch(
        (dam_x, dam_bot), dam_w, dam_top - dam_bot,
        boxstyle="round,pad=0.2",
        facecolor=CONCRETE, edgecolor=CONCRETE_DK,
        linewidth=2.0, alpha=0.85, zorder=5))
    # Horizontal construction lines
    for dy in np.linspace(dam_bot + 2, dam_top - 2, 8):
        ax.plot([dam_x + 0.5, dam_x + dam_w - 0.5], [dy, dy],
                color=CONCRETE_DK, linewidth=0.4, alpha=0.5, zorder=6)
    ax.text(dam_x + dam_w / 2, dam_bot - 2, "Kol Dam",
            fontsize=8, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # ── Reservoir surface ──
    water_y = 52
    water_xs = np.linspace(0, dam_x + 1, 200)
    # Subtle ripples
    water_top = water_y + 0.3 * np.sin(water_xs * 0.5) + rng.uniform(-0.1, 0.1, 200)
    ax.fill_between(water_xs, 15, water_top,
                     color=RESERVOIR, alpha=0.35, zorder=3)
    ax.fill_between(water_xs, water_y - 3, water_top,
                     color=RESERVOIR_LT, alpha=0.25, zorder=4)
    # Surface glare
    for _ in range(15):
        gx = rng.uniform(10, 70)
        ax.plot([gx, gx + rng.uniform(2, 5)],
                [water_y + rng.uniform(-0.5, 0.5)] * 2,
                color=PARCHMENT, linewidth=0.8, alpha=0.3, zorder=5)

    # ── Depth gradient below surface ──
    for i in range(15):
        dy = water_y - 3 - i * 2.5
        alpha = 0.05 + 0.02 * i
        ax.axhspan(dy, dy + 2.5, xmin=0, xmax=dam_x / 100,
                    color=RESERVOIR_DEEP, alpha=alpha, zorder=3)

    # ── Hot springs at depth (glow from below) ──
    spring_x, spring_y = 35, 18
    for r, a in [(8, 0.04), (5, 0.08), (3, 0.12), (1.5, 0.2)]:
        ax.add_patch(Circle((spring_x, spring_y), r,
                             color=THERMAL_GLOW, alpha=a, zorder=3))
    # Rising thermal plume (faint)
    for i in range(12):
        py = spring_y + i * 2.5
        pw = 2 - i * 0.12
        if pw > 0:
            ax.add_patch(mpatches.Ellipse(
                (spring_x + rng.uniform(-0.5, 0.5), py),
                pw, 1.5, color=THERMAL_GLOW,
                alpha=0.03 * (12 - i), zorder=3))
    ax.text(spring_x, spring_y - 3,
            "the springs\n(still flowing, 130m below)",
            fontsize=7, color=THERMAL, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # ── Depth annotation ──
    ax.annotate("", xy=(dam_x + dam_w + 3, water_y),
                xytext=(dam_x + dam_w + 3, spring_y),
                arrowprops=dict(arrowstyle="<->", color=INK_LIGHT,
                                linewidth=0.8))
    ax.text(dam_x + dam_w + 5, (water_y + spring_y) / 2,
            "130m", fontsize=9, color=INK,
            fontfamily="serif", ha="left", va="center", zorder=7)

    # ── Location text ──
    ax.text(10, 8, "Tattapani \u2014 the hot water\n"
            "Sutlej valley between Shimla and Rampur\n"
            "Springs drowned by Kol Dam reservoir, 2015",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", zorder=7)

    attribution(ax, y=3)
    fig.savefig(OUT / "sutlej-reservoir.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 sutlej-reservoir.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 2: Deposit layers — cross-section on dam wall
# ═══════════════════════════════════════════════════════════════════

def deposit_layers():
    fig, ax = make_fig(width=10, height=12)
    ax.set_ylim(0, 120)
    add_parchment_texture(ax, seed=201)
    rng = np.random.default_rng(55)

    title_block(ax, "The Deposit on the Dam Wall",
                "37 layers \u2014 37 seasons \u2014 twelve metres below the waterline", y=117)

    # ── Rock face background ──
    ax.add_patch(FancyBboxPatch(
        (15, 8), 70, 95, boxstyle="round,pad=0.5",
        facecolor=STONE_GREY, edgecolor=STONE_DARK,
        linewidth=1.5, alpha=0.3, zorder=1))

    # ── Mineral deposit layers ──
    # 37 layers, with 7-season periodicity
    # Scale to fill the rock face (y=12 to y=98)
    y_cursor = 12
    layer_colors = []
    for i in range(37):
        cycle_pos = i % 7
        # Manganese-dark at cycle start, calcium-pale in middle
        if cycle_pos == 0:
            color = MANGANESE
            thickness = 1.6
        elif cycle_pos in (1, 6):
            color = IRON_OXIDE
            thickness = 2.0
        elif cycle_pos in (2, 5):
            # Iron-calcium transition
            r = 0.5 + 0.1 * rng.random()
            color = WALNUT_LIGHT
            thickness = 2.2
        else:
            color = CALCIUM
            thickness = 2.6
        layer_colors.append(color)

        # Draw layer
        alpha = 0.7 + 0.15 * rng.random()
        draw_mineral_layer(ax, 20, 80, y_cursor, thickness, color,
                          alpha=alpha, wobble_seed=100 + i)
        y_cursor += thickness + 0.15

    # ── Labels for periodicity ──
    # Mark every 7th layer (manganese returns)
    label_x = 83
    y_cursor_label = 12
    cycle_count = 0
    for i in range(37):
        cycle_pos = i % 7
        thickness = 1.6 if cycle_pos == 0 else (2.0 if cycle_pos in (1, 6) else (2.2 if cycle_pos in (2, 5) else 2.6))
        if cycle_pos == 0:
            cycle_count += 1
            ax.plot([81, label_x - 1], [y_cursor_label + thickness / 2] * 2,
                    color=MANGANESE, linewidth=0.6, alpha=0.6, zorder=5)
            ax.text(label_x, y_cursor_label + thickness / 2,
                    f"cycle {cycle_count}", fontsize=6, color=INK_LIGHT,
                    fontfamily="serif", va="center", zorder=5)
        y_cursor_label += thickness + 0.15

    # ── Annotation ──
    ax.text(50, 108, "Each layer a mineral ratio from the same source",
            fontsize=9, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # ── Legend ──
    legend_y = 7
    for label, color in [("manganese (cycle start)", MANGANESE),
                         ("iron oxide", IRON_OXIDE),
                         ("transition", WALNUT_LIGHT),
                         ("calcium carbonate", CALCIUM)]:
        ax.add_patch(FancyBboxPatch(
            (20, legend_y - 0.8), 3, 1.6, boxstyle="round,pad=0.1",
            facecolor=color, edgecolor=INK_FAINT,
            linewidth=0.5, alpha=0.8, zorder=5))
        ax.text(25, legend_y, label, fontsize=7, color=INK,
                fontfamily="serif", va="center", zorder=5)
        legend_y -= 3

    attribution(ax, y=2)
    fig.savefig(OUT / "deposit-layers.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 deposit-layers.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 3: Seven-layer cycle — oscillation pattern
# ═══════════════════════════════════════════════════════════════════

def seven_layer_cycle():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=301)
    rng = np.random.default_rng(77)

    title_block(ax, "The Seven-Layer Cycle",
                "The drift is the speaking \u2014 the return is the breath")

    # ── Oscillation plot ──
    # Show 5 complete cycles (35 layers) as a waveform
    n_layers = 35
    xs = np.arange(n_layers)
    # Mineral ratio: 0 = manganese-dark, 1 = calcium-pale
    ratios = np.array([
        0.0, 0.3, 0.6, 0.9, 0.85, 0.5, 0.15,  # cycle 1
        0.0, 0.35, 0.65, 0.92, 0.82, 0.45, 0.12,  # cycle 2
        0.0, 0.28, 0.58, 0.88, 0.87, 0.52, 0.18,  # cycle 3
        0.0, 0.32, 0.62, 0.91, 0.83, 0.48, 0.14,  # cycle 4
        0.0, 0.30, 0.60, 0.90, 0.84, 0.50, 0.16,  # cycle 5
    ])

    # Map to plot coordinates
    plot_x_start, plot_x_end = 12, 88
    plot_y_start, plot_y_end = 18, 70
    plot_xs = plot_x_start + (plot_x_end - plot_x_start) * xs / (n_layers - 1)
    plot_ys = plot_y_start + (plot_y_end - plot_y_start) * ratios

    # ── Background bands for each cycle ──
    cycle_colors = [PARCHMENT_DK, PARCHMENT]
    for c in range(5):
        x_left = plot_x_start + (plot_x_end - plot_x_start) * (c * 7) / (n_layers - 1)
        x_right = plot_x_start + (plot_x_end - plot_x_start) * ((c + 1) * 7 - 1) / (n_layers - 1)
        ax.axvspan(x_left, x_right, ymin=0.15, ymax=0.75,
                   color=cycle_colors[c % 2], alpha=0.3, zorder=1)

    # ── Draw the waveform ──
    # Color-coded line: dark where manganese, warm where calcium
    for i in range(len(plot_xs) - 1):
        ratio = (ratios[i] + ratios[i + 1]) / 2
        # Interpolate color from manganese to calcium
        r1, g1, b1 = int(MANGANESE[1:3], 16), int(MANGANESE[3:5], 16), int(MANGANESE[5:7], 16)
        r2, g2, b2 = int(CALCIUM[1:3], 16), int(CALCIUM[3:5], 16), int(CALCIUM[5:7], 16)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        color = f"#{r:02x}{g:02x}{b:02x}"
        ax.plot([plot_xs[i], plot_xs[i + 1]], [plot_ys[i], plot_ys[i + 1]],
                color=color, linewidth=2.5, zorder=4)

    # ── Cycle start markers (manganese returns) ──
    for c in range(5):
        idx = c * 7
        ax.plot(plot_xs[idx], plot_ys[idx], "o", color=MANGANESE,
                markersize=6, markeredgecolor=INK, markeredgewidth=0.8, zorder=5)
        ax.text(plot_xs[idx], plot_ys[idx] - 4, f"return\n{c+1}",
                fontsize=6, color=INK_LIGHT, fontfamily="serif",
                fontstyle="italic", ha="center", zorder=5)

    # ── Axis labels ──
    ax.text(92, plot_y_end + 2, "calcium-pale\n(middle of\nutterance)",
            fontsize=7, color=WALNUT_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)
    ax.text(92, plot_y_start - 2, "manganese-dark\n(breath\nbetween)",
            fontsize=7, color=MANGANESE, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # ── Vertical axis line ──
    ax.plot([plot_x_start - 1, plot_x_start - 1],
            [plot_y_start - 2, plot_y_end + 2],
            color=INK_LIGHT, linewidth=0.8, zorder=3)
    ax.text(plot_x_start - 3, (plot_y_start + plot_y_end) / 2,
            "mineral\nratio", fontsize=8, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic",
            ha="center", va="center", rotation=90, zorder=5)

    # ── Horizontal axis ──
    ax.plot([plot_x_start - 1, plot_x_end + 1],
            [plot_y_start - 2, plot_y_start - 2],
            color=INK_LIGHT, linewidth=0.8, zorder=3)
    ax.text(50, plot_y_start - 12, "layer number \u2192 time",
            fontsize=9, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # ── Key insight ──
    ax.text(50, 85, "Each cycle is a complete utterance.",
            fontsize=13, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    attribution(ax, y=3)
    fig.savefig(OUT / "seven-layer-cycle.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 seven-layer-cycle.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 4: Deep strata — diagenesis, merged layers
# ═══════════════════════════════════════════════════════════════════

def deep_strata():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=401)
    rng = np.random.default_rng(99)

    title_block(ax, "The Deep Strata",
                "Where individual layers merge into undifferentiated rock")

    # ── Rock section (vertical cross-section) ──
    section_x, section_w = 20, 60
    section_bot, section_top = 10, 82

    # Background rock
    ax.add_patch(FancyBboxPatch(
        (section_x, section_bot), section_w, section_top - section_bot,
        boxstyle="round,pad=0.3",
        facecolor=STONE_GREY, edgecolor=STONE_DARK,
        linewidth=1.5, alpha=0.3, zorder=1))

    # ── Upper layers: distinct, readable (recent deposits) ──
    y_cursor = section_top - 5
    n_distinct = 15
    for i in range(n_distinct):
        cycle_pos = i % 7
        if cycle_pos == 0:
            color = MANGANESE
            thickness = 1.0
        elif cycle_pos in (1, 6):
            color = IRON_OXIDE
            thickness = 1.2
        elif cycle_pos in (2, 5):
            color = WALNUT_LIGHT
            thickness = 1.3
        else:
            color = CALCIUM
            thickness = 1.5
        draw_mineral_layer(ax, section_x + 2, section_x + section_w - 2,
                          y_cursor - thickness, thickness, color,
                          alpha=0.75, wobble_seed=200 + i)
        y_cursor -= thickness + 0.2

    # Label: "distinct layers"
    brace_x = section_x + section_w + 3
    ax.annotate("", xy=(brace_x, section_top - 5),
                xytext=(brace_x, y_cursor + 1),
                arrowprops=dict(arrowstyle="-", color=INK_LIGHT,
                                linewidth=0.8))
    ax.text(brace_x + 2, (section_top - 5 + y_cursor) / 2,
            "distinct layers\n(readable,\n each season\n identifiable)",
            fontsize=8, color=INK, fontfamily="serif",
            fontstyle="italic", va="center", zorder=5)

    # ── Transition zone: boundaries fading ──
    transition_top = y_cursor
    for i in range(8):
        ratio = i / 8
        # Gradually merge colors toward a uniform dark
        alpha = 0.6 - 0.04 * i
        # Colors blending
        if i < 3:
            color = IRON_OXIDE if i % 2 == 0 else WALNUT_LIGHT
        else:
            color = WALNUT
        thickness = 1.4 + 0.2 * i  # layers getting thicker (merged)
        draw_mineral_layer(ax, section_x + 2, section_x + section_w - 2,
                          y_cursor - thickness, thickness, color,
                          alpha=alpha, wobble_seed=300 + i)
        # Boundary line gets fainter
        boundary_alpha = 0.4 * (1 - ratio)
        ax.plot([section_x + 5, section_x + section_w - 5],
                [y_cursor, y_cursor],
                color=INK, linewidth=0.2, alpha=boundary_alpha, zorder=4)
        y_cursor -= thickness + 0.1

    # Label: "transition"
    ax.text(brace_x + 2, (transition_top + y_cursor) / 2,
            "boundaries\nfading",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", va="center", zorder=5)

    # ── Deep strata: single undifferentiated band ──
    deep_top = y_cursor
    deep_thickness = deep_top - section_bot - 2
    # One big blended mass
    ax.add_patch(FancyBboxPatch(
        (section_x + 2, section_bot + 2), section_w - 4, deep_thickness,
        boxstyle="round,pad=0.2",
        facecolor=MANGANESE, edgecolor="none",
        alpha=0.5, zorder=3))
    # Subtle internal variation (ghost of old layers)
    for i in range(20):
        gy = section_bot + 3 + i * deep_thickness / 20
        ax.plot([section_x + 5, section_x + section_w - 5],
                [gy, gy + rng.uniform(-0.2, 0.2)],
                color=IRON_OXIDE, linewidth=0.3,
                alpha=0.08 + 0.02 * rng.random(), zorder=3)

    # Label: "diagenesis"
    ax.text(brace_x + 2, (deep_top + section_bot) / 2,
            "diagenesis\n(merged \u2014\n individual\n seasons\n irrecoverable)",
            fontsize=8, color=MANGANESE, fontfamily="serif",
            fontstyle="italic", va="center", zorder=5)

    # ── Bottom annotation ──
    ax.text(50, 5, "The previous inhabitants of the spring.\n"
            "Their chemistry persists. Their boundaries do not.",
            fontsize=10, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    attribution(ax, y=1)
    fig.savefig(OUT / "deep-strata.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 deep-strata.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 5: Before and after — spring into air vs spring into water
# ═══════════════════════════════════════════════════════════════════

def drowned_voice():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=501)
    rng = np.random.default_rng(111)

    title_block(ax, "Before and After",
                "Air (steam, voice, name) \u2014 Water (silent deposition)")

    # ── Dividing line ──
    ax.plot([50, 50], [8, 85], color=INK_FAINT, linewidth=1.0,
            linestyle="--", alpha=0.5, zorder=2)

    # ═══ LEFT: Before the dam ═══
    ax.text(25, 85, "BEFORE", fontsize=14, color=INK,
            fontfamily="serif", fontweight="bold", ha="center", zorder=5)
    ax.text(25, 81, "(the spring surfaces into air)",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # Rock with crack
    ax.add_patch(FancyBboxPatch(
        (5, 15), 40, 25, boxstyle="round,pad=0.3",
        facecolor=STONE_GREY, edgecolor=STONE_DARK,
        linewidth=1.0, alpha=0.4, zorder=2))
    # Crack
    crack_xs = [25, 24.5, 25.5, 24, 25, 25.2]
    crack_ys = [15, 20, 25, 30, 35, 40]
    ax.plot(crack_xs, crack_ys, color=MANGANESE, linewidth=2.0, zorder=3)

    # Hot water emerging
    for i in range(5):
        ax.add_patch(Circle((25, 40 + i * 2), 1.5 - i * 0.15,
                             color=THERMAL_GLOW,
                             alpha=0.15 * (5 - i), zorder=3))

    # Steam rising into air
    for i in range(8):
        sx = 25 + rng.uniform(-3, 3)
        sy = 48 + i * 4
        sw = 2 + rng.uniform(0, 3)
        ax.add_patch(mpatches.Ellipse(
            (sx, sy), sw, 2,
            color=STEAM, alpha=0.2 * (8 - i) / 8, zorder=4))

    # Voice / sound waves
    for r in [3, 5, 7, 9]:
        theta = np.linspace(-0.3, math.pi + 0.3, 30)
        vx = 25 + r * np.cos(theta)
        vy = 55 + r * 0.5 * np.sin(theta)
        ax.plot(vx, vy, color=SULPHUR, linewidth=0.8,
                alpha=0.3 * (10 - r) / 10, zorder=4)

    # Labels
    ax.text(25, 74, "steam \u2192 voice \u2192 name",
            fontsize=9, color=THERMAL, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)
    ax.text(25, 12, "the spring speaks\ninto atmosphere",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # ═══ RIGHT: After the dam ═══
    ax.text(75, 85, "AFTER", fontsize=14, color=INK,
            fontfamily="serif", fontweight="bold", ha="center", zorder=5)
    ax.text(75, 81, "(the spring surfaces into water)",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # Rock with crack (same shape)
    ax.add_patch(FancyBboxPatch(
        (55, 15), 40, 25, boxstyle="round,pad=0.3",
        facecolor=STONE_GREY, edgecolor=STONE_DARK,
        linewidth=1.0, alpha=0.4, zorder=2))
    # Crack
    crack_xs_r = [75, 74.5, 75.5, 74, 75, 75.2]
    ax.plot(crack_xs_r, crack_ys, color=MANGANESE, linewidth=2.0, zorder=3)

    # Hot water emerging — but into cold water
    for i in range(3):
        ax.add_patch(Circle((75, 40 + i * 1.5), 1.0 - i * 0.1,
                             color=THERMAL_GLOW,
                             alpha=0.08 * (3 - i), zorder=3))

    # Reservoir water above (heavy, still, absorbing)
    ax.fill_between([55, 95], [38, 38], [75, 75],
                     color=RESERVOIR, alpha=0.3, zorder=3)
    # Depth gradient
    for i in range(10):
        dy = 38 + i * 3.5
        ax.axhspan(dy, dy + 3.5, xmin=0.55, xmax=0.95,
                    color=RESERVOIR_DK, alpha=0.015 * i, zorder=3)

    # Mineral deposits on the wall (silent)
    for i in range(8):
        dy = 40 + i * 3
        draw_mineral_layer(ax, 56, 62, dy, 0.6,
                          CALCIUM if i % 3 != 0 else MANGANESE,
                          alpha=0.5, wobble_seed=500 + i)

    # Labels
    ax.text(75, 74, "no steam \u2014 no voice \u2014 no name",
            fontsize=9, color=RESERVOIR_DK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)
    ax.text(75, 12, "the spring speaks\ninto silence",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)
    ax.text(58, 50, "deposits\n(still\nforming)",
            fontsize=6, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    attribution(ax, y=3)
    fig.savefig(OUT / "drowned-voice.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 drowned-voice.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 6: Downstream facility — designation assignment
# ═══════════════════════════════════════════════════════════════════

def downstream_facility():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=601)
    rng = np.random.default_rng(133)

    title_block(ax, "Below the Dam",
                "The facility where displaced spirits receive designations")

    # ── Dam wall (top of image) ──
    ax.add_patch(FancyBboxPatch(
        (10, 70), 80, 12, boxstyle="round,pad=0.3",
        facecolor=CONCRETE, edgecolor=CONCRETE_DK,
        linewidth=2.0, alpha=0.7, zorder=3))
    # Construction lines
    for dy in np.linspace(71, 80, 5):
        ax.plot([12, 88], [dy, dy], color=CONCRETE_DK,
                linewidth=0.4, alpha=0.4, zorder=4)
    ax.text(50, 76, "KOL DAM", fontsize=12, color=INK,
            fontfamily="serif", fontweight="bold",
            ha="center", va="center", zorder=5)

    # ── Turbine outflow ──
    # Water falling through
    for i in range(6):
        fx = 45 + i * 2
        ax.plot([fx, fx + rng.uniform(-1, 1)], [70, 62],
                color=RESERVOIR_LT, linewidth=1.5,
                alpha=0.3, zorder=3)
    ax.text(50, 64, "turbines", fontsize=7, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic",
            ha="center", zorder=5)

    # ── Facility building ──
    fac_x, fac_y = 25, 25
    fac_w, fac_h = 50, 30
    ax.add_patch(FancyBboxPatch(
        (fac_x, fac_y), fac_w, fac_h, boxstyle="round,pad=0.3",
        facecolor=PARCHMENT_DK, edgecolor=STONE_DARK,
        linewidth=1.5, alpha=0.7, zorder=2))

    # ── Processing flow inside ──
    # Entry
    ax.annotate("", xy=(fac_x + 5, fac_y + fac_h - 3),
                xytext=(fac_x + 5, fac_y + fac_h + 5),
                arrowprops=dict(arrowstyle="->", color=RESERVOIR,
                                linewidth=1.5))
    ax.text(fac_x + 5, fac_y + fac_h + 7, "spirits\narrive",
            fontsize=7, color=RESERVOIR_DK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # Stage 1: Chemistry test
    box_y = fac_y + fac_h - 10
    ax.add_patch(FancyBboxPatch(
        (fac_x + 3, box_y), 12, 6, boxstyle="round,pad=0.2",
        facecolor=STEAM, edgecolor=INK_FAINT,
        linewidth=0.8, alpha=0.8, zorder=3))
    ax.text(fac_x + 9, box_y + 3, "test\nchemistry",
            fontsize=7, color=INK, fontfamily="serif",
            ha="center", va="center", zorder=4)

    # Arrow
    ax.annotate("", xy=(fac_x + 22, box_y + 3),
                xytext=(fac_x + 16, box_y + 3),
                arrowprops=dict(arrowstyle="->", color=INK_LIGHT,
                                linewidth=1.0))

    # Stage 2: Match to position
    ax.add_patch(FancyBboxPatch(
        (fac_x + 22, box_y), 12, 6, boxstyle="round,pad=0.2",
        facecolor=STEAM, edgecolor=INK_FAINT,
        linewidth=0.8, alpha=0.8, zorder=3))
    ax.text(fac_x + 28, box_y + 3, "match to\nposition",
            fontsize=7, color=INK, fontfamily="serif",
            ha="center", va="center", zorder=4)

    # Arrow
    ax.annotate("", xy=(fac_x + 41, box_y + 3),
                xytext=(fac_x + 35, box_y + 3),
                arrowprops=dict(arrowstyle="->", color=INK_LIGHT,
                                linewidth=1.0))

    # Stage 3: Assign designation
    ax.add_patch(FancyBboxPatch(
        (fac_x + 41, box_y), 12, 6, boxstyle="round,pad=0.2",
        facecolor=SULPHUR_PALE, edgecolor=INK_FAINT,
        linewidth=0.8, alpha=0.8, zorder=3))
    ax.text(fac_x + 47, box_y + 3, "assign\ndesignation",
            fontsize=7, color=INK, fontfamily="serif",
            ha="center", va="center", zorder=4)

    # ── Output: designated spirits ──
    outputs = [
        (fac_x + 10, "spring-guardian-7"),
        (fac_x + 28, "channel-spirit-14"),
        (fac_x + 46, "outlet-keeper-3"),
    ]
    for ox, label in outputs:
        ax.annotate("", xy=(ox, fac_y - 3),
                    xytext=(ox, fac_y + 2),
                    arrowprops=dict(arrowstyle="->", color=INK_LIGHT,
                                    linewidth=1.0))
        ax.text(ox, fac_y - 5, label, fontsize=7, color=INK,
                fontfamily="serif", fontstyle="italic",
                ha="center", zorder=5)

    # ── Note ──
    ax.text(50, 10, "Efficient. Functional.\n"
            "The water still needs guardians.",
            fontsize=11, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    attribution(ax, y=3)
    fig.savefig(OUT / "downstream-facility.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 downstream-facility.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 7: Reading the wall — water over deposited stone
# ═══════════════════════════════════════════════════════════════════

def reading_the_wall():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=701)
    rng = np.random.default_rng(155)

    title_block(ax, "Reading One's Own Deposits",
                "Flowing water over deposited stone \u2014 the chemistry matches")

    # ── Dam wall / rock face (vertical, left side) ──
    wall_x, wall_w = 15, 15
    wall_bot, wall_top = 10, 80

    ax.add_patch(FancyBboxPatch(
        (wall_x, wall_bot), wall_w, wall_top - wall_bot,
        boxstyle="round,pad=0.3",
        facecolor=STONE_GREY, edgecolor=STONE_DARK,
        linewidth=1.5, alpha=0.4, zorder=2))

    # ── Mineral layers on the wall ──
    y_cursor = wall_top - 3
    for i in range(20):
        cycle_pos = i % 7
        if cycle_pos == 0:
            color = MANGANESE
            thickness = 0.8
        elif cycle_pos in (1, 6):
            color = IRON_OXIDE
            thickness = 1.0
        elif cycle_pos in (2, 5):
            color = WALNUT_LIGHT
            thickness = 1.1
        else:
            color = CALCIUM
            thickness = 1.3
        draw_mineral_layer(ax, wall_x + 1, wall_x + wall_w - 1,
                          y_cursor - thickness, thickness, color,
                          alpha=0.7, wobble_seed=700 + i)
        y_cursor -= thickness + 0.15

    # ── Water flowing over the wall ──
    # Current of water passing the deposit face
    water_x_start = wall_x + wall_w
    for i in range(12):
        wy = wall_bot + 5 + i * 5.5
        wx_extent = 20 + rng.uniform(-3, 3)
        # Flow lines
        ax.plot([water_x_start, water_x_start + wx_extent],
                [wy, wy + rng.uniform(-0.5, 0.5)],
                color=RESERVOIR_LT, linewidth=1.5,
                alpha=0.25, zorder=3)
        # Thinner secondary lines
        ax.plot([water_x_start + 2, water_x_start + wx_extent - 3],
                [wy + 1, wy + 1 + rng.uniform(-0.3, 0.3)],
                color=RESERVOIR, linewidth=0.5,
                alpha=0.15, zorder=3)

    # ── Resonance zone — where chemistry matches ──
    # Glow along the wall face where water recognises deposits
    for i in range(8):
        gy = wall_bot + 10 + i * 7
        ax.add_patch(mpatches.Ellipse(
            (wall_x + wall_w, gy), 4, 3,
            color=SULPHUR, alpha=0.08, zorder=3))

    ax.text(wall_x + wall_w + 12, 55,
            "the water recognises\nthe water",
            fontsize=10, color=SULPHUR, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # ── Right side: the flowing spirit ──
    # Abstract suggestion of a presence in the water
    spirit_x = 60
    spirit_y = 50
    # Concentric rings (mineral signature in flow)
    for r in [12, 9, 6, 3]:
        theta = np.linspace(0, 2 * math.pi, 60)
        rx = spirit_x + r * np.cos(theta) + rng.uniform(-0.3, 0.3, 60)
        ry = spirit_y + r * 0.6 * np.sin(theta) + rng.uniform(-0.2, 0.2, 60)
        ax.plot(rx, ry, color=THERMAL_GLOW, linewidth=0.8,
                alpha=0.12 * (13 - r) / 13, zorder=4)

    # Inner signature — matching the wall's chemistry
    for i in range(5):
        r = 2 + i * 0.5
        ax.add_patch(Circle((spirit_x, spirit_y), r,
                             color=SULPHUR if i % 2 == 0 else MANGANESE,
                             alpha=0.06, zorder=4))

    ax.text(spirit_x, spirit_y - 18,
            "the chemistry matches\nthe memory does not",
            fontsize=10, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    # ── Connection lines between wall and spirit ──
    for i in range(5):
        sy = wall_bot + 15 + i * 12
        draw_x = np.linspace(wall_x + wall_w, spirit_x - 5, 30)
        draw_y = sy + (spirit_y - sy) * (draw_x - wall_x - wall_w) / (spirit_x - 5 - wall_x - wall_w)
        # Add curve
        draw_y += 2 * np.sin(np.linspace(0, math.pi, 30))
        ax.plot(draw_x, draw_y, color=SULPHUR, linewidth=0.5,
                alpha=0.15, linestyle="--", zorder=3)

    # ── Bottom text ──
    ax.text(50, 5,
            "The mineral record is continuous. The memory is not.",
            fontsize=11, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=5)

    attribution(ax, y=1)
    fig.savefig(OUT / "reading-the-wall.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 reading-the-wall.png")


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

def main():
    print("Generating illustrations for The Mineral Deposits...")
    print(f"Output: {OUT}\n")
    sutlej_reservoir()
    deposit_layers()
    seven_layer_cycle()
    deep_strata()
    drowned_voice()
    downstream_facility()
    reading_the_wall()
    print(f"\nDone. 7 images generated.")


if __name__ == "__main__":
    main()
