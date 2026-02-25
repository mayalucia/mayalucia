+++
title = "Lesson 00: The Bloch Equations"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayapramana", "physics", "lesson"]
draft = false
+++

> "I think I can safely say that nobody understands quantum mechanics." --- Richard Feynman

The Bloch equations describe how a magnetic moment precesses, relaxes, and responds to resonant driving fields. They are the foundation of everything that follows in the magnetometer: optical pumping, Larmor precession, signal demodulation, and state estimation all reduce to solving these equations under different conditions.

## What This Lesson Covers

Starting from a single spin-½ in a static magnetic field, the lesson builds up to the full Bloch vector equations through:

1. **The Larmor frequency** --- why spins precess, and at what rate
2. **The density matrix** --- parameterising the quantum state of an ensemble
3. **The Bloch vector** --- three real numbers that capture everything observable
4. **Relaxation** --- T₁ (longitudinal) and T₂ (transverse) decay
5. **Optical pumping** --- preparing the spin state with circularly polarised light

Each concept is implemented in Python, Haskell, and C++ simultaneously. The three implementations must agree on the physics --- a discrepancy between them means someone has misunderstood something.

## Pedagogical Cadenzas

The lesson includes self-contained "cadenza" modules for prerequisite concepts that a first-year graduate student might need to review: angular momentum, the Pauli matrices, density operators, and the rotating frame.

---

**Content pipeline:** This page summarises Lesson 00. The full lesson with derivations, code blocks, and exercises lives in the source repository and will be exported here as the ox-hugo pipeline matures.

**Source:** [`modules/mayapramana/lessons/00-bloch-equations/concept.org`](https://github.com/mayalucia/mayapramana) (885 lines, ~34 KB)
