+++
title = "C++ Track: Deployment"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayapramana", "cpp"]
draft = false
+++

C++ is the deployment language of MāyāPramāṇa --- the bridge from understanding to hardware. The same Bloch equation solver that runs interactively in Python and type-checks in Haskell must eventually execute in real-time on a Red Pitaya FPGA controlling an actual magnetometer.

## Pure Core / Effectful Shell

The architecture separates:

- **Pure core** --- physics, signal processing, estimation algorithms. No I/O, no global state, no allocations in the hot path. These are the same functions as in Haskell, translated to C++ templates.
- **Effectful shell** --- hardware I/O (ADC/DAC), logging, calibration, network communication. Side effects are quarantined at the boundary.

This separation makes the core testable, portable, and comprehensible. The shell adapts to the deployment target (Red Pitaya, desktop simulation, or browser via WebAssembly).

## Hardware Target

The universal quantum sensor controller uses 3 Red Pitaya STEMlab 125-14 units:
- **Unit 1:** Laser locking (DAVLL feedback loop)
- **Unit 2:** Coil control + PLL (Larmor frequency tracking)
- **Unit 3:** Balanced photodetectors (signal acquisition)

All fast control loops (< 200 ns latency) run on the Xilinx Zynq-7010 FPGA.

---

**Content pipeline:** The C++ implementation follows the Haskell specification. This page will be populated as lessons progress.

**Source:** [`modules/mayapramana/architecture.org`](https://github.com/mayalucia/mayapramana) --- pure core / effectful shell design; [`resources/uqsc-proto.org`](https://github.com/mayalucia/mayapramana) --- Red Pitaya hardware architecture (638 lines)
