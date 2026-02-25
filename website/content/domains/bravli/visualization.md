+++
title = "Visualization Portal"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["bravli", "visualization", "portal", "lesson"]
draft = false
+++

Where atlas, connectome, physiology, and simulation converge into an interactive exploration tool. The visualisation portal is the feedback loop that closes the scientific cycle: build a model, render it, inspect it, find the gaps, refine.

## Lesson 04 --- Visualization

3D rendering and interactive exploration with `navis` and `plotly`:
- **Neuron point clouds** --- scatter plots of cell body positions, coloured by type
- **Connection matrices** --- heatmaps of neuropil-to-neuropil connectivity
- **3D neuropil meshes** --- surface renderings of the 78 brain regions
- **Interactive HTML exports** --- explorable in any browser

## Lesson 12 --- The Digital Twin Portal

The portal philosophy: a model's limitations are as informative as its successes. The portal exposes:
- **Parameter inspection** --- every synapse weight, every time constant, traceable to its source
- **Simulation playback** --- raster plots, firing rate dynamics, population synchrony
- **What-if experiments** --- perturb a parameter, re-simulate, compare
- **Known gaps** --- explicitly marking where the model is uncertain or incomplete

---

**Source files:**
- [`domains/bravli/codev/04-visualization.org`](https://github.com/mayalucia/bravli) (912 lines)
- [`domains/bravli/codev/12-portal.org`](https://github.com/mayalucia/bravli) (1,123 lines)
