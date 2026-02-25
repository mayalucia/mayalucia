+++
title = "Effectful Shell: SDL3 and WebGPU Platform"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["portal", "platform", "sdl3", "webgpu"]
draft = false
+++

The effectful shell is everything the pure core cannot be: window creation, GPU device acquisition, input handling, file I/O. It quarantines side effects at the boundary so that the rendering algorithms remain testable and portable.

## Technology Stack

| Layer | Technology | Role |
|-------|-----------|------|
| Window & input | SDL3 | Cross-platform abstraction |
| GPU API | WebGPU (via wgpu-native) | Modern, portable graphics |
| Math | GLM 1.0+ | Vector/matrix operations |
| Build | CMake 3.24+ with FetchContent | Dependency management |
| Test | Catch2 | BDD-style test framework |

## Why WebGPU?

The evaluation considered SDL3's built-in SDL_GPU against WebGPU via Dawn/wgpu-native. WebGPU won on three counts:
1. **Browser deployment** --- the same shaders run in Chrome/Firefox via WebAssembly
2. **Compute shaders** --- essential for particle simulations and volume rendering
3. **Explicit resource management** --- closer to the metal, more to learn

SDL3 remains the platform layer (window, input, event loop) while WebGPU handles all GPU work.

---

**Source:** [`modules/mayaportal/project/techstack.org`](https://github.com/mayalucia/mayaportal), [`specs/spec-build.org`](https://github.com/mayalucia/mayaportal) (448 lines --- formal build specification)
