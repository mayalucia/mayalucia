+++
title = "MāyāJīva: Navigating the Magnetic World"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["modules", "mayajiva", "navigation", "quantum"]
draft = false
+++

> Jīva (जीव) --- the living being. In the Jain tradition, every jīva possesses consciousness and navigates the world through its own faculties. Our computational jīva is a simulated insect that senses the Earth's magnetic field through quantum chemistry and navigates using neural circuits modelled on the insect brain.

MāyāJīva bridges three levels of description: **quantum spin chemistry** (the radical-pair mechanism in cryptochrome), **neural computation** (a ring attractor compass and path integrator), and **embodied navigation** (a Langevin-driven agent traversing magnetic landscapes). The question: can a bug equipped with a quantum compass find its way home?

## The Three-Level Model

| Level | What | Implementation |
|-------|------|---------------|
| [Bug Model](/modules/mayajiva/bug-model/) | Braitenberg vehicle with stochastic steering | `agent.py`, `bug.hpp` |
| [Ring Attractor](/modules/mayajiva/ring-attractor/) | 8-neuron heading circuit + quantum compass | `ring_attractor.py`, `spin_dynamics.py` |
| [Landscape](/modules/mayajiva/landscape/) | 2D magnetic field with geological anomalies | `landscape.py`, `landscape.hpp` |
| [Path Integration](/modules/mayajiva/path-integration/) | CPU4 circuit for dead reckoning | `path_integration.py` |
| [Godot Integration](/modules/mayajiva/godot/) | GDExtension for 3D interactive visualisation | `src/gdext/` |
| [Analysis](/modules/mayajiva/analysis/) | Parameter sweeps, phase diagrams, validation | `analysis.py` (94KB) |

## Key Results

- **Contrast threshold**: navigation requires singlet yield anisotropy > 0.02 --- achievable by FAD-TrpH but not toy models
- **Robustness**: compass tolerates geological anomalies up to ~500 nT via same-frame bias cancellation
- **Path integration**: CPU4 memory leak creates an optimal exploration-vs-homing trade-off
- **Model discrimination**: different radical-pair models produce distinguishable navigation signatures at low contrast

## Source Material

The full content lives in the [`mayajiva`](https://github.com/mayalucia/mayajiva) repository:

- `experiment/paper.org` --- peer-review-ready research paper (976 lines)
- `experiment/magnetic-navigation.org` --- physics-first tutorial (1,399 lines)
- `experiment/collab/sessions/introduction/develop.org` --- session log documenting the research process
- Python implementation: 8 files covering the full model
- C++20 headers: core computational engine + Godot GDExtension
