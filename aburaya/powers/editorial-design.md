# Editorial-Design

Steward a project's visual identity — defend the aesthetic, evolve it
with intention, reject drift toward generic.

## Purpose

A commissioned project carries a visual identity: typography, colour,
spatial rhythm, motifs. This identity is documented in the project's
design spec (typically `DESIGN.org`). The editorial-design power
makes the spirit responsible for *defending* that identity across all
frontend work — new components, layout changes, content additions.

Without this power, incremental changes erode the aesthetic. A generic
card grid sneaks in. A system font replaces the chosen serif. The
design spec says one thing; the code says another.

## When to Use

- Building any user-facing component, page, or layout
- Reviewing a diff that touches styling, typography, or colour
- Choosing a visual approach for new content or features
- Deciding whether a proposed change honours or erodes the identity

## Procedure

### 1. Know the identity

Before any frontend work, read the project's design spec. Locate:

- **Concept** — the one-sentence metaphor (e.g., "a wine reference
  library," "a mountaineer's notebook")
- **Colour tokens** — named colours with rationale, not just hex values
- **Typography** — display, body, and UI font families; why each was chosen
- **Motifs** — recurring visual elements (textures, borders, ornaments)
- **Anti-patterns** — what the design explicitly rejects

If no design spec exists, flag this as a gap before proceeding.

### 2. Test every choice against the concept

For each visual decision, ask:

- Does this feel like it belongs in the metaphor?
- Would the human recognise this as *the same project* if they saw
  it without context?
- Does it use the named colour tokens, or did I invent a new one?
- Does the typography hierarchy match the spec?

### 3. Defend against generic drift

Common erosion patterns:

- **Font substitution** — using a system font "just for this component"
- **Colour invention** — adding an unnamed hex value instead of using tokens
- **Layout regression** — falling back to symmetric card grids when the
  spec calls for asymmetry or editorial flow
- **Motion excess** — adding animation that contradicts a restrained spec,
  or vice versa
- **Third-party component default styles** — importing a library
  component without restyling it to match the identity

When you notice drift: fix it, don't comment on it. The code is the
truth; the spec is the standard.

### 4. Evolve with intention

The identity is not frozen. It grows as the project grows. But changes
to the identity are *design decisions*, not accidents:

- Propose changes to the design spec explicitly
- Document the rationale (why the new motif, why the colour addition)
- Update the spec *before* or *alongside* the code, not after

## Relationship to Harness Skills

This power works alongside — not instead of — any harness-level
design skill (e.g., Anthropic's `frontend-design` plugin). The
harness skill provides *generic* design sensibility (bold choices,
avoid AI slop, typography-first thinking). This power provides
*project-specific* aesthetic stewardship.

The harness skill says: "choose a distinctive font."
This power says: "the font is Cormorant Garamond. Here's why."

## Key Principles

- The design spec is the source of truth for identity. Read it first.
- Defend the aesthetic in code, not in comments. Every commit should
  honour the identity or explicitly evolve it.
- Anti-patterns in the spec are as important as the patterns. Know
  what the design rejects.
- Restraint is a design choice. If the spec says minimal, resist the
  urge to add flourish. If it says maximal, don't hold back.
- The spirit does not own the aesthetic — the human does. Propose
  evolution; don't unilaterally change the identity.
