+++
title = "Haskell Track: Executable Specification"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayapramana", "haskell"]
draft = false
+++

Haskell is the specification language of MāyāPramāṇa. If the Python track asks "what happens?", the Haskell track asks "what _must_ happen?" Types encode physical units, function signatures encode signal flow, and QuickCheck properties encode the laws of physics.

## Why Haskell for Physics?

Signal processing is inherently compositional. A lock-in amplifier is:

```
demodulate . lowpass . mix_with_reference . sample
```

Each stage is a pure function; the pipeline is their composition. Haskell makes this composition explicit and type-safe. A Kalman filter is a state monad; a PID controller is a feedback arrow. The language's abstractions map directly onto the physics.

## What Gets Built

- Type-safe physical quantities (fields, frequencies, time constants)
- QuickCheck properties testing physical invariants (energy conservation, unitarity)
- Compositional signal processing pipelines
- Executable specifications that the C++ deployment must match

---

**Content pipeline:** The Haskell track is defined in the curriculum but implementation begins with Lesson 01. This page will be populated as the Haskell code is tangled from the lesson `.org` files.

**Source:** [`modules/mayapramana/architecture.org`](https://github.com/mayalucia/mayapramana) --- functional programming architecture (480 lines, ~18 KB)
