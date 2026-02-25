+++
title = "Python Track: Interactive Exploration"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayapramana", "python"]
draft = false
+++

Python is the exploration language of MāyāPramāṇa --- the medium for quick experiments, interactive plots, and org-babel notebooks. When you want to see what happens when you change the pump rate or sweep the RF frequency, you reach for Python.

## Role in the Three-Language Architecture

| Language | Role | Strength |
|----------|------|----------|
| **Python** | Exploration | Fast iteration, plotting, org-babel integration |
| Haskell | Specification | Type safety, QuickCheck property testing |
| C++ | Deployment | Real-time performance, FPGA bridge |

The Python track implements the same physics as Haskell and C++, but optimises for **readability and interactivity** rather than performance or type safety. NumPy and SciPy handle the numerics; Matplotlib handles the visualisation; org-babel handles the narrative.

## What Gets Built

Each lesson produces Python code that can be executed in an org-babel block or as a standalone script:
- RK4 integrators for the Bloch equations
- Lock-in amplifier signal chains
- Kalman filter state estimators
- PID controller loops
- Spectral analysis utilities

---

**Content pipeline:** The Python implementations are tangled from the lesson `.org` files. This page will be populated as lessons 01--09 are developed.

**Source:** [`modules/mayapramana/curriculum.org`](https://github.com/mayalucia/mayapramana) --- Python sections throughout the 10-lesson sequence
