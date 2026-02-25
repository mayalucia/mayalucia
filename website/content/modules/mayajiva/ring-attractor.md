+++
title = "The Ring Attractor and Quantum Compass"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayajiva", "neuroscience", "quantum"]
draft = false
+++

How does an insect brain represent a compass heading? The ring attractor is a neural circuit where activity forms a bump that rotates around a ring of neurons, tracking the animal's heading. In _Drosophila_, this circuit lives in the ellipsoid body (E-PG neurons). In our model, it serves as the bridge between quantum chemistry and behaviour.

## The Radical-Pair Compass

The compass sensor models cryptochrome --- a flavoprotein in the insect eye that forms radical pairs under blue light. The singlet yield of the radical pair depends on the orientation of the Earth's magnetic field relative to the molecule's hyperfine axis. This anisotropy is tiny (a few percent) but sufficient for navigation.

The model implements the full quantum spin Hamiltonian:
- Zeeman interaction (external field)
- Anisotropic hyperfine coupling (nuclear spins)
- Exchange interaction (electron-electron)
- Haberkorn recombination (singlet/triplet decay)

Four radical-pair models are available, ranging from a toy 8-dimensional system to a 64-dimensional FAD-TrpH model with realistic hyperfine tensors.

## The Ring Attractor

An 8-neuron rate model with:
- **Local cosine excitation** --- nearby neurons reinforce each other
- **Global inhibition** --- a single inhibitory population (Δ7 equivalent) enforces winner-take-all
- **Compass input** --- the quantum singlet yield drives the ring through double-angle encoding (resolving the π-ambiguity inherent in an inclination compass)
- **Population vector decoding** --- the bump position gives the decoded heading

---

**Source:** [`modules/mayajiva/experiment/ring_attractor.py`](https://github.com/mayalucia/mayajiva) (183 lines), [`experiment/spin_dynamics.py`](https://github.com/mayalucia/mayajiva) (490 lines), [`experiment/magnetic-navigation.org`](https://github.com/mayalucia/mayajiva) (1,399 lines --- full physics tutorial)
