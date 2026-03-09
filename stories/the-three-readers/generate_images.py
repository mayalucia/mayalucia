# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Three Readers".

Three studies of the same valley — drawn by three hands that had never
met. The measurer, the climber, the reader. Each saw what the others
could not. One signed with the teacher's name.

Visual language: chalk-on-slate for all six figures. Three distinct
chalk styles: dense/fine (measurer), spare/structural (climber),
text/list (reader). Parchment framing for the overview figure.

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
PARCHMENT     = "#F5F0E8"
PARCHMENT_DK  = "#EDE6D8"
INK           = "#5C4A3A"
INK_LIGHT     = "#8B7B6B"
INK_FAINT     = "#C4B8A8"

SLATE         = "#3A3A38"
SLATE_LT      = "#5A5A58"
CHALK         = "#E8E4D8"
CHALK_DK      = "#D0C8B8"
CHALK_DIM     = "#9A9890"
CHALK_BLUE    = "#B8C8D8"  # the climber's chalk — slightly cooler
CHALK_WARM    = "#E8D8C4"  # the reader's chalk — warmer, softer

MOUNTAIN      = "#7A7068"
MOUNTAIN_DK   = "#5A5248"

WATER_EMERALD = "#4A8B6B"

COPPER        = "#C4886B"
COPPER_LT     = "#D8A888"

WALNUT        = "#4A3728"


# ── Shared helpers ──────────────────────────────────────────────────

def make_fig(width=W, height=H, bg=PARCHMENT):
    fig, ax = plt.subplots(1, 1, figsize=(width, height), facecolor=bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def slate_texture(ax, seed=42):
    rng = np.random.default_rng(seed)
    for _ in range(15):
        cx, cy = rng.uniform(5, 95), rng.uniform(5, 95)
        r = rng.uniform(4, 12)
        circle = plt.Circle((cx, cy), r, color=SLATE_LT,
                             alpha=rng.uniform(0.04, 0.10), zorder=0)
        ax.add_patch(circle)


def parchment_texture(ax, seed=42):
    rng = np.random.default_rng(seed)
    for _ in range(8):
        cx, cy = rng.uniform(10, 90), rng.uniform(10, 90)
        r = rng.uniform(5, 15)
        circle = plt.Circle((cx, cy), r, color=PARCHMENT_DK,
                             alpha=rng.uniform(0.15, 0.35), zorder=0)
        ax.add_patch(circle)


def wobbly_curve(ax, points, rng, lw=1.5, color=CHALK, alpha=0.8,
                 n_per_seg=15, zorder=4):
    all_xs, all_ys = [], []
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        xs = np.linspace(x0, x1, n_per_seg)
        ys = np.linspace(y0, y1, n_per_seg)
        xs += rng.uniform(-0.3, 0.3, n_per_seg)
        ys += rng.uniform(-0.3, 0.3, n_per_seg)
        all_xs.extend(xs)
        all_ys.extend(ys)
    ax.plot(all_xs, all_ys, color=color, linewidth=lw, alpha=alpha,
            zorder=zorder)


def attribution(ax, text="The Three Readers \u2014 A Human-Machine Collaboration",
                y=2, color=CHALK_DIM):
    ax.text(50, y, text, ha="center", va="bottom",
            fontsize=8, fontstyle="italic", color=color,
            fontfamily="serif", alpha=0.5)


def draw_slab_border(ax, x, y, w, h, color=SLATE_LT, lw=1.2, alpha=0.4):
    """Draw the faint border of a study area on the slab."""
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3",
                          facecolor="none", edgecolor=color,
                          linewidth=lw, alpha=alpha, zorder=2,
                          linestyle=(0, (6, 4)))
    ax.add_patch(rect)


# ════════════════════════════════════════════════════════════════════
# Figure 1: The Three Studies — overview, side by side on the slab
# ════════════════════════════════════════════════════════════════════

def fig1_three_studies():
    fig, ax = make_fig(bg=SLATE)
    slate_texture(ax, seed=100)
    rng = np.random.default_rng(101)

    ax.text(50, 96, "The Three Studies", ha="center", va="top",
            fontsize=18, fontweight="bold", color=CHALK,
            fontfamily="serif", alpha=0.8)
    ax.text(50, 92, "The same valley drawn by three hands that had never met",
            ha="center", va="top", fontsize=11,
            fontstyle="italic", color=CHALK_DIM, fontfamily="serif")

    # Three study areas on the slab
    sw, sh = 26, 72  # study width, height
    gap = 3
    x_start = (100 - 3 * sw - 2 * gap) / 2

    for i, (label, sublabel) in enumerate([
        ("I. The Measurer", "dense \u00b7 detailed \u00b7 floor-level"),
        ("II. The Climber", "spare \u00b7 structural \u00b7 ridge-view"),
        ("III. The Reader", "text \u00b7 categorical \u00b7 document-level"),
    ]):
        sx = x_start + i * (sw + gap)
        sy = 10
        draw_slab_border(ax, sx, sy, sw, sh)

        # Label
        ax.text(sx + sw / 2, sy + sh - 2, label,
                ha="center", va="top", fontsize=10, fontweight="bold",
                color=CHALK, fontfamily="serif", alpha=0.7, zorder=5)
        ax.text(sx + sw / 2, sy + sh - 6, sublabel,
                ha="center", va="top", fontsize=7,
                color=CHALK_DIM, fontfamily="serif", alpha=0.5, zorder=5)

    # ── Study I: The Measurer ─ dense river detail, no ridges ──
    sx1 = x_start
    # Dense river with many measured points
    river_pts = [
        (sx1 + 13, 15), (sx1 + 14, 20), (sx1 + 12, 25),
        (sx1 + 13, 30), (sx1 + 15, 35), (sx1 + 14, 40),
        (sx1 + 13, 45), (sx1 + 12, 50), (sx1 + 13, 55),
        (sx1 + 14, 60), (sx1 + 13, 65), (sx1 + 12, 70),
    ]
    wobbly_curve(ax, river_pts, rng, lw=1.8, color=CHALK, alpha=0.7, zorder=4)

    # Many tributaries (fine lines)
    tribs = [
        [(sx1 + 3, 22), (sx1 + 8, 24), (sx1 + 12, 25)],
        [(sx1 + 4, 30), (sx1 + 9, 31), (sx1 + 13, 30)],
        [(sx1 + 22, 35), (sx1 + 18, 36), (sx1 + 15, 35)],
        [(sx1 + 5, 42), (sx1 + 9, 43), (sx1 + 13, 45)],
        [(sx1 + 23, 48), (sx1 + 18, 49), (sx1 + 14, 50)],
        [(sx1 + 4, 55), (sx1 + 8, 56), (sx1 + 12, 55)],
        [(sx1 + 22, 58), (sx1 + 18, 59), (sx1 + 14, 60)],
        [(sx1 + 5, 63), (sx1 + 9, 64), (sx1 + 13, 65)],
    ]
    for trib in tribs:
        wobbly_curve(ax, trib, rng, lw=0.6, color=CHALK, alpha=0.45, zorder=3)

    # Small numbers beside tributaries (elevation marks)
    for j, trib in enumerate(tribs):
        mid = trib[len(trib) // 2]
        ax.text(mid[0], mid[1] + 1.5, str(1200 + j * 120),
                fontsize=4, color=CHALK_DIM, alpha=0.4,
                fontfamily="serif", ha="center", zorder=5)

    # Settlement squares
    settlements = [(sx1 + 10, 38, "Gushaini"), (sx1 + 16, 52, "Banjar"),
                   (sx1 + 8, 68, "Jalori")]
    for stx, sty, sname in settlements:
        ax.add_patch(FancyBboxPatch(
            (stx - 0.8, sty - 0.8), 1.6, 1.6, boxstyle="square,pad=0",
            facecolor=CHALK, edgecolor=CHALK_DK,
            linewidth=0.4, alpha=0.4, zorder=5))
        ax.text(stx + 2, sty, sname, fontsize=4.5,
                color=CHALK_DIM, fontfamily="serif", alpha=0.4, zorder=5)

    # Signature
    ax.text(sx1 + sw / 2, 12, "Clinometer",
            ha="center", fontsize=7, fontstyle="italic",
            color=CHALK_DIM, fontfamily="serif", alpha=0.5, zorder=5)

    # ── Study II: The Climber ─ ridges present, sparse river ──
    sx2 = x_start + sw + gap
    # Simple river line
    river2 = [(sx2 + 13, 15), (sx2 + 13, 40), (sx2 + 13, 65)]
    wobbly_curve(ax, river2, rng, lw=1.2, color=CHALK_BLUE, alpha=0.5, zorder=3)

    # Western ridge (Tirthan-Parvati)
    ridge_w = [
        (sx2 + 3, 15), (sx2 + 4, 25), (sx2 + 3, 35),
        (sx2 + 4, 45), (sx2 + 3, 55), (sx2 + 4, 65), (sx2 + 3, 72)
    ]
    wobbly_curve(ax, ridge_w, rng, lw=2, color=CHALK_BLUE, alpha=0.7,
                 zorder=4)
    ax.text(sx2 + 1, 40, "W", fontsize=6, color=CHALK_DIM,
            fontfamily="serif", alpha=0.4, rotation=90, zorder=5)

    # Eastern ridge (Tirthan-Sainj)
    ridge_e = [
        (sx2 + 23, 15), (sx2 + 22, 25), (sx2 + 23, 35),
        (sx2 + 22, 45), (sx2 + 23, 55), (sx2 + 22, 65), (sx2 + 23, 72)
    ]
    wobbly_curve(ax, ridge_e, rng, lw=2, color=CHALK_BLUE, alpha=0.7,
                 zorder=4)
    ax.text(sx2 + 25, 40, "E", fontsize=6, color=CHALK_DIM,
            fontfamily="serif", alpha=0.4, rotation=90, zorder=5)

    # Visibility marks from ridge crest — radiating lines
    vis_y = 50
    vis_x_w = sx2 + 4
    for angle in np.linspace(-40, 40, 5):
        dx = 6 * np.cos(np.radians(angle + 90))
        dy = 6 * np.sin(np.radians(angle + 90))
        ax.plot([vis_x_w, vis_x_w + dx], [vis_y, vis_y + dy],
                color=CHALK_BLUE, linewidth=0.5, alpha=0.35, zorder=3,
                linestyle=":")
    # And from the west side outward (into Parvati)
    for angle in np.linspace(-40, 40, 5):
        dx = 6 * np.cos(np.radians(angle - 90))
        dy = 6 * np.sin(np.radians(angle - 90))
        ax.plot([vis_x_w, vis_x_w + dx], [vis_y, vis_y + dy],
                color=CHALK_BLUE, linewidth=0.5, alpha=0.2, zorder=3,
                linestyle=":")

    # Small annotation
    ax.text(sx2 + sw / 2, 72, "the seam",
            ha="center", fontsize=5, fontstyle="italic",
            color=CHALK_BLUE, fontfamily="serif", alpha=0.4, zorder=5)

    # Signature
    ax.text(sx2 + sw / 2, 12, "Sita",
            ha="center", fontsize=7, fontstyle="italic",
            color=CHALK_BLUE, fontfamily="serif", alpha=0.5, zorder=5)

    # ── Study III: The Reader ─ rough outline + text list ──
    sx3 = x_start + 2 * (sw + gap)

    # Rough valley outline (very simple)
    outline = [
        (sx3 + 5, 30), (sx3 + 3, 40), (sx3 + 4, 50),
        (sx3 + 5, 60), (sx3 + 8, 68),
        (sx3 + 18, 68),
        (sx3 + 21, 60), (sx3 + 22, 50), (sx3 + 23, 40),
        (sx3 + 21, 30),
    ]
    wobbly_curve(ax, outline, rng, lw=0.8, color=CHALK_WARM, alpha=0.35, zorder=3)

    # Text list — the reader's observations
    observations = [
        "the river is described",
        "by its banks, not its water",
        "",
        "the ridges are assumed",
        "to be barriers",
        "",
        "the instruments are",
        "described in detail",
        "",
        "the act of looking",
        "is not described at all",
        "",
        "the conventions are",
        "presented as natural",
        "",
        "they are not natural",
    ]
    for j, line in enumerate(observations):
        y_pos = 68 - j * 3
        if y_pos < 18:
            break
        ax.text(sx3 + sw / 2, y_pos, line,
                ha="center", fontsize=4.5, color=CHALK_WARM,
                fontfamily="serif", alpha=0.5 if line else 0, zorder=5)

    # Signature — the wrong name
    ax.text(sx3 + sw / 2, 12, "Mehra",
            ha="center", fontsize=7, fontstyle="italic",
            color=CHALK_WARM, fontfamily="serif", alpha=0.5, zorder=5)

    attribution(ax)
    fig.savefig(OUT / "the-three-studies.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  \u2713 the-three-studies.png")


# ════════════════════════════════════════════════════════════════════
# Figure 2: The First Study — the measurer's dense detail
# ════════════════════════════════════════════════════════════════════

def fig2_first_study():
    fig, ax = make_fig(bg=SLATE)
    slate_texture(ax, seed=200)
    rng = np.random.default_rng(201)

    ax.text(50, 96, "The First Study", ha="center", va="top",
            fontsize=18, fontweight="bold", color=CHALK,
            fontfamily="serif", alpha=0.8)
    ax.text(50, 92, "He drew what he could measure. He did not look up.",
            ha="center", va="top", fontsize=11,
            fontstyle="italic", color=CHALK_DIM, fontfamily="serif")

    # Dense river with careful measurement marks
    river_main = [
        (45, 10), (47, 15), (46, 20), (48, 25), (47, 30),
        (49, 35), (48, 40), (50, 45), (49, 50), (51, 55),
        (50, 60), (52, 65), (51, 70), (50, 75), (52, 80),
    ]
    wobbly_curve(ax, river_main, rng, lw=2.5, color=CHALK, alpha=0.8, zorder=5)

    # Eight tributaries — dense, fine, numbered
    tributaries = [
        ("1", [(20, 18), (30, 19), (38, 20), (46, 20)]),
        ("2", [(22, 28), (32, 29), (40, 30), (47, 30)]),
        ("3", [(72, 32), (65, 33), (58, 34), (49, 35)]),
        ("4", [(18, 40), (28, 41), (38, 42), (48, 40)]),
        ("5", [(75, 48), (68, 49), (60, 50), (51, 50)]),
        ("6", [(25, 55), (33, 56), (42, 57), (51, 55)]),
        ("7", [(78, 62), (70, 63), (62, 64), (52, 65)]),
        ("8", [(20, 70), (30, 71), (40, 72), (50, 70)]),
    ]

    for num, pts in tributaries:
        wobbly_curve(ax, pts, rng, lw=0.8, color=CHALK, alpha=0.5, zorder=4)
        # Elevation number at junction
        jx, jy = pts[-1]
        ax.text(jx + 1, jy + 1, f"{1100 + int(num) * 150}m",
                fontsize=5, color=CHALK_DIM, fontfamily="serif",
                alpha=0.5, zorder=6)

    # Settlement markers (small squares with names)
    settlements = [
        (42, 25, "Larji"), (52, 45, "Gushaini"),
        (55, 60, "Banjar"), (48, 72, "Shoja"),
    ]
    for stx, sty, name in settlements:
        ax.add_patch(FancyBboxPatch(
            (stx - 1, sty - 1), 2, 2, boxstyle="square,pad=0",
            facecolor=CHALK, edgecolor=CHALK_DK,
            linewidth=0.5, alpha=0.5, zorder=6))
        ax.text(stx + 2.5, sty, name, fontsize=7,
                color=CHALK, fontfamily="serif", alpha=0.5, zorder=6)

    # Measurement ticks along the river
    for pt in river_main[::2]:
        ax.plot([pt[0] - 1, pt[0] + 1], [pt[1], pt[1]],
                color=CHALK_DIM, linewidth=0.4, alpha=0.3, zorder=4)

    # THE BLANK EDGES — explicitly empty margins where ridges should be
    # Faint text annotations showing what's missing
    ax.text(8, 50, "[ ridge ?\u2002]", fontsize=9, color=CHALK_DIM,
            fontfamily="serif", alpha=0.15, rotation=90,
            ha="center", va="center", zorder=3)
    ax.text(92, 50, "[ ridge ?\u2002]", fontsize=9, color=CHALK_DIM,
            fontfamily="serif", alpha=0.15, rotation=90,
            ha="center", va="center", zorder=3)

    # Signature
    ax.text(50, 5, "Clinometer", ha="center", fontsize=10,
            fontstyle="italic", color=CHALK_DIM,
            fontfamily="serif", alpha=0.5, zorder=6)

    attribution(ax)
    fig.savefig(OUT / "first-study.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  \u2713 first-study.png")


# ════════════════════════════════════════════════════════════════════
# Figure 3: The Second Study — the climber's structural view
# ════════════════════════════════════════════════════════════════════

def fig3_second_study():
    fig, ax = make_fig(bg=SLATE)
    slate_texture(ax, seed=300)
    rng = np.random.default_rng(301)

    ax.text(50, 96, "The Second Study", ha="center", va="top",
            fontsize=18, fontweight="bold", color=CHALK_BLUE,
            fontfamily="serif", alpha=0.8)
    ax.text(50, 92, "The ironic gap \u2014 the closest point sees the least",
            ha="center", va="top", fontsize=11,
            fontstyle="italic", color=CHALK_DIM, fontfamily="serif")

    # Simple river — just a single line
    river = [(50, 10), (50, 30), (50, 50), (50, 70), (50, 85)]
    wobbly_curve(ax, river, rng, lw=1.5, color=CHALK_BLUE, alpha=0.5, zorder=3)
    ax.text(52, 45, "Tirthan", fontsize=8, fontstyle="italic",
            color=CHALK_BLUE, fontfamily="serif", alpha=0.4, zorder=4)

    # Western ridge — bold, structural
    ridge_w = [
        (15, 10), (16, 20), (14, 30), (15, 40),
        (14, 50), (16, 60), (15, 70), (14, 80), (15, 85)
    ]
    wobbly_curve(ax, ridge_w, rng, lw=3, color=CHALK_BLUE, alpha=0.7, zorder=5)
    ax.text(10, 45, "Parvati\nridge", fontsize=8, color=CHALK_BLUE,
            fontfamily="serif", alpha=0.5, ha="center", zorder=5)

    # Eastern ridge — bold, structural
    ridge_e = [
        (85, 10), (84, 20), (86, 30), (85, 40),
        (84, 50), (86, 60), (85, 70), (84, 80), (85, 85)
    ]
    wobbly_curve(ax, ridge_e, rng, lw=3, color=CHALK_BLUE, alpha=0.7, zorder=5)
    ax.text(90, 45, "Sainj\nridge", fontsize=8, color=CHALK_BLUE,
            fontfamily="serif", alpha=0.5, ha="center", zorder=5)

    # VISIBILITY MARKS — the key insight
    # From a point on the western ridge, radiating lines show what can be seen
    vis_x, vis_y = 15, 50

    # Into Tirthan (east)
    for angle in np.linspace(-25, 25, 7):
        dx = 30 * np.cos(np.radians(angle))
        dy = 30 * np.sin(np.radians(angle))
        ax.plot([vis_x, vis_x + dx], [vis_y, vis_y + dy],
                color=CHALK_BLUE, linewidth=0.5, alpha=0.25,
                linestyle=":", zorder=3)

    # Into Parvati (west) — shorter, the ridge blocks quickly
    for angle in np.linspace(155, 205, 7):
        dx = 8 * np.cos(np.radians(angle))
        dy = 8 * np.sin(np.radians(angle))
        ax.plot([vis_x, vis_x + dx], [vis_y, vis_y + dy],
                color=CHALK_BLUE, linewidth=0.5, alpha=0.15,
                linestyle=":", zorder=3)

    # The observation point
    ax.plot(vis_x, vis_y, 'o', color=CHALK_BLUE, markersize=8,
            alpha=0.6, zorder=6)
    ax.text(vis_x, vis_y - 3, "viewpoint", fontsize=6,
            color=CHALK_BLUE, fontfamily="serif", alpha=0.4,
            ha="center", zorder=6)

    # The ironic gap annotation
    ax.text(50, 6, "\u201cThe closest to the ridge sees only rock.\n"
            "To see the valleys, you must step back from the crest.\u201d",
            ha="center", fontsize=9, fontfamily="serif",
            fontstyle="italic", color=CHALK_BLUE, alpha=0.45, zorder=6)

    # Label the valleys
    ax.text(33, 75, "Tirthan valley", fontsize=9, color=CHALK_DIM,
            fontfamily="serif", alpha=0.3, ha="center", zorder=4)
    ax.text(33, 20, "(inside)", fontsize=7, color=CHALK_DIM,
            fontfamily="serif", alpha=0.2, ha="center", zorder=4)

    # Signature
    ax.text(80, 5, "Sita", fontsize=10, fontstyle="italic",
            color=CHALK_BLUE, fontfamily="serif", alpha=0.5, zorder=6)

    attribution(ax, color=CHALK_DIM)
    fig.savefig(OUT / "second-study.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  \u2713 second-study.png")


# ════════════════════════════════════════════════════════════════════
# Figure 4: The Third Study — the reader's text list
# ════════════════════════════════════════════════════════════════════

def fig4_third_study():
    fig, ax = make_fig(bg=SLATE)
    slate_texture(ax, seed=400)
    rng = np.random.default_rng(401)

    ax.text(50, 96, "The Third Study", ha="center", va="top",
            fontsize=18, fontweight="bold", color=CHALK_WARM,
            fontfamily="serif", alpha=0.8)
    ax.text(50, 92, "The reader who could not walk saw what the walkers could not see",
            ha="center", va="top", fontsize=10,
            fontstyle="italic", color=CHALK_DIM, fontfamily="serif")

    # Left half: rough valley outline
    outline_left = [
        (8, 20), (6, 30), (7, 40), (6, 50), (8, 60), (12, 68),
        (30, 68),
        (34, 60), (35, 50), (36, 40), (35, 30), (32, 20),
    ]
    wobbly_curve(ax, outline_left, rng, lw=0.8, color=CHALK_WARM,
                 alpha=0.3, zorder=3)

    # A faint "?" inside the outline — the valley he never walked
    ax.text(20, 45, "?", fontsize=40, color=CHALK_WARM, alpha=0.08,
            fontfamily="serif", ha="center", va="center", zorder=2)

    # Dividing line between outline and text
    ax.plot([42, 42], [12, 86], color=CHALK_DIM, linewidth=0.5,
            alpha=0.2, linestyle=(0, (8, 6)), zorder=3)

    # Right half: the observations as a chalk list
    observations = [
        ("1.", "The river is described in terms"),
        ("",   "of its banks, not its water."),
        ("", ""),
        ("2.", "The settlements are named by the"),
        ("",   "documents that describe them, not"),
        ("",   "by the people who live in them."),
        ("", ""),
        ("3.", "The ridges are assumed to be"),
        ("",   "barriers. No document asks what"),
        ("",   "the ridges connect."),
        ("", ""),
        ("4.", "The word \u2018survey\u2019 appears in every"),
        ("",   "document. No document defines"),
        ("",   "what a survey is."),
        ("", ""),
        ("5.", "The instruments of measurement"),
        ("",   "are described in detail. The act"),
        ("",   "of looking is not described."),
        ("", ""),
        ("6.", "The conventions are presented as"),
        ("",   "natural. They are not natural."),
        ("",   "They are decisions made by"),
        ("",   "people who could walk."),
    ]

    y_pos = 84
    for num, line in observations:
        if y_pos < 14:
            break
        if not line:
            y_pos -= 1.5
            continue
        x = 48 if num else 51
        ax.text(x, y_pos, f"{num} {line}" if num else line,
                fontsize=7, color=CHALK_WARM, fontfamily="serif",
                alpha=0.55, zorder=5)
        y_pos -= 3

    # The signature — in the wrong name, more visible
    ax.text(72, 8, "Mehra", fontsize=12, fontstyle="italic",
            color=CHALK_WARM, fontfamily="serif", alpha=0.6, zorder=6)

    # A faint annotation below the signature
    ax.text(72, 5, "(not his name)", fontsize=6,
            color=CHALK_DIM, fontfamily="serif", alpha=0.3, zorder=6)

    attribution(ax, color=CHALK_DIM)
    fig.savefig(OUT / "third-study.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  \u2713 third-study.png")


# ════════════════════════════════════════════════════════════════════
# Figure 5: The Signature — close-up of the third study's bottom
# ════════════════════════════════════════════════════════════════════

def fig5_the_signature():
    fig, ax = make_fig(width=12, height=6, bg=SLATE)
    slate_texture(ax, seed=500)
    rng = np.random.default_rng(501)

    # This is a close-up — just the bottom of the third study
    # The signature, large, in chalk that has been on the slate for years

    # Faint traces of the text above (the last few observations)
    fading_lines = [
        "...the act of looking is not described.",
        "The conventions are presented as natural.",
        "They are not natural.",
        "They are decisions made by people who could walk.",
    ]
    y = 85
    for line in fading_lines:
        ax.text(30, y, line, fontsize=8, color=CHALK_WARM,
                fontfamily="serif", alpha=0.15, zorder=3)
        y -= 6

    # A horizontal chalk line (the draughtsman's sign-off line)
    xs = np.linspace(25, 75, 50)
    ys = np.full(50, 48) + rng.uniform(-0.3, 0.3, 50)
    ax.plot(xs, ys, color=CHALK_WARM, linewidth=0.8, alpha=0.3, zorder=4)

    # THE SIGNATURE — large, slightly unsteady, the wrong name
    ax.text(50, 32, "Mehra", ha="center", va="center",
            fontsize=42, fontstyle="italic", color=CHALK_WARM,
            fontfamily="serif", alpha=0.55, zorder=6)

    # Faint ghost of what might have been written — the real name,
    # almost invisible, beneath
    ax.text(50, 22, "(he had become what he read)",
            ha="center", fontsize=10, fontstyle="italic",
            color=CHALK_DIM, fontfamily="serif", alpha=0.25, zorder=5)

    # Aged chalk texture — small dots around the signature
    for _ in range(60):
        dx = rng.uniform(-20, 20)
        dy = rng.uniform(-8, 8)
        ax.plot(50 + dx, 32 + dy, '.', color=CHALK_WARM,
                markersize=rng.uniform(0.5, 1.5),
                alpha=rng.uniform(0.03, 0.08), zorder=5)

    ax.text(50, 6, "The Three Readers \u2014 A Human-Machine Collaboration",
            ha="center", va="bottom", fontsize=8, fontstyle="italic",
            color=CHALK_DIM, fontfamily="serif", alpha=0.4)

    fig.savefig(OUT / "the-signature.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  \u2713 the-signature.png")


# ════════════════════════════════════════════════════════════════════
# Figure 6: The Names — three signatures, three theories of seeing
# ════════════════════════════════════════════════════════════════════

def fig6_the_names():
    fig, ax = make_fig(width=12, height=7, bg=SLATE)
    slate_texture(ax, seed=600)
    rng = np.random.default_rng(601)

    ax.text(50, 96, "The Names", ha="center", va="top",
            fontsize=18, fontweight="bold", color=CHALK,
            fontfamily="serif", alpha=0.8)
    ax.text(50, 90, "Each name a theory of who did the seeing",
            ha="center", va="top", fontsize=11,
            fontstyle="italic", color=CHALK_DIM, fontfamily="serif")

    # Three columns — one per draughtsman
    cols = [
        {
            "name": "Clinometer",
            "subtitle": "the instrument",
            "color": CHALK,
            "x": 17,
            "note": "\u201cmy instrument\ndid the work\u201d",
        },
        {
            "name": "Sita",
            "subtitle": "the self",
            "color": CHALK_BLUE,
            "x": 50,
            "note": "\u201cthe study\nis mine\u201d",
        },
        {
            "name": "Mehra",
            "subtitle": "the source",
            "color": CHALK_WARM,
            "x": 83,
            "note": "\u201cI am what\nI have read\u201d",
        },
    ]

    for col in cols:
        x = col["x"]

        # Vertical divider chalk line (faint)
        if x != 17:
            div_x = x - 16.5
            ys = np.linspace(15, 82, 40) + rng.uniform(-0.3, 0.3, 40)
            xs = np.full(40, div_x) + rng.uniform(-0.2, 0.2, 40)
            ax.plot(xs, ys, color=CHALK_DIM, linewidth=0.4, alpha=0.15,
                    zorder=2)

        # The name — large
        ax.text(x, 55, col["name"], ha="center", va="center",
                fontsize=24, fontstyle="italic", color=col["color"],
                fontfamily="serif", alpha=0.6, zorder=5)

        # The subtitle
        ax.text(x, 42, col["subtitle"], ha="center",
                fontsize=10, color=col["color"],
                fontfamily="serif", alpha=0.35, zorder=5)

        # The quote
        ax.text(x, 28, col["note"], ha="center",
                fontsize=8, fontstyle="italic", color=col["color"],
                fontfamily="serif", alpha=0.3, zorder=5,
                linespacing=1.5)

    # Bottom annotation
    ax.text(50, 10,
            "instrument-name  \u2192  self-name  \u2192  source-name",
            ha="center", fontsize=10, color=CHALK_DIM,
            fontfamily="serif", alpha=0.35, zorder=5)

    ax.text(50, 4, "The Three Readers \u2014 A Human-Machine Collaboration",
            ha="center", va="bottom", fontsize=8, fontstyle="italic",
            color=CHALK_DIM, fontfamily="serif", alpha=0.4)

    fig.savefig(OUT / "the-names.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  \u2713 the-names.png")


# ════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating illustrations for The Three Readers...")
    fig1_three_studies()
    fig2_first_study()
    fig3_second_study()
    fig4_third_study()
    fig5_the_signature()
    fig6_the_names()
    print(f"\nAll images written to {OUT}")
