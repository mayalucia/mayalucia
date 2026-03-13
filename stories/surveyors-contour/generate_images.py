# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib>=3.9", "numpy>=1.26", "scipy>=1.12"]
# ///
"""
The Surveyor's Contour — 6 illustrated figures
Setting: Thalpan petroglyph terrace, Indus gorge, Diamer

Story #21. The figures use real SRTM elevation data from Experiment 03.
The core argument: measurement beats imagination. The DEM's own geometry
produces the gorge more truly than any painted surface.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.ndimage import gaussian_filter

SLUG = "the-surveyors-contour"
OUT = (Path(__file__).parent / f"../../website/static/images/writing/{SLUG}").resolve()
OUT.mkdir(parents=True, exist_ok=True)

DEM_PATH = (Path(__file__).parent / "../../experiments/03-procedural-realism/output/transects.npz").resolve()

DPI = 150
W, H = 12, 9  # standard story figure size → 1800×1350 px

# ── Palette ──────────────────────────────────────────────────────────
SLATE = "#3A3A38"
SLATE_DARK = "#2A2A28"
CHALK = "#E8E4D8"
CHALK_DIM = "#9A9890"
PARCHMENT = "#F5F0E8"
PARCHMENT_DARK = "#EDE6D8"
INK = "#5C4A3A"
INK_LIGHT = "#8A7A6A"
WATER = "#4A8B6B"
COPPER = "#C4886B"
MOUNTAIN = "#7A7068"
MOUNTAIN_DARK = "#5A5248"
SNOW_WHITE = "#E8EEF0"


def make_fig(width=W, height=H, bg=SLATE):
    fig, ax = plt.subplots(1, 1, figsize=(width, height))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    return fig, ax


def make_fig_3d(width=W, height=H, bg=SLATE):
    fig = plt.figure(figsize=(width, height))
    fig.patch.set_facecolor(bg)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(bg)
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=DPI, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  ✓ {name}.png")


def attribution(ax, y=-0.06):
    ax.text(0.5, y, "SRTM 3″ · Thalpan, 35.62°N 74.60°E",
            transform=ax.transAxes, ha="center", fontsize=8,
            color=CHALK_DIM, style="italic", family="serif")


def load_dem():
    data = np.load(DEM_PATH)
    return {
        "d_ene": data["d_ene"],
        "e_ene": data["e_ene"],
        "d_ns": data["d_ns"],
        "e_ns": data["e_ns"],
        "dem_patch": data["dem_patch"],
        "lat": float(data["lat"]),
        "lon": float(data["lon"]),
    }


# ── Figure 1: The Asymmetry ─────────────────────────────────────────
# The SRTM cross-section — ENE→WSW transect. Chalk on slate.
# The profile that shows the wound.

def fig1_asymmetry(dem):
    fig, ax = make_fig(bg=SLATE_DARK)
    d = dem["d_ene"]
    e = dem["e_ene"]

    # Fill below the profile
    ax.fill_between(d, 1000, e, color=MOUNTAIN_DARK, alpha=0.6)
    ax.fill_between(d, 1000, e, color=SLATE, alpha=0.3)

    # The profile line itself — chalk
    ax.plot(d, e, color=CHALK, lw=2.0, solid_capstyle="round")

    # River marker
    river_idx = np.argmin(e)
    ax.plot(d[river_idx], e[river_idx], 'o', color=WATER, ms=6, zorder=5)
    ax.annotate("Indus\n1213 m", (d[river_idx], e[river_idx]),
                textcoords="offset points", xytext=(12, -20),
                fontsize=10, color=WATER, family="serif", style="italic")

    # Peak annotation
    peak_idx = np.argmax(e)
    ax.annotate("4230 m", (d[peak_idx], e[peak_idx]),
                textcoords="offset points", xytext=(-30, 10),
                fontsize=10, color=CHALK_DIM, family="serif", style="italic")

    # WSW annotation
    wsw_idx = -1
    ax.annotate("1800 m", (d[wsw_idx], e[wsw_idx]),
                textcoords="offset points", xytext=(-10, 10),
                fontsize=10, color=CHALK_DIM, family="serif", style="italic")

    # Axis labels
    ax.set_xlabel("Distance along transect (km)", fontsize=11,
                  color=CHALK_DIM, family="serif", labelpad=10)
    ax.set_ylabel("Elevation (m)", fontsize=11,
                  color=CHALK_DIM, family="serif", labelpad=10)

    # Direction labels
    ax.text(d[0], 1050, "ENE", fontsize=11, color=CHALK_DIM,
            family="serif", ha="center", style="italic")
    ax.text(d[-1], 1050, "WSW", fontsize=11, color=CHALK_DIM,
            family="serif", ha="center", style="italic")

    # Styling
    ax.set_ylim(1000, 4500)
    ax.tick_params(colors=CHALK_DIM, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(CHALK_DIM)
        spine.set_linewidth(0.5)
    ax.grid(True, color=CHALK_DIM, alpha=0.1, lw=0.5)

    attribution(ax)
    save(fig, "fig1-asymmetry")


# ── Figure 2: The Platonic Gorge ────────────────────────────────────
# A symmetrical gorge silhouette — warm, golden, deliberately wrong.
# "The average of ten thousand gorges is not a gorge."

def fig2_platonic_gorge(dem):
    fig, ax = make_fig(bg=PARCHMENT)

    rng = np.random.default_rng(42)
    x = np.linspace(0, 100, 300)

    # Deliberately symmetrical V-gorge
    center = 50
    # Left wall rises smoothly
    left_wall = 20 + 55 * np.exp(-((x - center) ** 2) / 800)
    # Mirror for right wall — same shape, same height
    right_wall = left_wall.copy()
    # Add gentle noise for "painted" feel
    noise = gaussian_filter(rng.normal(0, 1.5, 300), sigma=8)
    left_wall += noise
    right_wall += gaussian_filter(rng.normal(0, 1.5, 300), sigma=8)

    # Golden warm palette
    ax.fill_between(x, 0, left_wall, color="#D4A055", alpha=0.5)
    ax.fill_between(x, 0, right_wall, color="#C89040", alpha=0.3)
    ax.plot(x, left_wall, color=INK_LIGHT, lw=1.5, alpha=0.7)

    # Gentle "river" at the bottom — centred, tidy
    river_y = 20 + 2 * np.sin(x * 0.1)
    ax.fill_between(x, river_y - 2, river_y + 2,
                    where=(np.abs(x - center) < 12),
                    color="#7AB0C0", alpha=0.5)

    # "Snow" on peaks — both sides equal
    snow_mask = left_wall > 60
    ax.fill_between(x, left_wall - 3, left_wall,
                    where=snow_mask, color="white", alpha=0.4)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 85)
    ax.axis("off")

    # Caption
    ax.text(50, 3, "The Platonic gorge — competent and false",
            ha="center", fontsize=11, color=INK, family="serif",
            style="italic")

    save(fig, "fig2-platonic-gorge")


# ── Figure 3: The Survey Becoming Shape ─────────────────────────────
# Data points resolving into the profile — numbers becoming a line.

def fig3_survey_to_shape(dem):
    fig, ax = make_fig(bg=SLATE_DARK)
    d = dem["d_ene"]
    e = dem["e_ene"]

    # Show measurement points as dots (every Nth for legibility)
    step = 2
    ax.scatter(d[::step], e[::step], color=COPPER, s=14, alpha=0.6,
               zorder=3, edgecolors="none")

    # Vertical drop lines from each point — the "measurement"
    for i in range(0, len(d), step):
        ax.plot([d[i], d[i]], [1000, e[i]], color=CHALK_DIM,
                lw=0.3, alpha=0.15)

    # The profile line emerging from the points
    ax.plot(d, e, color=CHALK, lw=2.5, solid_capstyle="round", zorder=4)

    # River
    river_idx = np.argmin(e)
    ax.plot(d[river_idx], e[river_idx], 'o', color=WATER, ms=6, zorder=5)

    # "90 m" bracket showing the measurement interval
    bracket_i = len(d) // 3
    if bracket_i + 1 < len(d):
        dx = abs(d[bracket_i + 1] - d[bracket_i])
        mid_x = (d[bracket_i] + d[bracket_i + 1]) / 2
        ax.annotate("", xy=(d[bracket_i], 1100), xytext=(d[bracket_i + 1], 1100),
                    arrowprops=dict(arrowstyle="<->", color=COPPER, lw=1.0))
        ax.text(mid_x, 1130, "~90 m", fontsize=8, color=COPPER,
                family="serif", ha="center", style="italic")

    ax.set_ylim(1000, 4500)
    ax.set_xlabel("Distance (km)", fontsize=11,
                  color=CHALK_DIM, family="serif", labelpad=10)
    ax.set_ylabel("Elevation (m)", fontsize=11,
                  color=CHALK_DIM, family="serif", labelpad=10)
    ax.tick_params(colors=CHALK_DIM, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(CHALK_DIM)
        spine.set_linewidth(0.5)

    attribution(ax)
    save(fig, "fig3-survey-to-shape")


# ── Figure 4: The 3D Projection ─────────────────────────────────────
# DEM projected from the terrace viewpoint. Shadow-only.
# The mountain's own body tells you where the light falls.

def fig4_projection(dem):
    patch = dem["dem_patch"]       # 88 × 134, elevation in metres
    ny, nx = patch.shape           # rows=N-S, cols=E-W

    # Build coordinate grids (km, origin at centre)
    x_km = np.linspace(-nx * 0.09 / 2, nx * 0.09 / 2, nx)  # E-W
    y_km = np.linspace(-ny * 0.09 / 2, ny * 0.09 / 2, ny)  # N-S
    X, Y = np.meshgrid(x_km, y_km)

    # Scale elevation for visual impact (keep proportional)
    Z = patch / 1000.0  # km

    # Hillshade: sun from ENE, low elevation (dawn)
    ls = LightSource(azdeg=60, altdeg=15)
    shade = ls.hillshade(patch, vert_exag=1.5, dx=90, dy=90)

    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor(SLATE_DARK)
    ax = fig.add_subplot(111, projection='3d',
                         computed_zorder=False)
    ax.set_facecolor(SLATE_DARK)

    # Map shade to a monochrome colourmap: dark shadow → chalk highlight
    # Custom colourmap: deep slate → warm chalk
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "gorge_shadow",
        [(0.08, 0.08, 0.07),    # deep shadow
         (0.25, 0.22, 0.20),    # dark rock
         (0.55, 0.48, 0.40),    # mid-tone
         (0.85, 0.80, 0.72)],   # lit chalk
    )

    ax.plot_surface(X, Y, Z,
                    facecolors=cmap(shade),
                    rstride=1, cstride=1,
                    antialiased=True,
                    shade=False)

    # Viewpoint: from the WSW terrace, looking ENE toward the steep wall
    ax.view_init(elev=12, azim=-55)

    # Remove axes clutter
    ax.set_axis_off()

    # Tighten
    ax.set_box_aspect([nx/ny, 1, 0.5])

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0.05)
    ax.text2D(0.5, 0.02, "SRTM 3″ · view from Thalpan terrace, looking ENE",
              transform=fig.transFigure, ha="center", fontsize=8,
              color=CHALK_DIM, style="italic", family="serif")

    save(fig, "fig4-projection")


# ── Figure 5: The Slope Field ───────────────────────────────────────
# The 2D DEM patch as hillshade — gullies and spurs emerge.
# "A field of heights, like a woven cloth."

def fig5_slope_field(dem):
    patch = dem["dem_patch"]

    # Hillshade from dawn direction (ENE)
    ls = LightSource(azdeg=60, altdeg=20)
    shade = ls.hillshade(patch, vert_exag=2.0, dx=90, dy=90)

    # Slope magnitude
    dy, dx = np.gradient(patch, 90, 90)  # gradient in metres per 90m
    slope = np.sqrt(dx**2 + dy**2)
    slope_norm = slope / slope.max()

    fig, ax = make_fig(bg=SLATE_DARK)

    # Composite: hillshade for shape, slope for intensity
    composite = shade * 0.7 + slope_norm * 0.3

    cmap = mcolors.LinearSegmentedColormap.from_list(
        "slope_chalk",
        [(0.08, 0.08, 0.07),
         (0.20, 0.19, 0.18),
         (0.45, 0.40, 0.35),
         (0.75, 0.70, 0.62),
         (0.91, 0.89, 0.85)],
    )

    extent = [-6.0, 6.0, -4.0, 4.0]  # approximate km
    ax.imshow(composite, cmap=cmap, extent=extent,
              origin="lower", aspect="auto")

    ax.set_xlabel("E ← → W  (km)", fontsize=10,
                  color=CHALK_DIM, family="serif", labelpad=8)
    ax.set_ylabel("S ← → N  (km)", fontsize=10,
                  color=CHALK_DIM, family="serif", labelpad=8)
    ax.tick_params(colors=CHALK_DIM, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(CHALK_DIM)
        spine.set_linewidth(0.5)

    # Mark the river — find the valley floor as the smoothed min-elevation band
    # The Indus runs roughly N-S through the patch, so find min per row
    river_cols = np.argmin(patch, axis=1)
    river_xs_raw = extent[0] + (river_cols / patch.shape[1]) * (extent[1] - extent[0])
    river_ys_raw = np.linspace(extent[2], extent[3], patch.shape[0])
    # Smooth to avoid column-hopping noise
    river_xs_smooth = gaussian_filter(river_xs_raw, sigma=3)
    ax.plot(river_xs_smooth, river_ys_raw, color=WATER, lw=1.5, alpha=0.7,
            solid_capstyle="round")
    mid = len(river_ys_raw) // 2
    ax.text(river_xs_smooth[mid] + 0.4, river_ys_raw[mid], "Indus",
            fontsize=9, color=WATER, family="serif", style="italic")

    attribution(ax, y=-0.08)
    save(fig, "fig5-slope-field")


# ── Figure 6: Hachure vs Contour ────────────────────────────────────
# Split panel — left: hand-drawn hachure strokes (parchment),
# right: contour lines from the same DEM (slate).

def fig6_hachure_vs_contour(dem):
    patch = dem["dem_patch"]
    ny, nx = patch.shape

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(W, H))
    fig.patch.set_facecolor(SLATE)

    # ── Left panel: Hachures (parchment) ────────────────────────────
    ax_left.set_facecolor(PARCHMENT)

    # Compute gradient for hachure direction
    dy, dx = np.gradient(patch, 90, 90)
    slope = np.sqrt(dx**2 + dy**2)
    slope_norm = slope / slope.max()

    # Hachure strokes: short lines in the direction of steepest descent
    rng = np.random.default_rng(42)
    # Dense pass for steep areas, sparser for gentle
    for iy in range(0, ny):
        for ix in range(0, nx):
            s = slope_norm[iy, ix]
            if s < 0.08:  # skip near-flat
                continue
            # Probabilistic thinning for gentler slopes
            if s < 0.3 and rng.random() > s * 3:
                continue
            # Length proportional to slope
            length = s * 2.5 + 0.4
            # Direction of steepest descent
            angle = np.arctan2(-dy[iy, ix], dx[iy, ix])
            # Wobble for hand-drawn feel
            angle += rng.normal(0, 0.12)
            length *= rng.uniform(0.7, 1.3)

            x0, y0 = ix, iy
            x1 = x0 + length * np.cos(angle)
            y1 = y0 + length * np.sin(angle)

            # Thickness proportional to slope (steeper = much thicker)
            lw = 0.3 + s * 2.5
            ax_left.plot([x0, x1], [y0, y1], color=INK,
                         lw=lw, alpha=0.35 + s * 0.5, solid_capstyle="round")

    ax_left.set_xlim(0, nx)
    ax_left.set_ylim(0, ny)
    ax_left.set_aspect("auto")  # stretch to fill panel
    ax_left.axis("off")
    ax_left.set_title("The hachure — the draughtsman's hand",
                      fontsize=11, color=INK, family="serif",
                      style="italic", pad=12)

    # ── Right panel: Contours (slate) ───────────────────────────────
    ax_right.set_facecolor(SLATE_DARK)

    levels = np.arange(1200, 4400, 100)
    cs = ax_right.contour(patch, levels=levels, colors=[CHALK_DIM],
                          linewidths=0.5, alpha=0.5)
    # Major contours every 500m
    major_levels = np.arange(1500, 4500, 500)
    cs_major = ax_right.contour(patch, levels=major_levels, colors=[CHALK],
                                linewidths=1.2, alpha=0.8)
    ax_right.clabel(cs_major, fmt="%d m", fontsize=7, colors=CHALK_DIM)

    ax_right.set_xlim(0, nx)
    ax_right.set_ylim(0, ny)
    ax_right.set_aspect("auto")  # stretch to fill panel
    ax_right.axis("off")
    ax_right.set_title("The contour — the mountain's body",
                       fontsize=11, color=CHALK, family="serif",
                       style="italic", pad=12)

    fig.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.08,
                        wspace=0.05)
    fig.text(0.5, 0.02, "SRTM 3″ · same ground, different notation",
             ha="center", fontsize=8, color=CHALK_DIM,
             style="italic", family="serif")

    save(fig, "fig6-hachure-vs-contour")


# ── Main ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Loading SRTM data from {DEM_PATH}")
    dem = load_dem()
    print(f"  DEM patch: {dem['dem_patch'].shape}")
    print(f"  Transect: {len(dem['d_ene'])} points, {dem['e_ene'].min():.0f}–{dem['e_ene'].max():.0f} m")
    print(f"\nGenerating 6 figures → {OUT}\n")

    fig1_asymmetry(dem)
    fig2_platonic_gorge(dem)
    fig3_survey_to_shape(dem)
    fig4_projection(dem)
    fig5_slope_field(dem)
    fig6_hachure_vs_contour(dem)

    n = len(list(OUT.glob("*.png")))
    print(f"\nDone. {n} figures in {OUT}")
