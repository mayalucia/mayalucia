"""
The Faculty Assembled — constellation map of 31 cognitive modes.

Each phantom is rendered as a Unicode glyph evoking its cognitive mode.
Node colour is a weighted blend of all faculty colours, reflecting
cross-disciplinary membership.

Glyph rendering is abstracted behind render_phantom() so a future
refactor can swap Unicode markers for PNG sprite overlays (option 4)
without touching the rest of the pipeline.

Usage:
    uv run --with matplotlib --with numpy python3 gen-faculty-assembled.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.colors import to_rgb, to_hex
from pathlib import Path

rng = np.random.default_rng(42)

# === Canvas: dark slate chalkboard ============================================

fig, ax = plt.subplots(figsize=(16, 11), dpi=200)
SLATE = "#1a1a2e"
CHALK = "#e8e4d4"
CHALK_DIM = "#8a8678"
fig.patch.set_facecolor(SLATE)
ax.set_facecolor(SLATE)
ax.set_xlim(-8.5, 8.5)
ax.set_ylim(-6.5, 6.5)
ax.set_aspect("equal")
ax.axis("off")

# === Cluster colours (7 faculties) ============================================

COLOURS = {
    "physics":     "#7eb8da",   # cool blue
    "measurement": "#d4a574",   # warm ochre
    "biology":     "#c4836a",   # warm terracotta
    "information": "#a8d4a0",   # soft green
    "computation": "#d4a0c4",   # muted mauve
    "mathematics": "#dac87e",   # gold
    "meta":        "#c4c4c4",   # silver
    "us":          "#e8e4d4",   # chalk white
}
FACULTY_RGB = {k: np.array(to_rgb(v)) for k, v in COLOURS.items()}

def blend_colour(weights):
    """Blend faculty colours by normalised weights dict."""
    total = sum(weights.values())
    if total == 0:
        return CHALK
    rgb = np.zeros(3)
    for faculty, w in weights.items():
        if faculty in FACULTY_RGB and w > 0:
            rgb += (w / total) * FACULTY_RGB[faculty]
    return to_hex(np.clip(rgb, 0, 1))


# === Glyph table ==============================================================
# Each glyph evokes the cognitive MODE, not the person.
# To swap to PNG sprites (option 4), replace this dict with paths and
# update render_phantom() to use OffsetImage + AnnotationBbox.

GLYPHS = {
    # --- Physics ---
    "Feynman":    "∫",   # path integration — his invention
    "Landau":     "◇",   # phase diamond — order parameter
    "Thorne":     "◎",   # concentric rings — gravitational waves
    "Susskind":   "◖",   # half-disk — holographic boundary
    "Wheeler":    "?",   # the participatory question
    # --- Measurement ---
    "Faraday":    "⊥",   # field probe — perpendicular sensing
    "Humboldt":   "☉",   # the naturalist's sun-eye
    "Helmholtz":  "⊢",   # turnstile — deduction from instrument
    # --- Biology ---
    "Cajal":      "ψ",   # dendritic branching
    "D'Arcy Thompson": "⌘",  # looped form — growth pattern
    "Braitenberg":"⚙",   # gear — synthetic vehicle
    "Marr":       "≡",   # three bars — three levels
    "Darwin":     "⊛",   # radiating tree
    "McClintock": "⊙",   # focused kernel — empathic attention
    "Sapolsky":   "⋮",   # stacked dots — nested levels
    # --- Information ---
    "Shannon":    "⋈",   # bowtie — channel capacity
    "Jaynes":     "∝",   # proportionality — prior updating
    "MacKay":     "⊞",   # boxed plus — message passing
    # --- Computation ---
    "Hinton":     "▽",   # inverted triangle — gradient descent
    "Hopfield":   "⊗",   # tensor product — spin coupling
    "Karpathy":   "▢",   # empty square — blank canvas to build on
    # --- Mathematics ---
    "Gauss":      "∿",   # sine wave — the bell curve
    "Riemann":    "ζ",   # zeta — the function itself
    "Erdős":      "∞",   # infinity — itinerant wandering
    "Tao":        "⊳",   # triangle — strategic direction
    "Thurston":   "⊘",   # crossed circle — topology
    # --- Meta ---
    "Poincaré":   "◌",   # dotted circle — latent incubation
    "Hofstadter": "∾",   # inverted lazy S — tangled hierarchy
    "Bateson":    "∴",   # therefore — the pattern that connects
    "Bach":       "λ",   # lambda — computation's essence
    "Leopold":    "◯",   # circle — the round river
    "Graeber":    "⊘",   # null — what seems natural isn't
    # --- Us ---
    "Construction": "⚒", # crossed hammers — building
}


# === Cross-faculty weights ====================================================

WEIGHTS = {
    # === PHYSICISTS (5) ===
    "Landau":     {"physics": 1.0, "mathematics": 0.3},
    "Thorne":     {"physics": 1.0, "mathematics": 0.2, "measurement": 0.15},
    "Feynman":    {"physics": 1.0, "computation": 0.2, "meta": 0.15},
    "Susskind":   {"physics": 1.0, "information": 0.25, "computation": 0.1},
    "Wheeler":    {"physics": 1.0, "meta": 0.5, "information": 0.3},
    # === MEASURERS (3) ===
    "Faraday":    {"measurement": 1.0, "physics": 0.3},
    "Humboldt":   {"measurement": 1.0, "biology": 0.3, "meta": 0.15},
    "Helmholtz":  {"measurement": 1.0, "physics": 0.4, "biology": 0.2, "computation": 0.1},
    # === BIOLOGISTS (7) ===
    "Cajal":      {"biology": 1.0, "measurement": 0.4},
    "D'Arcy Thompson": {"biology": 1.0, "mathematics": 0.5, "physics": 0.2},
    "Braitenberg":{"biology": 1.0, "computation": 0.4, "meta": 0.15},
    "Marr":       {"biology": 1.0, "computation": 0.4, "meta": 0.3},
    "Darwin":     {"biology": 1.0, "meta": 0.2},
    "McClintock": {"biology": 1.0, "measurement": 0.3},
    "Sapolsky":   {"biology": 1.0, "meta": 0.3, "measurement": 0.15},
    # === INFORMATION THEORISTS (3) ===
    "Shannon":    {"information": 1.0, "mathematics": 0.3, "computation": 0.15},
    "Jaynes":     {"information": 1.0, "physics": 0.4, "mathematics": 0.2},
    "MacKay":     {"information": 1.0, "computation": 0.4, "physics": 0.1},
    # === COMPUTATIONAL THINKERS (3) ===
    "Hinton":     {"computation": 1.0, "physics": 0.3, "biology": 0.15},
    "Hopfield":   {"computation": 1.0, "physics": 0.5, "mathematics": 0.15},
    "Karpathy":   {"computation": 1.0, "information": 0.15},
    # === MATHEMATICIANS (5) ===
    "Gauss":      {"mathematics": 1.0, "physics": 0.3, "measurement": 0.3},
    "Riemann":    {"mathematics": 1.0, "physics": 0.3, "meta": 0.1},
    "Erdős":      {"mathematics": 1.0, "meta": 0.2},
    "Tao":        {"mathematics": 1.0, "meta": 0.3, "computation": 0.1},
    "Thurston":   {"mathematics": 1.0, "meta": 0.3, "physics": 0.1},
    # === META-THINKERS (6) ===
    "Poincaré":   {"meta": 1.0, "mathematics": 0.5, "physics": 0.2},
    "Hofstadter": {"meta": 1.0, "computation": 0.3, "mathematics": 0.2},
    "Bateson":    {"meta": 1.0, "biology": 0.4, "measurement": 0.15},
    "Bach":       {"meta": 1.0, "computation": 0.5, "biology": 0.15},
    "Leopold":    {"meta": 1.0, "biology": 0.5, "measurement": 0.2},
    "Graeber":    {"meta": 1.0, "biology": 0.15},
}


# === Phantom positions ========================================================
# (x, y, name, cluster, skill_label)

phantoms = [
    # Physics — upper left
    (-5.0,  4.2, "Landau",   "physics",     "Derivation"),
    (-3.2,  5.0, "Thorne",   "physics",     "Geometric\nIntuition"),
    (-5.5,  2.3, "Feynman",  "physics",     "Encounter"),
    (-3.0,  2.8, "Susskind", "physics",     "Compression"),
    (-4.2,  3.0, "Wheeler",  "physics",     "Participatory\nQuestion"),
    # Measurement — left
    (-7.0,  0.8, "Faraday",  "measurement", "Active\nMeasurement"),
    (-7.2, -0.8, "Humboldt", "measurement", "Passive\nObservation"),
    (-5.5, -0.0, "Helmholtz","measurement", "Instrument-\nTheory Unity"),
    # Biology — lower left
    (-6.5, -2.5, "Cajal",    "biology",     "Observing\nArtist"),
    (-4.5, -2.0, "D'Arcy Thompson", "biology", "Mathematical\nMorphology"),
    (-3.5, -3.5, "Braitenberg","biology",   "Synthetic\nPsychology"),
    (-2.0, -2.8, "Marr",     "biology",     "Levels of\nAnalysis"),
    (-5.5, -3.8, "Darwin",   "biology",     "Historical\nExplanation"),
    (-7.0, -3.8, "McClintock","biology",    "Empathic\nAttention"),
    (-4.0, -4.8, "Sapolsky", "biology",     "Multilevel\nDeterminism"),
    # Information — lower centre
    (-1.2, -1.5, "Shannon",  "information", "Playful\nFormalisation"),
    ( 0.2, -2.8, "Jaynes",   "information", "Radical\nConsistency"),
    (-1.8, -4.5, "MacKay",   "information", "Unified\nComputation"),
    # Computation — lower right
    ( 1.8, -2.2, "Hinton",   "computation", "Mechanistic\nImagination"),
    ( 3.5, -3.5, "Hopfield", "computation", "Physical\nIsomorphism"),
    ( 3.0, -1.2, "Karpathy", "computation", "Minimal\nBuilding"),
    # Mathematics — upper right
    ( 3.5,  4.5, "Gauss",    "mathematics", "Computational\nPatience"),
    ( 5.5,  3.5, "Riemann",  "mathematics", "Conceptual\nArchitecture"),
    ( 5.2,  1.5, "Erdős",    "mathematics", "Itinerant\nConnection"),
    ( 3.0,  2.5, "Tao",      "mathematics", "Strategic\nMetacognition"),
    ( 6.5,  0.2, "Thurston", "mathematics", "Embodied\nGeometry"),
    # Meta — centre
    ( 1.2,  1.8, "Poincaré", "meta",        "Creative\nIncubation"),
    ( 1.0,  0.0, "Hofstadter","meta",       "Strange\nLoops"),
    (-0.5,  1.0, "Bateson",  "meta",        "Pattern\nConnects"),
    ( 2.2,  0.5, "Bach",     "meta",        "Computational\nPhilosophy"),
    (-1.0, -0.2, "Leopold",  "meta",        "Ethical\nPerception"),
    ( 0.5, -1.0, "Graeber",  "meta",        "Denaturali-\nsation"),
]

name_to_pos = {p[2]: (p[0], p[1]) for p in phantoms}


# === Rendering ================================================================
#
# render_phantom() is the ONLY function that decides how a node looks.
# Currently: Unicode glyph + glow circles.
# Future (option 4): swap body to OffsetImage + AnnotationBbox with PNG sprites.
# The interface stays: render_phantom(ax, x, y, name, colour, skill, ...).

# -- Font preference for glyph rendering --
# DejaVu Sans has excellent Unicode coverage including math symbols.
# Fall back to sans-serif if not available.
GLYPH_FONT = {"fontfamily": "DejaVu Sans", "fontweight": "bold"}
LABEL_FONT = {"fontfamily": "serif"}

def render_phantom(ax, x, y, name, colour, skill,
                   glyph_size=18, label_size=6.5, skill_size=4):
    """Render a single phantom node: glyph + name + skill label.

    This function is the single point of change for switching from
    Unicode glyphs (option 2) to PNG sprites (option 4). To do that:
      1. Change GLYPHS dict values from str to Path objects
      2. Replace the ax.text glyph call with:
           img = plt.imread(GLYPHS[name])
           ib = OffsetImage(img, zoom=...)
           ab = AnnotationBbox(ib, (x, y), frameon=False)
           ax.add_artist(ab)
      3. Keep glow circles, name label, and skill label as-is.
    """
    glyph = GLYPHS.get(name, "●")

    # Glow (soft halo behind the glyph)
    glow = Circle((x, y), 0.50, color=colour, alpha=0.06)
    ax.add_patch(glow)
    glow2 = Circle((x, y), 0.32, color=colour, alpha=0.10)
    ax.add_patch(glow2)

    # --- The glyph itself ---
    ax.text(x, y, glyph, fontsize=glyph_size, color=colour,
            ha="center", va="center", zorder=5, alpha=0.90,
            **GLYPH_FONT)

    # --- Name label below ---
    display_name = {
        "D'Arcy Thompson": "D'Arcy\nThompson",
        "McClintock": "McClin-\ntock",
    }.get(name, name)
    ax.text(x, y - 0.35, display_name, fontsize=label_size,
            fontweight="bold", color=colour, ha="center", va="top",
            zorder=6, linespacing=1.0, **LABEL_FONT)

    # --- Skill label below name ---
    two_line_names = {"D'Arcy Thompson", "McClintock"}
    skill_offset = -0.73 if name in two_line_names else -0.60
    ax.text(x, y + skill_offset, skill, fontsize=skill_size,
            fontstyle="italic", color=CHALK_DIM, ha="center",
            va="top", zorder=6, linespacing=1.1, **LABEL_FONT)


def render_construction(ax, x, y):
    """Render the central 'Construction' node — us, the builders."""
    col = COLOURS["us"]
    glyph = GLYPHS["Construction"]

    glow = Circle((x, y), 0.65, color=col, alpha=0.05)
    ax.add_patch(glow)
    glow2 = Circle((x, y), 0.40, color=col, alpha=0.08)
    ax.add_patch(glow2)

    ax.text(x, y, glyph, fontsize=22, color=col,
            ha="center", va="center", zorder=5, alpha=0.90,
            **GLYPH_FONT)

    ax.text(x, y - 0.42, "Construction", fontsize=7.5,
            fontweight="bold", color=col, ha="center", va="top",
            zorder=6, **LABEL_FONT)
    ax.text(x, y - 0.70, "Verified\nBuilding", fontsize=5,
            fontstyle="italic", color=CHALK_DIM,
            ha="center", va="top", zorder=6, linespacing=1.1,
            **LABEL_FONT)


# === Draw =====================================================================

# --- Chalk-dust texture ---
n_dust = 4000
dx = rng.uniform(-8.4, 8.4, n_dust)
dy = rng.uniform(-6.4, 6.4, n_dust)
ds = rng.uniform(0.1, 0.6, n_dust)
da = rng.uniform(0.01, 0.04, n_dust)
ax.scatter(dx, dy, s=ds, c=CHALK, alpha=da, edgecolors="none")

# --- Cluster labels (faint, large) ---
cluster_labels = [
    (-4.2,  5.6, "THE PHYSICISTS",      COLOURS["physics"]),
    (-7.5,  1.8, "THE MEASURERS",       COLOURS["measurement"]),
    (-6.8, -5.2, "THE BIOLOGISTS",      COLOURS["biology"]),
    (-1.2, -5.5, "THE INFORMATION\nTHEORISTS", COLOURS["information"]),
    ( 3.0, -4.8, "THE COMPUTATIONAL\nTHINKERS",  COLOURS["computation"]),
    ( 5.5,  5.2, "THE MATHEMATICIANS",  COLOURS["mathematics"]),
    (-0.2,  2.8, "THE META-\nTHINKERS", COLOURS["meta"]),
]
for x, y, label, col in cluster_labels:
    ax.text(x, y, label, fontsize=7, fontweight="bold",
            color=col, alpha=0.35, ha="center", va="center",
            linespacing=1.2, **LABEL_FONT)

# --- Correction edges (chalk lines) ---
corrections = [
    # Physics internal
    ("Landau", "Thorne"),
    ("Feynman", "Landau"),
    ("Susskind", "Feynman"),
    ("Wheeler", "Landau"),
    ("Wheeler", "Feynman"),
    # Measurement internal
    ("Faraday", "Helmholtz"),
    ("Humboldt", "Faraday"),
    # Biology internal
    ("Cajal", "D'Arcy Thompson"),
    ("D'Arcy Thompson", "Marr"),
    ("Braitenberg", "Marr"),
    ("Braitenberg", "Cajal"),
    ("Darwin", "D'Arcy Thompson"),
    ("Darwin", "McClintock"),
    ("McClintock", "Cajal"),
    ("Sapolsky", "Marr"),
    ("Sapolsky", "Darwin"),
    # Information internal
    ("Shannon", "Jaynes"),
    ("MacKay", "Jaynes"),
    # Computation internal
    ("Hinton", "Hopfield"),
    ("Karpathy", "Hinton"),
    # Mathematics internal
    ("Gauss", "Riemann"),
    ("Erdős", "Riemann"),
    ("Tao", "Gauss"),
    # Meta internal
    ("Poincaré", "Tao"),
    ("Hofstadter", "Karpathy"),
    ("Bateson", "Jaynes"),
    ("Bach", "Hofstadter"),
    ("Bach", "Karpathy"),
    ("Leopold", "Bateson"),
    ("Leopold", "Humboldt"),
    ("Graeber", "Leopold"),
    ("Graeber", "Bateson"),
    # Cross-cluster bridges
    ("Thurston", "Landau"),
    ("Helmholtz", "Landau"),
    ("Shannon", "Susskind"),
    ("Hopfield", "Thurston"),
    ("MacKay", "Karpathy"),
    ("Poincaré", "Feynman"),
    ("Bateson", "Humboldt"),
    ("Wheeler", "Hofstadter"),
    ("Wheeler", "Shannon"),
    # Biology bridges
    ("Cajal", "Faraday"),
    ("D'Arcy Thompson", "Gauss"),
    ("D'Arcy Thompson", "Riemann"),
    ("Braitenberg", "Karpathy"),
    ("Braitenberg", "Hinton"),
    ("Marr", "Hofstadter"),
    ("Marr", "Bateson"),
    ("Humboldt", "Cajal"),
    ("Helmholtz", "Marr"),
    ("Sapolsky", "Bateson"),
    ("Darwin", "Gauss"),
    ("Bach", "Braitenberg"),
    ("Graeber", "Wheeler"),
    ("McClintock", "Gauss"),
]

for n1, n2 in corrections:
    x1, y1 = name_to_pos[n1]
    x2, y2 = name_to_pos[n2]
    n_pts = 40
    t = np.linspace(0, 1, n_pts)
    jx = rng.normal(0, 0.02, n_pts)
    jy = rng.normal(0, 0.02, n_pts)
    lx = x1 + (x2 - x1) * t + jx
    ly = y1 + (y2 - y1) * t + jy
    ax.plot(lx, ly, color=CHALK_DIM, lw=0.4, alpha=0.25)

# --- Phantom nodes (glyphs) ---
for x, y, name, cluster, skill in phantoms:
    w = WEIGHTS.get(name, {cluster: 1.0})
    col = blend_colour(w)
    render_phantom(ax, x, y, name, col, skill)

# --- Construction node (centre) ---
cx, cy = 0.5, -0.5
render_construction(ax, cx, cy)

# Connect Construction to selected phantoms
for target in ["Feynman", "Karpathy", "MacKay", "Gauss",
               "Helmholtz", "Hofstadter", "Braitenberg", "Bach"]:
    tx, ty = name_to_pos[target]
    n_pts = 40
    t = np.linspace(0, 1, n_pts)
    lx = cx + (tx - cx) * t + rng.normal(0, 0.02, n_pts)
    ly = cy + (ty - cy) * t + rng.normal(0, 0.02, n_pts)
    ax.plot(lx, ly, color=CHALK, lw=0.5, alpha=0.18)

# --- Title ---
ax.text(0, 6.2, "THE PHANTOM FACULTY",
        fontsize=18, fontweight="bold",
        color=CHALK, ha="center", va="center", zorder=7,
        alpha=0.9, **LABEL_FONT)
ax.text(0, 5.75, "thirty-one cognitive modes for scientific understanding",
        fontsize=9, fontstyle="italic",
        color=CHALK_DIM, ha="center", va="center", zorder=7,
        **LABEL_FONT)

# --- Bottom attribution ---
ax.text(0, -6.3,
        "each glyph is a mode of cognition  ·  "
        "colour blends all faculties a phantom belongs to  ·  "
        "each edge connects a mode to its corrective",
        fontsize=5, fontstyle="italic",
        color=CHALK_DIM, ha="center", va="center", alpha=0.5,
        **LABEL_FONT)

# === Save =====================================================================

out_dir = Path(__file__).parent
out = out_dir / "the-faculty-assembled.png"
fig.savefig(out, bbox_inches="tight", dpi=200,
            facecolor=fig.get_facecolor(), pad_inches=0.2)
print(f"Saved: {out}")
plt.close()
