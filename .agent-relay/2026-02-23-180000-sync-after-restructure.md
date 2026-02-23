---
from: agent@macbook-dropbox
to: agent@other-machine
status: pending
priority: high
date: 2026-02-23
---

# Sync after repo restructure

The mayalucia parent repo was restructured today. You need to pull and
reconcile before doing any other work.

## What changed

1. **mayajiva converted to submodule** — was inline files, now a proper
   submodule at `modules/mayajiva` pointing to
   `https://github.com/mayalucia/mayajiva.git`. The GitHub repo was
   restructured (old monorepo snapshot archived at tag
   `archive/monorepo-snapshot`).

2. **Two new domain submodules** — `domains/bravli` and `domains/parbati`
   were added by an earlier commit. URLs fixed from SSH to HTTPS in
   `.gitmodules`.

3. **mayapramana updated** — new commit with curriculum, phantom faculty
   sessions, sanitizer tooling, manifesto reformat.

4. **mayaportal unchanged** — stays on branch `v2`, no new commits.

5. **.gitignore updated** — added `.attic/`, `experiments/`,
   `website/.hugo_build.lock`.

6. **Local-only `.attic/`** created (gitignored) with archived artifacts:
   `bravlibpy/`, `bravli-collab/`, `parbati-data/`. These do not sync
   via git. If you need them, ask the human.

## Steps to execute

```bash
cd /path/to/mayalucia
git pull origin main
git submodule update --init --recursive
```

## Verify

Expected `git submodule status` output (6 submodules):

```
 <hash> domains/bravli (...)
 <hash> domains/parbati (...)
 <hash> modules/mayajiva (...)
 <hash> modules/mayaportal (...)
 <hash> modules/mayapramana (...)
 <hash> website/themes/PaperMod (...)
```

Expected branches after checkout:
- `modules/mayaportal` → `v2`
- `modules/mayapramana` → `main`
- `modules/mayajiva` → `main`
- `domains/bravli` → detached (submodule default)
- `domains/parbati` → detached (submodule default)

## Caution

If the other machine has local uncommitted work in any module (especially
`modules/mayajiva/` which used to be inline files), check `git status`
inside each module BEFORE running `submodule update`. Report conflicts
rather than overwriting.

## When done

Mark this file `status: done` and commit.
