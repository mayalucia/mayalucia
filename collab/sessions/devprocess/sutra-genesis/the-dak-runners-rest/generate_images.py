# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Dāk Runner's Rest".

A story about the old postal relay — runners who carried sealed pouches
over Himalayan passes. The difference between carrying a message and
carrying a custom. Three hands in a register: the Runner, the Inspector,
the third hand who tried to write the custom into words.

Visual language: parchment/walnut base. Dāk palette — postal leather,
faded blue ledger ink, copper twilight, trail ochre, slate rubble,
deodar green. Hand-drawn jitter throughout.

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
OUT = Path(__file__).parent / "../../../../../website/static/images/writing/the-dak-runners-rest"
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

# Leather / postal
LEATHER       = "#6B4A30"
LEATHER_DK    = "#4A3020"
LEATHER_LT    = "#8B6B50"

# Ledger ink (faded blue)
LEDGER_BLUE   = "#8898A8"
LEDGER_BLUE_DK = "#6B7888"
LEDGER_BLUE_LT = "#A8B8C8"

# Trail / earth
TRAIL_OCHRE   = "#C4A868"
TRAIL_DK      = "#8B7848"

# Copper light
COPPER        = "#C4886B"
COPPER_LT     = "#D8A888"
COPPER_DK     = "#A86848"

# Slate (rubble)
SLATE_BG      = "#7A7A78"
SLATE_LT      = "#9A9A98"

# Charcoal
CHARCOAL      = "#4A4A48"
CHARCOAL_LT   = "#6A6A68"


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


def attribution(ax, text="The D\u0101k Runner\u2019s Rest \u2014 A Human-Machine Collaboration",
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


# ═══════════════════════════════════════════════════════════════════
# Figure 1: The ruined dāk bungalow
# Stone and timber, collapsed east end, channel leading to it
# ═══════════════════════════════════════════════════════════════════

def dak_bungalow():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=501)
    rng = np.random.default_rng(42)

    title_block(ax, "The D\u0101k Bungalow, Tirthan Stage IV",
                "Too long, too narrow \u2014 a building designed to be arrived at and departed from")

    # ── Hillside ──
    hill_xs = np.linspace(0, 100, 200)
    hill_ys = 55 - 0.1 * hill_xs + 3 * np.sin(hill_xs * 0.04)
    ax.fill_between(hill_xs, 8, hill_ys, color=DEODAR_LT, alpha=0.12, zorder=1)

    # ── Deodar trees (sparse, around bungalow) ──
    for _ in range(20):
        tx = rng.uniform(3, 97)
        ty = rng.uniform(35, 55)
        th = rng.uniform(3, 7)
        tw = rng.uniform(1.2, 2.5)
        xs_t = [tx - tw / 2, tx, tx + tw / 2]
        ys_t = [ty, ty + th, ty]
        ax.fill(xs_t, ys_t, color=DEODAR, alpha=rng.uniform(0.15, 0.3), zorder=2)

    # ── The bungalow (long, narrow, Kath-Kuni) ──
    # Western end (standing)
    bx, by, bw, bh = 20, 22, 35, 20
    draw_kath_kuni_wall(ax, bx, by, bw, bh, n_courses=10, zorder=4)

    # Roof on western end
    roof_xs = [bx - 2, bx + bw / 2, bx + bw + 2]
    roof_ys = [by + bh, by + bh + 6, by + bh]
    ax.fill(roof_xs, roof_ys, color=STONE_DK, alpha=0.5, zorder=5)
    ax.plot(roof_xs, roof_ys, color=INK, linewidth=0.6, zorder=5)

    # Eastern end (collapsed) — rubble
    rubble_x = bx + bw
    for _ in range(25):
        rx = rubble_x + rng.uniform(0, 18)
        ry = by + rng.uniform(-2, 12)
        rs = rng.uniform(0.8, 2.5)
        color = rng.choice([STONE, TIMBER, STONE_DK, TIMBER_DK])
        angle = rng.uniform(0, 360)
        rect = mpatches.FancyBboxPatch(
            (rx, ry), rs, rs * 0.6, boxstyle="square,pad=0",
            facecolor=color, edgecolor=INK_FAINT,
            linewidth=0.2, alpha=rng.uniform(0.3, 0.6))
        t = matplotlib.transforms.Affine2D().rotate_deg_around(
            rx + rs / 2, ry + rs * 0.3, angle) + ax.transData
        rect.set_transform(t)
        ax.add_patch(rect)

    # Collapsed deodar beams (diagonal)
    for i in range(4):
        beam_x = rubble_x + i * 4 + rng.uniform(0, 2)
        beam_y = by + 8 + rng.uniform(-2, 2)
        beam_angle = rng.uniform(-30, -10)
        beam_len = rng.uniform(8, 14)
        bx2 = beam_x + beam_len * np.cos(np.radians(beam_angle))
        by2 = beam_y + beam_len * np.sin(np.radians(beam_angle))
        ax.plot([beam_x, bx2], [beam_y, by2],
                color=TIMBER, linewidth=2.5, alpha=0.5, zorder=5)

    # ── Windows (narrow, passage-spaced) ──
    for i in range(4):
        wx = bx + 4 + i * 8
        wy = by + bh * 0.5
        ax.add_patch(FancyBboxPatch(
            (wx, wy), 2.5, 4, boxstyle="round,pad=0.15",
            facecolor=SKY_WARM, edgecolor=INK_FAINT,
            linewidth=0.5, alpha=0.4, zorder=6))

    # ── The channel (leading uphill to bungalow) ──
    ch_t = np.linspace(0, 1, 60)
    ch_x = 10 + (bx - 5) * ch_t + 2 * np.sin(ch_t * 3 * np.pi)
    ch_y = 12 + (by - 2) * ch_t
    # Displaced stones along channel
    for i in range(0, len(ch_t), 4):
        offset = rng.uniform(-1.5, 1.5)
        ax.add_patch(Circle((ch_x[i] + offset, ch_y[i]),
                             rng.uniform(0.3, 0.6),
                             color=STONE_LT, alpha=0.4, zorder=3))
    # Water in channel (thin, erratic)
    ax.plot(ch_x, ch_y, color=WATER_EMERALD, linewidth=1.0,
            alpha=0.4, zorder=3)
    ax.text(8, 10, "silted\nchannel", fontsize=7, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", ha="center", zorder=7)

    # ── Labels ──
    ax.text(bx + bw / 2, by - 4, "D\u0101k Bungalow \u2014 Tirthan Stage IV",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)
    ax.text(rubble_x + 8, by + 18, "collapsed\n(single snow load)",
            fontsize=7, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7)

    # ── Distance: mountains ──
    draw_mountain_ridge(ax, 0, 100, 52, 18, n_peaks=5, color=MOUNTAIN, seed=50)

    attribution(ax, y=3)
    fig.savefig(OUT / "dak-bungalow.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 dak-bungalow.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 2: The register — three hands
# Leather-bound ledger, faded blue ruling, three handwriting samples
# ═══════════════════════════════════════════════════════════════════

def the_register():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=502)
    rng = np.random.default_rng(55)

    title_block(ax, "The Register \u2014 Three Hands",
                "Runner, Inspector, and the one who could not be identified")

    # ── Ledger background (leather cover, open pages) ──
    # Cover (visible at edges)
    ax.add_patch(FancyBboxPatch(
        (12, 12), 76, 70, boxstyle="round,pad=0.8",
        facecolor=LEATHER, edgecolor=LEATHER_DK,
        linewidth=2.0, alpha=0.6, zorder=2))

    # Open pages
    ax.add_patch(FancyBboxPatch(
        (15, 14), 70, 66, boxstyle="round,pad=0.3",
        facecolor=PARCHMENT, edgecolor=INK_FAINT,
        linewidth=0.5, alpha=0.9, zorder=3))

    # Spine (center line)
    ax.plot([50, 50], [14, 80], color=LEATHER_LT, linewidth=1.5,
            alpha=0.4, zorder=4)

    # Blue ruling (faded)
    for y in range(18, 78, 3):
        ax.plot([17, 48], [y, y], color=LEDGER_BLUE_LT,
                linewidth=0.3, alpha=0.25, zorder=3)
        ax.plot([52, 83], [y, y], color=LEDGER_BLUE_LT,
                linewidth=0.3, alpha=0.25, zorder=3)

    # ── The Runner's hand (left page, upper) ──
    runner_y = 70
    ax.text(18, runner_y, "The Runner", fontsize=10, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    # Simulated practical handwriting (short horizontal strokes)
    entries = [
        "14 M\u0101gh. Clear. Trail firm.",
        "3 letters, 1 packet.",
        "Arrived before the shadow",
        "reached the stream.",
        "",
        "27 Ph\u0101gun. Snow to the knee.",
        "1 letter, marked urgent.",
        "Left the packet for next day.",
    ]
    for i, line in enumerate(entries):
        y = runner_y - 4 - i * 2.8
        # Simulate handwriting with slightly wobbly baseline
        for j, ch in enumerate(line):
            x = 18 + j * 0.85
            if x > 47:
                break
            ax.text(x + rng.uniform(-0.1, 0.1),
                    y + rng.uniform(-0.15, 0.15),
                    ch, fontsize=7, color=INK,
                    fontfamily="serif", alpha=0.7, zorder=5)

    # ── The Inspector's hand (left page, lower) ──
    insp_y = 38
    ax.text(18, insp_y, "The Inspector", fontsize=10, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    insp_entries = [
        "Inspected 3 Chaitra.",
        "Register entries complete.",
        "Cupboard lock functions.",
        "Water channel requires",
        "clearing \u2014 silted at the",
        "second bend.",
    ]
    for i, line in enumerate(insp_entries):
        y = insp_y - 4 - i * 2.8
        for j, ch in enumerate(line):
            x = 18 + j * 0.75
            if x > 47:
                break
            # Copperplate: more regular, slightly more spaced
            ax.text(x, y + rng.uniform(-0.05, 0.05),
                    ch, fontsize=6.5, color=LEDGER_BLUE_DK,
                    fontfamily="serif", alpha=0.65, zorder=5)

    # ── The Third Hand (right page) ──
    third_y = 70
    ax.text(53, third_y, "The Third Hand", fontsize=10, color=INK,
            fontfamily="serif", fontweight="bold", zorder=5)
    third_entries = [
        "The runner does not open",
        "the pouch because the",
        "custom is that the pouch",
        "is not opened between",
        "stages. The seal is not",
        "a lock. It is a record",
        "of the custom having",
        "been observed.",
        "",
        "The question is not who",
        "can read the message.",
        "The question is who",
        "carries the custom.",
    ]
    for i, line in enumerate(third_entries):
        y = third_y - 4 - i * 2.8
        for j, ch in enumerate(line):
            x = 53 + j * 0.82
            if x > 83:
                break
            # Different rhythm — correct letters, foreign phrasing
            ax.text(x + rng.uniform(-0.12, 0.12),
                    y + rng.uniform(-0.1, 0.1),
                    ch, fontsize=7, color=WALNUT,
                    fontfamily="serif", fontstyle="italic",
                    alpha=0.6, zorder=5)

    # ── Embossed title on cover (top) ──
    ax.text(50, 83, "D\u0101K BUNGALOW REGISTER",
            fontsize=9, color=LEATHER_DK, fontfamily="serif",
            fontweight="bold", ha="center", alpha=0.5, zorder=4)
    ax.text(50, 80.5, "TIRTHAN STAGE IV",
            fontsize=7, color=LEATHER_DK, fontfamily="serif",
            ha="center", alpha=0.4, zorder=4)

    attribution(ax, y=3)
    fig.savefig(OUT / "the-register.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 the-register.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 3: Trail marks — the runner's notation system
# Weather symbols, the invented triangle, the cross for washout
# ═══════════════════════════════════════════════════════════════════

def trail_marks():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=503)
    rng = np.random.default_rng(66)

    title_block(ax, "The Runner\u2019s Trail Marks",
                "Not in any manual \u2014 marks invented because the register needed them")

    # ── Slate background (like a notation tablet) ──
    ax.add_patch(FancyBboxPatch(
        (10, 12), 80, 70, boxstyle="round,pad=0.5",
        facecolor=SLATE_BG, edgecolor=STONE_DK,
        linewidth=1.5, alpha=0.2, zorder=1))

    # ── The notation system ──
    marks = [
        (20, 65, "clear", "circle",
         "the day is open\nnothing between\nthe runner and the pass"),
        (50, 65, "snow", "hatched_circle",
         "the trail is covered\nbut the trail is there"),
        (80, 65, "rain", "wavy",
         "water falling\nwater rising\nwater everywhere"),
        (20, 38, "washout", "cross",
         "the trail is gone\nfind another way"),
        (50, 38, "changed", "triangle",
         "the trail is there\nbut different\nadjust your step"),
        (80, 38, "urgent", "exclamation",
         "leave the packet\ncarry the letter"),
    ]

    for (cx, cy, label, mark_type, desc) in marks:
        # Draw the mark
        if mark_type == "circle":
            theta = np.linspace(0, 2 * np.pi, 40)
            xs = cx + 4 * np.cos(theta) + rng.uniform(-0.2, 0.2, 40)
            ys = cy + 4 * np.sin(theta) + rng.uniform(-0.2, 0.2, 40)
            ax.plot(xs, ys, color=CHARCOAL, linewidth=2.0, alpha=0.7, zorder=5)

        elif mark_type == "hatched_circle":
            theta = np.linspace(0, 2 * np.pi, 40)
            xs = cx + 4 * np.cos(theta) + rng.uniform(-0.2, 0.2, 40)
            ys = cy + 4 * np.sin(theta) + rng.uniform(-0.2, 0.2, 40)
            ax.plot(xs, ys, color=CHARCOAL, linewidth=2.0, alpha=0.7, zorder=5)
            # Hatching
            for i in range(5):
                hx = cx - 3 + i * 1.5
                wobbly_line(ax, hx, cy - 3, hx + 1, cy + 3, rng,
                           lw=0.8, color=CHARCOAL, alpha=0.4, zorder=5)

        elif mark_type == "wavy":
            t = np.linspace(-np.pi, np.pi, 50)
            wx = cx + 4 * t / np.pi
            wy = cy + 1.5 * np.sin(t * 2) + rng.uniform(-0.15, 0.15, 50)
            ax.plot(wx, wy, color=CHARCOAL, linewidth=2.0, alpha=0.7, zorder=5)
            wx2 = cx + 4 * t / np.pi
            wy2 = cy - 1.5 + 1.5 * np.sin(t * 2 + 0.5) + rng.uniform(-0.15, 0.15, 50)
            ax.plot(wx2, wy2, color=CHARCOAL, linewidth=1.5, alpha=0.5, zorder=5)

        elif mark_type == "cross":
            wobbly_line(ax, cx - 3.5, cy - 3.5, cx + 3.5, cy + 3.5, rng,
                       lw=2.5, color=CHARCOAL, alpha=0.7, zorder=5)
            wobbly_line(ax, cx - 3.5, cy + 3.5, cx + 3.5, cy - 3.5, rng,
                       lw=2.5, color=CHARCOAL, alpha=0.7, zorder=5)

        elif mark_type == "triangle":
            # THE invented mark — larger, more emphatic
            tx = [cx - 4, cx, cx + 4, cx - 4]
            ty = [cy - 3, cy + 4, cy - 3, cy - 3]
            tx = np.array(tx) + rng.uniform(-0.3, 0.3, 4)
            ty = np.array(ty) + rng.uniform(-0.3, 0.3, 4)
            ax.plot(tx, ty, color=CHARCOAL, linewidth=2.5, alpha=0.8, zorder=5)
            # Emphasis: slight fill
            ax.fill(tx, ty, color=CHARCOAL_LT, alpha=0.1, zorder=4)

        elif mark_type == "exclamation":
            wobbly_line(ax, cx, cy + 4, cx, cy - 1.5, rng,
                       lw=2.5, color=CHARCOAL, alpha=0.7, zorder=5)
            ax.add_patch(Circle((cx, cy - 3), 0.6,
                                 color=CHARCOAL, alpha=0.7, zorder=5))

        # Label
        ax.text(cx, cy + 7, label, fontsize=9, color=INK,
                fontfamily="serif", fontstyle="italic",
                ha="center", va="bottom", zorder=7)

        # Description
        ax.text(cx, cy - 8.5, desc, fontsize=6.5, color=INK_LIGHT,
                fontfamily="serif", fontstyle="italic",
                ha="center", va="top", zorder=7, linespacing=1.3)

    # ── The key insight ──
    ax.text(50, 10, "this mark is not in any manual\n"
            "it is a mark my grandfather invented",
            fontsize=10, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=PARCHMENT,
                      edgecolor=INK_FAINT, alpha=0.7))

    attribution(ax, y=3)
    fig.savefig(OUT / "trail-marks.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 trail-marks.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 4: The trail at dusk — copper light on the Tirthan
# Overgrown runner's trail, copper river, the gradient that persists
# ═══════════════════════════════════════════════════════════════════

def trail_at_dusk():
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=504)
    rng = np.random.default_rng(77)

    title_block(ax, "The Trail at Dusk",
                "The gradient carries everything at the same speed \u2014 the runner carries the urgent letter first")

    # ── Dusk sky (warm copper gradient) ──
    for i in range(20):
        gy = 60 + i * 2.2
        alpha = 0.02 + 0.015 * i
        color = SKY_COPPER if i < 12 else SKY_DUSK
        ax.axhspan(gy, gy + 2.2, color=color, alpha=alpha, zorder=0)

    # ── Mountains (silhouette against dusk) ──
    draw_mountain_ridge(ax, 0, 100, 60, 25, n_peaks=7,
                        color=MOUNTAIN_DK, seed=70)

    # ── Hillsides ──
    hill_xs = np.linspace(0, 100, 200)
    hill_ys = 58 - 0.08 * hill_xs + 3 * np.sin(hill_xs * 0.05)
    ax.fill_between(hill_xs, 8, hill_ys, color=DEODAR_DK, alpha=0.15, zorder=1)

    # ── The Tirthan in copper light ──
    t = np.linspace(0, 1, 300)
    river_x = 75 - 50 * t + 10 * np.sin(t * 4.5 * np.pi)
    river_y = 55 - 40 * t + 3 * np.cos(t * 3 * np.pi)

    widths = 1.0 + 0.6 * np.sin(t * 7 * np.pi) ** 2

    for i in range(len(t) - 1):
        x0, y0 = river_x[i], river_y[i]
        x1, y1 = river_x[i + 1], river_y[i + 1]
        w = widths[i]

        dx = x1 - x0
        dy_seg = y1 - y0
        length = max(np.sqrt(dx**2 + dy_seg**2), 0.01)
        nx, ny = -dy_seg / length, dx / length

        xs = [x0 - nx * w, x0 + nx * w, x1 + nx * w, x1 - nx * w]
        ys = [y0 - ny * w, y0 + ny * w, y1 + ny * w, y1 - ny * w]
        ax.fill(xs, ys, color=WATER_COPPER, alpha=0.6, zorder=3)

    ax.plot(river_x, river_y, color=COPPER_DK, linewidth=0.4, alpha=0.4, zorder=4)

    # ── The overgrown trail (runner's path, dotted, fading) ──
    trail_t = np.linspace(0, 1, 100)
    trail_x = 20 + 30 * trail_t + 5 * np.sin(trail_t * 6 * np.pi)
    trail_y = 12 + 35 * trail_t + 2 * np.cos(trail_t * 4 * np.pi)

    # Trail fades as it goes up (older, more overgrown)
    for i in range(len(trail_t) - 1):
        alpha = 0.5 * (1 - trail_t[i] * 0.7)
        ax.plot([trail_x[i], trail_x[i + 1]], [trail_y[i], trail_y[i + 1]],
                color=TRAIL_OCHRE, linewidth=1.2, alpha=alpha,
                linestyle=(0, (2, 3)), zorder=4)

    # ── Overgrowth on trail (small marks) ──
    for i in range(0, len(trail_t), 6):
        if rng.random() < 0.5:
            gx = trail_x[i] + rng.uniform(-1, 1)
            gy = trail_y[i] + rng.uniform(-0.5, 0.5)
            gh = rng.uniform(1, 2.5)
            ax.plot([gx, gx + rng.uniform(-0.3, 0.3)], [gy, gy + gh],
                    color=DEODAR_LT, linewidth=0.6, alpha=0.3, zorder=4)

    # ── The old channel (parallel to trail, broken) ──
    ch_x = trail_x - 3 + rng.uniform(-0.5, 0.5, len(trail_t))
    ch_y = trail_y - 1.5
    # Draw as discontinuous segments
    for i in range(0, len(trail_t) - 2, 3):
        if rng.random() < 0.6:  # gaps where channel is broken
            ax.plot([ch_x[i], ch_x[i + 2]], [ch_y[i], ch_y[i + 2]],
                    color=WATER_EMERALD, linewidth=0.6, alpha=0.25, zorder=3)

    # ── Deodar trees (dark silhouettes) ──
    for _ in range(25):
        tx = rng.uniform(3, 97)
        ty = rng.uniform(20, 50)
        th = rng.uniform(3, 8)
        tw = rng.uniform(1.2, 2.5)
        xs_t = [tx - tw / 2, tx, tx + tw / 2]
        ys_t = [ty, ty + th, ty]
        ax.fill(xs_t, ys_t, color=DEODAR_DK, alpha=rng.uniform(0.2, 0.4), zorder=2)

    # ── The Thread Walker's notebook entry ──
    ax.text(50, 8, "the channel carries water because the ground is shaped for it\n"
            "the runner carried mail because the custom shaped him for it",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=7,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=PARCHMENT,
                      edgecolor=INK_FAINT, alpha=0.8))

    attribution(ax, y=2)
    fig.savefig(OUT / "trail-at-dusk.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print("  \u2713 trail-at-dusk.png")


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating illustrations for The D\u0101k Runner\u2019s Rest...")
    dak_bungalow()
    the_register()
    trail_marks()
    trail_at_dusk()
    print(f"\nDone. Output: {OUT}")
