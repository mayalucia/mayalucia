+++
title = "DEM Processing: Reading the Earth's Surface"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["parbati", "dem", "elevation", "data"]
draft = false
+++

Everything starts with elevation. The SRTM (Shuttle Radar Topography Mission) provides 1-arc-second (~30 m) digital elevation models covering the entire Parvati Valley and surrounding ranges. These are the raw material from which terrain meshes, hillshades, and satellite-textured landscapes are built.

## Data Source

SRTM tiles from AWS Mapzen elevation tiles (public, no authentication):
- **N31E077** and **N32E077** --- two tiles covering the Parvati Valley extent
- 3601 × 3601 pixels per tile, signed 16-bit big-endian
- ~30 m horizontal resolution, ~1 m vertical accuracy

## Processing Pipeline

1. **Download** --- fetch `.hgt.gz` tiles from S3
2. **Parse** --- load as NumPy float32, handle voids (NaN)
3. **Stitch** --- combine adjacent tiles into continuous elevation grids
4. **Subsample** --- reduce resolution for mesh generation (step=3 to step=8)
5. **Hillshade** --- compute synthetic illumination for 2D visualisation
6. **Satellite texture** --- fetch Sentinel-2 Cloudless composite from EOX WMS

The pipeline covers extents ranging from the Parbati Parbat peak (±0.10°, ~11 km) to the full Kullu district (1.3° × 1.2°, ~145 km).

---

**Source:** [`domains/parbati/parbati_dem.py`](https://github.com/mayalucia/parbati) (169 lines), [`parbati_textured.py`](https://github.com/mayalucia/parbati) (261 lines)
