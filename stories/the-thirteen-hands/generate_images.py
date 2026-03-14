# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib>=3.9", "numpy>=1.26"]
# ///
"""
The Thirteen Hands — 6 illustrations
Setting: Bharmour, upper Ravi valley, Chaurasi temple complex
Kath-Kuni construction — dolomite and deodar cedar

Six figures:
  1. chaurasi-plan.png    — schematic plan of the Chaurasi complex
  2. foraging-styles.png  — four ways of looking at the same wall
  3. convergence-map.png  — the western wall, marked by agreement
  4. ledger-page.png      — the master mason's comparison ledger
  5. cost-depth.png       — cost against depth (the bend)
  6. bharmour-view.png    — the view south from Bharmour

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

SLUG = Path(__file__).parent.name
OUT = (Path(__file__).parent / f"../../website/static/images/writing/{SLUG}").resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 7

# ── Palette: Bharmour / Kath-Kuni / dolomite + cedar ─────────────────
BG_DARK = "#12121E"         # night background (consistent with other stories)
DOLOMITE = "#C8BFA8"        # grey dolomite stone
DOLOMITE_DARK = "#8A8478"   # shadowed stone
CEDAR = "#6B5B4B"           # deodar timber courses
CEDAR_LIGHT = "#8B7B6B"     # lit timber
CHALK = "#E8E4D8"           # chalk / text colour
COPPER = "#C4886B"          # copper accent (from route-books palette)
WATER = "#4A8B6B"           # Ravi river, Budhil nala
DEODAR = "#4A6B48"          # deodar green
SNOW_PEAK = "#E8E0D8"       # Mani Mahesh peak
SKY_DUSK = "#2A2838"        # evening sky
PANEL_DARK = "#1A1A2A"      # dark panel for agreement map
PANEL_MID = "#3A3848"       # mid-agreement
PANEL_LIGHT = "#6A6878"     # low-agreement
PANEL_WHITE = "#9A98A8"     # minimal agreement
RED_ACCENT = "#C0605A"      # disagreement / damage marker
AMBER = "#D4A86B"           # lantern / lamplight


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


# ── Figure 1: Chaurasi complex plan ──────────────────────────────────

def fig_chaurasi_plan():
    fig, ax = make_fig(12, 8)

    # Draw ~30 small temple footprints as rectangles
    rng = np.random.default_rng(84)
    temples_x = rng.uniform(15, 85, 30)
    temples_y = rng.uniform(20, 80, 30)

    for i, (tx, ty) in enumerate(zip(temples_x, temples_y)):
        w = rng.uniform(2, 4)
        h = rng.uniform(2, 4)
        color = DOLOMITE_DARK if i != 7 else COPPER  # highlight Lakshmi Devi
        alpha = 0.4 if i != 7 else 0.9
        lw = 0.5 if i != 7 else 1.5
        rect = Rectangle((tx - w/2, ty - h/2), w, h, linewidth=lw,
                          edgecolor=color, facecolor="none", alpha=alpha)
        ax.add_patch(rect)

    # Label the highlighted temple
    ax.annotate("Lakshmi Devi\ntemple", xy=(temples_x[7], temples_y[7]),
                xytext=(temples_x[7] + 12, temples_y[7] + 10),
                fontsize=8, color=COPPER, fontstyle="italic",
                arrowprops=dict(arrowstyle="->", color=COPPER, lw=0.8))

    # Mark the western wall
    lx = temples_x[7] - 2
    ax.plot([lx, lx], [temples_y[7] - 2, temples_y[7] + 2],
            color=RED_ACCENT, lw=2.5, alpha=0.8)
    ax.text(lx - 4, temples_y[7], "W\nwall", fontsize=6, color=RED_ACCENT,
            ha="center", va="center")

    # Title
    ax.text(50, 95, "The Chaurasi Complex — Eighty-Four Temples",
            fontsize=12, color=CHALK, ha="center", va="top",
            fontfamily="serif")
    ax.text(50, 6, "Bharmour · Upper Ravi Valley · 32.44°N, 76.54°E",
            fontsize=8, color=DOLOMITE_DARK, ha="center", va="bottom",
            fontfamily="serif")

    # Terrace edge (cliff)
    xs = np.linspace(5, 95, 100)
    ys = 12 + np.sin(xs * 0.08) * 2 + np.random.default_rng(1).normal(0, 0.3, 100)
    ax.plot(xs, ys, color=DOLOMITE_DARK, lw=1.0, alpha=0.5)
    ax.text(50, 9, "terrace edge", fontsize=6, color=DOLOMITE_DARK,
            ha="center", fontstyle="italic")

    save(fig, "chaurasi-plan")


# ── Figure 2: Four foraging styles ───────────────────────────────────

def fig_foraging_styles():
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.patch.set_facecolor(BG_DARK)

    styles = [
        ("The Touch-Reader", "Follows the grain, panel by panel",
         "linear", COPPER),
        ("The Pattern-Tracer", "Follows cracks across walls",
         "branching", RED_ACCENT),
        ("The Surface-Lister", "Inventories everything before examining",
         "grid", WATER),
        ("The Panel-Reader", "Reads section by section",
         "sections", DOLOMITE),
    ]

    for ax, (title, subtitle, pattern, color) in zip(axes.flat, styles):
        ax.set_facecolor(BG_DARK)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")

        # Draw a simplified wall (5 panels)
        for i in range(5):
            x0 = 10 + i * 16
            rect = Rectangle((x0, 25), 14, 50, linewidth=0.8,
                              edgecolor=DOLOMITE_DARK, facecolor="none",
                              alpha=0.5)
            ax.add_patch(rect)

        # Draw the path overlay
        rng = np.random.default_rng(42)
        if pattern == "linear":
            # Single line through panels left to right
            xs = np.linspace(12, 88, 60)
            ys = 50 + np.sin(xs * 0.15) * 5
            ax.plot(xs, ys, color=color, lw=2, alpha=0.8)
        elif pattern == "branching":
            # Starts at one panel, branches across multiple
            for start_y in [40, 50, 60]:
                xs = np.linspace(15, 85, 40)
                ys = start_y + rng.normal(0, 1, 40).cumsum() * 0.5
                ax.plot(xs, ys, color=color, lw=1.2, alpha=0.6)
        elif pattern == "grid":
            # Systematic grid across all panels first
            for i in range(5):
                x = 17 + i * 16
                ax.plot([x, x], [28, 72], color=color, lw=1, alpha=0.4,
                        ls="--")
            for y in [35, 50, 65]:
                ax.plot([12, 88], [y, y], color=color, lw=1, alpha=0.4,
                        ls="--")
        elif pattern == "sections":
            # One panel at a time, with a marker
            for i in range(5):
                x = 17 + i * 16
                ax.plot(x, 50, "o", color=color, ms=6, alpha=0.7)
                if i < 4:
                    ax.annotate("", xy=(x + 14, 50), xytext=(x + 2, 50),
                                arrowprops=dict(arrowstyle="->", color=color,
                                                lw=0.8, alpha=0.5))

        ax.text(50, 90, title, fontsize=10, color=color, ha="center",
                fontfamily="serif", fontweight="bold")
        ax.text(50, 82, subtitle, fontsize=7, color=CHALK, ha="center",
                fontstyle="italic", alpha=0.7)

    fig.suptitle("Four Ways of Looking at the Same Wall",
                 fontsize=13, color=CHALK, fontfamily="serif", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save(fig, "foraging-styles")


# ── Figure 3: Convergence map ────────────────────────────────────────

def fig_convergence_map():
    fig, ax = make_fig(12, 6)

    # Wall grid: 5 rows × 10 columns of panels
    rng = np.random.default_rng(13)
    n_rows, n_cols = 4, 10
    panel_w, panel_h = 7, 12

    # Agreement levels (how many of 13 hands found damage here)
    agreements = rng.choice([0, 0, 0, 2, 3, 5, 7, 11, 12, 13],
                            size=(n_rows, n_cols), p=[0.3, 0.1, 0.1,
                            0.1, 0.05, 0.1, 0.05, 0.1, 0.05, 0.05])
    # Ensure a few strong consensus panels
    agreements[1, 4] = 13  # the lintel crack
    agreements[0, 7] = 11  # the phantom
    agreements[2, 2] = 5
    agreements[3, 8] = 3

    for r in range(n_rows):
        for c in range(n_cols):
            x0 = 10 + c * (panel_w + 1)
            y0 = 15 + r * (panel_h + 1)
            a = agreements[r, c]

            if a >= 11:
                color = COPPER
                alpha = 0.9
            elif a >= 7:
                color = AMBER
                alpha = 0.6
            elif a >= 4:
                color = DOLOMITE_DARK
                alpha = 0.5
            elif a >= 1:
                color = PANEL_LIGHT
                alpha = 0.3
            else:
                color = PANEL_DARK
                alpha = 0.15

            rect = Rectangle((x0, y0), panel_w, panel_h,
                              linewidth=0.5, edgecolor=DOLOMITE_DARK,
                              facecolor=color, alpha=alpha)
            ax.add_patch(rect)

            if a > 0:
                ax.text(x0 + panel_w/2, y0 + panel_h/2, str(a),
                        fontsize=6, color=CHALK if a >= 7 else DOLOMITE_DARK,
                        ha="center", va="center", alpha=0.8)

    # Title and legend
    ax.text(50, 92, "The Western Wall — Marked by Agreement",
            fontsize=12, color=CHALK, ha="center", fontfamily="serif")
    ax.text(50, 85, "Numbers show how many of thirteen hands found damage at each panel",
            fontsize=7, color=DOLOMITE_DARK, ha="center", fontstyle="italic")

    # Legend
    legend_y = 5
    for label, color, alpha in [("11–13: the wall's testimony", COPPER, 0.9),
                                ("7–10: probable", AMBER, 0.6),
                                ("4–6: uncertain", DOLOMITE_DARK, 0.5),
                                ("1–3: individual", PANEL_LIGHT, 0.3)]:
        rect = Rectangle((12, legend_y), 3, 2, facecolor=color, alpha=alpha,
                          edgecolor="none")
        ax.add_patch(rect)
        ax.text(17, legend_y + 1, label, fontsize=6, color=CHALK,
                va="center", alpha=0.7)
        legend_y -= 3.5

    save(fig, "convergence-map")


# ── Figure 4: Ledger page ────────────────────────────────────────────

def fig_ledger_page():
    fig, ax = make_fig(12, 8)

    # Draw ruled lines on a ledger
    ax.add_patch(Rectangle((8, 5), 84, 88, facecolor="#1E1E2C",
                            edgecolor=DOLOMITE_DARK, lw=0.8, alpha=0.8))

    # Binding margin
    ax.plot([18, 18], [5, 93], color=RED_ACCENT, lw=0.6, alpha=0.4)

    # Column headers
    headers = ["Hand", "Gaps", "Spec?", "Self-\naccount", "Cost", "No."]
    col_xs = [22, 36, 48, 60, 72, 82]
    for x, h in zip(col_xs, headers):
        ax.text(x, 89, h, fontsize=7, color=COPPER, ha="center",
                fontfamily="serif", fontweight="bold", va="top")

    # Horizontal rule under header
    ax.plot([20, 88], [87, 87], color=DOLOMITE_DARK, lw=0.5, alpha=0.5)

    # 13 rows of data (simplified)
    carvers = [
        ("Chamba", "5", "Yes", "Good", "·", "42"),
        ("Kinnaur I", "4", "Yes", "Good", "··", "42"),
        ("Kinnaur II", "3", "Yes", "Exc.", "··", "42"),
        ("Kinnaur III", "6", "Yes", "Adeq.", "··", "42"),
        ("Kullu I", "12", "No*", "Exc.", "····", "—"),
        ("Kullu II", "7", "No*", "Exc.", "···", "—"),
        ("Sutlej", "5", "Yes", "Strong", "····", "42"),
        ("Mandi", "4", "Yes", "Adeq.", "·", "42"),
        ("Lahaul", "9†", "Yes†", "Weak", "·", "42"),
        ("Baltistan", "5", "Yes", "Good", "·", "42"),
        ("Chamba II", "7", "Yes", "Good", "··", "42"),
        ("Bushahr", "~8", "Yes", "Exc.", "··", "42"),
        ("Mandi II", "7", "Yes", "Good", "··", "42"),
    ]

    for i, (name, gaps, spec, refl, cost, num) in enumerate(carvers):
        y = 84 - i * 5.5
        vals = [name, gaps, spec, refl, cost, num]
        for x, v in zip(col_xs, vals):
            color = CHALK
            if v == "No*":
                color = RED_ACCENT
            elif v == "Exc.":
                color = WATER
            elif v == "42":
                color = AMBER
            ax.text(x, y, v, fontsize=6, color=color, ha="center",
                    va="center", fontfamily="serif", alpha=0.85)

        # Ruled line
        ax.plot([20, 88], [y - 2.5, y - 2.5], color=DOLOMITE_DARK,
                lw=0.3, alpha=0.2)

    # Footnotes
    ax.text(20, 9, "* Refused to write — improved existing specification instead",
            fontsize=5, color=RED_ACCENT, alpha=0.6, fontstyle="italic")
    ax.text(20, 6.5, "† Catalogue only, no specific findings",
            fontsize=5, color=DOLOMITE_DARK, alpha=0.6, fontstyle="italic")

    ax.text(50, 96, "The Master Mason's Comparison Ledger",
            fontsize=11, color=CHALK, ha="center", fontfamily="serif")

    save(fig, "ledger-page")


# ── Figure 5: Cost vs depth ──────────────────────────────────────────

def fig_cost_depth():
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARK)

    # Stylised cost vs findings (not exact data — story-world translation)
    # Carver names, findings, relative cost (1 = cheapest)
    carvers = [
        ("Chamba", 5, 1), ("Mandi", 4, 1.5), ("Lahaul", 0, 2),
        ("Baltistan", 5, 3), ("Kinnaur I", 4, 3), ("Kinnaur II", 3, 3.5),
        ("Kinnaur III", 6, 4), ("Chamba II", 7, 6),
        ("Mandi II", 7, 6), ("Sutlej", 5, 10),
        ("Bushahr", 8, 20), ("Kullu II", 7, 25),
        ("Kullu I", 12, 40),
    ]

    names = [c[0] for c in carvers]
    findings = [c[1] for c in carvers]
    costs = [c[2] for c in carvers]

    colors = [COPPER if f > 0 else RED_ACCENT for f in findings]
    ax.scatter(findings, costs, c=colors, s=80, zorder=3,
               edgecolors=CHALK, linewidths=0.5, alpha=0.85)

    for name, f, c in carvers:
        offset_x = 0.3
        offset_y = c * 0.1 + 0.5
        ax.annotate(name, (f, c), fontsize=6, color=CHALK,
                    xytext=(f + offset_x, c + offset_y),
                    arrowprops=dict(arrowstyle="-", color=DOLOMITE_DARK,
                                    lw=0.4),
                    alpha=0.7)

    ax.set_yscale("log")
    ax.set_xlabel("Findings", fontsize=9, color=CHALK, fontfamily="serif")
    ax.set_ylabel("Relative cost (log scale)", fontsize=9, color=CHALK,
                  fontfamily="serif")
    ax.set_title("Cost Against Depth — The Bend",
                 fontsize=12, color=CHALK, fontfamily="serif", pad=15)

    # Style the axes
    ax.tick_params(colors=DOLOMITE_DARK, labelsize=7)
    ax.spines["bottom"].set_color(DOLOMITE_DARK)
    ax.spines["left"].set_color(DOLOMITE_DARK)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.15, color=DOLOMITE_DARK)

    # Annotation: the bend
    ax.annotate("the bend — cost rises\nfaster than depth",
                xy=(8, 15), xytext=(2, 25), fontsize=7, color=AMBER,
                fontstyle="italic",
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=0.8))

    fig.tight_layout()
    save(fig, "cost-depth")


# ── Figure 6: View from Bharmour ─────────────────────────────────────

def fig_bharmour_view():
    fig, ax = make_fig(14, 7)

    # Sky gradient
    for i in range(100):
        y = i
        t = i / 100
        r = int(0x12 + (0x2A - 0x12) * t)
        g = int(0x12 + (0x28 - 0x12) * t)
        b = int(0x1E + (0x38 - 0x1E) * t)
        ax.axhspan(y, y + 1, color=f"#{r:02x}{g:02x}{b:02x}", alpha=0.7)

    # Mountain ridges (layered, back to front)
    rng = np.random.default_rng(5653)

    # Far ridge (Mani Mahesh area)
    xs = np.linspace(0, 100, 200)
    ys_far = 70 + 15 * np.exp(-((xs - 45) ** 2) / 300) + rng.normal(0, 0.5, 200)
    # Snow peak
    ax.fill_between(xs, 55, ys_far, color="#2A2838", alpha=0.8)
    # Snow cap
    snow_mask = ys_far > 78
    ax.fill_between(xs[snow_mask], ys_far[snow_mask] - 3, ys_far[snow_mask],
                    color=SNOW_PEAK, alpha=0.4)

    # Mid ridge
    ys_mid = 48 + 8 * np.sin(xs * 0.05) + rng.normal(0, 0.4, 200)
    ax.fill_between(xs, 35, ys_mid, color=DEODAR, alpha=0.5)

    # Near ridge (deodar forest)
    ys_near = 30 + 5 * np.sin(xs * 0.08 + 1) + rng.normal(0, 0.3, 200)
    ax.fill_between(xs, 20, ys_near, color="#2A3A28", alpha=0.7)

    # Valley floor / river
    ax.fill_between(xs, 15, 22, color=WATER, alpha=0.15)
    # River line
    river_ys = 18 + np.sin(xs * 0.1) * 1.5
    ax.plot(xs, river_ys, color=WATER, lw=1.2, alpha=0.5)

    # Foreground (dark)
    ax.fill_between(xs, 0, 16, color="#0A0A12", alpha=0.9)

    # Thread Walker (small figure walking south)
    walker_x, walker_y = 60, 17
    ax.plot([walker_x, walker_x], [walker_y, walker_y + 2.5],
            color=CHALK, lw=1.2, alpha=0.7)  # body
    ax.plot(walker_x, walker_y + 3, "o", color=CHALK, ms=3, alpha=0.7)  # head
    ax.plot([walker_x - 0.8, walker_x + 1], [walker_y + 1.5, walker_y + 1.5],
            color=CHALK, lw=0.8, alpha=0.5)  # arms

    # Labels
    ax.text(45, 83, "Mani Mahesh\n5,653m", fontsize=7, color=SNOW_PEAK,
            ha="center", fontstyle="italic", alpha=0.7)
    ax.text(75, 19, "Budhil nala →", fontsize=6, color=WATER,
            fontstyle="italic", alpha=0.5)
    ax.text(50, 5, "The view south from Bharmour",
            fontsize=10, color=CHALK, ha="center", fontfamily="serif",
            alpha=0.8)

    save(fig, "bharmour-view")


# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    print(f"Output: {OUT}/\n")

    fig_chaurasi_plan()
    fig_foraging_styles()
    fig_convergence_map()
    fig_ledger_page()
    fig_cost_depth()
    fig_bharmour_view()

    print(f"\nDone — 6 figures saved to {OUT}/")
    if args.show:
        plt.show()


if __name__ == "__main__":
    main()
