+++
title = "Mesh Generation: From Elevation to Geometry"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["parbati", "mesh", "3d", "terrain"]
draft = false
+++

A digital elevation model is a grid of numbers. A mesh is geometry that can be rotated, lit, textured, and explored. This stage transforms SRTM grids into OBJ meshes with UV-mapped satellite textures --- ready for import into Blender or any 3D application.

## Mesh Products

| Name | Extent | Resolution | Vertices | Texture |
|------|--------|-----------|----------|---------|
| **Peak** | Parbati Parbat ±10 km | step=3 (~90 m) | ~400K | 2048² Sentinel-2 |
| **Valley** | Bhuntar to Pin Parvati | step=4 (~120 m) | ~300K | 4096×2048 Sentinel-2 |
| **Expanded** | Full GHNP + Khirganga NP | step=6 (~180 m) | ~416K | Bare (vertex colour) |
| **Kullu** | Full Beas drainage | step=8 (~240 m) | ~316K | Bare (vertex colour) |

## Output Format

Each mesh produces three files:
- `.obj` --- vertex positions and UV coordinates
- `.mtl` --- material definition referencing the texture
- `.jpg` --- satellite texture from EOX Sentinel-2 Cloudless WMS

Coordinates are in local meters with 1:1 scale. Vertical exaggeration is applied in Blender, not in the mesh, preserving the true aspect ratio for scientific use.

---

**Source:** [`domains/parbati/parbati_mesh.py`](https://github.com/mayalucia/parbati) (267 lines), [`parbati_expanded_mesh.py`](https://github.com/mayalucia/parbati) (306 lines)
