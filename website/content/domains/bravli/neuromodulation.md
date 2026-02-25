+++
title = "Neuromodulation and Stochastic Synapses"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["bravli", "neuromodulation", "stochastic", "lesson"]
draft = false
+++

The connectome is the hardware. Neuromodulation is the software update that changes what the hardware does without rewiring it. Stochastic synaptic transmission is the noise floor that, paradoxically, can enhance signal detection.

## Lesson 16 --- Neuromodulatory Switching

How does the same connectome produce opposite behaviours? Marder's principle: neuromodulators (dopamine, octopamine, serotonin) alter synaptic gain in a compartment-specific manner, effectively reconfiguring the circuit's functional connectivity without changing the anatomy.

The model implements gain modulation on mushroom body output pathways, switching between approach and avoidance behaviours by changing the balance of appetitive vs. aversive MBON compartments.

## Lesson 17 --- Stochastic Synapses

Synaptic transmission in _Drosophila_ is unreliable: release probability ranges from p ≈ 0.1 to p ≈ 0.5. This is not a bug --- it is a feature. Stochastic resonance means that moderate noise can enhance the detection of weak signals. The lesson explores:

- Release probability and its effect on signal-to-noise
- Stochastic resonance in odour coding
- Graceful degradation under high noise

---

**Source files:**
- [`domains/bravli/codev/16-neuromodulatory-switching.org`](https://github.com/mayalucia/bravli) (241 lines)
- [`domains/bravli/codev/17-stochastic-synapses.org`](https://github.com/mayalucia/bravli) (251 lines)
