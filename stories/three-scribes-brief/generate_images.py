# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib>=3.9", "numpy>=1.26"]
# ///
"""
The Three Scribes' Brief — 6 illustrations
Setting: Thalpan petroglyph terrace, Indus gorge, Gilgit-Baltistan

Six figures:
  1. terrace-overview.png    — the Thalpan terrace with three paths
  2. one-direction.png       — the inventory's blind spot
  3. three-surveys.png       — three scribe approaches compared
  4. comparison-rock.png     — three documents on the flat rock
  5. phantom-register.png    — a name with no person behind it
  6. ibex-on-cliff.png       — the ibex, indifferent to the inventory

Usage:
    uv run generate_images.py          # saves PNGs
    uv run generate_images.py --show   # also opens matplotlib window
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

SLUG = "the-three-scribes-brief"
OUT = (Path(__file__).parent / f"../../website/static/images/writing/{SLUG}").resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 7

# ── Palette: Thalpan / Indus gorge / gneiss + carved rock ────────────
BG_DARK = "#12121E"         # night background (consistent across stories)
GNEISS = "#4A4845"          # Indian plate gneiss
GNEISS_LIGHT = "#8A8580"    # lit gneiss face
CARVED = "#C8C0B0"          # petroglyph carved surface
CARVED_OLD = "#9A9488"      # weathered carving
INDUS = "#5888A8"           # river blue
INDUS_DEEP = "#3A6080"      # deep water
CHALK = "#E8E4D8"           # text colour
COPPER = "#C4886B"          # accent (first scribe)
WATER = "#4A8B6B"           # second scribe accent
AMBER = "#D4A86B"           # third scribe accent
RED_ACCENT = "#C0605A"      # damage / missing
JUNIPER = "#4A5840"         # sparse vegetation
SNOW = "#F0EDE8"            # summit snow
SKY_DUSK = "#2A2838"        # evening sky
SHADOW = "#0A0A08"          # deep shadow
STONE_WARM = "#B8A890"      # warm sandstone register


def make_fig(width=W, height=H, bg=BG_DARK):
    fig, ax = plt.subplots(1, 1, figsize=(width, height))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.2, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ {name}.png")


def rock_texture(ax, x0, y0, x1, y1, color=GNEISS, n=40, seed=42):
    """Horizontal foliation lines suggesting gneiss banding."""
    rng = np.random.default_rng(seed)
    for _ in range(n):
        y = rng.uniform(y0, y1)
        xstart = rng.uniform(x0, x0 + (x1 - x0) * 0.3)
        xend = rng.uniform(x0 + (x1 - x0) * 0.5, x1)
        xs = np.linspace(xstart, xend, 30)
        ys = y + rng.normal(0, 0.3, 30).cumsum() * 0.1
        ax.plot(xs, ys, color=color, alpha=0.15, lw=0.5)


def draw_ibex(ax, cx, cy, scale=1.0, color=CARVED, facing="right"):
    """Petroglyph-style ibex silhouette."""
    flip = 1 if facing == "right" else -1
    s = scale
    body = mpatches.Ellipse((cx, cy), 4 * s, 1.8 * s, color=color, lw=0)
    ax.add_patch(body)
    for dx in [-1.2, -0.6, 0.6, 1.2]:
        ax.plot([cx + dx * s * flip, cx + dx * s * flip + 0.2 * s * flip],
                [cy - 0.9 * s, cy - 2.2 * s], color=color, lw=1.5 * s)
    ax.plot([cx + 2 * s * flip, cx + 3 * s * flip],
            [cy + 0.2 * s, cy + 0.8 * s], color=color, lw=2 * s)
    horn_t = np.linspace(0, 1, 20)
    hx = cx + (3 + horn_t * 1.5) * s * flip
    hy = cy + (0.8 + horn_t * 2.5 - horn_t**2 * 1.0) * s
    ax.plot(hx, hy, color=color, lw=2 * s)


# ── Figure 1: Terrace overview ──────────────────────────────────────

def fig_terrace_overview():
    fig, ax = make_fig(12, 8)

    # Sky gradient
    for i in range(100):
        t = i / 100
        r = int(0x12 + (0x2A - 0x12) * t)
        g = int(0x12 + (0x28 - 0x12) * t)
        b = int(0x1E + (0x38 - 0x1E) * t)
        ax.axhspan(i, i + 1, color=f"#{r:02x}{g:02x}{b:02x}", alpha=0.5)

    # Far mountains (Nanga Parbat direction)
    rng = np.random.default_rng(8126)
    xs = np.linspace(0, 100, 200)
    ys_far = 72 + 12 * np.exp(-((xs - 30) ** 2) / 200) + rng.normal(0, 0.5, 200)
    ax.fill_between(xs, 55, ys_far, color="#2A2838", alpha=0.7)
    snow_mask = ys_far > 79
    ax.fill_between(xs[snow_mask], ys_far[snow_mask] - 2, ys_far[snow_mask],
                    color=SNOW, alpha=0.3)

    # Mid-slopes (barren Karakoram)
    ys_mid = 45 + 6 * np.sin(xs * 0.06) + rng.normal(0, 0.3, 200)
    ax.fill_between(xs, 32, ys_mid, color=GNEISS, alpha=0.4)

    # Terrace (the flat platform where the carvings are)
    ax.fill_between([10, 90], [30, 30], [34, 34], color=GNEISS_LIGHT, alpha=0.5)
    rock_texture(ax, 10, 30, 90, 34, color=GNEISS_LIGHT, n=25, seed=99)

    # Boulders on terrace (carved rocks)
    boulder_positions = [(20, 32), (35, 31.5), (50, 32.5), (65, 31), (80, 32)]
    for bx, by in boulder_positions:
        w = rng.uniform(3, 5)
        h = rng.uniform(2, 3.5)
        boulder = mpatches.Ellipse((bx, by), w, h, color=GNEISS_LIGHT,
                                    alpha=0.6, lw=0)
        ax.add_patch(boulder)
        # Tiny carved marks
        for _ in range(3):
            mx = bx + rng.uniform(-w / 3, w / 3)
            my = by + rng.uniform(-h / 4, h / 4)
            ax.plot(mx, my, ".", color=CARVED, ms=2, alpha=0.5)

    # Three scribe paths (different colours)
    # First scribe: dense, thorough, covers 2/3 of terrace
    path1_x = np.linspace(12, 72, 80)
    path1_y = 32 + np.sin(path1_x * 0.3) * 1.5 + rng.normal(0, 0.3, 80)
    ax.plot(path1_x, path1_y, color=COPPER, lw=1.8, alpha=0.7, ls="-")

    # Second scribe: direct, efficient, reaches the end
    path2_x = np.linspace(12, 88, 50)
    path2_y = 31 + 0.5 * np.sin(path2_x * 0.1)
    ax.plot(path2_x, path2_y, color=WATER, lw=1.5, alpha=0.7, ls="--")

    # Third scribe: moderate, reaches end
    path3_x = np.linspace(12, 88, 60)
    path3_y = 33 + np.sin(path3_x * 0.15) * 1.0 + rng.normal(0, 0.15, 60)
    ax.plot(path3_x, path3_y, color=AMBER, lw=1.5, alpha=0.7, ls="-.")

    # River below
    river_y = 18 + np.sin(xs * 0.08) * 2
    ax.fill_between(xs, 10, river_y, color=INDUS_DEEP, alpha=0.3)
    ax.plot(xs, river_y, color=INDUS, lw=1.0, alpha=0.5)

    # Foreground darkness
    ax.fill_between(xs, 0, 12, color=SHADOW, alpha=0.8)

    # Labels
    ax.text(50, 93, "The Thalpan Terrace — Three Paths, One Rock",
            fontsize=12, color=CHALK, ha="center", fontfamily="serif")
    ax.text(12, 37, "First scribe", fontsize=7, color=COPPER,
            fontstyle="italic", alpha=0.8)
    ax.text(70, 28, "Second scribe", fontsize=7, color=WATER,
            fontstyle="italic", alpha=0.8)
    ax.text(55, 36, "Third scribe", fontsize=7, color=AMBER,
            fontstyle="italic", alpha=0.8)
    ax.text(50, 7, "Thalpan · Indus Gorge · 35.62°N, 74.60°E",
            fontsize=8, color=GNEISS_LIGHT, ha="center", fontfamily="serif")

    save(fig, "terrace-overview")


# ── Figure 2: One-directional inventory ─────────────────────────────

def fig_one_direction():
    fig, ax = make_fig(12, 6)

    # Two columns: "Figures on the Rock" (left) and "Names in the Register" (right)
    # Left column — carved figures as petroglyph-style marks
    ax.text(25, 90, "Figures on the Rock", fontsize=11, color=CARVED,
            ha="center", fontfamily="serif")
    ax.text(75, 90, "Names in the Register", fontsize=11, color=STONE_WARM,
            ha="center", fontfamily="serif")

    # Dividing line
    ax.plot([50, 50], [10, 85], color=GNEISS, lw=0.5, alpha=0.3, ls=":")

    # Rock figures (left) — small ovals representing carved panels
    fig_positions = [(18, 75), (32, 75), (18, 60), (32, 60),
                     (18, 45), (32, 45), (18, 30), (32, 30)]
    fig_labels = ["ibex I", "hunt scene", "stupa", "ibex II",
                  "warrior", "caravan", "worship", "ibex III"]

    # Register names (right) — text entries
    reg_positions = [(68, 75), (82, 75), (68, 60), (82, 60),
                     (68, 45), (82, 45), (68, 30), (82, 30)]
    reg_labels = ["#001 ibex I", "#002 hunt", "#003 stupa", "#004 ibex II",
                  "#005 warrior", "#006 caravan", "#007 worship", "#008 ibex III"]

    # Add a phantom (register entry with no figure) and an unregistered figure
    # Phantom: register entry #009 with no corresponding figure
    reg_positions.append((75, 18))
    reg_labels.append("#009 conservator")

    for (fx, fy), label in zip(fig_positions, fig_labels):
        boulder = mpatches.Ellipse((fx, fy), 8, 5, facecolor=GNEISS,
                                    edgecolor=GNEISS_LIGHT, lw=0.8, alpha=0.5)
        ax.add_patch(boulder)
        ax.text(fx, fy, label, fontsize=5, color=CARVED, ha="center",
                va="center", fontstyle="italic")

    for (rx, ry), label in zip(reg_positions, reg_labels):
        rect = FancyBboxPatch((rx - 7, ry - 2.5), 14, 5,
                               boxstyle="round,pad=0.3",
                               facecolor="#1E1E2C", edgecolor=STONE_WARM,
                               lw=0.6, alpha=0.7)
        ax.add_patch(rect)
        color = RED_ACCENT if "conservator" in label else STONE_WARM
        ax.text(rx, ry, label, fontsize=5, color=color, ha="center",
                va="center", fontfamily="monospace")

    # Forward arrows (figure → register): solid, verified
    for i in range(8):
        fx, fy = fig_positions[i]
        rx, ry = reg_positions[i]
        ax.annotate("", xy=(rx - 7, ry), xytext=(fx + 4, fy),
                    arrowprops=dict(arrowstyle="->", color=CHALK,
                                    lw=0.8, alpha=0.5))

    # Missing reverse arrow for phantom — draw a red X
    rx, ry = reg_positions[8]
    ax.annotate("", xy=(35, 20), xytext=(rx - 7, ry),
                arrowprops=dict(arrowstyle="->", color=RED_ACCENT,
                                lw=1.2, alpha=0.6, ls="--"))
    ax.text(35, 20, "?", fontsize=14, color=RED_ACCENT, ha="center",
            va="center", fontweight="bold", alpha=0.7)

    # Annotation
    ax.text(50, 5, "The inventory checked in one direction only",
            fontsize=8, color=CHALK, ha="center", fontstyle="italic",
            alpha=0.7)
    ax.text(50, 95, "Figure → Register: Verified.  Register → Figure: Never Checked.",
            fontsize=10, color=CHALK, ha="center", fontfamily="serif")

    save(fig, "one-direction")


# ── Figure 3: Three surveys compared ────────────────────────────────

def fig_three_surveys():
    fig, axes = plt.subplots(1, 3, figsize=(14, 6))
    fig.patch.set_facecolor(BG_DARK)

    scribes = [
        ("The First Scribe", "12 findings · no brief",
         COPPER, 12, False, "Taxila-trained"),
        ("The Second Scribe", "4 findings · precise brief",
         WATER, 4, True, "Chitral-trained"),
        ("The Third Scribe", "3 findings · brief + reflection",
         AMBER, 3, True, "Peshawar-trained"),
    ]

    rng = np.random.default_rng(35)

    for ax, (title, subtitle, color, n_findings, has_brief, school) in zip(axes, scribes):
        ax.set_facecolor(BG_DARK)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")

        # Draw a terrace cross-section (simplified rock face)
        xs = np.linspace(5, 95, 100)
        rock_top = 65 + rng.normal(0, 0.5, 100)
        rock_bot = 25 + rng.normal(0, 0.3, 100)
        ax.fill_between(xs, rock_bot, rock_top, color=GNEISS, alpha=0.3)
        rock_texture(ax, 5, 25, 95, 65, color=GNEISS_LIGHT, n=15,
                     seed=hash(title) % 10000)

        # Damage marks — scattered across the rock face
        for i in range(n_findings):
            dx = rng.uniform(10, 90)
            dy = rng.uniform(30, 60)
            # Draw a crack mark
            crack_len = rng.uniform(2, 5)
            angle = rng.uniform(-0.5, 0.5)
            ax.plot([dx, dx + crack_len * np.cos(angle)],
                    [dy, dy + crack_len * np.sin(angle)],
                    color=color, lw=2.0, alpha=0.8)
            ax.plot(dx, dy, "o", color=color, ms=4, alpha=0.6)

        # Brief indicator
        if has_brief:
            # Draw a small document at bottom
            doc = Rectangle((60, 8), 25, 14, facecolor="#1E1E2C",
                             edgecolor=color, lw=1.0, alpha=0.7)
            ax.add_patch(doc)
            # Ruled lines inside
            for ly in range(10, 20, 2):
                ax.plot([63, 82], [ly, ly], color=color, lw=0.3, alpha=0.4)
            ax.text(72.5, 15, "brief", fontsize=6, color=color,
                    ha="center", va="center", fontstyle="italic")

        ax.text(50, 92, title, fontsize=10, color=color, ha="center",
                fontfamily="serif", fontweight="bold")
        ax.text(50, 84, subtitle, fontsize=7, color=CHALK, ha="center",
                fontstyle="italic", alpha=0.7)
        ax.text(50, 78, school, fontsize=6, color=GNEISS_LIGHT, ha="center",
                alpha=0.5)

    fig.suptitle("Three Surveys of the Same Rock",
                 fontsize=13, color=CHALK, fontfamily="serif", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save(fig, "three-surveys")


# ── Figure 4: The flat rock with three documents ────────────────────

def fig_comparison_rock():
    fig, ax = make_fig(12, 7)

    # The flat rock surface
    rock = mpatches.FancyBboxPatch((8, 15), 84, 60,
                                    boxstyle="round,pad=2",
                                    facecolor=GNEISS, edgecolor=GNEISS_LIGHT,
                                    lw=1.5, alpha=0.5)
    ax.add_patch(rock)
    rock_texture(ax, 8, 15, 92, 75, color=GNEISS_LIGHT, n=30, seed=77)

    # Three documents laid side by side
    docs = [
        ("Survey", COPPER, 12, 34, 22, 38, "12 findings\n\n· ibex panel\n· re-carved figure\n· drifted archives\n· stale guild list\n· undemonstrated\n  skills\n· ...\n\n(no brief)"),
        ("Brief", WATER, 40, 34, 22, 38, "4 findings\n\nRepair order:\n1. panel 47\n2. lintel crack\n3. re-carved fig.\n4. phantom name\n\nExecutor: the\nconservator"),
        ("Brief +\nReflection", AMBER, 68, 34, 22, 38, "3 findings\n\nRepair order\n(general)\n\n\"I crossed a line\nin this survey\nthat I should\nhave marked\nmore clearly.\""),
    ]

    for label, color, x, y, w, h, content in docs:
        # Document rectangle
        doc = Rectangle((x, y), w, h, facecolor="#1A1A2A",
                         edgecolor=color, lw=1.2, alpha=0.85)
        ax.add_patch(doc)
        # Label
        ax.text(x + w / 2, y + h + 2, label, fontsize=8, color=color,
                ha="center", fontfamily="serif", fontweight="bold")
        # Content text
        ax.text(x + 1.5, y + h - 2, content, fontsize=4.5, color=CHALK,
                va="top", fontfamily="monospace", alpha=0.7,
                linespacing=1.3)

    # The archivist figure (small, sitting beside the rock)
    ax.plot([5, 5], [30, 35], color=CHALK, lw=1.2, alpha=0.5)
    ax.plot(5, 36, "o", color=CHALK, ms=3, alpha=0.5)
    ax.text(5, 27, "archivist", fontsize=5, color=CHALK, ha="center",
            fontstyle="italic", alpha=0.4)

    # Thread Walker (sitting to the other side, writing)
    ax.plot([95, 95], [30, 35], color=CHALK, lw=1.0, alpha=0.4)
    ax.plot(95, 36, "o", color=CHALK, ms=2.5, alpha=0.4)
    ax.text(95, 27, "Thread\nWalker", fontsize=5, color=CHALK, ha="center",
            fontstyle="italic", alpha=0.3)

    # River suggestion below
    xs = np.linspace(0, 100, 100)
    ax.fill_between(xs, 0, 10, color=INDUS_DEEP, alpha=0.15)
    ax.plot(xs, 10 + np.sin(xs * 0.1) * 1.5, color=INDUS, lw=0.8, alpha=0.3)

    ax.text(50, 92, "Three Documents on the Flat Rock Above the River",
            fontsize=11, color=CHALK, ha="center", fontfamily="serif")
    ax.text(50, 5, "\"I need all three.\"", fontsize=9, color=CHALK,
            ha="center", fontstyle="italic", alpha=0.7)

    save(fig, "comparison-rock")


# ── Figure 5: The phantom in the register ───────────────────────────

def fig_phantom_register():
    fig, ax = make_fig(12, 6)

    # Register (a ruled page with entries)
    page = Rectangle((15, 10), 70, 78, facecolor="#1E1E2C",
                       edgecolor=GNEISS_LIGHT, lw=0.8, alpha=0.85)
    ax.add_patch(page)

    # Binding margin
    ax.plot([25, 25], [10, 88], color=RED_ACCENT, lw=0.5, alpha=0.3)

    # Title on the register
    ax.text(50, 84, "Conservation Register — Upper Terrace",
            fontsize=9, color=STONE_WARM, ha="center", fontfamily="serif")
    ax.plot([27, 83], [81, 81], color=STONE_WARM, lw=0.4, alpha=0.4)

    # Entries — names with status
    entries = [
        ("#001  Khan, A.    Chitral guild    assigned    mark confirmed", CHALK, 0.7),
        ("#002  Begum, S.   Taxila guild     assigned    mark confirmed", CHALK, 0.7),
        ("#003  Malik, R.   Peshawar guild   assigned    mark confirmed", CHALK, 0.7),
        ("#004  Shah, T.    Hunza guild      assigned    mark confirmed", CHALK, 0.7),
        ("#005  Lone, F.    Chitral guild    assigned    mark confirmed", CHALK, 0.7),
        ("#006  Wali, M.    newest guild     assigned    ——————————————", RED_ACCENT, 0.9),
        ("#007  Akhtar, N.  Taxila guild     assigned    mark confirmed", CHALK, 0.7),
        ("#008  Baig, H.    Peshawar guild   assigned    mark confirmed", CHALK, 0.7),
    ]

    for i, (text, color, alpha) in enumerate(entries):
        y = 74 - i * 8
        ax.text(28, y, text, fontsize=5.5, color=color, fontfamily="monospace",
                alpha=alpha)
        ax.plot([27, 83], [y - 3, y - 3], color=GNEISS, lw=0.2, alpha=0.2)

    # Highlight the phantom entry
    phantom_y = 74 - 5 * 8
    highlight = Rectangle((26, phantom_y - 3.5), 58, 8,
                           facecolor=RED_ACCENT, edgecolor="none", alpha=0.08)
    ax.add_patch(highlight)

    # Annotation arrow pointing to the phantom
    ax.annotate("the register says\nshe lives here.\nthe room is empty.",
                xy=(84, phantom_y), xytext=(90, phantom_y + 20),
                fontsize=7, color=RED_ACCENT, ha="center",
                fontstyle="italic",
                arrowprops=dict(arrowstyle="->", color=RED_ACCENT,
                                lw=0.8, alpha=0.6))

    # "Three pairs of eyes found it. Three years of calipers did not."
    ax.text(50, 3, "Three pairs of eyes found it.  Three years of calipers did not.",
            fontsize=8, color=CHALK, ha="center", fontstyle="italic", alpha=0.6)

    ax.text(50, 95, "The Phantom in the Register",
            fontsize=12, color=CHALK, ha="center", fontfamily="serif")

    save(fig, "phantom-register")


# ── Figure 6: The ibex on the cliff ────────────────────────────────

def fig_ibex_on_cliff():
    fig, ax = make_fig(12, 8)

    # Sky gradient (dusk over the gorge)
    for i in range(100):
        t = i / 100
        r = int(0x12 + (0x2A - 0x12) * t)
        g = int(0x12 + (0x28 - 0x12) * t)
        b = int(0x1E + (0x38 - 0x1E) * t)
        ax.axhspan(i, i + 1, color=f"#{r:02x}{g:02x}{b:02x}", alpha=0.5)

    # Gorge walls (steep)
    rng = np.random.default_rng(3562)
    xs = np.linspace(0, 100, 200)

    # Left cliff face
    left_wall = 50 + 20 * np.exp(-((xs - 15) ** 2) / 80) + rng.normal(0, 0.4, 200)
    ax.fill_between(xs[:80], 0, left_wall[:80], color=GNEISS, alpha=0.5)

    # Right cliff face
    right_wall = 55 + 18 * np.exp(-((xs - 85) ** 2) / 80) + rng.normal(0, 0.4, 200)
    ax.fill_between(xs[120:], 0, right_wall[120:], color=GNEISS, alpha=0.5)

    # River at the bottom of the gorge
    gorge_xs = np.linspace(30, 70, 100)
    river_y = 12 + np.sin(gorge_xs * 0.15) * 1.5
    ax.fill_between(gorge_xs, 5, river_y, color=INDUS_DEEP, alpha=0.3)
    ax.plot(gorge_xs, river_y, color=INDUS, lw=1.0, alpha=0.4)

    # Terrace ledge (where the carvings are, far below)
    ax.fill_between([28, 72], [15, 15], [18, 18], color=GNEISS_LIGHT, alpha=0.2)
    ax.text(50, 16, "terrace", fontsize=5, color=GNEISS_LIGHT, ha="center",
            fontstyle="italic", alpha=0.3)

    # Three tiny figures on the terrace (the scribes, barely visible)
    for sx, sc in [(38, COPPER), (50, WATER), (62, AMBER)]:
        ax.plot([sx, sx], [18, 19.5], color=sc, lw=0.8, alpha=0.4)
        ax.plot(sx, 20, "o", color=sc, ms=1.5, alpha=0.4)

    # The ibex — high on the left cliff, above everything
    draw_ibex(ax, 22, 62, scale=2.0, color=CARVED, facing="right")

    # Cliff edge where the ibex stands
    ledge_xs = np.linspace(12, 32, 50)
    ledge_ys = 58 + np.sin(ledge_xs * 0.3) * 0.8
    ax.plot(ledge_xs, ledge_ys, color=GNEISS_LIGHT, lw=1.0, alpha=0.4)

    # Labels
    ax.text(50, 93, "The ibex does not need repair.  It needs only the cliff.",
            fontsize=10, color=CHALK, ha="center", fontfamily="serif",
            fontstyle="italic")
    ax.text(50, 4, "Indus gorge, above Thalpan",
            fontsize=7, color=GNEISS_LIGHT, ha="center", fontfamily="serif",
            alpha=0.5)

    save(fig, "ibex-on-cliff")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    print(f"Output: {OUT}/\n")

    fig_terrace_overview()
    fig_one_direction()
    fig_three_surveys()
    fig_comparison_rock()
    fig_phantom_register()
    fig_ibex_on_cliff()

    print(f"\nDone — 6 figures saved to {OUT}/")
    if args.show:
        plt.show()


if __name__ == "__main__":
    main()
