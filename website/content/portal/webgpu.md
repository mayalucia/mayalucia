+++
title = "WebGPU: Browser Deployment"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["portal", "webgpu", "web", "deployment"]
draft = false
+++

The final lesson of MāyāPortal brings the renderer to the browser. The same C++ core, compiled to WebAssembly, runs inside a web page --- making every digital twin explorable by anyone with a browser.

## The Web Pipeline

1. **C++23 core** → Emscripten → WebAssembly module
2. **WGSL shaders** → served as text, compiled at runtime by the browser's WebGPU implementation
3. **HTML canvas** → the viewport element that receives the rendered output
4. **JavaScript glue** → event handling, canvas resizing, data loading

## Compute Shaders in the Browser

WebGPU compute shaders enable GPU-accelerated simulation directly in the browser:
- Particle systems with millions of particles
- Volume rendering via ray marching
- Terrain LOD computation

This is the "Open Window" --- the moment the digital twin becomes shareable.

---

**Content pipeline:** Web deployment is Lesson 13, the final lesson in the sequence. The experimental `galaxy-interaction.org` document explores browser-based WebGPU visualisation concepts.

**Source:** [`modules/mayaportal/web/develop/galaxy-interaction.org`](https://github.com/mayalucia/mayaportal) (513 lines)
