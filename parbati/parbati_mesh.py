#!/usr/bin/env python3
"""
Export Parvati Valley and Peak as textured OBJ meshes for Blender.

Produces OBJ + MTL + texture JPEG that Blender opens directly.
Coordinates converted to local meters (origin at center of extent).

Usage:
    vload py310
    python3 parbati/parbati_mesh.py

Then in Blender: File → Import → Wavefront (.obj)

Usage notes for Blender:
  - The mesh is in real-world meters at 1:1 scale
  - The peak mesh (~240×240 vertices) is lightweight
  - The valley mesh is subsampled to ~650×700 vertices
  - Vertical exaggeration can be applied in Blender via scale Z
  - The satellite texture is UV-mapped; Blender should pick it up
    automatically from the MTL file
"""

import gzip
import os
import numpy as np
from PIL import Image
from io import BytesIO
from urllib.request import urlopen, Request

# ── Configuration ──────────────────────────────────────────────────────

SRTM_SIZE = 3601
VOID = -32768
SRTM_BASE = "https://elevation-tiles-prod.s3.amazonaws.com/skadi"
EOX_WMS = "https://tiles.maps.eox.at/wms"

TILES = [(32, 77), (31, 77)]

# Two extents to export
EXTENTS = {
    'peak': dict(
        lat_min=31.99, lat_max=32.19, lon_min=77.63, lon_max=77.83,
        step=3,       # subsample factor
        tex_w=2048, tex_h=2048,
    ),
    'valley': dict(
        lat_min=31.84, lat_max=32.20, lon_min=77.10, lon_max=77.88,
        step=4,       # heavier subsampling for the larger extent
        tex_w=4096, tex_h=2048,
    ),
}

# Meters per degree at this latitude
DEG_LAT_M = 111320.0
DEG_LON_M = 111320.0 * np.cos(np.radians(32.05))

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
        return path
    print(f"  downloading {name} ...")
    raw = gzip.decompress(urlopen(url).read())
    with open(path, 'wb') as f:
        f.write(raw)
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
    print(f"  fetching S2 ({width}×{height}) ...")
    req = Request(url, headers={'User-Agent': 'MayaLucIA/0.1'})
    data = urlopen(req).read()
    img = Image.open(BytesIO(data))
    img.save(cache_path, quality=95)
    print(f"  saved: {os.path.basename(cache_path)}")
    return cache_path

# ── OBJ export ────────────────────────────────────────────────────────

def write_obj(filepath, elev, lats, lons, tex_filename, mtl_filename):
    """Write OBJ mesh from elevation grid with UV texture mapping.

    Coordinate system: X = east (meters), Y = north (meters), Z = up (meters).
    Origin at center of extent.
    """
    nr, nc = elev.shape
    center_lat = (lats[0] + lats[-1]) / 2
    center_lon = (lons[0] + lons[-1]) / 2

    # Fill NaN with nearest valid elevation (Blender doesn't like NaN)
    from scipy.ndimage import distance_transform_edt
    mask = np.isnan(elev)
    if mask.any():
        _, indices = distance_transform_edt(mask, return_distances=True, return_indices=True)
        elev = elev.copy()
        elev[mask] = elev[tuple(indices[:, mask])]

    obj_name = os.path.splitext(os.path.basename(filepath))[0]

    print(f"  writing OBJ: {nr}×{nc} = {nr*nc} vertices, {2*(nr-1)*(nc-1)} triangles ...")

    with open(filepath, 'w') as f:
        f.write(f"# Parvati Valley DEM mesh\n")
        f.write(f"# {nr}×{nc} grid, {nr*nc} vertices\n")
        f.write(f"mtllib {os.path.basename(mtl_filename)}\n")
        f.write(f"usemtl terrain\n\n")

        # Vertices: convert lat/lon to local meters
        for r in range(nr):
            lat = lats[r]
            for c in range(nc):
                lon = lons[c]
                x = (lon - center_lon) * DEG_LON_M
                y = (lat - center_lat) * DEG_LAT_M
                z = elev[r, c]
                f.write(f"v {x:.1f} {y:.1f} {z:.1f}\n")

        f.write(f"\n# Texture coordinates\n")
        # UVs: row 0 = north = top of image (v=1), last row = south (v=0)
        for r in range(nr):
            v = 1.0 - r / (nr - 1)
            for c in range(nc):
                u = c / (nc - 1)
                f.write(f"vt {u:.6f} {v:.6f}\n")

        f.write(f"\n# Faces (triangulated quads)\n")
        # Faces: each quad → 2 triangles
        # Vertex indices are 1-based in OBJ
        for r in range(nr - 1):
            for c in range(nc - 1):
                # Four corners of the quad
                tl = r * nc + c + 1           # top-left
                tr = r * nc + (c + 1) + 1     # top-right
                bl = (r + 1) * nc + c + 1     # bottom-left
                br = (r + 1) * nc + (c + 1) + 1  # bottom-right
                # Triangle 1: tl-bl-tr
                f.write(f"f {tl}/{tl} {bl}/{bl} {tr}/{tr}\n")
                # Triangle 2: tr-bl-br
                f.write(f"f {tr}/{tr} {bl}/{bl} {br}/{br}\n")

    print(f"  wrote: {os.path.basename(filepath)}")


def write_mtl(filepath, tex_filename):
    """Write MTL material file referencing texture."""
    with open(filepath, 'w') as f:
        f.write("# Parvati terrain material\n")
        f.write("newmtl terrain\n")
        f.write("Ka 0.2 0.2 0.2\n")      # ambient
        f.write("Kd 0.8 0.8 0.8\n")      # diffuse
        f.write("Ks 0.0 0.0 0.0\n")      # no specular
        f.write("d 1.0\n")                # opaque
        f.write("illum 1\n")              # diffuse illumination
        f.write(f"map_Kd {os.path.basename(tex_filename)}\n")
    print(f"  wrote: {os.path.basename(filepath)}")

# ── Main ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")
    mesh_dir = os.path.join(data_dir, "meshes")
    os.makedirs(mesh_dir, exist_ok=True)

    # Load DEM tiles
    print("Loading DEM tiles...")
    tiles_data = []
    for lat, lon in TILES:
        path = download_tile(lat, lon, data_dir)
        tiles_data.append((lat, lon, load_hgt(path)))

    for name, ext in EXTENTS.items():
        print(f"\n── {name} mesh ──")

        # Crop DEM
        elev, lats, lons = stitch_and_crop(
            tiles_data, ext['lat_min'], ext['lat_max'],
            ext['lon_min'], ext['lon_max'])
        print(f"  DEM: {elev.shape}, {np.nanmin(elev):.0f}–{np.nanmax(elev):.0f} m")

        # Subsample
        step = ext['step']
        elev_s = elev[::step, ::step]
        lats_s = lats[::step]
        lons_s = lons[::step]
        print(f"  subsampled ×{step}: {elev_s.shape}")

        # Fetch texture
        tex_path = os.path.join(mesh_dir, f"{name}_texture.jpg")
        fetch_s2(ext, ext['tex_w'], ext['tex_h'], tex_path)

        # Write OBJ + MTL
        obj_path = os.path.join(mesh_dir, f"{name}.obj")
        mtl_path = os.path.join(mesh_dir, f"{name}.mtl")
        write_mtl(mtl_path, tex_path)
        write_obj(obj_path, elev_s, lats_s, lons_s, tex_path, mtl_path)

        # Summary
        nv = elev_s.shape[0] * elev_s.shape[1]
        nf = 2 * (elev_s.shape[0] - 1) * (elev_s.shape[1] - 1)
        size_mb = os.path.getsize(obj_path) / (1024 * 1024)
        print(f"  → {nv:,} vertices, {nf:,} triangles, {size_mb:.1f} MB")

    print(f"\nMesh files in: {mesh_dir}/")
    print("Open in Blender: File → Import → Wavefront (.obj)")
    print("  - Texture should load automatically via MTL")
    print("  - For vertical exaggeration: S → Z → type scale factor")
    print("Done.")
