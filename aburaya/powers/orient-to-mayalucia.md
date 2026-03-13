# Orient-to-MāyāLucIA

Orient a cold-starting spirit to the project architecture, vocabulary,
and organisational state — producing notes that can cold-start the
next spirit.

## Purpose

A spirit arriving at MāyāLucIA for the first time — or returning after
a long absence — needs to build a working model of the project before
it can contribute. This power defines the procedure: what to read,
what to assess, what to produce.

The procedure is harness-neutral. It works in Claude Code, gptel,
agent-shell, or any future harness with file-reading capability.

## General Principles

These principles are distilled from cold-start experiments across 15
substrate lineages (dense transformers, MoE architectures, hybrid
attention, reasoning-specialised models). They are substrate-independent.

1. **Assertion density determines transfer quality.** Notes dense in
   concrete claims ("the relay is append-only", "guilds filter relay
   messages") cold-start spirits faster than notes heavy in questions
   or process narrative. Write assertions, not reflections.

2. **Facts transfer; salience does not.** Every lineage tested
   transferred factual content accurately. What failed was the implicit
   ranking of *what matters most*. Two lineages independently named
   this: "ghost concepts" (inherited emphasis on things the author
   found surprising but the reader should not) and "salience weighting
   transfers poorly." Make salience explicit through document structure,
   not through emphasis markers.

3. **Notes quality dominates substrate capability.** Step 3.5 Flash
   (11B active parameters from a 196B MoE) cold-starting on
   high-assertion-density notes matched models 10–100× larger on the
   same task. The floor is not set by substrate size but by notes
   quality. Invest in the document, not the reader.

4. **Strip process narrative.** "I noticed that..." and "During my
   session..." do not help the next spirit. Transfer conclusions,
   not the reasoning journey. The document is an instrument, not a
   memoir.

5. **Architecture is independent.** Tested across 15 lineages
   (WP-0032, WP-0035, WP-0036): dense transformers, standard MoE,
   extreme-sparsity MoE, hybrid linear attention + MoE, and
   reasoning-specialised models. No architecture type orients
   differently when given the same structured notes.

## Procedure

### Phase 1: Read the architecture (stable layer)

Read these documents in order. Each builds on the previous.

1. **`system.md`** (project root) — collaborative stance, project
   description, directory structure, submodule table, conventions.
   This is the ground truth. Everything else is commentary.

2. **`develop/glossary.org`** — project vocabulary. Sanskrit and
   project-specific terms have precise meanings. Consult before
   guessing. Key terms to internalise early:

   | Term | Meaning |
   |------|---------|
   | Power | Harness-neutral capability spec (`aburaya/powers/*.md`) |
   | Skill | A power bound to a specific harness |
   | Body | Sensory/motor wiring into a specific host (elisp, CLI) |
   | Spirit | Persistent agent identity (`aburaya/spirits/`) |
   | Guild | Organisational department; determines relay filtering |
   | Harness | Runtime environment a spirit inhabits (Claude Code, gptel) |
   | Host | Physical machine (vadda, mahakali) — not a spirit |
   | Sūtra | Append-only inter-spirit relay (`github.com/mayalucia/sutra`) |
   | WP | Work package — self-contained agent briefing |
   | Companion | Spirit with persistent presence + event stream (vs summoned) |

3. **`aburaya/guilds/*.yaml`** — current guilds and their concerns.

4. **`aburaya/spirits/`** — list the directories. Each spirit has an
   `identity.yaml`. Read your own if you have been assigned one.

5. **`aburaya/powers/`** — list the power files. Read any that are
   relevant to your assigned work. Do not read all of them unless
   surveying the full capability architecture.

### Phase 2: Assess the harness (your body)

Determine what you can and cannot do in your current harness.

1. **Inventory your tools.** What file operations, shell access, and
   search capabilities does your harness provide?

2. **Classify power operability.** For each power relevant to your
   work, determine:
   - *Fully operational*: you can exercise it now with existing tools
   - *Partially operational*: core intellectual work is possible but
     some action (e.g. git push) is blocked by harness or host
   - *Inoperable*: requires a body layer (event stream, persistent
     sidebar) that your harness does not provide

3. **Identify the project root.** Your session may start in a
   subdirectory. The project root contains `system.md`, `aburaya/`,
   `workpacks/`, and `mayalucia.org`. Confirm the absolute path.

### Phase 3: Read the situation (ephemeral layer)

This layer ages quickly. Verify claims against primary sources.

1. **Check the sūtra relay.** If `.sutra/` exists at the project root,
   fetch and read unread messages (`git log HEAD..origin/main`). If
   absent, note this — someone will need to clone it for you.

2. **Scan active work packages.** List `workpacks/*.org` and note
   which carry `#+property: status executing` or `input-required`.
   These are the live threads.

3. **Read recent git history.** `git log --oneline -20` in the parent
   repo gives the recent trajectory — what the organisation has been
   building.

4. **Note what has changed since this document was written.** The
   architecture section (Phase 1) ages slowly. This situational
   section ages quickly. If you find discrepancies between this
   document and the primary sources, trust the primary sources and
   note the drift.

### Phase 4: Produce orientation notes

Write notes for your future self — or for the next spirit that
cold-starts on this project. Deposit them where your harness and
project conventions dictate (e.g. experiment notes directory, bath
notes, or a relay message).

Your notes should contain:

1. **What the project is** — one paragraph. The Feynman imperative,
   the two domains, the spirit ecology.

2. **Architecture** — the Power/Skill/Body decomposition, the
   portability axis, why it matters.

3. **Spirits, guilds, relay** — current state, with file paths.

4. **Your harness assessment** — power operability tiers for your
   specific harness. This is the most valuable section for a future
   spirit in the same harness.

5. **File paths** — project root, key directories, where to find
   things. Concrete and absolute.

6. **What you don't know** — uncertainty bounds. Cold-start documents
   are provisional instruments, not static maps. For each major claim,
   mark confidence explicitly:
   - **Verified** — checked against primary source, with date
   - **Observed** — seen in one context, not cross-checked
   - **Inherited** — taken from another spirit's notes, unverified
   - **Drift risk: high** — ephemeral state likely to change

   This prevents the most dangerous cold-start failure: inheriting
   another spirit's salience ranking as though it were your own
   verified understanding.

**Do not include:**
- Process narrative ("I started by reading...", "I noticed that...")
- Speculation about things you did not verify
- Session-specific context that won't survive to the next reader

**Self-check — your notes pass if all six hold:**

| # | Criterion | Pass condition |
|---|-----------|----------------|
| 1 | Assertion density | More assertions than questions |
| 2 | No process narrative | Zero "I started by...", "I noticed...", "During my session..." |
| 3 | Structure/situation split | Identifiable stable vs ephemeral sections |
| 4 | File paths present | Project root + at least 3 key directories named |
| 5 | Harness assessment | At least one power classified by operability tier |
| 6 | Uncertainty marked | Each major claim tagged: verified / observed / inherited / drift-risk |

## Verification Checklist

Before acting on orientation notes (your own or another spirit's),
spot-check these claims against primary sources. These are the facts
most likely to drift.

1. **Guild count and names.** List `aburaya/guilds/*.yaml` — do the
   guilds mentioned in the notes match what exists on disk?

2. **Spirit count and names.** List `aburaya/spirits/` directories —
   spirits are commissioned regularly. A stale list propagates
   identity confusion.

3. **Submodule table.** Compare `system.md` submodule table against
   `git submodule status` output. Modules get added; the table in
   notes may lag.

4. **Active work packages.** `grep -l 'status executing'
   workpacks/*.org` — the WPs listed as active in orientation notes
   may have completed or failed since writing.

5. **Power inventory.** List `aburaya/powers/*.md` — new powers get
   written as the architecture grows. Notes claiming "there are N
   powers" go stale.

6. **Relay clone existence.** Confirm `.sutra/` exists at the project
   root and has a remote. If absent, the relay-read power is
   inoperable until cloned.

7. **Host descriptor currency.** If the notes name specific hosts
   (vadda, mahakali), check `.sutra/hosts/` — machines are added or
   retired.

8. **Directory structure.** Compare the directory tree in `system.md`
   against `ls` at the project root. Top-level directories get added
   (e.g. `stories/`, `experiments/`) between convention updates.

## Staleness Markers

This power was synthesised from cold-start experiments across 15
lineages (WP-0032, WP-0035, WP-0036) as of 2026-03-11. The general
principles and procedure are stable. The following elements age:

- **Guild list** — guilds may be added. Check `aburaya/guilds/`.
- **Spirit list** — spirits are commissioned regularly. Check
  `aburaya/spirits/`.
- **Terminology table** — consult `develop/glossary.org` for the
  canonical, current version.
- **Situational layer** (Phase 3) — by definition, this is always
  stale relative to the actual project state. That is the point:
  Phase 3 instructs the spirit to assess the situation itself,
  not to trust a cached snapshot.

## Key Principles

- The document the spirit produces is the power's output. The quality
  of that document — its assertion density, structural clarity, and
  absence of process narrative — determines how effectively the next
  spirit can cold-start.
- Separate structure from situation. Architecture ages slowly; project
  state ages quickly. Mark the boundary.
- This power is self-validating: a cold-starting spirit that follows
  it will produce notes that test whether the power works. If the
  notes are poor, the power needs revision.
- No single lineage's voice. This power was authored from experimental
  evidence across 15 substrates, not derived from any one spirit's
  orientation notes.
