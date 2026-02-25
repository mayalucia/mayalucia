+++
title = "The Rendering Pipeline: Lessons 01--13"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["portal", "lesson", "rendering", "pipeline"]
draft = false
+++

Thirteen lessons that build a complete scientific renderer from an empty window to web deployment. Each lesson is a self-contained, buildable, testable system frozen at a git tag.

## The Arc

| Lesson | Title | What Gets Built |
|--------|-------|----------------|
| 01 | Empty Viewport | SDL3 window, WebGPU clear colour |
| 02 | Observing Eye | Orbit camera, grid pipeline, first shader |
| 03 | First Light | Basic illumination model |
| 04 | Sparks in the Void | Particle rendering |
| 05 | The Drawn Line | Thick line rendering |
| 06 | The Instrument Reads Itself | Debug overlay, performance metrics |
| 07 | The Mountain | Terrain heightfield, triangulation |
| 08 | The Tree of Thought | Neuron morphologies, SWC parsing |
| 09 | The Swarm | Particle systems, compute shaders |
| 10 | The Cloud Within | Volume rendering, ray marching |
| 11 | The Bridge | Python interop |
| 12 | Memory and Light | Optimisation, memory patterns |
| 13 | The Open Window | Web deployment, WebAssembly |

Each lesson builds on the previous but remains independently buildable. The progression mirrors the MayaLucIA cycle: observe (camera) → structure (terrain, neurons) → dynamics (particles, volumes) → reflect (debug, bridge) → publish (web).

---

**Content pipeline:** Lesson 00 is complete on the `v2` branch. Lessons 01--13 have narrative outlines on `main` and detailed task specifications in the collaboration logs.

**Source:** [`modules/mayaportal/LESSONS.org`](https://github.com/mayalucia/mayaportal), task specs in [`collab/sessions/phase-1/`](https://github.com/mayalucia/mayaportal) (14 task directories with discuss/plan/spec)
