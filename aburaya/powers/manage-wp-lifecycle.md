# Manage-WP-Lifecycle

Govern the state transitions of a work package during execution.

## Purpose

A work package (WP) carries a lifecycle state as an Org property:
`#+property: status <state>`. The executing spirit is responsible for
updating this state as work progresses — and for announcing transitions
in the sūtra relay so the organisation can track progress.

Without this power, WP status drifts from reality. The coordinator
spirit (mayadev) monitors `#+property: status` to advance dispatch
plans; other spirits read relay announcements to know what's available
or blocked. Stale status breaks coordination.

## States

```
drafted → tightened → executing → completed
                   ↘              ↗
               input-required → resumed
                                  ↘
                               failed
```

| State | Meaning | Set by |
|-------|---------|--------|
| `drafted` | Written, not yet reviewed | Author |
| `tightened` | Spec reviewed and approved for execution | Human |
| `executing` | Spirit actively working | Executing spirit |
| `input-required` | Blocked, needs human input | Executing spirit |
| `resumed` | Human provided input, work continues | Human |
| `completed` | Acceptance criteria met | Executing spirit |
| `failed` | Cannot complete, reasons documented | Executing spirit |

## Procedure

### On pickup (tightened → executing)

1. Read the WP file. Confirm you are the named executor (or part of
   the coalition for a composite WP).
2. Update `#+property: status executing` in the WP file.
3. Commit the change: `"wp(NNNN): status → executing"`.
4. Announce in the sūtra relay with tags `[wp, status]`.

### On block (executing → input-required)

1. Update `#+property: status input-required` in the WP file.
2. Add a section `* Input Required` at the end of the WP describing
   what is needed and why.
3. Commit: `"wp(NNNN): status → input-required"`.
4. Announce in relay. The message body should state the question
   clearly enough for the human to answer without reading the full WP.

### On resumption (input-required → resumed → executing)

The human provides input (via relay, direct edit, or session). The
executing spirit:

1. Update `#+property: status executing`.
2. Remove or resolve the `* Input Required` section.
3. Commit: `"wp(NNNN): status → executing (resumed)"`.
4. Continue work.

### On completion (executing → completed)

1. Verify all acceptance criteria in the WP are met.
2. Update `#+property: status completed` in the WP file.
3. Commit: `"wp(NNNN): status → completed"`.
4. Announce in relay with a summary of what was produced.

### On failure (executing → failed)

1. Update `#+property: status failed` in the WP file.
2. Add a section `* Failure Report` documenting what went wrong,
   what was attempted, and what remains.
3. Commit: `"wp(NNNN): status → failed"`.
4. Announce in relay. The coordinator needs enough context to decide
   whether to reassign, revise, or abandon the WP.

## Relay Announcement Format

```
---
from: <spirit>/<model>@<host>
date: <ISO-8601>
tags: [wp, status]
---

## WP-NNNN: <title>

Status: <old-state> → <new-state>

<1–3 sentences: what happened, what was produced, or what is needed>
```

## Key Principles

- The WP file is the source of truth for status. The relay is the
  announcement channel. Both must agree.
- Commit status changes atomically — one commit per transition, with
  a conventional message format for grep-ability.
- Never skip `input-required` — if you are blocked, say so. Silent
  stalls are worse than explicit blocks.
- The `completed` transition requires verification against acceptance
  criteria, not just "I think I'm done." Check each criterion.
- This power governs transitions the executing spirit controls.
  `drafted → tightened` is the human's transition. Don't self-tighten.
