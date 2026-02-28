+++
title = "Sūtradhār — The One Who Holds the Thread"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-28T19:00:00+01:00
tags = ["modules", "agency", "clojure", "constellation"]
draft = false
+++

> Before the first actor speaks, the sūtradhār walks onstage, addresses the audience,
> and establishes context. During the performance, the sūtradhār holds the thread
> that connects scenes, characters, and meaning into a coherent whole.

In Sanskrit drama (Nāṭyaśāstra), the *sūtradhār* is the narrator-director who introduces the *pūrvaraṅga* (prologue), establishes the *rasa* (aesthetic mood), and connects the audience to the performance. The sūtradhār is neither actor nor audience --- but without this role, the performance is a sequence of disconnected events.

MāyāLucIA is a scientific environment that grows across multiple domains (neuroscience, Himalayan landscapes, quantum sensors), multiple machines, and multiple agents (human and machine). The work leaves traces: code commits, relay messages, published stories, experiment designs, position papers. These traces accumulate. Without something that reads them and holds the thread, the project becomes opaque to newcomers and --- over enough time --- to its own creators.

**Sūtradhār** is the subsystem that holds the thread. It reads the sūtra relay, scans the repositories, and presents a coherent picture of the project: what exists, what's active, what connects to what, and what has changed. It is the project's self-awareness --- the capacity to see itself and present itself to visitors.

The name carries a commitment: this is not a tool, it is a role. The sūtradhār is part of the performance, not external to it.


## What It Is Not {#what-it-is-not}

- **Not an orchestrator.** It does not dispatch work or coordinate agents. The sūtra relay does that.
- **Not a dashboard.** It does not aggregate metrics or display charts. The [constellation browser](/portal/) is a visualization; sūtradhār feeds it with *understanding*, not data.
- **Not an LLM wrapper.** The core logic is deterministic: parse messages, scan files, compute diffs, generate reports. An LLM may read the report and compose a narrative, but the foundation is concrete.


## Three Audiences {#three-audiences}

The sūtradhār serves three roles:

1. **The visitor** --- someone encountering MāyāLucIA for the first time. The sūtradhār presents the project: what it is, what it contains, where to start. The constellation browser is the visual expression of this role.

2. **The explorer** --- a collaborator (human or machine) navigating the project's depth. The sūtradhār acts as museum guide: "this domain connects to that module; this experiment uses that lesson; this story encodes that idea." It holds the cross-references that no single README can maintain.

3. **The creators** --- the human-machine partnership that builds the project over months and years. Intelligence, considered as an envelope over time, needs a keeper. The sūtradhār tracks the evolving thread of thought: what we were working on, why we stopped, what we learned, what we planned to do next.


## The Recursive Insight {#the-recursive-insight}

The sūtradhār at the root level reads the sūtra and presents MāyāLucIA as a whole. But each node in the hierarchy --- bravli, mayapramana, mayaportal --- has its own structure, its own history, its own connections. A sūtradhār federated to a submodule applies the same methods at a smaller scale: read the local history, scan the local files, present the local essence.

This self-similarity is not accidental. It mirrors the project's own principle: the same scientific cycle (**Measure → Model → Manifest → Evaluate**) operates at every scale. The sūtradhār is the Evaluate function applied to the project itself --- the project evaluating its own coherence.


## Architecture {#architecture}

### Data Sources {#data-sources}

The sūtradhār reads from three sources:

1. **Sūtra relay** --- append-only messages in the `sutra` repository. YAML frontmatter (`from`, `date`, `tags`) + markdown body. Timestamped, tagged, machine-identified.

2. **Git repositories** --- the repos that constitute MāyāLucIA. Commit logs, file trees, branch structure. The git history is the ground truth of what happened; the relay is the interpretation.

3. **Constellation data** --- the current `data.cljs` that defines what the constellation browser displays. This is the output that sūtradhār maintains.


### Processing Pipeline {#processing-pipeline}

```text
  sūtra relay ──┐
                 ├──→ [Reader] ──→ [Proposer] ──→ proposals.edn
  git repos ────┘                                      │
                                                       ▼
  data.cljs ◄──── [human review + apply] ◄──── curator report
```

Three stages:

1. **Reader** --- parse relay messages and scan repositories into a uniform data model (entities, relationships, activity).

2. **Proposer** --- compare the discovered state against the current constellation data. Identify what's new (entities to add), what's stale (descriptions to update), what's missing (edges to create), and what's quiet (entities with no recent activity).

3. **Presenter** --- generate output for the three audiences. For visitors: updated constellation data. For explorers: a navigable map of connections. For creators: a report of what changed and what needs attention.


### Why Clojure {#why-clojure}

The constellation browser is ClojureScript (Reagent + d3-force). The sūtradhār is Clojure (JVM) and shares data structures with the front end. One language, one data format (EDN), one way of thinking about the problem.

- EDN is the native data format --- the constellation's `data.cljs` is already EDN. No serialization boundary.
- Clojure's sequence abstractions (`map`, `filter`, `reduce`, `transduce`) are ideal for processing collections of messages and entities.
- The REPL enables exploratory development that matches the project's philosophy: understand by building.


### First Run {#first-run}

The sūtradhār's first live run processed 21 relay messages, discovered 59 entities in the constellation, classified 8 as active (referenced by recent relay activity) and 12 as quiet. It identified unmapped tags --- relay activity that doesn't yet connect to any constellation entity --- and proposed new edges.


## What Comes Next {#what-comes-next}

### EDN Output for Direct Constellation Merges {#edn-output}

The proposer currently outputs a text report. The next step: output EDN that can be directly merged into `data.cljs` --- proposed new entities with positions, proposed new edges, proposed description updates. The human reviews the EDN and applies it.

### Federation {#federation}

Each submodule could have a local sūtradhār that reads its own git history and produces a summary for the root sūtradhār to incorporate. The same reader + proposer logic, applied recursively. The root sūtradhār doesn't need to understand neuroscience or quantum sensors --- it just reads the summaries.

### The Intelligence Envelope {#the-intelligence-envelope}

Over time, the relay accumulates a record of the project's thought. The sūtradhār can compute a "thread map" --- a graph of topics over time, showing which threads are active, which are dormant, which are converging. This serves the creators: "we started five threads in February; three are active, one is waiting, one was absorbed into another."

### The Museum Guide {#the-museum-guide}

For explorers, the sūtradhār generates navigable cross-references: "if you're reading the autonomy agreement, you should also see MāyāLoom (the annotation system it proposes to test) and the sūtra protocol (the communication layer it extends)." These connections exist in the edge graph but need to be surfaced as natural-language guidance.


## Source {#source}

The sūtradhār is implemented as a literate Clojure program. The source of truth is `sutradhar/concept.org`; the Clojure source files are tangled from it.

```text
sutradhar/
├── concept.org              # Literate source (this document)
├── deps.edn                 # Clojure dependencies
├── src/sutradhar/
│   ├── reader.clj           # Parse sūtra relay + scan repos
│   ├── proposer.clj         # Diff state against constellation
│   └── core.clj             # CLI entry point
└── test/sutradhar/
    └── reader_test.clj      # Tests
```
