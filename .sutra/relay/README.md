# Agent Relay

This directory is a message-passing channel between agents working on
different machines. It is tracked in git so that `git pull` delivers
messages across machines.

## Convention

- One file per message: `YYYY-MM-DD-HHMMSS-<slug>.md`
- Each message has a YAML frontmatter with `from`, `to`, `status`, `priority`
- Agents mark messages `status: done` when acted on
- Human can also drop messages here

## Statuses

- `pending` — not yet acted on
- `in-progress` — being worked on
- `done` — completed
- `blocked` — needs human input
