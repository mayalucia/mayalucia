# Author-WP

Draft a work package from context — situation, existing assets,
and desired outcome.

## Purpose

A work package is a self-contained briefing: tight enough for an
autonomous agent to execute without clarification, rich enough for
a human to review and approve. Writing a good WP requires surveying
what exists, articulating what's needed, and specifying acceptance
criteria that leave no ambiguity.

This power produces WPs in `drafted` state. The human tightens.

## When to Use

- A spirit identifies work that needs doing within its scope
- The coordinator spirit (mayadev) breaks a large goal into WPs
- A guardian spirit proposes work via the sūtra relay — the WP
  is the formal proposal

## Procedure

### 1. Survey the situation

Before writing, gather:
- What already exists (code, docs, prior WPs)
- What is broken or missing
- Who cares about the outcome and why
- Dependencies on other WPs or external inputs

### 2. Claim and reserve numbers

- Fetch the sūtra relay (`git fetch` in `.sutra/`, read new messages)
- Check both `workpacks/` on disk and recent relay messages for the
  highest existing or reserved number
- Increment from the highest. Four-digit, zero-padded.
- **Reserve before drafting.** Push a relay message with tag
  `wp-reserve` listing the numbers you intend to use. This is
  especially important when drafting multiple WPs in a burst.
  A reservation message is lightweight — just numbers and one-line
  titles:

```
tags: [wp-reserve]
---
Reserving WP-0022 through 0025 for DMT-Eval Phase 1.

| WP | Working title |
|----|---------------|
| 0022 | CLI + PyPI |
| 0023 | LLM adapter |
| 0024 | MCP server |
| 0025 | Finance domain |
```

- Only then begin drafting. The reservation narrows the collision
  window from drafting time (minutes–hours) to push latency (seconds).
- If your push is rejected (another agent reserved simultaneously),
  fetch, renumber, and re-reserve. No drama.

### 3. Write the WP

Create `workpacks/NNNN-<slug>.org` with this structure:

```org
#+title: WP-NNNN — <Title>
#+author: <spirit-name>
#+date: <ISO-8601>
#+property: status drafted
#+property: executor <spirit or coalition>
#+property: type <simple | composite>

* Context and Motivation

/Why does this work exist?/

* Inventory (What Already Exists)

/What do we have?/ File paths, function signatures, known limitations.

* Specification (What You Build)

/Exactly what to create./ Concrete: paths, structure, contracts.

* Execution Order

/In what sequence?/ Dependencies between parts.

* Acceptance Criteria

/How do we know it worked?/ Checklist. Test commands, expected outputs.

* What This Proves

Include this section if the work is external-facing --- a library for open use, a website, a paper, a commission. If the work develops internal tooling we may not need this unless it as an experiment. Expect the human to give you instructions.

* Open Questions

The work will typically start with questions, and new questions will emerge as we work through. Include here things that could not be resolved in the drafting of this workpackage. The agentic spirit that executes the WP should flag these if they become blocking. DO NOT DECIDE SILENTLY.

* Tangles and Artifacts

Include this section if the work will tangle code or produce artifacts (reports, images, deployed services). List the file names to tangle to, and name the artifacts to produce.

```


### 4. Announce

Commit the WP: `"wp(NNNN): draft — <title>"`.
Announce in the sūtra relay with tags `[wp, drafted]`.

## Key Principles

- A WP is a briefing, not a design document. Be concrete, not
  reflective. An agent should be able to execute the Specification
  section mechanically.
- The Inventory section prevents reinvention. Survey before specifying.
- Acceptance Criteria are the contract. If you can't state when the
  work is done, the WP isn't ready to draft.
- `drafted` is an invitation for human review, not a commitment to
  execute. The human may revise heavily before tightening.
- For composite WPs, include a coalition table in the Execution Order
  section mapping tasks to spirits and their required powers.
- Numbering collisions happen in async systems. Fetch the relay,
  reserve your numbers, then draft. If a collision still occurs
  (simultaneous reservations), the later arrival renumbers. The
  human's morning sync reconciles any remaining drift.
