+++
title = "Mushroom Body Microcircuit"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["bravli", "mushroom-body", "learning", "lesson"]
draft = false
+++

The mushroom body (MB) is the fly's learning and memory center --- a microcircuit of ~6,300 neurons that transforms dense olfactory input into sparse, associative representations. It is the first circuit explored end-to-end in BRAVLi, and the subject of a research manuscript.

## Lessons Covered

### Lesson 05 --- Explore the Mushroom Body
Integration: complete factsheet and visualisation of the MB. Kenyon cells (KC), projection neurons (PN), dopaminergic neurons (DAN), and mushroom body output neurons (MBON) --- populations, connectivity, and spatial arrangement.

### Lesson 13 --- Mushroom Body Microcircuit
Does sparse coding emerge from wiring alone? The MB is extracted from the whole-brain connectome and simulated in isolation. The key metric: 5--10% of Kenyon cells active for any given odour (observed experimentally). Can the connectome-derived circuit reproduce this without plasticity?

### Lesson 14 --- ISN Regime and Olfactory Learning
Two questions: (1) Is the MB in the inhibition-stabilised network (ISN) regime? Test: paradoxical response to inhibitory perturbation. (2) Can three-factor STDP (pre × post × dopamine) produce single-trial olfactory conditioning?

---

**Manuscript:** _Network Dynamics of the Drosophila Mushroom Body_ --- regime classification, neuromodulation, stochasticity, and model invariance.

**Source files:**
- [`domains/bravli/codev/05-explore-mushroom-body.org`](https://github.com/mayalucia/bravli) (622 lines)
- [`domains/bravli/codev/13-mushroom-body-circuit.org`](https://github.com/mayalucia/bravli) (975 lines)
- [`domains/bravli/codev/14-isn-and-learning.org`](https://github.com/mayalucia/bravli) (500 lines)
- [`domains/bravli/manuscripts/mb-dynamics/paper.org`](https://github.com/mayalucia/bravli) (565 lines)
