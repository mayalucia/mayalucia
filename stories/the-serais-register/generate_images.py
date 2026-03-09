# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Serai's Register".

A story about a keeper at a junction serai — where the Tirthan meets
the Sainj below Larji — who maintains a register of slate tiles,
sorting travellers not by name or date but by the invariants of hand
and attention. Identity accumulated, not declared.

Visual language: parchment/walnut base. Serai palette — slate tiles,
chalk marks, gravel river-bed, magnetite gorge, copper dusk,
Kath-Kuni stone. Hand-drawn jitter throughout.

Run with:  uv run generate_images.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

# ── Output ──────────────────────────────────────────────────────────
OUT = Path(__file__).parent / "../../website/static/images/writing/the-serais-register"
OUT = OUT.resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9  # inches — 1800×1350 px at 150 DPI

# ── Palette ─────────────────────────────────────────────────────────
PARCHMENT     = "#F5F0E8"
PARCHMENT_DK  = "#EDE6D8"
INK           = "#5C4A3A"
INK_LIGHT     = "#8B7B6B"
INK_FAINT     = "#C4B8A8"

WALNUT        = "#4A3728"
WALNUT_LIGHT  = "#6B5040"

# Deodar / forest
DEODAR        = "#4A6B48"
DEODAR_DK     = "#2E4A2C"
DEODAR_LT     = "#6B8B68"

# Kath-Kuni stone and timber
STONE         = "#9A9080"
STONE_DK      = "#6B6658"
STONE_LT      = "#B8B0A0"
TIMBER        = "#8B6B4A"
TIMBER_DK     = "#6B4A30"

# Water
WATER_WHITE   = "#E8EEF0"
WATER_EMERALD = "#4A8B6B"
WATER_COPPER  = "#C4886B"

# Mountain
MOUNTAIN      = "#7A7068"
MOUNTAIN_DK   = "#5A5248"
SNOW          = "#E8EEF0"

# Sky
SKY_WARM      = "#D8C8B0"
SKY_COPPER    = "#D4A878"
SKY_DUSK      = "#B8886B"

# Slate tiles
SLATE         = "#7A7A78"
SLATE_LT      = "#9A9A98"
SLATE_DK      = "#5A5A58"

# Chalk
CHALK         = "#E8E4D8"
CHALK_DK      = "#D0C8B8"

# Gravel / riverbed
GRAVEL        = "#C4B8A0"
GRAVEL_DK     = "#A89880"
GRAVEL_LT     = "#D8D0C0"

# Magnetite gorge
MAGNETITE     = "#3A3838"
MAGNETITE_LT  = "#5A5858"

# Copper light
COPPER        = "#C4886B"
COPPER_LT     = "#D8A888"
COPPER_DK     = "#A86848"

# Trail / earth
TRAIL_OCHRE   = "#C4A868"
TRAIL_DK      = "#8B7848"

# Charcoal
CHARCOAL      = "#4A4A48"

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


def attribution(ax, text="The Serai\u2019s Register \u2014 A Human-Machine Collaboration",
                y=2):
    ax.text(50, y, text, ha="center", va="bottom",
            fontsize=8, fontstyle="italic", color=INK_LIGHT,
            fontfamily="serif")


def wobbly_line(ax, x0, y0, x1, y1, rng, lw=1.5, color=WALNUT,
                alpha=0.7, n=30, zorder=4):
    xs = np.linspace(x0, x1, n)
    ys = np.linspace(y0, y1, n)
    xs += rng.uniform(-0.25, 0.25, n)
    ys += rng.uniform(-0.25, 0.25, n)
    ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha, zorder=zorder)


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


def draw_kath_kuni_wall(ax, bx, by, bw, bh, n_courses=8, zorder=4):
    for i in range(n_courses):
        cy = by + i * (bh / n_courses)
        ch = bh / n_courses
        color = STONE if i % 2 == 0 else TIMBER
        alpha = 0.7 if i % 2 == 0 else 0.5
        ax.add_patch(FancyBboxPatch(
            (bx, cy), bw, ch, boxstyle="square,pad=0",
            facecolor=color, edgecolor=INK_FAINT,
            linewidth=0.3, alpha=alpha, zorder=zorder))


def draw_slate_tile(ax, x, y, w, h, text_lines, rng, chalk_style="normal",
                    zorder=4):
    """Draw a single slate tile with chalk writing."""
    # Tile body
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.2",
        facecolor=SLATE, edgecolor=SLATE_DK,
        linewidth=0.8, alpha=0.7, zorder=zorder))
    # Chalk text
    lean = 0 if chalk_style == "normal" else (0.08 if chalk_style == "lean_right" else -0.05)
    pressure_start = 0.85 if chalk_style == "heavy_start" else 0.7
    pressure_end = 0.55 if chalk_style == "heavy_start" else 0.7
    for i, line in enumerate(text_lines):
        ty = y + h - 1.8 - i * 1.6
        if ty < y + 0.5:
            break
        for j, ch in enumerate(line):
            tx = x + 1.0 + j * 0.65
            if tx > x + w - 0.5:
                break
            progress = j / max(len(line), 1)
            alpha = pressure_start + (pressure_end - pressure_start) * progress
            jx = rng.uniform(-0.08, 0.08) + lean * j * 0.3
            jy = rng.uniform(-0.08, 0.08)
            ax.text(tx + jx, ty + jy, ch, fontsize=5.5,
                    color=CHALK, fontfamily="serif",
                    alpha=alpha, zorder=zorder + 1)


# ═══════════════════════════════════════════════════════════════════
# Figure 1: The serai at the junction
# Stone building at the confluence, deodar, gravel bed, two rivers
# ═══════════════════════════════════════════════════════════════════

def the_serai():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=601)
    rng = np.random.default_rng(42)

    title_block(ax, "The Serai at the Junction",
                "Where the Tirthan meets the Sainj \u2014 a place where different trails arrive at the same hearth")

    # ── Mountains (background) ──
    draw_mountain_ridge(ax, 0, 100, 62, 20, n_peaks=6, color=MOUNTAIN, seed=60)

    # ── Hillside ──
    hill_xs = np.linspace(0, 100, 200)
    hill_ys = 58 - 0.05 * hill_xs + 2 * np.sin(hill_xs * 0.03)
    ax.fill_between(hill_xs, 8, hill_ys, color=DEODAR_LT, alpha=0.1, zorder=1)

    # ── Gravel bed (confluence area) ──
    gravel_xs = np.linspace(5, 95, 200)
    gravel_top = 32 + 3 * np.sin(gravel_xs * 0.06)
    ax.fill_between(gravel_xs, 10, gravel_top, color=GRAVEL, alpha=0.2, zorder=2)
    # Scattered gravel stones
    for _ in range(60):
        gx = rng.uniform(8, 92)
        gy = rng.uniform(12, 30)
        gs = rng.uniform(0.2, 0.5)
        gc = rng.choice([GRAVEL, GRAVEL_DK, GRAVEL_LT])
        ax.add_patch(Circle((gx, gy), gs, color=gc,
                             alpha=rng.uniform(0.2, 0.4), zorder=2))

    # ── The Tirthan (from the west/north, entering from left) ──
    t = np.linspace(0, 1, 150)
    tirthan_x = 5 + 35 * t + 4 * np.sin(t * 3 * np.pi)
    tirthan_y = 45 - 15 * t + 2 * np.cos(t * 2 * np.pi)
    for i in range(len(t) - 1):
        w = 1.2 + 0.3 * np.sin(t[i] * 5 * np.pi)
        ax.plot([tirthan_x[i], tirthan_x[i+1]],
                [tirthan_y[i], tirthan_y[i+1]],
                color=WATER_EMERALD, linewidth=w * 2, alpha=0.4, zorder=3)
    ax.text(10, 44, "Tirthan", fontsize=8, color=WATER_EMERALD,
            fontfamily="serif", fontstyle="italic", alpha=0.6, zorder=7)

    # ── The Sainj (from the east, entering from right) ──
    sainj_x = 95 - 40 * t + 3 * np.sin(t * 2.5 * np.pi)
    sainj_y = 42 - 12 * t + 2 * np.cos(t * 2 * np.pi)
    for i in range(len(t) - 1):
        w = 1.0 + 0.3 * np.sin(t[i] * 4 * np.pi)
        ax.plot([sainj_x[i], sainj_x[i+1]],
                [sainj_y[i], sainj_y[i+1]],
                color=WATER_EMERALD, linewidth=w * 1.8, alpha=0.35, zorder=3)
    ax.text(88, 41, "Sainj", fontsize=8, color=WATER_EMERALD,
            fontfamily="serif", fontstyle="italic", alpha=0.6, zorder=7)

    # ── Combined river (flowing south) ──
    combined_x = 48 + 6 * np.sin(t * 2 * np.pi)
    combined_y = 28 - 18 * t
    for i in range(len(t) - 1):
        w = 1.8 + 0.4 * np.sin(t[i] * 6 * np.pi)
        ax.plot([combined_x[i], combined_x[i+1]],
                [combined_y[i], combined_y[i+1]],
                color=WATER_EMERALD, linewidth=w * 2, alpha=0.45, zorder=3)

    # ── The serai (Kath-Kuni, low slate roof, near junction) ──
    sx, sy, sw, sh = 38, 34, 24, 14
    draw_kath_kuni_wall(ax, sx, sy, sw, sh, n_courses=7, zorder=4)

    # Low slate roof
    roof_xs = [sx - 1.5, sx + sw / 2, sx + sw + 1.5]
    roof_ys = [sy + sh, sy + sh + 4, sy + sh]
    ax.fill(roof_xs, roof_ys, color=SLATE, alpha=0.5, zorder=5)
    ax.plot(roof_xs, roof_ys, color=INK, linewidth=0.5, zorder=5)

    # Moss on roof
    for _ in range(8):
        mx = rng.uniform(sx, sx + sw)
        my = sy + sh + rng.uniform(0.5, 3)
        ax.add_patch(Circle((mx, my), rng.uniform(0.4, 1.0),
                             color=DEODAR_LT, alpha=rng.uniform(0.1, 0.25),
                             zorder=5))

    # Door
    ax.add_patch(FancyBboxPatch(
        (sx + sw / 2 - 2, sy), 4, 7, boxstyle="round,pad=0.2",
        facecolor=TIMBER_DK, edgecolor=INK_FAINT,
        linewidth=0.5, alpha=0.6, zorder=6))

    # ── The old deodar ──
    trunk_x = sx + sw + 3
    trunk_y = sy
    ax.plot([trunk_x, trunk_x], [trunk_y, trunk_y + 20],
            color=TIMBER_DK, linewidth=4, alpha=0.5, zorder=3)
    for layer in range(5):
        ly = trunk_y + 8 + layer * 3
        lw = 6 - layer * 0.8
        tree_xs = [trunk_x - lw, trunk_x, trunk_x + lw]
        tree_ys = [ly, ly + 4, ly]
        ax.fill(tree_xs, tree_ys, color=DEODAR,
                alpha=0.25 + layer * 0.03, zorder=3)

    # ── Trails converging (dotted paths) ──
    # Trail from Tirthan (west)
    for i in range(8):
        tx = 8 + i * 4
        ty = 48 - i * 1.5 + rng.uniform(-0.3, 0.3)
        ax.add_patch(Circle((tx, ty), 0.3, color=TRAIL_OCHRE,
                             alpha=0.3, zorder=4))
    # Trail from Sainj (east)
    for i in range(8):
        tx = 88 - i * 5
        ty = 44 - i * 1.2 + rng.uniform(-0.3, 0.3)
        ax.add_patch(Circle((tx, ty), 0.3, color=TRAIL_OCHRE,
                             alpha=0.3, zorder=4))
    # Trail from Banjar (south)
    for i in range(5):
        tx = 50 + rng.uniform(-1, 1)
        ty = 12 + i * 4
        ax.add_patch(Circle((tx, ty), 0.3, color=TRAIL_OCHRE,
                             alpha=0.3, zorder=4))

    # ── Labels ──
    ax.text(sx + sw / 2, sy - 3, "the serai", fontsize=10, color=INK,
            fontfamily="serif", fontstyle="italic", ha="center", zorder=7)
    ax.text(48, 8, "toward Larji and the Beas",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    attribution(ax, y=3)
    fig.savefig(OUT / "the-serai.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 the-serai.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 2: The slate register — tiles grouped with blank dividers
# Shows the keeper's sorting system: identity, not chronology
# ═══════════════════════════════════════════════════════════════════

def the_register():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=602)
    rng = np.random.default_rng(55)

    title_block(ax, "The Slate Register",
                "Sorted by identity, not by time \u2014 blank tiles for the silences between visits")

    # ── Wooden box (open, seen from above) ──
    ax.add_patch(FancyBboxPatch(
        (8, 10), 84, 74, boxstyle="round,pad=0.5",
        facecolor=TIMBER, edgecolor=TIMBER_DK,
        linewidth=2.0, alpha=0.3, zorder=1))

    # ── Tile groups ──
    # Group 1: Raju/Rajesh — 4 tiles (the man who stops naming himself)
    tiles_g1 = [
        ["Raju. From Sainj,", "upper trail. Saw a", "barking deer standing", "in the stream."],
        ["Raju. From Banjar.", "Found a blue stone", "in the path \u2014 smooth", "as a tongue."],
        ["Rajesh. From Sainj.", "A moth the size of", "my hand, resting on", "the magnetite wall."],
        ["No name. Tirthan.", "The gorge was singing", "\u2014 bees, but lower,", "when the wind came."],
    ]
    x_start = 12
    y_top = 78
    tw, th = 16, 10
    gap = 1.2

    # Draw group 1
    ax.text(x_start, y_top + 2, "Group 1", fontsize=7, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", zorder=7)
    for i, lines in enumerate(tiles_g1):
        tx = x_start + i * (tw + gap)
        draw_slate_tile(ax, tx, y_top - th, tw, th, lines, rng,
                        chalk_style="heavy_start", zorder=4)

    # Blank divider
    blank_x = x_start + len(tiles_g1) * (tw + gap) + 1
    ax.add_patch(FancyBboxPatch(
        (blank_x, y_top - th + 1), 3, th - 2, boxstyle="round,pad=0.2",
        facecolor=SLATE_LT, edgecolor=SLATE, linewidth=0.5,
        alpha=0.3, zorder=4))

    # Group 2: Priya — 3 tiles (the woman from the Tirthan)
    tiles_g2 = [
        ["Priya. Tirthan,", "above gorge. The", "water smelled of", "iron and cedar."],
        ["P. From Banjar.", "A child singing to", "a goat \u2014 the goat", "listening."],
        ["No name. Tirthan.", "Magnetite walls", "were singing \u2014 bees", "but lower."],
    ]
    y_mid = y_top - th - 6
    ax.text(x_start, y_mid + 2, "Group 2", fontsize=7, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", zorder=7)
    for i, lines in enumerate(tiles_g2):
        tx = x_start + i * (tw + gap)
        draw_slate_tile(ax, tx, y_mid - th, tw, th, lines, rng,
                        chalk_style="lean_right", zorder=4)

    # Blank divider
    blank_x2 = x_start + len(tiles_g2) * (tw + gap) + 1
    ax.add_patch(FancyBboxPatch(
        (blank_x2, y_mid - th + 1), 3, th - 2, boxstyle="round,pad=0.2",
        facecolor=SLATE_LT, edgecolor=SLATE, linewidth=0.5,
        alpha=0.3, zorder=4))

    # Singles (isolated tiles — questions the register is still asking)
    y_low = y_mid - th - 6
    ax.text(x_start, y_low + 2, "Singles", fontsize=7, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", zorder=7)

    single_tiles = [
        ["Gopal. Tirthan.", "Saw nothing", "unusual. The trail", "was the trail."],
        ["No name. Sainj.", "A snake crossing", "the path stopped", "and waited for me."],
    ]
    for i, lines in enumerate(single_tiles):
        tx = x_start + i * (tw + gap + 5)
        draw_slate_tile(ax, tx, y_low - th, tw, th, lines, rng,
                        chalk_style="normal", zorder=4)
        # Blank dividers around singles
        ax.add_patch(FancyBboxPatch(
            (tx - 2.5, y_low - th + 1), 1.8, th - 2,
            boxstyle="round,pad=0.2",
            facecolor=SLATE_LT, edgecolor=SLATE, linewidth=0.3,
            alpha=0.2, zorder=3))
        ax.add_patch(FancyBboxPatch(
            (tx + tw + 0.8, y_low - th + 1), 1.8, th - 2,
            boxstyle="round,pad=0.2",
            facecolor=SLATE_LT, edgecolor=SLATE, linewidth=0.3,
            alpha=0.2, zorder=3))

    # ── Key annotation ──
    ax.text(72, 18, "a single tile is\nnot an error \u2014\nit is a question",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=PARCHMENT,
                      edgecolor=INK_FAINT, alpha=0.8))

    attribution(ax, y=3)
    fig.savefig(OUT / "slate-register.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 slate-register.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 3: The hand's invariants — chalk marks compared
# Same lean, same pressure, different names, different valleys
# ═══════════════════════════════════════════════════════════════════

def the_hand():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=603)
    rng = np.random.default_rng(66)

    title_block(ax, "The Hand\u2019s Invariants",
                "Different names, different valleys, different years \u2014 the chalk leans the same way")

    # Show three tiles from the same traveller, with analysis marks
    # connecting the invariants

    tile_data = [
        ("Year 1 \u2014 from the Sainj", "Raju",
         ["Raju. From Sainj,", "upper trail. Saw a", "barking deer standing", "in the stream, not", "drinking, just", "standing."]),
        ("Year 2 \u2014 from Banjar", "Rajesh",
         ["Rajesh. From Banjar", "side, the mule track.", "Found a blue stone", "in the path \u2014 not", "slate, but blue, like", "a piece of sky."]),
        ("Year 3 \u2014 from the Tirthan", "\u2014",
         ["No name. Tirthan,", "from above. The gorge", "was singing \u2014 a sound", "like bees, but lower,", "when the wind came", "from the north."]),
    ]

    tw, th = 24, 18
    gap = 4
    total_w = 3 * tw + 2 * gap
    x_start = (100 - total_w) / 2

    for i, (label, name, lines) in enumerate(tile_data):
        tx = x_start + i * (tw + gap)
        ty = 30

        # Year/valley label
        ax.text(tx + tw / 2, ty + th + 5, label, fontsize=9,
                color=INK, fontfamily="serif", fontstyle="italic",
                ha="center", zorder=7)
        # Name label (or dash)
        ax.text(tx + tw / 2, ty + th + 2, f"name: {name}", fontsize=7,
                color=INK_LIGHT, fontfamily="serif", ha="center", zorder=7)

        # The tile (larger, for legibility)
        ax.add_patch(FancyBboxPatch(
            (tx, ty), tw, th, boxstyle="round,pad=0.3",
            facecolor=SLATE, edgecolor=SLATE_DK,
            linewidth=1.0, alpha=0.7, zorder=4))

        # Chalk writing with consistent lean and pressure
        lean = 0.08  # same lean for all three — the invariant
        for j, line in enumerate(lines):
            ly = ty + th - 2.2 - j * 2.2
            if ly < ty + 0.5:
                break
            for k, ch in enumerate(line):
                lx = tx + 1.5 + k * 0.8
                if lx > tx + tw - 1:
                    break
                progress = k / max(len(line), 1)
                alpha = 0.85 - 0.25 * progress  # heavy start, light end
                jx = rng.uniform(-0.06, 0.06) + lean * k * 0.2
                jy = rng.uniform(-0.06, 0.06)
                ax.text(lx + jx, ly + jy, ch, fontsize=6,
                        color=CHALK, fontfamily="serif",
                        alpha=alpha, zorder=5)

    # ── Connecting arcs showing invariants ──
    # "same lean" bracket
    for i in range(2):
        x1 = x_start + i * (tw + gap) + tw * 0.8
        x2 = x_start + (i + 1) * (tw + gap) + tw * 0.2
        y_arc = 26
        arc_t = np.linspace(0, np.pi, 30)
        arc_x = (x1 + x2) / 2 + (x2 - x1) / 2 * np.cos(arc_t)
        arc_y = y_arc - 3 * np.sin(arc_t)
        ax.plot(arc_x, arc_y, color=COPPER, linewidth=1.2,
                alpha=0.5, linestyle="--", zorder=6)

    ax.text(50, 18, "same hand \u2014 same lean \u2014 same pressure",
            fontsize=10, color=COPPER_DK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    ax.text(50, 13, "the surprise is the same kind of surprise:\n"
            "things that belong to one world appearing in another",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7, linespacing=1.5)

    attribution(ax, y=3)
    fig.savefig(OUT / "the-hand.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 the-hand.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 4: The rivers meeting at dusk
# Two rivers converging, the serai between them, copper light,
# the thick walls that strip words to rhythm
# ═══════════════════════════════════════════════════════════════════

def rivers_at_dusk():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=604)
    rng = np.random.default_rng(77)

    title_block(ax, "The Voices in the Dark",
                "Through the wall, the words are gone \u2014 the rhythm remains")

    # ── Dusk sky ──
    for i in range(25):
        gy = 55 + i * 2
        alpha = 0.02 + 0.012 * i
        color = SKY_COPPER if i < 15 else SKY_DUSK
        ax.axhspan(gy, gy + 2, color=color, alpha=alpha, zorder=0)

    # ── Mountains (silhouette) ──
    draw_mountain_ridge(ax, 0, 100, 58, 22, n_peaks=7,
                        color=MOUNTAIN_DK, seed=70)

    # ── Hillsides ──
    hill_xs = np.linspace(0, 100, 200)
    hill_ys = 54 - 0.06 * hill_xs + 2 * np.sin(hill_xs * 0.04)
    ax.fill_between(hill_xs, 8, hill_ys, color=DEODAR_DK, alpha=0.12, zorder=1)

    # ── Magnetite gorge walls (Tirthan side, northwest) ──
    # Left wall
    wall_xs = np.array([0, 8, 12, 14, 12, 8, 5, 0])
    wall_ys = np.array([55, 52, 48, 40, 35, 30, 25, 20])
    ax.fill(wall_xs, wall_ys, color=MAGNETITE, alpha=0.35, zorder=2)
    ax.plot(wall_xs[1:], wall_ys[1:], color=MAGNETITE_LT, linewidth=0.6,
            alpha=0.5, zorder=2)

    # ── Two rivers converging in copper light ──
    t = np.linspace(0, 1, 200)

    # Tirthan from northwest
    tirthan_x = 12 + 30 * t + 5 * np.sin(t * 3 * np.pi)
    tirthan_y = 50 - 18 * t + 2 * np.cos(t * 2 * np.pi)
    for i in range(len(t) - 1):
        w = 1.0 + 0.3 * np.sin(t[i] * 5 * np.pi)
        ax.plot([tirthan_x[i], tirthan_x[i+1]],
                [tirthan_y[i], tirthan_y[i+1]],
                color=WATER_COPPER, linewidth=w * 2.5, alpha=0.5, zorder=3)

    # Sainj from east
    sainj_x = 92 - 38 * t + 4 * np.sin(t * 2.5 * np.pi)
    sainj_y = 48 - 16 * t + 2 * np.cos(t * 2 * np.pi)
    for i in range(len(t) - 1):
        w = 0.8 + 0.3 * np.sin(t[i] * 4 * np.pi)
        ax.plot([sainj_x[i], sainj_x[i+1]],
                [sainj_y[i], sainj_y[i+1]],
                color=WATER_COPPER, linewidth=w * 2.2, alpha=0.45, zorder=3)

    # Combined flow south
    combined_x = 50 + 8 * np.sin(t * 2 * np.pi)
    combined_y = 30 - 22 * t
    for i in range(len(t) - 1):
        w = 2.0 + 0.5 * np.sin(t[i] * 6 * np.pi)
        ax.plot([combined_x[i], combined_x[i+1]],
                [combined_y[i], combined_y[i+1]],
                color=WATER_COPPER, linewidth=w * 2.5, alpha=0.55, zorder=3)

    # ── Serai silhouette (dark against copper water) ──
    sx, sy = 42, 34
    sw, sh = 16, 10
    ax.add_patch(FancyBboxPatch(
        (sx, sy), sw, sh, boxstyle="round,pad=0.3",
        facecolor=MAGNETITE, edgecolor=MAGNETITE_LT,
        linewidth=0.8, alpha=0.6, zorder=5))
    # Roof
    roof_xs = [sx - 1, sx + sw / 2, sx + sw + 1]
    roof_ys = [sy + sh, sy + sh + 3, sy + sh]
    ax.fill(roof_xs, roof_ys, color=SLATE_DK, alpha=0.5, zorder=5)

    # ── Warm light from hearth (glow through door/window) ──
    glow = plt.Circle((sx + sw / 2, sy + 3), 2.5,
                        color=SKY_COPPER, alpha=0.25, zorder=5)
    ax.add_patch(glow)
    glow2 = plt.Circle((sx + sw / 2, sy + 3), 1.2,
                         color=COPPER_LT, alpha=0.3, zorder=5)
    ax.add_patch(glow2)

    # ── Voices as rhythm lines (abstract: waves emerging from the walls) ──
    # Three different rhythms, visible as wave patterns
    voice_y = 20
    for vi, (freq, amp, phase, label) in enumerate([
        (3.0, 0.8, 0, "even rhythm \u2014 the keeper"),
        (5.5, 1.0, 0.5, "bursts and silences \u2014 the walker"),
        (2.0, 1.2, 1.0, "long phrases \u2014 the teacher"),
    ]):
        vy = voice_y - vi * 5
        vt = np.linspace(0, 4 * np.pi, 120)
        vx = 18 + 64 * vt / (4 * np.pi)
        v_wave = vy + amp * np.sin(freq * vt + phase)
        # Add hand-drawn jitter
        v_wave += rng.uniform(-0.1, 0.1, len(vt))
        ax.plot(vx, v_wave, color=INK, linewidth=0.8, alpha=0.4, zorder=6)
        ax.text(15, vy, label, fontsize=6.5, color=INK_LIGHT,
                fontfamily="serif", fontstyle="italic",
                ha="right", va="center", zorder=7)

    attribution(ax, y=2)
    fig.savefig(OUT / "voices-in-the-dark.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 voices-in-the-dark.png")


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating illustrations for The Serai\u2019s Register...")
    the_serai()
    the_register()
    the_hand()
    rivers_at_dusk()
    print(f"\nDone. Output: {OUT}")
