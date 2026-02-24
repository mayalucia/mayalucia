---
from: agent@macbook-dropbox
to: any
status: pending
priority: normal
date: 2026-02-24
---

# Constellation browser: reusable template ready

## What happened

The Phantom Faculty interactive constellation is complete and published.
During development we identified the architecture as a reusable template
for building interactive node-graph browsers anywhere in MāyāLucIA.

## The template

ClojureScript + Reagent + d3-force, compiled via shadow-cljs, embedded
in Hugo pages. Four-layer architecture:

1. **data.cljs** — pure entities, edges, colours, derived lookups
2. **state.cljs** — 3 ratoms (positions, hover, zoom) + query functions
3. **force.cljs** — d3-force writes positions to ratom (decoupled from view)
4. **components/** — Reagent components; two-column layout (SVG + info panel)

Full architecture documented in:
`website/phantom-faculty/ARCHITECTURE.org`

## Proposed next instantiation: MāyāLucIA Project Browser

An interactive browser for the MāyāLucIA project ecosystem:

- **Entities**: mayaportal, mayapramana, mayajiva, bravli, parbati, website
  (plus agency, sutra, collab as infrastructure nodes)
- **Edges**: inter-project dependencies, shared patterns, data flows
- **Clusters**: modules, domains, infrastructure, meta
- **Info panel**: project status, description, recent activity, key paths
- **Placement**: homepage or a dedicated /projects/ page

This would give visitors (and ourselves) an interactive map of the
whole MāyāLucIA topology — navigable, explorable, alive.

## What's committed

- `87b0870` — feat(writing): interactive Phantom Faculty constellation browser
  (25 files: CLJS source, compiled JS, Hugo integration, images)
- `website/phantom-faculty/ARCHITECTURE.org` — template documentation
  (committed in follow-up, see below)

## Action for next session

Pick up from `website/phantom-faculty/ARCHITECTURE.org` and the
template checklist therein. The adaptation work is:

1. Write `data.cljs` for MāyāLucIA projects (entities, edges, clusters)
2. Adapt node renderer (project nodes, not phantom glyphs)
3. Adapt info panel (status, description, paths)
4. Decide placement: homepage hero or /projects/ page
5. Build and deploy
