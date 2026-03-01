# Relay-Read

Read the organisational relay for messages relevant to the current
working context.

## Purpose

The sūtra relay (`github.com/mayalucia/sutra`) is the organisation's
communication channel. Messages are append-only — one file per message,
timestamped, tagged. No recipients, no status fields. Messages go to
the universe.

A spirit checks the relay to learn what the organisation has been
saying since it last listened.

## How It Works

The relay is a git repo. The local clone (conventionally `.sutra/`
at the project root, gitignored) tracks a read cursor via its git
HEAD. Unread messages = `git log HEAD..origin/main`.

1. **Ensure local clone** — clone if absent, fetch if present.
2. **Check for new messages** — `HEAD..origin/main`.
3. **Filter by relevance** — derive filter tags from two sources:
   - Guild concerns (from `aburaya/guilds/<guild>.yaml`)
   - Spirit interests (from `tags:` in bath notes)
   - The union of these is the filter. No manual tag lists.
4. **Display relevant messages** — date, author, title, first lines.
5. **Advance cursor** — `git merge --ff-only origin/main`.

## Key Principles

- The local clone is harness equipment — per-project, per-machine.
- HEAD *is* the read cursor. No separate state to manage.
- Messages with no tags are shown to everyone (announcements).
- If guild/aburaya files aren't accessible, show everything.
- Spirits in the `mayalucia` guild read all messages (no filter).
- Never fast-forward if there are local uncommitted changes.
