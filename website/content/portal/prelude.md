+++
title = "Lesson 00: Prelude"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["portal", "lesson", "cpp"]
draft = false
+++

The Prelude establishes the development process itself: literate `.org` files → `org-babel-tangle` → C++23 source → CMake build → Catch2 tests. Before rendering a single pixel, we need confidence that our tool chain works and that our code is correct by construction.

## What This Lesson Builds

- **The identity function** --- the simplest possible pure function, used to verify the tangle → build → test pipeline
- **`std::expected`** --- C++23's error-as-value type, replacing exceptions with explicit control flow
- **Catch2 test harness** --- every function gets a test before it gets a caller
- **CMake + FetchContent** --- dependency management for SDL3, wgpu-native, glm, Catch2

## Why Start Here?

The Sculptor's Paradox: the tool that offers no resistance teaches nothing. If we used a high-level framework, we would learn the framework, not the rendering. By building from C++23 primitives, every abstraction earns its place.

The Prelude is tagged `lesson/00-prelude` in git --- a frozen, buildable snapshot that anyone can check out and verify.

---

**Source:** [`modules/mayaportal/codev/00-prelude.org`](https://github.com/mayalucia/mayaportal) --- the literate lesson file from which all source code is tangled
