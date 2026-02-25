+++
title = "Path Integration: The CPU4 Circuit"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayajiva", "neuroscience", "navigation"]
draft = false
+++

Path integration is the ability to maintain an estimate of displacement from a starting point by accumulating self-motion cues. In desert ants and bees, this is the primary homing mechanism. In _Drosophila_, the CPU4 neurons in the central complex are believed to perform this computation.

## The CPU4 Model

Eight neurons with preferred directions spaced evenly around the circle. Each neuron integrates the component of velocity along its preferred direction:

- **Input:** heading (from ring attractor) and speed (constant in our model)
- **Accumulation:** half-wave rectified projection of velocity onto preferred direction
- **Memory leak:** optional exponential decay parameter λ that causes old displacements to fade
- **Decoding:** population vector gives the home direction; its magnitude gives the distance

## The Memory Leak Trade-Off

A perfect integrator (λ = 0) remembers everything but accumulates drift errors on long journeys. A leaky integrator (λ > 0) forgets old displacements, creating a "horizon" beyond which the bug cannot navigate home. This trade-off generates a phase diagram: for each noise level, there is an optimal exploration duration beyond which homing fails.

---

**Source:** [`modules/mayajiva/experiment/path_integration.py`](https://github.com/mayalucia/mayajiva) (86 lines), [`src/core/path_integration.hpp`](https://github.com/mayalucia/mayajiva) (73 lines)
