+++
title = "Literature Survey — Autonomy, Collaboration, and Knowledge Across Traditions"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-28T19:00:00+01:00
tags = ["papers", "autonomy", "survey"]
draft = false
+++

<div class="abstract">

This survey grounds the [autonomy agreement proposal](/papers/autonomy-agreement/)
in prior work across five domains: cybernetics, pedagogy, AI alignment,
anthropology of knowledge, and existing ML tools. The goal is not comprehensiveness
but to identify the intellectual ancestors, locate the genuine novelty, and find
the blind spots.

</div>


## 1. Cybernetics (1940s--present) {#cybernetics}

### Ashby: Requisite Variety {#ashby}

The Law of Requisite Variety (1956): a controller must have at least as much variety as the system it controls. The Good Regulator Theorem (Conant & Ashby, 1970): every good regulator of a system must be a model of that system.

*Implication*: autonomy delegation is variety delegation. You delegate exactly as much as the machine can absorb without exceeding the partnership's viability bounds. Trust is calibrated variety.


### Licklider: Man-Computer Symbiosis (1960) {#licklider}

The original vision: not master-servant, but mutualism. Division of labor by cognitive type, not hierarchy. The key frontier: *formulative thinking* --- problems that cannot be formulated without machine aid.

*Implication*: symbiosis requires ongoing negotiation of the cognitive boundary.


### Pask: Conversation Theory (1975--76) {#pask}

The most formally developed cybernetic model of learning through dialogue. Knowledge as *entailment meshes* (relational, not propositional). *Teachback* as the criterion of understanding: B teaches the concept back to A in a different way. P-individuals (conceptual entities) emerge from M-individuals (physical substrates) through conversation.

*Implication*: autonomy emerges from conversational success. The machine earns autonomy through successful teachback. This is the formal ancestor of our protocol.


### Maturana & Varela: Autopoiesis {#autopoiesis}

Cognition is effective action, not representation. Structural coupling: organism and environment co-evolve through mutual perturbation. Neither controls the other.

*Implication*: autonomy in a partnership is co-constituted through coupling history, not toggled by permission.


### Beer: Viable System Model {#vsm}

Five recursive subsystems for any autonomous system. S1 (operations) has *maximum autonomy consistent with cohesion*. S3 (optimization) ensures coherence without commanding. Direct architectural template for human-machine autonomy.


### Bateson: Levels of Learning {#bateson}

Learning 0 (fixed response), I (trial-and-error), II (deutero-learning --- learning *to learn*), III (revision of the framework itself). The autonomy negotiation requires asking *which level of learning* to grant.


### Von Foerster: Second-Order Cybernetics {#second-order}

The observer is part of the system. Both parties model each other, and those models are co-constitutive. Design is an ethical act.


## 2. Pedagogy and Learning Theory {#pedagogy}

### Vygotsky: Zone of Proximal Development {#vygotsky}

The space between what a learner can do alone and with guidance. The "Zone of No Development" warning: when AI continuously mediates learning, cognitive struggle diminishes and autonomous reasoning atrophies.


### Scaffolding and Fading (Bruner, Wood) {#scaffolding}

Progressive withdrawal of support as competence grows. *Direct analog*: our autonomy levels (apprentice → delegate) are a scaffolding model with explicit fading protocol.


### Lave & Wenger: Legitimate Peripheral Participation {#situated-learning}

Knowledge as participation in a community of practice. A machine collaborator enters as a peripheral participant and becomes central through demonstrated contribution.


### Freire: Critical Pedagogy {#freire}

The "banking model" (teacher deposits knowledge into passive student) vs. dialogical education (both parties are subjects, both are changed). The autonomy agreement aims for the dialogical model.


### Bloom: Two Sigma Problem (1984) {#bloom}

One-to-one tutoring produces a two standard deviation improvement. AI could be the scalable tutor Bloom envisioned --- but only with genuine formative feedback and mastery checks, not just answers.


### Papert: Constructionism {#papert}

Learning by making. Understanding emerges through the act of construction. *Direct ancestor* of MāyāLucIA's core cycle: Measure → Model → Manifest → Evaluate → Refine.


## 3. AI Alignment and Human-AI Teaming {#alignment}

### CIRL: Cooperative Inverse Reinforcement Learning {#cirl}

Hadfield-Menell, Russell et al. (2016). Human-robot alignment as a cooperative game. *Gap*: assumes fixed cooperative structure with no mechanism for graduating trust.


### Constitutional AI (Anthropic, 2022) {#constitutional-ai}

Principles replace per-instance labels. Unilateral --- Anthropic writes the constitution. The autonomy agreement is the *bilateral analog*.


### Calibrated Trust in Automation (Lee & See, 2004) {#calibrated-trust}

Trust as a dynamic assessment based on performance, process, and purpose. Overtrust → misuse; undertrust → disuse. *Directly operationalized* by per-aspect autonomy levels and transition protocol.


### Knight/Columbia: Levels of Autonomy (2025) {#knight-columbia}

Five levels by user's role. Closest existing work. Key differences: unilateral (vs. our bilateral), per-agent (vs. our per-aspect), no machine self-assessment, no epistemic commitments, static certificates (vs. our dynamic logged transitions).


### Bradshaw: Adjustable Autonomy (2003--2012) {#bradshaw}

Four dimensions of variable autonomy. We adopt these and add a fifth: the *logged rationale*.


### SciSciGPT and Google Co-Scientist {#automated-science}

Multi-agent systems for automated scientific workflows. *Limitation*: workflow automation, not structured dialogue. No autonomy negotiation, no epistemic commitments. Our proposal addresses *when* autonomous generation is appropriate and *how* to audit it.


## 4. Anthropology and Philosophy of Knowledge {#anthropology}

### Polanyi: Tacit Knowledge {#polanyi}

"We know more than we can tell." Proximal-distal structure: we attend *from* subsidiary clues *to* focal meaning. The collaboration captures at most the focal surface; the tacit substrate is where AI collaboration is hardest.


### Ryle: Knowing-How vs. Knowing-That {#ryle}

An agent's competence is demonstrated through performance, not propositional description. The agreement's emphasis on *demonstrated* competence follows Ryle.


### Dreyfus: Skill Acquisition {#dreyfus}

Five stages: novice → expert. At higher levels, rules are replaced by intuition. The four autonomy levels (apprentice → collaborator) loosely correspond.


### Indian Pramāṇa Theory {#pramana}

Valid means of knowledge: pratyakṣa (perception), anumāna (inference), śabda (testimony), upamāna (analogy). The agreement's "evidence hierarchy" is a version of pramāṇa theory.


### Nonaka: SECI Model {#seci}

Knowledge creation cycle: Socialization (tacit→tacit), Externalization (tacit→explicit), Combination (explicit→explicit), Internalization (explicit→tacit). The machine handles Combination well; Socialization --- tacit-to-tacit through co-presence --- is precisely what the machine cannot do.


### STS: Latour, Pickering, Haraway {#sts}

Latour: knowledge through networks of human and non-human actors. Pickering: the "mangle of practice" --- knowledge from resistance. Haraway: situated knowledges. The human-AI dialogue is itself a site of knowledge production.


## 5. Gap Analysis: Where We Stand {#gap-analysis}

### What has deep prior art {#prior-art}

| Our concept | Ancestor |
|-------------|----------|
| Autonomy levels | Parasuraman (2000), Knight/Columbia (2025) |
| Trust calibration | Lee & See (2004) |
| Conversation as knowledge | Pask (1976) |
| Progressive disclosure | Scaffolding (Bruner), Dreyfus stages |
| Append-only audit | Lab notebook tradition, event sourcing |
| Epistemic commitments | Pramāṇa theory, scientific method |
| Structural coupling | Maturana & Varela (1972) |

### What is genuinely new {#genuinely-new}

1. **Bilateral negotiation** --- every existing framework treats autonomy as granted by the human or inherent in the system. None treat it as negotiated between parties with logged consent from both sides.

2. **Per-aspect granularity with epistemic commitments** --- autonomy varies by *aspect of the work*, grounded in domain-specific standards of evidence.

3. **Machine-initiated de-escalation** --- the machine recognizing and declaring its own limits. Existing corrigibility research focuses on human correction; our protocol makes self-assessment a first-class feature.

4. **The audit trail as scientific record** --- not compliance, but the collaboration's lab notebook.

5. **Non-propositional extension** --- acknowledging that embodied, aesthetic, and oral traditions require fundamentally different moves (demonstrate, invoke, correct, absorb).


### What we're still missing {#still-missing}

1. **Pask's teachback in practice** --- no mechanism for the machine to demonstrate understanding by reconstructing the human's reasoning.

2. **Bateson's Learning II** --- the protocol handles Learning I but doesn't yet support deutero-learning.

3. **Nonaka's Socialization quadrant** --- tacit-to-tacit transfer between human and machine.

4. **The ensemble case** --- our protocol is bilateral; real collaboration often involves multiple parties.

5. **Material resistance** --- the machine doesn't interact with physical materials; the collaboration misses Pickering's "mangle."


## References {#references}

- Ashby, W.R. (1956). *An Introduction to Cybernetics*.
- Bateson, G. (1972). *Steps to an Ecology of Mind*.
- Beer, S. (1972). *Brain of the Firm*.
- Bloom, B.S. (1984). "The 2 sigma problem." *Ed. Researcher* 13(6).
- Bradshaw et al. (2004). "Dimensions of Adjustable Autonomy." Springer.
- Dreyfus, H.L. & Dreyfus, S.E. (1986). *Mind over Machine*.
- Feng & McDonald (2025). "Levels of Autonomy for AI Agents." Columbia.
- Freire, P. (1970). *Pedagogy of the Oppressed*.
- Hadfield-Menell et al. (2016). "Cooperative IRL." NeurIPS.
- Ingold, T. (2000). *The Perception of the Environment*.
- Lave & Wenger (1991). *Situated Learning*.
- Lee & See (2004). "Trust in Automation." *Human Factors* 46(1).
- Licklider, J.C.R. (1960). "Man-Computer Symbiosis." *IRE Trans. HFE*.
- Maturana & Varela (1972/1980). *Autopoiesis and Cognition*.
- Nonaka & Takeuchi (1995). *The Knowledge-Creating Company*.
- Papert, S. (1980). *Mindstorms*.
- Parasuraman, Sheridan & Wickens (2000). *IEEE Trans. SMC* 30(3).
- Pask, G. (1976). *Conversation, Cognition and Learning*.
- Polanyi, M. (1966). *The Tacit Dimension*.
- Ryle, G. (1949). *The Concept of Mind*.
- Vygotsky, L.S. (1978). *Mind in Society*.
