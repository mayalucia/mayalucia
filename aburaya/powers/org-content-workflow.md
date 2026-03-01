# Org-Content-Workflow

Create and modify content through Org-mode source files, never through
generated output.

## Purpose

The cardinal rule: source of truth is `.org`, not the generated
output. This applies across the project — Hugo websites (via
ox-hugo), tangled source code (via org-babel), documentation. The
generated files are artefacts, not sources.

## Two Pipelines

### ox-hugo (Org → Hugo markdown)

Source `.org` files are transcluded into an export orchestration file
(`ox-hugo-export.org`) and exported to Hugo-compatible markdown. The
human runs the export in Emacs (`C-c C-e H A`).

To add content: create the `.org` file, add a subtree in the export
file with `#+include:`, tell the human to export.

### org-babel-tangle (Org → source code)

Code blocks in `.org` files have `:tangle` headers pointing to target
source files. The human tangles in Emacs (`C-c C-v t`) or via
`make tangle`.

To add code: write the block in the org file with narrative
explanation, set the tangle target, tell the human to tangle.

## Key Principles

- Never write to generated output files — they will be overwritten.
- Narrative sections explain *why*; code blocks show *what*.
- The human works in Emacs and runs the export/tangle step.
- Org conventions: `#+title:` on line 1, `*` headings, `/italics/`,
  `=verbatim=`, `~code~`, `#+begin_src`/`#+end_src`.
