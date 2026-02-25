+++
title = "Interactive Demo: The Bloch Sphere"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayapramana", "demo", "interactive"]
draft = false
+++

The Bloch sphere is the geometric representation of a two-level quantum system --- every point on the sphere corresponds to a pure state, every point inside to a mixed state. Watching a spin precess on the Bloch sphere builds intuition that no equation can replace.

## What the Demo Will Show

An interactive 3D Bloch sphere in the browser where the user can:

- **Apply a static field** and watch Larmor precession
- **Turn on optical pumping** and see the state spiral toward the poles
- **Add relaxation** (T₁, T₂) and observe the magnetisation decay
- **Sweep the RF field** and find the resonance condition
- **Compare** the quantum spin dynamics with the Bloch vector approximation

## Applications Context

The same physics drives optically pumped magnetometers (OPMs) used for:
- **MEG** --- wearable brain imaging with quantum sensors
- **Magnetic anomaly navigation** --- GNSS-denied positioning using Earth's crustal field
- **Geophysical surveying** --- mapping subsurface geological structure

---

**Content pipeline:** The interactive demo is planned. The physics engine exists in the lesson code; the browser deployment will use WebAssembly or ClojureScript.

**Source:** [`modules/mayapramana/applications.org`](https://github.com/mayalucia/mayapramana) --- quantum magnetometry for brain imaging (288 lines, ~11 KB)
