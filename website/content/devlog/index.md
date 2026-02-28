+++
title = "Development Log"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-28T01:34:57+01:00
tags = ["devlog"]
draft = false
+++

## Open Threads {#open-threads}


### <span class="org-todo todo TODO">TODO</span> [MayaLucIA] Convention for preserving `collab/` artifacts {#mayalucia-convention-for-preserving-collab-artifacts}

How do we selectively preserve valuable outputs from ephemeral collaboration
sessions? Discussion document: [preserving-collab-artifacts.org]({{< relref "preserving-collab-artifacts" >}}).
Current recommendation: promote to project tree + devlog reference (Option C).


## Decision Log {#decision-log}


### <span class="timestamp-wrapper"><span class="timestamp">&lt;2026-02-08 Sun&gt; </span></span> Devlog structure adopted {#devlog-structure-adopted}

-   Context: Need to track development decisions and progress across sessions with AI collaborators.
-   Decision: Adopted structured devlog format with three sections — open threads, decision log, work log.
-   Alternatives considered: Formal project management tools (too heavy), pure git log (loses narrative/intent).
-   Consequences: Each project maintains its own devlog. A top-level index links them.


## Work Log {#work-log}


### <span class="timestamp-wrapper"><span class="timestamp">&lt;2025-07-27 Sun&gt; </span></span> Session: OBI GitHub survey {#session-obi-github-survey}

-   Surveyed the [Open Brain Institute](https://github.com/openbraininstitute) GitHub organization.
-   114 repos, 55 active (pushed in last 6 months), 305 open issues across 41 repos.
-   Domains identified: Simulation, Morphology/Synthesis, Atlas/Spatial, Knowledge/Data,
    Platform/Infrastructure, Visualization, Workflows.
-   Created Org-as-instruction-file pattern: task spec + execution log + report in one file.
-   Created project-level `CLAUDE.md` for Claude Code sessions.
-   Session artifacts (in `bravli/collab/sessions/obi-projects/`, ephemeral):
    -   `obi-github-survey.org` — instruction file with embedded report
    -   `scripts/obi_survey.py` — reusable stdlib-only survey script
    -   `data/*.json` — raw API data (repos, issues, manifest)
-   Discussion: [Preserving Collaboration Artifacts]({{< relref "preserving-collab-artifacts" >}})
    on how to promote `collab/` artifacts when worth keeping.
-   Next: decide on artifact preservation convention (Option C recommended).
    Consider promoting the OBI survey report to `bravli/surveys/`.


### <span class="timestamp-wrapper"><span class="timestamp">&lt;2026-02-08 Sun&gt; </span></span> Session: Devlog scaffolding {#session-devlog-scaffolding}

-   Created devlog structure for MayaLucIA.
-   Next: Populate open threads from existing project documents.
