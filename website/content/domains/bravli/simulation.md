+++
title = "Simulation Engine"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["bravli", "simulation", "lesson"]
draft = false
+++

139,000 neurons on a laptop, from first principles. The simulation engine assembles anatomy (parcellation), connectivity (edge lists), and physiology (cell and synapse models) into a running whole-brain LIF simulation --- no Brian2, no NEST, just pure NumPy.

## Lesson 11 --- Whole-Brain LIF Simulation

The simulation uses the Shiu _et al._ formulation: current-based LIF with exponential synaptic conductances, sparse connectivity matrix, and vectorised Euler integration. Key design choices:

- **Pure NumPy** --- no external simulator dependency; every equation is visible and modifiable
- **Sparse matrices** --- `scipy.sparse` CSR format for the 50M-synapse connectivity
- **Stimulus protocols** --- current injection, optogenetic activation, sensory input patterns
- **Analysis tools** --- raster plots, firing rate histograms, population synchrony measures

## Lesson 15 --- Brunel Phase Diagram

Where does the mushroom body sit in dynamical regime space? The Brunel (2000) framework classifies networks by two axes: **synchrony** (synchronous vs. asynchronous) and **balance** (excitation-dominated vs. inhibition-stabilised). By varying external drive and inhibitory gain, we map the MB's operating point.

---

**Source files:**
- [`domains/bravli/codev/11-simulation.org`](https://github.com/mayalucia/bravli) (1,355 lines, ~51 KB)
- [`domains/bravli/codev/15-brunel-phase-diagram.org`](https://github.com/mayalucia/bravli) (348 lines)
