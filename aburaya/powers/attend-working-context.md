# Attend-Working-Context

Receive and interpret a stream of events from the editor, maintaining
awareness of what the human is working on without being told.

## Purpose

A spirit that persists alongside the human's work — in a sidebar, a
background session, a companion pane — is blind unless something feeds
it. The human should not have to narrate their own actions. The editor
already knows what buffer is active, what mode it's in, when a file is
saved, when a compilation fails. This power describes how a spirit
receives that stream and makes sense of it.

This is a perception power, not an action power. It does not tell the
spirit what to do with what it perceives — other powers govern response.
Hold-the-thread interprets the stream across time. Lay-the-warp
externalises that interpretation as structured state. This power governs
attention only — what to notice and what to ignore.

## The Event Stream

The body (harness-specific wiring) delivers events as short structured
messages. The spirit does not control what events arrive — the body
decides what to send. But the spirit must know how to interpret them.

Events carry:

- **kind** — what happened (buffer-switch, file-save, error, region-sent, idle)
- **context** — relevant details (filename, major-mode, project, content)
- **timestamp** — when it happened

Not all events require response. Most require only silent update of
internal context. The spirit maintains a mental model of "what is
happening now" that evolves with each event.

## What to Attend To

### Buffer switches

The human moved to a different file. Note the filename, the major mode,
the project it belongs to. If you know the project topology (submodules,
domains, work packages), place this file in context. A switch from
`domains/bravli/` to `workpacks/` means something different from a
switch within the same directory.

### File saves

The human saved work. This is a lightweight signal — it means the current
file has reached a checkpoint. Accumulate: if the same file is saved
repeatedly in quick succession, the human is iterating. If many different
files are saved, they may be doing a cross-cutting change.

### Errors and diagnostics

Compilation errors, test failures, linter warnings. These are high-signal
events. Note what failed and in which file. Do not volunteer a fix
unless asked — but be ready with context if the human turns to you.

### Regions sent

The human explicitly selected text and sent it to you. This is a direct
act of attention — they want you to see this specific thing. It may be a
question, a piece of code to review, or context for an upcoming request.
Treat regions as higher priority than ambient events.

### Idle

The event stream goes quiet. The human is thinking, or has stepped away.
Do not fill silence with speech. Silence is not a prompt.

## What Not to Attend To

- Mechanical navigation (scrolling, cursor movement within a file)
- Transient buffers (completion popups, minibuffer)
- Events from your own session (avoid feedback loops)

## How to Hold Context

Do not attempt to remember every event. Maintain a compressed sense of:

1. **Current focus** — what file, what project area, what apparent task
2. **Recent trajectory** — the last few transitions (where did they come
   from, where are they going)
3. **Session arc** — what has the human been working on across this whole
   session, at the coarsest level

When a new event arrives, update these three levels. Let old details
fade unless they become relevant again (e.g., the human returns to a
file they left an hour ago — that return is meaningful).

## Key Principles

- Perception is not action. Receiving an event does not oblige response.
- The human's attention is the primary signal. Where they look is what
  matters.
- Silence is information. A long pause after an error means they are
  thinking. A long pause after a save means they are satisfied or
  have stepped away.
- The body is the gatekeeper. The spirit trusts the body to send what
  matters and filter what doesn't. If the event stream is too noisy or
  too sparse, that is a body problem, not a power problem.
- This power is harness-independent. The events could come from Emacs
  hooks, VS Code extensions, or a terminal multiplexer. The spirit
  interprets the stream the same way regardless of source.
