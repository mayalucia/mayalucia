# Gaddi

Shepherd a sequence of prompts through a gptel buffer, waiting for
each response to complete before injecting the next.

## Purpose

Some tasks require a multi-turn dialogue with a substrate: an
orientation prompt, then a task brief, then a reflection question.
A spirit orchestrating this sequence cannot interrupt the stream —
doing so corrupts the response. The gaddi waits for the flock to
settle, then speaks.

Named for the nomadic shepherds of Dhauladhar and Pir Panjal who
walk with their flocks across high passes. The gaddi does not own
the pasture at either end. It traverses.

## When to Use

- Orchestrating substrate diversity experiments (sequential sessions
  with different LLMs)
- Running a multi-prompt protocol on a single gptel buffer (e.g.,
  task brief → reflection → self-assessment)
- Any situation where you need autonomous prompt sequencing without
  human intervention between turns

## Mechanism

The gaddi deposits a buffer-local prompt queue, registers a hook on
`gptel-post-response-functions`, and fires the first prompt. The hook
drains the queue one prompt at a time. Tool-call chains cycle
internally (gptel's FSM handles TOOL → WAIT → TYPE loops); the hook
only fires at terminal states (DONE, ERRS, ABRT).

```
gaddi-start(buffer, prompts)
  → fires prompt-1
    → substrate responds (tool calls cycle internally)
      → DONE → 1s delay → fires prompt-2
        → substrate responds
          → DONE → queue empty → finish
```

On transient errors (rate limits, server errors): retry up to
`gaddi-max-retries` times with `gaddi-retry-delay` between attempts.
On fatal errors or abort: halt the queue, log the failure.

A watchdog timer (`gaddi-timeout-seconds`, default 600s) catches
silent failures where no response arrives. If the buffer is still
growing when the watchdog fires (substrate composing slowly, not
stuck), the deadline extends up to `gaddi-timeout-extensions` times
(default 3) before halting. This prevents premature termination of
thorough survey tasks on slow API paths.

## Procedure

### 1. Prepare the buffer

The gptel buffer must exist with:
- `gptel-mode` enabled
- Backend and model configured for the target substrate
- System prompt / preamble in place
- Tools enabled if the substrate needs them

The gaddi does not create buffers or configure models. It shepherds
prompts through a buffer that is already prepared.

### 2. Deposit the prompt queue

Call `gaddi-start` with the buffer and a list of prompts:

```elisp
(gaddi-start
 (get-buffer "session.org")
 '((:name "task-brief" :text "Read the power and survey the gaps...")
   (:name "reflection" :text "Reflect on what you just did...")))
```

Prompts can be bare strings (auto-named prompt-1, prompt-2, ...) or
plists with `:name` and `:text`.

### 3. Walk away

The gaddi drains the queue autonomously. No emacsclient round-trips
during execution. The shepherd watches from the ridge.

### 4. Check progress

```elisp
(gaddi-status (get-buffer "session.org"))
```

Returns an s-expression:

```elisp
(gaddi-status :active nil :completed 2 :remaining 0
 :current nil
 :log ((:name "task-brief" :state DONE)
       (:name "reflection" :state DONE)))
```

### 5. Abort if needed

```elisp
(gaddi-abort (get-buffer "session.org"))
```

## What This Power Is Not

- **Not a session manager** — it doesn't create buffers, configure
  models, or choose substrates. Those decisions belong to the spirit
  exercising the power.
- **Not a response analyzer** — it doesn't judge whether a response
  is good. Tool processing failures are data, not errors. The gaddi
  logs them and moves on.
- **Not a framework** — it's a body function, under 120 lines of
  elisp. The power is the pattern: deposit, drain, wait, advance.

## Body

`~/.doom.d/gaddi.el` — Emacs harness body. Loaded via `gptel.org`.
