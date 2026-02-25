+++
title = "Connectivity"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["bravli", "connectivity", "lesson"]
draft = false
+++

The FlyWire connectome provides the complete synaptic wiring diagram: every connection between every neuron, annotated with neurotransmitter type and synapse count. This lesson turns that raw edge list into analysable connectivity matrices and pathway maps.

## Lesson 08 --- Connectivity

Starting from ~50 million synaptic connections:

1. **Edge list loading** --- parsing the FlyWire synapse table
2. **Neurotransmitter assignment** --- each synapse inherits its presynaptic neuron's NT identity (ACh, GABA, Glu, 5-HT, DA, OA)
3. **Neuropil connectivity matrices** --- aggregating synapses by source/target neuropil to reveal the coarse wiring diagram
4. **Pathway analysis** --- tracing multi-hop paths between regions
5. **Motif analysis** --- identifying recurring circuit motifs (reciprocal, convergent, divergent)

The connectivity matrix is the skeleton on which all simulation and analysis hangs. Get this right, and the dynamics emerge from the wiring.

---

**Source:** [`domains/bravli/codev/08-connectivity.org`](https://github.com/mayalucia/bravli) (1,045 lines, ~39 KB)
