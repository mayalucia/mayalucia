#!/usr/bin/env python3
"""
Parvati Valley — full extent from Bhuntar to Pin Parvati Pass.

Stitches two SRTM tiles (N31E077 + N32E077) to cover the valley's
~70 km run from the Beas confluence up to the glacial headwaters.

Usage:
    vload py310
    python3 parbati/parbati_valley.py
"""

import gzip
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import LightSource
from urllib.request import urlopen

# ── Configuration ──────────────────────────────────────────────────────

SRTM_SIZE = 3601
VOID = -32768
SRTM_BASE = "https://elevation-tiles-prod.s3.amazonaws.com/skadi"

# Bounding box: full Parvati Valley
LAT_MIN, LAT_MAX = 31.84, 32.20
LON_MIN, LON_MAX = 77.10, 77.88

# Tiles needed (SW corners)
TILES = [(32, 77), (31, 77)]

# Landmarks
PLACES = {
    'Parvati Parbat\n6632 m':   (32.0905, 77.7347, 'r^', 12),
    'Bhuntar':                   (31.876,  77.160,  'wo', 8),
    'Kasol':                     (32.010,  77.315,  'wo', 8),
    'Manikaran':                 (32.030,  77.348,  'ws', 8),
    'Kheerganga':                (32.038,  77.493,  'wo', 8),
    'Pin Parvati\nPass ~5300 m': (32.070,  77.820,  'r*', 10),
}

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
    response = urlopen(url)
    raw = gzip.decompress(response.read())
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
    """Stitch multiple 1°×1° tiles and crop to bounding box.

    tiles_data: list of (sw_lat, sw_lon, dem_array)
    """
    # Determine full grid extent
    all_lats = sorted(set(t[0] for t in tiles_data))
    all_lons = sorted(set(t[1] for t in tiles_data))

    n_lat = len(all_lats)  # tiles in latitude
    n_lon = len(all_lons)  # tiles in longitude

    # Full stitched array (tiles share border pixels — overlap by 1)
    rows = n_lat * (SRTM_SIZE - 1) + 1
    cols = n_lon * (SRTM_SIZE - 1) + 1
    full = np.full((rows, cols), np.nan, dtype=np.float32)

    for sw_lat, sw_lon, dem in tiles_data:
        # Position in grid: northernmost tile = row 0
        lat_idx = n_lat - 1 - all_lats.index(sw_lat)
        lon_idx = all_lons.index(sw_lon)
        r0 = lat_idx * (SRTM_SIZE - 1)
        c0 = lon_idx * (SRTM_SIZE - 1)
        full[r0:r0+SRTM_SIZE, c0:c0+SRTM_SIZE] = dem

    # Full extent
    full_north = max(all_lats) + 1
    full_south = min(all_lats)
    full_west = min(all_lons)
    full_east = max(all_lons) + 1

    # Pixel coordinates for crop
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

# ── Main ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")
    os.makedirs(data_dir, exist_ok=True)

    # 1. Download tiles
    print("Fetching SRTM tiles...")
    tiles_data = []
    for lat, lon in TILES:
        path = download_tile(lat, lon, data_dir)
        dem = load_hgt(path)
        tiles_data.append((lat, lon, dem))
        print(f"  {lat}°N {lon}°E: range {np.nanmin(dem):.0f}–{np.nanmax(dem):.0f} m")

    # 2. Stitch and crop
    print("Stitching and cropping...")
    elev, lats, lons = stitch_and_crop(tiles_data, LAT_MIN, LAT_MAX, LON_MIN, LON_MAX)
    print(f"  extent: {LAT_MIN}–{LAT_MAX}°N, {LON_MIN}–{LON_MAX}°E")
    print(f"  grid:   {elev.shape[0]}×{elev.shape[1]} ({elev.shape[0]*30/1000:.0f}×{elev.shape[1]*30/1000:.0f} km)")
    print(f"  range:  {np.nanmin(elev):.0f}–{np.nanmax(elev):.0f} m")

    # 3. Render hillshade with matplotlib's LightSource
    print("Rendering valley view...")
    ls = LightSource(azdeg=315, altdeg=40)
    rgb = ls.shade(elev, cmap=plt.cm.terrain, blend_mode='soft',
                   vert_exag=2, vmin=np.nanmin(elev), vmax=np.nanmax(elev))

    fig, ax = plt.subplots(figsize=(18, 10))
    ax.imshow(rgb, extent=[LON_MIN, LON_MAX, LAT_MIN, LAT_MAX],
              aspect='auto')

    # Mark places
    for name, (lat, lon, marker, size) in PLACES.items():
        ax.plot(lon, lat, marker, markersize=size, markeredgecolor='k',
                markeredgewidth=0.5)
        ax.annotate(name, (lon, lat), fontsize=8, fontweight='bold',
                    color='white', ha='left', va='bottom',
                    xytext=(5, 3), textcoords='offset points',
                    path_effects=[pe.withStroke(linewidth=2, foreground='black')])

    ax.set_xlabel('Longitude (°E)')
    ax.set_ylabel('Latitude (°N)')
    ax.set_title('Parvati Valley — Bhuntar to Pin Parvati Pass', fontsize=16)

    out_path = os.path.join(data_dir, 'parbati_valley.png')
    fig.savefig(out_path, dpi=180, bbox_inches='tight')
    print(f"  saved: {out_path}")

    # 4. Elevation profile along the valley (approximate river course)
    print("Extracting valley profile...")
    # Sample points along the river (rough centerline, west to east)
    river_pts = [
        (31.876, 77.160),  # Bhuntar
        (31.92,  77.20),
        (31.96,  77.25),
        (32.00,  77.29),   # near Kasol
        (32.01,  77.32),
        (32.03,  77.35),   # Manikaran
        (32.03,  77.40),
        (32.04,  77.45),
        (32.04,  77.50),   # Kheerganga area
        (32.05,  77.55),
        (32.06,  77.60),
        (32.07,  77.65),
        (32.08,  77.70),
        (32.09,  77.73),   # below peak
    ]

    profile_lats = [p[0] for p in river_pts]
    profile_lons = [p[1] for p in river_pts]

    # Interpolate elevation at these points
    from scipy.interpolate import RegularGridInterpolator
    interp = RegularGridInterpolator((lats[::-1], lons), elev[::-1, :],
                                      method='linear', bounds_error=False)
    profile_elev = interp(np.array(river_pts))

    # Cumulative distance (approximate, in km)
    dist = [0.0]
    for i in range(1, len(river_pts)):
        dlat = (river_pts[i][0] - river_pts[i-1][0]) * 111.0
        dlon = (river_pts[i][1] - river_pts[i-1][1]) * 111.0 * np.cos(np.radians(river_pts[i][0]))
        dist.append(dist[-1] + np.sqrt(dlat**2 + dlon**2))

    fig2, ax2 = plt.subplots(figsize=(14, 5))
    ax2.fill_between(dist, profile_elev, alpha=0.3, color='steelblue')
    ax2.plot(dist, profile_elev, 'o-', color='steelblue', linewidth=2, markersize=4)
    ax2.set_xlabel('Distance along valley (km)')
    ax2.set_ylabel('Elevation (m)')
    ax2.set_title('Parvati Valley — Longitudinal Profile (Bhuntar → Peak)')
    ax2.grid(True, alpha=0.3)

    # Annotate key points
    labels = ['Bhuntar', '', '', 'Kasol', '', 'Manikaran', '', '', 'Kheerganga', '', '', '', '', 'Peak base']
    for i, lbl in enumerate(labels):
        if lbl:
            ax2.annotate(lbl, (dist[i], profile_elev[i]), fontsize=9,
                         ha='center', va='bottom', xytext=(0, 8),
                         textcoords='offset points')

    prof_path = os.path.join(data_dir, 'parbati_profile.png')
    fig2.savefig(prof_path, dpi=150, bbox_inches='tight')
    print(f"  saved: {prof_path}")

    plt.show()
    print("Done.")
