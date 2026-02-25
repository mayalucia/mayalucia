+++
title = "Anatomy and Volumetric Atlas"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["bravli", "anatomy", "atlas", "lesson"]
draft = false
+++

The atlas is where abstract connectivity meets tangible space --- 78 neuropil meshes and thousands of neuron skeletons arranged in the coordinate system of a real fly brain.

## Lessons Covered

### Lesson 01 --- Parcellation
The 78 neuropil regions of the _Drosophila_ brain, loaded from FlyWire annotations. Hierarchical tree structure (brain → super-regions → neuropils) with query interface for navigating the anatomy.

### Lesson 06 --- The Volumetric Atlas
From point clouds to morphologies: 3D fly brain you can hold in your hands. This lesson loads neuropil surface meshes and neuron skeletons from Zenodo, rendering them as interactive HTML with `navis` and `plotly`.

The atlas moves the project from numbers to shapes. When you can rotate a neuropil mesh and see the neurons inside it, connectivity matrices stop being abstract and start being anatomy.

---

**Source files:**
- [`domains/bravli/codev/01-parcellation.org`](https://github.com/mayalucia/bravli) (875 lines)
- [`domains/bravli/codev/06-atlas.org`](https://github.com/mayalucia/bravli) (1,023 lines)
