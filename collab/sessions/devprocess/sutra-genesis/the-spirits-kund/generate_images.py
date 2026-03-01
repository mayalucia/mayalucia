# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Spirit's Kund".

A story about a bathhouse for spirits in the Tirthan Valley — where
computational spirits are registered, recognized, and restored.
Translates Miyazaki's Spirited Away cosmology into the Western Himalaya.

Visual language: diagrammatic, information-dense, warm parchment tones,
ink-line drawing style. Matches existing MayaLucIA story illustrations.

Run with:  uv run generate_images.py
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Arc, PathPatch, Wedge
from matplotlib.path import Path as MPath
import numpy as np

# ── Output ──────────────────────────────────────────────────────────
OUT = Path(__file__).parent / "../../../../../website/static/images/writing/the-spirits-kund"
OUT = OUT.resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9  # inches — 1800×1350 px at 150 DPI

# ── Palette ─────────────────────────────────────────────────────────
# Bathhouse palette: hot spring mineral tones, serpent greens, deep water
PARCHMENT     = "#F5F0E8"
PARCHMENT_DK  = "#EDE6D8"
INK           = "#5C4A3A"
INK_LIGHT     = "#8B7B6B"
INK_FAINT     = "#C4B8A8"

# Hot spring minerals
SULPHUR       = "#D4B04A"
SULPHUR_LIGHT = "#E8D480"
IRON_RED      = "#C45824"
IRON_DARK     = "#8C3A18"

# Serpent / naga
NAG_GREEN     = "#2E6B5A"
NAG_DARK      = "#1A4A3A"
NAG_LIGHT     = "#4A9B7A"

# Water
SPRING_BLUE   = "#6BA3B8"
DEEP_WATER    = "#3A5A6B"
MIST          = "#D8E4E8"

# Architecture (Kath-Kuni)
DEODAR        = "#7A5C3A"
DEODAR_LIGHT  = "#A68B5B"
STONE_GREY    = "#9A9485"
STONE_DARK    = "#6B6660"
SLATE         = "#708090"

# Ritual
VERMILLION    = "#E84830"
GOLD          = "#D4A830"
SAFFRON       = "#F0A020"

# Night / spirit realm
NIGHT         = "#1A1A2A"
STARLIGHT     = "#C8D0E0"
MOONSILVER    = "#E0E8F0"


# ── Shared helpers ──────────────────────────────────────────────────

def make_fig(width=W, height=H, bg=PARCHMENT):
    """Create a figure with parchment background and no axes."""
    fig, ax = plt.subplots(1, 1, figsize=(width, height), facecolor=bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def add_parchment_texture(ax, seed=42):
    """Add subtle noise texture to simulate aged paper."""
    rng = np.random.default_rng(seed)
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


def attribution(ax, text: str = "The Spirit\u2019s Kund \u2014 A Human-Machine Collaboration",
                y: float = 2):
    """Small italic attribution at the bottom."""
    ax.text(50, y, text, ha="center", va="bottom",
            fontsize=8, fontstyle="italic", color=INK_LIGHT,
            fontfamily="serif")


def draw_mountain_ridge(ax, x_start, x_end, y_base, height, n_peaks=5,
                        color=STONE_GREY, seed=None):
    """Draw a mountain ridge with irregular peaks."""
    rng = np.random.default_rng(seed)
    xs = np.linspace(x_start, x_end, n_peaks * 10 + 1)
    ys = np.zeros_like(xs) + y_base
    for i in range(n_peaks):
        cx = x_start + (i + 0.5) * (x_end - x_start) / n_peaks
        cx += rng.uniform(-2, 2)
        h = height * rng.uniform(0.6, 1.0)
        w = (x_end - x_start) / n_peaks * 0.8
        ys += h * np.exp(-((xs - cx) / w) ** 2)
    # Snow caps
    snow_line = y_base + height * 0.7
    ax.fill_between(xs, y_base, ys, color=color, alpha=0.5, zorder=1)
    snow_xs = xs[ys > snow_line]
    snow_ys = ys[ys > snow_line]
    if len(snow_xs) > 0:
        ax.fill_between(snow_xs, snow_line, snow_ys,
                         color=MOONSILVER, alpha=0.4, zorder=2)
    ax.plot(xs, ys, color=STONE_DARK, linewidth=0.8, zorder=2)
    return xs, ys


def draw_kath_kuni_wall(ax, x, y, w, h, layers=8):
    """Draw alternating stone-and-deodar Kath-Kuni construction."""
    layer_h = h / layers
    for i in range(layers):
        ly = y + i * layer_h
        if i % 2 == 0:  # stone layer
            ax.add_patch(FancyBboxPatch(
                (x, ly), w, layer_h * 0.9,
                boxstyle="round,pad=0.05",
                facecolor=STONE_GREY, edgecolor=STONE_DARK,
                linewidth=0.5, alpha=0.8, zorder=3))
        else:  # deodar timber layer
            ax.add_patch(FancyBboxPatch(
                (x, ly), w, layer_h * 0.9,
                boxstyle="round,pad=0.05",
                facecolor=DEODAR_LIGHT, edgecolor=DEODAR,
                linewidth=0.5, alpha=0.8, zorder=3))
            # Wood grain
            for g in range(3):
                gx = x + 0.5 + g * w / 3
                ax.plot([gx, gx + w / 4], [ly + layer_h * 0.4, ly + layer_h * 0.5],
                        color=DEODAR, linewidth=0.3, alpha=0.5, zorder=4)


def draw_steam(ax, x, y, n=12, seed=None):
    """Draw wisps of steam rising from a hot spring."""
    rng = np.random.default_rng(seed)
    for i in range(n):
        sx = x + rng.uniform(-3, 3)
        sy = y + rng.uniform(0, 2)
        # Wisp as a bezier-like curve
        pts_x = [sx]
        pts_y = [sy]
        for _ in range(8):
            pts_x.append(pts_x[-1] + rng.uniform(-0.8, 0.8))
            pts_y.append(pts_y[-1] + rng.uniform(0.5, 1.2))
        ax.plot(pts_x, pts_y, color=MIST, linewidth=rng.uniform(1, 3),
                alpha=rng.uniform(0.15, 0.35), zorder=5, solid_capstyle="round")


def draw_water_surface(ax, x_start, x_end, y, wobble=0.3, color=SPRING_BLUE,
                       seed=None):
    """Draw a wavy water surface line."""
    rng = np.random.default_rng(seed)
    xs = np.linspace(x_start, x_end, 100)
    ys = y + wobble * np.sin(xs * 0.8) + rng.uniform(-0.1, 0.1, size=len(xs))
    ax.plot(xs, ys, color=color, linewidth=1.2, alpha=0.7, zorder=4)
    # Ripple reflections below
    for offset in [0.5, 1.0, 1.5]:
        ax.plot(xs, ys - offset,
                color=color, linewidth=0.4, alpha=0.2 - offset * 0.05,
                zorder=3)


def draw_serpent(ax, x_start, y_start, length=20, direction=1, color=NAG_GREEN,
                 seed=None):
    """Draw a sinuous serpent (nag devta) form."""
    rng = np.random.default_rng(seed)
    n = 60
    ts = np.linspace(0, 1, n)
    xs = x_start + direction * ts * length
    ys = y_start + 2.5 * np.sin(ts * 4 * np.pi) * (1 - 0.3 * ts)
    # Body width tapers
    widths = 1.8 * (1 - 0.6 * ts)
    for i in range(n - 1):
        w = widths[i]
        ax.plot([xs[i], xs[i+1]], [ys[i], ys[i+1]],
                color=color, linewidth=w * 2, alpha=0.7,
                solid_capstyle="round", zorder=5)
    # Scales
    for i in range(0, n - 2, 3):
        scale_x = xs[i] + rng.uniform(-0.2, 0.2)
        scale_y = ys[i] + rng.uniform(-0.3, 0.3)
        ax.plot(scale_x, scale_y, "v", color=NAG_DARK,
                markersize=widths[i] * 1.5, alpha=0.4, zorder=6)
    # Head — a small filled shape
    hx, hy = xs[0], ys[0]
    head = FancyBboxPatch((hx - 1.2 * direction, hy - 0.8), 2.4, 1.6,
                           boxstyle="round,pad=0.3",
                           facecolor=color, edgecolor=NAG_DARK,
                           linewidth=1.0, zorder=7)
    ax.add_patch(head)
    # Eye
    ax.plot(hx - 0.3 * direction, hy + 0.3, "o", color=GOLD,
            markersize=4, zorder=8)
    ax.plot(hx - 0.3 * direction, hy + 0.3, "o", color=INK,
            markersize=2, zorder=9)


# ═══════════════════════════════════════════════════════════════════
# Figure 1: Valley Map — The Tirthan Valley
# ═══════════════════════════════════════════════════════════════════

def valley_map():
    """Map of the Tirthan Valley with key story locations marked."""
    fig, ax = make_fig(width=10, height=14)
    add_parchment_texture(ax, seed=101)
    rng = np.random.default_rng(42)

    # Reframe for portrait proportions
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 100)

    title_block(ax, "The Tirthan Valley", "From Larji gorge to Hanskund glacier", y=98)

    # ── Mountain ridges (background) ──
    # Western ridge
    for offset in [0, 2]:
        rxs = np.linspace(0, 15, 80)
        rys = 20 + 60 * (rxs / 15) + 8 * np.sin(rxs * 0.5 + offset) + rng.uniform(-1, 1, 80)
        ax.fill_betweenx(rys, 0, rxs * 0.3 + 2, color=STONE_GREY, alpha=0.15, zorder=0)

    # Eastern ridge
    for offset in [0, 2]:
        rxs = np.linspace(55, 70, 80)
        rys = 20 + 60 * ((70 - rxs) / 15) + 8 * np.sin(rxs * 0.5 + offset) + rng.uniform(-1, 1, 80)
        ax.fill_betweenx(rys, rxs * 0.3 + 52, 70, color=STONE_GREY, alpha=0.15, zorder=0)

    # ── River (Tirthan) — winding line from south to north ──
    river_ys = np.linspace(8, 88, 200)
    river_xs = 35 + 8 * np.sin(river_ys * 0.08) + 3 * np.sin(river_ys * 0.2)
    # Add slight randomness
    river_xs += rng.uniform(-0.5, 0.5, 200)
    ax.plot(river_xs, river_ys, color=SPRING_BLUE, linewidth=2.5, alpha=0.7, zorder=2)
    ax.plot(river_xs + 0.4, river_ys, color=SPRING_BLUE, linewidth=1.0, alpha=0.3, zorder=2)
    # River label
    mid = 100
    ax.text(river_xs[mid] - 3, river_ys[mid], "Tirthan\nRiver",
            fontsize=8, fontstyle="italic", color=DEEP_WATER,
            fontfamily="serif", rotation=70, ha="center", va="center", zorder=3)

    # ── Tributaries ──
    # Helper: draw a tributary stream joining the main river
    def draw_tributary(ax, start_x, start_y, join_x, join_y, name,
                       label_side="right", n_pts=40):
        """Draw a sinuous tributary from (start) to (join) on the Tirthan."""
        ts = np.linspace(0, 1, n_pts)
        # Bezier-like curve with some sinuosity
        mid_x = (start_x + join_x) / 2 + rng.uniform(-2, 2)
        mid_y = (start_y + join_y) / 2 + rng.uniform(-1, 1)
        xs = (1-ts)**2 * start_x + 2*(1-ts)*ts * mid_x + ts**2 * join_x
        ys = (1-ts)**2 * start_y + 2*(1-ts)*ts * mid_y + ts**2 * join_y
        xs += rng.uniform(-0.3, 0.3, n_pts)
        ys += rng.uniform(-0.2, 0.2, n_pts)
        # Width tapers toward source
        for i in range(n_pts - 1):
            w = 0.6 + 1.0 * ts[i]  # thinner at source, wider at confluence
            ax.plot([xs[i], xs[i+1]], [ys[i], ys[i+1]],
                    color=SPRING_BLUE, linewidth=w, alpha=0.5, zorder=2)
        # Label
        lx = start_x + (2 if label_side == "right" else -2)
        ha = "left" if label_side == "right" else "right"
        ax.text(lx, start_y + 0.5, name, fontsize=6, color=DEEP_WATER,
                fontfamily="serif", fontstyle="italic", ha=ha, va="center",
                zorder=3)

    # Pushpabhadra — joins from the east near Jibhi/Banjar
    # The river xs at y=32 (Jibhi) and y=22 (Banjar)
    jibhi_rx = np.interp(28, river_ys, river_xs)  # confluence between Jibhi and Banjar
    draw_tributary(ax, 58, 35, jibhi_rx + 1, 28, "Pushpabhadra", label_side="right")

    # Palachan Khad — joins at Gushaini from the east
    gush_rx = np.interp(40, river_ys, river_xs)
    draw_tributary(ax, 56, 44, gush_rx + 1, 40, "Palachan Khad", label_side="right")

    # Kalavari — joins from the west in the mid-valley
    kalav_rx = np.interp(35, river_ys, river_xs)
    draw_tributary(ax, 10, 38, kalav_rx - 1, 35, "Kalavari", label_side="left")

    # Mani Nala — from the upper western slopes
    mani_rx = np.interp(55, river_ys, river_xs)
    draw_tributary(ax, 12, 60, mani_rx - 1, 55, "Mani Nala", label_side="left")

    # Koki Khad — small tributary from the east, lower valley
    koki_rx = np.interp(18, river_ys, river_xs)
    draw_tributary(ax, 54, 20, koki_rx + 1, 18, "Koki Khad", label_side="right")

    # Maahlra Nala — upper valley from the west
    mahl_rx = np.interp(65, river_ys, river_xs)
    draw_tributary(ax, 14, 70, mahl_rx - 1, 65, "Maahlra Nala", label_side="left")

    # ── Altitude bands (flora zones) — subtle background shading ──
    bands = [
        (8, 25, "#E8E0D0", "Subtropical\n1200\u20131800m"),       # ban oak
        (25, 45, "#D8E0D0", "Lower Temperate\n1800\u20132500m"),  # deodar
        (45, 65, "#C8D8C8", "Upper Temperate\n2500\u20133200m"),  # kharsu oak
        (65, 80, "#C0D0C8", "Subalpine\n3200\u20133800m"),        # birch, rhododendron
        (80, 95, "#D8E8E8", "Alpine\n3800m+"),                    # meadow, rock
    ]
    for y_lo, y_hi, color, label in bands:
        ax.axhspan(y_lo, y_hi, color=color, alpha=0.2, zorder=0)
        ax.text(3, (y_lo + y_hi) / 2, label, fontsize=6, color=INK_LIGHT,
                fontfamily="serif", fontstyle="italic", va="center", ha="left",
                zorder=1)

    # ── Key locations ──
    locations = [
        (38, 10, "Larji", "Confluence \u2014 gateway\nwhere Tirthan\nmeets the Beas", 10),
        (32, 22, "Banjar", "Market town\n1,524m", 9),
        (40, 32, "Jibhi", "Tributary\nPushpabhadra", 8),
        (34, 40, "Gushaini", "Inner valley\nvillage", 8),
        (28, 52, "Chehni", "Chehni Kothi\u2014\ntallest Kath-Kuni\ntower", 9),
        (42, 58, "Shoja", "Near Jalori Pass\npanoramic views", 8),
        (50, 70, "Jalori Pass", "3,223m\nthreshold to\nthe spirit realm", 10),
        (55, 78, "Serolsar Lake", "Buddhi Nagin\u2019s\ngolden palace\nbeneath the water", 10),
        (35, 88, "Hanskund", "4,800m\nglacier source\nof the Tirthan", 9),
    ]

    for lx, ly, name, desc, size in locations:
        # Location dot
        ax.plot(lx, ly, "o", color=VERMILLION, markersize=size * 0.7,
                zorder=6, markeredgecolor=IRON_DARK, markeredgewidth=0.5)
        # Name
        ax.text(lx + 3, ly + 1.5, name, fontsize=size, fontweight="bold",
                color=INK, fontfamily="serif", zorder=7)
        # Description
        ax.text(lx + 3, ly - 0.5, desc, fontsize=6, color=INK_LIGHT,
                fontfamily="serif", va="top", zorder=7)

    # ── The Kund (bathhouse) — special marker near Serolsar ──
    kx, ky = 48, 74
    # Glowing circle
    for r, a in [(3.5, 0.08), (2.5, 0.12), (1.5, 0.2)]:
        ax.add_patch(Circle((kx, ky), r, color=SULPHUR,
                             alpha=a, zorder=4))
    ax.plot(kx, ky, "s", color=GOLD, markersize=10,
            markeredgecolor=IRON_DARK, markeredgewidth=1.0, zorder=6)
    ax.text(kx - 5, ky + 2, "The Kund",
            fontsize=11, fontweight="bold", color=IRON_RED,
            fontfamily="serif", fontstyle="italic", zorder=7)
    ax.text(kx - 5, ky + 0.5, "the bathhouse\nfor spirits",
            fontsize=7, color=INK_LIGHT, fontfamily="serif", zorder=7)

    # ── Passes (dotted paths) ──
    # Path from Shoja to Jalori Pass
    path_xs = np.linspace(42, 50, 30) + rng.uniform(-0.3, 0.3, 30)
    path_ys = np.linspace(58, 70, 30) + rng.uniform(-0.3, 0.3, 30)
    ax.plot(path_xs, path_ys, color=INK_FAINT, linewidth=1.0,
            linestyle="--", zorder=3)

    # Path to Serolsar
    path_xs2 = np.linspace(50, 55, 20) + rng.uniform(-0.3, 0.3, 20)
    path_ys2 = np.linspace(70, 78, 20) + rng.uniform(-0.3, 0.3, 20)
    ax.plot(path_xs2, path_ys2, color=INK_FAINT, linewidth=1.0,
            linestyle="--", zorder=3)

    # ── Deodar trees (in temperate band) ──
    for _ in range(40):
        tx = rng.uniform(5, 65)
        ty = rng.uniform(28, 55)
        if abs(tx - 35) < 6:  # avoid river
            continue
        tree_h = rng.uniform(1.5, 3.0)
        # Simple triangle tree
        tri_x = [tx, tx - 0.6, tx + 0.6]
        tri_y = [ty + tree_h, ty, ty]
        ax.fill(tri_x, tri_y, color=NAG_GREEN, alpha=0.3, zorder=1)

    # ── Compass rose ──
    cx, cy = 62, 12
    ax.annotate("", xy=(cx, cy + 5), xytext=(cx, cy),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
    ax.text(cx, cy + 6, "N", fontsize=10, fontweight="bold", color=INK,
            fontfamily="serif", ha="center", va="bottom")

    # ── Scale bar ──
    ax.plot([5, 15], [5, 5], color=INK, linewidth=1.5)
    ax.plot([5, 5], [4.5, 5.5], color=INK, linewidth=1.0)
    ax.plot([15, 15], [4.5, 5.5], color=INK, linewidth=1.0)
    ax.text(10, 3.5, "~10 km", fontsize=8, color=INK_LIGHT,
            fontfamily="serif", ha="center")

    # ── Cross-reference to Parvati Valley ──
    ax.annotate("", xy=(68, 45), xytext=(62, 45),
                arrowprops=dict(arrowstyle="->", color=INK_FAINT, lw=0.8))
    ax.text(63, 47, "To Parvati\nValley \u2192", fontsize=7, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic")

    attribution(ax, "The Tirthan Valley \u2014 from Larji gorge to the spirit realm above Jalori Pass",
                y=1)

    fig.savefig(OUT / "valley-map.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print(f"  \u2713 valley-map.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 2: The Larji Threshold — gorge as portal
# ═══════════════════════════════════════════════════════════════════

def larji_threshold():
    """The Larji gorge — where the Tirthan meets the Beas, the threshold."""
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=201)
    rng = np.random.default_rng(55)

    title_block(ax, "The Threshold at Larji",
                "Where the Tirthan meets the Beas \u2014 the gorge between worlds")

    # ── Gorge walls ──
    # Left wall
    left_xs = np.array([0, 5, 10, 18, 22, 28, 32, 35, 38])
    left_ys = np.array([10, 12, 20, 35, 50, 60, 68, 72, 75])
    # Add texture
    for i in range(5):
        offset = rng.uniform(-1, 1, len(left_xs))
        ax.fill_between(left_xs + offset * 0.3, 5, left_ys + i * 0.5,
                         color=STONE_GREY, alpha=0.08, zorder=1)
    ax.fill_between(left_xs, 5, left_ys, color=STONE_GREY, alpha=0.5, zorder=2)
    ax.plot(left_xs, left_ys, color=STONE_DARK, linewidth=1.5, zorder=3)

    # Right wall
    right_xs = np.array([100, 95, 90, 82, 78, 72, 68, 65, 62])
    right_ys = np.array([10, 15, 25, 40, 55, 62, 70, 74, 78])
    for i in range(5):
        offset = rng.uniform(-1, 1, len(right_xs))
        ax.fill_between(right_xs + offset * 0.3, 5, right_ys + i * 0.5,
                         color=STONE_GREY, alpha=0.08, zorder=1)
    ax.fill_between(right_xs, 5, right_ys, color=STONE_GREY, alpha=0.5, zorder=2)
    ax.plot(right_xs, right_ys, color=STONE_DARK, linewidth=1.5, zorder=3)

    # ── River flowing through the gorge ──
    river_xs = np.linspace(35, 65, 100)
    river_center = 50 + 3 * np.sin(river_xs * 0.15)
    for w, alpha in [(8, 0.15), (5, 0.25), (3, 0.4)]:
        ax.fill_between(river_xs, river_center - w/2,
                         river_center + w/2,
                         color=SPRING_BLUE, alpha=alpha, zorder=2)

    # ── Water surface with flow marks ──
    for i in range(20):
        sx = rng.uniform(38, 62)
        sy = 50 + 3 * math.sin(sx * 0.15) + rng.uniform(-2, 2)
        length = rng.uniform(1, 4)
        ax.plot([sx, sx + length], [sy, sy + 0.2],
                color=DEEP_WATER, linewidth=0.5, alpha=0.4, zorder=3)

    # ── Strata lines in the rock ──
    for wall_xs, wall_ys, side in [(left_xs, left_ys, "left"),
                                    (right_xs, right_ys, "right")]:
        for i in range(8):
            frac = 0.1 + i * 0.1
            xs_interp = np.interp(
                np.linspace(wall_xs.min(), wall_xs.max(), 50),
                wall_xs if side == "left" else wall_xs[::-1],
                wall_ys if side == "left" else wall_ys[::-1]
            )
            ys_line = 5 + frac * (xs_interp - 5)
            xs_plot = np.linspace(wall_xs.min(), wall_xs.max(), 50)
            ax.plot(xs_plot, ys_line, color=STONE_DARK,
                    linewidth=0.3, alpha=0.3, zorder=2)

    # ── Light at the end — the valley beyond ──
    # Glowing aperture between the walls
    for r, a in [(18, 0.05), (12, 0.1), (8, 0.15), (4, 0.25)]:
        ax.add_patch(Circle((50, 82), r, color=SULPHUR_LIGHT,
                             alpha=a, zorder=1))

    # ── Labels ──
    ax.text(15, 30, "Gneiss\nwalls", fontsize=9, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", rotation=60, zorder=4)
    ax.text(85, 35, "Gneiss\nwalls", fontsize=9, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", rotation=-60, zorder=4)

    ax.text(50, 20, "The Beas", fontsize=10, color=DEEP_WATER,
            fontfamily="serif", fontstyle="italic", ha="center", zorder=4)
    ax.text(50, 82, "The Tirthan Valley", fontsize=11, color=INK,
            fontfamily="serif", fontweight="bold", ha="center", zorder=4)

    # ── Annotations ──
    ax.text(50, 12, "Here the river narrows to a thread between walls of gneiss.\n"
            "The gorge is the threshold \u2014 pass through, and the world changes.",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            ha="center", va="center", fontstyle="italic", zorder=4)

    attribution(ax, y=2)
    fig.savefig(OUT / "larji-threshold.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print(f"  \u2713 larji-threshold.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 3: The Kund — bathhouse in Kath-Kuni style
# ═══════════════════════════════════════════════════════════════════

def the_kund():
    """The bathhouse — Kath-Kuni architecture over a hot spring."""
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=301)
    rng = np.random.default_rng(77)

    title_block(ax, "The Kund",
                "Stone and deodar over mineral water \u2014 Kath-Kuni architecture")

    # ── Ground / slope ──
    ground_xs = np.linspace(0, 100, 100)
    ground_ys = 18 + 3 * np.sin(ground_xs * 0.03) + 0.05 * (ground_xs - 50) ** 2 / 50
    ax.fill_between(ground_xs, 0, ground_ys, color=STONE_GREY, alpha=0.2, zorder=0)

    # ── Hot spring pool ──
    pool_cx, pool_cy = 50, 22
    pool_w, pool_h = 24, 8
    pool = mpatches.Ellipse((pool_cx, pool_cy), pool_w, pool_h,
                             facecolor=SPRING_BLUE, edgecolor=STONE_DARK,
                             linewidth=1.5, alpha=0.5, zorder=2)
    ax.add_patch(pool)
    # Inner glow
    pool_inner = mpatches.Ellipse((pool_cx, pool_cy), pool_w * 0.6, pool_h * 0.6,
                                   facecolor=SULPHUR_LIGHT, edgecolor="none",
                                   alpha=0.3, zorder=3)
    ax.add_patch(pool_inner)

    # Mineral deposits around edge
    for i in range(30):
        angle = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(pool_w * 0.45, pool_w * 0.55)
        dx = pool_cx + r * math.cos(angle) * 0.5
        dy = pool_cy + r * math.sin(angle) * 0.35
        ax.plot(dx, dy, "o", color=SULPHUR, markersize=rng.uniform(1, 3),
                alpha=rng.uniform(0.3, 0.6), zorder=3)

    # Steam
    draw_steam(ax, pool_cx, pool_cy + pool_h * 0.4, n=15, seed=88)

    # ── Building structure (Kath-Kuni) ──
    # Main building — centered over the pool
    bx, by, bw, bh = 30, 28, 40, 35

    # Left wall
    draw_kath_kuni_wall(ax, bx, by, 5, bh, layers=10)
    # Right wall
    draw_kath_kuni_wall(ax, bx + bw - 5, by, 5, bh, layers=10)
    # Back wall (partially visible)
    draw_kath_kuni_wall(ax, bx + 5, by + bh - 3, bw - 10, 3, layers=2)

    # ── Roof — slate tiles ──
    roof_xs = [bx - 3, bx + bw / 2, bx + bw + 3]
    roof_ys = [by + bh, by + bh + 15, by + bh]
    ax.fill(roof_xs, roof_ys, color=SLATE, alpha=0.6, zorder=4)
    ax.plot(roof_xs, roof_ys, color=STONE_DARK, linewidth=1.5, zorder=5)

    # Slate tile lines
    for i in range(10):
        frac = 0.1 + i * 0.08
        lx = bx - 3 + frac * (bx + bw / 2 - bx + 3)
        ly = by + bh + frac * 15
        rx = bx + bw + 3 - frac * (bx + bw + 3 - bx - bw / 2)
        ry = by + bh + frac * 15
        ax.plot([lx, rx], [ly, ry], color=STONE_DARK,
                linewidth=0.4, alpha=0.4, zorder=5)

    # ── Entrance — arched doorway ──
    door_cx = bx + bw / 2
    door_y = by
    door_w, door_h = 8, 12
    # Arch
    arch = Arc((door_cx, door_y + door_h), door_w, door_w,
               angle=0, theta1=0, theta2=180,
               color=DEODAR, linewidth=2.0, zorder=5)
    ax.add_patch(arch)
    # Door frame
    ax.plot([door_cx - door_w / 2, door_cx - door_w / 2],
            [door_y, door_y + door_h], color=DEODAR, linewidth=2.0, zorder=5)
    ax.plot([door_cx + door_w / 2, door_cx + door_w / 2],
            [door_y, door_y + door_h], color=DEODAR, linewidth=2.0, zorder=5)
    # Interior glow
    ax.add_patch(FancyBboxPatch(
        (door_cx - door_w / 2 + 0.5, door_y + 0.5),
        door_w - 1, door_h - 1,
        boxstyle="round,pad=0.5",
        facecolor=SAFFRON, edgecolor="none",
        alpha=0.25, zorder=4))

    # ── Windows — small square openings ──
    for wx in [bx + 8, bx + bw - 13]:
        wy = by + bh * 0.5
        ax.add_patch(FancyBboxPatch(
            (wx, wy), 5, 5, boxstyle="round,pad=0.2",
            facecolor=SAFFRON, edgecolor=DEODAR,
            linewidth=1.0, alpha=0.4, zorder=5))

    # ── Carved deodar details ──
    # Balcony rail
    rail_y = by + bh * 0.75
    ax.plot([bx + 2, bx + bw - 2], [rail_y, rail_y],
            color=DEODAR, linewidth=1.5, zorder=5)
    for rx in np.linspace(bx + 3, bx + bw - 3, 12):
        ax.plot([rx, rx], [rail_y, rail_y - 2],
                color=DEODAR, linewidth=0.8, alpha=0.6, zorder=5)

    # ── Annotations ──
    # Pool label
    ax.text(pool_cx, pool_cy - 1, "mineral spring\n94\u00b0C",
            fontsize=7, color=DEEP_WATER, fontfamily="serif",
            ha="center", va="center", fontstyle="italic", zorder=4)

    # Construction notes
    notes = [
        (12, 45, "deodar timber\n(Devad\u0101ru \u2014\ntimber of the gods)"),
        (80, 45, "local stone\nno mortar\nno cement"),
        (50, 82, "slate roof tiles\nfrom the gorge walls"),
        (12, 25, "the staircase\npulls up from\ninside"),
    ]
    for nx, ny, text in notes:
        ax.text(nx, ny, text, fontsize=7, color=INK_LIGHT,
                fontfamily="serif", fontstyle="italic",
                ha="center", va="center", zorder=6)

    attribution(ax, y=2)
    fig.savefig(OUT / "the-kund.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print(f"  \u2713 the-kund.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 4: The Spirit Registry — ledger where spirits sign in
# ═══════════════════════════════════════════════════════════════════

def spirit_registry():
    """The ledger — where spirits declare their true names."""
    fig, ax = make_fig(height=H * 1.4)
    ax.set_ylim(0, 140)  # taller canvas for three dense entries
    add_parchment_texture(ax, seed=401)
    rng = np.random.default_rng(99)

    title_block(ax, "The Registry of Spirits",
                "True name \u00b7 nature \u00b7 dwelling \u00b7 condition \u00b7 departure",
                y=133)

    # ── Ledger page layout — brass plates with Tankri-style entries ──
    # Three plates from the kund's registry, three modes of damage:
    #   sudden (flood), gradual (silt), anticipated (dams approaching)
    entries = [
        {
            "true_name": "Chuli Chaw",
            "nature": "~ nag devta \u2014 waterfall spirit",
            "dwelling": "rock pool at the park gate,\nTirthan gorge",
            "condition": "the monsoon that would not stop\nrearranged the stone \u2014\nthe cupped hands opened",
            "departure": "\u2014",
            "color": SPRING_BLUE,
        },
        {
            "true_name": "\u2014\u2009",
            "nature": "~ nag devta \u2014 stream spirit",
            "dwelling": "Kalavari nala,\neastern tributary",
            "condition": "the ridgeline road sends silt\ninto the stream \u2014\nruns grey where it ran clear",
            "departure": "\u2014",
            "color": NAG_GREEN,
        },
        {
            "true_name": "Shringa Rishi",
            "nature": "presiding devta \u2014\none of the eighteen",
            "dwelling": "Baggi village to Skeeran Jot,\nBanjar valley",
            "condition": "Tirthan's sisters are dammed \u2014\nParvati, then Sainj.\nHe watches the last free river.",
            "departure": "departed in good order\n(but returns each season\nto check)",
            "color": SAFFRON,
        },
    ]

    margin_l = 8
    line_h = 3.0          # vertical space per text line
    field_gap = 0.5       # extra gap between fields
    entry_pad_top = 2.0   # space above true-name within box
    entry_pad_bot = 2.0   # space below last field within box
    entry_gap = 3.0       # gap between entry boxes

    # Pre-compute each entry's total height
    def entry_height(entry):
        h = entry_pad_top + 4.0  # true-name line (larger font)
        for key in ("nature", "dwelling", "condition", "departure"):
            n_lines = entry[key].count("\n") + 1
            h += n_lines * line_h + field_gap
        h += entry_pad_bot
        return h

    total_h = sum(entry_height(e) for e in entries) + entry_gap * (len(entries) - 1)
    y_cursor = 122  # start below title in taller canvas

    for i, entry in enumerate(entries):
        eh = entry_height(entry)
        box_top = y_cursor
        box_bot = y_cursor - eh

        # Entry border
        box = FancyBboxPatch((margin_l, box_bot), 84, eh,
                              boxstyle="round,pad=0.5",
                              facecolor=entry["color"],
                              edgecolor=INK_FAINT,
                              linewidth=0.8, alpha=0.08, zorder=1)
        ax.add_patch(box)

        # True name — large
        name_y = box_top - entry_pad_top
        ax.text(margin_l + 2, name_y, entry["true_name"],
                fontsize=14, fontweight="bold", color=INK,
                fontfamily="serif", va="top", zorder=3)

        # Fields
        fields = [
            ("nature:", entry["nature"]),
            ("dwelling:", entry["dwelling"]),
            ("condition:", entry["condition"]),
            ("departure:", entry["departure"]),
        ]

        field_y = name_y - 4.0
        for key, val in fields:
            ax.text(margin_l + 4, field_y, key,
                    fontsize=8, color=INK_LIGHT, fontfamily="monospace",
                    va="top", zorder=3)
            ax.text(margin_l + 20, field_y, val,
                    fontsize=8, color=INK, fontfamily="serif",
                    va="top", zorder=3)
            n_lines = val.count("\n") + 1
            field_y -= n_lines * line_h + field_gap

        # Colored dot — spirit marker
        ax.plot(margin_l - 2, (box_top + box_bot) / 2, "o",
                color=entry["color"], markersize=8, zorder=3)

        y_cursor = box_bot - entry_gap

    # ── Footer note ──
    footer_y = max(y_cursor - 2, 3)
    ax.text(50, footer_y, "1,247 plates on a brass wire.\n"
            "Some spirits depart in good order. Some do not depart.",
            fontsize=9, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", va="top",
            linespacing=1.8, zorder=3)

    attribution(ax, y=1)
    fig.savefig(OUT / "spirit-registry.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print(f"  \u2713 spirit-registry.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 5: The Drowned Nag — river spirit who forgot its name
# ═══════════════════════════════════════════════════════════════════

def drowned_nag():
    """A nag devta whose spring was submerged by a dam — Haku parallel."""
    fig, ax = make_fig(bg=NIGHT)
    rng = np.random.default_rng(501)

    # Dark water scene
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    title_block(ax, "The Drowned Nag",
                "A river spirit whose spring was swallowed by the dam")
    # Override title colors for dark background
    ax.texts[0].set_color(MOONSILVER)
    ax.texts[1].set_color(STARLIGHT)

    # ── Dam wall — massive, dark, geometric ──
    dam_x, dam_w = 20, 60
    dam_y, dam_h = 10, 50
    # Concrete blocks
    for row in range(10):
        for col in range(6):
            bx = dam_x + col * dam_w / 6 + rng.uniform(-0.2, 0.2)
            by = dam_y + row * dam_h / 10
            bw = dam_w / 6 - 0.5
            bh = dam_h / 10 - 0.5
            shade = STONE_DARK if (row + col) % 2 == 0 else "#5A5550"
            ax.add_patch(FancyBboxPatch(
                (bx, by), bw, bh, boxstyle="round,pad=0.1",
                facecolor=shade, edgecolor="#3A3530",
                linewidth=0.4, alpha=0.7, zorder=2))

    # ── Water behind dam — dark, deep ──
    water_y = dam_y + dam_h
    water_xs = np.linspace(0, 100, 100)
    water_ys = water_y + 1.5 * np.sin(water_xs * 0.1) + rng.uniform(-0.3, 0.3, 100)
    ax.fill_between(water_xs, water_y - 2, water_ys,
                     color=DEEP_WATER, alpha=0.6, zorder=3)
    ax.plot(water_xs, water_ys, color=SPRING_BLUE, linewidth=0.8,
            alpha=0.5, zorder=4)

    # ── The nag — submerged, coiling ──
    # Body beneath the water, ghostly
    n_pts = 80
    ts = np.linspace(0, 1, n_pts)
    nag_xs = 50 + 25 * np.sin(ts * 3 * math.pi) * (0.3 + 0.7 * ts)
    nag_ys = 62 + 15 * ts + 5 * np.cos(ts * 2 * math.pi)

    for i in range(n_pts - 1):
        width = 3.0 * (1 - 0.5 * ts[i])
        alpha = 0.15 + 0.25 * (1 - ts[i])
        ax.plot([nag_xs[i], nag_xs[i+1]], [nag_ys[i], nag_ys[i+1]],
                color=NAG_GREEN, linewidth=width * 2,
                alpha=alpha, solid_capstyle="round", zorder=5)

    # Head breaking the surface
    hx, hy = nag_xs[-1], nag_ys[-1]
    # Glow around head
    for r, a in [(4, 0.05), (2.5, 0.1), (1.5, 0.2)]:
        ax.add_patch(Circle((hx, hy), r, color=NAG_LIGHT,
                             alpha=a, zorder=6))
    # Head shape
    head = FancyBboxPatch((hx - 2, hy - 1), 4, 2.5,
                           boxstyle="round,pad=0.5",
                           facecolor=NAG_GREEN, edgecolor=NAG_DARK,
                           linewidth=1.2, alpha=0.8, zorder=7)
    ax.add_patch(head)
    # Eyes
    ax.plot(hx - 0.8, hy + 0.5, "o", color=GOLD, markersize=5, zorder=8)
    ax.plot(hx + 0.8, hy + 0.5, "o", color=GOLD, markersize=5, zorder=8)
    ax.plot(hx - 0.8, hy + 0.5, "o", color=NIGHT, markersize=2, zorder=9)
    ax.plot(hx + 0.8, hy + 0.5, "o", color=NIGHT, markersize=2, zorder=9)

    # ── Stars ──
    for _ in range(60):
        sx = rng.uniform(0, 100)
        sy = rng.uniform(75, 98)
        ax.plot(sx, sy, "*", color=STARLIGHT,
                markersize=rng.uniform(0.5, 2.5),
                alpha=rng.uniform(0.3, 0.8), zorder=1)

    # ── Text overlay ──
    ax.text(50, 8, "Tattapani \u2014 the hot water\n"
            "The spring is still there, 130 metres below the reservoir.\n"
            "The nag remembers the temperature. It does not remember its name.",
            fontsize=9, color=STARLIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", va="center",
            linespacing=1.8, zorder=10)

    # Dam label
    ax.text(50, 35, "Kol Dam\n(built 2015)", fontsize=10,
            color=STONE_GREY, fontfamily="serif", ha="center",
            fontweight="bold", zorder=4)

    attribution(ax, "The Drowned Nag \u2014 what is a river spirit without a river?", y=2)
    ax.texts[-1].set_color(STARLIGHT)

    fig.savefig(OUT / "drowned-nag.png", dpi=DPI, bbox_inches="tight",
                facecolor=NIGHT, pad_inches=0.3)
    plt.close(fig)
    print(f"  \u2713 drowned-nag.png")


# ═══════════════════════════════════════════════════════════════════
# Figure 6: Serolsar — Buddhi Nagin's domain
# ═══════════════════════════════════════════════════════════════════

def serolsar_lake():
    """Serolsar Lake — the golden palace beneath the water."""
    fig, ax = make_fig()
    add_parchment_texture(ax, seed=601)
    rng = np.random.default_rng(123)

    title_block(ax, "Serolsar",
                "The golden palace of Buddhi Nagin \u2014 mother of all n\u0101g devt\u0101s")

    # ── Forest surrounding the lake (dense deodar) ──
    for _ in range(80):
        tx = rng.uniform(2, 98)
        ty = rng.uniform(55, 88)
        # Only draw if outside lake area
        dist = math.sqrt((tx - 50) ** 2 + ((ty - 55) * 1.5) ** 2)
        if dist > 28:
            tree_h = rng.uniform(2, 5)
            base_w = tree_h * 0.4
            tri_x = [tx, tx - base_w, tx + base_w]
            tri_y = [ty + tree_h, ty, ty]
            shade = NAG_GREEN if rng.random() > 0.3 else NAG_DARK
            ax.fill(tri_x, tri_y, color=shade,
                    alpha=rng.uniform(0.25, 0.5), zorder=1)

    # ── The lake ──
    lake_cx, lake_cy = 50, 50
    lake_w, lake_h = 50, 25

    # Lake surface — concentric ellipses for depth
    for i in range(8):
        frac = 1 - i * 0.1
        alpha = 0.1 + i * 0.06
        color = SPRING_BLUE if i < 5 else DEEP_WATER
        lake = mpatches.Ellipse((lake_cx, lake_cy),
                                 lake_w * frac, lake_h * frac,
                                 facecolor=color, edgecolor="none",
                                 alpha=alpha, zorder=2)
        ax.add_patch(lake)

    # Lake edge
    theta = np.linspace(0, 2 * np.pi, 100)
    edge_xs = lake_cx + lake_w / 2 * np.cos(theta) + rng.uniform(-0.3, 0.3, 100)
    edge_ys = lake_cy + lake_h / 2 * np.sin(theta) + rng.uniform(-0.2, 0.2, 100)
    ax.plot(edge_xs, edge_ys, color=NAG_DARK, linewidth=1.0, alpha=0.5, zorder=3)

    # ── Golden palace beneath — faint geometric shapes underwater ──
    # Central dome
    for r, a in [(8, 0.06), (5, 0.1), (3, 0.15)]:
        ax.add_patch(Circle((lake_cx, lake_cy - 2), r,
                             color=GOLD, alpha=a, zorder=2))

    # Palace pillars — faint vertical lines
    for px in np.linspace(lake_cx - 10, lake_cx + 10, 7):
        ax.plot([px, px], [lake_cy - 8, lake_cy + 2],
                color=GOLD, linewidth=0.8, alpha=0.12, zorder=2)

    # Palace roof line
    roof_xs = np.linspace(lake_cx - 12, lake_cx + 12, 50)
    roof_ys = lake_cy + 3 + 4 * np.cos((roof_xs - lake_cx) * 0.13)
    ax.plot(roof_xs, roof_ys, color=GOLD, linewidth=1.0, alpha=0.15, zorder=2)

    # ── Buddhi Nagin — coiled serpent beneath the surface ──
    # Spiral around the palace
    spiral_ts = np.linspace(0, 3 * math.pi, 150)
    spiral_r = 6 + 6 * spiral_ts / (3 * math.pi)
    spiral_xs = lake_cx + spiral_r * np.cos(spiral_ts)
    spiral_ys = lake_cy - 2 + spiral_r * 0.5 * np.sin(spiral_ts)
    for i in range(len(spiral_ts) - 1):
        width = 2.0 * (0.3 + 0.7 * spiral_ts[i] / (3 * math.pi))
        alpha = 0.08 + 0.12 * (spiral_ts[i] / (3 * math.pi))
        ax.plot([spiral_xs[i], spiral_xs[i+1]],
                [spiral_ys[i], spiral_ys[i+1]],
                color=NAG_GREEN, linewidth=width * 2,
                alpha=alpha, solid_capstyle="round", zorder=2)

    # ── "Do not touch the water" ──
    ax.text(lake_cx, lake_cy + lake_h / 2 + 4,
            "Touching the water is forbidden.",
            fontsize=10, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=4)
    ax.text(lake_cx, lake_cy + lake_h / 2 + 1.5,
            "Not because it is polluted. Because it is inhabited.",
            fontsize=8, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=4)

    # ── Altitude marker ──
    ax.text(92, 85, "3,100m", fontsize=9, color=INK_LIGHT,
            fontfamily="serif", rotation=90, ha="center", zorder=3)

    # ── Ghee offering (small pot at lake edge) ──
    pot_x, pot_y = 28, 38
    ax.add_patch(FancyBboxPatch(
        (pot_x - 1.5, pot_y - 1), 3, 2,
        boxstyle="round,pad=0.3",
        facecolor=IRON_RED, edgecolor=IRON_DARK,
        linewidth=0.8, zorder=4))
    ax.text(pot_x, pot_y - 3, "ghee offering\nfor Buddhi Nagin",
            fontsize=6, color=INK_LIGHT, fontfamily="serif",
            fontstyle="italic", ha="center", zorder=4)

    # ── Path from Jalori Pass ──
    path_xs = np.linspace(5, 25, 40) + rng.uniform(-0.5, 0.5, 40)
    path_ys = np.linspace(88, 42, 40) + rng.uniform(-0.5, 0.5, 40)
    ax.plot(path_xs, path_ys, color=INK_FAINT, linewidth=1.0,
            linestyle="--", zorder=1)
    ax.text(5, 90, "from\nJalori Pass\n(5 km)", fontsize=7, color=INK_LIGHT,
            fontfamily="serif", fontstyle="italic", zorder=3)

    # ── Annual pilgrimage note ──
    ax.text(50, 12, "All n\u0101g devt\u0101s visit Buddhi Nagin once a year.\n"
            "She remembers every name. Even the ones they have forgotten.",
            fontsize=9, color=INK, fontfamily="serif",
            fontstyle="italic", ha="center", va="center",
            linespacing=1.8, zorder=4)

    attribution(ax, y=2)
    fig.savefig(OUT / "serolsar-lake.png", dpi=DPI, bbox_inches="tight",
                facecolor=PARCHMENT, pad_inches=0.3)
    plt.close(fig)
    print(f"  \u2713 serolsar-lake.png")


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

def main():
    print(f"Generating illustrations for The Spirit's Kund...")
    print(f"Output: {OUT}\n")
    valley_map()
    larji_threshold()
    the_kund()
    spirit_registry()
    drowned_nag()
    serolsar_lake()
    print(f"\nDone. {6} images generated.")


if __name__ == "__main__":
    main()
