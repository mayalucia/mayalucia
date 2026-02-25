+++
title = "Pure Core: Monadic Composition in C++"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["portal", "architecture", "functional"]
draft = false
+++

The pure core of MāyāPortal is a library of types and algorithms with zero side effects --- no I/O, no global state, no allocations in the hot path. Everything that touches the outside world (SDL3 windows, WebGPU devices, file systems) lives in the effectful shell.

## The Monadic Vocabulary

Haskell's abstractions map onto C++ with surprising fidelity:

| Haskell | C++ | Purpose |
|---------|-----|---------|
| `Maybe a` | `std::optional<T>` | Presence or absence |
| `Either e a` | `std::expected<T,E>` | Errors as values |
| `Reader r a` | Function taking config | Immutable context |
| `State s a` | Transform of `(S) → (T, S)` | Evolving world |
| `Writer w a` | `(T, Log)` pairs | Accumulating knowledge |
| `>>=` (bind) | `and_then` / `transform` | Sequential composition |

The monadic composition guide teaches these patterns through 12 chapters, each with a concept document and an interactive workbook.

## Why Functional for Rendering?

A rendering pipeline is a sequence of pure transformations: vertices → clip space → fragments → pixels. State (camera, lights, materials) flows through as immutable context. Errors (missing textures, shader compilation failures) propagate as values, not exceptions. The functional vocabulary is not imposed on rendering --- it is discovered in it.

---

**Source:** [`modules/mayaportal/project/monadic-composition.org`](https://github.com/mayalucia/mayaportal) (512 lines), [`develop/monadic-composition-guide/`](https://github.com/mayalucia/mayaportal) (12 chapters, ~3,500 lines)
