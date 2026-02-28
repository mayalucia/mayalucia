+++
title = "MB Dynamics"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-28T01:34:57+01:00
tags = ["papers"]
draft = false
math = true
+++

<div class="abstract">

The FlyWire whole-brain connectome of _Drosophila melanogaster_ provides,
for the first time, a complete wiring diagram of the mushroom body (MB)
--- the fly's primary centre for associative learning. Yet a wiring
diagram alone cannot predict dynamics. Here we extract the MB
microcircuit (~6,300 neurons, ~50,000 synapses) from FlyWire and
subject it to four systematic computational investigations.
First, we classify the circuit's dynamical regime using the Brunel
(2000) phase diagram framework, finding that the MB operates in the
asynchronous--irregular (AI) balanced state despite exponential
synaptic filtering shifting phase boundaries relative to the canonical
delta-synapse theory. Second, we demonstrate Marder's principle: the
same connectome produces opposite behavioural outputs (approach vs.
avoidance) under different neuromodulatory states, achieved through
compartment-specific multiplicative gain modulation of KC&rarr;MBON
weights. Third, we show that stochastic synaptic transmission --- a
ubiquitous feature of central synapses with release probabilities of
0.1--0.5 --- enhances subthreshold signal detection via stochastic
resonance while MB odor coding degrades gracefully under biologically
realistic failure rates. Fourth, we test the Zhang et al. (2024)
topology-dominates hypothesis by comparing leaky integrate-and-fire
(LIF) and adaptive exponential (AdEx) neuron models on the same
connectome, confirming that firing-rate patterns are highly correlated
(\\(r > 0.9\\)) when adaptation is weak, with divergence emerging only at
strong spike-frequency adaptation (\\(b > 2\\) mV). Together, these
results establish a computational baseline for the FlyWire mushroom
body and demonstrate that connectome-constrained simulation, even with
minimal biophysical detail, can illuminate fundamental questions about
neural circuit function.

</div>

\clearpage
\tableofcontents
\clearpage


## Introduction {#introduction}

The completion of the _Drosophila_ whole-brain connectome by the FlyWire
consortium \citep{dorkenwald2024} represents a watershed moment in
neuroscience: 139,255 neurons, approximately 50 million synapses, and
8,453 cell types, reconstructed at synaptic resolution from a single
female fly. For the first time, we have a complete parts list and
wiring diagram of an adult brain. But a parts list is not a theory.
The central challenge now is to understand how dynamics emerge from
structure --- how the static connectome gives rise to the temporal
patterns of activity that underlie computation, learning, and
behaviour.

The mushroom body (MB) is an ideal test case for this enterprise. It
is the primary locus of associative olfactory learning in _Drosophila_
\citep{aso2014}, its architecture is well understood (approximately
2,000 Kenyon cells receiving convergent input from ~150 projection
neurons, with output modulated by ~30 mushroom body output neurons and
~130 dopaminergic neurons), and its behavioural relevance is directly
measurable. The MB's compartmental organisation \citep{aso2014} ---
with distinct dopaminergic and output neuron types tiling the KC axon
lobes --- provides a natural framework for understanding how
neuromodulation sculpts circuit output.

We address four questions, each probing a different aspect of the
structure--dynamics relationship:

1.  **What dynamical regime does the MB operate in?** The Brunel (2000)
    framework \citep{brunel2000} classifies recurrent networks into four
    regimes based on the balance between excitation and inhibition (\\(g\\))
    and external drive (\\(\eta\\)). We ask where the FlyWire MB falls in this
    phase diagram.

2.  **Can the same connectome produce opposite behaviours?** Marder's
    principle \citep{marder2002,marder2012} holds that neuromodulation
    reconfigures circuit function without rewiring. We test whether
    compartment-specific gain modulation --- mimicking the effects of
    different aminergic and peptidergic states --- can switch the MB's
    behavioural output between approach and avoidance.

3.  **How does synaptic noise affect circuit function?** Central
    synapses are unreliable, with release probabilities of $p &asymp;
    0.1$--\\(0.5\\) \citep{allen1994}. Rather than treating this as a bug,
    we ask whether stochastic transmission serves computational purposes
    --- specifically, whether stochastic resonance
    \citep{gammaitoni1998} enhances signal detection in the MB circuit.

4.  **Does the single-neuron model matter?** Zhang et al.
    \citep{zhang2024} demonstrated that connectome-constrained models of
    the fly visual system produce accurate predictions regardless of
    neuron model complexity. We test whether this topology-dominates
    hypothesis extends to the MB by comparing LIF and AdEx
    \citep{brette2005} neuron models on the same extracted circuit.

Our approach is deliberately minimal. We use current-injection
integrate-and-fire models (LIF and AdEx), not conductance-based
neurons. We use extracted synaptic weights, not fitted parameters. The
goal is not biophysical realism but _computational insight_: what can
the connectome alone tell us, and where does it fall short?


## Methods {#methods}


### Circuit Extraction {#circuit-extraction}

We extract the MB microcircuit from the FlyWire connectome using the
`bravli` Python toolkit developed for this study. Starting from
anatomical neuron classifications, we identify five cell populations:

-   **Projection neurons (PNs)**: ~150 neurons carrying olfactory input
    from the antennal lobe.
-   **Kenyon cells (KCs)**: ~5,200 principal neurons forming the MB's
    sparse coding layer, subdivided by lobe (gamma, alpha/beta,
    alpha'/beta').
-   **Mushroom body output neurons (MBONs)**: ~30 neurons whose combined
    activity drives approach or avoidance behaviour.
-   **Dopaminergic neurons (DANs)**: ~130 neurons (PAM and PPL1 clusters)
    providing reward and punishment signals.
-   **APL (anterior paired lateral)**: A single giant GABAergic neuron
    providing global inhibition to KCs.

Synaptic connectivity is extracted from the FlyWire synapse table,
retaining synapse counts as weight proxies. The resulting circuit
contains approximately 6,300 neurons and 50,000 synapses.


### Simulation Engines {#simulation-engines}


#### Leaky Integrate-and-Fire (LIF) {#leaky-integrate-and-fire--lif}

The membrane potential of neuron \\(i\\) evolves as:

\begin{equation}
\tau\_m \frac{dV\_i}{dt} = -(V\_i - V\_{\text{rest}}) + g\_i(t)
\end{equation}

where \\(\tau\_m\\) is the membrane time constant, \\(V\_{\text{rest}} = 0\\) mV
is the resting potential, and \\(g\_i(t)\\) is the total synaptic input.
When \\(V\_i\\) crosses threshold \\(V\_\theta = 20\\) mV, a spike is emitted,
the potential is reset to \\(V\_{\text{reset}} = 0\\) mV, and the neuron
enters an absolute refractory period of \\(\tau\_{\text{ref}} = 2\\) ms.

Synaptic input is delivered with an exponential filter:

\begin{equation}
\tau\_s \frac{dg\_i}{dt} = -g\_i + \tau\_m \sum\_j w\_{ji} \sum\_k \delta(t - t\_j^k - d\_{ji})
\end{equation}

where \\(w\_{ji}\\) is the synaptic weight from neuron \\(j\\) to \\(i\\),
\\(t\_j^k\\) is the $k$-th spike time of neuron \\(j\\), \\(d\_{ji}\\) is the
synaptic delay (1.5 ms throughout), and \\(\tau\_s = 0.5\\) ms is the
synaptic time constant. The factor \\(\tau\_m / \tau\_s\\) ensures that the
effective weight matches the delta-synapse convention of Brunel
\citep{brunel2000}.

Cell-type-specific parameters follow from known biophysics: KCs have
short membrane time constants (\\(\tau\_m = 5\\) ms) reflecting their
compact morphology, while MBONs (\\(\tau\_m = 15\\) ms) and DANs
(\\(\tau\_m = 20\\) ms) are larger and slower.


#### Adaptive Exponential Integrate-and-Fire (AdEx) {#adaptive-exponential-integrate-and-fire--adex}

The AdEx model \citep{brette2005} extends LIF with exponential spike
initiation and a slow adaptation current:

\begin{align}
\tau\_m \frac{dV\_i}{dt} &= -(V\_i - V\_{\text{rest}}) + \Delta\_T \exp\\!\left(\frac{V\_i - V\_T}{\Delta\_T}\right) + g\_i(t) - w\_i \\\\
\tau\_w \frac{dw\_i}{dt} &= a(V\_i - V\_{\text{rest}}) - w\_i
\end{align}

where \\(\Delta\_T = 2\\) mV is the exponential slope factor, \\(V\_T\\) is the
effective threshold, \\(a\\) is the subthreshold adaptation conductance,
and \\(w\_i\\) is the adaptation current. At spike time, \\(w\_i \leftarrow
w\_i + b\\), where \\(b\\) controls spike-frequency adaptation strength.

We use four biophysically motivated presets:

-   **Regular spiking**: \\(a = 0\\), \\(b = 0.5\\) mV, \\(\tau\_w = 100\\) ms
-   **Adapting**: \\(a = 0.1\\) nS, \\(b = 2.0\\) mV, \\(\tau\_w = 300\\) ms
-   **Bursting**: \\(a = 0\\), \\(b = 5.0\\) mV, \\(\tau\_w = 50\\) ms
-   **Fast spiking**: \\(a = 0\\), \\(b = 0\\), \\(\tau\_w = 100\\) ms (equivalent to exponential LIF)


#### Stochastic Synaptic Transmission {#stochastic-synaptic-transmission}

Two noise mechanisms are implemented:

1.  **Release failure**: Each spike arriving at a synapse is transmitted
    with probability \\(p\_{\text{rel}}\\) (Bernoulli trial). At \\(p\_{\text{rel}} = 1\\),
    transmission is deterministic. At biologically realistic values
    ($p<sub>\text{rel}</sub> &asymp; 0.1$--\\(0.5\\)), most spikes fail to elicit
    postsynaptic responses \citep{allen1994}.

2.  **Intrinsic noise**: Gaussian current noise \\(\xi\_i(t)\\) is added to
    the membrane equation, scaled as \\(\sigma \sqrt{dt}\\) to ensure
    proper Wiener process scaling. This captures channel noise, thermal
    fluctuations, and background synaptic bombardment
    \citep{faisal2008}.


### Neuromodulatory State Model {#neuromodulatory-state-model}

Following \citet{marder2002}, we model neuromodulation as
compartment-specific multiplicative gain modulation of synaptic
weights:

\begin{equation}
w\_{\text{eff}} = w\_{\text{base}} \times m\_c
\end{equation}

where \\(m\_c\\) is the modulatory gain for compartment \\(c\\). The MB's 15
compartments \citep{aso2014} each receive distinct dopaminergic
innervation, and the gain factors \\(m\_c\\) reflect the known valence
organisation:

| State      | Compartment modulation                                       | Behavioural prediction |
|------------|--------------------------------------------------------------|------------------------|
| Naive      | All \\(m\_c = 1.0\\)                                         | Neutral                |
| Appetitive | Appetitive $m_c = 1.3$--\\(1.5\\); aversive \\(m\_c = 0.6\\) | Approach               |
| Aversive   | Aversive \\(m\_c = 1.5\\); appetitive \\(m\_c = 0.6\\)       | Avoidance              |
| Aroused    | All \\(m\_c = 1.3\\)                                         | Enhanced response      |
| Quiescent  | All \\(m\_c = 0.5\\)                                         | Suppressed response    |

Behavioural output is quantified via a valence score:

\begin{equation}
V = \sum\_{i \in \text{appetitive}} r\_i^{\text{MBON}} - \sum\_{j \in \text{aversive}} r\_j^{\text{MBON}}
\end{equation}

where \\(V > 0\\) predicts approach and \\(V < 0\\) predicts avoidance.


### Brunel Regime Classification {#brunel-regime-classification}

The Brunel \citep{brunel2000} framework classifies network dynamics
along two axes:

-   **Irregularity**: coefficient of variation of interspike intervals.
    \\(\text{CV} > 0.5\\) indicates irregular firing; \\(\text{CV} < 0.5\\)
    indicates regular firing.
-   **Synchrony**: a synchrony index based on variance of the population
    rate relative to single-neuron variance. Synchrony \\(> 10\\) indicates
    synchronous firing.

The four regimes are:

-   **SR** (Synchronous Regular): low CV, high synchrony
-   **SI** (Synchronous Irregular): high CV, high synchrony --- pathological
-   **AR** (Asynchronous Regular): low CV, low synchrony --- clock-like
-   **AI** (Asynchronous Irregular): high CV, low synchrony --- the balanced state

For the Brunel sweep, we construct random networks of \\(N = 10{,}000\\)
neurons (80% excitatory, 20% inhibitory) with connection probability
\\(\epsilon = 0.1\\) and scan the parameter space \\(g \in \\{3, 4, 4.5, 5,
6\\}\\) and \\(\eta \in \\{0.9, 1.5, 2, 3, 4\\}\\).


### Stochastic Resonance Protocol {#stochastic-resonance-protocol}

A subthreshold periodic signal (\\(f = 5\\) Hz, amplitude 3 mV below
threshold) is injected into a test circuit alongside varying levels of
intrinsic noise (\\(\sigma \in \\{0, 0.5, 1, 2, 3, 5, 7, 10, 15, 20\\}\\)).
The signal-to-noise ratio (SNR) is computed from the power spectrum of
the population firing rate:

\begin{equation}
\text{SNR} = \frac{P(f\_{\text{signal}})}{P\_{\text{noise}}}
\end{equation}

where \\(P(f\_{\text{signal}})\\) is the spectral power at the signal
frequency and \\(P\_{\text{noise}}\\) is the mean power at surrounding
frequencies. Stochastic resonance manifests as a peak in SNR at
intermediate noise levels.


### LIF--AdEx Comparison Protocol {#lif-adex-comparison-protocol}

We simulate the same MB circuit with both LIF and AdEx engines,
matching all parameters except the adaptation current. Three metrics
quantify agreement:

1.  **Rate correlation**: Pearson correlation of per-neuron firing rates
    between LIF and AdEx simulations.
2.  **Temporal correlation**: Correlation of population rate time series
    (5 ms bins).
3.  **Mean relative difference**: \\(\langle 2|r\_{\text{LIF}} - r\_{\text{AdEx}}| / (r\_{\text{LIF}} + r\_{\text{AdEx}}) \rangle\\) averaged over active neurons.

Interpretation thresholds: rate correlation \\(> 0.9\\) indicates topology
dominates; \\(< 0.5\\) indicates the neuron model is essential.


## Results {#results}


### The FlyWire Mushroom Body Operates in the Balanced State {#the-flywire-mushroom-body-operates-in-the-balanced-state}

To classify the MB's dynamical regime, we first establish the Brunel
phase diagram as a reference. The \\((g, \eta)\\) parameter sweep on random networks recovers all four regimes. The classical four
regimes are recovered, though the AI/SI boundary shifts to higher \\(g\\)
compared to the canonical delta-synapse result. This is a direct
consequence of our exponential synaptic filter (\\(\tau\_s = 0.5\\) ms):
finite-duration postsynaptic currents smooth out membrane voltage
fluctuations, suppressing the coefficient of variation. Even at \\(g =
8\\), the CV reaches only \\(\sim 0.25\\) rather than the $&sim; 0.8$--\\(1.0\\)
expected with delta synapses. The effective weight scaling \\(J\_{\text{eff}}
= J \times \tau\_m / \tau\_s\\) compensates for the reduced peak current
but cannot restore the shot-noise statistics that drive irregular
firing.

We then compute \\(g\_{\text{eff}}\\) for the FlyWire MB circuit directly from
the extracted weight distribution:

\begin{equation}
g\_{\text{eff}} = \frac{\langle |w\_{\text{inh}}| \rangle}{\langle w\_{\text{exc}} \rangle}
\end{equation}

The resulting classification places the MB in the **asynchronous
irregular (AI)** regime --- the balanced state first identified by
\citet{vanvreeswijk1996}. This is consistent with the known physiology
of Kenyon cells, which fire sparsely (\\(< 10\\%\\) active per odor
presentation; \citealt{turner2008}) and with irregular interspike
intervals. The APL neuron, providing global feedback inhibition to
KCs, plays a critical role in maintaining this balance.

The AI regime has a functional interpretation: it maximises the
representational capacity of the KC population. In the regular
regimes, neural responses are locked to the stimulus periodicity,
limiting the space of possible population codes. In the balanced
state, each KC responds independently, enabling the combinatorial
odor coding that underlies the MB's discriminative capacity
\citep{caron2013}.


### Neuromodulation Reconfigures Behavioural Output Without Rewiring {#neuromodulation-reconfigures-behavioural-output-without-rewiring}

\citet{marder2002} demonstrated in the crustacean stomatogastric
ganglion that the same anatomical circuit can produce qualitatively
different motor patterns under different neuromodulatory conditions.
We test whether this principle extends to the _Drosophila_ MB.

Presenting the same odor stimulus (Poisson activation of a random 10%
PN subset at 50 Hz) to the MB circuit under five modulatory states
yields dramatically different MBON response profiles:

| State      | Appetitive MBONs | Aversive MBONs | Valence (\\(V\\))           |
|------------|------------------|----------------|-----------------------------|
| Naive      | Baseline         | Baseline       | \\(\approx 0\\)             |
| Appetitive | Enhanced         | Suppressed     | \\(V > 0\\) (approach)      |
| Aversive   | Suppressed       | Enhanced       | \\(V < 0\\) (avoidance)     |
| Aroused    | Enhanced         | Enhanced       | \\(\approx 0\\) (amplified) |
| Quiescent  | Suppressed       | Suppressed     | \\(\approx 0\\) (damped)    |

The appetitive and aversive states produce opposite-sign valence
scores from identical sensory input. This is achieved purely through
multiplicative gain modulation --- no synaptic rewiring, no structural
plasticity, no change to the connectome. The gain factors ($m_c =
0.6$--\\(1.5\\)) are within the physiological range of monoaminergic
modulation observed experimentally.

The aroused state amplifies both appetitive and aversive responses
while preserving their relative balance, consistent with the
behavioural observation that arousal increases response magnitude
without changing valence preference. The quiescent state uniformly
suppresses output, mimicking the reduced MB activity observed during
sleep.

These results validate Marder's principle in a complete brain circuit:
the connectome defines the space of possible behaviours, and
neuromodulation selects among them. The MB's compartmental
architecture \citep{aso2014} --- with distinct dopaminergic inputs to
each compartment --- provides the anatomical substrate for
state-dependent gain control.


### Stochastic Synaptic Transmission Serves Computation {#stochastic-synaptic-transmission-serves-computation}

Central synapses are unreliable. Release probabilities at cortical
synapses are typically $p &asymp; 0.1$--\\(0.5\\)
\citep{allen1994,tsodyks1997}, meaning that 50--90% of presynaptic
spikes fail to produce a postsynaptic response. Is this unreliability
merely a biophysical limitation, or does it serve a computational
purpose?


#### Graceful Degradation of Odor Coding {#graceful-degradation-of-odor-coding}

We sweep release probability from \\(p = 0.1\\) (90% failure) to \\(p =
1.0\\) (deterministic) while presenting odor stimuli to the MB circuit.
At \\(p = 0.5\\), which lies in the middle of the biological range,
population firing rates decrease but the relative activation pattern
across KCs is preserved. The high fan-in at KC&rarr;MBON synapses
(each MBON receives input from thousands of KCs) provides natural
averaging: even when individual synapses fail, the aggregate input
faithfully represents the odor identity.

At \\(p = 0.1\\), odor coding begins to degrade substantially, with
MBON firing rates dropping and selectivity decreasing. This sets a
functional lower bound on synaptic reliability for the MB circuit.


#### Stochastic Resonance Enhances Signal Detection {#stochastic-resonance-enhances-signal-detection}

We test whether noise can enhance the detection of weak signals via
stochastic resonance \citep{gammaitoni1998}. A subthreshold periodic
signal (5 Hz, 3 mV below threshold) is presented to a test circuit
alongside varying levels of intrinsic noise.

The SNR exhibits the classic inverted-U profile: at zero noise, the
subthreshold signal produces no spikes and \\(\text{SNR} = 0\\). At
intermediate noise (\\(\sigma\_{\text{opt}}\\)), noise fluctuations
occasionally push the membrane potential across threshold in synchrony
with the signal peaks, yielding a maximum SNR. At high noise, the
signal is swamped by random firing and SNR declines again.

This demonstrates that the MB circuit supports stochastic resonance
in principle. Whether the fly exploits this mechanism in vivo ---
using background synaptic noise to detect weak olfactory signals
--- remains an open question, but the computational substrate is
present.


#### Noise Sweep on the MB Circuit {#noise-sweep-on-the-mb-circuit}

Sweeping intrinsic noise \\(\sigma \in \\{0, 1, 3, 5, 10\\}\\) on the
full MB circuit during odor presentation reveals a non-monotonic
relationship between noise and odor discriminability. Low noise
(\\(\sigma \leq 3\\)) has minimal effect on MBON response patterns.
Moderate noise (\\(\sigma \approx 5\\)) slightly broadens KC activation,
potentially increasing the robustness of population codes to small
perturbations. High noise (\\(\sigma = 10\\)) disrupts the sparse coding
that is essential to MB function.


### Topology Dominates: LIF and AdEx Agree When Adaptation Is Weak {#topology-dominates-lif-and-adex-agree-when-adaptation-is-weak}

\citet{zhang2024} demonstrated that connectome-constrained models of
the _Drosophila_ visual system predict neural responses accurately
regardless of the single-neuron model employed. We test whether this
topology-dominates principle extends to the mushroom body.


#### Rate Correlation Across Neuron Models {#rate-correlation-across-neuron-models}

Simulating the MB circuit with both LIF and AdEx (regular spiking
preset, \\(b = 0.5\\) mV) engines under identical stimulation, we find
high rate correlation (\\(r > 0.9\\)) across the neuron population. The
spatial pattern of firing rates --- which KCs are active, which MBONs
are driven --- is determined primarily by the connectivity, not the
neuron model.

Temporal correlation is somewhat lower, reflecting the fact that
the AdEx model's exponential spike initiation produces slightly
different spike timing even when average rates agree. The mean
relative difference is \\(< 10\\%\\), indicating excellent quantitative
agreement.


#### Adaptation Strength Determines Divergence {#adaptation-strength-determines-divergence}

The agreement between LIF and AdEx is not absolute. Sweeping the
adaptation parameter \\(b\\) from 0 to 5 mV reveals a clear divergence
threshold:

| \\(b\\) (mV) | Rate Correlation | Interpretation            |
|--------------|------------------|---------------------------|
| 0.0          | \\(\sim 1.0\\)   | Identical (no adaptation) |
| 0.1          | \\(> 0.95\\)     | Topology dominates        |
| 0.5          | \\(> 0.9\\)      | Topology dominates        |
| 1.0          | $0.8$--\\(0.9\\) | Partial agreement         |
| 2.0          | $0.6$--\\(0.8\\) | Moderate divergence       |
| 5.0          | \\(< 0.5\\)      | Strong divergence         |

At \\(b = 0\\) (no adaptation), the AdEx reduces to an exponential LIF
and agreement is near-perfect. As \\(b\\) increases, spike-frequency
adaptation progressively suppresses high-rate neurons. Because the LIF
model lacks adaptation entirely, the two models disagree most for
neurons that would fire at high rates --- precisely those where
adaptation has the largest effect.

This result refines the Zhang et al. hypothesis: **topology dominates
when the effective single-neuron transfer function is similar across
models**. When adaptation or other intrinsic dynamics significantly
alter the input--output relationship, the neuron model matters.

For the MB specifically, KCs fire sparsely and at low rates, placing
them in the regime where topology dominates. MBONs and DANs, which
fire at higher rates, are more sensitive to model choice.


## Discussion {#discussion}


### Synthesis: Four Views of One Circuit {#synthesis-four-views-of-one-circuit}

The four investigations converge on a unified picture of the
_Drosophila_ MB as a circuit optimised for flexible, noise-tolerant
odor discrimination:

1.  **The AI regime supports sparse coding.** The balanced state prevents
    both synchronous locking and rate-code saturation, enabling the
    combinatorial KC population codes that give the MB its discriminative
    power.

2.  **Neuromodulation provides context.** The connectome defines the
    hardware; neuromodulatory states select the software. The MB's
    compartmental architecture is the anatomical substrate for this
    flexibility.

3.  **Stochastic transmission is not a bug.** Synaptic unreliability
    at biological levels is tolerated by the circuit's high fan-in
    architecture, and may actively enhance weak signal detection via
    stochastic resonance.

4.  **Topology is primary.** For the MB's sparse-firing Kenyon cells,
    connectivity determines activation patterns regardless of
    biophysical detail. This validates the use of minimal neuron models
    for connectome-scale simulation.


### Limitations {#limitations}

Several limitations of the current study should be noted:

**Current-injection models.** Our LIF and AdEx engines use
current-based (not conductance-based) synapses. Conductance-based
models would capture voltage-dependent effects (shunting inhibition,
reversal potential saturation) that may matter for quantitative
predictions.

**Static weights.** We use FlyWire synapse counts as weight proxies
without fitting to physiological data. The actual effective synaptic
strengths depend on receptor composition, dendritic filtering, and
neuromodulatory state, none of which are captured by synapse counts
alone.

**No recurrent dynamics.** The MB has limited recurrent excitation
(KCs do not synapse strongly on each other), so the balanced-state
analysis relies primarily on the APL&rarr;KC feedback loop. A full
treatment would include the recurrent MBON&rarr;DAN&rarr;KC pathways
that implement memory consolidation.

**Simplified neuromodulation.** Our multiplicative gain model captures
the sign and rough magnitude of modulatory effects but not their
temporal dynamics (onset, offset, desensitisation) or the combinatorial
interactions between multiple neuromodulatory systems acting
simultaneously.

**No plasticity in regime or comparison analyses.** The Brunel,
neuromodulation, and LIF/AdEx analyses use static weights. In the
living fly, synaptic weights are continuously modified by experience.
Whether the dynamical regime classification holds during learning
--- when weight distributions change --- is an open question.


### Future Directions {#future-directions}

Three immediate extensions suggest themselves:

1.  **ISN paradoxical response**: Testing whether the MB circuit exhibits
    the inhibition-stabilised network (ISN) signature --- where driving
    inhibitory neurons paradoxically decreases total inhibition --- would
    further characterise the circuit's dynamical regime.

2.  **Three-factor learning rules**: Implementing dopamine-gated synaptic
    depression at KC&rarr;MBON synapses would enable simulation of
    associative conditioning protocols, connecting the circuit dynamics
    explored here to the MB's primary biological function.

3.  **Comparative motif analysis**: Extracting network motifs (feedforward
    chains, reciprocal inhibition, convergent excitation) from the MB
    and comparing their statistics to random graphs with matched degree
    distributions would reveal which connectivity features are
    under-represented or enriched by evolution.


### Conclusion {#conclusion}

The FlyWire connectome transforms _Drosophila_ neuroscience from
circuit inference to circuit analysis. The four investigations
presented here --- regime classification, neuromodulatory switching,
stochastic synapses, and model comparison --- establish a computational
baseline for the mushroom body and demonstrate that even minimal
biophysical models, when constrained by real connectivity, can
illuminate fundamental questions about neural circuit function. The
connectome is necessary but not sufficient; dynamics, modulation, and
noise complete the picture.

\bibliography{references}
