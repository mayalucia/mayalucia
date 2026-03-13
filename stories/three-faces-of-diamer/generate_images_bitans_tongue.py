# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
# ]
# ///
"""
Generate illustrations for "The Bitan's Tongue" (Story #19).

The iron bangle. The choosing during blossom season. The twelve tunes.
The tongue that speaks a language the medium does not know.

Visual language: dark warm tones — juniper smoke, iron, the warm interior
of a gathering space. Apricot blossom (white on dark stone) for the
choosing. Sound visualised as rhythm patterns for the music.

Run with:  uv run generate_images_bitans_tongue.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Output ──────────────────────────────────────────────────────────
SLUG = "the-bitans-tongue"
OUT = (Path(__file__).parent / f"../../website/static/images/writing/{SLUG}").resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 12, 9

# ── Palette: Juniper Smoke / Iron / Blossom ───────────────────────
SMOKE_DARK    = "#2A2420"   # dark interior, juniper-stained
SMOKE_MED     = "#4A4238"   # mid-tone smoke
SMOKE_LT      = "#8A7868"   # light smoke wisps
IRON          = "#5A5858"   # iron bangle — cold metal
IRON_BRIGHT   = "#8A8888"   # highlight on iron
BLOSSOM_WHITE = "#F0EDE8"   # apricot blossom
BLOSSOM_PINK  = "#E8D0C8"   # blossom with warmth
BRANCH        = "#6A5848"   # dark branch
STONE_GREY    = "#7A7672"   # Karimabad stone walls
STONE_DARK    = "#4A4845"   # darker stone
MOUNTAIN_BG   = "#C8C0B8"   # distant Rakaposhi — muted
SKY_WARM      = "#D8D0C8"   # warm pale sky
DRUM_SKIN     = "#C8A878"   # drum surface — warm leather
DRUM_WOOD     = "#6A5040"   # drum body
REED_PIPE     = "#A08060"   # surnai — reed-coloured
BLOOD_RED     = "#8A3030"   # restrained — not bright
MILK_WHITE    = "#F0EDE8"   # makhakhar
JUNIPER_GREEN = "#5A6848"   # juniper branch
FIRE_ORANGE   = "#C88040"   # small juniper fire


# ── Shared helpers ──────────────────────────────────────────────────

def make_fig(width=W, height=H, bg=SMOKE_DARK):
    fig, ax = plt.subplots(1, 1, figsize=(width, height), facecolor=bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def smoke_wisps(ax, seed=42, n=20, base_x=50, base_y=20):
    """Rising juniper smoke."""
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x = base_x + rng.uniform(-8, 8)
        y = base_y + rng.uniform(0, 50)
        # Wisp as a short curved line
        t = np.linspace(0, 1, 10)
        wx = x + rng.uniform(-3, 3) * np.sin(t * np.pi)
        wy = y + t * rng.uniform(3, 10)
        ax.plot(wx, wy, color=SMOKE_LT,
                alpha=rng.uniform(0.05, 0.2),
                linewidth=rng.uniform(1, 4))


def save(fig, name):
    path = OUT / f"{name}.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  ✓ {path.name}")


# ════════════════════════════════════════════════════════════════════
# Figure 1: The Kau — iron bangle, binding and protection
# ════════════════════════════════════════════════════════════════════

def fig1_the_kau():
    fig, ax = make_fig(bg=SMOKE_DARK)

    # The bangle — a circle of iron, centre of the composition
    cx, cy = 50, 50
    outer_r = 25
    inner_r = 20

    # Iron ring — thick, with metallic variation
    theta = np.linspace(0, 2 * np.pi, 200)
    rng = np.random.default_rng(11)

    for layer in range(8):
        r = inner_r + layer * (outer_r - inner_r) / 8
        variation = rng.uniform(-0.3, 0.3, 200)
        x = cx + (r + variation) * np.cos(theta)
        y = cy + (r + variation) * np.sin(theta)
        shade = IRON if layer < 4 else IRON_BRIGHT
        ax.plot(x, y, color=shade,
                alpha=0.15 + layer * 0.05,
                linewidth=1.5)

    # Highlight arc — metallic sheen on upper left
    theta_hi = np.linspace(2.0, 3.5, 50)
    for dr in range(-2, 3):
        r = 22.5 + dr * 0.3
        ax.plot(cx + r * np.cos(theta_hi), cy + r * np.sin(theta_hi),
                color=IRON_BRIGHT, alpha=0.08, linewidth=2)

    # Inner text: "binds"
    ax.text(cx, cy + 3, "binds", fontsize=16, color=IRON_BRIGHT,
            alpha=0.5, ha="center", fontfamily="serif", style="italic")

    # Outer text: "protects"
    ax.text(cx, cy - 3, "protects", fontsize=16, color=IRON_BRIGHT,
            alpha=0.5, ha="center", fontfamily="serif", style="italic")

    # Caption
    ax.text(50, 8, "a paradox held in metal",
            fontsize=14, color=SMOKE_LT, alpha=0.5,
            ha="center", fontfamily="serif", style="italic")

    save(fig, "fig1-the-kau")


# ════════════════════════════════════════════════════════════════════
# Figure 2: The Choosing — blossoms falling on dark stone
# ════════════════════════════════════════════════════════════════════

def fig2_the_choosing():
    fig, ax = make_fig(bg=STONE_DARK)

    # Stone wall background with terraces
    rng = np.random.default_rng(22)
    for _ in range(20):
        x0 = rng.uniform(0, 100)
        y0 = rng.uniform(0, 60)
        w = rng.uniform(5, 20)
        h = rng.uniform(2, 6)
        rect = mpatches.FancyBboxPatch(
            (x0, y0), w, h,
            boxstyle="round,pad=0.5",
            facecolor=STONE_GREY, alpha=rng.uniform(0.05, 0.15))
        ax.add_patch(rect)

    # Apricot branch — crossing upper portion
    # Main branch
    branch_x = [10, 25, 40, 55, 70, 85]
    branch_y = [75, 78, 74, 77, 73, 76]
    ax.plot(branch_x, branch_y, color=BRANCH, linewidth=3, alpha=0.7)

    # Sub-branches
    for bx, by in zip(branch_x[1:-1], branch_y[1:-1]):
        for _ in range(rng.integers(1, 4)):
            dx = rng.uniform(-5, 5)
            dy = rng.uniform(-8, 3)
            ax.plot([bx, bx + dx], [by, by + dy],
                    color=BRANCH, linewidth=1.5, alpha=0.5)

    # Blossoms on the branch
    for bx, by in zip(branch_x, branch_y):
        for _ in range(rng.integers(3, 8)):
            fx = bx + rng.uniform(-4, 4)
            fy = by + rng.uniform(-3, 5)
            size = rng.uniform(1.5, 3)
            color = rng.choice([BLOSSOM_WHITE, BLOSSOM_PINK])
            blossom = plt.Circle((fx, fy), size,
                                color=color, alpha=rng.uniform(0.3, 0.7))
            ax.add_patch(blossom)

    # Falling petals — scattered down toward the ground
    for _ in range(25):
        px = rng.uniform(10, 90)
        py = rng.uniform(10, 65)
        size = rng.uniform(0.5, 1.5)
        # Petal as small ellipse
        petal = mpatches.Ellipse(
            (px, py), size * 2, size,
            angle=rng.uniform(0, 180),
            facecolor=BLOSSOM_WHITE,
            alpha=rng.uniform(0.15, 0.45))
        ax.add_patch(petal)

    # Caption
    ax.text(50, 5, "the season when the peri descend and choose",
            fontsize=13, color=BLOSSOM_WHITE, alpha=0.5,
            ha="center", fontfamily="serif", style="italic")

    save(fig, "fig2-the-choosing")


# ════════════════════════════════════════════════════════════════════
# Figure 3: The Twelve Tunes — rhythm as protocol
# ════════════════════════════════════════════════════════════════════

def fig3_twelve_tunes():
    fig, ax = make_fig(width=14, height=9, bg=SMOKE_DARK)

    tunes = [
        "Dhani",    "Bazmi",    "Tajwar",   "Alghani",
        "Saus",     "Lolo",     "Tambal",   "Bulla",
        "Razm",     "Yudaani",  "·",        "Danyal"
    ]

    occasions = [
        "celebration", "assembly", "procession", "lament",
        "love",        "lullaby",  "dance",      "challenge",
        "battle",      "war",      "",           "trance"
    ]

    rng = np.random.default_rng(77)

    cols, rows = 4, 3
    for i, (tune, occasion) in enumerate(zip(tunes, occasions)):
        col = i % cols
        row = 2 - i // cols
        cx = 15 + col * 23
        cy = 18 + row * 28

        if tune == "·":
            continue

        # Each tune as a rhythm pattern — horizontal marks
        is_danyal = tune == "Danyal"

        if is_danyal:
            # Danyal gets special treatment — highlighted
            box = mpatches.FancyBboxPatch(
                (cx - 10, cy - 10), 20, 22,
                boxstyle="round,pad=1",
                facecolor=BLOOD_RED, alpha=0.15)
            ax.add_patch(box)

        # Rhythm dots/dashes — abstract representation
        n_beats = rng.integers(5, 12)
        for j in range(n_beats):
            bx = cx - 8 + j * (16 / n_beats)
            beat_size = rng.uniform(0.3, 1.5)
            color = FIRE_ORANGE if is_danyal else DRUM_SKIN
            alpha_val = 0.7 if is_danyal else rng.uniform(0.2, 0.5)
            ax.plot(bx, cy, 'o', color=color, markersize=beat_size * 3,
                    alpha=alpha_val)

        # Tune name
        name_color = FIRE_ORANGE if is_danyal else SMOKE_LT
        name_alpha = 0.8 if is_danyal else 0.5
        ax.text(cx, cy + 6, tune, fontsize=13, color=name_color,
                alpha=name_alpha, ha="center", fontfamily="serif",
                style="italic", fontweight="bold" if is_danyal else "normal")

        # Occasion
        occ_color = BLOSSOM_PINK if is_danyal else SMOKE_LT
        ax.text(cx, cy - 6, occasion, fontsize=9, color=occ_color,
                alpha=0.4, ha="center", fontfamily="serif")

    # The eleventh position — the gap (Danyal's predecessor? or silence?)
    ax.text(15 + 2 * 23, 18 + 0 * 28, "·", fontsize=24,
            color=SMOKE_LT, alpha=0.2, ha="center")

    # Caption
    ax.text(50, 3, "twelve tunes  ·  one opens the door to the peri",
            fontsize=13, color=FIRE_ORANGE, alpha=0.5,
            ha="center", fontfamily="serif", style="italic")

    save(fig, "fig3-twelve-tunes")


# ════════════════════════════════════════════════════════════════════
# Figure 4: The Tongue — two languages, one throat
# ════════════════════════════════════════════════════════════════════

def fig4_the_tongue():
    fig, ax = make_fig(bg=SMOKE_DARK)
    smoke_wisps(ax, seed=99, n=30, base_x=50, base_y=10)

    # Two columns of text — Burushaski (left, faint) and Shina (right, bright)
    # Represented as abstract line patterns, not real text

    rng = np.random.default_rng(44)

    # Burushaski side — the waking language, fading
    ax.text(25, 88, "Burushaski", fontsize=14, color=SMOKE_LT,
            alpha=0.3, ha="center", fontfamily="serif", style="italic")

    for i in range(10):
        y = 78 - i * 5
        length = rng.uniform(8, 18)
        x_start = 25 - length / 2
        # Fading lines — the language that recedes in trance
        ax.plot([x_start, x_start + length], [y, y],
                color=SMOKE_LT, alpha=0.1 + 0.02 * (10 - i),
                linewidth=rng.uniform(1, 2))

    # Arrow / flow from left to right — the transition
    transition_y = 50
    for t in np.linspace(35, 65, 15):
        ax.plot(t, transition_y + rng.uniform(-2, 2), 'o',
                color=FIRE_ORANGE, alpha=0.1,
                markersize=rng.uniform(1, 3))

    # Shina side — the spirit's language, arriving
    ax.text(75, 88, "Shina", fontsize=18, color=BLOSSOM_WHITE,
            alpha=0.7, ha="center", fontfamily="serif", style="italic")

    for i in range(10):
        y = 78 - i * 5
        length = rng.uniform(8, 18)
        x_start = 75 - length / 2
        # Bright lines — the language that arrives in trance
        ax.plot([x_start, x_start + length], [y, y],
                color=BLOSSOM_WHITE, alpha=0.3 + 0.04 * i,
                linewidth=rng.uniform(1.5, 3))

    # The throat — a narrow passage between the two
    throat_x = [48, 50, 52, 50, 48]
    throat_y = [65, 70, 65, 35, 40]
    ax.plot(throat_x, throat_y, color=IRON, alpha=0.2, linewidth=2)

    # Caption
    ax.text(50, 5, "the voice is not borrowed  ·  it arrives",
            fontsize=14, color=BLOSSOM_WHITE, alpha=0.5,
            ha="center", fontfamily="serif", style="italic")

    save(fig, "fig4-the-tongue")


# ════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Generating illustrations → {OUT}/")
    fig1_the_kau()
    fig2_the_choosing()
    fig3_twelve_tunes()
    fig4_the_tongue()
    print("Done.")
