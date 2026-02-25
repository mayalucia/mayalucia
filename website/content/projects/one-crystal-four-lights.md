+++
title = "One Crystal, Four Lights"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T18:00:00+01:00
tags = ["constellation", "svg", "geometry", "philosophy", "clojurescript"]
draft = false
+++

The project constellation uses a brilliant-cut diamond as its central metaphor. Four phases of the MāyāLucIA cycle --- Measure, Model, Manifest, Evaluate --- are not four separate operations. They are four viewpoints of a single inferential process. The visual language reflects this: one diamond at center, four identical copies at the cardinal positions, each illuminated from a different direction.

## The Geometry

A simplified brilliant-cut diamond viewed from above. Three concentric rings of vertices:

| Ring | Radius | Count | Position | Role |
|------|--------|-------|----------|------|
| Table | 0.38 | 8 | i x 45 degrees | Central octagon (the "face" of the diamond) |
| Stars | 0.90 | 4 | Intercardinals | Between phases --- connecting tissue |
| Kites | 1.40 | 4 | Cardinals | Outermost reach --- pointing at phases |

The table octagon has its **vertices** on the cardinal axes (not flat edges). This makes the diamond *point at* the phases rather than presenting faces toward them. Sharper, more crystalline.

Eight crown facets (two per quadrant) fill the ring between table and girdle. Each is a quadrilateral: two table vertices + one kite tip + one star tip.

## Directional Lighting

Three linear SVG gradients per phase colour create the 3D illusion:

- **crystal-top** --- brightest (white highlight fading to base colour)
- **crystal-left** --- medium (base colour fading to navy shadow)
- **crystal-right** --- darkest (base colour fading to deep indigo)

For the central diamond, gradient assignment is controlled by **hover state**: the hovered phase's quadrant gets `crystal-top`, adjacent quadrants get `crystal-left`, the opposite gets `crystal-right`.

For the outer crystals, gradient assignment is controlled by **position**: the quadrant facing the center gets `crystal-top` (it catches the light from the diamond). The far side gets `crystal-right` (deep shadow).

## The Inversion

Each outer crystal's brightest face is named after its opposite phase:

| Crystal | Position | Lit quadrant | Because |
|---------|----------|-------------|---------|
| Measure | Left | Manifest | Light comes from the right (center) |
| Model | Top | Evaluate | Light comes from below |
| Manifest | Right | Measure | Light comes from the left |
| Evaluate | Bottom | Model | Light comes from above |

To understand Measure, you look at it from Manifest's direction. To understand Model, you illuminate it from Evaluate's angle. The opposite is not the enemy --- it's the light source.

## Cycle Resonance

The four phases form a ring. When you hover one, the others respond based on topological distance:

- **Distance 0** (self): bright --- full attention
- **Distance 1** (adjacent): warm --- the cycle flows through
- **Distance 2** (opposite): gentle --- still connected, never extinguished

This uses a `cycle-distance` function: `min(|a-b| mod 4, |b-a| mod 4)`. The minimum of clockwise and anticlockwise distance on a 4-element ring.

## One Function, Four Instances

The code has a single `unit-diamond` definition (pre-computed vertices in unit coordinates) and a single `crystal-view` function that renders it at any position with any lighting direction. The four outer crystals are four calls to the same function with different `(cx, cy)` and different `phase-lit-quadrant` lookups. No special cases. No geometry duplication.

---

[**&#9671; See it live in the constellation**](/projects/) --- hover the diamond at the center.

**Literate source:** [`codev/00-one-crystal-four-lights.org`](https://github.com/mayalucia/mayalucia) --- the full lesson with code blocks, architecture diagrams, design decisions, and exercises.

**Implementation:** [`components/node.cljs`](https://github.com/mayalucia/mayalucia) (diamond, crystal-view, unit-diamond), [`components/constellation.cljs`](https://github.com/mayalucia/mayalucia) (SVG gradient defs).
