+++
title = "Bravli: Brain Reconstruction"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-28T19:02:25+01:00
tags = ["domains"]
draft = false
+++

What does it take to build biologically faithful digital copied of the brain?

At BBP we discovered that to build digital twins of the brain we had to:

1.  Generate the volumes and dimensions of all brai regions
2.  Populate neurons and glia according to their densities and distributions in each brain region
3.  Define morphological, electrical, and genetic cell types in each brain region
4.  Develop algorithms for computationally growing the dendrites of an unlimited number of neurons expressing their variety of morphological types in each brain region
5.  Model an unlimited number of neurons that express their variety of electrical behaviors
6.  Grow all the local, regional and whole brain axons of every type of neuron in the mouse brain
7.  Recreate the connectome down to a neuron to neuron level
8.  Model various types of synapses formed between any two neurons in the brain
9.  Simulate neurons, brain regions, brain systems, and the whole mouse brain on supercomputers and in the cloud.

A key strategy is to exploit interdependencies in the experimental data to build detailed, dense models from sparse data sets and employ algorithmic procedures that apply the converging constraints to fill in the experimentally missing data.


## A Computational Environment to Build Brains {#a-computational-environment-to-build-brains}

We want a computational environment in which we can,

Explore
: Conduct atlas-driven exploration of existing experimental data, model data, digital brain models, and simulations. This structured and systematic exploration is further enhanced by powerful literature mining tools ensuring that their investigations are grounded in the most current and relevant scientific information.


Build
: Use available tools, or develop new ones, to create custom brain models at multiple scales, either from scratch or by modifying existing models, empowering hypothesis testing and innovative approaches to understanding the brain.


Experiment
: Run experiments and model complex brain processes in a controlled, reproducible setting,— extending possibilities beyond traditional biological labs.

We do not want an _enterprise_ solution for this. We want to develop a scientist's personal brain building assistant. In our endeavor we will start from scratch in early 2026, employing the latest AI technologies.

Data-driven modeling approach will require us to organize our data, such that it is well curated and indexed to allow efficient search and cross-referencing. The input data we need for brain building is _multi-modal_ and our data banks must accommodate different custom data formats. This is a complex problem, and BBP developed an independent knowledge management tool, Blue Brain Nexus. For the growth of the individual scientist,  Nexus is an overkill. It is an enterprise solution for knowledge management.

What about a single scientist's personal adventures? For that each scientist chooses their own. In my experience their choice is determined mostly by their work culture, and career aspirations. There are a lot of online services --- centered around sharing. However, my feeling is that most of the interface offering services are a thing of the past in the age of modern AI in early 2026. We should be able to allow a completely totally personalized to extreme interface to any scientist. Coding agents should be able to handle the details of interfacing the scientist's `virtual-lab` or studio to a distributed knowledge base from where they can draw experimental data.

The exercise of brain building cannot be automated. The scientist will have to make many choices. The whole process must be lead by a hypothesis. Just like the science we are studying, our scientific  hypothesis will also be complex. We may not even begin with a hypothesis. The computational environment we are making should allow us to explore the world of neuroscience. And not just with raw scientific facts. But by describing neurological processes of information processing in an interactive way.

The brain's anatomy and physiology and fascinating. The main goal of our computational environment will not be to advance the frontier of neuroscience. That is for actual humans to do. What we aim for is to enable the scientist to enjoy their science by providing a computational environment with rich audio-visual interaction. With modern coding agents in 2026 we should be able to develop an environment that is mostly invisible to the scientist when they are developing a study, and yet completely customizable. Neuroscientists are delighted to see animations of action potentials running up and down a neuron's neurites, especially if the animation demonstrates their scientific inquiry. Yet, this remains a complex thing to implement even for advanced computational neuroscientist because of the complexities of GPU rendering. BBP had dedicated graphics team for visualization. However, in 2026 with advanced LLMs and AI at our side, we should not need much help from graphics engineers. Our computational environment should be able to provide agents that are expert engineer of any particular expertize we want. By doing the extra effort of learning a little about how to customize such an agent, the user neuroscientist should be able to develop bespoke visualizations in our computational environment.

In the next section [Blue Brain Project's Rat SSCx](#blue-brain-project-s-rat-sscx) we can read the introduction to BBP's publication on their juvenile rat SSCx model. It takes enterprise level resources to reproduce a digital artifact such as a the anatomically detailed model developed by BBP. However, it should not take an enterprise solution for an enthusiastic scientist to explore brain circuit anatomy and physiology by recreating it on their computer. Once again, in early 2026 we should be able to summon our computational environment's LLM agents to help us along.


## Blue Brain Project's Rat SSCx {#blue-brain-project-s-rat-sscx}

Cortical dynamics underlie many cognitive processes and emerge from complex multi-scale interactions. These emerging dynamics can be explored in _large-scale, data-driven, biophysically-detailed_ models (??, ????,  ??, a), which integrate different levels of organization. The strict biological and spatial context enables the integration of knowledge and theories, the testing and generation of precise hypotheses, and the opportunity to recreate and extend diverse laboratory experiments based on a single model. This approach differs from more abstract models in that it emphasizes _anatomical completeness_ of a chosen brain volume rather than implementing a specific hypothesis. Using a “bottom-up" modelling approach, many detailed constituent models are combined to produce a larger, multi-scale model. To the best possible approximation, such models should explicitly include different cell and synapse types with the same quantities, geometric configuration and connectivity patterns as the biological tissue it represents.

Investigating the multi-scale interactions that shape perception requires a model of multiple cortical subregions with inter-region connectivity, and for certain aspects, the subcellular resolution provided by a morphologically detailed model is also required. In particular, (??, a) argued that the function of the healthy or diseased brain can only be understood when the true physical nature of neurons is taken into account and no longer simplified into point-neuron networks. Also, ?? (a) pointed out that simulations of large-scale models are essential for bridging the scales between the neuron and system levels in the brain. In that regard, modern electron-microscopic datasets have reached a scale that allows the reconstruction of a ground truth wiring diagram of local connectivity between several thousand neurons (??, a). However, this only covers a small fraction of the inputs a cortical neuron receives. While afferents from outside the reconstructed volume are detected, one can only speculate about the identity of their source neurons and connections between them. The scale required to understand inter-regional interactions is only available at lower resolutions in the form of region-to-region or voxel-to-voxel connectivity data.

To help better understand cortical structure and function, we present a general approach to create morphologically detailed models of multiple interconnected cortical regions based on the geometry of a digitized volumetric brain atlas, with synaptic connectivity predicted from anatomy and biological constraints (Figure [BROKEN LINK: fig:workflow-overview]). We used it to build a model of the juvenile rat non-barrel somatosensory (nbS1) regions (Figure [BROKEN LINK: fig:workflow-overview], center). These regions were selected for the wealth of available experimental data from various labs, and to build upon our previous modeling work (Table [BROKEN LINK: tab:tab_references]). The workflow is based on the work described in ?? (), with several additions, refinements and new data sources that have been independently described and validated in separate publications (Table [BROKEN LINK: tab:tab_references]). The model captures the morphological diversity of neurons and their placement in the actual geometry of the modeled regions through the use of voxelized atlas information. We calculated at each point represented in the atlas the distance to and direction towards the cortical surface (Figure [BROKEN LINK: fig:workflow-overview]; step 1). We used that information to select from a pool of morphological reconstructions anatomically fitting ones and orient their dendrites and axons appropriately (Figure [BROKEN LINK: fig:workflow-overview]; step 2). As a result, the model was anatomically complete in terms of the volume occupied by dendrites in individual layers. We then combined established algorithms for the prediction of local (??, a) and mid-range (??, a) connectivity (Figure [BROKEN LINK: fig:workflow-overview]; step 3) as well as extrinsic connectivity from thalamic sources ((??, ), (Figure [BROKEN LINK: fig:workflow-overview]; step 4) to generate a connectome at subcellular resolution that combines those scales.

We characterized several emerging aspects of connectivity (Figure [BROKEN LINK: fig:workflow-overview]; step 5). First, we found that brain geometry, i.e., differences in cortical thickness and curvature have surprisingly large effects on how much individual layers contribute to the connections a neuron partakes in. Second we characterized the predicted structure of connectivity at an unprecedented scale and determine its implications for neuronal function. In particular, we analyzed how the widths of thalamo-cortical axons constrains the types of cortical maps emerging. Furthermore, we characterized the global topology of interacting local and mid-range connectivity, finding highly complex topology of local and mid-range connectivity that specifically requires neuronal morphologies. Finally, we systematically analyzed the higher-order structure of connectivity beyond the level of pairwise statistics, such as connection probabilities. Doing so, we characterized highly connected clusters of neurons, distributed throughout the volume that are tied together by mid-range synaptic paths mediated by neurons in layer 5, which act as “highway hubs" interconnecting spatially distant neurons in the model. The highly non-random structure of higher-order interactions in the model's connectivity was further validated in a range of follow-up publications using the model (??, a,  ??, a,  ??, a,  ??, a).

Finally, we present an accompanying manuscript that details neuronal and synaptic physiology modeled on top of these results, describes the emergence of an _in vivo_-like state of simulated activity, and delivers a number of _in silico_ experiments generating insights about the neuronal mechanisms underlying published _in vivo_ and _in vitro_ experiments (?? (a); Figure [BROKEN LINK: fig:workflow-overview]; step 6).

The anatomically detailed modeling approach provides a one-to-one correspondence between most types of experimental data and the model, allowing the data to be readily integrated. However, this also leads to the difficult challenge to curate the data and decide which anatomical trend should be integrated next. Due to the incredible speed of discovery in the field of neuroscience an integrative model will always be lagging behind the latest results, and due to its immense breadth, there is no clear answer to which feature is most important. We believe the solution to this is to provide a validated model with clearly characterized strengths and weaknesses, along with the computational tools to customize it to fit individual projects. We have therefore made not only the model, but also most of our tool chain openly available to the public (Figure [BROKEN LINK: fig:workflow-overview]; step 7).

Already the process of adding a new data source to drive a refinement of the model serves to provide important insights. We demonstrate this by comparing the model to connectivity characterized through electron microscopy (??, a), finding mismatches, and describing the changes required to fix them. This allowed us to determine which rules are required to predict connectivity from the locations and densities of neuronal processes. Previously, simple overlap of distributions of axonal and dendritic segments has been proposed (Peters' rule; (??, a,  ??, a)), and contrasted with findings of preference for specific cell types or subcellular domains (??, a,  ??, a). Our approach to local connectivity combines overlap with the principle of cooperative synapse formation (??, a,  ??, a), additionally ?? (a) proposed a combination of overlap and targeting preferences. Our comparison to electron microscopy let us uncover the strength and nature of the targeting preferences shaping connectivity beyond neuronal and regional anatomy. We found that cooperative synapse formation explains some forms of apparent targeting. Additionally, we found that the distribution of postsynaptic compartments targeted by connections from somatostatin (Sst)-positive neurons is readily predicted from overlap only, while for parvalbumin (PV)-positive and vasoactive intestinal peptide (VIP)-positive neurons additional specificity plays a role. We found no indication of additional specificity for excitatory neurons. The model is available both with and without the characterized inhibitory specificity.


### Overview of the model building and analysis workflow. {#overview-of-the-model-building-and-analysis-workflow-dot}

Step 1
: Building was based on a volumetric atlas of the modeled regions: (1) S1J; (2) S1FL; (3) S1Tr; (4) S1HL; (5) S1Sh; (6) S1DZ; (7) S1DZO; (8) S1ULp. Additional atlases of biological cell densities and local orientation towards the surface were built.


Step 2
: Neuron morphologies were reconstructed and classified into 60 morphological types (_m-types_). They were placed in the volume according to the densities and orientations from step 1.


Step 3
: The anatomy of intrinsic synaptic connectivity was derived as the union of one algorithm for _local_ connectivity and one for _mid-range_ connectivity.


Step 4
: Extrinsic inputs from two thalamic sources were placed on modeled dendrites according to published methods.


Step 5
: Taken together, these steps allowed us to predict the topology of connectivity at scale with (sub-)cellular resolution.


Step 6
: The anatomical model served as the basis of a physiological model, ready to be simulated. This is presented in an accompanying manuscript.


Step 7
: The model, simulation and analysis tools have been made publicly available. Left: During modeling, three types of generalization had to be made to fulfill input data requirements: from mouse to rat, from adult to juvenile, and from one cortical region to another. Generalizations used are indicated in each step.


## Open Brain Institute {#open-brain-institute}

The Open Brain Institute, an outgrowbh is non-profit organization whose mission is to empower researchers and organizations with advanced digital brain building technology to perform neuroscience at the speed of thought.

**Markram's Radical Hypothesis**
Since every parameter in any complex system depends on every other parameter - in other words, any one piece is shaped by the others - then laying down one piece of the puzzle might start revealing the missing parts, and only a few landmark pieces might be needed to infer the entire map.

**Pioneering AI for Brain Knowledge**
The BBP built artificial intelligence search tools to automatically read the neuroscience literature and push the boundaries of knowledge engineering to register data in knowledge graphs and anchor it spatially in brain atlases - creating a unified and semi-self-updating library of the latest brain mappings. AI tools were also developed to extract parameters needed from the literature and in brain databases to feed algorithms developed to build digital brain models, creating a living continuously updating library of the latest neuroscience discoveries around the world.

**Overcoming the Accessibility Challenge**
The next seemingly insurmountable challenge that the project faced as it began finalizing the recipe was how to make the data and all the digital brain-building technologies accessible to any neuroscientist in the world. Amazon’s AWS came to the rescue, generously providing a freely available academic platform for anyone to access all of Blue Brain’s data as part of their Academic Sponsorship Program. The data is now publicly available in the AWS Open Data Registry, including millions of neuronal morphologies and electrical recordings of neurons, synapses, ion channels, brain models as well as simulation experiments and around 290 repositories were created on GitHub featuring the various software packages. The brain atlas environment also serves as a single point of entry to brain databases around the world.

Early on Markram started preparing the next generation neuroscientist for simulation neuroscience by developing a series of Massive On-line Courses (MOOCs) that have been taken by over 22’000 students to date.

**LLMs Simplify the Recipe**
Yet accessibility would still be a major challenge for even the most expert neuroscientist, because the recipe is made up of a huge number of values, equations, algorithms, processes, and workflows—all organized into a suite of software applications amounting to millions of lines of code—that would limit its dissemination. “A solution emerged. We are in the midst of an AI revolution where Large Language Models (LLMs) can capture all the world’s knowledge and serve it in any language, including the language of computers. So, we wrapped the applications in LLMs, giving them access to the recipe, simplifying interactions with the digital brain-building technologies,” says Jean-Denis Courcol, the Director of Engineering during the Blue Brain Project and now CTO of the OBI. “We are on a path that will make it possible for researchers to perform neuroscience at the speed of thought,” says Georges Khazen, one of the first of 45 PhD students of the Blue Brain Project, and now the CEO of OBI.

**A New Challenge**
The third new pillar of neuroscience besides experiments and theory: simulation neuroscience.
 “I feel like I can be a student all over again,” says Professor Idan Segev, a founding father of computational neuroscience and a board member of the OBI. “Turning electron-microscopic images of the brain into functional computational models is something even Ramón y Cajal, the founding father of neuroanatomy, could not have dreamed about,” says Professor Javier de Felipe, Founder of the Cajal Blue Brain initiative and board member of the OBI.


## Sub-Cellular Labs: Simulation Neuroscience for Molecular Processes {#sub-cellular-labs-simulation-neuroscience-for-molecular-processes}

The OBI will host and support labs across the levels of brain organization. Sub-cellular labs will allow modeling of the brain at the molecular level with detailed models for the brain’s metabolic system and for ion channel models prescribed by genes, paving the way to replicate neurons at the genetic level. “For the first time, we can build circuit models that incorporate blood flow and metabolic energy constraints. We also show how ion channels encoded by the genes expressed in each neuron come together to form the electrical behavior of the neuron.” says Dan Keller, in charge of supporting the Sub-Cellular Labs.


## Cellular Labs: Simulation Neuroscience for Single Neurons {#cellular-labs-simulation-neuroscience-for-single-neurons}

Cellular labs will allow simulation neuroscience on single neurons with all their incoming synapses—from any region of the mouse brain, selected regions of the rat brain, and all types of neurons in the human neocortex. “We have turned the Harvard-Google electron-microscopic images of the human neocortex into functional neuron models,” says Marwan Abdellah, a legend in the Blue Brain team for capturing the exquisite morphological detail of neurons and their supporting cells, the glia.


## Circuit Labs: Simulation Neuroscience for Brain Circuits of Neurons {#circuit-labs-simulation-neuroscience-for-brain-circuits-of-neurons}

The Circuit Lab allows users to call up and run any one of the many microcircuit models from various brain regions that were built by the Blue Brain, by the community, or from scratch. “Researchers can run an algorithm that computationally synthesizes, from a point in space, the full morphologies for any type of neuron and generate as many morphological variants as required to fill up a circuit with neurons,” explains Lida Kanari, who developed the breakthrough mathematical method and will continue supporting the Cellular Labs after joining Oxford University as a faculty member.


## Systems Lab: Brain Regions with Brain Wide Connections {#systems-lab-brain-regions-with-brain-wide-connections}

The Systems Lab allows users to select from a brain atlas as many brain regions as desired to form what we call a Brain System that can extend all the way to a whole brain. “We can now also synthesize not only the local axonal arborizations of neurons, but also the inter-regional axons connecting microcircuits to form a brain region—and even grow any neuron’s axons to span across the whole brain following major tracts connecting brain regions,” Kanari adds.


## Free Parameters {#free-parameters}

“Some physicists criticized that such models would never work like the real brain because of a potential explosion in the number of free parameters. But when the proper techniques are used, they are not free parameters, but biologically prescribed and with strong inter-dependencies. So, free parameters, so free parameters decrease exponentially the closer one follows biology. The Blue Brain has published many papers that show that model neurons and brain tissue constructed in this way closely mirror the behavior of real neurons and brain tissue, replicating what biologists observe in their experiments. And when it does not, it is not a failure—it is an exciting moment, a potential breakthrough because it means we are at the very frontier of our knowledge. It can point to what is missing or what is not understood properly, guiding the next breakthrough,” says Michael Reimann, Director of the Blue Brain Project’s Simulation Neuroscience division and Chief Science Officer of the OBI.

“We made a huge number of breakthroughs, published in several hundred papers, in this way. For example, this is how we found a key factor that switches the behavior of brain circuits from an awake-like state, into a sleep-like state with implications for our understanding of learning, we discovered how neuron connectivity shapes their collective behavior, how diversity of morphological and electrical properties makes the brain more resilient, and gained a deep insight into how a group of neurons processes information and more. When we recreated synaptic plasticity mechanisms in this way, we also found that it unified many theories and resolved many discrepancies in how synapses learn,” he added.


## An Invitation to Explore {#an-invitation-to-explore}


## Scratch {#scratch}
