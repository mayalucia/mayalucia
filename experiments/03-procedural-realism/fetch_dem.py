# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26", "matplotlib>=3.9"]
# ///
"""
Experiment 03 — Procedural Realism
Fetch SRTM DEM tile for the Thalpan / Indus gorge area and extract
a cross-section transect.

Thalpan petroglyph site: ~35.62°N, 74.60°E
The Indus flows roughly SSE→NNW here, so a transect perpendicular
to the river runs roughly ENE→WSW.

SRTM tile: N35E074 (1°×1° tile, 30m resolution → 3601×3601 int16)
Source: ViewFinder Panoramas (no auth required for 3-arcsec / 90m)
        or USGS EarthExplorer (requires free account for 1-arcsec / 30m)

We'll try 90m (3-arcsec) first — the gorge is ~2km wide at Thalpan,
so 90m gives us ~22 samples across the gorge. Enough for a profile.
"""

from pathlib import Path
import zipfile
import io
import urllib.request
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
DEM_CACHE = OUT / "dem_cache"
DEM_CACHE.mkdir(exist_ok=True)

# ── SRTM tile coordinates ───────────────────────────────────────────
# ViewFinder Panoramas 3-arcsec (90m) tiles
# Coverage area H (Central Asia) includes N35E074
# URL pattern: http://viewfinderpanoramas.org/dem3/H44.zip
# H44 contains tiles for approximately 32-40N, 72-78E

TILE_NAME = "N35E074"
# 3-arcsec tiles are 1201×1201 (90m resolution)
TILE_SIZE_3AS = 1201
# 1-arcsec tiles are 3601×3601 (30m resolution)
TILE_SIZE_1AS = 3601


def load_hgt(hgt_path, tile_size=TILE_SIZE_3AS):
    """Load a .hgt SRTM file as a numpy array."""
    data = np.fromfile(hgt_path, dtype=">i2")
    return data.reshape((tile_size, tile_size))


def latlon_to_pixel(lat, lon, tile_lat=35, tile_lon=74, tile_size=TILE_SIZE_3AS):
    """Convert lat/lon to pixel coordinates within the tile."""
    # SRTM tiles: row 0 = north edge, col 0 = west edge
    row = int((tile_lat + 1 - lat) * (tile_size - 1))
    col = int((lon - tile_lon) * (tile_size - 1))
    return row, col


def extract_transect(dem, lat_center, lon_center, bearing_deg, length_km, tile_size=TILE_SIZE_3AS):
    """
    Extract an elevation transect across the terrain.

    bearing_deg: compass bearing of the transect (0=N, 90=E)
    length_km: total length of the transect
    Returns: (distances_km, elevations_m)
    """
    # Approximate degrees per km at this latitude
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * np.cos(np.radians(lat_center))

    bearing_rad = np.radians(bearing_deg)
    half_len = length_km / 2.0

    n_samples = 200
    distances = np.linspace(-half_len, half_len, n_samples)
    elevations = np.zeros(n_samples)

    for i, d in enumerate(distances):
        # Offset in degrees
        dlat = (d * np.cos(bearing_rad)) / km_per_deg_lat
        dlon = (d * np.sin(bearing_rad)) / km_per_deg_lon

        lat = lat_center + dlat
        lon = lon_center + dlon

        row, col = latlon_to_pixel(lat, lon, tile_size=tile_size)
        row = np.clip(row, 0, tile_size - 1)
        col = np.clip(col, 0, tile_size - 1)

        elevations[i] = dem[row, col]

    return distances, elevations


def plot_transect(distances, elevations, title, out_path):
    """Plot the elevation transect."""
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.fill_between(distances, elevations, min(elevations) - 50,
                    color="#4A4845", alpha=0.6)
    ax.plot(distances, elevations, color="#C8C0B0", lw=1.5)

    # Mark the river (lowest point)
    river_idx = np.argmin(elevations)
    ax.axvline(distances[river_idx], color="#5888A8", lw=1, ls="--", alpha=0.6)
    ax.annotate(f"Indus ~{elevations[river_idx]:.0f}m",
                (distances[river_idx], elevations[river_idx]),
                textcoords="offset points", xytext=(10, 15),
                color="#5888A8", fontsize=9)

    ax.set_xlabel("Distance along transect (km)")
    ax.set_ylabel("Elevation (m)")
    ax.set_title(title)
    ax.set_facecolor("#1A1816")
    fig.patch.set_facecolor("#1A1816")
    ax.tick_params(colors="#C8C0B0")
    ax.xaxis.label.set_color("#C8C0B0")
    ax.yaxis.label.set_color("#C8C0B0")
    ax.title.set_color("#C8C0B0")
    for spine in ax.spines.values():
        spine.set_color("#4A4845")

    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  → {out_path}")


def main():
    hgt_path = DEM_CACHE / f"{TILE_NAME}.hgt"

    if not hgt_path.exists():
        # Try to download from ViewFinder Panoramas
        # The 3-arcsec tiles for this region are in area "H"
        # We'll try direct download of the specific tile
        url = f"https://viewfinderpanoramas.org/dem3/{TILE_NAME}.zip"
        print(f"Downloading {url} ...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                zip_data = resp.read()
            with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
                for name in zf.namelist():
                    if name.upper().endswith(".HGT"):
                        with open(hgt_path, "wb") as f:
                            f.write(zf.read(name))
                        print(f"  Extracted {name} → {hgt_path}")
                        break
        except Exception as e:
            print(f"  Download failed: {e}")
            print(f"  Manual download: get {TILE_NAME}.hgt and place in {DEM_CACHE}/")
            print(f"  Sources: https://viewfinderpanoramas.org/dem3.html")
            print(f"           https://dwtkns.com/srtm30m/")
            return

    # Detect tile resolution from file size
    file_size = hgt_path.stat().st_size
    if file_size >= TILE_SIZE_1AS * TILE_SIZE_1AS * 2:
        tile_size = TILE_SIZE_1AS
        res_label = "1-arcsec (30m)"
    else:
        tile_size = TILE_SIZE_3AS
        res_label = "3-arcsec (90m)"

    print(f"Loading {hgt_path.name} ({res_label}, {tile_size}×{tile_size})...")
    dem = load_hgt(hgt_path, tile_size)
    print(f"  Elevation range: {dem.min()}m – {dem.max()}m")

    # ── Transects ────────────────────────────────────────────────────
    # Thalpan petroglyph site
    lat, lon = 35.62, 74.60

    # Transect 1: ENE–WSW (perpendicular to Indus, ~bearing 70°)
    print("\nTransect 1: ENE–WSW across the gorge at Thalpan")
    d1, e1 = extract_transect(dem, lat, lon, bearing_deg=70, length_km=12,
                               tile_size=tile_size)
    plot_transect(d1, e1,
                  "Thalpan — ENE→WSW transect (⊥ to Indus)",
                  OUT / "output" / "transect-thalpan-ene.png")

    # Transect 2: N–S (shows the gorge depth against Nanga Parbat)
    print("Transect 2: N–S from the river toward Nanga Parbat")
    d2, e2 = extract_transect(dem, lat, lon, bearing_deg=0, length_km=20,
                               tile_size=tile_size)
    plot_transect(d2, e2,
                  "Thalpan — N→S transect (toward Nanga Parbat)",
                  OUT / "output" / "transect-thalpan-ns.png")

    # ── 2D DEM patch ──────────────────────────────────────────────────
    # Extract a rectangular patch around Thalpan for lateral wall texture.
    # ~10km ENE–WSW × ~8km along the gorge (NNW–SSE)
    print("\nExtracting 2D DEM patch around Thalpan...")
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * np.cos(np.radians(lat))

    patch_half_x = 5.0  # km ENE–WSW
    patch_half_y = 4.0  # km NNW–SSE (along gorge)

    dlat = patch_half_y / km_per_deg_lat
    dlon = patch_half_x / km_per_deg_lon

    # Pixel bounds in the tile
    row_n, col_w = latlon_to_pixel(lat + dlat, lon - dlon, tile_size=tile_size)
    row_s, col_e = latlon_to_pixel(lat - dlat, lon + dlon, tile_size=tile_size)
    row_n = max(0, row_n)
    row_s = min(tile_size - 1, row_s)
    col_w = max(0, col_w)
    col_e = min(tile_size - 1, col_e)

    dem_patch = dem[row_n:row_s+1, col_w:col_e+1].astype(np.float64)
    print(f"  Patch shape: {dem_patch.shape} ({dem_patch.shape[1]*90:.0f}m × {dem_patch.shape[0]*90:.0f}m at 90m)")
    print(f"  Elevation range: {dem_patch.min():.0f}m – {dem_patch.max():.0f}m")

    # Save raw transect data and DEM patch for the procedural renderer
    np.savez(OUT / "output" / "transects.npz",
             d_ene=d1, e_ene=e1,
             d_ns=d2, e_ns=e2,
             dem_patch=dem_patch,
             lat=lat, lon=lon)
    print(f"\n  Raw data → {OUT / 'output' / 'transects.npz'}")


if __name__ == "__main__":
    main()
