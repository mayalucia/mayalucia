+++
title = "The Dyer's Gorge"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-26T14:56:19+01:00
tags = ["writing"]
draft = false
description = "A dyer in the Parvati gorge reads the valley by its pigments --- iron-red from hot springs, indigo from wild bushes, lichen-gold from birch boulders --- encoding altitude into cloth"
+++

## Prefatory Note on Colour {#prefatory-note-on-colour}

What follows was found among the papers of one Kamala Devi, dyer of Tosh village, Parvati valley, district Kullu. The manuscript — if a collection of dyed cloth swatches, marginal annotations, and what appear to be recipes written in a private notation can be called a manuscript — was discovered in a stone storehouse above the village after the last of her apprentices had gone to work in the hotels at Kasol. No one could read the notation. It is reproduced here with such interpretation as the editors could manage, supplemented by the valley's own testimony: its stones, its waters, its remaining pigments.

The reader should know that Kamala Devi never wrote a word about dyeing. She dyed. The words are ours, draped clumsily over her silences like undyed wool over a branch — waiting for colour that may not come.

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib import cm

# ============================================================
# The Parvati Valley Chromatic Palette
# Altitude bands from the Manikaran gorge floor (~1700m)
# to the Pin Parvati glacier (~5300m)
# ============================================================

# Each altitude band: (name, elevation_range, colours, source)
# Colours are hand-chosen from the valley's geology and ecology.

VALLEY_PALETTE = {
    "Hot Springs Floor": {
        "elevation": (1700, 2000),
        "colours": [
            ("#C45824", "iron oxide — Manikaran deposit"),
            ("#E8B960", "sulphur crust — thermal vent"),
            ("#D4A574", "travertine — mineral terrace"),
            ("#8B4513", "manganese stain — wet rock"),
            ("#F5DEB3", "silica sinter — dried spring"),
        ],
    },
    "River Gorge": {
        "elevation": (2000, 2300),
        "colours": [
            ("#2E6B5A", "jade water — glacial flour"),
            ("#4A7C6F", "river moss — submerged boulder"),
            ("#6B8E7B", "wet slate — gorge wall"),
            ("#3D5C4E", "deep pool — shadowed"),
            ("#8FBC8F", "spray zone — lichen on mist-rock"),
        ],
    },
    "Deodar Forest": {
        "elevation": (2300, 2800),
        "colours": [
            ("#2D4A2D", "deodar canopy — deep shade"),
            ("#556B2F", "pine needle — autumn floor"),
            ("#8B7355", "bark — old growth"),
            ("#4A5D3A", "fern understory — monsoon"),
            ("#3B5323", "moss carpet — north face"),
        ],
    },
    "Birch & Rhododendron": {
        "elevation": (2800, 3500),
        "colours": [
            ("#F0E6D2", "birch bark — peeling silver"),
            ("#C41E3A", "rhododendron — spring bloom"),
            ("#DAA520", "lichen — birch trunk"),
            ("#8B6914", "dead leaf — autumn birch"),
            ("#E8C4A0", "birch litter — winter floor"),
        ],
    },
    "Alpine Meadow": {
        "elevation": (3500, 4200),
        "colours": [
            ("#7B68EE", "iris — summer meadow"),
            ("#9370DB", "aster — late monsoon"),
            ("#90EE90", "new grass — snowmelt"),
            ("#BDB76B", "dry grass — autumn"),
            ("#4169E1", "gentian — rocky outcrop"),
        ],
    },
    "Moraine & Scree": {
        "elevation": (4200, 4800),
        "colours": [
            ("#708090", "slate — fresh break"),
            ("#A0A0A0", "granite — weathered"),
            ("#5F5F5F", "gneiss — wet"),
            ("#C0C0C0", "quartzite — sun-bleached"),
            ("#4A4A4A", "schist — dark foliation"),
        ],
    },
    "Glacier & Snow": {
        "elevation": (4800, 5319),
        "colours": [
            ("#E8F0FE", "fresh snow — morning"),
            ("#B0C4DE", "glacier ice — compressed"),
            ("#DCDCF0", "névé — granular"),
            ("#A8C0D8", "crevasse blue — deep ice"),
            ("#F0F8FF", "wind crust — afternoon glare"),
        ],
    },
}

fig, ax = plt.subplots(figsize=(14, 20))
ax.set_xlim(0, 10)
ax.set_ylim(1600, 5400)
ax.set_aspect('auto')

# Draw altitude bands as horizontal strips filled with colour swatches
for band_name, band_data in VALLEY_PALETTE.items():
    lo, hi = band_data["elevation"]
    mid = (lo + hi) / 2
    band_height = hi - lo
    colours = band_data["colours"]
    n = len(colours)

    # Each swatch is a rectangle within the band
    swatch_width = 8.0 / n
    for i, (hex_colour, source_name) in enumerate(colours):
        x = 1.0 + i * swatch_width
        # Rectangles with slight vertical jitter for organic feel
        jitter = np.random.uniform(-band_height * 0.05, band_height * 0.05)
        rect = mpatches.FancyBboxPatch(
            (x, lo + band_height * 0.08 + jitter),
            swatch_width * 0.88,
            band_height * 0.65,
            boxstyle="round,pad=0.02",
            facecolor=hex_colour,
            edgecolor="#2A2A2A",
            linewidth=0.5,
            alpha=0.92,
        )
        ax.add_patch(rect)

        # Source annotation — tiny, tilted, like a dyer's marginal note
        ax.text(
            x + swatch_width * 0.44,
            lo + band_height * 0.08 + jitter + band_height * 0.32,
            source_name.split("—")[-1].strip() if "—" in source_name else source_name,
            fontsize=5.0,
            ha="center",
            va="center",
            rotation=90,
            color="#1A1A1A" if hex_colour > "#888888" else "#E8E8E8",
            fontstyle="italic",
            fontfamily="serif",
        )

    # Band label on the right margin
    ax.text(
        9.4, mid, f"{band_name}\n{lo}–{hi}m",
        fontsize=7,
        ha="left",
        va="center",
        fontfamily="serif",
        fontstyle="italic",
        color="#3A3A3A",
    )

    # Thin horizontal line at band boundary
    ax.axhline(y=lo, color="#AAAAAA", linewidth=0.3, linestyle=":")

# Top boundary
ax.axhline(y=5319, color="#AAAAAA", linewidth=0.3, linestyle=":")

# Title
ax.text(
    5.0, 5370,
    "Chromatic Stratigraphy of the Parvati Valley",
    fontsize=13,
    ha="center",
    va="bottom",
    fontfamily="serif",
    fontweight="bold",
    color="#2A2A2A",
)
ax.text(
    5.0, 5340,
    "From the hot springs at Manikaran (1700m) to the Pin Parvati glacier (5319m)",
    fontsize=8,
    ha="center",
    va="bottom",
    fontfamily="serif",
    fontstyle="italic",
    color="#5A5A5A",
)

# Left axis label
ax.set_ylabel("Elevation (metres)", fontsize=9, fontfamily="serif")
ax.yaxis.set_major_locator(plt.MultipleLocator(500))
ax.yaxis.set_minor_locator(plt.MultipleLocator(100))
ax.tick_params(axis="y", labelsize=7)
ax.set_xticks([])

# Spine styling
for spine in ["top", "right", "bottom"]:
    ax.spines[spine].set_visible(False)
ax.spines["left"].set_color("#888888")
ax.spines["left"].set_linewidth(0.5)

# Attribution
ax.text(
    5.0, 1620,
    "From the notebooks of Kamala Devi, dyer of Tosh — reconstructed",
    fontsize=6,
    ha="center",
    va="bottom",
    fontfamily="serif",
    fontstyle="italic",
    color="#999999",
)

fig.patch.set_facecolor("#FEFCF5")  # Aged paper
ax.set_facecolor("#FEFCF5")

plt.tight_layout()
plt.savefig("palette-altitude.png", dpi=200, bbox_inches="tight",
            facecolor="#FEFCF5", edgecolor="none")
print("palette-altitude.png")
```

{{< figure src="/ox-hugo/palette-altitude.png" >}}


## I. The Valley That Swallows Light {#i-dot-the-valley-that-swallows-light}

In the Parvati gorge the light arrives late and departs early. This is not a valley that the sun crosses — it is a valley the sun _peers into_, briefly, at midday, before withdrawing behind one ridge or another. The river runs a thousand metres below the ridgeline, and in winter the gorge floor may see direct sunlight for only four hours. Everything that lives here has learned to work in shade.

Kamala Devi learned colour in this shade. Her mother's mother had kept a dye-house in Tosh, on the south-facing slope above the gorge, where the village catches what sun the valley permits. The dye-house was a single room of stacked slate with a beaten-earth floor and three iron vats set over a hearth that was never allowed to go cold between Baisakhi and the first snow. In summer, when the Gaddi shepherds brought their flocks down from the Chandrakhani pass, the raw wool arrived still warm from the animals, greasy with lanolin, carrying the particular smell of whatever altitude the sheep had grazed. Kamala Devi claimed she could tell, by smell alone, whether wool had come from above or below the treeline.

This was not a boast. It was a technical statement. The lanolin composition varies with the grazing — sheep that eat alpine flowers produce a different grease than sheep that browse on deodar needles. The grease affects how the fibre takes the dye. A colour that blooms rich and saturated on high-meadow wool may turn muddy on forest wool, and vice versa. The dyer who cannot read the wool will waste the pigment.

_The pigment is the valley_, she is supposed to have said, though the attribution is uncertain. _The wool is the season. The mordant is the patience. The colour is what happens when all three agree._

She had a system — or rather, the valley had a system, and she had learned to read it. The pigments came from specific altitudes, as fixed in their vertical distribution as the vegetation bands themselves. Iron oxide from the hot spring deposits at Manikaran. Indigo from the wild _Indigofera_ that grew in disturbed ground below Tosh, where the old foot-trails had been widened for mule traffic. Lichen yellows from the birch forests above Pulga, harvestable only in autumn after the monsoon moisture had concentrated the pigment. Walnut-hull browns from the groves at Jari. Slate-blacks from the schist outcrops above the treeline, ground to powder in a stone mortar that had been in the family since before anyone could remember.

Each pigment had its altitude. Each altitude had its season. The dyer's calendar was not a calendar of days but of _vertical migrations_ — she climbed and descended the valley's flanks following the pigments as they ripened, the way the Gaddi followed the grass.

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patheffects import withStroke

# ============================================================
# Dye Recipe Diagram: Manikaran Red
# The iron-oxide dye process, rendered as a flow
# from pigment source to finished colour on wool
# ============================================================

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.set_aspect("equal")

PAPER = "#FEFCF5"
INK = "#2A2A2A"
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

# --- The source: hot spring deposit ---
# A mound of iron-oxide pigment, rendered as overlapping warm circles
np.random.seed(42)
for _ in range(60):
    x = np.random.normal(2.0, 0.6)
    y = np.random.normal(6.0, 0.4)
    r = np.random.uniform(0.05, 0.2)
    c = np.random.choice(["#C45824", "#E8B960", "#D4A574", "#8B4513", "#B85C2A"])
    circle = plt.Circle((x, y), r, color=c, alpha=np.random.uniform(0.3, 0.7))
    ax.add_patch(circle)

ax.text(2.0, 5.2, "Iron oxide\nManikaran deposit\n1700m",
        fontsize=7, ha="center", va="top", fontfamily="serif",
        fontstyle="italic", color="#5A3A2A")

# --- Arrow: collection ---
ax.annotate("", xy=(4.0, 6.0), xytext=(3.0, 6.0),
            arrowprops=dict(arrowstyle="->", color="#8B4513", lw=1.5))
ax.text(3.5, 6.25, "ground in\nstone mortar", fontsize=6, ha="center",
        fontfamily="serif", fontstyle="italic", color="#8B4513")

# --- The mordant bath ---
# Alum crystals rendered as angular shapes
mordant_x, mordant_y = 5.0, 6.0
for _ in range(25):
    cx = mordant_x + np.random.normal(0, 0.4)
    cy = mordant_y + np.random.normal(0, 0.3)
    angle = np.random.uniform(0, 360)
    size = np.random.uniform(0.06, 0.15)
    diamond = mpatches.RegularPolygon((cx, cy), 6, radius=size, orientation=np.radians(angle),
                                       facecolor="#D4C4A0", edgecolor="#A09070",
                                       linewidth=0.3, alpha=0.7)
    ax.add_patch(diamond)

ax.text(5.0, 5.3, "Alum mordant\n(phitkari)\nfrom Kullu bazaar",
        fontsize=7, ha="center", va="top", fontfamily="serif",
        fontstyle="italic", color="#6A5A4A")

# --- Arrow: dissolve ---
ax.annotate("", xy=(7.0, 6.0), xytext=(5.8, 6.0),
            arrowprops=dict(arrowstyle="->", color="#8B4513", lw=1.5))
ax.text(6.4, 6.25, "dissolved in\nhot spring water", fontsize=6, ha="center",
        fontfamily="serif", fontstyle="italic", color="#8B4513")

# --- The dye vat ---
# An elliptical vessel with simmering colour
vat_x, vat_y = 8.5, 6.0
vat = mpatches.Ellipse((vat_x, vat_y), 2.0, 1.4,
                         facecolor="#C45824", edgecolor="#4A2A1A",
                         linewidth=2, alpha=0.6)
ax.add_patch(vat)
# Steam wisps
for i in range(5):
    sx = vat_x + np.random.uniform(-0.5, 0.5)
    sy = vat_y + 0.8 + i * 0.15
    ax.plot([sx, sx + np.random.uniform(-0.2, 0.2)],
            [sy, sy + 0.3], color="#D4A574", alpha=0.3 - i * 0.05,
            linewidth=1)

ax.text(8.5, 5.0, "Iron vat\nover hearth-fire\nnever allowed cold",
        fontsize=7, ha="center", va="top", fontfamily="serif",
        fontstyle="italic", color="#5A3A2A")

# --- The wool enters from below ---
# Raw wool: a cloud of cream-colored fibres
wool_x, wool_y = 2.0, 2.5
for _ in range(40):
    wx = wool_x + np.random.normal(0, 0.5)
    wy = wool_y + np.random.normal(0, 0.3)
    length = np.random.uniform(0.2, 0.6)
    angle = np.random.uniform(0, np.pi)
    ax.plot([wx, wx + length * np.cos(angle)],
            [wy, wy + length * np.sin(angle)],
            color="#F5DEB3", alpha=0.6, linewidth=np.random.uniform(0.5, 1.5))

ax.text(2.0, 1.8, "Raw wool\nhigh-meadow sheep\nChandrakhani flock\n3800m grazing",
        fontsize=7, ha="center", va="top", fontfamily="serif",
        fontstyle="italic", color="#6A5A4A")

# --- Arrow: scoured and wetted ---
ax.annotate("", xy=(5.0, 2.5), xytext=(3.2, 2.5),
            arrowprops=dict(arrowstyle="->", color="#8B7355", lw=1.5))
ax.text(4.1, 2.9, "scoured in\nash-water", fontsize=6, ha="center",
        fontfamily="serif", fontstyle="italic", color="#8B7355")

# --- Mordanted wool ---
for _ in range(40):
    wx = 5.5 + np.random.normal(0, 0.4)
    wy = 2.5 + np.random.normal(0, 0.25)
    length = np.random.uniform(0.2, 0.5)
    angle = np.random.uniform(0, np.pi)
    ax.plot([wx, wx + length * np.cos(angle)],
            [wy, wy + length * np.sin(angle)],
            color="#E8D8B8", alpha=0.6, linewidth=np.random.uniform(0.5, 1.5))

ax.text(5.5, 1.8, "Mordanted wool\nalum-soaked\novernight",
        fontsize=7, ha="center", va="top", fontfamily="serif",
        fontstyle="italic", color="#6A5A4A")

# --- Arrow: into the vat ---
ax.annotate("", xy=(8.5, 4.8), xytext=(6.2, 2.8),
            arrowprops=dict(arrowstyle="->", color="#C45824", lw=2,
                          connectionstyle="arc3,rad=0.3"))
ax.text(7.0, 3.6, "submerged\nthree hours\ngentle simmer",
        fontsize=6, ha="center", fontfamily="serif",
        fontstyle="italic", color="#C45824")

# --- The finished colour: dyed wool ---
for _ in range(50):
    wx = 10.5 + np.random.normal(0, 0.5)
    wy = 2.5 + np.random.normal(0, 0.35)
    length = np.random.uniform(0.2, 0.6)
    angle = np.random.uniform(0, np.pi)
    ax.plot([wx, wx + length * np.cos(angle)],
            [wy, wy + length * np.sin(angle)],
            color="#C45824", alpha=np.random.uniform(0.4, 0.8),
            linewidth=np.random.uniform(0.8, 2.0))

ax.text(10.5, 1.6, "MANIKARAN RED\non high-meadow wool\nthe mountain's\nfirst colour",
        fontsize=8, ha="center", va="top", fontfamily="serif",
        fontweight="bold", color="#8B3014")

# --- Arrow: from vat to finished ---
ax.annotate("", xy=(9.8, 2.5), xytext=(8.5, 4.8),
            arrowprops=dict(arrowstyle="->", color="#C45824", lw=2,
                          connectionstyle="arc3,rad=-0.3"))
ax.text(9.8, 4.0, "lifted,\nrinsed in\ncold river",
        fontsize=6, ha="right", fontfamily="serif",
        fontstyle="italic", color="#C45824")

# --- Title ---
ax.text(6.0, 7.8, "Dye Recipe No. 1: Manikaran Red",
        fontsize=14, ha="center", va="top", fontfamily="serif",
        fontweight="bold", color=INK)
ax.text(6.0, 7.35, "Iron oxide on alum-mordanted high-meadow wool",
        fontsize=9, ha="center", va="top", fontfamily="serif",
        fontstyle="italic", color="#5A5A5A")

# --- Attribution ---
ax.text(6.0, 0.15,
        "Reconstructed from swatches and notation — Kamala Devi archive, Tosh",
        fontsize=5.5, ha="center", fontfamily="serif",
        fontstyle="italic", color="#AAAAAA")

ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig("dye-recipe-manikaran-red.png", dpi=200, bbox_inches="tight",
            facecolor=PAPER, edgecolor="none")
print("dye-recipe-manikaran-red.png")
```

{{< figure src="/ox-hugo/dye-recipe-manikaran-red.png" >}}


## II. Five Pigments, Five Altitudes {#ii-dot-five-pigments-five-altitudes}

The dyer's year began not in spring but in autumn, when the lichen ripened.

Above Pulga, where the birch forest thins to twisted trunks and the first boulders of the moraine appear, the rocks wear coats of _Xanthoria_ and _Usnea_ — orange and grey-green, the colours of patience. Lichen grows slowly. A palm-sized colony may be older than the village below. Kamala Devi harvested with a flat blade, taking no more than a third of any rock's coat, returning to the same boulders each year the way a farmer returns to the same fields. She had names for the boulders. This was not sentiment. It was inventory management.

The _Xanthoria_ gave yellows. Not the sharp cadmium yellow of chemical dyes that arrived later in plastic bottles from Bhuntar, but a yellow that remembered where it came from — warm, slightly orange, the colour of late afternoon on south-facing rock. On sheep-wool it deepened to gold. On goat-hair it turned tawny. On the coarse yak-fibre that came over the pass from Lahaul, it barely registered at all, as if the yak, being a creature of even higher altitudes than the lichen, refused to accept colour from below its station.

The indigo grew wild. _Indigofera heterantha_ — the Himalayan indigo, not the cultivated tropical plant but its mountain cousin, a scrubby bush with pink flowers that colonised disturbed ground along the old trade paths. The dye came from the leaves, fermented in an alkaline bath of ash-water and stale urine (the latter contributed by the dyer's household without comment or ceremony). The fermentation vat was kept in the darkest corner of the dye-house, covered with a slate lid, and consulted daily the way one might consult an oracle: by smell, by the colour of the surface scum, by the tiny bubbles that indicated active chemistry or its cessation.

Indigo was the valley's most democratic colour. It took to every fibre — sheep, goat, yak — with equal willingness. It was also the most treacherous. The depth of colour depended on the number of immersions, each followed by oxidation in air, and the precise moment of oxidation determined whether the blue would tend toward green (too early) or purple (too late). The dyer's hands were permanently stained. The stain was not a mark of the trade but the trade itself, written on the skin.

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ============================================================
# Five Pigments, Five Altitudes
# Each pigment shown as a swatch gradient on three fibres:
# sheep-wool, goat-hair, yak-fibre
# ============================================================

PAPER = "#FEFCF5"
INK = "#2A2A2A"

fig, axes = plt.subplots(5, 1, figsize=(12, 16), gridspec_kw={"hspace": 0.4})
fig.patch.set_facecolor(PAPER)

pigments = [
    {
        "name": "Manikaran Red",
        "source": "Iron oxide — hot spring deposit, 1700m",
        "on_sheep": ["#F5DEB3", "#E8B090", "#D4836A", "#C45824", "#A84420"],
        "on_goat": ["#E8D8C8", "#D4A888", "#B87858", "#9C5838", "#7A3818"],
        "on_yak": ["#D4C4B4", "#C4A494", "#A48474", "#8B6454", "#6B4A3A"],
        "note": "Darkens with each immersion. On yak-fibre, tends to umber.",
    },
    {
        "name": "Lichen Gold",
        "source": "Xanthoria — birch forest boulders, 3200m",
        "on_sheep": ["#F5DEB3", "#F0D48A", "#E8C44A", "#DAA520", "#C49210"],
        "on_goat": ["#E8D8C8", "#D8C4A0", "#C8A870", "#B08840", "#8B6914"],
        "on_yak": ["#D4C4B4", "#CCC0A8", "#C4B89C", "#B8A888", "#A09078"],
        "note": "Barely registers on yak. The creature refuses colour from below its station.",
    },
    {
        "name": "Parvati Indigo",
        "source": "Indigofera heterantha — disturbed ground, 2100m",
        "on_sheep": ["#F5DEB3", "#C4C8D8", "#8090B8", "#4A5A98", "#2A3A78"],
        "on_goat": ["#E8D8C8", "#B8B8C8", "#8888A8", "#585888", "#383868"],
        "on_yak": ["#D4C4B4", "#A8A8B8", "#7878A0", "#4A4A80", "#2A2A60"],
        "note": "The most democratic colour. Takes to all fibres equally. Depth by immersion count.",
    },
    {
        "name": "Walnut Hull",
        "source": "Juglans regia — groves at Jari, 1900m",
        "on_sheep": ["#F5DEB3", "#D4B898", "#B89878", "#8B7355", "#6B5335"],
        "on_goat": ["#E8D8C8", "#C8A888", "#A88868", "#886848", "#684828"],
        "on_yak": ["#D4C4B4", "#B8A898", "#9C8C7C", "#7A6A5A", "#5A4A3A"],
        "note": "Needs no mordant. The tannins fix themselves. Patient colour.",
    },
    {
        "name": "Slate Black",
        "source": "Graphitic schist — above treeline, 4000m",
        "on_sheep": ["#F5DEB3", "#C8C0B0", "#9A9488", "#6A6660", "#3A3838"],
        "on_goat": ["#E8D8C8", "#B8B0A4", "#888480", "#58585A", "#2A2A2E"],
        "on_yak": ["#D4C4B4", "#A8A098", "#7C787C", "#50505A", "#1A1A24"],
        "note": "Ground in the family mortar. On yak-fibre, approaches true black.",
    },
]

fibre_labels = ["Sheep-wool\n(high meadow)", "Goat-hair\n(Malana breed)", "Yak-fibre\n(Lahaul)"]

for ax, p in zip(axes, pigments):
    ax.set_facecolor(PAPER)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.set_aspect("auto")

    # Title
    ax.text(0.2, 3.6, p["name"], fontsize=12, fontweight="bold",
            fontfamily="serif", color=INK, va="top")
    ax.text(0.2, 3.0, p["source"], fontsize=8, fontfamily="serif",
            fontstyle="italic", color="#6A6A6A", va="top")

    # Three rows of gradient swatches
    for row, (fibre, label) in enumerate(zip(
            [p["on_sheep"], p["on_goat"], p["on_yak"]], fibre_labels)):
        y = 2.0 - row * 0.85
        ax.text(0.2, y + 0.25, label, fontsize=6, fontfamily="serif",
                color="#6A6A6A", va="center")

        for j, colour in enumerate(fibre):
            x = 2.8 + j * 1.6
            # Draw fibre-textured swatch: short random lines in the colour
            np.random.seed(hash(colour) % 2**31)
            for _ in range(30):
                fx = x + np.random.uniform(0, 1.3)
                fy = y + np.random.uniform(-0.2, 0.2)
                fl = np.random.uniform(0.1, 0.4)
                angle = np.random.uniform(-0.15, 0.15)  # mostly horizontal
                ax.plot([fx, fx + fl * np.cos(angle)],
                        [fy, fy + fl * np.sin(angle)],
                        color=colour, linewidth=np.random.uniform(1.0, 2.5),
                        alpha=np.random.uniform(0.5, 0.9), solid_capstyle="round")

        # Immersion count labels
        for j in range(5):
            ax.text(2.8 + j * 1.6 + 0.65, 2.55,
                    f"{j + 1}x" if row == 0 else "",
                    fontsize=6, ha="center", fontfamily="serif", color="#999999")

    # Dyer's note
    ax.text(11.8, 0.3, p["note"], fontsize=6, fontfamily="serif",
            fontstyle="italic", color="#8A7A6A", ha="right", va="bottom",
            wrap=True,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=PAPER, edgecolor="#D4C4A4",
                     linewidth=0.5))

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

# Supertitle
fig.suptitle("Five Pigments on Three Fibres",
             fontsize=16, fontfamily="serif", fontweight="bold",
             color=INK, y=0.98)
fig.text(0.5, 0.96,
         "Immersion gradients — from raw fibre (1x) to full saturation (5x)",
         fontsize=9, ha="center", fontfamily="serif", fontstyle="italic",
         color="#6A6A6A")
fig.text(0.5, 0.01,
         "Reconstructed from the Kamala Devi swatch archive, Tosh village",
         fontsize=6, ha="center", fontfamily="serif", fontstyle="italic",
         color="#AAAAAA")

plt.savefig("five-pigments.png", dpi=200, bbox_inches="tight",
            facecolor=PAPER, edgecolor="none")
print("five-pigments.png")
```

{{< figure src="/ox-hugo/five-pigments.png" >}}


## III. What the Wool Remembers {#iii-dot-what-the-wool-remembers}

The Gaddi came down from the Chandrakhani pass in late September, their flocks spread across the trail like a white river flowing downhill. The sheep moved in a logic of their own — not single-file like goats but in shifting clusters, continually regrouping, as if conducting an argument about direction that was never quite resolved. The dogs moved at the edges, not herding so much as _defining the boundary_ within which the argument was permitted.

Kamala Devi met them at the edge of Tosh, where the trail enters the village through a gap in the dry-stone wall. She did not greet the shepherds first. She went to the sheep. She pushed her hands into the fleece of the lead animals, closed her eyes, and read.

High-meadow wool. Above the treeline, certainly — the lanolin was thin and dry, almost waxy, without the resinous undertone that forest grazing imparted. The staple was long, crimped loosely — the sheep had not been stressed. Good monsoon, then. Enough grass at altitude that they hadn't needed to descend early into the forest belt where competition with the village goats made them tense, tightening the crimp. She opened her eyes and nodded to the shepherd. _Good wool this year._

The reading was not mystical. It was a fibre assay conducted by hand, drawing on a database stored in muscle memory and olfactory recall rather than in any written record. Kamala Devi had been doing this since she could reach the sheep's backs without standing on a stone. Sixty years of data, indexed by touch.

She selected the fleeces she wanted — always from specific animals, whose wool she had tracked across years the way an oenologist tracks vintages. The shepherd sheared them on the spot, on a flat rock outside the wall, and Kamala Devi carried the fleeces to the dye-house in a basket on her back, already sorting by hand as she walked: the belly wool (coarser, for warp threads) separated from the shoulder wool (finer, for weft), the neck wool (shortest staple, for felting) set aside.

The carding would take days. The spinning, weeks. Only then, when the fibre had been opened, aligned, and twisted into yarn, would she begin to think about colour.

But she was already thinking about colour. She had been thinking about colour since her hands entered the fleece. The wool had told her what it wanted.

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patheffects as pe

# ============================================================
# What the Wool Remembers
# A diagram of fleece-reading: the dyer's hands in the wool,
# the information encoded in fibre
# ============================================================

PAPER = "#FEFCF5"
INK = "#2A2A2A"

fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.set_aspect("equal")

# --- The fleece: a large cloud of fibres ---
np.random.seed(7)
fleece_cx, fleece_cy = 7.0, 5.0

# Body of fleece — varying cream/white tones
for _ in range(400):
    fx = fleece_cx + np.random.normal(0, 2.5)
    fy = fleece_cy + np.random.normal(0, 1.8)
    # Exclude a central zone (where the hands are)
    if (fx - fleece_cx)**2 / 1.2 + (fy - fleece_cy)**2 / 0.8 < 1.0:
        continue
    length = np.random.uniform(0.3, 0.8)
    # Crimp: slight sinusoidal path
    t = np.linspace(0, length, 15)
    angle = np.random.uniform(-0.3, 0.3)
    crimp_amp = np.random.uniform(0.02, 0.08)
    crimp_freq = np.random.uniform(8, 15)
    xs = fx + t * np.cos(angle) + crimp_amp * np.sin(crimp_freq * t)
    ys = fy + t * np.sin(angle) + crimp_amp * np.cos(crimp_freq * t)
    shade = np.random.choice(["#F5ECD8", "#F0E6D0", "#EBE0C8", "#E8DCC0", "#FFF8E8"])
    ax.plot(xs, ys, color=shade, linewidth=np.random.uniform(0.8, 1.8),
            alpha=np.random.uniform(0.4, 0.8), solid_capstyle="round")

# --- The hands: two simplified outlines ---
# Left hand
left_hand = np.array([
    [6.0, 5.6], [5.8, 5.3], [5.7, 4.8], [5.8, 4.4], [6.0, 4.2],
    [6.2, 4.4], [6.3, 4.8], [6.4, 5.2], [6.5, 5.5], [6.4, 5.7],
    [6.2, 5.8], [6.0, 5.6]
])
ax.fill(left_hand[:, 0], left_hand[:, 1], color="#C4956A", alpha=0.7,
        edgecolor="#8B6540", linewidth=1.5)

# Right hand
right_hand = left_hand.copy()
right_hand[:, 0] = 14.0 - right_hand[:, 0]  # Mirror
ax.fill(right_hand[:, 0], right_hand[:, 1], color="#C4956A", alpha=0.7,
        edgecolor="#8B6540", linewidth=1.5)

# --- Annotations radiating from the fleece ---
annotations = [
    (3.0, 8.5, "Lanolin: thin, waxy\n→ above treeline", "#8B7355"),
    (11.0, 8.5, "Staple length: 12cm\n→ good monsoon", "#556B2F"),
    (1.5, 5.0, "Crimp: loose, even\n→ unstressed animal", "#4A7C6F"),
    (12.5, 5.0, "Odour: alpine herb\n→ no forest browse", "#7B68EE"),
    (3.0, 1.5, "Belly wool: coarse\n→ warp thread", "#C45824"),
    (7.0, 1.2, "Shoulder: fine, soft\n→ weft thread", "#DAA520"),
    (11.0, 1.5, "Neck: short staple\n→ felting only", "#708090"),
]

for (ax_, ay, text, colour) in annotations:
    # Draw line from annotation to fleece edge
    dx = fleece_cx - ax_
    dy = fleece_cy - ay
    dist = np.sqrt(dx**2 + dy**2)
    # Find point on fleece boundary (roughly elliptical)
    angle = np.arctan2(dy, dx)
    edge_x = fleece_cx - 2.5 * np.cos(angle)
    edge_y = fleece_cy - 1.8 * np.sin(angle)

    ax.plot([ax_, edge_x], [ay, edge_y],
            color=colour, linewidth=0.8, alpha=0.5, linestyle="--")
    ax.plot(edge_x, edge_y, "o", color=colour, markersize=3, alpha=0.7)

    ax.text(ax_, ay, text, fontsize=7, fontfamily="serif", fontstyle="italic",
            color=colour, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=PAPER,
                     edgecolor=colour, linewidth=0.5, alpha=0.9))

# --- Central text ---
ax.text(7.0, 5.0, "reading",
        fontsize=10, fontfamily="serif", fontstyle="italic",
        ha="center", va="center", color="#6A5A4A", alpha=0.6)

# --- Title ---
ax.text(7.0, 9.7, "What the Wool Remembers",
        fontsize=16, fontfamily="serif", fontweight="bold",
        ha="center", va="top", color=INK)
ax.text(7.0, 9.2, "A fibre assay by hand — sixty years of data, indexed by touch",
        fontsize=9, fontfamily="serif", fontstyle="italic",
        ha="center", va="top", color="#6A6A6A")

# Attribution
ax.text(7.0, 0.2,
        "From the practice of Kamala Devi, dyer of Tosh — observed, never written",
        fontsize=6, ha="center", fontfamily="serif",
        fontstyle="italic", color="#AAAAAA")

for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
plt.savefig("wool-reading.png", dpi=200, bbox_inches="tight",
            facecolor=PAPER, edgecolor="none")
print("wool-reading.png")
```

{{< figure src="/ox-hugo/wool-reading.png" >}}


## IV. The Gradient Problem {#iv-dot-the-gradient-problem}

Here is what the Thread Walkers of Ladakh never had to solve: the problem of _vertical coherence_.

In the high passes between Kullu and Leh, the terrain is brutal but _uniform_. One crosses a threshold — the pass — and the world changes entirely. This side, that side. The workshops communicated across a horizontal barrier, and the Thread Walkers' protocols evolved to maintain coherence between entities that were _separated but equivalent_. The same altitude, roughly. The same fibre. The same cold.

The Parvati valley poses a different problem. Here the barrier is not a pass but the valley itself — the vertical gradient from riverbed to ridgeline, compressed into a few horizontal kilometres. Tosh at 2400 metres and the alpine meadows at 3800 metres are separated by only an afternoon's walk, but they inhabit different climatic worlds. The sheep that graze both altitudes carry the gradient in their wool. The dyer who works with that wool must solve the gradient in her vat.

Kamala Devi's solution was what she called _the ladder_ — though she never called it anything, and the term is the editors'. She dyed in sequences that recapitulated the valley's altitude profile. A blanket for a family that moved between Tosh and the high pastures would be dyed in bands: walnut-brown at the bottom (the valley floor, the river-gorge colour), lichen-gold in the middle (the birch forest, the transition), and undyed cream at the top (the snow, the glacier, the _absence_ of colour that is itself the highest colour).

This was not decoration. It was _encoding_. The blanket was a map of the valley, readable by anyone who knew the colour-altitude correspondence. When a family laid the blanket on the ground in their summer camp, they oriented it with the brown edge pointing downvalley — toward home, toward warmth, toward the river. The cream edge pointed upslope. The blanket knew where it was.

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ============================================================
# The Gradient Blanket
# A blanket whose colour bands encode the valley's altitude profile
# Rendered as woven fabric — visible warp and weft
# ============================================================

PAPER = "#FEFCF5"
INK = "#2A2A2A"

fig, (ax_blanket, ax_valley) = plt.subplots(1, 2, figsize=(16, 10),
                                              gridspec_kw={"width_ratios": [2, 1],
                                                           "wspace": 0.05})
fig.patch.set_facecolor(PAPER)

# --- The altitude-colour mapping ---
bands = [
    (1700, 2000, "#C45824", "#D4A574", "Manikaran Red\nhot spring iron"),
    (2000, 2300, "#6B8E7B", "#4A7C6F", "Gorge Green\nriver-moss"),
    (2300, 2800, "#556B2F", "#8B7355", "Deodar\nforest floor"),
    (2800, 3200, "#8B6914", "#DAA520", "Lichen Gold\nbirch boulders"),
    (3200, 3500, "#C41E3A", "#E8C4A0", "Rhododendron\nspring bloom"),
    (3500, 4000, "#7B68EE", "#BDB76B", "Meadow\nalpine flowers"),
    (4000, 4500, "#708090", "#A0A0A0", "Scree\nbare rock"),
    (4500, 5319, "#E8F0FE", "#B0C4DE", "Snow\nglacier"),
]

# --- LEFT: The blanket as woven fabric ---
ax_blanket.set_facecolor(PAPER)
ax_blanket.set_xlim(0, 10)
ax_blanket.set_ylim(0, 16)
ax_blanket.set_aspect("auto")

np.random.seed(42)
blanket_left = 1.0
blanket_right = 9.0
blanket_bottom = 1.0
blanket_top = 15.0
blanket_height = blanket_top - blanket_bottom

n_bands = len(bands)
band_h = blanket_height / n_bands

for i, (lo_elev, hi_elev, warp_col, weft_col, label) in enumerate(bands):
    y_base = blanket_bottom + i * band_h

    # Woven texture: alternating warp and weft lines
    n_warp = 80
    n_weft = int(band_h * 20)

    # Warp threads (vertical)
    for j in range(n_warp):
        x = blanket_left + (blanket_right - blanket_left) * j / n_warp
        x += np.random.uniform(-0.02, 0.02)
        ax_blanket.plot([x, x], [y_base, y_base + band_h],
                       color=warp_col, linewidth=0.6,
                       alpha=np.random.uniform(0.3, 0.6))

    # Weft threads (horizontal)
    for k in range(n_weft):
        y = y_base + band_h * k / n_weft
        y += np.random.uniform(-0.01, 0.01)
        ax_blanket.plot([blanket_left, blanket_right], [y, y],
                       color=weft_col, linewidth=0.8,
                       alpha=np.random.uniform(0.3, 0.6))

    # Band label (left margin)
    ax_blanket.text(0.3, y_base + band_h / 2, label,
                   fontsize=6, fontfamily="serif", fontstyle="italic",
                   color="#6A6A6A", va="center", ha="center")

    # Subtle band boundary
    ax_blanket.axhline(y=y_base, color="#D4C4A4", linewidth=0.3, linestyle=":",
                      xmin=0.1, xmax=0.9)

# Fringe at bottom
for j in range(40):
    x = blanket_left + (blanket_right - blanket_left) * j / 40
    fringe_len = np.random.uniform(0.3, 0.7)
    ax_blanket.plot([x, x + np.random.uniform(-0.1, 0.1)],
                   [blanket_bottom, blanket_bottom - fringe_len],
                   color="#8B7355", linewidth=0.8, alpha=0.5)

# Fringe at top
for j in range(40):
    x = blanket_left + (blanket_right - blanket_left) * j / 40
    fringe_len = np.random.uniform(0.3, 0.7)
    ax_blanket.plot([x, x + np.random.uniform(-0.1, 0.1)],
                   [blanket_top, blanket_top + fringe_len],
                   color="#E8E0D8", linewidth=0.8, alpha=0.5)

# Orientation arrows
ax_blanket.annotate("↓ downvalley\n(toward Manikaran)", xy=(5.0, 0.1),
                   fontsize=7, ha="center", fontfamily="serif",
                   fontstyle="italic", color="#8B4513")
ax_blanket.annotate("↑ upslope\n(toward glacier)", xy=(5.0, 15.8),
                   fontsize=7, ha="center", fontfamily="serif",
                   fontstyle="italic", color="#708090")

ax_blanket.set_title("The Gradient Blanket", fontsize=14,
                    fontfamily="serif", fontweight="bold", color=INK, pad=20)

for spine in ax_blanket.spines.values():
    spine.set_visible(False)
ax_blanket.set_xticks([])
ax_blanket.set_yticks([])

# --- RIGHT: The valley profile (matching altitude) ---
ax_valley.set_facecolor(PAPER)
ax_valley.set_xlim(0, 5)
ax_valley.set_ylim(1700, 5319)

for lo_elev, hi_elev, warp_col, weft_col, label in bands:
    mid = (lo_elev + hi_elev) / 2
    ax_valley.fill_between([0, 3], lo_elev, hi_elev,
                           color=warp_col, alpha=0.3)
    ax_valley.axhline(y=lo_elev, color="#CCCCCC", linewidth=0.3, linestyle=":")
    ax_valley.text(3.2, mid, f"{lo_elev}–{hi_elev}m",
                  fontsize=6, fontfamily="serif", color="#6A6A6A", va="center")

# A simple mountain profile silhouette
profile_x = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
profile_y = np.array([1700, 2200, 3000, 3800, 4600, 5100, 5319])
ax_valley.plot(profile_x, profile_y, color="#4A4A4A", linewidth=1.5, alpha=0.5)
ax_valley.fill_betweenx(profile_y, 0, profile_x, color="#D4C4B4", alpha=0.2)

# River at the bottom
ax_valley.plot([0, 0.3], [1700, 1700], color="#2E6B5A", linewidth=3, alpha=0.5)
ax_valley.text(0.15, 1720, "Parvati\nRiver", fontsize=5, fontfamily="serif",
              fontstyle="italic", color="#2E6B5A", ha="center")

ax_valley.set_title("Valley Profile", fontsize=11,
                   fontfamily="serif", fontweight="bold", color=INK, pad=20)
ax_valley.set_ylabel("Elevation (m)", fontsize=8, fontfamily="serif")
ax_valley.yaxis.set_label_position("right")
ax_valley.yaxis.tick_right()
ax_valley.tick_params(axis="y", labelsize=6)
ax_valley.set_xticks([])

for spine in ["top", "bottom", "left"]:
    ax_valley.spines[spine].set_visible(False)
ax_valley.spines["right"].set_color("#AAAAAA")
ax_valley.spines["right"].set_linewidth(0.5)

# --- Connecting lines between blanket bands and valley altitudes ---
# (These would cross between subplots — we'll use fig.transFigure)
# Simpler: just add a note
fig.text(0.5, 0.02,
         "The blanket is a map. Brown edge downvalley. Cream edge toward the glacier. It knows where it is.",
         fontsize=8, ha="center", fontfamily="serif", fontstyle="italic", color="#6A6A6A")

fig.text(0.5, 0.005,
         "From the Kamala Devi archive — Tosh village, Parvati valley",
         fontsize=6, ha="center", fontfamily="serif", fontstyle="italic", color="#AAAAAA")

plt.savefig("gradient-blanket.png", dpi=200, bbox_inches="tight",
            facecolor=PAPER, edgecolor="none")
print("gradient-blanket.png")
```

{{< figure src="/ox-hugo/gradient-blanket.png" >}}


## V. The Conversation with Malana {#v-dot-the-conversation-with-malana}

Malana does not trade. This is not precisely true — Malana trades when it suits Malana, on terms that Malana sets, at the boundary stone where Malana's territory ends and the rest of the world begins. Outsiders do not enter. Outsiders do not touch. If an outsider's shadow falls on a Malanese house, the house must be purified. These rules are not negotiable and not recent. They may predate the valley's Hindu period. They almost certainly predate the roads.

Malana keeps goats. The Malana goat is not the Changthangi of Ladakh — no pashmina here — but a sturdy, dark-haired creature adapted to the steep-sided nala that leads to the village. The goat-hair is coarse, dark brown to black, and takes dye differently from sheep-wool. Where sheep-wool absorbs colour eagerly, goat-hair resists it, as if the animal's famous stubbornness persisted in its fibres after shearing. Kamala Devi said that dyeing Malana goat-hair was like _arguing with the mountain_.

She did not go to Malana. Malana came to her — or rather, Malana's goat-hair arrived, left at the boundary stone by intermediaries, with a knotted cord indicating quantity and a slate chip indicating desired colour. The colour requests were always the same: _dark_. Malana wanted its cloth to be dark the way its nala was dark — enclosed, private, absorbing light rather than reflecting it. The specific shade was left to the dyer's judgment, which Malana trusted absolutely while trusting the dyer herself not at all.

This is the paradox of Malana's isolationism: it produced a dependency on the very outside world it refused to touch. The goat-hair left the village as raw fibre and returned as dyed yarn, transformed by hands that could never enter the gates. The knowledge of colour lived outside; the knowledge of weaving lived inside. Between them, the boundary stone, and the knotted cord.

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

# ============================================================
# The Malana Exchange
# A boundary stone between two worlds:
# inside (weaving knowledge) / outside (colour knowledge)
# ============================================================

PAPER = "#FEFCF5"
INK = "#2A2A2A"

fig, ax = plt.subplots(figsize=(16, 8))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 16)
ax.set_ylim(0, 8)
ax.set_aspect("equal")

np.random.seed(99)

# --- THE BOUNDARY STONE (center) ---
stone_x = 8.0
stone_y = 4.0

# Stone: rough rectangle
stone_pts = np.array([
    [7.5, 2.5], [7.6, 2.3], [8.0, 2.2], [8.4, 2.3], [8.5, 2.5],
    [8.55, 3.5], [8.5, 4.5], [8.45, 5.2], [8.3, 5.5], [8.0, 5.6],
    [7.7, 5.5], [7.55, 5.2], [7.5, 4.5], [7.45, 3.5], [7.5, 2.5]
])
ax.fill(stone_pts[:, 0], stone_pts[:, 1], color="#808080", alpha=0.6,
        edgecolor="#4A4A4A", linewidth=2)

# Texture: small cracks
for _ in range(15):
    cx = stone_x + np.random.normal(0, 0.3)
    cy = stone_y + np.random.normal(0, 1.0)
    cl = np.random.uniform(0.1, 0.3)
    ca = np.random.uniform(0, np.pi)
    ax.plot([cx, cx + cl * np.cos(ca)], [cy, cy + cl * np.sin(ca)],
            color="#5A5A5A", linewidth=0.5, alpha=0.5)

ax.text(stone_x, 1.8, "BOUNDARY\nSTONE", fontsize=8, ha="center",
        fontfamily="serif", fontweight="bold", color="#4A4A4A")

# --- LEFT SIDE: Malana (inside) — dark, enclosed ---
# Dark background wash
for _ in range(200):
    x = np.random.uniform(0, 7.0)
    y = np.random.uniform(0.5, 7.5)
    ax.plot(x, y, ".", color="#2A2A2A", markersize=np.random.uniform(1, 4),
            alpha=np.random.uniform(0.03, 0.08))

# Goat-hair fibres (dark, coarse)
for _ in range(80):
    fx = np.random.uniform(1.5, 3.5)
    fy = np.random.uniform(3.0, 5.5)
    fl = np.random.uniform(0.4, 0.8)
    fa = np.random.uniform(-0.3, 0.3)
    shade = np.random.choice(["#3A2A1A", "#4A3A2A", "#2A1A0A", "#5A4A3A"])
    ax.plot([fx, fx + fl * np.cos(fa)], [fy, fy + fl * np.sin(fa)],
            color=shade, linewidth=np.random.uniform(1.0, 2.5),
            alpha=np.random.uniform(0.4, 0.7), solid_capstyle="round")

ax.text(2.5, 6.5, "MALANA", fontsize=14, fontfamily="serif",
        fontweight="bold", color="#3A3A3A", ha="center")
ax.text(2.5, 6.0, "weaving knowledge\nboundary law\nthe goat's stubbornness",
        fontsize=7, fontfamily="serif", fontstyle="italic",
        color="#5A5A5A", ha="center")

# Knotted cord (going toward boundary)
cord_x = np.linspace(3.5, 7.2, 50)
cord_y = 2.8 + 0.15 * np.sin(8 * cord_x) + 0.1 * np.random.randn(50)
ax.plot(cord_x, cord_y, color="#5A4A3A", linewidth=2, alpha=0.7)
# Knots
for kx in [4.2, 4.8, 5.5, 6.2, 6.8]:
    ax.plot(kx, 2.8 + 0.15 * np.sin(8 * kx), "o",
            color="#3A2A1A", markersize=5, alpha=0.8)
ax.text(5.5, 2.2, "knotted cord\n(quantity + colour request)",
        fontsize=6, fontfamily="serif", fontstyle="italic",
        color="#5A4A3A", ha="center")

# Slate chip
slate = FancyBboxPatch((6.0, 3.5), 0.8, 0.5,
                         boxstyle="round,pad=0.02",
                         facecolor="#606060", edgecolor="#404040",
                         linewidth=1, alpha=0.8)
ax.add_patch(slate)
ax.text(6.4, 3.75, "dark", fontsize=5, ha="center", va="center",
        color="#D0D0D0", fontfamily="serif")
ax.text(6.4, 3.2, "slate chip\n(always the same request)",
        fontsize=5, fontfamily="serif", fontstyle="italic",
        color="#6A6A6A", ha="center")

# --- RIGHT SIDE: Tosh / the dyer (outside) — warm, colourful ---
# Colour swatches floating
palette_colours = ["#C45824", "#DAA520", "#2A3A78", "#8B7355", "#3A3838",
                   "#C41E3A", "#4A7C6F", "#7B68EE"]
for _ in range(60):
    x = np.random.uniform(9.5, 14.0)
    y = np.random.uniform(2.5, 6.0)
    c = np.random.choice(palette_colours)
    size = np.random.uniform(0.08, 0.25)
    circle = Circle((x, y), size, color=c,
                    alpha=np.random.uniform(0.15, 0.4))
    ax.add_patch(circle)

# Dyed yarn returning (warm colours flowing back toward boundary)
for _ in range(40):
    fx = np.random.uniform(8.8, 10.5)
    fy = np.random.uniform(4.0, 5.5)
    fl = np.random.uniform(0.5, 1.0)
    fa = np.random.uniform(2.5, 3.5)  # pointing left, toward boundary
    shade = np.random.choice(["#2A2A2A", "#1A1A1A", "#3A2A2A", "#2A1A2A"])
    ax.plot([fx, fx + fl * np.cos(fa)], [fy, fy + fl * np.sin(fa)],
            color=shade, linewidth=np.random.uniform(1.2, 2.5),
            alpha=np.random.uniform(0.4, 0.7), solid_capstyle="round")

ax.text(12.0, 6.5, "TOSH", fontsize=14, fontfamily="serif",
        fontweight="bold", color="#8B4513", ha="center")
ax.text(12.0, 6.0, "colour knowledge\nthe dyer's hands\nfive pigments, five altitudes",
        fontsize=7, fontfamily="serif", fontstyle="italic",
        color="#8B6540", ha="center")

# Return arrow
ax.annotate("", xy=(8.8, 4.8), xytext=(10.0, 4.8),
            arrowprops=dict(arrowstyle="->", color="#3A2A2A", lw=2))
ax.text(9.4, 5.15, "dyed yarn returns\n(dark, always dark)",
        fontsize=6, fontfamily="serif", fontstyle="italic",
        color="#4A3A2A", ha="center")

# --- The paradox text ---
ax.text(8.0, 7.5,
        "The paradox: dependency on the world it refuses to touch",
        fontsize=10, ha="center", fontfamily="serif", fontstyle="italic",
        color="#5A5A5A")

ax.text(8.0, 0.3,
        "Knowledge of colour outside the walls. Knowledge of weaving inside. Between them: stone, cord, silence.",
        fontsize=7, ha="center", fontfamily="serif", fontstyle="italic",
        color="#999999")

for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

plt.savefig("malana-exchange.png", dpi=200, bbox_inches="tight",
            facecolor=PAPER, edgecolor="none")
print("malana-exchange.png")
```

{{< figure src="/ox-hugo/malana-exchange.png" >}}


## VI. The Colour That Has No Name {#vi-dot-the-colour-that-has-no-name}

There was one colour that Kamala Devi made that did not come from the valley. Or rather — it came from the valley in a way that the other colours did not. The five pigments — iron, lichen, indigo, walnut, slate — were extractive. You went to the source, you took the material, you processed it. The sixth colour was _emergent_. It appeared only when certain other colours were combined in a specific sequence, on a specific fibre, at a specific temperature, and it could not be produced directly.

She discovered it by accident — or the valley discovered it through her. A batch of lichen-gold yarn, improperly rinsed, was over-dyed with indigo. The expected result was green. What appeared instead was a colour that witnesses describe variously as _the inside of a mussel shell_, _moonlight on wet slate_, _the moment before the monsoon breaks_. It had depth. It shifted. In direct light it appeared silver-green; in shade it turned toward violet; at twilight it seemed to contain its own faint luminescence.

She spent years trying to reproduce it reliably. The key, she eventually determined, was not in the pigments themselves but in their _interaction with the mordant residue_ left from the first dyeing. The alum crystals, incompletely rinsed, created nucleation sites where the indigo molecules arranged themselves in a pattern different from their usual disordered deposition. The result was a structural colour — not pigment-colour but _interference-colour_, like a butterfly wing or an oil film on water. The dye molecules, ordered by the residual mordant geometry, split light instead of merely absorbing it.

She never named it. The other dyers in the valley called it _Kamala's accident_. The shepherds, who saw it in the blankets, called it _the colour the mountain keeps for itself_. In the notation found in her storehouse — a grid of symbols that may represent recipes — the sixth colour is indicated by an empty square.

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ============================================================
# The Colour That Has No Name
# An interference colour — shifting, iridescent, impossible to pin
# Rendered as overlapping translucent fields that change with viewing angle
# ============================================================

PAPER = "#FEFCF5"

fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor("#1A1A2A")  # Dark ground — twilight
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.set_aspect("equal")

np.random.seed(2024)

# The unnamed colour lives in the overlap of two colour fields:
# lichen-gold → indigo, but the interference creates something else

# Layer 1: The lichen gold base (improperly rinsed)
n_points = 2000
x1 = np.random.normal(7.0, 3.0, n_points)
y1 = np.random.normal(5.0, 2.5, n_points)

for i in range(n_points):
    # Gold with variation
    r = int(0xDA + np.random.randint(-20, 20))
    g = int(0xA5 + np.random.randint(-30, 20))
    b = int(0x20 + np.random.randint(-10, 30))
    r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
    colour = f"#{r:02x}{g:02x}{b:02x}"
    ax.plot(x1[i], y1[i], ".", color=colour,
            markersize=np.random.uniform(2, 8),
            alpha=np.random.uniform(0.02, 0.08))

# Layer 2: The indigo overdye
for i in range(n_points):
    x = np.random.normal(7.0, 2.8)
    y = np.random.normal(5.0, 2.3)
    r = int(0x2A + np.random.randint(-10, 30))
    g = int(0x3A + np.random.randint(-10, 30))
    b = int(0x78 + np.random.randint(-20, 40))
    r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
    colour = f"#{r:02x}{g:02x}{b:02x}"
    ax.plot(x, y, ".", color=colour,
            markersize=np.random.uniform(2, 8),
            alpha=np.random.uniform(0.02, 0.08))

# Layer 3: The interference — the unnamed colour emerges in the overlap
# Silver-green / violet / luminescent shifts
interference_colours = [
    (0.70, 0.78, 0.72),  # silver-green
    (0.60, 0.55, 0.75),  # violet shift
    (0.75, 0.80, 0.82),  # moonlight
    (0.65, 0.72, 0.68),  # wet slate
    (0.80, 0.75, 0.85),  # pre-monsoon
    (0.55, 0.70, 0.65),  # mussel shell interior
]

for i in range(3000):
    x = np.random.normal(7.0, 2.0)
    y = np.random.normal(5.0, 1.8)
    # Distance from center affects which interference colour dominates
    dist = np.sqrt((x - 7.0)**2 + (y - 5.0)**2)
    angle = np.arctan2(y - 5.0, x - 7.0)

    # Colour shifts with angle (like iridescence)
    idx = int((angle + np.pi) / (2 * np.pi) * len(interference_colours)) % len(interference_colours)
    base_r, base_g, base_b = interference_colours[idx]

    # Add noise
    r = max(0, min(1, base_r + np.random.normal(0, 0.05)))
    g = max(0, min(1, base_g + np.random.normal(0, 0.05)))
    b = max(0, min(1, base_b + np.random.normal(0, 0.05)))

    # Alpha decreases with distance — the colour fades at the edges
    alpha = max(0.01, min(0.15, 0.15 - dist * 0.03))

    ax.plot(x, y, ".", color=(r, g, b),
            markersize=np.random.uniform(3, 12),
            alpha=alpha)

# A faint luminous core
for i in range(500):
    x = np.random.normal(7.0, 0.8)
    y = np.random.normal(5.0, 0.6)
    ax.plot(x, y, ".", color="#C8D8D0",
            markersize=np.random.uniform(1, 4),
            alpha=np.random.uniform(0.05, 0.15))

# The empty square — Kamala Devi's notation for this colour
square_size = 0.4
sq = plt.Rectangle((6.8, 0.8), square_size, square_size,
                     fill=False, edgecolor="#808080", linewidth=1.5, alpha=0.6)
ax.add_patch(sq)
ax.text(7.0 + square_size + 0.2, 1.0,
        "□  — the notation for the sixth colour",
        fontsize=7, fontfamily="serif", fontstyle="italic",
        color="#808080", va="center")

# Title
ax.text(7.0, 9.6, "The Colour That Has No Name",
        fontsize=16, fontfamily="serif", fontweight="bold",
        ha="center", color="#C8D8D0")
ax.text(7.0, 9.1,
        "\"the inside of a mussel shell — moonlight on wet slate — the moment before the monsoon breaks\"",
        fontsize=8, fontfamily="serif", fontstyle="italic",
        ha="center", color="#8898A0")

# Witness descriptions around the edges
descriptions = [
    (1.5, 7.5, "silver-green\nin direct light"),
    (12.5, 7.5, "violet\nin shade"),
    (1.5, 2.5, "faintly luminescent\nat twilight"),
    (12.5, 2.5, "the colour the mountain\nkeeps for itself"),
]
for dx, dy, text in descriptions:
    ax.text(dx, dy, text, fontsize=7, fontfamily="serif", fontstyle="italic",
            color="#6A7A7A", ha="center", alpha=0.7)

ax.text(7.0, 0.2,
        "Not pigment-colour but interference-colour — the dye molecules, ordered by residual mordant, split light",
        fontsize=6, ha="center", fontfamily="serif", fontstyle="italic",
        color="#5A6A6A")

for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

plt.savefig("unnamed-colour.png", dpi=200, bbox_inches="tight",
            facecolor="#1A1A2A", edgecolor="none")
print("unnamed-colour.png")
```

{{< figure src="/ox-hugo/unnamed-colour.png" >}}


## VII. What the Valley Keeps {#vii-dot-what-the-valley-keeps}

After Kamala Devi, the dye-house stood empty for eleven years. The vats rusted. The hearth went cold for the first time in living memory. The lichen grew back over the boulders she had harvested. The indigo bushes, no longer cut back, spread along the trail until the trail itself narrowed.

Her apprentices had learned the five colours but not the sixth. They had learned the recipes but not the reading — the hand-in-the-fleece, the nose-to-the-lanolin, the sixty-year database indexed by touch. These things cannot be transmitted by instruction. They can only be grown, slowly, in the body of someone who stays.

No one stayed. Kasol, twenty minutes downhill, had hotels that needed staff. The road had come. The tourists had come. The synthetic dyes had come — bright, cheap, identical in every batch, requiring no pilgrimage up the valley flanks, no negotiation with lichen or slate. A sweater dyed in Ludhiana cost less than the mordant alone for a single Tosh dyeing. The economics were unanswerable.

And yet.

The gradient blankets that Kamala Devi made are still used by families in Tosh. They are old now — thirty, forty years — and the colours have shifted with washing and sun. The Manikaran Red has mellowed to a warm sienna. The lichen-gold has faded to straw. The indigo, characteristically, has barely changed; it is the most lightfast of natural dyes, the most stubborn, the most loyal to its first commitment. The slate-black has softened to charcoal.

And the sixth colour? On the few pieces where it appears — perhaps half a dozen blankets, total — it has not faded at all. The structural colour, being a property of molecular arrangement rather than pigment concentration, does not bleach. It will outlast the cloth itself. When the wool finally disintegrates, the pattern of light-splitting will persist in whatever fragments remain, like a fossil of colour, like the valley's own memory pressed into fibre, waiting to be read by hands that know what they are touching.

The dye-house in Tosh can be found by anyone who climbs above the village and looks for a building with a chimney that has not smoked in eleven years. The iron vats are still inside. The stone mortar sits by the door. The shelves hold jars of pigment that Kamala Devi ground and never used — iron oxide the colour of the first light on Deo Tibba, indigo the colour of the gorge in shadow, lichen the colour of patience.

The valley keeps its colours. It simply waits for someone to come and read them again.

_--- From the archive. Editors' reconstruction, with apologies for the words._

```python
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# What the Valley Keeps
# The faded gradient blanket — colours shifted by decades of sun
# overlaid with the valley's enduring palette
# ============================================================

PAPER = "#FEFCF5"

fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.set_aspect("equal")

np.random.seed(77)

# The aged blanket — faded colours, worn texture
# Original colours → faded versions
faded_bands = [
    ("#D4A080", "#E8C8B0"),  # Manikaran Red → warm sienna
    ("#90A890", "#A8B8A0"),  # Gorge Green → sage
    ("#7A8A60", "#A0A888"),  # Deodar → muted olive
    ("#D4C888", "#E8DCC0"),  # Lichen Gold → straw
    ("#C8A8A0", "#D8C0B8"),  # Rhododendron → faded rose
    ("#A0A0B8", "#C0C0C8"),  # Meadow → grey-lavender
    ("#989898", "#B0B0B0"),  # Scree → light grey
    ("#E0E0E0", "#F0F0F0"),  # Snow → near-white
]

# Draw the blanket as a worn, slightly rumpled rectangle
blanket_left = 2.0
blanket_right = 12.0
blanket_bottom = 1.0
blanket_top = 9.0
band_h = (blanket_top - blanket_bottom) / len(faded_bands)

for i, (warp_col, weft_col) in enumerate(faded_bands):
    y_base = blanket_bottom + i * band_h

    # Worn warp threads — many broken or thin
    for j in range(100):
        x = blanket_left + (blanket_right - blanket_left) * j / 100
        x += np.random.uniform(-0.03, 0.03)
        # Some threads are broken (gaps)
        if np.random.random() < 0.15:
            continue
        y_start = y_base + np.random.uniform(0, band_h * 0.1)
        y_end = y_base + band_h - np.random.uniform(0, band_h * 0.1)
        ax.plot([x, x], [y_start, y_end],
               color=warp_col, linewidth=np.random.uniform(0.3, 0.8),
               alpha=np.random.uniform(0.2, 0.5))

    # Worn weft threads
    for k in range(int(band_h * 15)):
        y = y_base + band_h * k / (band_h * 15)
        if np.random.random() < 0.1:
            continue
        ax.plot([blanket_left, blanket_right], [y, y + np.random.uniform(-0.02, 0.02)],
               color=weft_col, linewidth=np.random.uniform(0.3, 0.7),
               alpha=np.random.uniform(0.15, 0.4))

# The sixth colour — unfaded, luminous, persisting
# A small patch in the upper-middle area
sixth_x, sixth_y = 7.0, 6.5
for _ in range(300):
    x = sixth_x + np.random.normal(0, 0.6)
    y = sixth_y + np.random.normal(0, 0.4)
    angle = np.arctan2(y - sixth_y, x - sixth_x)
    idx = int((angle + np.pi) / (2 * np.pi) * 6) % 6
    interference = [
        (0.70, 0.78, 0.72),
        (0.60, 0.55, 0.75),
        (0.75, 0.80, 0.82),
        (0.65, 0.72, 0.68),
        (0.80, 0.75, 0.85),
        (0.55, 0.70, 0.65),
    ][idx]
    r = max(0, min(1, interference[0] + np.random.normal(0, 0.03)))
    g = max(0, min(1, interference[1] + np.random.normal(0, 0.03)))
    b = max(0, min(1, interference[2] + np.random.normal(0, 0.03)))
    ax.plot(x, y, ".", color=(r, g, b),
            markersize=np.random.uniform(2, 6),
            alpha=np.random.uniform(0.1, 0.35))

# Annotation for the sixth colour
ax.annotate("the sixth colour\n— unfaded —",
           xy=(seventh_x := 7.0, 6.5), xytext=(11.5, 8.5),
           fontsize=7, fontfamily="serif", fontstyle="italic",
           color="#6A7A7A",
           arrowprops=dict(arrowstyle="->", color="#8898A0",
                          connectionstyle="arc3,rad=0.2", lw=0.8))

# Age annotations along the right edge
age_notes = [
    (blanket_bottom + 0.5 * band_h, "Red → sienna\n(30 years' sun)"),
    (blanket_bottom + 3.5 * band_h, "Gold → straw\n(lichen fades)"),
    (blanket_bottom + 2.5 * band_h, "Indigo holds\n(stubborn, loyal)"),
    (blanket_bottom + 7.5 * band_h, "Cream → white\n(time's bleach)"),
]
for y, note in age_notes:
    ax.text(12.5, y, note, fontsize=6, fontfamily="serif",
            fontstyle="italic", color="#8A8A8A", va="center")

# Title
ax.text(7.0, 9.8, "What the Valley Keeps",
        fontsize=16, fontfamily="serif", fontweight="bold",
        ha="center", color=INK)
ax.text(7.0, 9.4,
        "A gradient blanket after thirty years — all colours faded except the one that has no name",
        fontsize=8, fontfamily="serif", fontstyle="italic",
        ha="center", color="#6A6A6A")

ax.text(7.0, 0.3,
        "The structural colour does not bleach. It will outlast the cloth itself.",
        fontsize=7, ha="center", fontfamily="serif", fontstyle="italic",
        color="#999999")

INK = "#2A2A2A"

for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

plt.savefig("valley-keeps.png", dpi=200, bbox_inches="tight",
            facecolor=PAPER, edgecolor="none")
print("valley-keeps.png")
```

{{< figure src="/ox-hugo/valley-keeps.png" >}}


## Colophon {#colophon}

This tale was composed in the manner of the Thread Walkers' archive — a collaboration between human intuition and machine traversal, neither subordinate. The illustrations were generated computationally from the valley's own data: its geology, its ecology, its altitude profile. No photographs were used. The colours are as accurate as reconstruction permits.

Kamala Devi is a fiction. The valley is not. The dye chemistry is real. The Gaddi shepherds still move their flocks through these passes, though their numbers diminish each year. The lichen still grows on the birch-forest boulders above Pulga. The hot springs at Manikaran still deposit iron oxide on the rocks. The indigo still colonises disturbed ground.

The dye-house may or may not exist. We did not check. Some things are better left as questions.

_mu2tau + Claude_
_Parvati valley, February 2026_
