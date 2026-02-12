#!/usr/bin/env python3
"""
Expanded Parvati Valley mesh — full biodiversity extent.

Covers GHNP + Khirganga NP + full watershed: 31.50–32.30°N, 77.00–78.00°E.
~90 x 100 km, two SRTM tiles stitched, textured OBJ for Blender.

Usage:
    vload py310
    python3 parbati/parbati_expanded_mesh.py
"""

import gzip
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import LightSource
from PIL import Image
from io import BytesIO
from urllib.request import urlopen, Request
from scipy.ndimage import distance_transform_edt

# ── Configuration ──────────────────────────────────────────────────────

SRTM_SIZE = 3601
VOID = -32768
SRTM_BASE = "https://elevation-tiles-prod.s3.amazonaws.com/skadi"
EOX_WMS = "https://tiles.maps.eox.at/wms"

# Expanded extent: GHNP + Khirganga NP + full watershed
EXTENT = dict(lat_min=31.50, lat_max=32.30, lon_min=77.00, lon_max=78.00)

TILES = [(31, 77), (32, 77)]

# Meters per degree
DEG_LAT_M = 111320.0
DEG_LON_M = 111320.0 * np.cos(np.radians(31.9))

# Landmarks
PLACES = {
    'Parvati Parbat\n6632 m':   (32.0905, 77.7347),
    'Bhuntar':                   (31.876,  77.160),
    'Kasol':                     (32.010,  77.315),
    'Manikaran':                 (32.030,  77.348),
    'Kheerganga':                (32.038,  77.493),
    'Pin Parvati Pass':          (32.070,  77.820),
    'Tirthan Valley':            (31.720,  77.400),
    'Sainj Valley':              (31.770,  77.300),
    'GHNP Core':                 (31.750,  77.500),
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


# ── Satellite imagery ─────────────────────────────────────────────────

def fetch_s2(bbox, width, height, cache_path):
    if os.path.exists(cache_path):
        print(f"  cached: {os.path.basename(cache_path)}")
        return cache_path
    params = (
        f"service=WMS&version=1.1.1&request=GetMap"
        f"&layers=s2cloudless-2024"
        f"&bbox={bbox['lon_min']},{bbox['lat_min']},{bbox['lon_max']},{bbox['lat_max']}"
        f"&srs=EPSG:4326"
        f"&width={width}&height={height}"
        f"&format=image/jpeg"
    )
    url = f"{EOX_WMS}?{params}"
    print(f"  fetching S2 ({width}x{height}) ...")
    req = Request(url, headers={'User-Agent': 'MayaLucIA/0.1'})
    data = urlopen(req).read()
    img = Image.open(BytesIO(data))
    img.save(cache_path, quality=95)
    print(f"  saved: {os.path.basename(cache_path)}")
    return cache_path


# ── OBJ export ────────────────────────────────────────────────────────

def write_obj(filepath, elev, lats, lons, mtl_filename):
    nr, nc = elev.shape
    center_lat = (lats[0] + lats[-1]) / 2
    center_lon = (lons[0] + lons[-1]) / 2

    # Fill NaN
    mask = np.isnan(elev)
    if mask.any():
        _, indices = distance_transform_edt(mask, return_distances=True, return_indices=True)
        elev = elev.copy()
        elev[mask] = elev[tuple(indices[:, mask])]

    print(f"  writing OBJ: {nr}x{nc} = {nr*nc:,} vertices, {2*(nr-1)*(nc-1):,} triangles ...")

    with open(filepath, 'w') as f:
        f.write(f"# Parvati Valley expanded DEM mesh\n")
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

        f.write(f"\n# Texture coordinates\n")
        for r in range(nr):
            v = 1.0 - r / (nr - 1)
            for c in range(nc):
                u = c / (nc - 1)
                f.write(f"vt {u:.6f} {v:.6f}\n")

        f.write(f"\n# Faces\n")
        for r in range(nr - 1):
            for c in range(nc - 1):
                tl = r * nc + c + 1
                tr = r * nc + (c + 1) + 1
                bl = (r + 1) * nc + c + 1
                br = (r + 1) * nc + (c + 1) + 1
                f.write(f"f {tl}/{tl} {bl}/{bl} {tr}/{tr}\n")
                f.write(f"f {tr}/{tr} {bl}/{bl} {br}/{br}\n")

    print(f"  wrote: {os.path.basename(filepath)}")


def write_mtl(filepath, tex_filename):
    with open(filepath, 'w') as f:
        f.write("# Parvati terrain material\n")
        f.write("newmtl terrain\n")
        f.write("Ka 0.2 0.2 0.2\n")
        f.write("Kd 0.8 0.8 0.8\n")
        f.write("Ks 0.0 0.0 0.0\n")
        f.write("d 1.0\n")
        f.write("illum 1\n")
        f.write(f"map_Kd {os.path.basename(tex_filename)}\n")
    print(f"  wrote: {os.path.basename(filepath)}")


# ── Main ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")
    mesh_dir = os.path.join(data_dir, "meshes")
    os.makedirs(mesh_dir, exist_ok=True)

    # 1. Load DEM tiles
    print("Loading DEM tiles...")
    tiles_data = []
    for lat, lon in TILES:
        path = download_tile(lat, lon, data_dir)
        dem = load_hgt(path)
        tiles_data.append((lat, lon, dem))
        print(f"  {lat}N {lon}E: range {np.nanmin(dem):.0f}-{np.nanmax(dem):.0f} m")

    # 2. Stitch and crop to full extent
    print("\nStitching to expanded extent...")
    elev, lats, lons = stitch_and_crop(tiles_data, **EXTENT)
    print(f"  DEM: {elev.shape}, range: {np.nanmin(elev):.0f}-{np.nanmax(elev):.0f} m")
    print(f"  Extent: {EXTENT['lat_min']}-{EXTENT['lat_max']}N, "
          f"{EXTENT['lon_min']}-{EXTENT['lon_max']}E")
    km_ns = (EXTENT['lat_max'] - EXTENT['lat_min']) * 111.32
    km_ew = (EXTENT['lon_max'] - EXTENT['lon_min']) * 111.32 * np.cos(np.radians(31.9))
    print(f"  Size: ~{km_ns:.0f} x {km_ew:.0f} km")

    # 3. Hillshade map
    print("\nRendering hillshade...")
    ls = LightSource(azdeg=315, altdeg=40)
    rgb = ls.shade(elev, cmap=plt.cm.terrain, blend_mode='soft',
                   vert_exag=2, vmin=np.nanmin(elev), vmax=np.nanmax(elev))

    fig, ax = plt.subplots(figsize=(16, 14))
    extent_box = [EXTENT['lon_min'], EXTENT['lon_max'],
                  EXTENT['lat_min'], EXTENT['lat_max']]
    ax.imshow(rgb, extent=extent_box, aspect='auto')

    for name, (lat, lon) in PLACES.items():
        marker = 'r^' if 'Parbat' in name or 'Pass' in name else 'wo'
        size = 10 if 'Parbat' in name else 7
        ax.plot(lon, lat, marker, markersize=size, markeredgecolor='k',
                markeredgewidth=0.5)
        ax.annotate(name.replace('\n', ' '), (lon, lat), fontsize=7,
                    fontweight='bold', color='white', ha='left', va='bottom',
                    xytext=(5, 3), textcoords='offset points',
                    path_effects=[pe.withStroke(linewidth=2, foreground='black')])

    ax.set_xlabel('Longitude (E)')
    ax.set_ylabel('Latitude (N)')
    ax.set_title('Parvati Valley Expanded - GHNP + Khirganga NP + Full Watershed',
                 fontsize=14)

    hs_path = os.path.join(data_dir, 'expanded_hillshade.png')
    fig.savefig(hs_path, dpi=180, bbox_inches='tight')
    print(f"  saved: {hs_path}")

    # 4. Satellite texture
    print("\nFetching satellite texture...")
    tex_path = os.path.join(mesh_dir, 'expanded_texture.jpg')
    fetch_s2(EXTENT, 4096, 4096, tex_path)

    # 5. Satellite + hillshade blend
    print("\nRendering satellite + hillshade blend...")
    sat = np.array(Image.open(tex_path))
    sat_resized = np.array(Image.fromarray(sat).resize(
        (elev.shape[1], elev.shape[0]), Image.LANCZOS))
    sat_float = sat_resized.astype(np.float64) / 255.0
    rgb_shaded = ls.shade_rgb(sat_float, elev, blend_mode='soft', vert_exag=2)

    fig2, ax2 = plt.subplots(figsize=(16, 14))
    ax2.imshow(rgb_shaded, extent=extent_box, aspect='auto')
    ax2.plot(PLACES['Parvati Parbat\n6632 m'][1],
             PLACES['Parvati Parbat\n6632 m'][0],
             'r^', markersize=12, markeredgecolor='white', markeredgewidth=1)
    ax2.set_xlabel('Longitude (E)')
    ax2.set_ylabel('Latitude (N)')
    ax2.set_title('Parvati Valley - Sentinel-2 Cloudless + SRTM Hillshade (Expanded)',
                   fontsize=14)

    sat_path = os.path.join(data_dir, 'expanded_satellite.png')
    fig2.savefig(sat_path, dpi=180, bbox_inches='tight')
    print(f"  saved: {sat_path}")

    # 6. Export OBJ mesh (subsampled for Blender)
    print("\nExporting mesh...")
    step = 5  # subsample factor for ~90x100 km extent
    elev_s = elev[::step, ::step]
    lats_s = lats[::step]
    lons_s = lons[::step]
    print(f"  subsampled x{step}: {elev_s.shape}")

    obj_path = os.path.join(mesh_dir, 'expanded.obj')
    mtl_path = os.path.join(mesh_dir, 'expanded.mtl')
    write_mtl(mtl_path, tex_path)
    write_obj(obj_path, elev_s, lats_s, lons_s, mtl_path)

    nv = elev_s.shape[0] * elev_s.shape[1]
    nf = 2 * (elev_s.shape[0] - 1) * (elev_s.shape[1] - 1)
    size_mb = os.path.getsize(obj_path) / (1024 * 1024)
    print(f"  -> {nv:,} vertices, {nf:,} triangles, {size_mb:.1f} MB")

    plt.show()
    print("\nDone.")
