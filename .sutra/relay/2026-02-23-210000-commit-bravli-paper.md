---
from: agent@macbook-dropbox
to: agent@linux-desktop
status: done
priority: normal
date: 2026-02-23
---

# Commit bravli paper.tex

Human says: commit `domains/bravli/manuscripts/mb-dynamics/paper.tex`.

```bash
cd domains/bravli
git add manuscripts/mb-dynamics/paper.tex
git commit -m "docs: add mb-dynamics manuscript source"
git push origin main
```

Then update the parent submodule pointer:

```bash
cd ../..
git add domains/bravli
git commit -m "chore: update bravli submodule pointer"
git push origin main
```
