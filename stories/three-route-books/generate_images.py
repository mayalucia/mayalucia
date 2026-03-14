# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.9",
#     "numpy>=1.26",
#     "scipy>=1.12",
# ]
# ///
"""
Generate illustrations for "Three Route-Books".

Six figures from real SRTM DEM data — the Western Himalaya as the three
travellers would see it: the Trader from the passes, the Pilgrim from
the valleys, the Shepherd from the meadows between.

Visual language: lantern-lit dark slate, chalk lines, copper accents.
Heights are essential — every map carries its own altitude.

Run with:  uv run generate_images.py
"""
from __future__ import annotations

import gzip
import os
from pathlib import Path
from urllib.request import urlopen

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LightSource, LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.ndimage import gaussian_filter, uniform_filter

# ── Output ──────────────────────────────────────────────────────────
SLUG = "three-route-books"
OUT = (Path(__file__).parent / f"../../website/static/images/writing/{SLUG}").resolve()
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
W, H = 14, 9  # wider than usual for terrain

# ── SRTM ────────────────────────────────────────────────────────────
SRTM_SIZE = 3601
VOID = -32768
SRTM_BASE = "https://elevation-tiles-prod.s3.amazonaws.com/skadi"

CACHE_DIR = (Path(__file__).parent / "../../experiments/01-micro-data-centers/data").resolve()

NEEDED_TILES = [(31, 76), (31, 77), (32, 76), (32, 77)]

# ── Palette ─────────────────────────────────────────────────────────
BG_DARK      = "#12121e"
SLATE_DARK   = "#1a1818"
SLATE        = "#2a2a28"
CHALK        = "#e8e4d8"
CHALK_DIM    = "#9a9890"
CHALK_FAINT  = "#6a6860"
PARCHMENT    = "#f5f0e8"
INK          = "#5c4a3a"
INK_LIGHT    = "#8a7a6a"

MOUNTAIN     = "#7a7068"
MOUNTAIN_DK  = "#5a5248"
SNOW         = "#e8eef0"
WATER        = "#4a8b6b"
WATER_DIM    = "#3a6b5b"
DEODAR       = "#4a6b48"
DEODAR_DK    = "#2a4a2a"
COPPER       = "#c4886b"
COPPER_DIM   = "#8a6048"

# Route colours
TRADER_COL   = SNOW        # white — the high passes, salt and snow
PILGRIM_COL  = WATER       # emerald — the valleys, temples, rivers
SHEPHERD_COL = DEODAR      # green — the meadows, grass, forest edge

# ── SRTM loading ────────────────────────────────────────────────────

def srtm_url(lat, lon):
    ns = 'N' if lat >= 0 else 'S'
    ew = 'E' if lon >= 0 else 'W'
    name = f"{ns}{abs(lat):02d}{ew}{abs(lon):03d}"
    return f"{SRTM_BASE}/{ns}{abs(lat):02d}/{name}.hgt.gz", name


def download_tile(lat, lon, data_dir):
    url, name = srtm_url(lat, lon)
    path = os.path.join(data_dir, f"{name}.hgt")
    # Check if path exists and is a valid file (not broken symlink)
    if os.path.isfile(path):
        print(f"  cached: {name}")
        return path
    # Remove broken symlink if present
    if os.path.islink(path):
        os.unlink(path)
    print(f"  downloading {name} ...")
    try:
        raw = gzip.decompress(urlopen(url).read())
        with open(path, 'wb') as f:
            f.write(raw)
        print(f"  saved {name} ({len(raw)/(1024*1024):.1f} MB)")
    except Exception as e:
        print(f"  FAILED {name}: {e}")
        return None
    return path


def load_hgt(path):
    with open(path, 'rb') as f:
        data = np.frombuffer(f.read(), dtype='>i2')
    dem = data.reshape((SRTM_SIZE, SRTM_SIZE)).astype(np.float32)
    dem[dem == VOID] = np.nan
    return dem


def stitch_tiles(tiles_data):
    all_lats = sorted(set(t[0] for t in tiles_data))
    all_lons = sorted(set(t[1] for t in tiles_data))
    n_lat, n_lon = len(all_lats), len(all_lons)
    rows = n_lat * (SRTM_SIZE - 1) + 1
    cols = n_lon * (SRTM_SIZE - 1) + 1
    full = np.full((rows, cols), np.nan, dtype=np.float32)

    for sw_lat, sw_lon, dem in tiles_data:
        lat_idx = n_lat - 1 - all_lats.index(sw_lat)
        lon_idx = all_lons.index(sw_lon)
        r0 = lat_idx * (SRTM_SIZE - 1)
        c0 = lon_idx * (SRTM_SIZE - 1)
        full[r0:r0 + SRTM_SIZE, c0:c0 + SRTM_SIZE] = dem

    north = max(all_lats) + 1
    south = min(all_lats)
    west = min(all_lons)
    east = max(all_lons) + 1
    lats = np.linspace(north, south, rows)
    lons = np.linspace(west, east, cols)
    return full, lats, lons


def load_dem():
    """Load and stitch SRTM tiles for the story area."""
    print("Loading SRTM tiles...")
    tiles_data = []
    for lat, lon in NEEDED_TILES:
        path = download_tile(lat, lon, str(CACHE_DIR))
        if path:
            dem = load_hgt(path)
            tiles_data.append((lat, lon, dem))
    full, lats, lons = stitch_tiles(tiles_data)
    print(f"  Stitched DEM: {full.shape}, "
          f"elev {np.nanmin(full):.0f}–{np.nanmax(full):.0f} m")
    return full, lats, lons


# ── Helpers ─────────────────────────────────────────────────────────

def extract_transect(dem, lats, lons, start, end, n_samples=500):
    """Extract elevation along a line from start (lat,lon) to end (lat,lon)."""
    lat0, lon0 = start
    lat1, lon1 = end
    t_lats = np.linspace(lat0, lat1, n_samples)
    t_lons = np.linspace(lon0, lon1, n_samples)

    # Convert to pixel coordinates
    rows = np.interp(t_lats, lats[::-1], np.arange(len(lats))[::-1])
    cols = np.interp(t_lons, lons, np.arange(len(lons)))

    rows = np.clip(rows.astype(int), 0, dem.shape[0] - 1)
    cols = np.clip(cols.astype(int), 0, dem.shape[1] - 1)

    elevs = dem[rows, cols]

    # Compute distance in km
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * np.cos(np.radians((lat0 + lat1) / 2))
    dlat = (t_lats - lat0) * km_per_deg_lat
    dlon = (t_lons - lon0) * km_per_deg_lon
    dists = np.sqrt(dlat**2 + dlon**2)

    return dists, elevs


def extract_route_profile(dem, lats, lons, waypoints, samples_per_seg=60):
    """Extract elevation profile along a series of (lat, lon) waypoints."""
    all_dists, all_elevs = [], []
    total_dist = 0

    for i in range(len(waypoints) - 1):
        lat0, lon0 = waypoints[i][:2]
        lat1, lon1 = waypoints[i + 1][:2]
        d, e = extract_transect(dem, lats, lons, (lat0, lon0), (lat1, lon1),
                                n_samples=samples_per_seg)
        d = d + total_dist
        if i > 0:
            d = d[1:]
            e = e[1:]
        all_dists.extend(d)
        all_elevs.extend(e)
        total_dist = d[-1] if len(d) > 0 else total_dist

    return np.array(all_dists), np.array(all_elevs)


def style_ax_dark(ax, xlabel="", ylabel=""):
    """Apply dark atmospheric styling to an axis."""
    ax.set_facecolor(SLATE_DARK)
    for spine in ax.spines.values():
        spine.set_color(CHALK_FAINT)
        spine.set_linewidth(0.5)
    ax.tick_params(colors=CHALK_DIM, labelsize=8)
    if xlabel:
        ax.set_xlabel(xlabel, color=CHALK_DIM, fontsize=9, fontfamily="serif")
    if ylabel:
        ax.set_ylabel(ylabel, color=CHALK_DIM, fontsize=9, fontfamily="serif")


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.3, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ {name}.png")


def attribution(ax, text="SRTM 1″ · Western Himalaya", y=-0.06):
    ax.text(0.5, y, text, transform=ax.transAxes, ha="center",
            fontsize=7, color=CHALK_FAINT, style="italic", family="serif")


# ── Route waypoints ─────────────────────────────────────────────────
# (lat, lon, known_elev, label)

TRADER_ROUTE = [
    (31.9578, 77.1095, 1220, "Kullu"),
    (32.1000, 77.1664, 1760, "Naggar"),
    (32.2396, 77.1887, 2050, "Manali"),
    (32.3600, 77.1800, 3400, "Marhi"),
    (32.3719, 77.2371, 3978, "Rohtang"),
    (32.4100, 77.3600, 3140, "Khoksar"),
    (32.3667, 77.5500, 3980, "Batal"),
    (32.4100, 77.7900, 4550, "Kunzum"),
    (32.4400, 78.0200, 4080, "Losar"),
]

PILGRIM_ROUTE = [
    (31.8142, 77.3722, 3120, "Jalori"),
    (31.7639, 77.3611, 2400, "Shoja"),
    (31.6400, 77.2942, 1100, "Ani"),
    (31.5800, 77.3400, 1800, "Nirmand"),
    (31.4456, 77.6292,  975, "Rampur"),
    (31.5125, 77.7736, 1920, "Sarahan"),
    (31.4200, 77.9800, 1450, "Wangtu"),
    (31.4200, 78.2700, 2620, "Sangla"),
    (31.3492, 78.4456, 3450, "Chitkul"),
]

SHEPHERD_ROUTE = [
    (31.7800, 77.3200, 2800, "Khanag"),
    (31.7500, 77.3800, 3000, "ridge"),
    (31.7333, 77.4333, 3200, "Bashleo"),
    (31.7600, 77.4600, 3100, "east meadow"),
    (31.7900, 77.4200, 2900, "Baga Sarahan"),
    (31.7800, 77.3200, 2800, "Khanag"),
]


# ════════════════════════════════════════════════════════════════════
# Figure 1: Watershed Cross-Section
# The central figure — a NE→SW transect from Beas to Sutlej.
# Three altitude bands mark the three travellers' zones.
# ════════════════════════════════════════════════════════════════════

def fig1_watershed_cross_section(dem, lats, lons):
    # Transect: Beas valley → Jalori ridge → Sutlej approach
    start = (31.92, 77.12)   # Beas/Kullu valley floor
    end   = (31.50, 77.48)   # Ani/Sutlej side
    d, e = extract_transect(dem, lats, lons, start, end, n_samples=600)

    # Smooth slightly for visual clarity
    e_smooth = gaussian_filter(e, sigma=3)

    fig, ax = plt.subplots(figsize=(W, 7), facecolor=SLATE_DARK)
    style_ax_dark(ax, xlabel="Distance (km)", ylabel="Elevation (m)")

    # Altitude bands
    ax.axhspan(3500, 5000, color=SNOW, alpha=0.04, zorder=0)
    ax.axhspan(2600, 3500, color=DEODAR, alpha=0.06, zorder=0)
    ax.axhspan(500, 2600, color=WATER, alpha=0.04, zorder=0)

    # Band labels (right side)
    ax.text(d[-1] + 1.5, 4200, "The Trader's\naltitude",
            fontsize=8, color=SNOW, alpha=0.5, fontfamily="serif",
            fontstyle="italic", va="center")
    ax.text(d[-1] + 1.5, 3050, "The Shepherd's\naltitude",
            fontsize=8, color=DEODAR, alpha=0.6, fontfamily="serif",
            fontstyle="italic", va="center")
    ax.text(d[-1] + 1.5, 1800, "The Pilgrim's\naltitude",
            fontsize=8, color=WATER, alpha=0.5, fontfamily="serif",
            fontstyle="italic", va="center")

    # Terrain fill
    ax.fill_between(d, 500, e_smooth, color=MOUNTAIN_DK, alpha=0.5, zorder=2)
    ax.fill_between(d, 500, e_smooth, color=SLATE, alpha=0.3, zorder=2)
    ax.plot(d, e_smooth, color=CHALK, lw=2, zorder=3, alpha=0.9)

    # Jalori marker
    jalori_idx = np.argmax(e_smooth[len(e_smooth)//4:3*len(e_smooth)//4]) + len(e_smooth)//4
    ax.annotate("Jalori\n3,120 m", (d[jalori_idx], e_smooth[jalori_idx]),
                textcoords="offset points", xytext=(0, 18),
                ha="center", fontsize=9, color=COPPER, fontfamily="serif",
                fontstyle="italic",
                arrowprops=dict(arrowstyle="-", color=COPPER_DIM, lw=0.5))

    # Direction labels
    ax.text(d[0], 650, "Beas\n(Kullu)", ha="left", fontsize=9,
            color=CHALK_DIM, fontfamily="serif", fontstyle="italic")
    ax.text(d[-1], 650, "Sutlej\n(Rampur)", ha="right", fontsize=9,
            color=CHALK_DIM, fontfamily="serif", fontstyle="italic")

    # Title
    ax.text(0.5, 1.04, "The Divide", transform=ax.transAxes, ha="center",
            fontsize=14, color=CHALK, fontfamily="serif", fontweight="normal",
            fontstyle="italic")
    ax.text(0.5, 1.00, "Beas–Sutlej watershed through Jalori",
            transform=ax.transAxes, ha="center",
            fontsize=9, color=CHALK_DIM, fontfamily="serif")

    ax.set_xlim(d[0], d[-1])
    ax.set_ylim(500, 5000)
    attribution(ax)
    save(fig, "watershed-cross-section")


# ════════════════════════════════════════════════════════════════════
# Figure 2: Three Routes — Elevation Profiles
# Stacked panels, shared vertical scale. The Trader goes high,
# the Pilgrim goes low, the Shepherd stays between.
# ════════════════════════════════════════════════════════════════════

def fig2_three_routes(dem, lats, lons):
    fig, axes = plt.subplots(3, 1, figsize=(W, 11), facecolor=SLATE_DARK,
                             sharex=False)
    fig.subplots_adjust(hspace=0.35)

    ylim = (400, 5000)

    # ── The Trader ──
    ax = axes[0]
    wps = [(lat, lon) for lat, lon, *_ in TRADER_ROUTE]
    d, e = extract_route_profile(dem, lats, lons, wps)
    e_smooth = gaussian_filter(e, sigma=2)

    style_ax_dark(ax, ylabel="m")
    ax.fill_between(d, 400, e_smooth, color=MOUNTAIN_DK, alpha=0.4)
    ax.plot(d, e_smooth, color=TRADER_COL, lw=2, alpha=0.9)
    ax.set_ylim(*ylim)
    ax.set_xlim(d[0], d[-1])

    # Waypoint labels
    cum_d = 0
    for i, (lat, lon, elev, label) in enumerate(TRADER_ROUTE):
        if i > 0:
            km_per_lat = 111.0
            km_per_lon = 111.0 * np.cos(np.radians(lat))
            dlat = (lat - TRADER_ROUTE[i-1][0]) * km_per_lat
            dlon = (lon - TRADER_ROUTE[i-1][1]) * km_per_lon
            cum_d += np.sqrt(dlat**2 + dlon**2)
        if label in ("Kullu", "Rohtang", "Kunzum", "Losar"):
            ax.annotate(f"{label}\n{elev:,} m", (cum_d, elev),
                        textcoords="offset points",
                        xytext=(0, 12 if elev > 3000 else -18),
                        ha="center", fontsize=7, color=CHALK_DIM,
                        fontfamily="serif", fontstyle="italic")

    ax.text(0.02, 0.92, "The Trader", transform=ax.transAxes,
            fontsize=11, color=TRADER_COL, fontfamily="serif",
            fontstyle="italic", va="top", alpha=0.8)

    # Altitude bands (faint)
    for a in axes:
        a.axhspan(3500, 5000, color=SNOW, alpha=0.03, zorder=0)
        a.axhspan(2600, 3500, color=DEODAR, alpha=0.04, zorder=0)
        a.axhspan(400, 2600, color=WATER, alpha=0.03, zorder=0)

    # ── The Pilgrim ──
    ax = axes[1]
    wps = [(lat, lon) for lat, lon, *_ in PILGRIM_ROUTE]
    d, e = extract_route_profile(dem, lats, lons, wps)
    e_smooth = gaussian_filter(e, sigma=2)

    style_ax_dark(ax, ylabel="m")
    ax.fill_between(d, 400, e_smooth, color=MOUNTAIN_DK, alpha=0.4)
    ax.plot(d, e_smooth, color=PILGRIM_COL, lw=2, alpha=0.9)
    ax.set_ylim(*ylim)
    ax.set_xlim(d[0], d[-1])

    cum_d = 0
    for i, (lat, lon, elev, label) in enumerate(PILGRIM_ROUTE):
        if i > 0:
            km_per_lat = 111.0
            km_per_lon = 111.0 * np.cos(np.radians(lat))
            dlat = (lat - PILGRIM_ROUTE[i-1][0]) * km_per_lat
            dlon = (lon - PILGRIM_ROUTE[i-1][1]) * km_per_lon
            cum_d += np.sqrt(dlat**2 + dlon**2)
        if label in ("Jalori", "Nirmand", "Rampur", "Sarahan", "Chitkul"):
            ax.annotate(f"{label}\n{elev:,} m", (cum_d, elev),
                        textcoords="offset points",
                        xytext=(0, 12 if elev > 2000 else -18),
                        ha="center", fontsize=7, color=CHALK_DIM,
                        fontfamily="serif", fontstyle="italic")

    ax.text(0.02, 0.92, "The Pilgrim", transform=ax.transAxes,
            fontsize=11, color=PILGRIM_COL, fontfamily="serif",
            fontstyle="italic", va="top", alpha=0.8)

    # ── The Shepherd ──
    ax = axes[2]
    style_ax_dark(ax, xlabel="Distance along route (km)", ylabel="m")
    ax.set_ylim(*ylim)

    # The shepherd doesn't travel linearly — she circles the meadows
    # Show as dots connected by a dashed path
    cum_d = 0
    xs, ys = [0], [SHEPHERD_ROUTE[0][2]]
    for i in range(1, len(SHEPHERD_ROUTE)):
        lat, lon, elev = SHEPHERD_ROUTE[i][:3]
        plat, plon = SHEPHERD_ROUTE[i-1][:2]
        km_per_lat = 111.0
        km_per_lon = 111.0 * np.cos(np.radians(lat))
        dlat = (lat - plat) * km_per_lat
        dlon = (lon - plon) * km_per_lon
        cum_d += np.sqrt(dlat**2 + dlon**2)
        xs.append(cum_d)
        ys.append(elev)

    ax.plot(xs, ys, color=SHEPHERD_COL, lw=1.5, ls="--", alpha=0.7, zorder=3)
    ax.scatter(xs, ys, color=SHEPHERD_COL, s=30, zorder=4, alpha=0.9)

    for x, y, (_, _, _, label) in zip(xs, ys, SHEPHERD_ROUTE):
        if label != "ridge":
            ax.annotate(label, (x, y), textcoords="offset points",
                        xytext=(8, 5), fontsize=7, color=CHALK_DIM,
                        fontfamily="serif", fontstyle="italic")

    ax.set_xlim(-2, cum_d + 5)
    ax.text(0.02, 0.92, "The Shepherd", transform=ax.transAxes,
            fontsize=11, color=SHEPHERD_COL, fontfamily="serif",
            fontstyle="italic", va="top", alpha=0.8)

    # Title
    fig.text(0.5, 0.97, "Three Altitudes",
             ha="center", fontsize=14, color=CHALK, fontfamily="serif",
             fontstyle="italic")

    save(fig, "three-routes-elevation")


# ════════════════════════════════════════════════════════════════════
# Figure 3: Relief Map
# Hillshaded terrain with three routes drawn in their colours.
# ════════════════════════════════════════════════════════════════════

def fig3_relief_map(dem, lats, lons):
    # Crop to study area: 31.3–32.5°N, 76.9–78.5°E
    lat_n, lat_s = 32.50, 31.30
    lon_w, lon_e = 76.90, 78.50

    r0 = np.searchsorted(-lats, -lat_n)
    r1 = np.searchsorted(-lats, -lat_s)
    c0 = np.searchsorted(lons, lon_w)
    c1 = np.searchsorted(lons, lon_e)

    crop = dem[r0:r1, c0:c1].copy()
    crop_lats = lats[r0:r1]
    crop_lons = lons[c0:c1]

    # Fill NaN for hillshade computation
    mask = np.isnan(crop)
    if mask.any():
        crop[mask] = np.nanmean(crop)

    # Smooth slightly for visual clarity
    crop_smooth = gaussian_filter(crop, sigma=2)

    # Custom dark terrain colormap
    terrain_cmap = LinearSegmentedColormap.from_list("terrain_dark", [
        (0.00, "#1a1a18"),
        (0.10, "#2a2820"),
        (0.25, "#3a3830"),
        (0.40, "#5a5840"),
        (0.55, "#7a7058"),
        (0.70, "#9a9070"),
        (0.85, "#c8c0a8"),
        (1.00, "#e8eef0"),
    ])

    # Hillshade
    ls = LightSource(azdeg=315, altdeg=30)
    elev_norm = (crop_smooth - np.nanmin(crop_smooth)) / (np.nanmax(crop_smooth) - np.nanmin(crop_smooth) + 1)
    rgb = terrain_cmap(elev_norm)[:, :, :3]
    shaded = ls.shade_rgb(rgb, crop_smooth, vert_exag=3, blend_mode="soft")

    fig, ax = plt.subplots(figsize=(W, 10), facecolor=SLATE_DARK)
    ax.set_facecolor(SLATE_DARK)
    ax.imshow(shaded, extent=[crop_lons[0], crop_lons[-1],
                               crop_lats[-1], crop_lats[0]],
              aspect="auto", interpolation="bilinear")

    # Draw routes
    def plot_route(route, color, ls="-", lw=1.8, label=""):
        route_lons = [r[1] for r in route]
        route_lats = [r[0] for r in route]
        ax.plot(route_lons, route_lats, color=color, lw=lw, ls=ls,
                alpha=0.85, zorder=10, label=label)
        # Start and end markers
        ax.plot(route_lons[0], route_lats[0], 'o', color=color,
                markersize=5, zorder=11, alpha=0.9)
        ax.plot(route_lons[-1], route_lats[-1], 's', color=color,
                markersize=4, zorder=11, alpha=0.9)

    plot_route(TRADER_ROUTE, TRADER_COL, label="The Trader")
    plot_route(PILGRIM_ROUTE, PILGRIM_COL, label="The Pilgrim")
    plot_route(SHEPHERD_ROUTE, SHEPHERD_COL, ls="--", lw=1.5, label="The Shepherd")

    # Key place labels
    places = [
        (31.8142, 77.3722, "Jalori", COPPER),
        (32.3719, 77.2371, "Rohtang", CHALK_DIM),
        (32.4100, 77.7900, "Kunzum", CHALK_DIM),
        (31.5800, 77.3400, "Nirmand", CHALK_DIM),
        (31.4456, 77.6292, "Rampur", CHALK_DIM),
        (31.5125, 77.7736, "Sarahan", CHALK_DIM),
        (31.9578, 77.1095, "Kullu", CHALK_DIM),
        (32.2396, 77.1887, "Manali", CHALK_DIM),
        (31.3492, 78.4456, "Chitkul", CHALK_DIM),
    ]
    for lat, lon, name, col in places:
        if lat_s < lat < lat_n and lon_w < lon < lon_e:
            ax.annotate(name, (lon, lat), textcoords="offset points",
                        xytext=(6, 4), fontsize=7, color=col,
                        fontfamily="serif", fontstyle="italic",
                        zorder=12)
            ax.plot(lon, lat, '.', color=col, markersize=3, zorder=11)

    # "Two waters" meadow marker
    ax.plot(77.43, 31.73, 'o', color=COPPER, markersize=8,
            fillstyle="none", lw=1, alpha=0.6, zorder=11)
    ax.annotate("the meadow", (77.43, 31.73), textcoords="offset points",
                xytext=(10, -4), fontsize=7, color=COPPER,
                fontfamily="serif", fontstyle="italic", alpha=0.7, zorder=12)

    # Serai symbol at Jalori
    ax.plot(77.3722, 31.8142, '^', color=COPPER, markersize=8, zorder=12)

    ax.set_xlim(lon_w, lon_e)
    ax.set_ylim(lat_s, lat_n)
    ax.tick_params(colors=CHALK_FAINT, labelsize=7)
    for spine in ax.spines.values():
        spine.set_color(CHALK_FAINT)
        spine.set_linewidth(0.3)

    # Legend
    leg = ax.legend(loc="lower right", fontsize=8, framealpha=0.3,
                    edgecolor=CHALK_FAINT, facecolor=SLATE_DARK)
    for text in leg.get_texts():
        text.set_color(CHALK_DIM)
        text.set_fontfamily("serif")

    # Title
    ax.text(0.5, 1.03, "The Landscape", transform=ax.transAxes, ha="center",
            fontsize=14, color=CHALK, fontfamily="serif", fontstyle="italic")
    ax.text(0.5, 1.00, "Kullu – Seraj – Sutlej · three routes, one mountain",
            transform=ax.transAxes, ha="center",
            fontsize=9, color=CHALK_DIM, fontfamily="serif")

    attribution(ax, text="SRTM 1″ · 31.3–32.5°N, 76.9–78.5°E")
    save(fig, "relief-map")


# ════════════════════════════════════════════════════════════════════
# Figure 4: Jalori Cross-Section
# N–S through Jalori showing vegetation zones and the serai.
# ════════════════════════════════════════════════════════════════════

def fig4_jalori_section(dem, lats, lons):
    # Transect N–S through Jalori
    start = (31.95, 77.37)   # Beas/Tirthan side (north)
    end   = (31.65, 77.37)   # Shoja/Seraj side (south)
    d, e = extract_transect(dem, lats, lons, start, end, n_samples=400)
    e_smooth = gaussian_filter(e, sigma=3)

    fig, ax = plt.subplots(figsize=(W, 7), facecolor=SLATE_DARK)
    style_ax_dark(ax, xlabel="Distance (km)", ylabel="Elevation (m)")

    # Vegetation zone fills (under the profile)
    # Deodar zone: below 2400m
    below_2400 = np.minimum(e_smooth, 2400)
    ax.fill_between(d, 800, below_2400, color=DEODAR_DK, alpha=0.25,
                    zorder=1, label="Deodar (< 2,400 m)")
    # Birch zone: 2400-2800m
    below_2800 = np.minimum(e_smooth, 2800)
    ax.fill_between(d, 2400, below_2800,
                    where=(e_smooth > 2400),
                    color=DEODAR, alpha=0.15, zorder=1,
                    label="Birch (2,400–2,800 m)")
    # Scrub: 2800-3000m
    below_3000 = np.minimum(e_smooth, 3000)
    ax.fill_between(d, 2800, below_3000,
                    where=(e_smooth > 2800),
                    color=CHALK_FAINT, alpha=0.1, zorder=1,
                    label="Scrub (2,800–3,000 m)")
    # Bare: above 3000m
    ax.fill_between(d, 3000, e_smooth,
                    where=(e_smooth > 3000),
                    color=MOUNTAIN, alpha=0.15, zorder=1,
                    label="Bare ridge (> 3,000 m)")

    # Terrain profile
    ax.fill_between(d, 800, e_smooth, color=MOUNTAIN_DK, alpha=0.3, zorder=2)
    ax.plot(d, e_smooth, color=CHALK, lw=2, zorder=3)

    # Jalori/serai marker (highest point on profile)
    jalori_idx = np.argmax(e_smooth)
    ax.plot(d[jalori_idx], e_smooth[jalori_idx], '^', color=COPPER,
            markersize=10, zorder=5)
    ax.annotate("Serai\n3,120 m", (d[jalori_idx], e_smooth[jalori_idx]),
                textcoords="offset points", xytext=(12, 8),
                fontsize=9, color=COPPER, fontfamily="serif",
                fontstyle="italic")

    # Quote
    ax.text(0.98, 0.05,
            "the last weeks before snow\ncloses the pass",
            transform=ax.transAxes, ha="right", fontsize=8,
            color=COPPER_DIM, fontfamily="serif", fontstyle="italic",
            alpha=0.6)

    # Direction labels
    ax.text(d[0], 900, "Tirthan valley\n(Beas side)", ha="left", fontsize=8,
            color=CHALK_DIM, fontfamily="serif", fontstyle="italic")
    ax.text(d[-1], 900, "Outer Seraj\n(Sutlej side)", ha="right", fontsize=8,
            color=CHALK_DIM, fontfamily="serif", fontstyle="italic")

    ax.set_xlim(d[0], d[-1])
    ax.set_ylim(800, 3800)

    leg = ax.legend(loc="upper left", fontsize=7, framealpha=0.3,
                    edgecolor=CHALK_FAINT, facecolor=SLATE_DARK)
    for text in leg.get_texts():
        text.set_color(CHALK_DIM)
        text.set_fontfamily("serif")

    ax.text(0.5, 1.04, "The Serai at Jalori", transform=ax.transAxes,
            ha="center", fontsize=14, color=CHALK, fontfamily="serif",
            fontstyle="italic")

    attribution(ax)
    save(fig, "jalori-section")


# ════════════════════════════════════════════════════════════════════
# Figure 5: Two Waters
# 3D surface of the watershed saddle where two streams almost meet.
# ════════════════════════════════════════════════════════════════════

def fig5_two_waters(dem, lats, lons):
    # Crop around the Bashleo/Jalori ridge — the watershed divide
    lat_n, lat_s = 31.80, 31.70
    lon_w, lon_e = 77.35, 77.48

    r0 = np.searchsorted(-lats, -lat_n)
    r1 = np.searchsorted(-lats, -lat_s)
    c0 = np.searchsorted(lons, lon_w)
    c1 = np.searchsorted(lons, lon_e)

    patch = dem[r0:r1, c0:c1].copy()
    patch_lats = lats[r0:r1]
    patch_lons = lons[c0:c1]

    # Fill NaN
    mask = np.isnan(patch)
    if mask.any():
        patch[mask] = np.nanmean(patch)

    # Subsample for 3D rendering (every 3rd pixel)
    sub = 3
    Z = patch[::sub, ::sub]
    Z = gaussian_filter(Z, sigma=1)
    ny, nx = Z.shape
    X = np.linspace(0, (lon_e - lon_w) * 111 * np.cos(np.radians(31.75)), nx)
    Y = np.linspace(0, (lat_n - lat_s) * 111, ny)
    X, Y = np.meshgrid(X, Y)

    # Custom monochrome colormap — dark valleys to chalk ridges
    mono_cmap = LinearSegmentedColormap.from_list("mono_terrain", [
        (0.0, "#0e0c08"),
        (0.3, "#2a2820"),
        (0.5, "#5a5248"),
        (0.7, "#8a8070"),
        (1.0, "#d8d0c0"),
    ])

    fig = plt.figure(figsize=(W, 9), facecolor=SLATE_DARK)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(SLATE_DARK)

    # Normalize Z for colour mapping
    z_norm = (Z - Z.min()) / (Z.max() - Z.min() + 1)
    colors = mono_cmap(z_norm)

    # Hillshade via light source
    ls = LightSource(azdeg=315, altdeg=20)
    shade = ls.hillshade(Z, vert_exag=2)
    # Multiply colours by shade
    for i in range(3):
        colors[:, :, i] *= 0.4 + 0.6 * shade

    ax.plot_surface(X, Y, Z, facecolors=colors, rstride=1, cstride=1,
                    linewidth=0, antialiased=True, shade=False)

    ax.view_init(elev=28, azim=225)
    ax.set_box_aspect([1, 0.8, 0.4])

    # Remove axis clutter
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor(SLATE_DARK)
    ax.yaxis.pane.set_edgecolor(SLATE_DARK)
    ax.zaxis.pane.set_edgecolor(SLATE_DARK)
    ax.grid(False)

    # Stream direction annotations
    ax.text2D(0.15, 0.25, "→ Beas", transform=ax.transAxes,
              fontsize=10, color=WATER, fontfamily="serif",
              fontstyle="italic", alpha=0.7)
    ax.text2D(0.75, 0.25, "→ Sutlej", transform=ax.transAxes,
              fontsize=10, color=WATER_DIM, fontfamily="serif",
              fontstyle="italic", alpha=0.7)

    # Caption
    ax.text2D(0.5, 0.03,
              "\"the meadow where the two waters almost meet\"",
              transform=ax.transAxes, ha="center", fontsize=10,
              color=COPPER, fontfamily="serif", fontstyle="italic")

    ax.text2D(0.5, 0.97, "Two Waters", transform=ax.transAxes,
              ha="center", fontsize=14, color=CHALK, fontfamily="serif",
              fontstyle="italic")

    save(fig, "two-waters")


# ════════════════════════════════════════════════════════════════════
# Figure 6: Connections Web
# The hidden connections between route-books drawn as threads
# between three altitude bands on a simplified terrain profile.
# ════════════════════════════════════════════════════════════════════

def fig6_connections_web(dem, lats, lons):
    fig, ax = plt.subplots(figsize=(W, 8), facecolor=SLATE_DARK)
    ax.set_facecolor(SLATE_DARK)

    # Use watershed transect as background silhouette
    start = (31.92, 77.12)
    end   = (31.50, 77.48)
    d, e = extract_transect(dem, lats, lons, start, end, n_samples=300)
    e_smooth = gaussian_filter(e, sigma=5)

    # Normalise to 0–100 coordinate system
    x = np.linspace(5, 95, len(d))
    y = 10 + 60 * (e_smooth - e_smooth.min()) / (e_smooth.max() - e_smooth.min())

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 85)
    ax.set_aspect("equal")
    ax.axis("off")

    # Faint terrain silhouette
    ax.fill_between(x, 5, y, color=MOUNTAIN_DK, alpha=0.2)
    ax.plot(x, y, color=CHALK_FAINT, lw=1, alpha=0.4)

    # Altitude bands (horizontal)
    bands = [
        (62, 75, SNOW, "passes", 0.04),
        (42, 58, DEODAR, "meadows", 0.05),
        (12, 38, WATER, "valleys", 0.04),
    ]
    for y0, y1, col, label, alpha in bands:
        ax.axhspan(y0, y1, color=col, alpha=alpha, zorder=0)
        ax.text(98, (y0 + y1) / 2, label, ha="right", va="center",
                fontsize=8, color=col, fontfamily="serif",
                fontstyle="italic", alpha=0.5)

    # Connection nodes
    rng = np.random.default_rng(42)
    nodes = {
        "grandmother_song":  (25, 68, "the grandmother's\nsong", TRADER_COL),
        "grandmother_weave": (30, 48, "the grandmother's\nweaving", SHEPHERD_COL),
        "mark_kunzum":       (75, 70, "the carved mark\nat Kunzum", TRADER_COL),
        "mark_nirmand":      (70, 25, "the same mark\nat Nirmand", PILGRIM_COL),
        "ratan_muleteer":    (40, 66, "Ratan\nthe muleteer", TRADER_COL),
        "ratan_brother":     (45, 28, "\"my brother\nRatan\"", PILGRIM_COL),
        "meadow_song":       (20, 72, "\"where the two\nwaters almost meet\"", COPPER),
        "meadow_real":       (22, 50, "the actual\nmeadow", SHEPHERD_COL),
        "pilgrim_dream":     (60, 30, "the Pilgrim's\ndream", PILGRIM_COL),
        "shepherd_seen":     (55, 46, "\"you dreamed\nof me\"", SHEPHERD_COL),
    }

    for key, (nx, ny, label, col) in nodes.items():
        ax.plot(nx, ny, 'o', color=col, markersize=5, alpha=0.8, zorder=5)
        ax.text(nx + 2, ny + 1.5, label, fontsize=6.5, color=col,
                fontfamily="serif", fontstyle="italic", alpha=0.7, zorder=5)

    # Connection threads (bezier curves between nodes)
    connections = [
        ("grandmother_song", "grandmother_weave", COPPER, 1.5, "-"),
        ("mark_kunzum", "mark_nirmand", CHALK_DIM, 1.0, "--"),
        ("ratan_muleteer", "ratan_brother", WATER, 1.2, "-"),
        ("meadow_song", "meadow_real", DEODAR, 1.0, "-"),
        ("pilgrim_dream", "shepherd_seen", INK_LIGHT, 1.0, ":"),
    ]

    for n1, n2, col, lw, ls in connections:
        x1, y1 = nodes[n1][:2]
        x2, y2 = nodes[n2][:2]
        # Simple bezier via midpoint offset
        mid_x = (x1 + x2) / 2 + rng.uniform(-3, 3)
        mid_y = (y1 + y2) / 2 + rng.uniform(-2, 2)
        # Draw as smooth curve through 3 points
        ts = np.linspace(0, 1, 40)
        bx = (1 - ts)**2 * x1 + 2 * (1 - ts) * ts * mid_x + ts**2 * x2
        by = (1 - ts)**2 * y1 + 2 * (1 - ts) * ts * mid_y + ts**2 * y2
        ax.plot(bx, by, color=col, lw=lw, ls=ls, alpha=0.5, zorder=3)

    # Title
    ax.text(50, 82, "What the Thread Walker Sees",
            ha="center", fontsize=14, color=CHALK, fontfamily="serif",
            fontstyle="italic")

    save(fig, "connections-web")


# ════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════

def main():
    print(f"Output: {OUT}\n")
    dem, lats, lons = load_dem()

    print("\nGenerating illustrations...")
    fig1_watershed_cross_section(dem, lats, lons)
    fig2_three_routes(dem, lats, lons)
    fig3_relief_map(dem, lats, lons)
    fig4_jalori_section(dem, lats, lons)
    fig5_two_waters(dem, lats, lons)
    fig6_connections_web(dem, lats, lons)
    print("\nDone.")


if __name__ == "__main__":
    main()
