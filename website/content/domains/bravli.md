+++
title = "BRAVLi: Whole-Brain Digital Twin"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-20T12:00:00+01:00
tags = ["domains"]
draft = false
+++

![The complete Drosophila connectome: 139,255 neurons reconstructed at synaptic resolution. Image: FlyWire / Princeton.](/images/bravli/flywire-banner.jpg)

What does it take to build a biologically faithful digital twin of an entire brain?

Not a schematic. Not a wiring diagram. A computational object where 139,000 neurons fire, 50 million synapses transmit, and 8,453 cell types express their distinct electrical personalities --- all constrained by the actual anatomy.

BRAVLi is a literate codebase for reconstructing and simulating the _Drosophila_ connectome. The fruit fly brain is the first organism for which a complete synaptic-resolution wiring diagram exists (the FlyWire dataset). This makes it the ideal testbed for the MayaLucIA approach: start from sparse but high-quality measurements, exploit the interdependencies that physics and biology impose, and grow a dense, simulatable digital twin.

> Explore the connectome interactively: [FlyWire Codex](https://codex.flywire.ai) --- the Connectome Data Explorer lets you navigate 139,255 neurons, trace connections, and take snapshots of cells.


## Why Drosophila?

The fruit fly brain sits at a unique intersection: complex enough to exhibit rich behavior (navigation, learning, decision-making, sleep), yet small enough that every neuron and every synapse has been mapped. The FlyWire connectome provides:

- **139,255 neurons** with complete morphological reconstructions
- **~50 million synaptic connections** at nanometer resolution
- **8,453 cell types** classified by morphology, connectivity, and neurotransmitter identity

No other organism offers this combination of behavioral complexity and connectomic completeness. It is the natural starting point for anyone who wants to understand brains by building them.

> **Reference:** Dorkenwald _et al._, [Neuronal wiring diagram of an adult brain](https://doi.org/10.1038/s41586-024-07558-y), _Nature_ 634, 124--138 (2024).


## Roots in Blue Brain

![The Blue Brain Project at EPFL: building anatomically detailed digital twins of brain circuits. Image: Blue Brain Project / EPFL.](/images/bravli/bbp-header.jpg)

The human author of this project spent seven years (2017--2024) at the [Blue Brain Project](https://www.epfl.ch/research/domains/bluebrain/) at EPFL, where a team of 100+ scientists built anatomically detailed digital twins of rodent brain circuits. The Blue Brain pipeline --- from volumetric atlases through neuronal morphogenesis, connectome prediction, synaptic physiology, to large-scale simulation on supercomputers --- demonstrated that sparse experimental data, combined with biophysical constraints, can produce dense, biologically faithful models.

BRAVLi inherits the intellectual structure of that pipeline but applies it to a different organism (_Drosophila_ instead of rodent), a different data regime (complete connectome instead of statistical inference), and a radically different scale of operation (one scientist with AI agents instead of a dedicated engineering team). The lessons learned at Blue Brain --- about what works, what breaks, and what matters --- inform every design choice here.

**The BBP digital brain-building pipeline in its two landmark incarnations:**

- **2015 --- The Neocortical Microcircuit.** A digital reconstruction of ~31,000 neurons and ~37 million synapses in a 0.29 mm³ volume of juvenile rat somatosensory cortex. The first demonstration that biophysically detailed models could be built algorithmically from sparse data. Explore the data: [NMC Portal](https://bbp.epfl.ch/nmc-portal/).
  > Markram _et al._, [Reconstruction and Simulation of Neocortical Microcircuitry](https://doi.org/10.1016/j.cell.2015.09.029), _Cell_ 163(2), 456--492 (2015).

- **2024 --- The Somatosensory Cortex.** Scaling to ~4.2 million neurons and ~4.2 billion synapses across eight interconnected cortical subregions. The full non-barrel somatosensory cortex of the juvenile rat, with predicted inter-regional connectivity. Explore the data: [SSCx Portal](https://bbp.epfl.ch/sscx-portal/).
  > Reimann _et al._, [Modeling and Simulation of Rat Non-Barrel Somatosensory Cortex](https://doi.org/10.1101/2022.08.11.503144) (2024).

![The SSCx atlas: volumetric parcellation of eight interconnected cortical subregions. Image: Blue Brain Project / EPFL.](/images/bravli/sscx-hero.jpg)


## The Reconstruction Pipeline

BRAVLi follows MayaLucIA's iterative cycle --- Measure, Model, Manifest, Evaluate, Refine --- applied to neural tissue:

### 1. Parcellation & Atlas

Starting from the FlyWire volume, we define brain regions (neuropils), identify boundaries, and build a spatial atlas. This is the scaffold on which everything else is placed.

### 2. Cell Census

Each brain region is populated with the neurons that belong to it --- their positions, their morphological types, their neurotransmitter identities. The cell census is the first constraint: it tells us _who_ is where.

### 3. Morphological Diversity

Neurons are not points. They are extended objects whose dendritic and axonal arbors define the physical substrate of connectivity. We characterize the morphological diversity within each cell type and region.

### 4. Connectivity

The connectome provides ground-truth wiring at synaptic resolution. But connectivity is not random --- it follows rules imposed by morphology, spatial proximity, and cell-type identity. Understanding these rules is as important as knowing the wiring itself.

### 5. Synaptic Physiology

A synapse is not a binary switch. It has a weight, a time constant, a neurotransmitter, a plasticity rule. We assign physiological parameters to each synapse class, drawing on electrophysiological recordings and pharmacological data.

### 6. Neuromodulatory State

The same circuit can produce different behaviors depending on its neuromodulatory state (dopamine, serotonin, octopamine). We model state-dependent switching of circuit dynamics.

### 7. Simulation

The assembled digital twin is simulated: neurons fire, synapses transmit, circuits compute. We compare the emergent dynamics against known _in vivo_ recordings and behavioral observations.


## Literate Science

BRAVLi is organized as 18 Org-mode lessons that tangle into executable Python. Each lesson is simultaneously:

- A **tutorial** --- explaining the neuroscience and the computational method
- A **codebase** --- the source of truth lives in the prose, not in generated scripts
- A **research notebook** --- documenting choices, alternatives considered, and dead ends

This is MayaLucIA's co-ownership principle in practice: the artifact is legible to both human and machine. A scientist can read the lessons to understand the reasoning; an AI agent can read them to reproduce or extend the computation.


## What This Is Not

BRAVLi is not an enterprise brain-simulation platform. It is not trying to compete with large-scale initiatives. It is a _personal_ brain-building assistant --- a computational environment where a single scientist can explore, modify, and simulate neural circuits, guided by their own hypotheses and curiosity.

The goal is not to advance the frontier of neuroscience (that is for experimentalists). The goal is to _understand_ brain circuits by building them --- to make the abstract concrete, to turn connectivity matrices into firing patterns, to experience neural dynamics as something you can see, hear, and interact with.

In 2026, with modern AI agents at our side, a single scientist should be able to do what previously required a dedicated engineering team. BRAVLi is the proof of concept.
