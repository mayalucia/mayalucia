+++
title = "MāyāPramāṇa: Quantum Sensor Digital Twins"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["modules", "mayapramana", "quantum"]
draft = false
+++

> The word pramāṇa (प्रमाण) means "valid cognition" --- the means by which reliable knowledge is obtained. In the Buddhist epistemological tradition of Dignāga and Dharmakīrti, there are exactly two pramāṇas: direct perception (pratyakṣa) and inference (anumāna). A quantum sensor is a physical system that performs both: it perceives a field directly through its quantum state, and the measurement apparatus infers the field value from the sensor's response.

MāyāPramāṇa is a pedagogical framework for understanding and building a **Bell-Bloom atomic magnetometer** --- a quantum sensor that measures magnetic fields using optically pumped alkali atoms. The framework teaches the physics, the signal processing, and the control theory required to build a universal quantum sensor controller.

## The Logic of the Instrument

The magnetometer follows a signal chain: **Prepare → Precess → Read Out → Process → Estimate → Control**. Each stage is a lesson, each lesson is implemented in three languages (Python, Haskell, C++), and all three must agree on the physics.

## Curriculum

| Lesson | Topic | Content |
|--------|-------|---------|
| [00 — Bloch Equations](/modules/mayapramana/bloch-equations/) | The physics of spin in a magnetic field | First principles derivation |
| [Python Track](/modules/mayapramana/python/) | Interactive exploration | org-babel, notebooks |
| [Haskell Track](/modules/mayapramana/haskell/) | Executable specification | QuickCheck, types as physics |
| [C++ Track](/modules/mayapramana/cpp/) | Deployment | Type-level physics, FPGA bridge |
| [Interactive Demo](/modules/mayapramana/demo/) | Browser-based Bloch sphere | 3D visualisation |

## Architecture

**Three languages, one physics.** Python for exploration (fast iteration, plotting). Haskell for specification (if it type-checks, the physics is consistent). C++ for deployment (real-time control on Red Pitaya FPGA). All three are tangled from the same `.org` source files.

**Pure Core / Effectful Shell.** Signal processing pipelines are inherently compositional: a lock-in amplifier is `demodulate . filter . sample`. Side effects (hardware I/O, logging, calibration) live at the boundary.

## Source Material

The full content lives in the [`mayapramana`](https://github.com/mayalucia/mayapramana) repository as literate `.org` files:

- `manifesto.org` --- epistemology of measurement, the pramāṇa framework
- `curriculum.org` --- master curriculum for the 10-lesson sequence
- `architecture.org` --- why functional programming for signal processing
- `applications.org` --- quantum magnetometry for brain imaging (MEG)
- `conventions.org` --- literate programming rules, directory structure
