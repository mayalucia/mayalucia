#!/usr/bin/env python3
"""
Extract river network from SRTM DEM using D8 flow routing.

Reads the stitched himachal_dem.npz, computes:
  1. Pit-filled DEM (simple priority-flood)
  2. D8 flow direction
  3. Flow accumulation (catchment area in pixels)
  4. River network as polylines at multiple thresholds

Outputs GeoJSON of river segments for the interactive map.

This is a from-scratch implementation — no GDAL, no rasterio, just
numpy and scipy. The DEM is 10801x14401 (~155M pixels) so we work
at reduced resolution for the flow routing and full resolution for
the final rendering.

Usage:
    .venv/bin/python3 experiments/01-micro-data-centers/extract_rivers.py
"""

import os
import json
import numpy as np
from scipy.ndimage import uniform_filter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# ── D8 flow direction ─────────────────────────────────────────────────
# 8 neighbors: E, SE, S, SW, W, NW, N, NE
DR = np.array([0,  1,  1,  1,  0, -1, -1, -1], dtype=np.int32)
DC = np.array([1,  1,  0, -1, -1, -1,  0,  1], dtype=np.int32)
# Distance weights (diagonal = sqrt(2))
DIST = np.array([1.0, 1.414, 1.0, 1.414, 1.0, 1.414, 1.0, 1.414])


def fill_pits(dem):
    """Simple iterative pit-filling. Not optimal but correct for our scale."""
    print("  Filling pits...")
    filled = dem.copy()
    nr, nc = filled.shape
    changed = True
    iteration = 0
    while changed:
        changed = False
        iteration += 1
        for r in range(1, nr - 1):
            for c in range(1, nc - 1):
                if np.isnan(filled[r, c]):
                    continue
                z = filled[r, c]
                # Check if any neighbor is lower
                has_lower = False
                min_neighbor = np.inf
                for d in range(8):
                    nr2, nc2 = r + DR[d], c + DC[d]
                    nz = filled[nr2, nc2]
                    if not np.isnan(nz):
                        if nz < z:
                            has_lower = True
                            break
                        min_neighbor = min(min_neighbor, nz)
                if not has_lower and min_neighbor < np.inf:
                    filled[r, c] = min_neighbor + 0.001
                    changed = True
        if iteration > 100:
            break
        if iteration % 10 == 0:
            print(f"    iteration {iteration}")
    print(f"    {iteration} iterations")
    return filled


def fill_pits_fast(dem):
    """
    Priority-flood pit filling using numpy operations.
    Works by iteratively raising pit cells to their lowest neighbor + epsilon.
    """
    print("  Fast pit filling...")
    filled = dem.copy()
    nr, nc = filled.shape

    for iteration in range(200):
        # For each cell, find minimum neighbor
        min_nb = np.full_like(filled, np.inf)
        for d in range(8):
            shifted = np.full_like(filled, np.inf)
            r_src = slice(max(0, -DR[d]), nr + min(0, -DR[d]))
            c_src = slice(max(0, -DC[d]), nc + min(0, -DC[d]))
            r_dst = slice(max(0, DR[d]), nr + min(0, DR[d]))
            c_dst = slice(max(0, DC[d]), nc + min(0, DC[d]))
            shifted[r_dst, c_dst] = filled[r_src, c_src]
            min_nb = np.minimum(min_nb, shifted)

        # A cell is a pit if it's lower than or equal to all neighbors
        # but not on the boundary and not NaN
        is_pit = (filled <= min_nb) & ~np.isnan(filled)
        # Exclude boundary
        is_pit[0, :] = False
        is_pit[-1, :] = False
        is_pit[:, 0] = False
        is_pit[:, -1] = False
        # Exclude cells that already have a lower neighbor (not pits)
        has_lower = np.zeros_like(filled, dtype=bool)
        for d in range(8):
            shifted = np.full_like(filled, np.inf)
            r_src = slice(max(0, -DR[d]), nr + min(0, -DR[d]))
            c_src = slice(max(0, -DC[d]), nc + min(0, -DC[d]))
            r_dst = slice(max(0, DR[d]), nr + min(0, DR[d]))
            c_dst = slice(max(0, DC[d]), nc + min(0, DC[d]))
            shifted[r_dst, c_dst] = filled[r_src, c_src]
            has_lower |= (shifted < filled)
        is_pit &= ~has_lower

        n_pits = is_pit.sum()
        if n_pits == 0:
            print(f"    converged at iteration {iteration}")
            break
        filled[is_pit] = min_nb[is_pit] + 0.001
        if iteration % 20 == 0:
            print(f"    iteration {iteration}: {n_pits} pits remaining")

    return filled


def compute_flow_direction(dem):
    """D8 flow direction: for each cell, index of steepest descent neighbor."""
    print("  Computing D8 flow direction...")
    nr, nc = dem.shape
    flowdir = np.full((nr, nc), -1, dtype=np.int8)

    for d in range(8):
        # Compute slope to neighbor d
        slope = np.full((nr, nc), -np.inf)
        r_src = slice(max(0, -DR[d]), nr + min(0, -DR[d]))
        c_src = slice(max(0, -DC[d]), nc + min(0, -DC[d]))
        r_dst = slice(max(0, DR[d]), nr + min(0, DR[d]))
        c_dst = slice(max(0, DC[d]), nc + min(0, DC[d]))

        drop = dem[r_src, c_src] - dem[r_dst, c_dst]  # at source position
        slope_vals = drop / DIST[d]

        # Compare with current best
        slope_full = np.full((nr, nc), -np.inf)
        slope_full[r_src, c_src] = slope_vals

        # Current best slope
        best = np.full((nr, nc), -np.inf)
        for d2 in range(d):
            r_src2 = slice(max(0, -DR[d2]), nr + min(0, -DR[d2]))
            c_src2 = slice(max(0, -DC[d2]), nc + min(0, -DC[d2]))
            r_dst2 = slice(max(0, DR[d2]), nr + min(0, DR[d2]))
            c_dst2 = slice(max(0, DC[d2]), nc + min(0, DC[d2]))
            drop2 = dem[r_src2, c_src2] - dem[r_dst2, c_dst2]
            s2 = np.full((nr, nc), -np.inf)
            s2[r_src2, c_src2] = drop2 / DIST[d2]
            best = np.maximum(best, s2)

    # Simpler approach: compute all 8 slopes, take argmax
    slopes = np.full((8, nr, nc), -np.inf)
    for d in range(8):
        r_src = slice(max(0, -DR[d]), nr + min(0, -DR[d]))
        c_src = slice(max(0, -DC[d]), nc + min(0, -DC[d]))
        r_dst = slice(max(0, DR[d]), nr + min(0, DR[d]))
        c_dst = slice(max(0, DC[d]), nc + min(0, DC[d]))
        drop = np.zeros((nr, nc))
        drop[r_src, c_src] = dem[r_src, c_src] - dem[r_dst, c_dst]
        slopes[d, r_src, c_src] = drop[r_src, c_src] / DIST[d]

    flowdir = np.argmax(slopes, axis=0).astype(np.int8)
    # Mark flat areas (no positive slope anywhere)
    max_slope = np.max(slopes, axis=0)
    flowdir[max_slope <= 0] = -1
    flowdir[np.isnan(dem)] = -1

    return flowdir


def compute_flow_accumulation(flowdir):
    """
    Flow accumulation by topological sort.
    Each cell contributes 1 + its accumulated upstream area to its downstream cell.
    """
    print("  Computing flow accumulation...")
    nr, nc = flowdir.shape
    acc = np.ones((nr, nc), dtype=np.float64)

    # Count incoming flows for each cell
    n_incoming = np.zeros((nr, nc), dtype=np.int32)
    for d in range(8):
        # Cells flowing in direction d: their target is (r+DR[d], c+DC[d])
        mask = (flowdir == d)
        r_src, c_src = np.where(mask)
        r_dst = r_src + DR[d]
        c_dst = c_src + DC[d]
        valid = (r_dst >= 0) & (r_dst < nr) & (c_dst >= 0) & (c_dst < nc)
        np.add.at(n_incoming, (r_dst[valid], c_dst[valid]), 1)

    # Start from cells with no incoming flow (headwaters)
    queue_r, queue_c = np.where(n_incoming == 0)
    queue = list(zip(queue_r.tolist(), queue_c.tolist()))

    processed = 0
    total = nr * nc
    while queue:
        batch_r = []
        batch_c = []
        next_queue = []

        for r, c in queue:
            d = flowdir[r, c]
            if d < 0:
                continue
            r2 = r + DR[d]
            c2 = c + DC[d]
            if 0 <= r2 < nr and 0 <= c2 < nc:
                acc[r2, c2] += acc[r, c]
                n_incoming[r2, c2] -= 1
                if n_incoming[r2, c2] == 0:
                    next_queue.append((r2, c2))

        processed += len(queue)
        if processed % 5000000 == 0:
            print(f"    processed {processed}/{total} cells "
                  f"({100*processed/total:.0f}%)")

        queue = next_queue

    print(f"    done ({processed} cells)")
    return acc


def extract_river_segments(acc, lats, lons, threshold):
    """
    Extract river segments as polylines from flow accumulation.
    Returns list of (coordinates, max_accumulation) tuples.
    """
    print(f"  Extracting rivers (threshold={threshold} pixels)...")
    river_mask = acc >= threshold
    nr, nc = acc.shape

    # Trace connected river pixels into polylines
    # Simple approach: convert to coordinates
    rows, cols = np.where(river_mask)
    coords = []
    for r, c in zip(rows, cols):
        lat = lats[r]
        lon = lons[c]
        a = acc[r, c]
        coords.append((lon, lat, a))

    print(f"    {len(coords)} river pixels")
    return coords


def river_pixels_to_geojson(acc, flowdir, lats, lons, threshold):
    """
    Trace rivers from flow accumulation into connected polylines.
    Returns GeoJSON FeatureCollection with line width proportional to catchment.
    """
    print(f"  Tracing river polylines (threshold={threshold})...")
    nr, nc = acc.shape
    river_mask = acc >= threshold

    # Width classes based on accumulation
    # Higher accumulation = wider river
    width_thresholds = [
        (threshold * 100, 5, 'major'),      # major rivers
        (threshold * 20,  3, 'medium'),      # medium rivers
        (threshold * 5,   2, 'tributary'),   # tributaries
        (threshold,       1, 'stream'),      # small streams
    ]

    features = []

    # For each river pixel, follow flow downstream to build segments
    visited = np.zeros((nr, nc), dtype=bool)

    # Start from headwater river pixels (river pixels whose upstream
    # neighbors are not river pixels, or have lower accumulation)
    starts = []
    for r, c in zip(*np.where(river_mask & ~visited)):
        # Check if any upstream neighbor flows into this cell and is also a river
        is_headwater = True
        for d in range(8):
            r2 = r - DR[d]  # upstream cell
            c2 = c - DC[d]
            if 0 <= r2 < nr and 0 <= c2 < nc:
                if river_mask[r2, c2] and flowdir[r2, c2] == d:
                    # This cell has an upstream river neighbor
                    is_headwater = False
                    break
        if is_headwater:
            starts.append((r, c))

    print(f"    {len(starts)} headwater points")

    for start_r, start_c in starts:
        r, c = start_r, start_c
        line_coords = []
        line_acc = []

        while 0 <= r < nr and 0 <= c < nc and river_mask[r, c] and not visited[r, c]:
            visited[r, c] = True
            line_coords.append([float(lons[c]), float(lats[r])])
            line_acc.append(float(acc[r, c]))

            d = flowdir[r, c]
            if d < 0:
                break
            r = r + DR[d]
            c = c + DC[d]

        # Continue into already-visited territory for one more point
        # (to connect segments)
        if 0 <= r < nr and 0 <= c < nc and river_mask[r, c]:
            line_coords.append([float(lons[c]), float(lats[r])])
            line_acc.append(float(acc[r, c]))

        if len(line_coords) >= 2:
            max_acc = max(line_acc)
            # Classify width
            width = 1
            river_class = 'stream'
            for thresh, w, cls in width_thresholds:
                if max_acc >= thresh:
                    width = w
                    river_class = cls
                    break

            feature = {
                "type": "Feature",
                "properties": {
                    "max_accumulation": max_acc,
                    "width": width,
                    "class": river_class,
                    "n_pixels": len(line_coords),
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": line_coords,
                }
            }
            features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }
    print(f"    {len(features)} river segments")
    return geojson


# ── Main ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Load stitched DEM
    print("Loading DEM...")
    data = np.load(os.path.join(DATA, "himachal_dem.npz"))
    elev_full = data['elevation']
    lats_full = data['lats']
    lons_full = data['lons']
    print(f"  Full DEM: {elev_full.shape}")

    # Subsample for flow routing — step=3 gives ~90m resolution
    # (~3600x4800 = 17M pixels, manageable)
    STEP = 3
    elev = elev_full[::STEP, ::STEP].copy()
    lats = lats_full[::STEP]
    lons = lons_full[::STEP]
    print(f"  Subsampled x{STEP}: {elev.shape} ({elev.size/1e6:.1f}M pixels)")

    # Fill NaN with local minimum (edges of coverage)
    nan_mask = np.isnan(elev)
    if nan_mask.any():
        print(f"  Filling {nan_mask.sum()} NaN pixels...")
        elev[nan_mask] = 0

    # Fill pits
    elev = fill_pits_fast(elev)

    # Flow direction
    flowdir = compute_flow_direction(elev)

    # Flow accumulation
    acc = compute_flow_accumulation(flowdir)

    # Save flow accumulation for later use
    np.savez_compressed(
        os.path.join(DATA, "flow_accumulation.npz"),
        accumulation=acc,
        flowdir=flowdir,
        lats=lats,
        lons=lons,
        step=STEP,
    )
    print(f"  Saved flow_accumulation.npz")

    # Extract rivers at multiple thresholds
    # At 90m resolution, 1 pixel ≈ 0.008 km²
    # threshold=500 → catchment > ~4 km² (small streams)
    # threshold=2000 → catchment > ~16 km² (significant tributaries)
    # threshold=10000 → catchment > ~80 km² (major rivers)

    # We want all visible tributaries
    geojson = river_pixels_to_geojson(acc, flowdir, lats, lons, threshold=500)

    # Save
    geojson_path = os.path.join(DATA, "rivers.geojson")
    with open(geojson_path, 'w') as f:
        json.dump(geojson, f)
    size_mb = os.path.getsize(geojson_path) / (1024 * 1024)
    print(f"  Saved {geojson_path} ({size_mb:.1f} MB)")

    # Summary stats
    total_river_pixels = sum(f['properties']['n_pixels'] for f in geojson['features'])
    by_class = {}
    for f in geojson['features']:
        cls = f['properties']['class']
        by_class[cls] = by_class.get(cls, 0) + f['properties']['n_pixels']
    print(f"\n  River network summary:")
    print(f"    Total segments: {len(geojson['features'])}")
    print(f"    Total river pixels: {total_river_pixels}")
    km_per_pixel = 0.090  # ~90m at this resolution
    print(f"    Approximate total river length: {total_river_pixels * km_per_pixel:.0f} km")
    for cls, n in sorted(by_class.items(), key=lambda x: -x[1]):
        print(f"    {cls}: {n} pixels (~{n * km_per_pixel:.0f} km)")

    print("\nDone.")
