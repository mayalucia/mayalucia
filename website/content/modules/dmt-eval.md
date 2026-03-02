+++
title = "DMT-Eval: Universal Validation Framework"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-03-02T22:00:00+01:00
tags = ["modules", "dmt-eval", "validation", "neuroscience", "brain-score"]
draft = false
+++

**Data, Models, Tests** --- validation as structured scientific argumentation.

DMT-Eval decouples analyses from models through formal adapter interfaces,
producing structured scientific reports (LabReports) from any (model, data)
pair. The architectural insight was proven over seven years at the Blue Brain
Project (EPFL, 2017--2024) and is now rebuilt for any domain where
computational models need systematic evaluation.

## Live Demo

**[bench.mayalucia.dev](https://bench.mayalucia.dev)** --- run evaluations
in real time. Weather prediction, drug efficacy, and Brain-Score NeuroAI
benchmarks, all producing structured LabReports through the same pipeline.

## Architecture

The core cycle: **Scenario + Models + Data -> LabReport**.

A *Scenario* descriptor tells the evaluator which columns are observed, which
are predicted, and how to stratify. Models implement a minimal protocol
(`.name`, `.predict(observations)`). The evaluator computes metrics (RMSE,
bias, skill score), stratifies by group, and renders a Markdown report with
abstract, methods, results tables, and discussion.

### Three-Party Design

| Role | Responsibility |
|------|---------------|
| **Data Interface Authors** | Define what a valid model looks like for a domain |
| **Model Adapters** | Make existing models conform to the interface |
| **Validation Writers** | Compose evaluations from (adapter, interface) pairs |

### Seven-Level Interface Gradient

From `dmt.evaluate()` (zero concepts --- pass models and data, get a report)
to `typing.Protocol`-based interfaces with `@dmt.adapter` decorators and
parameterized measurements.

## Brain-Score Domain Adapter

The first domain adapter targets [Brain-Score](https://www.brain-score.org/)
--- the NeuroAI platform for comparing neural network representations to
primate visual cortex recordings.

**747 lines. 7 modules. Three architectural fixes over the original:**

| BBP Era (2017--2024) | DMT-Eval (2026) |
|----------------------|-----------------|
| `InterfaceMeta` metaclass (MRO conflicts) | `__init_subclass__` hooks |
| No enforcement until runtime | `@implements` validates at registration time |
| Shared mutable registry across all interfaces | Per-interface `PluginRegistry` |

**Results** (AlexNet on MajajHong2015 public subset):

| Benchmark | Raw Score | Ceiling | Normalized |
|-----------|-----------|---------|------------|
| IT-pls | 0.48 | 0.817 | 0.588 |
| V4-pls | 0.55 | 0.892 | 0.616 |

## Provenance

Co-author of the Blue Brain Project's validation methodology, published in
eLife (2024). The original framework evaluated cortical microcircuit models
against 40+ experimental constraints across morphology, electrophysiology,
and connectivity.

## Source

[github.com/mayalucia/dmt-eval](https://github.com/mayalucia/dmt-eval)
