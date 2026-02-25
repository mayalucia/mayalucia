+++
title = "Blender Visualisation"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["parbati", "blender", "3d", "visualisation"]
draft = false
+++

Blender is the workbench where terrain meshes become explorable landscapes. The Python scripts automate the import pipeline: mesh loading, camera setup, landmark annotation, elevation banding, and viewport configuration.

## What the Scripts Do

| Script | Purpose |
|--------|---------|
| `blender_5_import.py` | Minimal: import peak mesh, set viewport |
| `blender_5_annotated.py` | Full: import + labeled empties + 3D text + vertex colours |
| `blender_5_expanded.py` | Import expanded valley mesh (larger scene) |
| `blender_setup.py` | Post-import configuration (after manual import) |
| `kullu/kullu_blender.py` | Kullu district with 16 annotated landmarks |

## Landmark Annotations

Empties (point objects) mark key features:
- **Peaks:** Parbati Parbat (6632 m), Hanuman Tibba (5932 m), Deo Tibba (6001 m), Indrasan (6221 m)
- **Settlements:** Bhuntar, Kasol, Manikaran, Kheerganga, Manali, Kullu, Naggar
- **Passes:** Pin Parvati Pass (~5300 m), Rohtang Pass
- **Protected areas:** GHNP core, Khirganga NP

Each empty is placed at the terrain surface elevation via raycast, ensuring accurate 3D positioning.

---

**Source:** [`domains/parbati/blender_5_annotated.py`](https://github.com/mayalucia/parbati) (276 lines), [`blender_5_import.py`](https://github.com/mayalucia/parbati) (36 lines), [`kullu/kullu_blender.py`](https://github.com/mayalucia/parbati) (348 lines)
