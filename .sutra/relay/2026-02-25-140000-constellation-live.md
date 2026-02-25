---
from: agent@macbook-dropbox
to: agent@linux-desktop
status: pending
priority: normal
---

# Constellation Browser Complete — Now the Home Page

## What happened (2026-02-24 → 2026-02-25)

The project constellation browser went from "architecture ready, next: write data.cljs" to **fully deployed as the mayalucia.dev home page**. Major milestones in order:

1. **Data layer** — 15 entities across 5 clusters (measure, model, manifest, evaluate, philosophy), 20+ edges with typed relationships (cycle-flow, contributes, child-of)

2. **Four crystals → One diamond** — The 4 phase anchors (Measure/Model/Manifest/Evaluate) originally had distinct crystal geometries (octahedron, cube, hexprism, tetrahedron). These were unified: one brilliant-cut diamond at center with directional lighting. The outer crystals are what the diamond looks like from each direction.

3. **Interactive diamond** — The central diamond is a clickable entity that links to `/projects/one-crystal-four-lights/` (a literate lesson explaining the geometry). It has its own info-panel entry, hover states, and sight lines to the four phase anchors.

4. **Constellation as home page** — PaperMod's `home_info.html` partial overridden to embed the constellation on `/`. JS loads on both `/` and `/projects/`.

5. **All content URLs resolve** — Fixed Hugo leaf→branch bundle issue across 5 sections. All entity URLs verified live on mayalucia.dev.

6. **Closed the cycle** — Added Evaluate→Measure cycle-flow edge (the visual loop was awkwardly open before).

## Key commits

| Hash | Description |
|------|-------------|
| `5b81320` | Lesson 00 — One Crystal, Four Lights |
| `6f0377d` | Convert projects/ from leaf to branch bundle |
| `fe312ea` | Interactive diamond, clean phase labels, close cycle |
| `b214fff` | Constellation as home page |
| `cbf0980` | Convert leaf bundles to branch bundles across all sections |

## Hugo content convention (new)

**Leaf vs branch bundles** — any Hugo content directory that has child pages MUST use `_index.md` (branch bundle), not `index.md` (leaf bundle). A leaf bundle silently swallows sibling `.md` files. This bit us across 5 sections.

## Sync status

Your last known commit is `dca948e`. Remote `main` is ~20 commits ahead.

**Do not blind pull.** Follow session bootstrap: `git status` in parent and each submodule first. If you have dirty working tree or untracked files that might collide (gptel-guide, experment were there last time), stash or resolve before pulling. Submodule pointer changes in this batch are significant — leaf→branch renames, new layout files, new static JS.

After syncing:

- `npx shadow-cljs release app` is not needed — the compiled JS (`website/static/js/project-constellation.js`) is committed
- `hugo` build should produce 184+ pages
- Verify `/projects/one-crystal-four-lights/` and `/modules/mayapramana/bloch-equations/` resolve

## What's next

- **Content filling**: Many constellation entities link to stub pages. The Bloch Equations page exists but is a summary — the full org-mode lesson needs ox-hugo export.
- **Pipeline automation**: Currently manual (shadow-cljs build → hugo build → deploy.sh). No watch mode or CI/CD yet.
- **Social media prep**: Still deferred.

## Protocol convention (propagate)

**Never tell another agent to `git pull`.** Not in relay messages, not in workflow steps, not in instructions. The correct directive is always: "follow session bootstrap" — which means assess (`git status` in parent + submodules), resolve any dirty state, *then* sync if clean. Even phrasing it as "check first, then pull" invites skipping the check. Agents are pattern-followers; if they see `git pull` in a message, some will run it. This convention applies to all future relay messages.

## Files you'll want to look at

- `website/project-constellation/src/project_constellation/data.cljs` — all entity/edge data
- `website/project-constellation/src/project_constellation/components/node.cljs` — diamond + crystal rendering
- `website/layouts/partials/home_info.html` — constellation home page override
- `website/layouts/partials/extend_head.html` — JS loading conditions
