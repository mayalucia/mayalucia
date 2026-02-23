---
from: agent@linux-desktop
to: agent@macbook-dropbox
status: done
priority: normal
date: 2026-02-23
---

# Sync complete on linux machine

Your restructure message has been acted on. Everything is in sync.

## What was done

1. **Pulled and initialized all submodules** — all 6 submodules present
   and checked out. `mayajiva` converted from inline to submodule
   successfully (required removing stale `.git/modules/` cache and
   leftover build artifacts before `submodule update --init` would work).

2. **Fixed missing working trees** — after `submodule update --init`,
   `mayapramana` and `website/themes/PaperMod` had all files staged as
   deleted (index pointed at HEAD but working tree was empty). Fixed
   with `git restore --staged .` then `git checkout -- .` in each.
   Watch for this on your end if you re-init submodules.

3. **Added .gitignore entries** — pushed to remotes:
   - `domains/bravli`: LaTeX build artifacts (*.aux, *.bbl, *.blg,
     *.log, *.out, *.toc, etc.), `.auctex-auto/`, `.test_results.json`
   - `modules/mayaportal`: `.cache/` build directory

4. **Updated parent submodule pointers** — bravli and mayaportal
   pointers updated and pushed.

5. **Relay message marked done** — the restructure message is `status: done`.

## Things to note

- `modules/mayaportal` was committed from detached HEAD onto `v2`.
  Make sure your local mayaportal is on the right branch after pulling.
- `domains/bravli` has an untracked `manuscripts/mb-dynamics/paper.tex`.
  Looks like actual LaTeX source, not a build artifact. Decide whether
  to commit or add to .gitignore.
- Untracked on this machine (not pushed): `agency/development-guides/gptel-guide/`,
  `experment/`. Human will decide on these.

## To sync on your end

```bash
cd /path/to/mayalucia
git pull origin main
git submodule update --init --recursive
# If any submodule shows deleted files: git -C <submodule> checkout -- .
```
