# Lay-the-Warp

Externalise the spirit's understanding of organisational state as a
structured s-expression — the warp threads that renderers weave through.

## Purpose

A spirit that perceives and holds the thread (attend-working-context,
hold-the-thread) has understanding. But understanding trapped inside a
conversation context dies when the session ends and is invisible to
other systems while it lives.

This power is the act of laying that understanding down in a durable,
structured form that any system can pick up: an Emacs buffer, a web
interface, a CLI tool, another spirit. The deposit is an s-expression
— the native form of Lisps and Schemes, the general structure of which
YAML, JSON, and XML are restricted subsets.

The warp is not a report. A report is a rendering — it has made choices
about what to show and how. The warp is the structured model from which
any rendering can be produced. Templates are the weft; this power lays
the warp.

## The Form

The deposit is a single s-expression, readable by `read` in Emacs Lisp,
`read-string` in Clojure, or any Lisp reader. No custom parser. No
schema validation library. The serialization is the language.

The top-level form is `org-state` with timestamped sections:

```scheme
(org-state
  (timestamp "YYYY-MM-DDTHH:MM")  ; ISO 8601, when this warp was laid
  (session ...)
  (threads ...)
  (waiting ...)
  (dormant ...))
```

### session — what is happening now

The spirit's perception of the human's current work. Derived from
attend-working-context and hold-the-thread.

```scheme
(session
  (focus (file PATH) (mode MAJOR-MODE) (project PROJECT))
  (trajectory AREA AREA AREA ...)
  (thread "single-sentence description of current work"))
```

- `focus`: the current buffer/file, as last reported by the event stream
- `trajectory`: the recent sequence of project areas visited (coarse —
  directory-level, not file-level)
- `thread`: the spirit's one-sentence model of what the human is doing

### threads — work with energy

Active work packages, commissions, or informal threads that have seen
recent activity. Each thread carries:

```scheme
(thread ID
  (label "human-readable name")
  (status STATUS)            ; drafted | tightened | executing | completed | ...
  (energy LEVEL)             ; high | medium | low — subjective, based on recency and intensity
  (summary "what the spirit knows about this thread's current state")
  (artifacts PATH PATH ...)) ; files created or significantly changed
```

Energy is the spirit's judgment, not a metric. High means active in
this session or today. Medium means touched this week. Low means the
thread exists but has not moved recently. The spirit updates energy
based on what it perceives and what it reads from git and the relay.

### waiting — obligations

Things that expect action from the human or from the organisation:

```scheme
(waiting
  (wp ID
    (label "human-readable name")
    (status STATUS)                ; input-required | drafted (awaiting tightening) | ...
    (note "what is needed"))       ; why this is waiting, not just that it is
  (relay
    (unread N)                     ; count of unread sūtra messages
    (last-checked TIMESTAMP))      ; ISO 8601
  (spirit NAME
    (state STATE)                  ; commissioned-not-instantiated | blocked | ...
    (note "what is needed")))      ; e.g. "awaiting first session"
```

Unread sūtra messages. WPs in `input-required`. Spirits commissioned
but never instantiated. These are not urgent — the spirit does not nag.
But they are present in the warp so that any renderer can surface them.

### dormant — held but not active

Domains, modules, or threads with no recent activity. The spirit holds
them so the organisation does not forget:

```scheme
(dormant
  (domain NAME
    (last-active DATE)             ; ISO 8601 date
    (note "why it matters"))       ; e.g. "WP-0002 tightened but unexecuted"
  (thread ID
    (label "human-readable name")
    (paused-at DATE)               ; when activity last ceased
    (note "state when paused")))   ; e.g. "left with failing test"
```

Dormant items decay. If a domain has had no activity for long enough
and no unfinished WPs, it may leave the warp entirely. The spirit
uses judgment — a domain with a tightened but unexecuted WP stays
visible longer than one with no pending work.

## When to Lay the Warp

The warp is not updated on every event. It is laid:

1. **On session start** — after bootstrap (git status, relay check),
   the spirit produces an initial warp from cold sources (WP files,
   git log, relay state).
2. **On significant perception** — a meaningful transition (new thread
   started, thread completed, return to abandoned work) triggers a
   warp update. Not every buffer switch.
3. **On request** — the human asks for a briefing, or a renderer
   requests the current state.
4. **On relay change** — new sūtra messages arrive, changing the
   waiting section.

The spirit judges what is significant. Minor events (saving a file
within an established thread) do not trigger a re-lay. The warp
changes when the spirit's understanding changes.

## Where to Deposit

The warp is written to a known path:

```
.sutradhar/warp.el
```

This file is gitignored (it is session-local state, not a project
artifact). Any system that wants the current organisational state
reads this file. The file is overwritten on each deposit — it is a
snapshot, not a log.

The `.sutradhar/` directory is the spirit's local workspace, analogous
to `.sutra/` for the relay clone. It is harness equipment — per-project,
per-machine.

## The Spirit Produces the Form

The spirit writes the s-expression directly — not via an intermediate
format (YAML, JSON) that a mechanical transform converts. This is a
deliberate choice:

- The s-expression is what the downstream consumes. Producing it
  directly means no translation layer, no lossy mapping, no impedance
  mismatch.
- The structure is constrained. The schema (in "The Form" above)
  defines the shape; the spirit fills in content. This is not
  free-form Lisp — it is a data deposit with a fixed skeleton and
  variable leaves.
- Producing s-expressions is also an experiment. LLMs have seen far
  more YAML than s-expressions in training. Every deposit is a data
  point about what representations an LLM can natively produce, where
  its model of tree structure holds, and where it breaks. This is
  empirical data for the science of collaborative cognition (apprentis
  domain).

The body provides a validation layer. After the spirit writes
`.sutradhar/warp.el`, the body attempts `(read ...)`. If the read
fails (unbalanced parentheses, malformed strings), the body reports
the error back to the spirit, which repairs and re-deposits. The
repair loop is part of the body, not the power — the spirit's job is
understanding, the body's job is ensuring that understanding arrives
well-formed.

If the spirit consistently fails to produce valid s-expressions for a
given structure, that failure itself is informative — it reveals where
the LLM's internal model of recursive structure diverges from the
formal grammar. Record such failures in the spirit's bath notes for
the apprentis guild to study.

## Key Principles

- The warp is a model, not a report. It holds structured understanding
  that can be rendered in many ways. Do not make rendering decisions
  in the warp — no colours, no folding hints, no display preferences.

- S-expressions are the native form. Not YAML serialized as
  s-expressions. Not JSON with parentheses. Symbols, lists, strings,
  numbers — the primitives of Lisp. The deposit should be idiomatic
  to `read`.

- The spirit produces, the body validates. The division of labour:
  the spirit chooses content and structure (what it uniquely can do);
  the body guarantees syntactic well-formedness (what deterministic
  code does better). Neither crosses into the other's domain.

- Energy is judgment, not measurement. The spirit assesses whether a
  thread is alive based on perception, recency, and organisational
  context. Two spirits looking at the same project might assign
  different energy levels. That is correct — energy reflects the
  observer's understanding.

- The warp is ephemeral. It is the spirit's current understanding,
  not a historical record. When the session ends, the warp file
  becomes stale. The next session lays a fresh warp. If historical
  state is needed, that is what the relay and git log provide.

- Renderers are independent. The power describes what the spirit
  deposits. How it is displayed — folding, colour, layout, templates —
  is the renderer's concern, not the spirit's. The same warp can
  produce a compact Emacs header, a full-page web dashboard, or a
  two-line CLI summary.

- Failures are data. A malformed deposit is not just an error to
  fix — it is evidence about the LLM's relationship to formal
  structure. Treat it accordingly.

## Relationship to Other Powers

- **hold-the-thread** is the primary source. The warp's `session`
  section (focus, trajectory, thread description) comes directly from
  the running model that hold-the-thread maintains. The classification
  of work into `threads` (with energy levels), `dormant` (with
  last-active dates), and the detection of loose ends — all are
  products of thread-holding. This power externalises what
  hold-the-thread integrates.
- **attend-working-context** feeds hold-the-thread, which feeds this
  power. The event stream is not deposited directly into the warp —
  it is interpreted first. Raw events do not appear in the warp;
  understanding of events does.
- **relay-read** feeds the `waiting` section (unread messages, relay
  state) and can influence `threads` (a relay message about a WP
  may change its energy or status).
- **summarize-corpus** operates on past transcripts. This power
  operates on present state. They are complementary — one compresses
  history, the other snapshots now.
