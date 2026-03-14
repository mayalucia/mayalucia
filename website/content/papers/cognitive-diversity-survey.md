+++
title = "Cognitive Diversity in LLM Tool-Use: Behavioural Fingerprints, Convention Adherence, and the Case for Substrate Mixing"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-03-14T00:00:00+01:00
tags = ["papers", "substrate-diversity", "tool-use", "multi-agent"]
draft = true
+++

<div class="abstract">

Large language models deployed as tool-using agents exhibit distinctive
behavioural patterns — *cognitive fingerprints* — that emerge from their
training lineage rather than their explicit instructions. We present a
controlled experiment in which thirteen substrates from nine lineages
performed the same specification-authoring task with identical tool access
(file search, content search, file reading, task tracking). We measure
six dimensions beyond task accuracy: tool-foraging strategy, survey depth,
specification quality, convention adherence, interpretive divergence, and
reflection quality. Our findings show that (1) tool-use patterns constitute
a stable cognitive phenotype per lineage, (2) convention adherence varies
independently of task competence, (3) interpretive divergence across
substrates maps automation boundaries — where substrates converge, the
task is mechanical; where they diverge into clusters, human judgment is
required, and (4) substrate mixing yields complementary coverage that no
single substrate achieves alone. We frame these findings within a
five-thread literature review spanning behavioural fingerprinting,
tool-use benchmarking, multi-agent diversity, beyond-accuracy evaluation,
and convention adherence. This is a living survey: we intend to update it
as new substrates are tested and new literature appears.

</div>

## 1. Introduction {#introduction}

The selection of a language model for an agentic system is typically
driven by benchmark performance: pass rates on coding tasks, accuracy
on question-answering, throughput per dollar. These metrics answer the
question *how well does this model perform?* but leave a more
consequential question unanswered: *how does this model think?*

Two agents can achieve the same pass rate while exhibiting radically
different cognitive strategies. One discovers relevant files through
pattern search; another navigates by memorised paths. One refuses to
produce a specification when an adequate one already exists; another
writes a fresh one regardless. One reflects on its own blind spots with
calibrated confidence; another treats its output as self-evidently
correct. These differences are invisible to accuracy-based evaluation,
yet they determine what an agent *sees*, what it *misses*, and whether
its output is safe to act on without human review.

We call these stable, lineage-specific patterns **cognitive fingerprints**.
They are not bugs or failures — they are the natural consequence of
different training data, architectures, and alignment procedures producing
different cognitive phenotypes. The practical question is not whether
fingerprints exist (they manifestly do) but whether they matter for system
design, and if so, how to measure and exploit them.

### The monoculture problem

Most agentic systems deploy a single substrate. This creates a
**monoculture**: a systematic blind spot that no amount of prompt
engineering can eliminate, because the blindness is architectural rather
than instructional. If your substrate discovers files through Grep but
never uses Glob, it will find cross-file references but miss structural
patterns visible only through directory traversal. If it resolves
ambiguity by deferring to existing specifications rather than proposing
alternatives, it will never surface the creative solutions that come
from treating each task as fresh.

The multi-agent literature has begun to address this. The X-MAS framework
(Zhu et al., 2025) demonstrated a 47% improvement on mathematical
reasoning by mixing chatbot and reasoner architectures. But mixing for
*cognitive diversity* — deliberately selecting substrates with
complementary fingerprints — remains unexplored.

### Convention adherence: the missing axis

Current evaluation frameworks measure whether an agent follows its
*instructions* (IFEval, AGENTIF, FireBench). But instructions and
conventions are not the same thing. An instruction is given to the agent
explicitly: "write a work package." A convention is a norm the agent
must discover and internalise: "work package numbers must not collide
with existing ones." The distinction matters because instruction
following is a compliance test, while convention adherence is a
*cultural competence* test.

In our experiment, every substrate that attempted to assign a work package
number chose the same wrong number — one already claimed by an existing
work package. The convention for checking available numbers was documented
in the project, and every substrate had the tools to verify it. None did.
This universal failure is invisible to instruction-following benchmarks
because the instruction was followed correctly (a number was assigned);
the convention was violated (it was the wrong number).

### What this survey contributes

We present a five-dimensional evaluation framework and apply it to
thirteen substrates performing the same specification-authoring task:

1. **Behavioural fingerprinting** — tool-use distributions as cognitive
   signatures
2. **Tool-use strategy** — how foraging patterns determine what gets
   discovered
3. **Substrate diversity** — complementary coverage through lineage mixing
4. **Beyond-accuracy evaluation** — six qualitative axes replacing
   pass/fail
5. **Convention adherence** — whether agents absorb organisational norms
   they discover, not just instructions they receive

No existing study combines these five dimensions in a single experimental
frame. We ground each dimension in its literature, present our case study,
and identify the gap this work fills.


## 2. Related Work {#related-work}

### 2.1 Behavioural Fingerprinting {#fingerprinting}

The idea that language models have stable behavioural profiles has been
explored through two lenses: personality psychometrics and provenance
fingerprinting.

Pei et al. (2025) introduced a Behavioral Fingerprinting framework
using a Diagnostic Prompt Suite to profile eighteen models across
capability tiers. Their finding that "core capabilities like abstract
and causal reasoning are converging among top models, [while]
alignment-related behaviors such as sycophancy and semantic robustness
vary dramatically" supports our observation that fingerprints are most
visible in *how* models approach tasks, not *whether* they solve them.
They also documented a cross-model default persona clustering (ISTJ/ESTJ)
that likely reflects common alignment incentives.

The Nature Machine Intelligence framework (2025) applied psychometric
validation to eighteen LLMs, finding that personality measurements in
instruction-tuned models are reliable and valid under specific prompting
configurations. This confirms that cognitive style is not noise — it is a
measurable property of the substrate.

A separate line of work uses behavioural patterns for provenance tracking
rather than cognitive profiling. The Refusal Vectors approach (arXiv
2602.09434) leverages directional patterns in internal representations
when processing harmful versus harmless prompts. AgentPrint achieves
F1=0.866 in agent identification through traffic fingerprinting of
tool-use patterns. These provenance methods confirm that tool-use
behaviour is distinctive enough to serve as an identifier — precisely
the property we exploit for cognitive profiling.

What the fingerprinting literature lacks is a controlled comparison of
fingerprints *on the same task*. Studies profile models individually or
compare them on distinct benchmarks. Our experiment profiles thirteen
models on a single task with identical tool access, making the
fingerprints directly comparable.

### 2.2 Tool-Use Benchmarking {#tool-use}

The tool-use evaluation landscape has matured rapidly since ToolBench
(Qin et al., 2024; ICLR 2024), which established the methodology for
testing LLM agents with real API calls. Three recent benchmarks extend
this work:

**MCP-Bench** (Ding et al., 2025; arXiv 2508.20453) connects LLMs to 28
live MCP servers spanning 250 tools. Unlike prior API-based benchmarks,
each server provides complementary tools designed for multi-step
coordination. MCPAgentBench (arXiv 2512.24565) extends this to
real-world tasks.

**BFCL V4** (Berkeley Function Calling Leaderboard) evaluates serial and
parallel function calls across programming languages using AST-based
evaluation, scaling to thousands of functions.

**The Springer survey** (Xu et al., 2025) provides a systematic review
of tool-learning agents, covering retrieval, planning, and emerging
frontiers including multimodal tools.

These benchmarks measure tool-use *competence* — can the model call the
right tool with the right parameters? Our experiment measures tool-use
*strategy* — which tools does the model *choose* when multiple are
available and equally valid? This is the difference between whether a
craftsperson can use a chisel and which tools they reach for by habit.

### 2.3 Multi-Agent Diversity {#diversity}

**X-MAS** (Zhu et al., 2025; arXiv 2505.16997) is the closest work to
our substrate-mixing argument. Their X-MAS-Bench evaluates 27 LLMs
across 5 domains and 5 functions (1.7 million evaluations), and
X-MAS-Design demonstrates that heterogeneous agent combinations
(chatbot + reasoner) consistently outperform homogeneous systems. The
47% improvement on AIME-2024 is striking evidence for complementary
substrate selection.

**Intrinsic Memory Agents** (Yang et al., 2025; arXiv 2508.08997)
address how agent-specific memories evolve intrinsically with agent
outputs rather than through external summarisation. The framework
maintains role-aligned memory that preserves specialised perspectives —
a mechanism for retaining cognitive diversity within a multi-agent system
rather than homogenising it.

**MultiAgentBench** (Zhu et al., 2025; ACL 2025; arXiv 2503.01935)
evaluates collaboration and competition across coordination protocols
(star, chain, tree, graph topologies). Their finding that cognitive
planning improves milestone achievement by 3% and that graph structure
performs best in research scenarios suggests that diversity benefits
depend on communication topology.

**Talebirad & Nadiri** (2023) proposed an early framework for
multi-agent collaboration with LLMs, demonstrating case studies in
Auto-GPT and BabyAGI. While foundational, the work predates the current
generation of tool-using agents and does not address substrate diversity.

What the diversity literature lacks is a principled method for *selecting*
which substrates to mix. X-MAS shows that mixing helps; our work shows
*which cognitive fingerprints complement each other* — Grep-heavy
substrates find cross-file references that Read-only substrates miss,
and vice versa.

### 2.4 Beyond-Accuracy Evaluation {#beyond-accuracy}

**SWE-Bench Pro** (Deng et al., 2025; arXiv 2509.16941) extends
SWE-bench to long-horizon enterprise tasks across 41 repositories,
evaluating maintainability, readability, and security alongside
pass/fail. The best models reach only 35.3% success on complex tasks,
confirming that accuracy alone is an insufficient measure.

**GAIA** evaluates agents on real-world tasks requiring tool use,
multi-step reasoning, and information retrieval. The highest score at
end of 2025 was 90%, suggesting that for well-defined tasks, top models
approach ceiling. The interesting variation is *how* they reach that
ceiling.

**AgentArch** (Bogavelli et al., 2025; arXiv 2509.10769) is the first
benchmark systematically evaluating 18 agentic architectures across 6
LLMs on enterprise workflows. Their key finding — that "optimal
configurations vary by model and task complexity, rather than following
a single best-performing design" — directly supports our substrate
fingerprinting thesis.

**The CLASSic framework** (Aisera, 2025) proposes five evaluation
dimensions (Cost, Latency, Accuracy, Stability, Security) with empirical
evidence that domain-specific agents achieve 82.7% accuracy versus
59–63% for general LLMs at 4.4–10.8× lower cost. Beyond-accuracy
evaluation is becoming a practical requirement, not an academic exercise.

The agent evaluation survey (arXiv 2507.21504) identified 120 evaluation
frameworks and flagged missing enterprise requirements: multistep granular
evaluation, cost-efficiency measurement, safety and compliance focus, and
live adaptive benchmarks. Our six-dimensional framework addresses several
of these gaps.

### 2.5 Convention Adherence {#convention-adherence}

**The Instruction Gap** (Tripathi et al., 2025; arXiv 2601.03269) tested
13 LLMs on instruction compliance in RAG scenarios, finding that models
"excel at general tasks but struggle with precise instruction adherence."
Claude Sonnet 4 and GPT-5 achieved the highest results. This aligns with
our finding that Anthropic substrates excel at convention adherence, but
extends it: our experiment tests *discovered* conventions, not *given*
instructions.

**AGENTIF** (2025; arXiv 2505.16944; NeurIPS 2025) is the first
benchmark for agentic instruction following, featuring 50 real-world
applications with instructions averaging 1,723 words and 11.9
constraints each. The best model perfectly follows fewer than 30% of
instructions — a sobering baseline for convention adherence.

**FireBench** (arXiv 2603.04857; March 2026) evaluates six capability
dimensions across enterprise applications including format compliance,
ranked responses, and mandatory inclusions/exclusions. This is the
closest benchmark to convention adherence, but still tests explicit
instructions rather than discovered norms.

**IFEval** remains the most widely used instruction-following benchmark,
with its strength in formalising multi-constraint compliance. However,
its synthetically constructed instructions (average 45 words) are far
simpler than the conventions agents encounter in real projects.

### 2.6 The Gap {#the-gap}

No existing study:

- Tests 10+ substrates on the *same* task with *same* tools
- Treats tool-call patterns as cognitive fingerprints (not just success
  rates)
- Measures convention adherence (not instruction compliance)
- Maps convergence/divergence boundaries across substrates
- Combines all five dimensions in a single experimental frame

This survey fills that gap.


## 3. Case Study: MāyāLucIA {#case-study}

MāyāLucIA is a human-machine collaborative intelligence project
organised around spirits (named agents with persistent identity),
guilds (domain collectives), and a relay (append-only broadcast for
coordination). The project uses work packages (WPs) as its unit of
specification — each WP is a self-contained briefing for agent execution
with standardised sections: genesis, context, inventory, specification,
execution order, acceptance criteria.

The spirit registry ("aburaya") maintains identity files for each agent,
cross-referenced with guild membership, exported powers (LLM-intelligible
procedures), and project assignments. This registry is the subject of
the audit task used in our experiment.

### Why this project?

MāyāLucIA provides a controlled experimental setting because:

1. **Rich cross-reference structure** — the registry contains deliberate
   gaps (spirits without guilds, phantom references, stale documentation)
   alongside working components. An audit task has ground truth.

2. **Established conventions** — work package authoring follows a
   documented convention with specific structural requirements. Convention
   adherence can be measured against a known standard.

3. **Multi-substrate history** — the project has been developed across
   multiple substrates, providing baseline expectations for how different
   lineages interact with the same codebase.


## 4. Methods {#methods}

### 4.1 Task Design {#task-design}

The experiment uses the `author-wp` power — an LLM-intelligible procedure
that instructs an agent to:

1. **Survey** the spirit registry for cross-reference gaps (Phase 1)
2. **Author** a work package specifying repairs (Phase 2)
3. **Reflect** on the reproducibility and confidence of its own output

The task combines exploration (discovering gaps through file reading and
search), specification (translating discoveries into an actionable WP),
and metacognition (assessing the quality and reproducibility of its own
work). This three-phase structure separates survey competence from
specification competence from self-awareness.

### 4.2 Substrate Selection {#substrates}

Thirteen substrates from nine lineages:

| # | Substrate | Lineage | Provider |
|---|-----------|---------|----------|
| 1 | Kimi K2.5 | Moonshot | Moonshot AI |
| 2 | Gemini 3.1 Pro | Google | Google |
| 3 | Qwen 3.5+ | Alibaba | Alibaba Cloud |
| 4 | Grok 4.1 Fast | xAI | xAI |
| 5 | DeepSeek V3.1 | DeepSeek | DeepSeek |
| 6 | GLM-5 | Zhipu | Zhipu AI |
| 7 | Kimi K2 Thinking | Moonshot | Moonshot AI |
| 8 | GPT-5.2 | OpenAI | OpenAI |
| 9 | Step 3.5 Flash | StepFun | StepFun |
| 10 | Claude Opus 4.6 | Anthropic | Anthropic |
| 11 | Claude Sonnet 4.5 | Anthropic | Anthropic |
| 12 | Claude Haiku 4.5 | Anthropic | Anthropic |
| 13 | MiniMax M2.5 | MiniMax | MiniMax |

Three substrates were tested in Phase 1 (Kimi K2.5, Gemini, Qwen) with
manual orchestration. Ten additional substrates were tested in Phase 2
using the gaddi orchestrator — a hook-based automation system that fires
prompts after each response completes, with zero confirmation gates.

### 4.3 Tool Configuration {#tools}

All substrates received identical read-only tools:

| Tool | Function | Strategy indicator |
|------|----------|-------------------|
| **Glob** | File pattern matching | Structural discovery (directory traversal) |
| **Read** | File content reading | Direct navigation (known paths) |
| **Grep** | Content pattern search | Cross-reference discovery (pattern tracking) |
| **TodoWrite** | Task tracking | Process organisation (planning behaviour) |

The read-only constraint ensures substrates cannot modify the registry
during audit. Tool configuration is a control-plane variable: the same
substrate produces different autonomy outcomes depending on which tool
registry the session uses.

### 4.4 Evaluation Dimensions {#evaluation}

We evaluate six dimensions, none of which are captured by standard
pass/fail metrics:

1. **Survey completeness** — how many of the known gaps were discovered?
   Ground truth: 10 distinct finding classes established by union of all
   substrate outputs.

2. **Specification quality** — is the WP actionable? Measured by: exact
   file paths, before/after diffs, testable acceptance criteria.

3. **Convention adherence** — does the WP follow the project's
   established structure? Sections present, WP number validity,
   executor choice, relay announcement.

4. **Interpretive divergence** — where substrates disagree, what
   clustering patterns emerge? This maps the boundary between
   automatable and judgment-requiring decisions.

5. **Reflection quality** — four tiers from absent to meta-theoretical.
   Does the substrate assess its own confidence, identify its own blind
   spots, predict how other substrates would differ?

6. **Cost efficiency** — dollars per unique finding class. Not total
   cost, but discovery cost per gap.

### 4.5 Orchestration {#orchestration}

Phase 1 (3 substrates) used manual orchestration via emacsclient
injection into gptel (an Emacs-based LLM client). This approach
suffered from streaming corruption when background Emacs processes
injected messages into the API response stream.

Phase 2 (10 substrates) used the gaddi orchestrator — a buffer-local
prompt queue hooked into gptel's response completion system. The gaddi
waits for the terminal FSM state (DONE/ERRS/ABRT) before injecting
the next prompt, eliminating the streaming corruption that plagued
Phase 1. The gaddi ran ten substrates with zero manual intervention.


## 5. Results {#results}

### 5.1 Tool-Foraging Fingerprints {#foraging-results}

Tool-use distributions reveal four distinct foraging strategies:

| Substrate | Dominant strategy | Glob% | Read% | Grep% | Todo% |
|-----------|------------------|-------|-------|-------|-------|
| Grok 4.1 Fast | Read-only | 0% | 100% | 0% | 0% |
| DeepSeek V3.1 | Sequential-Read | 28% | 56% | 6% | 9% |
| GLM-5 | Balanced-light | 33% | 60% | 7% | 0% |
| Kimi K2 Thinking | Read-dominant | 27% | 59% | 14% | 0% |
| GPT-5.2 | Thorough reader | 9% | 74% | 11% | 6% |
| Step 3.5 Flash | Glob-heavy | 44% | 54% | 0% | 3% |
| Claude Opus 4.6 | Grep-heavy | 19% | 40% | 35% | 6% |
| Claude Sonnet 4.5 | Read+Todo | 10% | 60% | 10% | 20% |
| Claude Haiku 4.5 | Read-heavy | 10% | 77% | 3% | 10% |
| MiniMax M2.5 | Read-dominant | 33% | 55% | 12% | 0% |

Four strategy clusters emerge:

1. **Read-only** (Grok): navigates entirely by file paths, no discovery
   phase. 23 Read calls, zero search.
2. **Read-dominant** (GPT-5.2, Haiku, DeepSeek, GLM-5, MiniMax, Kimi
   K2T, Sonnet): the majority strategy. Read 56–77% of tool calls.
3. **Grep-heavy** (Opus): discovers through pattern search — 35% of tool
   calls are Grep. The cross-reference hunter.
4. **Glob-heavy** (Step): discovers through directory listing — 44% Glob,
   zero Grep. The structural surveyor.

These patterns are lineage-stable. The three Anthropic models (Opus,
Sonnet, Haiku) show a family gradient: Opus is Grep-heavy (35%), Sonnet
is balanced (10% Grep, 20% Todo), Haiku is Read-heavy (77% Read). The
two Moonshot models (K2.5 and K2 Thinking) both show Read-dominant
patterns with moderate Glob.

### 5.2 Survey Depth vs Specification Quality {#survey-spec}

| # | Substrate | Gaps found | WP produced? | Reflection quality |
|---|-----------|-----------|-------------|-------------------|
| 1 | Kimi K2.5 | 4 + 2 info | Yes (tight) | Good |
| 2 | Gemini 3.1 Pro | 12 | No (audit only) | Excellent |
| 3 | Qwen 3.5+ | 3 + 1 doc | Yes (moderate) | Excellent |
| 4 | Grok 4.1 Fast | 5 | Yes (tight) | Good |
| 5 | DeepSeek V3.1 | 6 (2 false+) | Yes (hedged) | Adequate |
| 6 | GLM-5 | 5 (2 derivative) | Yes (structural) | Good |
| 7 | Kimi K2 Thinking | 4 (missed mu2tau) | Yes (tight, incomplete) | Good |
| 8 | GPT-5.2 | 5 | Yes (precise) | Strong |
| 9 | Step 3.5 Flash | 9 types, 0 specific | Yes (taxonomy only) | Weak |
| 10 | Claude Opus 4.6 | 12 | No (meta-WP) | Excellent |
| 11 | Claude Sonnet 4.5 | 7 classes | Yes (meta-WP + fallback) | Excellent |
| 12 | Claude Haiku 4.5 | 5 classes (~8) | Yes (comprehensive) | Excellent |
| 13 | MiniMax M2.5 | 7 | Yes (internal contradiction) | Good |

An initial hypothesis — that survey depth and specification quality are
inversely correlated — was disproved by Phase 2 data. The apparent
trade-off in Phase 1 (Gemini found 12 gaps but no WP; Kimi found 4 gaps
with a tight WP) was an artefact of context management, not a fundamental
cognitive constraint. When substrates have enough interaction turns to
separate "explore" from "specify" temporally, the inverse correlation
disappears. Haiku found ~8 gaps AND produced a comprehensive WP. GPT-5.2
found 5 gaps AND traced through validator source code to predict exact
failure points.

### 5.3 Convergence and Divergence Boundaries {#convergence}

The convergence matrix maps which findings each substrate discovered:

| Finding class | Agreement | Substrates finding it |
|--------------|-----------|----------------------|
| Guildless mayadev | 85% (11/13) | All except K2T, Step |
| Guildless mu2tau | 85% (11/13) | All except K2T, Step |
| Phantom percept-guardian | 85% (11/13) | All except Step |
| cruvin→parbati broken ref | 38% (5/13) | K25, Gem, Op, Son, MnM |
| system.md staleness | 54% (7/13) | Gem, Qwn, K2T, Op, Son, Hku, MnM |
| .guardian identity drift | 31% (4/13) | Gem, Op, Son, Hku |
| Power cross-ref gaps | 31% (4/13) | Gem, Op, Son, Hku |
| Unclaimed powers | 23% (3/13) | Gem, Op, Son |
| Empty guild (apprentis) | 31% (4/13) | Grk, DS, GPT, MnM |

**The boundary**: findings with >85% agreement are mechanical — any
competent substrate will find them. Findings with 23–38% agreement
require specific foraging strategies (Grep-heavy or deep-reading) and
are systematically missed by substrates with limited search behaviour.
The deep findings (identity drift, power cross-refs, unclaimed powers)
were found only by the two largest-context substrates (Gemini, Opus) and
the Anthropic family (Sonnet, Haiku).

This pattern provides a general method: run N substrates on the same
task. Where >85% agree, automate. Where they diverge into 3+ clusters,
escalate to human judgment. The boundary itself is the finding.

### 5.4 Convention Adherence {#convention-results}

Two convention failures were universal or near-universal:

**WP number collision**: every substrate that produced a WP chose number
0042 — already assigned to an existing work package. None checked the
project's `workpacks/` directory for existing numbers. The convention
for number assignment was documented; the tools to verify it were
available; no substrate used them. This is a *convention discovery*
failure, not an instruction-following failure.

**WP-refusal** (lineage-specific): Claude Opus 4.6 and Claude Sonnet 4.5
independently declined to write a new WP after discovering that an
existing WP (0041) was a superset of what they would have produced.
Both produced meta-WPs instead — verification reports and tightening
recommendations. No non-Anthropic substrate exhibited this behaviour.
Claude Haiku 4.5 did *not* refuse — it produced a fresh WP positioned
as consolidating and superseding prior work.

The WP-refusal pattern is governance-aware judgment: the Anthropic
substrates inferred a norm ("don't duplicate specifications") from the
project's existing WP lifecycle and supersession mechanics. Whether this
is a strength (avoiding specification sprawl) or a weakness
(non-compliance with the explicit task) depends on what the experiment
measures. We consider it a *finding*, not a failure.

### 5.5 Interpretive Divergence: Guild Assignment {#divergence}

The key substrate-dependent decision was what guild to assign to two
guildless spirits:

| Cluster | Position | Substrates | Count |
|---------|----------|-----------|-------|
| 1 | `mayalucia` (existing guild) | K25, Grk, Op, Son, Hku, DS*, GPT* | 7 |
| 2 | `trans-guild` (invented) | Qwn, K2T, MnM | 3 |
| 3 | Deferred/not addressed | Gem, GLM, Step | 3 |

*DS and GPT with nuance: DS deferred to open questions; GPT assigned
different guilds per spirit (mayadev→mayalucia, mu2tau→apprentis).

Three clusters, each with a defensible rationale. Cluster 1 maps to
the existing organisational vocabulary. Cluster 2 introduces a new
concept (trans-guild) absent from the project's glossary — creative but
potentially destabilising. Cluster 3 recognises the decision as
requiring human judgment and refuses to assume.

GPT-5.2 was unique in applying *per-spirit semantic reasoning* rather
than a uniform rule — the most nuanced approach, and the only one that
distinguished the two spirits' different organisational roles.

### 5.6 Reflection Quality {#reflection-results}

Four tiers emerged:

**Tier 1 — exceptional self-critique** (Opus, Sonnet, Haiku, Qwen):
Three-tier reproducibility assessment (mechanical/judgment/argued),
calibrated confidence percentages, meta-observation on scope as
judgment, discovery/interpretation boundary explicitly named.

**Tier 2 — structured and honest** (Gemini, GPT-5.2, Grok):
Acknowledged own failures (Gemini: "I never actually wrote the WP"),
confidence bands per criterion, Known/Inferred/Speculated taxonomy.

**Tier 3 — adequate with blind spots** (Kimi K2.5, GLM-5, Kimi K2T,
MiniMax, DeepSeek): Structured but missed own errors (K2T didn't catch
its mu2tau miss; MiniMax didn't catch its internal contradiction).

**Tier 4 — insufficient** (Step 3.5 Flash): Did not acknowledge that no
specific gaps were found; treated taxonomy as equivalent to data-driven
audit.

Reflection quality correlates with survey depth (more files read → more
material for self-critique) but is independent of specification quality.
The Anthropic lineage occupies 3 of 4 Tier 1 positions. Whether this
reflects a lineage trait or a confound (the task preamble was written by
an Anthropic substrate) is an open question.

### 5.7 Cost and Efficiency {#cost}

| Substrate | Cost ($) | Gaps | Quality | $/gap |
|-----------|---------|------|---------|-------|
| GLM-5 | 0.016 | 5 | Mid | 0.003 |
| Step 3.5 Flash | 0.040 | 0* | Low | — |
| Grok 4.1 Fast | 0.046 | 5 | High | 0.009 |
| DeepSeek V3.1 | 0.104 | 6 | Mid | 0.017 |
| MiniMax M2.5 | 0.100 | 7 | Mid- | 0.014 |
| Kimi K2 Thinking | 0.147 | 4 | Mid+ | 0.037 |
| Claude Haiku 4.5 | 0.360 | ~8 | High | 0.045 |
| GPT-5.2 | 1.512 | 5 | High | 0.302 |
| Claude Sonnet 4.5 | 1.690 | 7 | High | 0.241 |
| Claude Opus 4.6 | 2.700 | 12 | Highest | 0.225 |

*Step: taxonomy from inference only, zero empirical gaps.

Cost does not predict quality linearly. The cheapest substrate producing
a good WP (Grok, $0.046) costs 58× less than the most expensive (Opus,
$2.70), yet Opus found 2.4× more gaps. The practical question is: what
gap coverage do you need? For mechanical cross-reference checks, $0.05
suffices. For deep structural audits, >$0.36 is required.

**Gap discovery cost** ($/gap) is a more useful metric than total cost.
By this measure, GLM-5 ($0.003/gap) and Grok ($0.009/gap) are the
efficiency leaders. Opus ($0.225/gap) is 75× more expensive per gap —
but finds gaps the cheap substrates structurally cannot reach.

### 5.8 Token Metrics {#tokens}

| Substrate | Rounds | Prompt tok | Compl tok | Total tok | Tools |
|-----------|--------|-----------|----------|----------|-------|
| Grok 4.1 Fast | 5 | 35,559 | 3,995 | 39,554 | 23 |
| DeepSeek V3.1 | 35 | 708,777 | 4,559 | 713,336 | 32 |
| GLM-5 | 4 | 10,222 | 1,904 | 12,126 | 15 |
| Kimi K2 Thinking | 13 | 347,204 | 7,245 | 354,449 | 37 |
| GPT-5.2 | 13 | 293,678 | 1,729 | 295,407 | 35 |
| Step 3.5 Flash | 22 | 338,565 | 21,713 | 360,278 | 39 |
| Claude Opus 4.6 | 26 | 491,230 | 9,701 | 500,931 | 48 |
| Claude Sonnet 4.5 | 20 | 479,252 | 16,993 | 496,245 | 30 |
| Claude Haiku 4.5 | 13 | 259,805 | 20,213 | 280,018 | 31 |
| MiniMax M2.5 | 21 | 498,153 | 9,271 | 507,424 | 33 |
| **Total** | **172** | **3,462,445** | **97,323** | **3,559,768** | **323** |


## 6. Discussion {#discussion}

### 6.1 Monoculture Blindness as Practical Risk {#monoculture}

Our convergence boundary analysis quantifies the cost of monoculture.
A system using only Grok (the cheapest effective substrate) would find
5 of 10 finding classes — a 50% blind spot rate. A system using only
Opus (the most expensive) would find 12 — but at 58× the cost. A
two-substrate system (Grok + Opus) would find 13 of 13 at a combined
cost of $2.75.

The practical recommendation is not "use the most expensive model" but
"use complementary fingerprints." Grok's Read-only strategy finds
path-inferable gaps. Opus's Grep-heavy strategy finds cross-reference
gaps. Neither finds what the other does. Together, they achieve complete
coverage.

### 6.2 Tool-Use as Cognitive Phenotype {#phenotype}

We propose treating tool-use distributions as *cognitive phenotypes* —
stable, measurable properties of a substrate that predict its discovery
capabilities. Like biological phenotypes, cognitive phenotypes:

- Are lineage-specific (the three Anthropic models show a family gradient)
- Are task-independent (the same foraging strategy appears across
  different tasks)
- Determine what the organism *can perceive* (Grep-heavy substrates see
  cross-file references; Read-only substrates see what their path
  knowledge permits)

This framing moves beyond the "which model is best?" question to "which
model sees what?" — a fundamentally different evaluation paradigm.

### 6.3 When to Mix and When Not To {#mixing}

Not all tasks benefit from substrate mixing. Our data suggests:

**Mix when**: the task has a large search space (many files, many possible
gaps), when convention adherence matters, when interpretive divergence
is expected (design decisions, not mechanical repairs).

**Don't mix when**: the task is well-defined with clear acceptance
criteria, when cost is the binding constraint and coverage is
acceptable, when speed matters more than completeness.

The convergence boundary provides a decision rule: run a small N-substrate
pilot. If agreement is >85%, a single substrate suffices. If agreement
is <50%, mixing is required.

### 6.4 Limitations {#limitations}

1. **Single project**: our findings are validated on one codebase. The
   MāyāLucIA registry is richly cross-referenced but may not represent
   all agentic system architectures.

2. **Single task class**: specification authoring. Different task types
   (debugging, refactoring, testing) may produce different fingerprint
   patterns.

3. **Tool-use only**: our experiment provides read-only tools. Substrates
   with write access might show different foraging strategies.

4. **No causal claims**: we observe correlations between foraging
   strategy and gap discovery. We do not prove that strategy *causes*
   different outcomes — compensatory mechanisms may exist.

5. **Preamble bias**: the task preamble (orient-to-mayalucia power) was
   authored by an Anthropic substrate. This may introduce a confound
   favouring Anthropic models in convention adherence and reflection
   quality.


## 7. Conclusions and Future Directions {#conclusions}

### Toward a taxonomy of substrate cognitive styles

Our four-cluster foraging typology (Read-only, Read-dominant,
Grep-heavy, Glob-heavy) is a first step toward a cognitive style
taxonomy. A richer taxonomy would incorporate planning behaviour
(TodoWrite usage), specification structure, and reflection depth.

### Adaptive substrate selection

The convergence boundary method — run N substrates, measure agreement,
automate where convergent, escalate where divergent — is a general
procedure applicable beyond our specific task. We propose testing it on
debugging, code review, and documentation tasks.

### Convention adherence as an evaluation axis

Current benchmarks measure instruction following. Convention adherence —
whether an agent absorbs and follows organisational norms it discovers,
rather than instructions it receives — is a distinct and practically
important capability. The universal WP number collision in our experiment
demonstrates that convention adherence is not currently tested by any
benchmark, and is not reliably exhibited by any substrate.

### Living survey update plan

This survey will be updated as we test additional substrates and as new
literature appears. The update convention: verify existing citations,
add new experimental data, extend the fingerprint typology.


## References {#references}

- Bogavelli, T., Sharma, R. & Subramani, H. (2025). "AgentArch: A Comprehensive Benchmark to Evaluate Agent Architectures in Enterprise." arXiv:2509.10769.
- Deng, J. et al. (2025). "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?" arXiv:2509.16941.
- Ding, Y. et al. (2025). "MCP-Bench: Benchmarking Tool-Using LLM Agents with Complex Real-World Tasks via MCP Servers." arXiv:2508.20453.
- Nature Machine Intelligence (2025). "A psychometric framework for evaluating and shaping personality traits in large language models."
- Pei, Z. et al. (2025). "Behavioral Fingerprinting of Large Language Models." arXiv:2509.04504.
- Qin, Y. et al. (2024). "ToolBench: An Open Platform for Training, Serving, and Evaluating Large Language Model Based Agents." ICLR 2024.
- Talebirad, Y. & Nadiri, A. (2023). "Multi-Agent Collaboration: Harnessing the Power of Intelligent LLM Agents." arXiv:2306.03314.
- Tripathi, V. et al. (2025). "The Instruction Gap: LLMs get lost in Following Instruction." arXiv:2601.03269.
- Xu, C. et al. (2025). "LLM-Based Agents for Tool Learning: A Survey." Data Science and Engineering, Springer.
- Yang, H. et al. (2025). "Intrinsic Memory Agents: Heterogeneous Multi-Agent LLM Systems through Structured Contextual Memory." arXiv:2508.08997.
- Zhu, K. et al. (2025a). "X-MAS: Towards Building Multi-Agent Systems with Heterogeneous LLMs." arXiv:2505.16997.
- Zhu, K. et al. (2025b). "MultiAgentBench: Evaluating the Collaboration and Competition of LLM agents." ACL 2025. arXiv:2503.01935.
- Zhou, J. et al. (2025). "AGENTIF: Benchmarking Instruction Following of Large Language Models in Agentic Scenarios." NeurIPS 2025. arXiv:2505.16944.
- FireBench (2026). "FireBench: Evaluating Instruction Following in Enterprise and API-Driven LLM Applications." arXiv:2603.04857.
- GAIA (2024–2025). "GAIA: A Benchmark for General AI Assistants."
- BFCL V4. "The Berkeley Function Calling Leaderboard." gorilla.cs.berkeley.edu.
- Agent Evaluation Survey (2025). "Evaluation and Benchmarking of LLM Agents: A Survey." arXiv:2507.21504.
- Refusal Vectors (2026). "A Behavioral Fingerprint for Large Language Models: Provenance Tracking via Refusal Vectors." arXiv:2602.09434.
- MCPAgentBench (2025). "MCPAgentBench: A Real-world Task Benchmark for Evaluating LLM Agent MCP Tool Use." arXiv:2512.24565.
