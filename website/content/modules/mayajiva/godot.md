+++
title = "Godot Integration: 3D Interactive Visualisation"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayajiva", "godot", "visualisation"]
draft = false
+++

The computational core of MāyāJīva is written in C++20 header-only templates. The Godot GDExtension wraps these templates as engine-native nodes, making the simulation inspectable and controllable inside a 3D scene.

## GDExtension Nodes

| Node | Wraps | Purpose |
|------|-------|---------|
| `BugNode` | `Bug<8>` | Navigating agent in 3D space |
| `LandscapeResource` | `Landscape` | Magnetic field environment |

The `BugNode` exposes all parameters (compass noise, steering gain, memory leak) as Godot properties, editable in the inspector. The `LandscapeResource` allows declarative anomaly setup through the Godot editor.

## Why Godot?

Godot provides a complete scene graph, physics, and rendering pipeline for free. By wrapping the C++ core as a GDExtension rather than building a custom renderer, we get:
- Interactive 3D inspection (orbit camera, gizmos, property inspector)
- Particle trails for bug trajectories
- Terrain mesh from the landscape elevation model
- Real-time parameter tuning during simulation

---

**Content pipeline:** The GDExtension bindings exist in the source repository. Integration with a full 3D scene (terrain mesh, particle trails, camera) is planned.

**Source:** [`modules/mayajiva/src/gdext/bug_node.hpp`](https://github.com/mayalucia/mayajiva) (97 lines), [`src/gdext/landscape_resource.hpp`](https://github.com/mayalucia/mayajiva) (52 lines)
