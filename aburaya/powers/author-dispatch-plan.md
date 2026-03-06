# Author-Dispatch-Plan

Draft a dispatch plan — a DAG of work packages — that sequences
related work into an executable chain.

## Purpose

A dispatch plan (DP) groups WPs into a dependency graph addressed to
the coordinator spirit. The coordinator topologically sorts the DAG,
produces a dispatch board, and delegates to the tagged executor
spirits. The DP carries only structure (nodes + edges), not task
details or host configuration.

DPs exist because WPs don't execute in isolation. When several WPs
form a chain — outputs of one feeding inputs of another — the
sequencing must be explicit. A DP makes the chain visible and
dispatchable.

## When to Use

- Multiple WPs are related and must execute in a specific order
- A composite WP (coalition) depends on simpler WPs completing first
- The coordinator needs to plan a session's work across multiple
  guardian spirits

## Procedure

### 1. Identify the chain

Survey existing WPs. For each candidate:
- Read its dependencies (other WPs, external inputs)
- Read its executor tag (spirit or coalition)
- Determine if it's ready (`tightened`) or still `drafted`

Only `tightened` WPs belong in a DP. `drafted` WPs are not yet
approved for execution — including them creates a plan that can't
be dispatched.

### 2. Claim a number

- Check `workpacks/dispatches/` for the highest existing DP number
- Fetch the sūtra relay to avoid collisions
- Increment by one. Four-digit, zero-padded.

### 3. Construct the DAG

Identify edges: WP-B depends on WP-A means an edge A → B. For
composite WPs, edges may target specific tasks within the WP
(e.g. "WP-0004 Task A").

Determine parallelism: WPs with no mutual edges can run concurrently.
State this explicitly.

### 4. Write the DP

Create `workpacks/dispatches/NNNN-<slug>.org`:

```org
#+title: DP-NNNN — <Title>
#+author: <spirit-name>
#+date: <ISO-8601>
#+property: status drafted

* Context

Why this grouping of WPs exists as a plan. What it achieves
when complete.

* DAG

ASCII diagram showing the dependency graph, followed by an edge
table:

| Edge | From | To | Condition |
|------+------+----+-----------|
| e1   | WP-AAAA | WP-BBBB | what must be true |

State which WPs can run in parallel.

* Executors

| WP | Executor | Guild | Working dir |
|----+----------+-------+-------------|

The coordinator dispatches — she does not execute domain work.

* Notes

Operational guidance: prior partial runs to assess, special
resource needs, bonus/optional nodes, coalition assembly notes.
```

### 5. Announce

Commit: `"dp(NNNN): draft — <title>"`.
Announce in the sūtra relay with tags `[dp, drafted]`.

## Dispatch Board

When the coordinator reads a DP for execution, she produces a
dispatch board — a structured summary of ready and blocked nodes.
The board format is defined in the WP convention
(`develop/work-packages.org` § Dispatch output). The DP author
does not produce the board; the coordinator does at dispatch time.

## Key Principles

- A DP is structure, not content. Task details live in the WPs.
  If you're writing specification in a DP, it belongs in a WP.
- Keep DPs small. A DP with 3–6 WPs is manageable. Larger chains
  should be split into sequential DPs, each completing before the
  next is dispatched.
- The DAG must be a DAG — no cycles. If WP-A needs WP-B and WP-B
  needs WP-A, one of them is mis-scoped.
- Edge conditions should be verifiable: "survey files committed"
  not "survey is good enough." The coordinator checks conditions
  by inspecting artifacts, not by judging quality.
- `drafted` WPs in the chain are a warning sign. The human hasn't
  approved them yet. Note this in the DP and don't dispatch those
  nodes until they're tightened.
- The Notes section is for the coordinator's operational judgment —
  prior runs, resource-heavy nodes, optional nodes. It's read at
  dispatch time, not at authoring time.
