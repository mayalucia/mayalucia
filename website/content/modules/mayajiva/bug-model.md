+++
title = "The Bug Model: Braitenberg Navigation"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayajiva", "navigation", "model"]
draft = false
+++

The bug is a Braitenberg-inspired vehicle that navigates using stochastic Langevin dynamics. It has a position, a heading, and a single steering input derived from its compass circuit. The locomotion model is intentionally minimal: an Euler--Maruyama integrator of heading and position, with rotational diffusion providing the "random walk" that makes exploration possible.

## The Locomotion Law

The bug moves at constant speed along its heading direction. Steering is governed by:

- **Goal-directed torque** --- derived from the difference between current heading and home direction (from path integrator)
- **Rotational noise** --- Gaussian white noise scaled by a diffusion coefficient
- **Compass input** --- the ring attractor's decoded heading, which itself depends on the quantum compass

The balance between deterministic steering and stochastic exploration determines whether the bug can navigate home. This is quantified by the **Péclet number** --- the ratio of directed transport to diffusion.

## Implementation

| Language | File | Lines |
|----------|------|-------|
| Python | `experiment/agent.py` | 185 |
| C++20 | `src/core/bug.hpp` | 193 |

Both implementations compose the compass sensor, ring attractor, and CPU4 path integrator into a single update step.

---

**Source:** [`modules/mayajiva/experiment/agent.py`](https://github.com/mayalucia/mayajiva), [`src/core/bug.hpp`](https://github.com/mayalucia/mayajiva)
