+++
title = "MayaPortal: The Visual Synthesis Kernel"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T22:24:43+01:00
tags = ["portal"]
draft = false
+++

> The eye sees only what the mind is prepared to comprehend.
> — Robertson Davies


## MayaPortal Within MayaLucIA {#mayaportal-within-mayalucia}

`MayaLucIA` operates through an iterative cycle: **Measure → Model → Manifest → Evaluate → Refine**. Each stage transforms understanding—from raw measurements, through scientific models, into perceptible forms that can be assessed and improved. `MayaPortal` is the engine of the **Manifest** stage: the viewport through which digital twins become observable.

Where `MayaLucIA` asks "how do we understand?", `MayaPortal` asks "how do we see?" The distinction matters. A reconstruction algorithm may produce a statistically faithful model of a mountain valley or a cortical circuit, but that model remains abstract—a collection of numbers in memory—until it is rendered into form. `MayaPortal` performs this transformation: it takes the dense state produced by reconstruction and simulation, and projects it into visual (and eventually auditory) experience.

```text
┌─────────────────────────────────────────────────────────────────┐
│                        MayaLucIA Cycle                          │
│                                                                 │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐    │
│   │ MEASURE │───▶│  MODEL  │───▶│MANIFEST │───▶│ EVALUATE │    │
│   └─────────┘    └─────────┘    └────┬────┘    └────┬─────┘    │
│        ▲                             │              │          │
│        │                             ▼              │          │
│        │                      ┌────────────┐        │          │
│        │                      │ MayaPortal │        │          │
│        │                      │  Viewport  │        │          │
│        │                      └────────────┘        │          │
│        │                                            │          │
│        └───────────── REFINE ◀──────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

This is not merely visualization. The act of rendering forces decisions: What matters? What can be abstracted? What must be preserved? These decisions are themselves acts of understanding. When a river rendered from hydrological simulation "looks wrong" to an expert eye, that perception encodes knowledge that no metric captures. `MayaPortal` makes such judgments possible.


## The Observing Eye {#the-observing-eye}

At the heart of `MayaPortal` is a simple but powerful concept: the **observing eye**. Rather than producing static images or pre-rendered animations, `MayaPortal` maintains a live, interactive window into the reconstructed world. The observer—represented as a point in space with orientation—can move freely through the digital twin, examining it from any angle, at any scale.

This matters because understanding is perspectival. A geologist examining erosion patterns needs different views than an ecologist studying vegetation gradients. A neuroscientist tracing an axonal projection needs to zoom from whole-brain scale down to synaptic resolution. The observing eye provides this freedom: the digital twin is not a picture but a place.

```text
The Digital Twin is not the visualization.
The Digital Twin is the territory.
MayaPortal provides the map—and the freedom to explore.
```

The observing eye also enables a crucial feedback loop. As the scientist explores, they notice discrepancies, raise questions, form hypotheses. These observations feed back into the **Evaluate** stage, driving refinement. `MayaPortal` is not a passive display; it is an instrument of inquiry.


## Design Philosophy {#design-philosophy}


### Understanding Over Production {#understanding-over-production}

`MayaPortal` is not production software. It is a \*learning artifact\*—a codebase designed to be understood as much as used. Every architectural decision prioritizes conceptual clarity:

-   **Explicit over implicit**: Dependencies are visible. State flows are traceable. There are no hidden globals or magical frameworks.

-   **Composition over inheritance**: Components combine through well-defined interfaces, not through class hierarchies that obscure behavior.

-   **Pure cores, effectful shells**: Simulation and rendering logic are separated from I/O and GPU side effects. The pure core can be tested, reasoned about, and ported independently.

This philosophy aligns with `MayaLucIA`'s broader commitment to understanding through creation. We do not merely use `MayaPortal`; we build it, and in building it, we learn modern GPU programming from first principles.


### Functional Architecture {#functional-architecture}

`MayaPortal` adopts patterns from functional programming—not as dogma, but as tools for managing complexity. The key insight: a rendering pipeline is fundamentally a **data transformation**.

```text
State → Commands → Pixels
```

Each frame, we transform simulation state into draw commands, and draw commands into pixels. By modeling this flow explicitly, we gain:

-   **Testability**: Pure transformation functions can be unit tested without GPU hardware.
-   **Composability**: Rendering passes combine cleanly without hidden interactions.
-   **Debuggability**: State at any point in the pipeline can be inspected and logged.

We organize these transformations using a monadic vocabulary:

| Pattern  | Role in MayaPortal                                      |
|----------|---------------------------------------------------------|
| Reader   | Immutable GPU context (device, pipelines, layouts)      |
| State    | Evolving simulation and camera state                    |
| Expected | Fallible operations (shader compilation, asset loading) |
| Writer   | Accumulated metrics and debug information               |

This vocabulary is documented in [monadic-composition.org]({{< relref "monadic-composition" >}}). We do not force Haskell idioms into C++; rather, we name recurring patterns so they can be recognized, discussed, and composed consistently.


### The Viewport as Instrument {#the-viewport-as-instrument}

Scientific instruments transform phenomena into perceptible signals. A microscope transforms light scattering into magnified images. A spectrometer transforms electromagnetic radiation into spectral plots. `MayaPortal` transforms computational state into interactive visual experience.

Like any instrument, `MayaPortal` has characteristics that shape what can be observed:

-   **Resolution**: How fine a detail can be rendered?
-   **Frame rate**: How smoothly can dynamics be perceived?
-   **Fidelity**: How accurately does the rendering reflect the underlying model?
-   **Interaction latency**: How responsive is exploration?

These characteristics define the "observational limits" of our digital twin—analogous to the metrology constraints in `MayaLucIA`'s reconstruction phase. A faithful digital twin rendered at 2 frames per second loses temporal information. A beautiful real-time visualization that misrepresents the data misleads. `MayaPortal` must balance these constraints consciously.


## Technical Architecture {#technical-architecture}


### Core Components {#core-components}

```text
┌──────────────────────────────────────────────────────────────┐
│                        MayaPortal                            │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐ │
│  │  Runtime   │  │  Context   │  │      Renderer          │ │
│  │  (IO)      │──│  (Reader)  │──│  State → DrawCommands  │ │
│  │            │  │            │  │                        │ │
│  │ - Window   │  │ - Device   │  │ - Camera               │ │
│  │ - Events   │  │ - Queue    │  │ - Scene graph          │ │
│  │ - Main     │  │ - Pipelines│  │ - Render passes        │ │
│  │   loop     │  │ - Layouts  │  │ - Post-processing      │ │
│  └────────────┘  └────────────┘  └────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    Simulation State                     │ │
│  │                                                         │ │
│  │  Particles, Fields, Meshes, Volumes, Time series...    │ │
│  │  (Data structures shared with MayaLucIA Model stage)   │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

-   **Runtime**: Manages the application lifecycle—window creation, event polling, frame timing. This is the "effectful shell" that interfaces with the operating system.

-   **Context**: Holds immutable GPU resources initialized at startup—the WebGPU device, queue, compiled pipelines, bind group layouts. Passed implicitly (Reader pattern) to rendering functions.

-   **Renderer**: Pure functions that transform simulation state into sequences of draw commands. The renderer does not execute commands; it describes what should be drawn.

-   **Simulation State**: The data being visualized—particle positions, scalar fields, mesh geometries, time series. This state is owned by `MayaLucIA`'s Model stage; `MayaPortal` reads it for rendering.


### Technology Stack {#technology-stack}

Our technology choices prioritize learning and transparency over convenience:

| Layer           | Technology    | Rationale                                |
|-----------------|---------------|------------------------------------------|
| GPU Abstraction | WebGPU (Dawn) | Modern, explicit, portable to web        |
| Native Binding  | wgpu-native   | Avoids Dawn build complexity             |
| Windowing       | SDL3          | Mature, cross-platform, Emscripten-ready |
| Shaders         | WGSL          | Native WebGPU language, no transpilation |
| C++ Standard    | C++23         | Expected, ranges, coroutines             |
| Python Bridge   | pybind11      | Expose viewport for scripting            |
| Prototyping     | wgpu-py       | Rapid Python experiments before C++ port |
| Web Deployment  | Emscripten    | Share visualizations via browser         |

The full rationale is documented in [techstack.org]({{< relref "techstack" >}}).


### The Rendering Pipeline {#the-rendering-pipeline}

A typical frame flows through these stages:

1.  **Input Processing**: SDL events are polled and translated into camera movements, parameter adjustments, or mode changes.

2.  **State Update**: If simulation is running, the state advances by one timestep. This is a pure function: `update(state, dt) → state'`.

3.  **Command Generation**: The renderer inspects current state and camera, producing a list of draw commands. This is also pure: `render(state, camera, context) → commands`.

4.  **Command Execution**: The effectful shell submits commands to the GPU queue and presents the frame.

5.  **Metrics Collection**: Frame time, draw call count, and other diagnostics are accumulated (Writer pattern) for display or logging.

<!--listend-->

```cpp
// Pseudocode: one frame of the main loop
auto frame(AppState& app, const GPUContext& ctx) -> void {
    // 1. Input
    auto events = poll_events();
    auto input = process_input(events);

    // 2. State update (pure)
    app.sim_state = update(app.sim_state, input, app.dt);
    app.camera = update_camera(app.camera, input);

    // 3. Command generation (pure)
    auto commands = render(app.sim_state, app.camera, ctx);

    // 4. Execution (effectful)
    submit_and_present(ctx, commands);

    // 5. Metrics
    app.metrics = collect_metrics(app.metrics, commands);
}
```


## Integration with MayaLucIA {#integration-with-mayalucia}


### Data Flow from Model to Manifest {#data-flow-from-model-to-manifest}

`MayaLucIA`'s Model stage produces structured representations of natural systems:

-   **Parbati** (mountain reconstruction): Terrain heightfields, river networks, vegetation distributions, geological strata.
-   **Bravli** (brain circuits): Neuron morphologies, synaptic connectivity matrices, voltage traces, spike trains.

`MayaPortal` must render all of these. This requires flexible data structures that can represent diverse phenomena:

```text
SimulationState
├── Geometry
│   ├── PointClouds (particles, cell bodies)
│   ├── Meshes (terrain, neuron surfaces)
│   ├── Volumes (density fields, scalar fields)
│   └── Lines (river networks, axonal projections)
├── Dynamics
│   ├── TimeSeries (voltage traces, flow rates)
│   └── Events (spikes, threshold crossings)
└── Metadata
    ├── Labels (region names, cell types)
    └── Annotations (user markers, highlights)
```

The key constraint: `MayaPortal` does not own this data. It receives immutable references from the Model stage and renders them. This separation ensures that visualization does not corrupt simulation state.


### Feedback to Evaluate {#feedback-to-evaluate}

The Evaluate stage needs information from visualization:

-   **Qualitative assessment**: Does the rendering "look right"? This requires human judgment, which `MayaPortal` enables through interactive exploration.

-   **Quantitative metrics**: Rendering can compute derived quantities—visibility statistics, occlusion percentages, spatial distributions—that feed into evaluation.

-   **Annotations**: The scientist may mark regions of interest, flag anomalies, or record observations. `MayaPortal` must support this annotation workflow.


### Agent Integration {#agent-integration}

In `MayaLucIA`'s Agency model, the **Sculptor Agent** specializes in visualization and media. `MayaPortal` is the Sculptor's primary instrument. The agent:

-   Suggests appropriate rendering modes for different data types
-   Adjusts visual parameters (color maps, opacity, level of detail) based on the scientist's focus
-   Generates scripted camera paths for documentation
-   Exports frames and animations for publication

The Sculptor Agent does not replace the scientist's judgment; it amplifies their capacity to explore and express.


## Phenomena Modules {#phenomena-modules}

`MayaPortal` will grow through \*phenomenon modules\*—self-contained packages that implement rendering for specific natural systems. Each module demonstrates techniques while serving `MayaLucIA`'s scientific goals.


### Planned Modules {#planned-modules}

| Module       | Phenomenon               | Techniques                            |
|--------------|--------------------------|---------------------------------------|
| Terrain      | Mountain landscapes      | Heightfield rendering, atmospheric    |
|              |                          | scattering, vegetation instancing     |
| Hydrology    | River networks, flow     | Streamlines, particle advection,      |
|              |                          | volume rendering for sediment         |
| Morphology   | Neuron shapes            | Tube rendering, transparency,         |
|              |                          | level-of-detail for dense scenes      |
| Connectivity | Synaptic networks        | Edge bundling, matrix visualization,  |
|              |                          | graph layout                          |
| Dynamics     | Spikes, waves, diffusion | Time-series overlay, animated fields, |
|              |                          | sonification hooks                    |

Each module follows a common structure:

1.  **Data interface**: What state does it read?
2.  **Rendering passes**: What GPU work does it perform?
3.  **Parameters**: What can the user adjust?
4.  **Integration**: How does it compose with other modules?


### Module 0: The Empty Viewport {#module-0-the-empty-viewport}

Before phenomena, we build the viewport itself:

-   [ ] Window creation and event loop (SDL3)
-   [ ] WebGPU device and surface initialization
-   [ ] Clear color and present
-   [ ] Frame timing and basic metrics
-   [ ] Camera controls (orbit, pan, zoom)

This "empty viewport" is the foundation. Every subsequent module builds upon it.


## Learning Objectives {#learning-objectives}

Building `MayaPortal` teaches:


### GPU Programming Fundamentals {#gpu-programming-fundamentals}

-   The explicit resource model (buffers, textures, bind groups)
-   Pipeline state (shaders, blend modes, depth testing)
-   Command encoding and submission
-   Synchronization and frame pacing


### Graphics Techniques {#graphics-techniques}

-   Rasterization and the graphics pipeline
-   Vertex and fragment shaders in WGSL
-   Compute shaders for simulation
-   Post-processing and compositing


### Software Architecture {#software-architecture}

-   Functional patterns in systems programming
-   Error handling without exceptions
-   Resource lifetime management
-   Testing graphics code


### Scientific Visualization {#scientific-visualization}

-   Mapping data to visual variables
-   Handling scale (molecular to planetary)
-   Interactive exploration design
-   Combining multiple representations


## Development Roadmap {#development-roadmap}


### Phase 0: Development Process Infrastructure {#phase-0-development-process-infrastructure}

Establish the literate, tagged, test-driven development process _before_ writing application code. Detailed plan in [plan.org]({{< relref "plan" >}}); process specification in [development-plan.org]({{< relref "development-plan" >}}).

-   [ ] Directory scaffold (`codex/`, `src/`, `tests/`, `shaders/`, `specs/`)
-   [ ] `codex/00-prelude.org` — first literate lesson (tangles to trivial C++ + test)
-   [ ] `CMakeLists.txt` with C++23, Catch2 v3, and `tangle` target
-   [ ] `specs/spec-build.org` — build requirements as testable contracts
-   [ ] `LESSONS.org` — index of tags → lessons → learning objectives
-   [ ] End-to-end validation: tangle → build → test
-   [ ] Tag `lesson/00-prelude`


### Phase 1: Foundation {#phase-1-foundation}

-   [X] Project structure and build system
-   [ ] SDL3 window with WebGPU surface
-   [ ] Basic render loop with timing
-   [ ] Camera controller
-   [ ] Debug overlay (metrics, state inspection)


### Phase 2: Primitives {#phase-2-primitives}

-   [ ] Point cloud rendering
-   [ ] Line rendering (thick lines, stippling)
-   [ ] Mesh rendering (indexed triangles)
-   [ ] Basic lighting (Blinn-Phong)


### Phase 3: Phenomenon Modules {#phase-3-phenomenon-modules}

-   [ ] Terrain heightfield (Parbati)
-   [ ] Neuron morphology (Bravli)
-   [ ] Particle systems
-   [ ] Volume rendering (scalar fields)


### Phase 4: Integration {#phase-4-integration}

-   [ ] Python bindings (pybind11)
-   [ ] State serialization for replay
-   [ ] Annotation system
-   [ ] Export (images, video, glTF)


### Phase 5: Polish {#phase-5-polish}

-   [ ] Web deployment (Emscripten)
-   [ ] Documentation and tutorials
-   [ ] Performance profiling
-   [ ] Accessibility considerations


## Guiding Principles {#guiding-principles}

As we develop `MayaPortal`, we hold to these principles:

1.  **Build to understand, not to ship.** The codebase is a learning artifact. Clarity matters more than features.

2.  **One phenomenon at a time.** Each module is a complete, working example. We do not build frameworks; we build working things that teach.

3.  **Pure cores, effectful shells.** Separate what can be tested from what must be run. Keep the GPU at the boundary.

4.  **Explicit is better than implicit.** Name the patterns. Document the decisions. Make the architecture visible.

5.  **The scientist stays in the loop.** `MayaPortal` amplifies human perception and judgment. It does not replace them.


## Conclusion {#conclusion}

`MayaPortal` is where `MayaLucIA`'s digital twins become visible. It transforms abstract reconstructions into interactive experiences that can be explored, assessed, and refined. More than a renderer, it is an instrument of understanding—a lens through which the scientist perceives their computational creations.

By building `MayaPortal` from first principles, with functional architecture and explicit patterns, we learn not just graphics programming but a way of thinking about complex systems. The code itself becomes documentation of that thinking—a trail of understanding that others can follow.

The viewport awaits. Let us build it, and through building, understand.
