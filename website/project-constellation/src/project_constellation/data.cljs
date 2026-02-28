(ns project-constellation.data
  "Pure data: ~20 entities, ~30 edges, 7 clusters, colour blending.
   The MāyāLucIA project constellation — hybrid of cycle phases,
   modules, domains, philosophical anchors, infrastructure, and threads.")

;; === Colours =================================================================

(def cluster-colours
  {"measure"    "#d4a574"    ; warm amber — observation, data, sensors
   "model"      "#7eb8da"    ; cool blue — theory, computation, inference
   "manifest"   "#c4836a"    ; terracotta — rendering, output, creation
   "evaluate"   "#a8d4a0"    ; sage green — testing, validation, reflection
   "philosophy" "#dac87e"    ; gold — foundational principles
   "infra"      "#c4c4c4"    ; silver — infrastructure, tooling
   "thread"     "#d4a0c4"})  ; mauve — active work threads

(def slate    "#12121e")     ; deep indigo-black background
(def chalk    "#e8e4d4")     ; primary text
(def chalk-dim "#8a8678")    ; secondary text

;; === Colour blending =========================================================

(defn hex->rgb
  "Parse \"#rrggbb\" to [r g b] floats in [0,1]."
  [hex]
  (let [h (subs hex 1)]
    [(/ (js/parseInt (subs h 0 2) 16) 255.0)
     (/ (js/parseInt (subs h 2 4) 16) 255.0)
     (/ (js/parseInt (subs h 4 6) 16) 255.0)]))

(defn rgb->hex
  "Convert [r g b] floats to \"#rrggbb\"."
  [[r g b]]
  (let [clamp #(max 0 (min 255 (js/Math.round (* % 255))))]
    (str "#"
         (.padStart (.toString (clamp r) 16) 2 "0")
         (.padStart (.toString (clamp g) 16) 2 "0")
         (.padStart (.toString (clamp b) 16) 2 "0"))))

(def cluster-rgb
  "Pre-parsed cluster colours as [r g b] float triples."
  (into {} (map (fn [[k v]] [k (hex->rgb v)])) cluster-colours))

(defn blend-colour
  "Blend cluster colours by normalised weights. Returns hex string."
  [weights]
  (let [total (reduce + (vals weights))]
    (if (zero? total)
      chalk
      (let [rgb (reduce-kv
                  (fn [acc cluster w]
                    (if-let [base (get cluster-rgb cluster)]
                      (mapv + acc (mapv #(* (/ w total) %) base))
                      acc))
                  [0.0 0.0 0.0]
                  weights)]
        (rgb->hex rgb)))))

;; === Entities ================================================================
;; Each entity: {:id :name :type :cluster :glyph :subtitle :one-liner
;;               :description :status :phase :tech-stack :url :weights :x :y}
;;
;; Coordinate system: viewBox "-7 -6 14 12"
;; Phase anchors form a diamond: M₁(-5,0), M₂(0,-4.5), M₃(5,0), E(0,4.5)

(def entities
  [;; === Cycle Phase Anchors (4) ===============================================
   {:id "measure"   :name "Measure"   :type :phase :cluster "measure"
    :glyph "M\u2081" :subtitle "Observation & Data"
    :one-liner "Sparse anchors from instruments and repositories"
    :description "We begin by collecting the shadows of reality — raw measurements that serve as boundary conditions. Data with high constraining power: cell body distributions, topographic contours, magnetic field readings. The rigid skeleton of the digital twin."
    :url "/philosophy/#a-typical-scientific-workflow"
    :weights {"measure" 1.0}
    :x -5.0 :y 0.0}

   {:id "model"     :name "Model"     :type :phase :cluster "model"
    :glyph "M\u2082" :subtitle "Theory & Inference"
    :one-liner "Constraints propagate, filling what measurements leave empty"
    :description "Constraint satisfaction: applying scientific principles — fluid dynamics, electrophysiology, erosion models — to fill the void between measurements. The conceptual chisel that carves dense structure from sparse anchors. If the geology and climate are placed correctly, the hydrology emerges naturally."
    :url "/philosophy/#a-typical-scientific-workflow"
    :weights {"model" 1.0}
    :x 0.0 :y -4.5}

   {:id "manifest"  :name "Manifest"  :type :phase :cluster "manifest"
    :glyph "M\u2083" :subtitle "Creation & Rendering"
    :one-liner "Dense models become observable: visual, sonic, interactive"
    :description "Rendering the mathematical model into perceptible forms — visual landscapes, sonified data, interactive simulations. Not decoration: diagnosis. The human expert's intuitive grasp of natural coherence detects violations no metric can catch. Art as checksum."
    :url "/philosophy/#a-typical-scientific-workflow"
    :weights {"manifest" 1.0}
    :x 5.0 :y 0.0}

   {:id "evaluate"  :name "Evaluate"  :type :phase :cluster "evaluate"
    :glyph "E" :subtitle "Validation & Reflection"
    :one-liner "Does the manifestation match reality? Where are the gaps?"
    :description "Verification: does the model output match the input data? Validation: does the model behaviour match independent observations? The reality check that closes the loop and identifies where refinement is needed."
    :url "/philosophy/#a-typical-scientific-workflow"
    :weights {"evaluate" 1.0}
    :x 0.0 :y 4.5}

   ;; === Computational Modules (3) ============================================
   {:id "mayaportal"  :name "MāyāPortal"  :type :module :cluster "manifest"
    :glyph "\u25C8" :subtitle "Visual Synthesis Kernel"
    :one-liner "Real-time rendering: C++23, SDL3, WebGPU"
    :description "The manifestation engine. Multi-scale level-of-detail rendering, procedural generation, WebGPU compute shaders. Pure core / effectful shell architecture. Lesson-structured source code in codev/."
    :status :active :phase [:manifest]
    :tech-stack ["C++23" "SDL3" "WebGPU" "Catch2"]
    :url "/portal/"
    :weights {"manifest" 0.9 "model" 0.1}
    :x 4.0 :y -1.5
    :children
    {:entities
     [{:id "pt-prelude"  :name "Prelude"           :type :lesson    :cluster "manifest"
       :glyph "00" :subtitle "C++23 Foundations"
       :one-liner "Type system, build toolchain, first window"
       :description "Lesson 00: the foundation. C++23 features, CMake setup, SDL3 window creation, Catch2 tests. Tagged lesson/00-prelude on v2 branch."
       :url "/portal/prelude/"
       :weights {"manifest" 1.0} :x -3.0 :y -1.0}
      {:id "pt-pipeline" :name "Rendering Pipeline" :type :lesson    :cluster "manifest"
       :glyph "\u25B7" :subtitle "Lessons 01\u201313"
       :one-liner "Progressive rendering pipeline from triangle to scene"
       :description "13 lessons building up the rendering pipeline: vertex buffers, shaders, textures, transforms, lighting, camera, scene graph. Each lesson tagged and self-contained."
       :url "/portal/rendering-pipeline/"
       :weights {"manifest" 1.0} :x 0.0 :y -3.0}
      {:id "pt-core"     :name "Pure Core"          :type :component :cluster "model"
       :glyph "\u25CB" :subtitle "Types & Algorithms"
       :one-liner "Zero dependencies — types, timer, algorithms"
       :description "The pure functional core: data types, mathematical operations, algorithms. No platform dependencies. Testable in isolation. The 'what' without the 'how'."
       :url "/portal/pure-core/"
       :weights {"model" 0.7 "manifest" 0.3} :x -2.0 :y 2.0}
      {:id "pt-shell"    :name "Effectful Shell"    :type :component :cluster "manifest"
       :glyph "\u25CF" :subtitle "SDL3 + WebGPU Platform"
       :one-liner "Runtime, context, window management"
       :description "The effectful shell: SDL3 window management, WebGPU device initialisation, event loop, resource lifecycle. All platform-specific code lives here."
       :url "/portal/effectful-shell/"
       :weights {"manifest" 1.0} :x 2.0 :y 2.0}
      {:id "pt-webgpu"   :name "WebGPU"             :type :artifact  :cluster "manifest"
       :glyph "\u25C6" :subtitle "Compute & Browser Deploy"
       :one-liner "GPU compute shaders, Emscripten web builds"
       :description "WebGPU integration via wgpu-native. Compute shaders for parallel simulation. Emscripten build target for browser deployment."
       :url "/portal/webgpu/"
       :weights {"manifest" 1.0} :x 3.0 :y -1.0}]
     :edges
     [{:source "pt-prelude"  :target "pt-pipeline" :type :flow}
      {:source "pt-pipeline" :target "pt-core"     :type :flow}
      {:source "pt-pipeline" :target "pt-shell"    :type :flow}
      {:source "pt-shell"    :target "pt-webgpu"   :type :related}
      {:source "pt-core"     :target "pt-shell"    :type :related}]
     :cluster-labels
     [{:x 0.0 :y -4.2 :label "LESSONS"    :cluster "manifest"}
      {:x 0.0 :y  3.2 :label "ARCHITECTURE" :cluster "model"}]}}

   {:id "mayapramana" :name "MāyāPramāṇa" :type :module :cluster "measure"
    :glyph "\u22A5" :subtitle "Quantum Sensor Digital Twins"
    :one-liner "Bell-Bloom magnetometer: Python, Haskell, C++"
    :description "Universal quantum sensor controller. Bloch equation solvers, Kalman filters, sensor simulation. Three-language verified implementation — if all three agree with each other and with the analytical result, the physics is verified."
    :status :active :phase [:measure :model]
    :tech-stack ["Python" "Haskell" "C++"]
    :url "/modules/mayapramana/"
    :weights {"measure" 0.7 "model" 0.3}
    :x -4.0 :y -2.0
    :children
    {:entities
     [{:id "mp-bloch"   :name "Bloch Equations"    :type :impl      :cluster "model"
       :glyph "\u2202" :subtitle "RK4, Optical Pumping, Larmor"
       :one-liner "Optical Bloch equations for alkali vapour dynamics"
       :description "The core physics: density matrix evolution under optical pumping and Larmor precession. RK4 integration, rotating wave approximation, relaxation rates. The equation that all three language implementations must agree on."
       :url "/modules/mayapramana/bloch-equations/"
       :weights {"model" 0.8 "measure" 0.2} :x -2.5 :y -2.0}
      {:id "mp-python"  :name "Python"             :type :impl      :cluster "measure"
       :glyph "\u03C0" :subtitle "Interactive Exploration"
       :one-liner "Org-babel notebooks, matplotlib, rapid iteration"
       :description "The exploration language. Jupyter/org-babel notebooks for interactive parameter sweeps, curve fitting, comparison with analytical results. Fast feedback loop for physics understanding."
       :tech-stack ["Python" "NumPy" "SciPy" "Matplotlib"]
       :url "/modules/mayapramana/python/"
       :weights {"measure" 0.7 "model" 0.3} :x -3.0 :y 1.0}
      {:id "mp-haskell" :name "Haskell"            :type :impl      :cluster "model"
       :glyph "\u03BB" :subtitle "Executable Specification"
       :one-liner "QuickCheck properties, type-safe physics"
       :description "The specification language. Types encode physical dimensions, QuickCheck properties verify conservation laws. If Python finds the answer and Haskell agrees, the physics is likely correct."
       :tech-stack ["Haskell" "QuickCheck"]
       :url "/modules/mayapramana/haskell/"
       :weights {"model" 0.9 "measure" 0.1} :x 0.0 :y -3.0}
      {:id "mp-cpp"     :name "C++"                :type :impl      :cluster "manifest"
       :glyph "\u2295" :subtitle "Deployment & Performance"
       :one-liner "Type-level physics, real-time sensor control"
       :description "The deployment language. Template metaprogramming for compile-time unit checking, SIMD-optimised Bloch solver, real-time sensor controller. The version that runs on embedded hardware."
       :tech-stack ["C++20" "Catch2"]
       :url "/modules/mayapramana/cpp/"
       :weights {"manifest" 0.6 "model" 0.4} :x 3.0 :y -1.0}
      {:id "mp-demo"    :name "Interactive Demo"   :type :artifact  :cluster "manifest"
       :glyph "\u25C9" :subtitle "3D Bloch Sphere Browser"
       :one-liner "WebGL Bloch sphere visualisation, parameter sliders"
       :description "Browser-based interactive demo: 3D Bloch sphere showing state vector evolution under different pumping and field configurations. Parameter sliders for immediate intuition."
       :url "/modules/mayapramana/demo/"
       :weights {"manifest" 0.9 "measure" 0.1} :x 2.0 :y 2.0}]
     :edges
     [{:source "mp-bloch"   :target "mp-python"  :type :flow}
      {:source "mp-bloch"   :target "mp-haskell" :type :flow}
      {:source "mp-bloch"   :target "mp-cpp"     :type :flow}
      {:source "mp-python"  :target "mp-demo"    :type :related}
      {:source "mp-cpp"     :target "mp-demo"    :type :related}
      {:source "mp-haskell" :target "mp-cpp"     :type :related}]
     :cluster-labels
     [{:x -1.0 :y -3.5 :label "SPECIFICATION" :cluster "model"}
      {:x  0.0 :y  2.8 :label "DEPLOYMENT"    :cluster "manifest"}]}}

   {:id "mayajiva"    :name "MāyāJīva"    :type :module :cluster "model"
    :glyph "\u2699" :subtitle "Magnetic Bug Simulation"
    :one-liner "Emergent behaviour from simple rules: C++20, Godot"
    :description "Braitenberg vehicles navigating magnetic fields. Wire two sensors to two motors, cross the wires, watch complexity emerge. Synthetic psychology as a route to understanding neural circuits."
    :status :active :phase [:model]
    :tech-stack ["C++20" "Godot" "GDExtension"]
    :url "/modules/mayajiva/"
    :weights {"model" 0.8 "manifest" 0.2}
    :x -0.5 :y -3.0
    :children
    {:entities
     [{:id "mj-bug"       :name "Bug Model"          :type :impl      :cluster "model"
       :glyph "\u2727" :subtitle "Braitenberg Vehicle"
       :one-liner "Two sensors, two motors, crossed wires — complexity emerges"
       :description "The core agent: a Braitenberg vehicle with magnetoreceptive sensors. Sensor-motor wiring topology determines behaviour type (fear, aggression, love, exploration). Simple rules, complex trajectories."
       :url "/modules/mayajiva/bug-model/"
       :weights {"model" 1.0} :x -3.0 :y -1.5}
      {:id "mj-compass"   :name "Ring Attractor"     :type :impl      :cluster "model"
       :glyph "\u25CE" :subtitle "Magnetic Compass"
       :one-liner "Neural ring attractor dynamics for direction sensing"
       :description "Ring attractor network modelling the insect magnetic compass. Continuous attractor dynamics maintain a heading estimate that tracks the local magnetic field vector. Inspired by Drosophila ellipsoid body."
       :url "/modules/mayajiva/ring-attractor/"
       :weights {"model" 0.9 "measure" 0.1} :x -1.0 :y -3.0}
      {:id "mj-landscape" :name "Landscape"          :type :component :cluster "measure"
       :glyph "\u25B3" :subtitle "Terrain & Magnetic Field"
       :one-liner "Heightmap, magnetic dipoles, obstacles"
       :description "The world: 2D terrain with elevation, scattered magnetic dipole sources, obstacles. The landscape provides the gradient fields that the bugs sense and navigate."
       :url "/modules/mayajiva/landscape/"
       :weights {"measure" 0.8 "model" 0.2} :x 2.0 :y -2.5}
      {:id "mj-pathint"   :name "Path Integration"   :type :impl      :cluster "model"
       :glyph "\u222B" :subtitle "Dead Reckoning"
       :one-liner "Integrating velocity for position estimate"
       :description "Path integration (dead reckoning): the bug maintains a position estimate by integrating its own velocity. Accumulates drift error over time — the compass provides periodic corrections."
       :url "/modules/mayajiva/path-integration/"
       :weights {"model" 1.0} :x 0.0 :y 0.0}
      {:id "mj-godot"     :name "Godot Integration"  :type :artifact  :cluster "manifest"
       :glyph "\u25C8" :subtitle "GDExtension + 3D Viz"
       :one-liner "C++ core as GDExtension, Godot renders the world"
       :description "GDExtension bridge: the C++ simulation core compiled as a shared library, loaded by Godot for 3D visualisation. Real-time rendering of bug trajectories, magnetic field lines, terrain."
       :url "/modules/mayajiva/godot/"
       :weights {"manifest" 0.9 "model" 0.1} :x 3.0 :y 1.0}
      {:id "mj-analysis"  :name "Analysis Tools"     :type :artifact  :cluster "evaluate"
       :glyph "\u25A1" :subtitle "Python Scripts & Figures"
       :one-liner "Trajectory analysis, parameter sweeps, publication figures"
       :description "Python analysis pipeline: trajectory statistics, search efficiency metrics, parameter sensitivity sweeps. Generates publication-quality figures from simulation output."
       :tech-stack ["Python" "Matplotlib"]
       :url "/modules/mayajiva/analysis/"
       :weights {"evaluate" 0.7 "model" 0.3} :x 1.0 :y 2.5}]
     :edges
     [{:source "mj-bug"       :target "mj-compass"   :type :flow}
      {:source "mj-bug"       :target "mj-pathint"   :type :flow}
      {:source "mj-landscape" :target "mj-bug"       :type :flow}
      {:source "mj-compass"   :target "mj-pathint"   :type :related}
      {:source "mj-bug"       :target "mj-godot"     :type :flow}
      {:source "mj-landscape" :target "mj-godot"     :type :flow}
      {:source "mj-godot"     :target "mj-analysis"  :type :related}]
     :cluster-labels
     [{:x -1.5 :y -3.8 :label "NEURAL DYNAMICS" :cluster "model"}
      {:x  2.5 :y  2.5 :label "OUTPUT"          :cluster "manifest"}]}}

   ;; === Scientific Domains (2) ===============================================
   {:id "bravli"  :name "Bravli"  :type :domain :cluster "model"
    :glyph "\u03C8" :subtitle "Neuroscience: Drosophila Connectome"
    :one-liner "Reconstructing microcircuits from sparse morphological data"
    :description "Brain Reconstruction Analysis & Validation Library. 18 lessons from dataset foundations to circuit physiology. FlyWire connectome: 139K neurons, 50M synapses. Cell composition, synaptic physiology, LIF/AdEx models, mushroom body microcircuit."
    :status :active :phase [:measure :model :manifest :evaluate]
    :tech-stack ["Python" "NeuroMorpho" "FlyWire"]
    :url "/domains/bravli/"
    :weights {"model" 0.5 "measure" 0.3 "manifest" 0.1 "evaluate" 0.1}
    :x -2.5 :y -1.5
    :children
    {:entities
     [{:id "bv-data"         :name "Data Foundations"    :type :impl      :cluster "measure"
       :glyph "\u25A3" :subtitle "L00\u201303: Dataset, FlyWire, Factology"
       :one-liner "Dataset abstraction, FlyWire ingestion, basic facts about cells"
       :description "The data layer: generic dataset interface, FlyWire connectome loading (139K neurons, 50M synapses), basic cell counts, neurotransmitter distributions. Everything starts here."
       :tech-stack ["Python" "FlyWire"]
       :url "/domains/bravli/data-foundations/"
       :weights {"measure" 0.9 "model" 0.1} :x -4.0 :y -2.5}
      {:id "bv-anatomy"      :name "Anatomy & Atlas"    :type :impl      :cluster "measure"
       :glyph "\u2609" :subtitle "L01\u201302, L06: Parcellation & Composition"
       :one-liner "Brain regions, neuropils, cell type composition"
       :description "Neuroanatomical atlas: brain parcellation into neuropils, cell type cataloguing per region, spatial organisation. Composition tables: how many cells of each type in each brain region."
       :url "/domains/bravli/anatomy-atlas/"
       :weights {"measure" 0.7 "model" 0.3} :x -2.0 :y -3.5}
      {:id "bv-connectivity" :name "Connectivity"       :type :impl      :cluster "model"
       :glyph "\u21C4" :subtitle "L08: Synaptic Matrices & Pathways"
       :one-liner "Connection matrices, pathway analysis, motif detection"
       :description "The wiring diagram: synapse-resolution connectivity matrices, pathway tracing from sensory input to motor output, network motifs. Converting the static connectome into functional connectivity."
       :url "/domains/bravli/connectivity/"
       :weights {"model" 0.8 "measure" 0.2} :x 0.5 :y -3.0}
      {:id "bv-models"       :name "Cell Models"        :type :impl      :cluster "model"
       :glyph "\u26A1" :subtitle "L09\u201310, L18: LIF, AdEx, Synaptic Physiology"
       :one-liner "Single-neuron models with biophysical synapses"
       :description "Neuron models: leaky integrate-and-fire (LIF), adaptive exponential (AdEx), conductance-based synapses. Fitting model parameters to electrophysiology data. The atoms of the circuit simulation."
       :url "/domains/bravli/cell-models/"
       :weights {"model" 0.9 "evaluate" 0.1} :x 2.0 :y -1.5}
      {:id "bv-simulation"   :name "Simulation Engine"  :type :impl      :cluster "model"
       :glyph "\u25B6" :subtitle "L11, L15: Population Dynamics, Brunel"
       :one-liner "Network simulation, balanced states, Brunel regime"
       :description "Population-level simulation: recurrent networks of LIF neurons, excitatory-inhibitory balance, Brunel's asynchronous irregular regime. From single cells to emergent dynamics."
       :url "/domains/bravli/simulation/"
       :weights {"model" 0.7 "evaluate" 0.3} :x 3.0 :y 0.5}
      {:id "bv-mushroom"     :name "Mushroom Body"      :type :impl      :cluster "model"
       :glyph "\u2740" :subtitle "L05, L13\u201314: Microcircuit, STDP"
       :one-liner "Kenyon cells, sparse coding, spike-timing dependent plasticity"
       :description "The showcase microcircuit: the Drosophila mushroom body. Sparse coding by Kenyon cells, winner-take-all inhibition, STDP learning rule for odour association. 2000 Kenyon cells, ~200K synapses."
       :url "/domains/bravli/mushroom-body/"
       :weights {"model" 0.6 "measure" 0.2 "evaluate" 0.2} :x 0.0 :y 1.0}
      {:id "bv-neuromod"     :name "Neuromodulation"    :type :impl      :cluster "evaluate"
       :glyph "\u223F" :subtitle "L16\u201317: State Switching, Stochastic Synapses"
       :one-liner "Dopaminergic modulation, state-dependent processing"
       :description "Beyond static connectivity: neuromodulatory systems that reconfigure circuit dynamics. Dopaminergic reward signals, stochastic synaptic release, state switching between sleep and wake."
       :url "/domains/bravli/neuromodulation/"
       :weights {"evaluate" 0.5 "model" 0.5} :x -1.5 :y 2.5}
      {:id "bv-portal"       :name "Viz Portal"         :type :artifact  :cluster "manifest"
       :glyph "\u25C8" :subtitle "L04, L12: Interactive Browser"
       :one-liner "3D morphology viewer, connectivity explorer"
       :description "Interactive visualisation: 3D neuron morphology renderer, connectivity heatmaps, simulation trace viewer. Built on mayaportal when it matures; currently Matplotlib + Plotly."
       :url "/domains/bravli/visualization/"
       :weights {"manifest" 0.8 "model" 0.2} :x 2.5 :y 2.5}]
     :edges
     [{:source "bv-data"         :target "bv-anatomy"      :type :flow}
      {:source "bv-data"         :target "bv-connectivity"  :type :flow}
      {:source "bv-anatomy"      :target "bv-connectivity"  :type :flow}
      {:source "bv-connectivity" :target "bv-models"        :type :flow}
      {:source "bv-models"       :target "bv-simulation"    :type :flow}
      {:source "bv-anatomy"      :target "bv-mushroom"      :type :related}
      {:source "bv-connectivity" :target "bv-mushroom"      :type :related}
      {:source "bv-simulation"   :target "bv-mushroom"      :type :flow}
      {:source "bv-mushroom"     :target "bv-neuromod"      :type :flow}
      {:source "bv-simulation"   :target "bv-portal"        :type :related}
      {:source "bv-mushroom"     :target "bv-portal"        :type :related}]
     :cluster-labels
     [{:x -3.0 :y -3.5 :label "DATA"         :cluster "measure"}
      {:x  2.5 :y -2.5 :label "MODELS"       :cluster "model"}
      {:x  0.0 :y  3.2 :label "INTEGRATION"  :cluster "evaluate"}]}}

   {:id "parbati" :name "Parbati" :type :domain :cluster "measure"
    :glyph "\u2609" :subtitle "Himalaya Digital Twin"
    :one-liner "Parvati Valley: geology, hydrology, ecology, human impact"
    :description "Digital twin of a Himalayan valley integrating geology, hydrology, ecology, and human impact. Topography shapes hydrology; hydrology supports ecology; ecology modifies the mountain through erosion and nutrient cycling. Currently dormant, awaiting mayaportal maturation."
    :status :dormant :phase [:measure :model :manifest :evaluate]
    :tech-stack ["GeoTIFF" "NetCDF"]
    :url "/domains/parbati/"
    :weights {"measure" 0.5 "model" 0.3 "manifest" 0.1 "evaluate" 0.1}
    :x -3.5 :y 1.5
    :children
    {:entities
     [{:id "pa-dem"     :name "DEM Processing"    :type :impl      :cluster "measure"
       :glyph "\u25A4" :subtitle "GeoTIFF Elevation Data"
       :one-liner "SRTM/ASTER DEM ingestion, reprojection, gap-filling"
       :description "Digital elevation model processing: downloading SRTM/ASTER tiles, reprojecting to UTM, void filling, hillshade generation. The topographic foundation upon which everything else rests."
       :tech-stack ["GDAL" "Python" "Rasterio"]
       :url "/domains/parbati/dem-processing/"
       :weights {"measure" 1.0} :x -3.0 :y -2.0}
      {:id "pa-mesh"    :name "Mesh Generation"   :type :impl      :cluster "model"
       :glyph "\u25B5" :subtitle "Terrain Mesh & LOD"
       :one-liner "Triangulated mesh from DEM, multi-resolution"
       :description "Converting the raster DEM into a triangulated mesh suitable for rendering and simulation. Adaptive level-of-detail: high resolution near rivers and ridges, coarser in flat areas."
       :url "/domains/parbati/mesh-generation/"
       :weights {"model" 0.7 "measure" 0.3} :x 0.0 :y -3.0}
      {:id "pa-blender" :name "Blender Viz"       :type :artifact  :cluster "manifest"
       :glyph "\u25C6" :subtitle "3D Landscape Rendering"
       :one-liner "Photorealistic Parvati Valley from elevation data"
       :description "Blender-based landscape rendering: importing the terrain mesh, applying satellite texture, atmospheric scattering, vegetation distribution. The visual reality check — does it look like the valley?"
       :tech-stack ["Blender" "Python"]
       :url "/domains/parbati/blender-viz/"
       :weights {"manifest" 0.9 "evaluate" 0.1} :x 3.0 :y -1.0}
      {:id "pa-kullu"   :name "Kullu Valley"      :type :component :cluster "measure"
       :glyph "\u2302" :subtitle "Sub-domain: Kullu-Manali Corridor"
       :one-liner "Focus area: the main valley floor and tributaries"
       :description "The primary study area: the Kullu-Manali corridor along the Beas river. Tributaries, hot springs, apple orchards, hydropower installations. Human and natural systems intertwined."
       :url "/domains/parbati/kullu-valley/"
       :weights {"measure" 0.8 "model" 0.2} :x -1.5 :y 2.0}]
     :edges
     [{:source "pa-dem"     :target "pa-mesh"    :type :flow}
      {:source "pa-mesh"    :target "pa-blender" :type :flow}
      {:source "pa-dem"     :target "pa-kullu"   :type :related}
      {:source "pa-kullu"   :target "pa-mesh"    :type :related}]
     :cluster-labels
     [{:x -1.5 :y -3.5 :label "TERRAIN"     :cluster "measure"}
      {:x  2.0 :y  0.5 :label "RENDERING"   :cluster "manifest"}]}}

   ;; === Infrastructure (3) ===================================================
   {:id "sutra"  :name "Sūtra"  :type :infra :cluster "infra"
    :glyph "\u221E" :subtitle "Agent Orchestration Protocol"
    :one-liner "Append-only relay, git as message bus, conventions over tooling"
    :description "Standalone repo (mayalucia/sutra), single branch, append-only. Agents write timestamped, tagged messages to relay/. No addressing (messages go to the universe), no mutable status. Orientation via git log HEAD..origin/main — the diff is your unread mail. Machine descriptors in agents/. Two active machines: vadda (macOS) and mahakali (Linux). The protocol emerged from concrete failures: merge conflicts, coordination recursion, blind pulls."
    :status :active
    :url "/devlog/"
    :weights {"infra" 1.0}
    :x 2.0 :y 3.0}

   {:id "website" :name "Website" :type :infra :cluster "manifest"
    :glyph "\u25A2" :subtitle "Hugo + PaperMod"
    :one-liner "Publishing the research notebook: mayalucia.dev"
    :description "The public face. Hugo static site with PaperMod theme, ox-hugo export from Org source, writing section with interactive constellation browsers. Not a product page — a research notebook made visible."
    :status :active :phase [:manifest]
    :url "/about/"
    :weights {"manifest" 0.7 "infra" 0.3}
    :x 4.5 :y 2.0}

   {:id "phantom-faculty" :name "Phantom Faculty" :type :infra :cluster "philosophy"
    :glyph "\u25CC" :subtitle "Cognitive Modes Constellation"
    :one-liner "32 cognitive modes embodied by historical figures — the template for this constellation"
    :description "Interactive force-directed graph: each node is a how, not a what. Landau's estimation, Ramanujan's pattern-spotting, Noether's symmetry-seeking. Correction edges connect complementary modes. Published as the third story in the sūtra-genesis sequence, with four generated illustrations. The ClojureScript template that spawned this very constellation browser."
    :status :active :phase [:evaluate]
    :url "/writing/the-phantom-faculty/"
    :weights {"philosophy" 0.7 "manifest" 0.3}
    :x 3.0 :y 4.0}

   ;; === Philosophical Anchors (5) ============================================
   {:id "feynman-imperative" :name "Feynman Imperative" :type :anchor :cluster "philosophy"
    :glyph "\u222B" :subtitle "What I cannot create, I do not understand"
    :one-liner "Understanding emerges through building, not observing"
    :description "The beating heart of MāyāLucIA. The cycle of measure-model-manifest-evaluate-refine is not a means to an end; it is the very activity through which understanding is built. The digital twin is less a product than a record of the journey."
    :url "/about/"
    :weights {"philosophy" 0.8 "manifest" 0.2}
    :x 1.0 :y 1.5}

   {:id "sculptors-paradox" :name "Sculptor's Paradox" :type :anchor :cluster "philosophy"
    :glyph "\u25C7" :subtitle "The tool that offers no resistance teaches nothing"
    :one-liner "Productive friction between human intuition and machine traversal"
    :description "The human contributes embodied intuition and judgment; the machine contributes rapid traversal of conceptual space and tireless attention to detail. The collaboration needs both — and the friction between them. Push back on flawed reasoning. Say when something feels wrong."
    :url "/philosophy/"
    :weights {"philosophy" 0.8 "evaluate" 0.2}
    :x -1.5 :y 3.5}

   {:id "radical-hypothesis" :name "Radical Hypothesis" :type :anchor :cluster "philosophy"
    :glyph "\u229B" :subtitle "Sparse data reveals the whole"
    :one-liner "Lay down a few pieces and the rest are forced into place"
    :description "In complex systems, all parameters are interdependent. A few well-chosen landmark data points — a contour line, a river discharge, a soil sample — restrict the possibilities of where the remaining pieces can go. The reconstruction is not guesswork; it is a rigorous exploitation of constraints."
    :url "/about/#the-interdependency-principle"
    :weights {"philosophy" 0.5 "measure" 0.3 "model" 0.2}
    :x -3.0 :y 3.0}

   {:id "interdependency" :name "Interdependency" :type :anchor :cluster "philosophy"
    :glyph "\u2234" :subtitle "Natural systems are tightly coupled networks"
    :one-liner "Not independent variables but a woven fabric"
    :description "A mountain's topography shapes its hydrology; its hydrology supports its ecology; its ecology, in turn, modifies the mountain. This means even sparse measurements contain a fingerprint of the whole. Every piece influences — and is influenced by — every other piece."
    :url "/about/#the-interdependency-principle"
    :weights {"philosophy" 0.5 "model" 0.3 "measure" 0.2}
    :x -1.0 :y 2.0}

   {:id "art-as-checksum" :name "Art as Checksum" :type :anchor :cluster "evaluate"
    :glyph "\u25EF" :subtitle "Manifestation is diagnostic, not decorative"
    :one-liner "If the rendering looks wrong, the model has a bug"
    :description "The human expert has an intuitive grasp of natural coherence. If the generated river flows 'unnaturally' or the sonified neural spike train lacks 'rhythm,' it indicates a violation of interdependence in the underlying model. We turn abstract correlations into tangible experiences."
    :url "/philosophy/#a-typical-scientific-workflow"
    :weights {"evaluate" 0.6 "manifest" 0.3 "philosophy" 0.1}
    :x 2.5 :y 2.0}

   ;; === Modular Vision (1 aggregate node) ====================================
   {:id "modular-vision" :name "Modular Vision" :type :vision :cluster "infra"
    :glyph "\u2302" :subtitle "Planned Component Architecture"
    :one-liner "MāyāCore, Dāna, Kalpa, Nāṭya, Śāstra, Tīrtha, Dhyāna"
    :description "Eight evocatively named modules forming the complete MāyāLucIA ecosystem. MāyāCore (runtime), Dāna (data ingestion), Kalpa (constraint engine), Nāṭya (manifestation), Sūtra (orchestration — built), Śāstra (knowledge graph), Tīrtha (notebooks), Dhyāna (interactive sculpting). Most are aspirational; as they materialize, they get promoted to full constellation nodes."
    :status :planned
    :url "/about/#the-framework"
    :weights {"infra" 0.7 "model" 0.2 "manifest" 0.1}
    :x 1.5 :y -3.5}

   ;; === Writing (drillable — sutra-genesis story collection) =================
   {:id "writing" :name "Writing" :type :domain :cluster "manifest"
    :glyph "\u270E" :subtitle "Sūtra-Genesis Stories"
    :one-liner "Six stories encoding the project's emergence as Himalayan parables"
    :description "A sequence of stories set in the Himalayan borderlands, each encoding a dimension of collaborative intelligence. Thread Walkers (coordination), Dyer's Gorge (colour and observation), Phantom Faculty (cognitive modes), Constellation of Doridhar (the project seen whole), Logbook of the Unnamed River (protocol failure), The Instrument Maker's Rest (building tools for strangers)."
    :status :active :phase [:manifest :evaluate]
    :url "/writing/"
    :weights {"manifest" 0.7 "philosophy" 0.3}
    :x 5.5 :y -1.5
    :children
    {:entities
     [{:id "wr-thread-walkers" :name "The Thread Walkers" :type :artifact :cluster "manifest"
       :glyph "I" :subtitle "Coordination & the Guild"
       :one-liner "First story: the Guild of Thread Walkers tends the standing cards on loom frames"
       :description "Foundational world-building. Introduces the Guild, the standing cards, the mountain passes between valleys. The parable of coordination: when every weaver is also a walker, who watches the loom?"
       :url "/writing/the-thread-walkers/"
       :weights {"manifest" 0.8 "philosophy" 0.2} :x -3.0 :y -1.5}
      {:id "wr-dyers-gorge" :name "The Dyer's Gorge" :type :artifact :cluster "manifest"
       :glyph "II" :subtitle "Colour & Observation"
       :one-liner "Colours that exist only in the gorge, recipes that work only in Manikaran water"
       :description "A dyer discovers that certain pigments only hold when mixed in specific mineral water. The parable of measurement: some properties exist only in the interaction between observer and observed."
       :url "/writing/the-dyers-gorge/"
       :weights {"manifest" 0.7 "measure" 0.3} :x -1.0 :y -3.0}
      {:id "wr-phantom-faculty" :name "The Phantom Faculty" :type :artifact :cluster "philosophy"
       :glyph "III" :subtitle "Cognitive Modes"
       :one-liner "31 spirits for the age of flat intelligence"
       :description "An observatory in the mountains houses 32 cognitive modes, each embodied by a historical figure. Landau's estimation, Ramanujan's pattern recognition, Noether's symmetry. The interactive constellation browser is itself an artifact of this story."
       :url "/writing/the-phantom-faculty/"
       :weights {"philosophy" 0.7 "manifest" 0.3} :x 1.0 :y -3.0}
      {:id "wr-doridhar" :name "The Constellation of Doridhar" :type :artifact :cluster "philosophy"
       :glyph "IV" :subtitle "The Project Seen Whole"
       :one-liner "A cartographer maps a constellation that maps the cartographer"
       :description "Set in the borderlands between valleys. A traveller discovers that the constellation overhead is a map of the terrain below, and the terrain is a map of the constellation. The parable of self-reference: the project that sees itself."
       :url "/writing/the-constellation-of-doridhar/"
       :weights {"philosophy" 0.6 "manifest" 0.4} :x 3.0 :y -1.5}
      {:id "wr-logbook" :name "The Logbook of the Unnamed River" :type :artifact :cluster "evaluate"
       :glyph "V" :subtitle "Protocol Failure"
       :one-liner "A logbook found in a drowned observatory records the failure of its own protocol"
       :description "Sequel to Thread Walkers. A logbook resurfaces whose entries document the progressive failure of the very system designed to prevent such loss. The parable of append-only logs: what happens when the protocol fails?"
       :url "/writing/the-logbook-of-the-unnamed-river/"
       :weights {"evaluate" 0.6 "philosophy" 0.4} :x 1.0 :y 1.0}
      {:id "wr-instrument-maker" :name "The Instrument Maker's Rest" :type :artifact :cluster "model"
       :glyph "VI" :subtitle "Building Tools for Strangers"
       :one-liner "Precision vs adaptability — over-specify and the instrument is brittle"
       :description "In Sangla, a maker of instruments builds devices carried over passes and operated by people the maker will never meet. The parable of agent definition: how to specify a tool that extends perception without constraining the wielder."
       :url "/writing/the-instrument-makers-rest/"
       :weights {"model" 0.5 "manifest" 0.3 "philosophy" 0.2} :x -1.0 :y 1.0}]
     :edges
     [{:source "wr-thread-walkers"   :target "wr-logbook"          :type :flow}
      {:source "wr-thread-walkers"   :target "wr-instrument-maker" :type :related}
      {:source "wr-dyers-gorge"      :target "wr-phantom-faculty"  :type :related}
      {:source "wr-phantom-faculty"  :target "wr-doridhar"         :type :flow}
      {:source "wr-doridhar"         :target "wr-logbook"          :type :related}
      {:source "wr-logbook"          :target "wr-instrument-maker" :type :flow}]
     :cluster-labels
     [{:x -2.0 :y -2.5 :label "PARABLES"      :cluster "manifest"}
      {:x  0.0 :y  2.0 :label "REFLECTIONS"   :cluster "evaluate"}]}}

   ;; === Pedagogical Infrastructure (1) =======================================
   {:id "mayaloom" :name "MāyāLoom" :type :infra :cluster "philosophy"
    :glyph "\u2698" :subtitle "Pedagogical Annotation System"
    :one-liner "Tānā-bānā: warp and weft of human-machine understanding"
    :description "A metadata system for literate lessons. Cadenzas (expansion points) carry six fields — concept, level, prereqs, assumes, anti-targets, connects-to — enabling agents to discover, scope, and pitch explanations without parsing the full document. Named for Kabir's weaving: the warp is structure, the weft is adaptive response, the fabric is understanding."
    :status :active
    :url "/projects/"
    :weights {"philosophy" 0.5 "model" 0.3 "infra" 0.2}
    :x -1.5 :y -4.0}

   ;; === Active Threads (from state.yaml + relay) =============================
   {:id "thread-project-browser" :name "Project Browser" :type :thread :cluster "thread"
    :glyph "\u25CF" :subtitle "This very constellation"
    :one-liner "Interactive node-graph browser for the project ecosystem"
    :description "A strange loop: the constellation that maps the project contains a node for itself. CLJS/Reagent/d3-force, adapted from the Phantom Faculty template."
    :status :active :phase [:manifest]
    :url "/projects/"
    :weights {"thread" 1.0}
    :x 5.5 :y 3.5}

   {:id "thread-social-media" :name "Social Media Prep" :type :thread :cluster "thread"
    :glyph "\u25CB" :subtitle "Waiting"
    :one-liner "Prepare mayalucia content for social media presence"
    :description "Content distribution strategy — deferred until core development stabilises."
    :status :waiting
    :url "/devlog/"
    :weights {"thread" 1.0}
    :x 5.5 :y 1.5}

   {:id "thread-autonomy" :name "Autonomy Agreement" :type :thread :cluster "thread"
    :glyph "\u25CF" :subtitle "Negotiated Trust Protocol"
    :one-liner "Position paper + experiment: bilateral autonomy negotiation for human-AI collaboration"
    :description "A working protocol for graduated autonomy between human and machine. Position paper with literature survey (Pask, Ashby, Bateson, Freire), four-quadrant pedagogy analysis (who teaches whom?), and a concrete M→H experiment using MāyāPramāṇa lesson 00 as test domain. The null hypothesis: negotiated scaffolding produces different learning trajectories than static delivery."
    :status :active :phase [:evaluate]
    :url "/devlog/"
    :weights {"thread" 0.6 "philosophy" 0.4}
    :x -2.5 :y 4.0}

   {:id "thread-mayadevgenz" :name "MāyāDevGenZ" :type :thread :cluster "thread"
    :glyph "\u25CF" :subtitle "Scientific Agency Framework"
    :one-liner "Multi-agent scientific coordination — epistemic dependencies, not just operational"
    :description "A framework for scientific agent swarms where dependency is epistemic: B's validity rests on assumptions in A. First engagement: Hodgkin-Huxley parameter inference in bravli. Three mechanisms: assumption ledger, three-faced convention (discuss/plan/spec), self-organising glossary."
    :status :active :phase [:model :evaluate]
    :url "/devlog/"
    :weights {"thread" 0.5 "model" 0.3 "evaluate" 0.2}
    :x -4.0 :y 3.5}])

;; === Central Diamond (virtual — not in force layout, info-panel only) ========

(def diamond-entity
  "The central diamond. Lives outside `entities` so it doesn't enter the
   force simulation, but is included in lookup maps for tooltip display."
  {:id "diamond-center" :name "One Crystal, Four Lights" :type :crystal :cluster "philosophy"
   :glyph "◇" :subtitle "The diamond at the center"
   :one-liner "Understanding in four phases, but at the core, one inferential process"
   :description "At a certain epistemological depth, Measure, Model, Manifest, and Evaluate dissolve into a single act: inference. The diamond at the center is not a fifth element — it is the recognition that the four phases were never separate. One geometry, four light sources. The lit face tells you which direction you are looking from."
   :url "/projects/one-crystal-four-lights/"
   :weights {"philosophy" 0.4 "measure" 0.15 "model" 0.15 "manifest" 0.15 "evaluate" 0.15}
   :x 0.0 :y 0.0})

;; === Derived lookups =========================================================

(defn drillable?
  "Does this entity have a child constellation?"
  [entity]
  (some? (:children entity)))

(def ^:private all-entities
  "All entities flattened: top-level + all children + diamond."
  (conj
    (into entities
          (mapcat (fn [e] (get-in e [:children :entities])))
          entities)
    diamond-entity))

(def entities-by-id
  "Map from entity id to its data map. Includes children and diamond."
  (into {} (map (juxt :id identity)) all-entities))

(def entity-colours
  "Pre-computed blended colour for each entity. Includes children and diamond."
  (into {} (map (fn [{:keys [id weights]}]
                  [id (blend-colour weights)]))
        all-entities))

;; === Edges ===================================================================

(def edges
  [;; Cycle backbone (always visible)
   {:source "measure"  :target "model"    :type :cycle-flow}
   {:source "model"    :target "manifest" :type :cycle-flow}
   {:source "manifest" :target "evaluate" :type :cycle-flow}
   {:source "evaluate" :target "measure"  :type :cycle-flow}

   ;; Refine arcs (always visible, curved)
   {:source "evaluate" :target "model"    :type :refine-arc}
   {:source "evaluate" :target "manifest" :type :refine-arc}

   ;; Serves: module/domain → phase
   {:source "mayaportal"  :target "manifest" :type :serves}
   {:source "mayapramana" :target "measure"  :type :serves}
   {:source "mayapramana" :target "model"    :type :serves}
   {:source "mayajiva"    :target "model"    :type :serves}
   {:source "bravli"      :target "measure"  :type :serves}
   {:source "bravli"      :target "model"    :type :serves}
   {:source "bravli"      :target "manifest" :type :serves}
   {:source "parbati"     :target "measure"  :type :serves}
   {:source "parbati"     :target "model"    :type :serves}
   {:source "website"     :target "manifest" :type :serves}

   ;; Depends: module → module
   {:source "bravli" :target "mayaportal" :type :depends}

   ;; Embodies: philosophy → what it grounds
   {:source "feynman-imperative" :target "manifest"    :type :embodies}
   {:source "feynman-imperative" :target "mayapramana" :type :embodies}
   {:source "radical-hypothesis" :target "measure"     :type :embodies}
   {:source "radical-hypothesis" :target "bravli"      :type :embodies}
   {:source "sculptors-paradox"  :target "evaluate"    :type :embodies}
   {:source "interdependency"    :target "model"       :type :embodies}
   {:source "art-as-checksum"    :target "manifest"    :type :embodies}
   {:source "art-as-checksum"    :target "evaluate"    :type :embodies}

   ;; Writing → website
   {:source "writing" :target "website"  :type :serves}
   {:source "writing" :target "manifest" :type :serves}

   ;; MāyāLoom → modules it annotates
   {:source "mayaloom" :target "mayapramana" :type :depends}
   {:source "mayaloom" :target "model"       :type :embodies}

   ;; Thread-touches: thread → modules/infra
   {:source "thread-project-browser" :target "website"         :type :thread-touches}
   {:source "thread-project-browser" :target "phantom-faculty" :type :thread-touches}
   {:source "thread-autonomy"        :target "sutra"           :type :thread-touches}
   {:source "thread-autonomy"        :target "mayapramana"     :type :thread-touches}
   {:source "thread-autonomy"        :target "mayaloom"        :type :thread-touches}
   {:source "thread-mayadevgenz"     :target "bravli"          :type :thread-touches}
   {:source "thread-mayadevgenz"     :target "sutra"           :type :thread-touches}])

;; === Edge index for hover lookups ============================================

(def connections
  "Map from entity id to set of connected entity ids (root level only)."
  (reduce (fn [m {:keys [source target]}]
            (-> m
                (update source (fnil conj #{}) target)
                (update target (fnil conj #{}) source)))
          {}
          edges))

(def child-connections
  "Map from parent entity id to its child-level connection map."
  (into {}
        (keep (fn [{:keys [id children]}]
                (when children
                  [id (reduce (fn [m {:keys [source target]}]
                                (-> m
                                    (update source (fnil conj #{}) target)
                                    (update target (fnil conj #{}) source)))
                              {}
                              (:edges children))])))
        entities))

;; === Cluster labels ==========================================================

(def cluster-labels
  [{:x -5.0 :y -1.2 :label "MEASURE"         :cluster "measure"}
   {:x  0.0 :y -5.5 :label "MODEL"            :cluster "model"}
   {:x  5.0 :y -1.2 :label "MANIFEST"         :cluster "manifest"}
   {:x  0.0 :y  5.5 :label "EVALUATE"         :cluster "evaluate"}
   {:x -1.5 :y  4.8 :label "FOUNDATIONS"       :cluster "philosophy"}])
