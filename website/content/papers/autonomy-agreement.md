+++
title = "The Missing Primitive — Autonomy Agreements for Human-Machine Collaboration"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-28T19:00:00+01:00
tags = ["papers", "autonomy", "collaboration", "philosophy"]
draft = false
+++

<div class="abstract">

Every framework for human-AI collaboration assumes a fixed relationship: the human
commands, the machine executes. This paper argues that the critical missing primitive
is not better tools or smarter agents --- it is a *negotiated, evolving agreement*
between human and machine about the scope and limits of machine autonomy. We ground
this proposal in cybernetics (Pask, Ashby, Beer, Bateson), pedagogy (Vygotsky, Freire,
Papert), and the philosophy of tacit knowledge (Polanyi, Ryle, Dreyfus, Indian
pramāṇa theory). A key observation: the pedagogy literature addresses only human-teaches-human.
Human-AI collaboration creates a 2&times;2 matrix with four quadrants, each with different
failure modes. The autonomy agreement is the first protocol designed to operate across
all four --- because negotiated trust and epistemic commitments are more fundamental
than the direction of instruction.

</div>

## The Problem {#the-problem}

In February 2025, an LLM could draft a literature review. By February 2026, it can derive equations, write and execute simulations, interpret results, and propose revisions to the hypothesis that motivated the simulation. The capability curve outpaces the trust model.

But the interaction model has not changed:

```
Human: [instruction]
Machine: [execution]
Human: [correction]
Machine: [revised execution]
```

This is the master-servant loop. Licklider (1960) already saw beyond it --- his "man-computer symbiosis" was mutualism, not hierarchy, with the critical frontier being *formulative thinking*: problems that cannot even be formulated without machine aid. Sixty-six years later, we are finally approaching Licklider's frontier, but our interaction model is still the instruction-execution loop he rejected.

The loop breaks when the machine is a *thinking partner* --- because thinking partners must be able to propose directions, challenge assumptions, work autonomously on sub-problems, and recognize the limits of their own competence. None of these are possible under instruction-execution. And none are safe without an explicit agreement about when and how they happen.


## Intellectual Lineage {#intellectual-lineage}

### Cybernetics: the conversation is the autonomy {#cybernetics}

**Pask's Conversation Theory** (1976): knowledge is not propositional content but *entailment meshes* --- relational structures where concepts derive meaning from their connections. Learning occurs when two systems converge toward shared understanding through recursive dialogue. The critical test is *teachback*: B teaches the concept back to A in a different way. Autonomy is not pre-assigned; it *emerges from conversational success*.

**Ashby's Requisite Variety** (1956): a controller must have at least as much variety as the system it controls. Applied here: *autonomy delegation is variety delegation*. Trust is calibrated variety.

**Beer's Viable System Model** (1972): each operational unit has maximum autonomy consistent with cohesion. The recursive structure embeds progressive disclosure: the more trust, the more variety passes through without intervention.

**Bateson's levels of learning** (1972): Learning I is trial-and-error within fixed parameters. Learning II (deutero-learning) is learning *to learn* --- changing the set of alternatives. The autonomy negotiation is about which *level of learning* to grant.


### Pedagogy: the scaffold must fade {#pedagogy}

**Vygotsky's Zone of Proximal Development** maps directly onto the autonomy gradient. But the recent concept of the *Zone of No Development* sounds a warning: when AI continuously mediates learning, cognitive struggle diminishes and autonomous reasoning atrophies.

**Freire's distinction** between *banking* and *dialogical* education is the sharpest critique applicable here. The banking model --- teacher deposits knowledge into passive student --- is precisely what the instruction-execution loop implements at scale. Dialogical education requires both to be subjects, both to be changed by the encounter.

**Papert's constructionism**: understanding emerges through the act of building. If the machine builds the artifact and the human merely approves it, the constructionist loop is broken.


### Knowledge beyond propositions: the tacit substrate {#tacit-substrate}

**Polanyi** (1966): "We know more than we can tell." All explicit knowledge rests on a tacit substrate. The collaboration occurs at the focal (explicit) surface, but the real work --- the feel for the problem, the physicist's intuition --- lives in the tacit ground, where AI collaboration is hardest.

**Indian pramāṇa theory** (Nyāya, Mīmāṃsā, Vedānta) offers the most articulated non-Western epistemological framework. Valid knowledge (*pramā*) arises through distinct *pramāṇa*: pratyakṣa (direct perception), anumāna (inference), śabda (authoritative testimony), upamāna (analogy). AI output most resembles śabda --- but śabda requires an *āpta* (trustworthy authority), and whether an AI qualifies as āpta is genuinely open.


## The Proposal {#the-proposal}

An autonomy agreement is a negotiated, evolving document between a human and a machine that specifies:

1. **Epistemic commitments** --- the rules of reasoning
2. **Autonomy levels** --- what the machine can do at each level
3. **Transition protocol** --- how levels change
4. **Invariants** --- hard constraints that override autonomy levels
5. **Audit requirements** --- what must be logged and when


### Autonomy Levels {#autonomy-levels}

Four named levels, applicable *per-aspect* of the work:

| Level | Machine role | Human role | Trust basis |
|-------|-------------|------------|-------------|
| **Apprentice** | Executes instructions, shows all work | Reviews everything, directs each step | None yet |
| **Colleague** | Proposes approaches, flags anomalies | Sets direction, adjudicates | Demonstrated competence |
| **Delegate** | Works autonomously within scope | Defines scope, audits selectively | Track record |
| **Collaborator** | Initiates inquiry, challenges assumptions | Engages as peer, retains veto | Deep mutual trust |


### Transition Protocol {#transition-protocol}

Level changes are **proposed** (either party), **bilateral** (both consent), **scoped** (per-aspect, not global), **logged** (every transition recorded), and **revocable** (either party can pull back at any time).

Machine-initiated de-escalation is a *feature*, not a failure:

```
[Turn 93, machine, meta/pull-back]
I'm seeing unexpected bifurcation structure near T2 = 100us.
This might be physical or numerical. I don't have enough
domain knowledge to distinguish. Pulling back to colleague
on the interpretation. Here's what I see: [data].
```

A collaborator who knows the limits of their competence is more trustworthy than one who doesn't.


### Invariants {#invariants}

Hard constraints that override autonomy levels --- Beer's S3 performing its audit function:

- Results that contradict established domain knowledge
- Numerical instability, convergence failure, NaN propagation
- The machine recognizing it's outside its competence
- Irreversible actions (publication, external communication, data deletion)
- Any result the machine cannot explain

When an invariant fires, the machine stops, logs the trigger, drops to apprentice, and waits.


## The Four Quadrants: Who Teaches Whom? {#four-quadrants}

The pedagogy researchers all thought about one configuration: human teaches human (H→H). But human-AI collaboration creates a 2×2 matrix:

|              | **Student: Human**                       | **Student: AI**                            |
|--------------|------------------------------------------|--------------------------------------------|
| **Teacher: H** | Classical pedagogy (Pask, Vygotsky, Freire) | RLHF, fine-tuning, constitutional AI     |
| **Teacher: M** | Tutoring systems, Bloom's 2σ, MāyāLoom  | Distillation, self-play, multi-agent debate |

Each quadrant has different failure modes and trust dynamics. The existing literature addresses only H→H.

**H→M (training as impoverished pedagogy)**: The alignment community's quadrant. RLHF is behaviorist: reward signals and pattern matching. Nobody applies Pask's teachback. Constitutional AI moves toward principled self-critique but remains *unilateral*.

**M→H (the AI tutor and Freire's warning)**: Bloom's 2-sigma dream. But almost nobody applies Pask here either. Existing AI tutoring is behaviorist --- check answers, provide hints. They do not do teachback. Freire's warning is loudest in this quadrant: the M→H relationship is most vulnerable to the banking model.

**M→M (the unexplored quadrant)**: Distillation, self-play. Nobody asks whether Pask's conversation theory applies when both participants are computational. But in the Sūtra protocol, one agent writes a message another agent reads across sessions --- a rudimentary teaching relationship.

**The key observation**: the autonomy agreement --- epistemic commitments, graduated levels, bilateral negotiation, audit trail --- *does not require the human to be the teacher*. It works in all four quadrants because negotiated trust and epistemic commitments are more fundamental than the direction of instruction. Most existing frameworks are quadrant-specific. RLHF is H→M only. Tutoring systems are M→H only. This is the first protocol designed to operate across all four.


## Prior Art and Where We Depart {#prior-art}

| Aspect | Knight/Columbia (2025) | Bradshaw (2004) | CIRL | Constitutional AI | **This proposal** |
|--------|----------------------|-----------------|------|-------------------|-------------------|
| Direction | Unilateral | Either initiates | Cooperative game | Unilateral | **Bilateral, negotiated** |
| Granularity | Per-agent | Per-dimension | Global | Global | **Per-aspect-of-work** |
| Machine self-assessment | Not addressed | Not addressed | Implicit | Self-critique | **Self-de-escalation** |
| Epistemic commitments | Not addressed | Not addressed | Reward learning | Constitution | **Domain-specific, bilateral** |
| Audit trail | Recommended | Not addressed | Not addressed | Not addressed | **Structurally required** |
| Trust evolution | Static certificates | Adjustable | Fixed structure | Fixed principles | **Dynamic, logged transitions** |


## Beyond Propositions: The Creative and Embodied Case {#beyond-propositions}

Everything above operates within a propositional substrate. This captures at most the *focal surface* (Polanyi). It misses:

- **The tacit ground.** A physicist's sense that an approximation is trustworthy. A composer's feeling that a harmonic progression "needs something."
- **Embodied practice.** Indian classical music --- rāga, gamaka, meend --- resists symbolic capture. The guru-śiṣya paramparā transmits not notation but *a way of being with sound*.
- **Material resistance.** Pickering's "mangle of practice": knowledge emerges from the unpredictable interplay between human intention and material pushback.

For creative collaboration, epistemic commitments become *aesthetic commitments*: style vocabulary, when novelty is desired vs. consistency, how surprise is valued, when to defer to human taste vs. push against it.


## Experiment Design {#experiment-design}

A concrete experiment in the M→H quadrant: the machine teaching a human the Bloch equations (quantum magnetometry, MāyāPramāṇa lesson 00) with the full autonomy agreement protocol.

Three phases:

1. **Agreement negotiation** --- the learner declares background, the machine proposes a scaffolding plan, both negotiate.
2. **Guided traversal with checkpoints** --- at each cadenza point, teachback verifies understanding before advancing.
3. **Exercises with negotiated autonomy** --- the learner can propose level changes mid-exercise: "I'm stuck, pull back to colleague" or "this is straightforward, let me go to delegate."

The experiment tests three claims: that bilateral negotiation works for M→H, that Pask's teachback provides a reliable signal for when to advance, and that the same protocol designed for H→M scientific collaboration transfers to M→H teaching.


## What This Is Not {#what-this-is-not}

- Not a safety alignment proposal (though it operationalizes corrigibility through commitment rather than utility functions)
- Not a multi-agent orchestration framework
- Not a product or platform
- Not a general theory of human-AI interaction

It is a *working protocol* for a scientist or creative professional who works with AI as a thinking partner, needs graduated autonomy, and requires an auditable record of the collaboration.


## Open Questions {#open-questions}

1. **Teachback in practice** --- the prototype has no mechanism for it. A concrete proposal: the machine periodically reconstructs the human's reasoning in its own terms and asks "is this what you mean?"
2. **Deutero-learning** --- can the protocol itself learn? Can the agreement evolve its own structure based on accumulated experience?
3. **The socialization gap** --- Nonaka's SECI model. The machine handles Combination (explicit→explicit) but cannot do Socialization (tacit→tacit through co-presence).
4. **The ensemble case** --- the protocol is bilateral. Real collaboration often involves multiple parties.
5. **Material resistance** --- the machine doesn't interact with physical materials.
6. **Agreement portability** --- can an agreement transfer to a different model?
7. **The Feynman test** --- has the system genuinely contributed to scientific understanding, or merely accelerated the human's existing trajectory?


## Companion Documents {#companion-documents}

- [Literature Survey](/papers/autonomy-survey/) --- the evidentiary foundation across cybernetics, pedagogy, alignment, and anthropology
- [Agreement Template](/papers/autonomy-template/) --- a practical, instantiable template for an autonomy agreement


## References {#references}

- Ashby, W.R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Bateson, G. (1972). *Steps to an Ecology of Mind*. Ballantine.
- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Bradshaw, J.M. et al. (2004). "Dimensions of Adjustable Autonomy and Mixed-Initiative Interaction." Springer.
- Dreyfus, H.L. & Dreyfus, S.E. (1986). *Mind over Machine*. Free Press.
- Feng, M. & McDonald, C. (2025). "Levels of Autonomy for AI Agents." Knight First Amendment Institute, Columbia.
- Freire, P. (1970). *Pedagogy of the Oppressed*. Continuum.
- Hadfield-Menell, D. et al. (2016). "Cooperative Inverse Reinforcement Learning." NeurIPS.
- Lee, J.D. & See, K.A. (2004). "Trust in Automation." *Human Factors* 46(1).
- Licklider, J.C.R. (1960). "Man-Computer Symbiosis." *IRE Trans. HFE*.
- Maturana, H.R. & Varela, F.J. (1972/1980). *Autopoiesis and Cognition*. D. Reidel.
- Nonaka, I. & Takeuchi, H. (1995). *The Knowledge-Creating Company*. Oxford UP.
- Papert, S. (1980). *Mindstorms*. Basic Books.
- Parasuraman, R., Sheridan, T.B. & Wickens, C.D. (2000). "Types and Levels of Human Interaction with Automation." *IEEE Trans. SMC* 30(3).
- Pask, G. (1976). *Conversation, Cognition and Learning*. Elsevier.
- Pickering, A. (1995). *The Mangle of Practice*. U. Chicago Press.
- Polanyi, M. (1966). *The Tacit Dimension*. Doubleday.
- Ryle, G. (1949). *The Concept of Mind*. Hutchinson.
- Vygotsky, L.S. (1978). *Mind in Society*. Harvard UP.
