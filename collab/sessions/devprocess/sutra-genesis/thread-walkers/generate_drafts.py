#!/usr/bin/env python3
"""
Generate weaving draft diagrams for "River Braid" — a point twill pattern
on four shafts, rendered in two variants:

  1. Point twill treadling  -> diamond / lozenge cloth  (Lahaul)
  2. Straight twill treadling -> diagonal twill cloth    (Leh variant)

Both share the same pointed threading (1-2-3-4-3-2 repeat) and
the same tie-up, but produce radically different cloth.

The drafts follow standard weaving-draft convention:
  - Threading: top-right quadrant  (shafts x warp ends)
  - Tie-up:    top-left quadrant   (shafts x treadles)
  - Treadling: bottom-left quadrant (picks x treadles)
  - Drawdown:  bottom-right quadrant (picks x warp ends, computed)

Warp-dominant squares (raised shaft -> warp floats over weft) are filled.
Weft-dominant squares are left in the ground colour.

Run:
    uv run --with matplotlib --with numpy python3 generate_drafts.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ---------------------------------------------------------------------------
# Colour palette — manuscript / parchment aesthetic
# ---------------------------------------------------------------------------
BG         = "#f4e8c1"   # warm parchment
INDIGO     = "#2c3e6b"   # dark indigo — warp-dominant face
GRID_LINE  = "#c4a96a"   # light sepia grid lines
TEXT_DARK  = "#3b2a1a"   # near-black sepia for titles
TEXT_MID   = "#6b5032"   # mid sepia for labels
TEXT_LIGHT = "#8a7050"   # light sepia for annotations

# ---------------------------------------------------------------------------
# Weaving structure definitions
# ---------------------------------------------------------------------------

NUM_SHAFTS   = 4
NUM_TREADLES = 6

# Threading: pointed / return twill on 4 shafts.
# One repeat unit: 1,2,3,4,3,2  (6 ends).
# Internally 0-indexed: shaft 0 = weaver's shaft 1.
THREADING_UNIT = [0, 1, 2, 3, 2, 1]

# Tie-up: which shafts are RAISED for each treadle.
# tieup[treadle_index, shaft_index] = True  =>  shaft is raised.
#
# For a 2/2 balanced twill the convention is to raise exactly 2 of 4
# shafts per treadle.  With 4 shafts there are C(4,2) = 6 such pairs,
# giving us 6 distinct treadles — exactly the number needed.
#
#   Treadle 1  (idx 0):  shafts 1,2   — the "adjacent" pairs that
#   Treadle 2  (idx 1):  shafts 2,3     walk around the shaft order
#   Treadle 3  (idx 2):  shafts 3,4     clockwise
#   Treadle 4  (idx 3):  shafts 1,4
#   Treadle 5  (idx 4):  shafts 1,3   — the "skip" pairs
#   Treadle 6  (idx 5):  shafts 2,4
#
# For point twill treadling we use treadles 1-4; treadles 5-6 are
# available on the loom but used only in tabby / other structures.

TIEUP = np.zeros((NUM_TREADLES, NUM_SHAFTS), dtype=bool)
TIEUP[0, [0, 1]] = True   # treadle 1: shafts 1,2
TIEUP[1, [1, 2]] = True   # treadle 2: shafts 2,3
TIEUP[2, [2, 3]] = True   # treadle 3: shafts 3,4
TIEUP[3, [0, 3]] = True   # treadle 4: shafts 1,4
TIEUP[4, [0, 2]] = True   # treadle 5: shafts 1,3
TIEUP[5, [1, 3]] = True   # treadle 6: shafts 2,4


# ---------------------------------------------------------------------------
# Construction helpers
# ---------------------------------------------------------------------------

def build_threading(n_warp: int) -> np.ndarray:
    """Return shape (n_warp,), values in 0..3. Point-twill repeat."""
    reps = (n_warp // len(THREADING_UNIT)) + 1
    return np.array((THREADING_UNIT * reps)[:n_warp], dtype=int)


def threading_to_grid(threading: np.ndarray) -> np.ndarray:
    """
    Shape (NUM_SHAFTS, n_warp).  grid[shaft, col] = True if that end
    is threaded on that shaft.
    """
    n = len(threading)
    grid = np.zeros((NUM_SHAFTS, n), dtype=bool)
    grid[threading, np.arange(n)] = True
    return grid


def treadling_to_grid(treadling_seq: list, n_picks: int) -> np.ndarray:
    """
    Shape (n_picks, NUM_TREADLES). grid[row, treadle] = True.
    """
    grid = np.zeros((n_picks, NUM_TREADLES), dtype=bool)
    seq = np.array(treadling_seq)
    full = np.tile(seq, (n_picks // len(seq)) + 1)[:n_picks]
    grid[np.arange(n_picks), full] = True
    return grid


def compute_drawdown(threading: np.ndarray, tieup: np.ndarray,
                     treadling_seq: list, n_picks: int) -> np.ndarray:
    """
    Shape (n_picks, n_warp).  True = warp on top (warp-dominant).

    For each pick, the pressed treadle determines which shafts rise
    (via tie-up).  Each warp end that sits on a raised shaft floats
    over the weft.
    """
    n_warp = len(threading)
    seq = np.array(treadling_seq)
    full_seq = np.tile(seq, (n_picks // len(seq)) + 1)[:n_picks]

    drawdown = np.zeros((n_picks, n_warp), dtype=bool)
    for row in range(n_picks):
        raised = tieup[full_seq[row]]          # (NUM_SHAFTS,) bool
        drawdown[row] = raised[threading]       # broadcast via fancy index
    return drawdown


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def draw_grid_cells(ax, grid, ox, oy, cell,
                    fill=INDIGO, empty=BG, edge=GRID_LINE, lw=0.5):
    """
    Render a boolean grid as filled/empty rectangles.

    (ox, oy) is the bottom-left corner in data coords.
    Row 0 of *grid* appears at the TOP of the rendered block
    (standard draft convention: first pick at top of drawdown /
    treadling; highest shaft at top of threading / tie-up after
    the caller flips the axis).
    """
    nr, nc = grid.shape
    for r in range(nr):
        for c in range(nc):
            x = ox + c * cell
            y = oy + (nr - 1 - r) * cell      # row 0 -> top
            colour = fill if grid[r, c] else empty
            ax.add_patch(mpatches.Rectangle(
                (x, y), cell, cell,
                facecolor=colour, edgecolor=edge, linewidth=lw))


def generate_draft(
    title: str,
    subtitle: str,
    treadling_seq: list,
    n_warp: int,
    n_picks: int,
    output_path: str,
    annotation: str = ""
):
    """Produce a complete four-quadrant weaving draft and save to PDF."""

    # --- build the four grids ---
    threading     = build_threading(n_warp)
    threading_g   = threading_to_grid(threading)        # (4, n_warp)
    treadling_g   = treadling_to_grid(treadling_seq, n_picks)  # (n_picks, 6)
    drawdown      = compute_drawdown(threading, TIEUP, treadling_seq, n_picks)

    # For display, the threading and tie-up grids need shaft 1 at the
    # BOTTOM and shaft 4 at the TOP.  Our raw grids have shaft 0 (=1)
    # in row 0.  draw_grid_cells puts row 0 at the top, so we flip
    # the shaft axis before passing:
    threading_disp = threading_g[::-1]                  # shaft 4 in row 0
    tieup_disp     = TIEUP.T[::-1]                      # (shafts, treadles), flipped

    # --- layout geometry ---
    cell = 0.22
    gap  = 0.45          # space between quadrants (for labels)

    tu_w = NUM_TREADLES * cell   # tie-up width
    tu_h = NUM_SHAFTS   * cell
    th_w = n_warp  * cell        # threading width
    th_h = NUM_SHAFTS * cell
    tr_w = NUM_TREADLES * cell   # treadling width
    tr_h = n_picks * cell
    dd_w = n_warp  * cell        # drawdown width
    dd_h = n_picks * cell

    # quadrant origins (bottom-left corners)
    tu_ox, tu_oy = 0,             tr_h + gap
    th_ox, th_oy = tu_w + gap,    tr_h + gap
    tr_ox, tr_oy = 0,             0
    dd_ox, dd_oy = tu_w + gap,    0

    content_w = tu_w + gap + dd_w
    content_h = tr_h + gap + th_h

    ml, mr, mt, mb = 2.0, 0.8, 1.8, 1.4   # margins
    fig_w = ml + content_w + mr
    fig_h = mb + content_h + mt

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-0.2, fig_w + 0.2)
    ax.set_ylim(-0.2, fig_h + 0.2)
    ax.set_aspect('equal')
    ax.axis('off')

    # offset for margins
    ox, oy = ml, mb

    # --- render quadrants ---
    draw_grid_cells(ax, tieup_disp,     ox + tu_ox, oy + tu_oy, cell)
    draw_grid_cells(ax, threading_disp, ox + th_ox, oy + th_oy, cell)
    draw_grid_cells(ax, treadling_g,    ox + tr_ox, oy + tr_oy, cell)
    draw_grid_cells(ax, drawdown,       ox + dd_ox, oy + dd_oy, cell)

    # --- shaft labels (between tie-up and threading, in the gap) ---
    for s in range(NUM_SHAFTS):
        lx = ox + tu_ox + tu_w + gap * 0.5
        ly = oy + tu_oy + s * cell + cell * 0.5
        ax.text(lx, ly, str(s + 1),
                ha='center', va='center', fontsize=7,
                color=TEXT_MID, fontfamily='serif')

    # --- treadle labels (between tie-up and treadling, in the gap) ---
    for t in range(NUM_TREADLES):
        lx = ox + tu_ox + t * cell + cell * 0.5
        ly = oy + tu_oy - gap * 0.45
        ax.text(lx, ly, str(t + 1),
                ha='center', va='center', fontsize=6,
                color=TEXT_MID, fontfamily='serif')

    # --- quadrant labels ---
    label_kw = dict(ha='center', va='center', fontsize=10,
                    color=TEXT_MID, fontfamily='serif', fontstyle='italic')

    ax.text(ox + tu_ox + tu_w * 0.5,
            oy + tu_oy + tu_h + 0.28,
            "Tie-up", **label_kw)

    ax.text(ox + th_ox + th_w * 0.5,
            oy + th_oy + th_h + 0.28,
            "Threading", **label_kw)

    ax.text(ox + tr_ox - 0.35,
            oy + tr_oy + tr_h * 0.5,
            "Treadling", rotation=90, **label_kw)

    ax.text(ox + dd_ox + dd_w * 0.5,
            oy + dd_oy - 0.35,
            "Drawdown", **label_kw)

    # --- title / subtitle ---
    ax.text(fig_w * 0.5, fig_h - 0.35,
            title,
            ha='center', va='top', fontsize=14,
            color=TEXT_DARK, fontfamily='serif', fontweight='bold')

    ax.text(fig_w * 0.5, fig_h - 0.78,
            subtitle,
            ha='center', va='top', fontsize=9,
            color=TEXT_MID, fontfamily='serif', fontstyle='italic')

    # --- threading repeat annotation ---
    repeat_str = "-".join(str(s + 1) for s in THREADING_UNIT)
    ax.text(ox + th_ox + th_w * 0.5,
            oy + th_oy - gap * 0.75,
            f"threading repeat: {repeat_str}",
            ha='center', va='top', fontsize=6,
            color=TEXT_LIGHT, fontfamily='serif')

    # --- treadling sequence annotation ---
    tread_str = "-".join(str(t + 1) for t in treadling_seq)
    ax.text(ox + tr_ox + tr_w + 0.15,
            oy + tr_oy + tr_h + 0.15,
            f"treadling: {tread_str}",
            ha='left', va='bottom', fontsize=5.5,
            color=TEXT_LIGHT, fontfamily='serif', fontstyle='italic')

    # --- bottom annotation ---
    if annotation:
        ax.text(fig_w * 0.5, 0.35,
                annotation,
                ha='center', va='bottom', fontsize=7,
                color=TEXT_LIGHT, fontfamily='serif', fontstyle='italic')

    # --- legend ---
    ax.add_patch(mpatches.Rectangle(
        (ox + dd_ox + dd_w - 1.6, oy + dd_oy - 0.85),
        cell, cell, facecolor=INDIGO, edgecolor=GRID_LINE, lw=0.5))
    ax.text(ox + dd_ox + dd_w - 1.6 + cell + 0.08,
            oy + dd_oy - 0.85 + cell * 0.5,
            "warp over weft", ha='left', va='center',
            fontsize=5.5, color=TEXT_LIGHT, fontfamily='serif')

    ax.add_patch(mpatches.Rectangle(
        (ox + dd_ox + dd_w - 0.55, oy + dd_oy - 0.85),
        cell, cell, facecolor=BG, edgecolor=GRID_LINE, lw=0.5))
    ax.text(ox + dd_ox + dd_w - 0.55 + cell + 0.08,
            oy + dd_oy - 0.85 + cell * 0.5,
            "weft over warp", ha='left', va='center',
            fontsize=5.5, color=TEXT_LIGHT, fontfamily='serif')

    # --- save ---
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        p = Path(output_path).with_suffix(f".{ext}")
        fig.savefig(p, bbox_inches='tight', dpi=200,
                    facecolor=fig.get_facecolor(), edgecolor='none')
        print(f"Saved: {p}")
    plt.close(fig)


# ===========================================================================
# Generate both variants
# ===========================================================================

OUT_DIR = Path(__file__).parent

N_WARP = 30   # 5 full repeats of the 6-end threading unit
N_PICKS = 30  # 5 full repeats of the 6-pick point treadling

# --- Variant 1: Point twill treadling -> diamond / lozenge ---
#
# Treadling mirrors the threading: 1,2,3,4,3,2 (0-indexed: 0,1,2,3,2,1).
# Combined with the pointed threading, this produces the classic
# diamond / lozenge / "bird's eye" pattern.  The reversal in BOTH
# threading and treadling creates a two-axis symmetry — the diamonds
# that, to a weaver in the Lahaul valley, look like braided water.

POINT_TREADLING = [0, 1, 2, 3, 2, 1]

generate_draft(
    title="River Braid \u2014 Point Twill on Four Shafts",
    subtitle="from the archive of the Lahaul workshop",
    treadling_seq=POINT_TREADLING,
    n_warp=N_WARP,
    n_picks=N_PICKS,
    output_path=str(OUT_DIR / "draft-river-braid.pdf"),
    annotation="selvedge treatment: plain weave for 4 picks at each edge"
)

# --- Variant 2: Straight twill treadling -> diagonal ---
#
# Treadling runs straight: 1,2,3,4 (0-indexed: 0,1,2,3) repeating.
# Same threading, same tie-up — but the treadling never reverses.
# Over the pointed threading this produces a zigzag diagonal:
# the warp's reversal creates a chevron, but without the treadling
# reversal there are no closed diamonds.  A different cloth entirely
# from the same named pattern.

STRAIGHT_TREADLING = [0, 1, 2, 3]

generate_draft(
    title="River Braid (Leh variant) \u2014 Straight Twill on Four Shafts",
    subtitle="from the archive of the distant workshop",
    treadling_seq=STRAIGHT_TREADLING,
    n_warp=N_WARP,
    n_picks=N_PICKS,
    output_path=str(OUT_DIR / "draft-river-braid-variant.pdf"),
    annotation="selvedge treatment: plain weave for 4 picks at each edge"
)
