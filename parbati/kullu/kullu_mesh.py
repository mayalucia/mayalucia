#!/usr/bin/env python3
"""
Kullu Valleys DEM mesh — entire Beas drainage from Aut to Lahaul.

Covers 31.40–32.70°N, 76.80–78.00°E: ~140 x 110 km.
Four SRTM tiles stitched, bare OBJ for Blender (vertex colors applied there).

Usage:
    vload py310
    python3 parbati/kullu/kullu_mesh.py
"""

import gzip
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import ListedColormap, BoundaryNorm
from PIL import Image
from io import BytesIO
from urllib.request import urlopen, Request
from scipy.ndimage import distance_transform_edt

# ── Configuration ──────────────────────────────────────────────────────

SRTM_SIZE = 3601
VOID = -32768
SRTM_BASE = "https://elevation-tiles-prod.s3.amazonaws.com/skadi"

# Full Kullu district Beas drainage: Aut to Lahaul/Chenab divide
EXTENT = dict(lat_min=31.40, lat_max=32.70, lon_min=76.80, lon_max=78.00)

# 2x2 SRTM tile grid
TILES = [(31, 76), (31, 77), (32, 76), (32, 77)]

# Meters per degree at center latitude (~32.05°N)
DEG_LAT_M = 111320.0
DEG_LON_M = 111320.0 * np.cos(np.radians(32.05))

# Subsample factor: step=8 → ~240m resolution, ~316K vertices
STEP = 8

# ── Landmarks ──────────────────────────────────────────────────────────

PLACES = {
    # Towns along the Beas
    'Aut':                       (31.530, 77.060),
    'Bhuntar':                   (31.876, 77.160),
    'Kullu':                     (31.958, 77.109),
    'Naggar':                    (32.112, 77.169),
    'Manali':                    (32.240, 77.189),
    'Keylong':                   (32.572, 77.031),
    # Parvati Valley
    'Kasol':                     (32.010, 77.315),
    'Manikaran':                 (32.030, 77.348),
    'Kheerganga':                (32.038, 77.493),
    # Peaks
    'Parvati Parbat\n6632 m':   (32.091, 77.735),
    'Hanuman Tibba\n5932 m':    (32.273, 77.132),
    'Deo Tibba\n6001 m':        (32.349, 77.196),
    'Indrasan\n6221 m':         (32.310, 77.130),
    # Passes
    'Rohtang Pass\n3978 m':     (32.372, 77.248),
    'Pin Parvati Pass':          (32.070, 77.820),
    'Hamta Pass':                (32.307, 77.212),
    'Jalori Pass':               (31.527, 77.370),
    'Chandrakhani Pass':         (31.979, 77.183),
    # Valleys
    'Tirthan Valley':            (31.630, 77.450),
    'Sainj Valley':              (31.720, 77.300),
    'Solang Valley':             (32.310, 77.160),
    # Protected areas
    'GHNP':                      (31.750, 77.500),
    'Khirganga NP':              (32.050, 77.600),
    # Rivers (label at midpoints)
    'Beas River':                (31.750, 77.100),
    'Parvati River':             (32.020, 77.380),
}

# ── Biome elevation bands ─────────────────────────────────────────────
# (z_min, z_max, label, RGBA color)

BIOME_BANDS = [
    (    0, 1000, 'Sub-tropical lowland',         (0.85, 0.75, 0.55, 1.0)),
    ( 1000, 1800, 'Subtropical (Chir pine)',       (0.70, 0.80, 0.40, 1.0)),
    ( 1800, 2700, 'Moist Temperate (Deodar)',      (0.18, 0.50, 0.20, 1.0)),
    ( 2700, 3200, 'Upper Temperate (Fir/Spruce)',  (0.15, 0.40, 0.25, 1.0)),
    ( 3200, 3600, 'Subalpine (Birch)',             (0.50, 0.60, 0.35, 1.0)),
    ( 3600, 4500, 'Alpine Meadow',                 (0.65, 0.75, 0.45, 1.0)),
    ( 4500, 5200, 'Subnival',                      (0.75, 0.72, 0.68, 1.0)),
    ( 5200, 9000, 'Nival (Snow/Ice)',              (0.95, 0.96, 0.98, 1.0)),
]


# ── SRTM functions ────────────────────────────────────────────────────

def srtm_url(lat, lon):
    ns = 'N' if lat >= 0 else 'S'
    ew = 'E' if lon >= 0 else 'W'
    name = f"{ns}{abs(lat):02d}{ew}{abs(lon):03d}"
    return f"{SRTM_BASE}/{ns}{abs(lat):02d}/{name}.hgt.gz", name


def download_tile(lat, lon, data_dir):
    url, name = srtm_url(lat, lon)
    path = os.path.join(data_dir, f"{name}.hgt")
    if os.path.exists(path):
        print(f"  cached: {name}")
        return path
    print(f"  downloading {name} ...")
    raw = gzip.decompress(urlopen(url).read())
    with open(path, 'wb') as f:
        f.write(raw)
    print(f"  saved ({len(raw)/(1024*1024):.1f} MB)")
    return path


def load_hgt(path):
    with open(path, 'rb') as f:
        data = np.frombuffer(f.read(), dtype='>i2')
    dem = data.reshape((SRTM_SIZE, SRTM_SIZE)).astype(np.float32)
    dem[dem == VOID] = np.nan
    return dem


def stitch_and_crop(tiles_data, lat_min, lat_max, lon_min, lon_max):
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
        full[r0:r0+SRTM_SIZE, c0:c0+SRTM_SIZE] = dem
    full_north = max(all_lats) + 1
    full_south = min(all_lats)
    full_west = min(all_lons)
    full_east = max(all_lons) + 1
    r0 = int((full_north - lat_max) / (full_north - full_south) * (rows - 1))
    r1 = int((full_north - lat_min) / (full_north - full_south) * (rows - 1))
    c0 = int((lon_min - full_west) / (full_east - full_west) * (cols - 1))
    c1 = int((lon_max - full_west) / (full_east - full_west) * (cols - 1))
    r0, r1 = max(0, r0), min(rows - 1, r1)
    c0, c1 = max(0, c0), min(cols - 1, c1)
    crop = full[r0:r1+1, c0:c1+1]
    lats = np.linspace(lat_max, lat_min, crop.shape[0])
    lons = np.linspace(lon_min, lon_max, crop.shape[1])
    return crop, lats, lons


# ── Bare OBJ export (no texture) ──────────────────────────────────────

def write_obj_bare(filepath, elev, lats, lons, mtl_filename):
    nr, nc = elev.shape
    center_lat = (lats[0] + lats[-1]) / 2
    center_lon = (lons[0] + lons[-1]) / 2

    # Fill NaN
    mask = np.isnan(elev)
    if mask.any():
        _, indices = distance_transform_edt(mask, return_distances=True, return_indices=True)
        elev = elev.copy()
        elev[mask] = elev[tuple(indices[:, mask])]

    print(f"  writing bare OBJ: {nr}x{nc} = {nr*nc:,} vertices, "
          f"{2*(nr-1)*(nc-1):,} triangles ...")

    with open(filepath, 'w') as f:
        f.write(f"# Kullu Valleys DEM mesh\n")
        f.write(f"# {nr}x{nc} grid, {nr*nc:,} vertices\n")
        f.write(f"# Extent: {EXTENT['lat_min']}-{EXTENT['lat_max']}N, "
                f"{EXTENT['lon_min']}-{EXTENT['lon_max']}E\n")
        f.write(f"mtllib {os.path.basename(mtl_filename)}\n")
        f.write(f"usemtl terrain\n\n")

        for r in range(nr):
            lat = lats[r]
            for c in range(nc):
                lon = lons[c]
                x = (lon - center_lon) * DEG_LON_M
                y = (lat - center_lat) * DEG_LAT_M
                z = elev[r, c]
                f.write(f"v {x:.1f} {y:.1f} {z:.1f}\n")

        f.write(f"\n# Faces\n")
        for r in range(nr - 1):
            for c in range(nc - 1):
                tl = r * nc + c + 1
                tr = r * nc + (c + 1) + 1
                bl = (r + 1) * nc + c + 1
                br = (r + 1) * nc + (c + 1) + 1
                f.write(f"f {tl} {bl} {tr}\n")
                f.write(f"f {tr} {bl} {br}\n")

    print(f"  wrote: {os.path.basename(filepath)}")


def write_mtl_bare(filepath):
    """Simple MTL — vertex colors will be applied in Blender."""
    with open(filepath, 'w') as f:
        f.write("# Kullu terrain material (vertex colors in Blender)\n")
        f.write("newmtl terrain\n")
        f.write("Ka 0.2 0.2 0.2\n")
        f.write("Kd 0.8 0.8 0.8\n")
        f.write("Ks 0.0 0.0 0.0\n")
        f.write("d 1.0\n")
        f.write("illum 1\n")
    print(f"  wrote: {os.path.basename(filepath)}")


# ── Main ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")
    mesh_dir = os.path.join(data_dir, "meshes")
    os.makedirs(mesh_dir, exist_ok=True)

    # 1. Load DEM tiles
    print("Loading DEM tiles (4-tile 2x2 grid)...")
    tiles_data = []
    for lat, lon in TILES:
        path = download_tile(lat, lon, data_dir)
        dem = load_hgt(path)
        tiles_data.append((lat, lon, dem))
        print(f"  {lat}N {lon}E: range {np.nanmin(dem):.0f}-{np.nanmax(dem):.0f} m")

    # 2. Stitch and crop
    print("\nStitching to Kullu extent...")
    elev, lats, lons = stitch_and_crop(tiles_data, **EXTENT)
    print(f"  DEM: {elev.shape}, range: {np.nanmin(elev):.0f}-{np.nanmax(elev):.0f} m")
    print(f"  Extent: {EXTENT['lat_min']}-{EXTENT['lat_max']}N, "
          f"{EXTENT['lon_min']}-{EXTENT['lon_max']}E")
    km_ns = (EXTENT['lat_max'] - EXTENT['lat_min']) * 111.32
    km_ew = (EXTENT['lon_max'] - EXTENT['lon_min']) * 111.32 * np.cos(np.radians(32.05))
    print(f"  Size: ~{km_ns:.0f} x {km_ew:.0f} km")

    # 3. Hillshade map with landmarks
    print("\nRendering hillshade...")
    from matplotlib.colors import LightSource
    ls = LightSource(azdeg=315, altdeg=40)
    rgb = ls.shade(elev, cmap=plt.cm.terrain, blend_mode='soft',
                   vert_exag=2, vmin=np.nanmin(elev), vmax=np.nanmax(elev))

    fig, ax = plt.subplots(figsize=(18, 20))
    extent_box = [EXTENT['lon_min'], EXTENT['lon_max'],
                  EXTENT['lat_min'], EXTENT['lat_max']]
    ax.imshow(rgb, extent=extent_box, aspect='auto')

    for name, (lat, lon) in PLACES.items():
        is_peak = any(kw in name for kw in ['Parbat', 'Tibba', 'Indrasan'])
        is_pass = 'Pass' in name
        is_river = 'River' in name
        is_np = name in ('GHNP', 'Khirganga NP')
        if is_peak:
            marker, color, size = '^', 'red', 10
        elif is_pass:
            marker, color, size = 'D', 'gold', 7
        elif is_river:
            marker, color, size = 's', 'deepskyblue', 6
        elif is_np:
            marker, color, size = 'p', 'limegreen', 9
        else:
            marker, color, size = 'o', 'white', 6
        ax.plot(lon, lat, marker=marker, color=color, markersize=size,
                markeredgecolor='k', markeredgewidth=0.5)
        ax.annotate(name.replace('\n', ' '), (lon, lat), fontsize=6,
                    fontweight='bold', color='white', ha='left', va='bottom',
                    xytext=(5, 3), textcoords='offset points',
                    path_effects=[pe.withStroke(linewidth=2, foreground='black')])

    ax.set_xlabel('Longitude (°E)')
    ax.set_ylabel('Latitude (°N)')
    ax.set_title('Kullu Valleys — Beas Drainage: Aut to Lahaul',
                 fontsize=14)

    hs_path = os.path.join(data_dir, 'kullu_hillshade.png')
    fig.savefig(hs_path, dpi=180, bbox_inches='tight')
    print(f"  saved: {hs_path}")

    # 4. Biome zone map
    print("\nRendering biome zone map...")
    boundaries = [b[0] for b in BIOME_BANDS] + [BIOME_BANDS[-1][1]]
    colors = [b[3] for b in BIOME_BANDS]
    labels = [b[2] for b in BIOME_BANDS]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(boundaries, cmap.N)

    # Shade with hillshade underneath biome colors
    elev_display = np.where(np.isnan(elev), 0, elev)
    hs_grey = ls.hillshade(elev_display, vert_exag=2)

    fig2, ax2 = plt.subplots(figsize=(18, 20))
    ax2.imshow(hs_grey, extent=extent_box, aspect='auto', cmap='gray',
               vmin=0, vmax=1, alpha=1.0)
    im = ax2.imshow(elev_display, extent=extent_box, aspect='auto',
                    cmap=cmap, norm=norm, alpha=0.6)

    # Legend
    from matplotlib.patches import Patch
    legend_handles = [Patch(facecolor=c[:3], label=f"{BIOME_BANDS[i][0]}-{BIOME_BANDS[i][1]}m: {labels[i]}")
                      for i, c in enumerate(colors)]
    ax2.legend(handles=legend_handles, loc='lower left', fontsize=7,
               framealpha=0.85, title='Biome Zones', title_fontsize=8)

    # Annotate protected areas
    for name in ('GHNP', 'Khirganga NP'):
        lat, lon = PLACES[name]
        ax2.plot(lon, lat, 'p', color='limegreen', markersize=12,
                 markeredgecolor='k', markeredgewidth=1)
        ax2.annotate(name, (lon, lat), fontsize=8, fontweight='bold',
                     color='white', ha='center', va='bottom',
                     xytext=(0, 8), textcoords='offset points',
                     path_effects=[pe.withStroke(linewidth=2, foreground='black')])

    ax2.set_xlabel('Longitude (°E)')
    ax2.set_ylabel('Latitude (°N)')
    ax2.set_title('Kullu Valleys — Biome Zones (Elevation-Based Classification)',
                  fontsize=14)

    biome_path = os.path.join(data_dir, 'kullu_biome_map.png')
    fig2.savefig(biome_path, dpi=180, bbox_inches='tight')
    print(f"  saved: {biome_path}")

    # 5. Export bare OBJ mesh (subsampled)
    print("\nExporting bare mesh...")
    elev_s = elev[::STEP, ::STEP]
    lats_s = lats[::STEP]
    lons_s = lons[::STEP]
    print(f"  subsampled x{STEP}: {elev_s.shape}")

    obj_path = os.path.join(mesh_dir, 'kullu.obj')
    mtl_path = os.path.join(mesh_dir, 'kullu.mtl')
    write_mtl_bare(mtl_path)
    write_obj_bare(obj_path, elev_s, lats_s, lons_s, mtl_path)

    nv = elev_s.shape[0] * elev_s.shape[1]
    nf = 2 * (elev_s.shape[0] - 1) * (elev_s.shape[1] - 1)
    size_mb = os.path.getsize(obj_path) / (1024 * 1024)
    print(f"  -> {nv:,} vertices, {nf:,} triangles, {size_mb:.1f} MB")

    plt.show()
    print("\nDone.")
