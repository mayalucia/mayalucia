# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib>=3.9", "numpy>=1.26"]
# ///
"""
The Seven Readers — 20 illustrated panels
Setting: Thalpan petroglyph terrace, Indus gorge, Nanga Parbat

Story #20. Image-primary format: each panel carries the narrative,
text bubbles overlay or sit below.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

SLUG = "the-seven-readers"
OUT = (Path(__file__).parent / f"../../website/static/images/writing/{SLUG}").resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 14, 8  # wider panels for the image-primary format → 2100×1200 px

# ── Palette: Indus gorge / Thalpan petroglyph register ──────────────
GORGE_DARK = "#1A1816"       # deep gorge shadow
GNEISS = "#4A4845"           # Indian plate gneiss (pale when lit)
GNEISS_LIGHT = "#8A8580"     # lit gneiss face
ARC_BASALT = "#2A2826"       # Kohistan arc rock (dark)
ARC_GREEN = "#3A4038"        # dark greenish tint of arc volcanic
CARVED = "#C8C0B0"           # petroglyph carved surface (exposed lighter rock)
CARVED_OLD = "#9A9488"       # weathered carving
INDUS = "#5888A8"            # river blue
INDUS_DEEP = "#3A6080"       # deep water
SKY_DAWN = "#E8D8C8"         # warm dawn sky
SKY_NOON = "#C8D8E8"         # cool midday
SKY_DUSK = "#D8A880"         # dusk alpenglow
ALPENGLOW = "#E8A8A0"        # pink on snow
SNOW = "#F0EDE8"             # summit snow
ICE = "#D8E4F0"              # glacier blue-white
SHADOW = "#0A0A08"           # deep shadow
STONE_WARM = "#B8A890"       # warm sandstone
STONE_COOL = "#98A0A8"       # cool stone
JUNIPER = "#4A5840"          # sparse juniper


def make_fig(width=W, height=H, bg=GORGE_DARK):
    fig, ax = plt.subplots(1, 1, figsize=(width, height))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=DPI, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f"  ✓ {name}.png")


# ── Drawing primitives ──────────────────────────────────────────────

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


def mountain_profile(ax, peaks, base_y, fill_color, edge_color=None, alpha=1.0):
    """Draw a mountain ridge from a list of (x, y) peak points."""
    xs = np.array([0] + [p[0] for p in peaks] + [100], dtype=float)
    ys = np.array([base_y] + [p[1] for p in peaks] + [base_y], dtype=float)
    xnew = np.linspace(0, 100, 300)
    ynew = np.interp(xnew, xs, ys)
    # Smooth with a moving average
    kernel = np.ones(15) / 15
    ynew = np.convolve(ynew, kernel, mode="same")
    ynew[:7] = np.interp(xnew[:7], xs, ys)[:7]
    ynew[-7:] = np.interp(xnew[-7:], xs, ys)[-7:]
    ax.fill_between(xnew, base_y, ynew, color=fill_color, alpha=alpha)
    if edge_color:
        ax.plot(xnew, ynew, color=edge_color, lw=0.8, alpha=0.6)


def draw_ibex(ax, cx, cy, scale=1.0, color=CARVED, facing="right"):
    """Petroglyph-style ibex silhouette."""
    flip = 1 if facing == "right" else -1
    s = scale
    # Body (horizontal oval)
    body = mpatches.Ellipse((cx, cy), 4*s, 1.8*s, color=color, lw=0)
    ax.add_patch(body)
    # Legs (4 lines)
    for dx in [-1.2, -0.6, 0.6, 1.2]:
        ax.plot([cx + dx*s*flip, cx + dx*s*flip + 0.2*s*flip],
                [cy - 0.9*s, cy - 2.2*s], color=color, lw=1.5*s)
    # Head
    ax.plot([cx + 2*s*flip, cx + 3*s*flip], [cy + 0.2*s, cy + 0.8*s],
            color=color, lw=2*s)
    # Horns — swept-back curves
    horn_t = np.linspace(0, 1, 20)
    hx = cx + (3 + horn_t * 1.5) * s * flip
    hy = cy + (0.8 + horn_t * 2.5 - horn_t**2 * 1.0) * s
    ax.plot(hx, hy, color=color, lw=2*s)


def draw_stupa(ax, cx, cy, scale=1.0, color=CARVED):
    """Petroglyph-style stupa."""
    s = scale
    # Base platform
    ax.fill_between([cx-2*s, cx+2*s], cy, cy+0.5*s, color=color, alpha=0.8)
    # Dome (half circle)
    theta = np.linspace(0, np.pi, 40)
    dx = 1.8 * s * np.cos(theta)
    dy = 1.5 * s * np.sin(theta) + cy + 0.5*s
    ax.fill(cx + dx, dy, color=color, alpha=0.7)
    # Yashti (pole)
    ax.plot([cx, cx], [cy + 2*s, cy + 4*s], color=color, lw=1.5*s)
    # Chattravali (umbrellas) — small horizontal dashes
    for i in range(3):
        yy = cy + 2.5*s + i * 0.5*s
        ax.plot([cx - 0.6*s, cx + 0.6*s], [yy, yy], color=color, lw=1.2*s)


def draw_stone(ax, cx, cy, w, h, color=STONE_WARM, marks=None, mark_color=CARVED,
               seed=42, rotation=0):
    """A flat stone with optional marks (dense/sparse/terse etc)."""
    rng = np.random.default_rng(seed)
    # Rounded rectangle for the stone
    stone = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                           boxstyle="round,pad=0.3",
                           facecolor=color, edgecolor=GNEISS_LIGHT,
                           lw=0.8, alpha=0.9)
    if rotation:
        import matplotlib.transforms as mtransforms
        t = mtransforms.Affine2D().rotate_deg_around(cx, cy, rotation) + ax.transData
        stone.set_transform(t)
    ax.add_patch(stone)

    if marks == "dense":
        for _ in range(60):
            mx = rng.uniform(cx - w/2 + 0.5, cx + w/2 - 0.5)
            my = rng.uniform(cy - h/2 + 0.3, cy + h/2 - 0.3)
            ml = rng.uniform(0.3, 1.2)
            ax.plot([mx, mx + ml], [my, my + rng.uniform(-0.2, 0.2)],
                    color=mark_color, lw=0.6, alpha=0.7)
    elif marks == "sparse":
        for _ in range(25):
            mx = rng.uniform(cx - w/2 + 0.8, cx + w/2 - 0.8)
            my = rng.uniform(cy - h/2 + 0.5, cy + h/2 - 0.5)
            ml = rng.uniform(0.5, 1.5)
            ax.plot([mx, mx + ml], [my, my + rng.uniform(-0.1, 0.1)],
                    color=mark_color, lw=0.8, alpha=0.6)
    elif marks == "terse":
        for _ in range(10):
            mx = rng.uniform(cx - w/2 + 1, cx + w/2 - 1)
            my = rng.uniform(cy - h/2 + 0.5, cy + h/2 - 0.5)
            ml = rng.uniform(0.8, 2.0)
            ax.plot([mx, mx + ml], [my, my + rng.uniform(-0.1, 0.1)],
                    color=mark_color, lw=1.0, alpha=0.8)
    elif marks == "philosophical":
        # Circular/curved marks
        for _ in range(15):
            mx = rng.uniform(cx - w/2 + 1, cx + w/2 - 1)
            my = rng.uniform(cy - h/2 + 0.5, cy + h/2 - 0.5)
            theta = np.linspace(0, rng.uniform(1, 4), 15)
            r = rng.uniform(0.3, 0.8)
            ax.plot(mx + r * np.cos(theta), my + r * np.sin(theta),
                    color=mark_color, lw=0.6, alpha=0.6)
    elif marks == "analytical":
        # Grid-like marks — structured
        for i in range(6):
            my = cy - h/2 + 0.5 + i * (h - 1) / 6
            ax.plot([cx - w/2 + 0.5, cx + w/2 - 0.5], [my, my],
                    color=mark_color, lw=0.5, alpha=0.4)
        for _ in range(30):
            mx = rng.uniform(cx - w/2 + 0.5, cx + w/2 - 0.5)
            my = rng.uniform(cy - h/2 + 0.3, cy + h/2 - 0.3)
            ml = rng.uniform(0.4, 1.0)
            ax.plot([mx, mx + ml], [my, my], color=mark_color, lw=0.7, alpha=0.65)
    elif marks == "operational":
        # Tiered marks — grouped in clusters
        for tier in range(3):
            ty = cy - h/2 + 0.8 + tier * (h - 1.5) / 3
            for _ in range(8):
                mx = rng.uniform(cx - w/2 + 0.5, cx + w/2 - 0.5)
                ml = rng.uniform(0.5, 1.5)
                ax.plot([mx, mx + ml], [ty + rng.uniform(-0.2, 0.2),
                        ty + rng.uniform(-0.2, 0.2)],
                        color=mark_color, lw=0.7, alpha=0.6)
    elif marks == "questions":
        # Scattered dots and short question-mark curves
        for _ in range(12):
            mx = rng.uniform(cx - w/2 + 1, cx + w/2 - 1)
            my = rng.uniform(cy - h/2 + 0.5, cy + h/2 - 0.5)
            ax.plot(mx, my, 'o', color=mark_color, ms=2, alpha=0.5)
            # Small hook
            hook_t = np.linspace(0, 2.5, 10)
            ax.plot(mx + 0.3 * np.sin(hook_t), my + 0.15 * hook_t,
                    color=mark_color, lw=0.5, alpha=0.4)


def river(ax, y_center=15, width=8, color=INDUS, alpha=0.7):
    """Horizontal river band."""
    xs = np.linspace(0, 100, 200)
    rng = np.random.default_rng(7)
    upper = y_center + width/2 + 0.8 * np.sin(xs * 0.08) + rng.normal(0, 0.15, 200).cumsum() * 0.02
    lower = y_center - width/2 + 0.6 * np.sin(xs * 0.1 + 1) + rng.normal(0, 0.15, 200).cumsum() * 0.02
    ax.fill_between(xs, lower, upper, color=color, alpha=alpha)
    # Current lines
    for _ in range(8):
        y = rng.uniform(y_center - width/3, y_center + width/3)
        x0 = rng.uniform(0, 60)
        xl = np.linspace(x0, x0 + rng.uniform(15, 35), 40)
        yl = y + 0.3 * np.sin(xl * 0.3 + rng.uniform(0, 6))
        ax.plot(xl, yl, color=INDUS_DEEP, alpha=0.3, lw=0.5)


# ── Panel compositions ──────────────────────────────────────────────

def panel_01_gorge_dawn():
    """The gorge at dawn — Indus below, Nanga Parbat above."""
    fig, ax = make_fig(bg=SKY_DAWN)
    # Sky gradient
    for i in range(100):
        y = 50 + i * 0.5
        t = i / 100
        c = np.array([0.91, 0.85, 0.78]) * (1-t) + np.array([0.58, 0.68, 0.80]) * t
        ax.axhspan(y, y + 0.5, color=c, alpha=0.8)
    # Distant snow peaks
    mountain_profile(ax, [(15, 88), (30, 82), (45, 92), (55, 85), (70, 90), (85, 80)],
                     65, SNOW, alpha=0.6)
    # Nanga Parbat — the dominant peak
    mountain_profile(ax, [(35, 78), (48, 95), (55, 92), (62, 80)],
                     60, GNEISS_LIGHT, edge_color=SNOW, alpha=0.8)
    # Alpenglow on summit
    ax.fill_between([42, 52], [92, 92], [95, 95], color=ALPENGLOW, alpha=0.4)
    # Near ridges (dark)
    mountain_profile(ax, [(10, 55), (25, 62), (40, 58), (60, 65), (80, 60), (95, 55)],
                     35, GNEISS, alpha=0.9)
    # Gorge walls
    mountain_profile(ax, [(5, 48), (20, 52), (35, 45), (50, 50), (65, 48), (80, 52), (95, 45)],
                     20, ARC_BASALT, alpha=0.95)
    rock_texture(ax, 0, 20, 100, 50, color=GNEISS_LIGHT, n=30)
    # River
    river(ax, y_center=12, width=10)
    # Foreground terrace (where we stand)
    ax.fill_between([0, 100], 0, 8, color=STONE_WARM, alpha=0.6)
    rock_texture(ax, 0, 0, 100, 8, color=CARVED_OLD, n=15, seed=99)
    save(fig, "panel-01-gorge-dawn")


def panel_02_terrace():
    """The petroglyph terrace at Thalpan — density of marks on dark rock."""
    fig, ax = make_fig(bg=ARC_BASALT)
    # Rock face filling most of canvas
    ax.fill_between([0, 100], 10, 90, color=GORGE_DARK, alpha=0.9)
    rock_texture(ax, 0, 10, 100, 90, color=GNEISS, n=60, seed=11)
    # Petroglyphs scattered across the face
    rng = np.random.default_rng(42)
    for _ in range(12):
        x = rng.uniform(10, 90)
        y = rng.uniform(20, 80)
        s = rng.uniform(0.4, 1.2)
        if rng.random() > 0.4:
            draw_ibex(ax, x, y, scale=s, color=CARVED,
                      facing="right" if rng.random() > 0.5 else "left")
        else:
            draw_stupa(ax, x, y, scale=s, color=CARVED_OLD)
    # Ground
    ax.fill_between([0, 100], 0, 10, color=STONE_WARM, alpha=0.5)
    save(fig, "panel-02-terrace")


def panel_03_ibex_closeup():
    """Close-up: a single ibex carved 8,000 years ago."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=80, seed=33)
    # Single large ibex center
    draw_ibex(ax, 50, 50, scale=5.0, color=CARVED)
    # Patina/weathering around it
    rng = np.random.default_rng(55)
    for _ in range(30):
        x = rng.uniform(20, 80)
        y = rng.uniform(20, 80)
        ax.plot(x, y, '.', color=CARVED_OLD, ms=rng.uniform(1, 3), alpha=0.3)
    save(fig, "panel-03-ibex-closeup")


def panel_04_stupa_around_ibex():
    """A Buddhist stupa carved around an ibex — accumulation, not erasure."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=70, seed=44)
    # Ibex first (older, more weathered)
    draw_ibex(ax, 50, 45, scale=3.0, color=CARVED_OLD)
    # Stupa carved around/over it (brighter, newer)
    draw_stupa(ax, 50, 35, scale=3.5, color=CARVED)
    save(fig, "panel-04-stupa-ibex")


def panel_05_seven_stones():
    """Seven flat stones laid on the terrace."""
    fig, ax = make_fig(bg=STONE_WARM)
    rock_texture(ax, 0, 0, 100, 100, color=CARVED_OLD, n=40, seed=55)
    # Seven stones in a loose semicircle
    positions = [
        (20, 55, 5), (35, 65, -8), (50, 68, 2),
        (65, 65, -5), (80, 55, 7),
        (30, 40, 10), (70, 40, -3),
    ]
    colors = [GNEISS_LIGHT, STONE_COOL, "#A0988C", GNEISS_LIGHT,
              STONE_COOL, "#B0A898", STONE_WARM]
    for i, (x, y, rot) in enumerate(positions):
        draw_stone(ax, x, y, 10, 6, color=colors[i], rotation=rot, seed=60+i)
    # River at bottom
    river(ax, y_center=8, width=6)
    save(fig, "panel-05-seven-stones")


def panel_06_stone_dense():
    """First stone: dense marks — the architect's map."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=30, seed=66)
    draw_stone(ax, 50, 50, 40, 28, color=GNEISS_LIGHT, marks="dense",
               mark_color=CARVED, seed=61)
    save(fig, "panel-06-stone-architect")


def panel_07_stone_sparse():
    """Second stone: sparse, structural — the taxonomist's map."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=30, seed=77)
    draw_stone(ax, 50, 50, 40, 28, color=STONE_COOL, marks="sparse",
               mark_color=CARVED, seed=62)
    save(fig, "panel-07-stone-taxonomist")


def panel_08_stone_terse():
    """Third stone: terse, telegraphic — the builder's sketch."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=30, seed=88)
    draw_stone(ax, 50, 50, 40, 28, color="#A0988C", marks="terse",
               mark_color=CARVED, seed=63)
    save(fig, "panel-08-stone-builder")


def panel_09_stone_philosophical():
    """Fourth stone: philosophical, curved — the traveller's map."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=30, seed=99)
    draw_stone(ax, 50, 50, 40, 28, color=GNEISS_LIGHT, marks="philosophical",
               mark_color=CARVED, seed=64)
    save(fig, "panel-09-stone-traveller")


def panel_10_stone_analytical():
    """Fifth stone: analytical, gridded — the cartographer's own map."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=30, seed=100)
    draw_stone(ax, 50, 50, 40, 28, color=STONE_COOL, marks="analytical",
               mark_color=CARVED, seed=65)
    save(fig, "panel-10-stone-cartographer")


def panel_11_stone_operational():
    """Sixth stone: operational, tiered — the inspector's map."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=30, seed=111)
    draw_stone(ax, 50, 50, 40, 28, color="#B0A898", marks="operational",
               mark_color=CARVED, seed=66)
    save(fig, "panel-11-stone-inspector")


def panel_12_stone_questions():
    """Seventh stone: mostly questions — the newcomer's uncertain marks."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=30, seed=122)
    draw_stone(ax, 50, 50, 40, 28, color=STONE_WARM, marks="questions",
               mark_color=CARVED_OLD, seed=67)
    save(fig, "panel-12-stone-newcomer")


def panel_13_cross_reader():
    """A reader picks up a stone not her own — cross-lineage."""
    fig, ax = make_fig(bg=STONE_WARM)
    rock_texture(ax, 0, 0, 100, 100, color=CARVED_OLD, n=25, seed=133)
    # Two stones: one being "read" (lifted, bright), one remaining
    draw_stone(ax, 35, 45, 10, 6, color=STONE_COOL, marks="operational",
               mark_color=CARVED, seed=66, rotation=-5)
    # The "reader's own" stone, set aside
    draw_stone(ax, 70, 55, 10, 6, color="#A0988C", marks="terse",
               mark_color=CARVED_OLD, seed=63, rotation=12)
    # Hands suggested by two curved lines reaching toward the operational stone
    ax.plot([55, 42], [60, 52], color=CARVED, lw=2, alpha=0.5)
    ax.plot([57, 44], [58, 50], color=CARVED, lw=2, alpha=0.5)
    # River at bottom
    river(ax, y_center=10, width=8)
    save(fig, "panel-13-cross-reader")


def panel_14_audit_to_builder():
    """The audit-stone read by the builder — densest exchange."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=35, seed=144)
    # The operational/audit stone (larger, central)
    draw_stone(ax, 40, 50, 35, 24, color="#B0A898", marks="operational",
               mark_color=CARVED, seed=66)
    # Small terse stone nearby — the builder's own, for contrast
    draw_stone(ax, 82, 30, 12, 7, color="#A0988C", marks="terse",
               mark_color=CARVED_OLD, seed=63, rotation=15)
    # Arrow/flow line suggesting reading direction
    ax.annotate("", xy=(78, 33), xytext=(60, 45),
                arrowprops=dict(arrowstyle="->", color=CARVED, lw=1.5, alpha=0.4))
    save(fig, "panel-14-audit-to-builder")


def panel_15_cartographer_to_newcomer():
    """The cartographer's stone read by the newcomer — the rescue."""
    fig, ax = make_fig(bg=GORGE_DARK)
    rock_texture(ax, 0, 0, 100, 100, color=GNEISS, n=35, seed=155)
    # Analytical stone (the cartographer's — rich, structured)
    draw_stone(ax, 40, 50, 35, 24, color=STONE_COOL, marks="analytical",
               mark_color=CARVED, seed=65)
    # Question stone (newcomer's own) set aside, smaller
    draw_stone(ax, 82, 30, 12, 7, color=STONE_WARM, marks="questions",
               mark_color=CARVED_OLD, seed=67, rotation=-8)
    # Light falling on the analytical stone — "illumination"
    for i in range(5):
        y = 58 + i * 2
        ax.plot([25, 55], [y, y - 3], color=SKY_DAWN, alpha=0.06, lw=3)
    save(fig, "panel-15-cartographer-to-newcomer")


def panel_16_gorge_midday():
    """The gorge at midday — shadows shorter, suture zone visible."""
    fig, ax = make_fig(bg=SKY_NOON)
    # Sky
    for i in range(50):
        y = 50 + i
        t = i / 50
        c = np.array([0.78, 0.85, 0.91]) * (1-t*0.3)
        ax.axhspan(y, y + 1, color=c, alpha=0.7)
    # Ridges
    mountain_profile(ax, [(20, 75), (40, 80), (55, 72), (75, 78), (90, 70)],
                     55, GNEISS, alpha=0.8)
    # Gorge walls — two different rock types visible
    # Left wall: Indian plate gneiss (lighter)
    ax.fill_between([0, 45], 20, 55, color=GNEISS_LIGHT, alpha=0.8)
    rock_texture(ax, 0, 20, 45, 55, color=SNOW, n=25, seed=16)
    # Right wall: Kohistan arc (darker, greenish)
    ax.fill_between([55, 100], 20, 55, color=ARC_GREEN, alpha=0.85)
    rock_texture(ax, 55, 20, 100, 55, color=ARC_BASALT, n=30, seed=17)
    # The suture — a visible line between them
    ax.plot([45, 55], [55, 20], color=CARVED_OLD, lw=2, alpha=0.6, linestyle="--")
    # River
    river(ax, y_center=15, width=8, color=INDUS)
    # Foreground
    ax.fill_between([0, 100], 0, 8, color=STONE_WARM, alpha=0.5)
    save(fig, "panel-16-gorge-midday")


def panel_17_two_rocks():
    """Two kinds of rock meeting — pale gneiss, dark arc basalt."""
    fig, ax = make_fig(bg=GORGE_DARK)
    # Left half: Indian plate gneiss
    ax.fill_between([0, 50], 0, 100, color=GNEISS_LIGHT, alpha=0.7)
    rock_texture(ax, 0, 0, 50, 100, color=SNOW, n=50, seed=171)
    # Right half: Kohistan arc
    ax.fill_between([50, 100], 0, 100, color=ARC_BASALT, alpha=0.9)
    rock_texture(ax, 50, 0, 100, 100, color=ARC_GREEN, n=50, seed=172)
    # The contact — jagged, not clean
    contact_x = 50 + 3 * np.sin(np.linspace(0, 8, 100))
    contact_y = np.linspace(0, 100, 100)
    ax.plot(contact_x, contact_y, color=CARVED, lw=1.5, alpha=0.6)
    # Label-like marks on each side (not text — marks suggesting identity)
    for i in range(5):
        y = 15 + i * 16
        # Gneiss side: horizontal foliation
        ax.plot([10, 40], [y, y + 0.5], color=SNOW, alpha=0.3, lw=2)
        # Arc side: more chaotic, volcanic texture
        rng = np.random.default_rng(173 + i)
        xs = np.linspace(60, 90, 20)
        ys = y + rng.normal(0, 1, 20).cumsum() * 0.2
        ax.plot(xs, ys, color=ARC_GREEN, alpha=0.3, lw=2)
    save(fig, "panel-17-two-rocks")


def panel_18_ibex_above():
    """The ibex on the cliff above — the symbol drowns, the animal climbs."""
    fig, ax = make_fig(bg=ARC_BASALT)
    # Water rising from below (dam waterline)
    ax.fill_between([0, 100], 0, 35, color=INDUS_DEEP, alpha=0.7)
    # Submerged petroglyphs (fading)
    for x, y in [(20, 25), (40, 20), (60, 28), (80, 22)]:
        draw_ibex(ax, x, y, scale=1.2, color=INDUS, facing="right")
    # Rock face above water
    ax.fill_between([0, 100], 35, 100, color=GORGE_DARK, alpha=0.95)
    rock_texture(ax, 0, 35, 100, 100, color=GNEISS, n=40, seed=181)
    # Living ibex on the cliff above (bright, alive)
    draw_ibex(ax, 55, 75, scale=3.0, color=CARVED)
    draw_ibex(ax, 75, 70, scale=2.0, color=CARVED, facing="left")
    # Waterline — sharp horizontal
    ax.axhline(35, color=INDUS, lw=2, alpha=0.8)
    save(fig, "panel-18-ibex-above")


def panel_19_terrace_dusk():
    """The terrace at dusk — all seven stones, river below, findings."""
    fig, ax = make_fig(bg=SKY_DUSK)
    # Dusk sky gradient
    for i in range(50):
        y = 50 + i
        t = i / 50
        c = np.array([0.85, 0.66, 0.50]) * (1-t) + np.array([0.45, 0.35, 0.40]) * t
        ax.axhspan(y, y + 1, color=c, alpha=0.8)
    # Distant mountain silhouette
    mountain_profile(ax, [(15, 80), (35, 88), (50, 82), (70, 85), (85, 75)],
                     60, GNEISS, alpha=0.7)
    # Terrace
    ax.fill_between([0, 100], 15, 50, color=STONE_WARM, alpha=0.6)
    rock_texture(ax, 0, 15, 100, 50, color=CARVED_OLD, n=30, seed=191)
    # All seven stones, closer together now — gathered
    stone_data = [
        (18, 35, "dense", GNEISS_LIGHT, 61, -3),
        (32, 38, "sparse", STONE_COOL, 62, 5),
        (44, 36, "terse", "#A0988C", 63, -2),
        (55, 38, "philosophical", GNEISS_LIGHT, 64, 7),
        (66, 35, "analytical", STONE_COOL, 65, -5),
        (77, 37, "operational", "#B0A898", 66, 3),
        (88, 34, "questions", STONE_WARM, 67, -8),
    ]
    for x, y, marks, color, seed, rot in stone_data:
        draw_stone(ax, x, y, 8, 5, color=color, marks=marks,
                   mark_color=CARVED, seed=seed, rotation=rot)
    # River
    river(ax, y_center=8, width=6, color=INDUS_DEEP)
    save(fig, "panel-19-terrace-dusk")


def panel_20_nanga_parbat_last_light():
    """Nanga Parbat at last light — the mountain that builds itself."""
    fig, ax = make_fig(bg="#2A1820")
    # Deep dusk sky
    for i in range(50):
        y = 50 + i
        t = i / 50
        c = np.array([0.35, 0.20, 0.22]) * (1-t) + np.array([0.15, 0.10, 0.15]) * t
        ax.axhspan(y, y + 1, color=c, alpha=0.9)
    # Stars
    rng = np.random.default_rng(200)
    for _ in range(40):
        ax.plot(rng.uniform(0, 100), rng.uniform(65, 98),
                '.', color=SNOW, ms=rng.uniform(0.5, 2), alpha=rng.uniform(0.3, 0.8))
    # The mountain — massive, dark, alpenglow on summit ridge
    mountain_profile(ax, [(20, 60), (35, 75), (48, 95), (55, 92),
                          (62, 80), (75, 65), (90, 55)],
                     30, GNEISS, alpha=0.9)
    # Alpenglow on the summit
    ax.fill_between([43, 53], [90, 90], [95, 95], color=ALPENGLOW, alpha=0.5)
    ax.fill_between([40, 56], [85, 85], [92, 92], color=ALPENGLOW, alpha=0.2)
    # Glacier (pale streak)
    glacier_x = np.array([48, 47, 46, 45.5, 46, 47])
    glacier_y = np.array([90, 78, 65, 55, 45, 35])
    ax.plot(glacier_x, glacier_y, color=ICE, lw=3, alpha=0.4)
    ax.plot(glacier_x + 1, glacier_y, color=ICE, lw=2, alpha=0.2)
    # Foreground darkness
    ax.fill_between([0, 100], 0, 30, color=SHADOW, alpha=0.8)
    # Faint river gleam
    ax.plot([0, 100], [15, 15], color=INDUS, lw=1, alpha=0.15)
    save(fig, "panel-20-last-light")


# ── Main ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Generating 20 panels → {OUT}")
    panel_01_gorge_dawn()
    panel_02_terrace()
    panel_03_ibex_closeup()
    panel_04_stupa_around_ibex()
    panel_05_seven_stones()
    panel_06_stone_dense()
    panel_07_stone_sparse()
    panel_08_stone_terse()
    panel_09_stone_philosophical()
    panel_10_stone_analytical()
    panel_11_stone_operational()
    panel_12_stone_questions()
    panel_13_cross_reader()
    panel_14_audit_to_builder()
    panel_15_cartographer_to_newcomer()
    panel_16_gorge_midday()
    panel_17_two_rocks()
    panel_18_ibex_above()
    panel_19_terrace_dusk()
    panel_20_nanga_parbat_last_light()
    print(f"\nDone. {len(list(OUT.glob('*.png')))} panels generated.")
