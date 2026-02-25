+++
title = "Cell Models and Synaptic Physiology"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["bravli", "physiology", "models", "lesson"]
draft = false
+++

Anatomy tells you who connects to whom. Physiology tells you what those connections _do_. These two lessons build the biophysical parameter database that turns a wiring diagram into a simulation.

## Lesson 09 --- Synaptic Physiology

A `SynapseModel` database covering 6 neurotransmitter types:
- **Reversal potentials** --- what voltage each synapse drives toward
- **Receptor kinetics** --- rise time, decay time, conductance amplitude
- **Confidence levels** --- distinguishing measured values from literature estimates from educated guesses

Each parameter carries provenance: where it came from, how reliable it is, what the fly-specific evidence says versus the generic insect value.

## Lesson 10 --- Cell Models

Point neuron models derived from first principles:
- **Leaky integrate-and-fire (LIF)** --- the simplest spiking model, sufficient when topology dominates
- **Graded transmission** --- for non-spiking interneurons (common in _Drosophila_)
- **Electrical properties per cell type** --- membrane time constant, threshold, reset, from the FlyWire cell type catalog

---

**Source files:**
- [`domains/bravli/codev/09-synaptic-physiology.org`](https://github.com/mayalucia/bravli) (1,029 lines)
- [`domains/bravli/codev/10-cell-models.org`](https://github.com/mayalucia/bravli) (919 lines)
