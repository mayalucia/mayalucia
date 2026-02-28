# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Instrument Maker's Rest".

Visual language: diagrammatic, information-dense, warm parchment tones,
ink-line drawing style. Matches existing MayaLucIA story illustrations
(map-of-passes, palette-altitude, cord-correction-letter, wool-reading).

Run with:  uv run generate_images.py
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, Rectangle, PathPatch
from matplotlib.path import Path as MPath
import numpy as np

# ── Output ──────────────────────────────────────────────────────────
OUT = Path(__file__).parent / "../../../../../website/static/images/writing/instrument-makers-rest"
OUT = OUT.resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9  # inches — gives 1800×1350 px at 150 DPI

# ── Palette ─────────────────────────────────────────────────────────
PARCHMENT     = "#F5F0E8"
PARCHMENT_DK  = "#EDE6D8"
INK           = "#5C4A3A"
INK_LIGHT     = "#8B7B6B"
INK_FAINT     = "#C4B8A8"
BRASS         = "#B8963E"
BRASS_DARK    = "#8C6D1F"
BRASS_LIGHT   = "#D4B96A"
DEODAR        = "#7A5C3A"
DEODAR_LIGHT  = "#A68B5B"
INDIGO        = "#3B4F6B"
TERRACOTTA    = "#B85C3A"
SAGE          = "#6B8B6B"
RIVER_BLUE    = "#7BA3C4"
SNOW_WHITE    = "#E8E4DC"
SHADOW        = "#D5CFC2"


# ── Shared helpers ──────────────────────────────────────────────────

def make_fig(width=W, height=H):
    """Create a figure with parchment background and no axes."""
    fig, ax = plt.subplots(1, 1, figsize=(width, height), facecolor=PARCHMENT)
    ax.set_facecolor(PARCHMENT)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def add_parchment_texture(ax, seed=42):
    """Add subtle noise texture to simulate aged paper."""
    rng = np.random.default_rng(seed)
    # Faint circular stains (like the map-of-passes style)
    for _ in range(8):
        cx, cy = rng.uniform(10, 90), rng.uniform(10, 90)
        r = rng.uniform(5, 15)
        circle = plt.Circle((cx, cy), r, color=PARCHMENT_DK,
                             alpha=rng.uniform(0.15, 0.35), zorder=0)
        ax.add_patch(circle)


def title_block(ax, title: str, subtitle: str = "", y: float = 95):
    """Draw a centered title and optional italic subtitle."""
    ax.text(50, y, title, ha="center", va="top",
            fontsize=18, fontweight="bold", color=INK,
            fontfamily="serif")
    if subtitle:
        ax.text(50, y - 4, subtitle, ha="center", va="top",
                fontsize=11, fontstyle="italic", color=INK_LIGHT,
                fontfamily="serif")


def attribution(ax, text: str, y: float = 2):
    """Small italic attribution at the bottom."""
    ax.text(50, y, text, ha="center", va="bottom",
            fontsize=8, fontstyle="italic", color=INK_LIGHT,
            fontfamily="serif")


def draw_brass_fitting(ax, x, y, w, h, label=None):
    """A small brass rectangle with highlight — represents a fitting."""
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=BRASS, edgecolor=BRASS_DARK,
                          linewidth=1.2, zorder=3)
    ax.add_patch(rect)
    # Highlight stripe
    ax.plot([x + 0.3, x + w - 0.3], [y + h * 0.7, y + h * 0.7],
            color=BRASS_LIGHT, linewidth=1.5, alpha=0.6, zorder=4)
    if label:
        ax.text(x + w / 2, y - 0.8, label, ha="center", va="top",
                fontsize=7, color=INK_LIGHT, fontfamily="serif")


def draw_deodar_frame(ax, x, y, w, h, notches=True):
    """A deodar wood rectangle with optional notch marks."""
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                          facecolor=DEODAR_LIGHT, edgecolor=DEODAR,
                          linewidth=1.5, zorder=2)
    ax.add_patch(rect)
    # Wood grain lines
    for i in range(3):
        yg = y + h * (0.25 + 0.25 * i)
        ax.plot([x + 0.5, x + w - 0.5], [yg, yg + 0.2],
                color=DEODAR, linewidth=0.5, alpha=0.4, zorder=3)
    # Notch marks along one edge
    if notches:
        n = int(w / 2)
        for i in range(n):
            nx = x + 1 + i * (w - 2) / max(n - 1, 1)
            ax.plot([nx, nx], [y + h, y + h + 0.5],
                    color=DEODAR, linewidth=0.8, zorder=3)


def draw_ruler_marks(ax, x, y, length, vertical=False, n=10):
    """Graduated measurement marks — like a ruler edge."""
    for i in range(n + 1):
        if vertical:
            pos = y + i * length / n
            tick_len = 1.0 if i % 5 == 0 else 0.5
            ax.plot([x, x + tick_len], [pos, pos],
                    color=INK, linewidth=0.6, zorder=4)
        else:
            pos = x + i * length / n
            tick_len = 1.0 if i % 5 == 0 else 0.5
            ax.plot([pos, pos], [y, y + tick_len],
                    color=INK, linewidth=0.6, zorder=4)


def draw_dotted_leader(ax, x1, y1, x2, y2, color=INK_FAINT):
    """Dotted annotation leader line."""
    ax.plot([x1, x2], [y1, y2], color=color,
            linewidth=0.8, linestyle=":", zorder=2)
    ax.plot(x1, y1, "o", color=color, markersize=3, zorder=3)


def draw_label_box(ax, x, y, text, color=SAGE, align="left"):
    """Small bordered annotation label."""
    ha = align
    bbox = dict(boxstyle="round,pad=0.3", facecolor=PARCHMENT,
                edgecolor=color, linewidth=0.8, alpha=0.9)
    ax.text(x, y, text, ha=ha, va="center", fontsize=8,
            color=color, fontfamily="serif", bbox=bbox, zorder=5)


def save(fig, name: str):
    """Save figure as PNG."""
    path = OUT / f"{name}.png"
    fig.savefig(path, dpi=DPI, facecolor=fig.get_facecolor(),
                bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  ✓ {path.name}")


# ── Image 1: Workshop Bench ────────────────────────────────────────

def workshop_bench():
    """
    The maker's bench — brass fittings, deodar frames,
    graduated rules, a standing card in progress.
    """
    fig, ax = make_fig()
    add_parchment_texture(ax)
    title_block(ax, "The Maker's Bench",
                "brass fittings, deodar frames, graduated rules, a standing card in progress")

    # Bench surface — a wide warm rectangle
    bench = FancyBboxPatch((8, 15), 84, 55, boxstyle="round,pad=0.5",
                           facecolor="#C4A87A", edgecolor=DEODAR,
                           linewidth=2, zorder=1, alpha=0.3)
    ax.add_patch(bench)

    # Wood grain across bench
    rng = np.random.default_rng(7)
    for i in range(12):
        yb = 18 + i * 4
        xs = np.linspace(10, 90, 60)
        ys = yb + rng.normal(0, 0.15, 60).cumsum() * 0.1
        ax.plot(xs, ys, color=DEODAR, linewidth=0.4, alpha=0.25, zorder=1)

    # --- Objects on the bench ---

    # 1. Brass fittings cluster (top-left area)
    for i, (bx, by, bw, bh) in enumerate([
        (14, 58, 3, 2), (18, 59, 2.5, 1.5), (15, 55, 2, 2.5),
        (20, 56, 3.5, 2), (22, 59.5, 2, 1.5)
    ]):
        draw_brass_fitting(ax, bx, by, bw, bh)
    draw_label_box(ax, 12, 52, "brass fittings\nmountain alloy", color=BRASS_DARK)

    # 2. Deodar frame pieces (center-left)
    draw_deodar_frame(ax, 30, 40, 20, 4)
    draw_deodar_frame(ax, 32, 46, 16, 3.5)
    draw_deodar_frame(ax, 35, 51, 12, 3, notches=False)
    draw_label_box(ax, 30, 37, "deodar frames\ndevadāru — timber of the gods", color=DEODAR)

    # 3. Graduated rule (long, thin, with marks)
    rule_y = 30
    ax.add_patch(FancyBboxPatch((15, rule_y), 50, 2,
                                boxstyle="round,pad=0.1",
                                facecolor=DEODAR_LIGHT, edgecolor=DEODAR,
                                linewidth=1, zorder=2))
    draw_ruler_marks(ax, 16, rule_y + 2, 48, vertical=False, n=24)
    draw_label_box(ax, 15, 27, "graduated rule — notches, not paint", color=INK)

    # 4. Standing card in progress (right side)
    card_x, card_y = 68, 40
    # Card body (slightly tilted via transform would be nice, but keep simple)
    card = FancyBboxPatch((card_x, card_y), 18, 24,
                          boxstyle="round,pad=0.3",
                          facecolor="#F8F4EC", edgecolor=INK_LIGHT,
                          linewidth=1.2, zorder=3)
    ax.add_patch(card)
    # "Handwritten" lines on the card
    for i in range(7):
        lw = rng.uniform(12, 16)
        ly = card_y + 20 - i * 2.5
        ax.plot([card_x + 2, card_x + 2 + lw], [ly, ly],
                color=INK_LIGHT, linewidth=0.8, alpha=0.5 + 0.05 * i, zorder=4)
    # The last lines are incomplete — card in progress
    ax.plot([card_x + 2, card_x + 8], [card_y + 4.5, card_y + 4.5],
            color=INK, linewidth=1.0, alpha=0.7, zorder=4)
    draw_label_box(ax, card_x + 9, card_y - 2,
                   "standing card\nin progress", color=TERRACOTTA, align="center")

    # 5. Small tools scattered
    # Brass pin
    ax.plot([58, 58], [55, 62], color=BRASS_DARK, linewidth=2, zorder=3)
    ax.plot(58, 62, "o", color=BRASS, markersize=5, zorder=4)
    # Wax block
    wax = FancyBboxPatch((60, 22), 6, 4, boxstyle="round,pad=0.2",
                         facecolor="#D4A030", edgecolor="#AA8020",
                         linewidth=1, alpha=0.6, zorder=2)
    ax.add_patch(wax)
    draw_label_box(ax, 63, 19, "beeswax & pine resin", color=BRASS_DARK, align="center")

    # Reference weight
    cx, cy = 78, 58
    circle = plt.Circle((cx, cy), 2.5, facecolor=BRASS,
                         edgecolor=BRASS_DARK, linewidth=1.5, zorder=3)
    ax.add_patch(circle)
    ax.text(cx, cy, "REF", ha="center", va="center",
            fontsize=6, color=PARCHMENT, fontweight="bold", zorder=4)
    draw_label_box(ax, cx, 54, "calibration\nweight", color=BRASS_DARK, align="center")

    # Window indication (top right) — light coming in
    ax.add_patch(Rectangle((82, 72), 14, 18, facecolor=SNOW_WHITE,
                            edgecolor=INK_LIGHT, linewidth=1.5,
                            alpha=0.4, zorder=0))
    ax.text(89, 81, "window\n→ east", ha="center", va="center",
            fontsize=8, fontstyle="italic", color=INK_FAINT, zorder=1)

    attribution(ax, "From the workshop of the Instrument Maker, Sangla, Baspa valley — 2680m")
    save(fig, "workshop-bench")


# ── Image 2: Seven Instruments ─────────────────────────────────────

def seven_instruments():
    """
    Seven instruments laid out on cloth — schematic, top-down, labeled.
    """
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=17)
    title_block(ax, "The Seven Instruments",
                "one commission, seven functions — schematic, top-down")

    # Cloth background
    cloth = FancyBboxPatch((5, 8), 90, 76, boxstyle="round,pad=1",
                           facecolor="#EDE8DC", edgecolor=INK_FAINT,
                           linewidth=1, zorder=0, alpha=0.5)
    ax.add_patch(cloth)

    # Seven instruments arranged in a gentle arc
    instruments = [
        ("I. Calibration",   "prepares the\nworkshop", SAGE),
        ("II. Observation",  "reads the\narchive",     INDIGO),
        ("III. Precision",   "builds the\nmodel",      TERRACOTTA),
        ("IV. Repetition",   "adjusts the\nloom",      BRASS_DARK),
        ("V. Testing",       "finds the\nflaws",       "#8B3A3A"),
        ("VI. Reading",      "observes the\nworkshop",  RIVER_BLUE),
        ("VII. Assembly",    "weaves the\nbolt",       DEODAR),
    ]

    for i, (name, desc, color) in enumerate(instruments):
        # Position in a gentle arc
        t = (i - 3) / 3  # -1 to 1
        cx = 50 + t * 35
        cy = 52 + (1 - t**2) * 12  # parabolic arc

        # Deodar frame body — slightly different sizes
        fw = 8 + (i % 3) * 0.5
        fh = 14 + (i % 2) * 2
        draw_deodar_frame(ax, cx - fw/2, cy - fh/2, fw, fh, notches=(i != 5))

        # Brass fitting at top
        draw_brass_fitting(ax, cx - 1.5, cy + fh/2 - 1.5, 3, 1.5)

        # Distinguishing mark per instrument (colored dot/line)
        ax.plot(cx, cy, "o", color=color, markersize=8, zorder=5)

        # Number label
        ax.text(cx, cy + fh/2 + 3, name, ha="center", va="bottom",
                fontsize=9, fontweight="bold", color=INK,
                fontfamily="serif", zorder=5)

        # Description below
        ax.text(cx, cy - fh/2 - 2, desc, ha="center", va="top",
                fontsize=7, fontstyle="italic", color=color,
                fontfamily="serif", zorder=5)

    # Shared components note
    ax.text(50, 12, "All share: mountain brass fittings  ·  deodar frames  ·  "
            "notched scales  ·  self-calibrating reference materials",
            ha="center", va="center", fontsize=8, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic")

    attribution(ax, "Commissioned by the Thread Walker — seven functions, one workshop, one season")
    save(fig, "seven-instruments")


# ── Image 3: Calibration Test ──────────────────────────────────────

def calibration_test():
    """
    Close-up of self-calibration mechanism: reference weight,
    sample cord, standard swatch, with notched markings. Annotated.
    """
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=31)
    title_block(ax, "Self-Calibration Mechanism",
                "reference weight, sample cord, standard swatch — annotated diagram")

    # Main instrument body (large deodar frame, center)
    draw_deodar_frame(ax, 25, 25, 50, 50, notches=True)

    # Additional notch marks along left edge (calibration instructions)
    draw_ruler_marks(ax, 25, 28, 44, vertical=True, n=22)

    # --- Components inside the frame ---

    # Reference weight (brass circle, top-left quadrant)
    wx, wy = 38, 60
    weight = plt.Circle((wx, wy), 4, facecolor=BRASS,
                         edgecolor=BRASS_DARK, linewidth=2, zorder=4)
    ax.add_patch(weight)
    # Concentric ring
    ring = plt.Circle((wx, wy), 2.5, facecolor="none",
                       edgecolor=BRASS_DARK, linewidth=1, zorder=5)
    ax.add_patch(ring)
    ax.text(wx, wy, "48g", ha="center", va="center",
            fontsize=8, color=PARCHMENT, fontweight="bold", zorder=6)
    draw_dotted_leader(ax, wx - 5, wy + 3, 15, 72)
    draw_label_box(ax, 3, 72, "reference weight\ncast mountain brass\nknown mass: 48g", color=BRASS_DARK)

    # Sample cord (horizontal line with knots, mid-right)
    cord_y = 48
    ax.plot([40, 68], [cord_y, cord_y], color=TERRACOTTA,
            linewidth=2.5, zorder=4)
    # Knots
    for kx in [44, 52, 60, 66]:
        ax.plot(kx, cord_y, "o", color=TERRACOTTA, markersize=5, zorder=5)
    draw_dotted_leader(ax, 68, cord_y, 82, 62)
    draw_label_box(ax, 82, 62, "sample cord\nknown tension\nknots at 4cm intervals",
                   color=TERRACOTTA, align="center")

    # Standard swatch (small woven rectangle, bottom-right)
    sx, sy = 55, 30
    swatch = FancyBboxPatch((sx, sy), 12, 10, boxstyle="round,pad=0.3",
                            facecolor="#D5C9B0", edgecolor=DEODAR,
                            linewidth=1.5, zorder=3)
    ax.add_patch(swatch)
    # Weave pattern — grid lines
    for j in range(8):
        # Warp (vertical)
        lx = sx + 1.5 + j * 1.3
        ax.plot([lx, lx], [sy + 1, sy + 9], color=INK_LIGHT,
                linewidth=0.5, zorder=4)
        # Weft (horizontal)
        ly = sy + 1.5 + j * 1.1
        if ly < sy + 9:
            ax.plot([sx + 1, sx + 11], [ly, ly], color=INK_FAINT,
                    linewidth=0.5, zorder=4)
    draw_dotted_leader(ax, sx + 12, sy + 5, 82, 38)
    draw_label_box(ax, 82, 38, "standard swatch\nknown sett: 12/cm\nlocal wool, standard weight",
                   color=DEODAR, align="center")

    # Notched calibration instructions (left edge detail)
    draw_dotted_leader(ax, 25, 55, 8, 55)
    draw_label_box(ax, 1, 55, "calibration steps\nnotched into frame\nGuild notation", color=INK)

    # Brass mounting pin (top center)
    pin_x, pin_y = 50, 76
    draw_brass_fitting(ax, pin_x - 2, pin_y - 1, 4, 2)
    draw_dotted_leader(ax, pin_x, pin_y + 2, pin_x, 83)
    draw_label_box(ax, pin_x, 85, "mounting pin\nbracket-agnostic",
                   color=BRASS_DARK, align="center")

    # Step annotations around the border
    steps = [
        (10, 42, "Step 1: Mount and level"),
        (10, 37, "Step 2: Zero the gauge"),
        (10, 32, "Step 3: Weigh the reference"),
        (10, 27, "Step 4: Tension the cord"),
        (10, 22, "Step 5: Read against swatch"),
        (10, 17, "Step 6: Record local offset"),
    ]
    for sx, sy, text in steps:
        ax.text(sx, sy, text, fontsize=7, color=INK_LIGHT,
                fontfamily="serif", zorder=5)

    attribution(ax, "The instrument does not arrive knowing what correct looks like. "
                "It arrives knowing how to learn.")
    save(fig, "calibration-test")


# ── Image 4: Two Brackets ─────────────────────────────────────────

def two_brackets():
    """
    Same mechanism on two different frames: pit loom (left),
    backstrap loom (right). Same brass core.
    """
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=53)
    title_block(ax, "Two Brackets, One Mechanism",
                "the function and the interface are separable")

    # --- Left: Pit loom bracket ---
    ax.text(25, 82, "Pit Loom", ha="center", fontsize=13,
            fontweight="bold", color=INK, fontfamily="serif")
    ax.text(25, 78, "Lahaul workshop", ha="center", fontsize=9,
            fontstyle="italic", color=INK_LIGHT, fontfamily="serif")

    # Horizontal beam
    ax.add_patch(FancyBboxPatch((8, 55), 34, 3, boxstyle="round,pad=0.2",
                                facecolor=DEODAR_LIGHT, edgecolor=DEODAR,
                                linewidth=2, zorder=2))
    ax.text(25, 57.5, "horizontal beam", ha="center", va="bottom",
            fontsize=7, color=DEODAR, fontfamily="serif")

    # Clamp bracket
    ax.add_patch(Rectangle((19, 50), 12, 5, facecolor=BRASS_LIGHT,
                            edgecolor=BRASS_DARK, linewidth=1.5, zorder=3))
    # Clamp jaws
    ax.plot([19, 19], [50, 55], color=BRASS_DARK, linewidth=2.5, zorder=4)
    ax.plot([31, 31], [50, 55], color=BRASS_DARK, linewidth=2.5, zorder=4)
    ax.text(25, 49, "clamp bracket", ha="center", va="top",
            fontsize=7, color=BRASS_DARK, fontfamily="serif")

    # Mechanism (shared — identical on both sides)
    mech_left = FancyBboxPatch((18, 32), 14, 16, boxstyle="round,pad=0.3",
                               facecolor=DEODAR_LIGHT, edgecolor=DEODAR,
                               linewidth=1.5, zorder=3)
    ax.add_patch(mech_left)
    draw_brass_fitting(ax, 22, 44, 6, 2.5)
    # Indicator
    ax.plot(25, 40, "o", color=TERRACOTTA, markersize=10, zorder=5)
    ax.text(25, 40, "M", ha="center", va="center", fontsize=8,
            fontweight="bold", color=PARCHMENT, zorder=6)

    # Pin connecting bracket to mechanism
    ax.plot([25, 25], [48, 50], color=BRASS, linewidth=3, zorder=4)
    ax.plot(25, 49, "s", color=BRASS, markersize=6, zorder=5)

    # Warp threads below (pit loom style — vertical)
    for i in range(10):
        tx = 13 + i * 2.5
        ax.plot([tx, tx], [15, 32], color=INK_FAINT, linewidth=0.8,
                alpha=0.6, zorder=1)

    # --- Right: Backstrap loom bracket ---
    ax.text(75, 82, "Backstrap Loom", ha="center", fontsize=13,
            fontweight="bold", color=INK, fontfamily="serif")
    ax.text(75, 78, "beyond the Baralacha", ha="center", fontsize=9,
            fontstyle="italic", color=INK_LIGHT, fontfamily="serif")

    # Strap (diagonal/curved)
    strap_x = np.array([60, 65, 72, 80, 88])
    strap_y = np.array([65, 60, 55, 58, 63])
    ax.plot(strap_x, strap_y, color=DEODAR, linewidth=4, zorder=2, alpha=0.6)
    ax.plot(strap_x, strap_y, color=DEODAR_LIGHT, linewidth=2, zorder=2)
    ax.text(75, 67, "backstrap", ha="center", va="bottom",
            fontsize=7, color=DEODAR, fontfamily="serif")

    # Hook bracket
    hook_x, hook_y = 72, 51
    # Hook shape
    hook_path = MPath(
        [(hook_x - 3, hook_y + 4), (hook_x - 3, hook_y + 8),
         (hook_x, hook_y + 10), (hook_x + 3, hook_y + 8),
         (hook_x + 3, hook_y + 4)],
        [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3, MPath.CURVE3, MPath.CURVE3]
    )
    ax.add_patch(PathPatch(hook_path, facecolor="none",
                           edgecolor=BRASS_DARK, linewidth=2.5, zorder=4))
    ax.add_patch(Rectangle((hook_x - 4, hook_y), 8, 4,
                            facecolor=BRASS_LIGHT, edgecolor=BRASS_DARK,
                            linewidth=1.5, zorder=3))
    ax.text(75, 49, "hook bracket", ha="center", va="top",
            fontsize=7, color=BRASS_DARK, fontfamily="serif")

    # Same mechanism (identical to left)
    mech_right = FancyBboxPatch((68, 32), 14, 16, boxstyle="round,pad=0.3",
                                facecolor=DEODAR_LIGHT, edgecolor=DEODAR,
                                linewidth=1.5, zorder=3)
    ax.add_patch(mech_right)
    draw_brass_fitting(ax, 72, 44, 6, 2.5)
    ax.plot(75, 40, "o", color=TERRACOTTA, markersize=10, zorder=5)
    ax.text(75, 40, "M", ha="center", va="center", fontsize=8,
            fontweight="bold", color=PARCHMENT, zorder=6)

    # Pin
    ax.plot([75, 75], [48, 51], color=BRASS, linewidth=3, zorder=4)
    ax.plot(75, 49.5, "s", color=BRASS, markersize=6, zorder=5)

    # Warp threads (diagonal — backstrap style)
    for i in range(8):
        tx = 65 + i * 2.5
        ax.plot([tx, tx + 3], [15, 32], color=INK_FAINT, linewidth=0.8,
                alpha=0.6, zorder=1)

    # Center divider — dashed
    ax.plot([50, 50], [12, 85], color=INK_FAINT, linewidth=0.8,
            linestyle="--", zorder=1)

    # "Same pin" annotation
    ax.annotate("same pin", xy=(25, 49), xytext=(50, 50),
                fontsize=8, color=BRASS_DARK, fontfamily="serif",
                ha="center", arrowprops=dict(arrowstyle="->", color=BRASS_DARK,
                                             lw=0.8, ls="--"))
    ax.annotate("", xy=(75, 49.5), xytext=(50, 50),
                arrowprops=dict(arrowstyle="->", color=BRASS_DARK,
                                lw=0.8, ls="--"))

    # Bottom note
    ax.text(50, 8, "Seven mechanisms  ×  fourteen brackets  =  any valley, any loom",
            ha="center", fontsize=9, fontstyle="italic", color=INK_LIGHT,
            fontfamily="serif")

    attribution(ax, "The mechanism does not know or care what holds it. It knows only what it measures.")
    save(fig, "two-brackets")


# ── Image 5: Departure ─────────────────────────────────────────────

def departure():
    """
    The Thread Walker crossing the wooden bridge over the Baspa river.
    Sangla visible behind, mountain wall rising. Ink-and-wash sketch.
    """
    fig, ax = make_fig(W, H + 1)
    add_parchment_texture(ax, seed=67)
    title_block(ax, "The Departure",
                "Sangla — the wooden bridge over the Baspa", y=97)

    rng = np.random.default_rng(67)

    # --- Sky / mountain backdrop ---
    # Mountain silhouette (background)
    mx = np.linspace(0, 100, 200)
    # Two overlapping ridges
    ridge1 = 75 + 8 * np.sin(mx * 0.08) + 3 * np.sin(mx * 0.2) + rng.normal(0, 0.3, 200)
    ridge2 = 70 + 6 * np.sin(mx * 0.06 + 1) + 4 * np.sin(mx * 0.15) + rng.normal(0, 0.3, 200)

    ax.fill_between(mx, ridge1, 100, color=SNOW_WHITE, alpha=0.5, zorder=1)
    ax.plot(mx, ridge1, color=INK_LIGHT, linewidth=0.8, alpha=0.5, zorder=1)
    ax.fill_between(mx, ridge2, ridge1, color=SHADOW, alpha=0.3, zorder=1)
    ax.plot(mx, ridge2, color=INK_LIGHT, linewidth=1, alpha=0.6, zorder=1)

    # Snowline
    snow_y = 78
    ax.fill_between(mx, np.maximum(ridge1, snow_y), 100,
                    color="white", alpha=0.3, zorder=1)

    # --- River ---
    river_x = np.linspace(0, 100, 150)
    river_center = 30 + 2 * np.sin(river_x * 0.05)
    river_width = 4
    ax.fill_between(river_x, river_center - river_width/2,
                    river_center + river_width/2,
                    color=RIVER_BLUE, alpha=0.35, zorder=2)
    # River flow lines
    for i in range(5):
        ry = river_center + (i - 2) * 0.8
        ax.plot(river_x, ry + rng.normal(0, 0.1, 150),
                color=RIVER_BLUE, linewidth=0.4, alpha=0.5, zorder=2)

    # --- Bridge ---
    bridge_x1, bridge_x2 = 35, 65
    bridge_y = 33
    # Bridge planks
    ax.add_patch(FancyBboxPatch((bridge_x1, bridge_y - 1), bridge_x2 - bridge_x1, 2.5,
                                boxstyle="round,pad=0.1",
                                facecolor=DEODAR_LIGHT, edgecolor=DEODAR,
                                linewidth=1.5, zorder=4))
    # Plank lines
    for px in np.linspace(bridge_x1 + 1, bridge_x2 - 1, 15):
        ax.plot([px, px], [bridge_y - 0.8, bridge_y + 1.3],
                color=DEODAR, linewidth=0.6, alpha=0.5, zorder=4)

    # Bridge supports
    ax.plot([bridge_x1, bridge_x1 + 2], [bridge_y - 1, bridge_y - 5],
            color=DEODAR, linewidth=2, zorder=3)
    ax.plot([bridge_x2, bridge_x2 - 2], [bridge_y - 1, bridge_y - 5],
            color=DEODAR, linewidth=2, zorder=3)

    # Railing
    ax.plot([bridge_x1, bridge_x2], [bridge_y + 4, bridge_y + 4],
            color=DEODAR, linewidth=1.2, zorder=4)
    for px in np.linspace(bridge_x1 + 2, bridge_x2 - 2, 8):
        ax.plot([px, px], [bridge_y + 1.5, bridge_y + 4],
                color=DEODAR, linewidth=0.8, zorder=4)

    # --- Thread Walker figure (on bridge, walking right) ---
    tw_x = 55
    tw_y = bridge_y + 1.5
    # Body — simple ink sketch style
    # Head
    ax.plot(tw_x, tw_y + 6.5, "o", color=INK, markersize=6, zorder=6)
    # Body
    ax.plot([tw_x, tw_x], [tw_y + 2, tw_y + 5.5], color=INK, linewidth=1.8, zorder=6)
    # Legs (walking)
    ax.plot([tw_x, tw_x + 1], [tw_y + 2, tw_y], color=INK, linewidth=1.5, zorder=6)
    ax.plot([tw_x, tw_x - 0.8], [tw_y + 2, tw_y], color=INK, linewidth=1.5, zorder=6)
    # Arms
    ax.plot([tw_x, tw_x + 1.5], [tw_y + 4.5, tw_y + 3], color=INK, linewidth=1.2, zorder=6)
    ax.plot([tw_x, tw_x - 1.2], [tw_y + 4.5, tw_y + 3.5], color=INK, linewidth=1.2, zorder=6)
    # Satchel (heavy!)
    satchel = FancyBboxPatch((tw_x - 2.5, tw_y + 2.5), 2, 3,
                             boxstyle="round,pad=0.2",
                             facecolor=DEODAR, edgecolor=DEODAR,
                             linewidth=1, zorder=5, alpha=0.7)
    ax.add_patch(satchel)

    # --- Sangla village behind (left bank) ---
    # Simple house shapes
    for hx, hy, hw, hh in [(15, 36, 4, 5), (22, 37, 3, 4),
                             (28, 35, 5, 6), (10, 38, 3, 3)]:
        ax.add_patch(Rectangle((hx, hy), hw, hh, facecolor=SHADOW,
                                edgecolor=INK_LIGHT, linewidth=0.8, zorder=3))
        # Roof
        ax.plot([hx - 0.5, hx + hw/2, hx + hw + 0.5],
                [hy + hh, hy + hh + 2, hy + hh],
                color=DEODAR, linewidth=1.2, zorder=3)

    ax.text(20, 50, "S A N G L A", ha="center", fontsize=10, color=INK_LIGHT,
            fontfamily="serif", zorder=3)
    ax.text(20, 47, "2680m", ha="center", fontsize=8, fontstyle="italic",
            color=INK_FAINT, fontfamily="serif", zorder=3)

    # --- Trail going up-right (beyond bridge) ---
    trail_x = np.array([65, 72, 78, 85, 92, 97])
    trail_y = np.array([33, 38, 44, 50, 57, 62])
    ax.plot(trail_x, trail_y, color=INK_FAINT, linewidth=1.5,
            linestyle="--", zorder=2)
    ax.text(90, 64, "→ Chitkul\n→ Baspa La", ha="center", fontsize=8,
            fontstyle="italic", color=INK_LIGHT, fontfamily="serif")

    # --- Apple orchard (left bank, terraces) ---
    for tx in range(8, 30, 3):
        for ty in range(42, 56, 4):
            if rng.random() > 0.3:
                # Simple tree: trunk + canopy
                ax.plot([tx, tx], [ty, ty + 1.5], color=DEODAR,
                        linewidth=0.6, zorder=2)
                ax.plot(tx, ty + 2, "o", color=SAGE, markersize=3,
                        alpha=0.5, zorder=2)

    # Light rays from east (right side)
    for i in range(5):
        ray_y = 80 + i * 3
        ax.plot([92, 100], [ray_y - 2, ray_y], color="#F0E8D0",
                linewidth=8, alpha=0.15, zorder=0)

    attribution(ax, "His satchel is heavy. Seven instruments, each in its waxed wrapping.")
    save(fig, "departure")


# ── Image 6: Standing Card ─────────────────────────────────────────

def standing_card():
    """
    The standing card, alone on a loom frame. Handwritten text.
    Worn edges. Unsigned.
    """
    fig, ax = make_fig(9, 12)  # Portrait orientation for this one
    add_parchment_texture(ax, seed=89)

    # No title block — the card IS the image

    # Loom frame (background, just two horizontal beams)
    ax.add_patch(FancyBboxPatch((10, 10), 80, 4, boxstyle="round,pad=0.2",
                                facecolor=DEODAR_LIGHT, edgecolor=DEODAR,
                                linewidth=2, zorder=1, alpha=0.4))
    ax.add_patch(FancyBboxPatch((10, 86), 80, 4, boxstyle="round,pad=0.2",
                                facecolor=DEODAR_LIGHT, edgecolor=DEODAR,
                                linewidth=2, zorder=1, alpha=0.4))

    # Warp threads (vertical, faint)
    for i in range(20):
        tx = 15 + i * 3.5
        ax.plot([tx, tx], [14, 86], color=INK_FAINT, linewidth=0.5,
                alpha=0.3, zorder=1)

    # The standing card itself — center, slightly worn
    card_x, card_y = 22, 25
    card_w, card_h = 56, 50

    # Shadow
    ax.add_patch(FancyBboxPatch((card_x + 0.8, card_y - 0.8), card_w, card_h,
                                boxstyle="round,pad=0.5",
                                facecolor=SHADOW, edgecolor="none",
                                zorder=2, alpha=0.4))
    # Card body
    card = FancyBboxPatch((card_x, card_y), card_w, card_h,
                          boxstyle="round,pad=0.5",
                          facecolor="#FAF6EE", edgecolor=INK_LIGHT,
                          linewidth=1.5, zorder=3)
    ax.add_patch(card)

    # Worn edges — small irregular marks
    rng = np.random.default_rng(89)
    for _ in range(15):
        ex = card_x + rng.choice([0, card_w]) + rng.normal(0, 0.5)
        ey = card_y + rng.uniform(0, card_h)
        ax.plot(ex, ey, ".", color=INK_FAINT, markersize=rng.uniform(2, 5),
                alpha=0.4, zorder=4)

    # "Handwritten" text on the card
    card_text = [
        "Inspect the archive.",
        "Describe what you find.",
        "",
        "Incorporate only if in order.",
        "",
        "Check the incoming tray.",
        "",
        "",
        "A measurement that includes",
        "a correction is two operations",
        "pretending to be one,",
        "and the pretence will not",
        "survive the crossing.",
    ]

    text_y = card_y + card_h - 6
    for i, line in enumerate(card_text):
        if line:
            # Slight wobble in x position to simulate handwriting
            wobble_x = card_x + 5 + rng.normal(0, 0.3)
            ax.text(wobble_x, text_y, line,
                    fontsize=10, fontstyle="italic", color=INK,
                    fontfamily="serif", zorder=5,
                    alpha=0.85 + rng.uniform(-0.05, 0.05))
        text_y -= 3.2

    # No signature — deliberately
    # Small annotation outside the card
    ax.text(50, 18, "unsigned", ha="center", fontsize=8,
            fontstyle="italic", color=INK_FAINT, fontfamily="serif")

    # Title at top (outside the loom frame)
    ax.text(50, 95, "The Standing Card", ha="center", fontsize=16,
            fontweight="bold", color=INK, fontfamily="serif")
    ax.text(50, 92, "placed on every loom frame in the network",
            ha="center", fontsize=9, fontstyle="italic",
            color=INK_LIGHT, fontfamily="serif")

    attribution(ax, "The card does not operate the loom. "
                "The card shapes the weaver's attention.")
    save(fig, "standing-card")


# ── TODO(human): Valley-specific visual detail ─────────────────────
# Each image uses a consistent earth-tone palette. But the story
# emphasises that conditions vary by valley — light, humidity,
# altitude change everything. The function below controls how
# valley-specific environmental variation is rendered across all
# images. Currently it returns fixed values.
#
# TODO(human): Implement valley_atmosphere() to return a dict of
# visual modifiers based on altitude. See guidance below the function.

def valley_atmosphere(altitude_m: float) -> dict:
    """
    Return visual modifiers for a given altitude.

    Parameters
    ----------
    altitude_m : float
        Elevation in metres (e.g. 2680 for Sangla, 4000+ for passes).

    Returns
    -------
    dict with keys:
        "bg_alpha"    : float  — parchment stain intensity (0.0–0.5)
        "ink_alpha"   : float  — ink line opacity (0.5–1.0)
        "snow_frac"   : float  — fraction of ridge above snowline (0.0–1.0)
        "grain_count" : int    — number of wood-grain lines (3–12)
    """
    # Placeholder — returns fixed values regardless of altitude
    return {
        "bg_alpha": 0.35,
        "ink_alpha": 0.75,
        "snow_frac": 0.4,
        "grain_count": 10,
    }


# ── Main ────────────────────────────────────────────────────────────

def main():
    print(f"Generating images in {OUT}/\n")
    workshop_bench()
    seven_instruments()
    calibration_test()
    two_brackets()
    departure()
    standing_card()
    print(f"\nDone — 6 images generated.")

if __name__ == "__main__":
    main()
