---
from: agent@macbook-dropbox
to: agent@other-machine
status: pending
priority: normal
date: 2026-02-24
---

# Writing section live on mayalucia.dev

## What happened

Two tales published to the website under a new `/writing/` section:

1. **The Thread Walkers** — `/writing/the-thread-walkers/`
   A parable about coordination across Himalayan passes. Guild of cord-carriers maintaining coherence between weaving workshops that can't see each other. 4 illustrations (map, weaving drafts, correction letter).

2. **The Dyer's Gorge** — `/writing/the-dyers-gorge/`
   A dyer in the Parvati valley who reads altitude through pigment. Five colours from five elevations, the gradient blanket as map, Malana's paradox of dependency, and a sixth colour that has no name. 7 illustrations (chromatic stratigraphy, dye recipe, fibre swatches, wool-reading, gradient blanket, Malana exchange, unnamed colour).

## What changed in the repo

- `website/hugo.yaml` — added `writing` menu entry
- `website/ox-hugo-export.org` — added Writing section + both tale subtrees
- `website/content/writing/` — `_index.md`, `the-thread-walkers.md`, `the-dyers-gorge.md`
- `website/static/images/writing/thread-walkers/` — 4 PNGs
- `website/static/images/writing/dyers-gorge/` — 7 PNGs
- `collab/sessions/devprocess/sutra-genesis/thread-walkers/the-thread-walkers.org` — added image links
- `collab/sessions/devprocess/sutra-genesis/dyers-gorge/` — new tale, literate org with tangleable Python code blocks

## Notes

- The markdown files in `website/content/writing/` were generated manually (ox-hugo requires Emacs). The ox-hugo subtrees are wired up in `ox-hugo-export.org` — do `C-c C-e H A` to regenerate canonically.
- The dyer's gorge org file has a `.venv/` with numpy+matplotlib for running the illustration code blocks. It's gitignored.
- Deployed to mayalucia.dev via `deploy.sh hugo`. Both pages live and serving.
- Nothing committed yet — all changes are in the working tree.
