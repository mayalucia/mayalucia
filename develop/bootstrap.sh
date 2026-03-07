#!/usr/bin/env bash
# MāyāLucIA — Bootstrap a fresh clone on a new host
#
# Usage:
#   curl -sL <raw-url> | bash -s -- ./mayalucia
#   — or —
#   bash bootstrap.sh ./mayalucia
#
# What this does:
#   1. Clones the parent repo + all submodules
#   2. Clones the sūtra relay as .sutra/ (gitignored harness)
#   3. Creates local gitignored directories
#   4. Prints a message for the first Claude Code agent session
#
# What this does NOT do:
#   - Install tools (hugo, node, shadow-cljs, uv, emacs)
#   - Register this host in sūtra/hosts/ (the agent does that)
#   - Set up SSH keys or git credentials
#   - Touch any existing Dropbox clone
#
# Migrating from Dropbox:
#   If this machine already has a Dropbox-synced mayalucia clone,
#   first check git status there — commit or stash any unsaved work.
#   Then run this script targeting a LOCAL path (outside Dropbox).
#   The old Dropbox clone can be left alone or removed later.
#
# Prerequisites:
#   - git with HTTPS access to github.com/mayalucia/*
#   - gh auth (or HTTPS credentials cached)

set -euo pipefail

# ── Argument: target directory ──────────────────────────────────────

TARGET="${1:?Usage: bootstrap.sh <target-directory>}"

if [ -d "$TARGET/.git" ]; then
    echo "ERROR: $TARGET already contains a git repo."
    echo "If you want to start fresh, remove it first."
    exit 1
fi

# ── Clone ───────────────────────────────────────────────────────────

echo "▸ Cloning mayalucia into $TARGET ..."
git clone https://github.com/mayalucia/mayalucia.git "$TARGET"

cd "$TARGET"

echo "▸ Initialising submodules ..."
git submodule update --init --recursive

# Verify submodule health
echo "▸ Submodule status:"
git submodule status

# ── Sūtra relay ─────────────────────────────────────────────────────

echo "▸ Cloning sūtra relay into .sutra/ ..."
git clone https://github.com/mayalucia/sutra.git .sutra/

echo "▸ Last 10 relay messages:"
cd .sutra/
git log --oneline -10
cd "$TARGET"

# ── Local directories (gitignored) ──────────────────────────────────

mkdir -p .attic
mkdir -p .sutradhar
echo "▸ Created .attic/ and .sutradhar/ (gitignored)"

# ── First-boot sentinel ─────────────────────────────────────────────
# Tells the first Claude Code session to run host registration.
# The agent will delete this file after completing setup.

cat > .first-boot << 'SENTINEL'
# MāyāLucIA — First Boot

This file was created by develop/bootstrap.sh. Its presence means
this host has not yet been registered with the organisation.

## What the agent must do

1. **Prompt the human**: ask for this host's name, role, and any
   git/SSH quirks (does bare `github.com` work, or does it need
   an alias like `github-visood`?).

2. **Create host descriptor**: write `.sutra/hosts/<name>.yaml`
   following the pattern of `vadda.yaml` and `mahakali.yaml`.
   Fields: id, hostname, aliases, os, shell, repos, git, tools, notes.

3. **Commit and push** the host descriptor to the sūtra repo.

4. **Purge stale memory**: check `~/.claude/projects/` for any
   auto-memory directory keyed to a *different* mayalucia path
   (e.g. a Dropbox-synced clone at `~/Library/CloudStorage/...`).
   If found, delete that directory entirely — it contains paths,
   submodule states, and host assumptions that will cause silent
   divergence. Then write fresh MEMORY.md for *this* installation.
   Ask the human before deleting anything.

5. **Announce on the relay**: write a sūtra message announcing the
   new host, tagged `[hosts, bootstrap]`.

6. **Delete this file**: `rm .first-boot`. The sentinel is one-shot.

## Reference

Existing host descriptors:
- `.sutra/hosts/vadda.yaml` — macOS, Dropbox-synced, primary dev
- `.sutra/hosts/mahakali.yaml` — Linux desktop, secondary

Bootstrap script: `develop/bootstrap.sh`
SENTINEL

echo "▸ Created .first-boot sentinel (agent will prompt you on first session)"

# ── Summary ─────────────────────────────────────────────────────────

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  MāyāLucIA cloned to: $TARGET"
echo "  Submodules: $(git submodule status | wc -l | tr -d ' ')"
echo "  Sūtra relay: .sutra/ ($(cd .sutra && git rev-list --count HEAD) messages)"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "  Next steps:"
echo "    1. Install tools as needed: hugo, node/npm, uv, emacs"
echo "    2. Open Claude Code in $TARGET"
echo "    3. The agent will find .first-boot and prompt you"
echo "════════════════════════════════════════════════════════════"
