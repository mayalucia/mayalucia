#!/usr/bin/env python3
"""
Download SRTM 1-arc-second DEM tiles for Himachal Pradesh.

12 tiles covering 30-33N, 75-79E (~311 MB uncompressed).
Downloads from AWS/Mapzen (public, no auth).

Usage:
    python3 experiments/01-micro-data-centers/fetch_dem.py
"""

import gzip
import os
import numpy as np
from urllib.request import urlopen

SRTM_SIZE = 3601
VOID = -32768
SRTM_BASE = "https://elevation-tiles-prod.s3.amazonaws.com/skadi"

# Full Himachal Pradesh coverage: 30-33N, 75-79E
TILES = [(lat, lon)
         for lat in range(30, 33)
         for lon in range(75, 79)]


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
    """Stitch tiles into a single array. tiles_data: list of (sw_lat, sw_lon, dem)."""
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


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Check for tiles already cached in parbati/data/
    parbati_data = os.path.join(here, "..", "..", "parbati", "data")

    print(f"Downloading {len(TILES)} SRTM tiles for Himachal Pradesh...")
    print(f"Coverage: 30-33N, 75-79E\n")

    tiles_data = []
    for lat, lon in TILES:
        _, name = srtm_url(lat, lon)
        local_path = os.path.join(data_dir, f"{name}.hgt")

        # Reuse from parbati/data/ if available
        parbati_path = os.path.join(parbati_data, f"{name}.hgt")
        if not os.path.exists(local_path) and os.path.exists(parbati_path):
            print(f"  linking {name} from parbati/data/")
            os.symlink(os.path.abspath(parbati_path), local_path)

        path = download_tile(lat, lon, data_dir)
        if path:
            dem = load_hgt(path)
            tiles_data.append((lat, lon, dem))
            print(f"    {name}: {np.nanmin(dem):.0f}–{np.nanmax(dem):.0f} m")

    print(f"\nLoaded {len(tiles_data)}/{len(TILES)} tiles.")

    # Stitch into single array and save as compressed numpy
    print("\nStitching into single DEM...")
    full, lats, lons = stitch_tiles(tiles_data)
    print(f"  Shape: {full.shape}")
    print(f"  Elevation range: {np.nanmin(full):.0f}–{np.nanmax(full):.0f} m")
    print(f"  NaN fraction: {np.isnan(full).sum() / full.size:.4f}")

    npz_path = os.path.join(data_dir, "himachal_dem.npz")
    np.savez_compressed(npz_path, elevation=full, lats=lats, lons=lons)
    size_mb = os.path.getsize(npz_path) / (1024 * 1024)
    print(f"  Saved: {npz_path} ({size_mb:.1f} MB)")
    print("\nDone.")
