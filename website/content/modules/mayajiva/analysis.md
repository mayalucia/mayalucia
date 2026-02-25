+++
title = "Analysis: Phase Diagrams and Validation"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayajiva", "analysis", "results"]
draft = false
+++

The analysis framework provides the tools for systematic exploration of the model's parameter space. It uses a fast vectorised simulation (bypassing per-step ring attractor dynamics) to enable large-scale sweeps: 200 bugs × 100+ parameter points per sweep.

## Key Analysis Products

### Navigation Phase Diagram
Contrast (singlet yield anisotropy) vs. compass noise → phase boundary separating navigating from lost regimes. The critical contrast threshold (~0.02) determines which radical-pair models support navigation.

### Robustness Budget
Suppression mechanisms that reduce compass contrast:
- Spin relaxation (T₁, T₂ in the radical pair)
- Rate asymmetry (unequal singlet/triplet recombination)
- Orientational disorder (molecules not perfectly aligned)

Each mechanism has a safety margin --- the factor by which it can increase before navigation fails.

### Anomaly Sweeps
Dipole and fault anomalies of increasing strength, testing whether same-frame bias cancellation keeps the bug on course. Result: robust to ~500 nT anomalies.

### Path Integration Phase Diagram
Homing error as a function of exploration duration and memory leak parameter. Reveals the optimal exploration horizon for each noise level.

### Model Discrimination
At low contrast (C ~ 0.1), different radical-pair models produce statistically distinguishable navigation signatures --- suggesting that behavioural experiments could discriminate between molecular mechanisms.

## Figures

The analysis produces 36+ diagnostic figures covering all aspects of the model. These are archived as PNGs in the `experiment/` directory.

---

**Source:** [`modules/mayajiva/experiment/analysis.py`](https://github.com/mayalucia/mayajiva) (2,359 lines, ~94 KB), [`experiment/sim.py`](https://github.com/mayalucia/mayajiva) (434 lines), [`experiment/paper.org`](https://github.com/mayalucia/mayajiva) (results sections)
