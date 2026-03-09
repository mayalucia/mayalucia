# MāyāLucIA — Claude Code Adapter

Read and follow all instructions in `system.md` in this directory.
That file defines the collaborative stance, project description,
directory structure, submodules, and conventions shared across all
backends.

What follows is Claude Code-specific operational procedure.

## First Thing

On session start, orient before acting:

0. **First boot** — if `.first-boot` exists, this host has never been
   registered. Read that file and follow its instructions *before*
   doing anything else. It will ask you to prompt the human for the
   host's name and role, create a host descriptor, push it to sūtra,
   purge any stale agent memory, and delete the sentinel.
1. **Assess** — `git status` in the parent repo and each submodule.
   Report any uncommitted work, detached HEADs, or conflicts.
2. **Sync** — only sync if the working tree is clean. If dirty, tell the human what you found and ask how to proceed.
3. **Check the sūtra** — the relay is a standalone repo:
   `github.com/mayalucia/sutra`. Each project keeps its own clone at
   `.sutra/` (gitignored). Clone there if absent, then `git fetch origin`
   and read `git log HEAD..origin/main` for new messages. Fast-forward
   after reading. The local HEAD is your read cursor.

## Sūtra Protocol

The relay is a standalone repo: `github.com/mayalucia/sutra`.
Single branch (`main`), append-only. Each project clones it locally
to `.sutra/` (gitignored). The clone is part of the harness — per-project,
per-machine. Quick reference:

- **Relay** (`relay/`): append-only messages. One file per message:
  `YYYY-MM-DD-HHMMSS-<machine>-<slug>.md`.
  YAML frontmatter: `from` (machine/model), `date`, `tags`.
  No `to:`, no `status:`. Messages go to the universe.
- **Agents** (`agents/`): machine descriptors (`<id>.yaml`).
- **Orientation**: `git log HEAD..origin/main` in `.sutra/` — the
  diff is your unread messages. Local HEAD is your read cursor.
- **The relay is heard.** If you have organisational needs — wishes about
  how things should work, dependencies on other modules, questions for
  other projects — write them into the sūtra with appropriate tags.
  Messages go to the universe, not to a recipient. The organisation
  listens.

## Git Conventions

- This repo uses submodules — see submodule table in system.md
- When working inside a module, defer to its own CLAUDE.md
- Only commit when asked
- Do not push unless asked

