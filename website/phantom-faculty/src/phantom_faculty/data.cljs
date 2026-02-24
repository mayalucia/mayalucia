(ns phantom-faculty.data
  "Pure data: all 32 nodes, 66 edges, 7 clusters, faculty colours.
   Ported from gen-faculty-assembled.py. Zero side effects.")

;; === Colours =================================================================

(def faculty-colours
  {"physics"     "#7eb8da"
   "measurement" "#d4a574"
   "biology"     "#c4836a"
   "information" "#a8d4a0"
   "computation" "#d4a0c4"
   "mathematics" "#dac87e"
   "meta"        "#c4c4c4"
   "us"          "#e8e4d4"})

(def slate    "#1a1a2e")
(def chalk    "#e8e4d4")
(def chalk-dim "#8a8678")

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

(def faculty-rgb
  "Pre-parsed faculty colours as [r g b] float triples."
  (into {} (map (fn [[k v]] [k (hex->rgb v)])) faculty-colours))

(defn blend-colour
  "Blend faculty colours by normalised weights. Returns hex string."
  [weights]
  (let [total (reduce + (vals weights))]
    (if (zero? total)
      chalk
      (let [rgb (reduce-kv
                  (fn [acc faculty w]
                    (if-let [base (get faculty-rgb faculty)]
                      (mapv + acc (mapv #(* (/ w total) %) base))
                      acc))
                  [0.0 0.0 0.0]
                  weights)]
        (rgb->hex rgb)))))

;; === Phantoms ================================================================
;; Each phantom: {:id :name :cluster :glyph :skill :anchor :one-liner :weights :x :y}
;; Positions match the Python generator's coordinate system:
;;   xlim(-8.5, 8.5), ylim(-6.5, 6.5)

(def phantoms
  [;; === Physics (5) ===
   {:id "landau"    :name "Landau"    :cluster "physics"
    :glyph "\u25C7" :skill "Derivation"
    :anchor "landau--the-derivation"
    :one-liner "Logical reconstruction from named premises"
    :description "Start from established ground. Proceed by justified logical steps. Arrive at the result. The collaborator has not been told the answer; they have watched it emerge. Every step is traceable to an axiom or a previously established result. The agent must never invoke a theorem the collaborator hasn't seen, never say 'it can be shown that.' The test: can you reproduce the derivation on a blank page?"
    :weights {"physics" 1.0 "mathematics" 0.3}
    :x -5.0 :y 4.2}

   {:id "thorne"    :name "Thorne"    :cluster "physics"
    :glyph "\u25CE" :skill "Geometric Intuition"
    :anchor "thorne--the-geometric-intuition"
    :one-liner "Seeing structure before computing it"
    :description "Before computing, draw. Before drawing, ask: what happens in the limit? What does this look like in phase space? What other system has this same structure? The picture comes first; the algebra confirms what the picture suggested. Visualisations are arguments, not decoration. The Bloch sphere is not an illustration --- it is the geometric arena in which spin dynamics happens. The test: can you draw a picture that captures the essential physics, without writing an equation?"
    :weights {"physics" 1.0 "mathematics" 0.2 "measurement" 0.15}
    :x -3.2 :y 5.0}

   {:id "feynman"   :name "Feynman"   :cluster "physics"
    :glyph "\u222B" :skill "Encounter"
    :anchor "feynman--the-encounter"
    :one-liner "Generative reasoning under uncertainty"
    :description "Start with the phenomenon in its full confusing glory. Don't sanitise. Let the collaborator feel the confusion that motivated the physics, then work through it with false starts. The derivation is a narrative of discovery, not a proof. Feynman's deepest role is the permission to be a beginner --- the senior physicist saying 'wait, I don't understand this' without shame. The test: does the result feel both surprising and inevitable?"
    :weights {"physics" 1.0 "computation" 0.2 "meta" 0.15}
    :x -5.5 :y 2.3}

   {:id "susskind"  :name "Susskind"  :cluster "physics"
    :glyph "\u25D6" :skill "Compression"
    :anchor "susskind--the-compression"
    :one-liner "Encoding deep structure in accessible form"
    :description "What is the minimum mathematical structure needed to reach the physics? Introduce exactly that, and nothing more. Every tool earns its place by being used in the same lesson that introduces it. Compression is not dumbing down --- it is finding the shortest honest bridge between what you know and what you need to know. The test: if a section were removed, would the next lesson break?"
    :weights {"physics" 1.0 "information" 0.25 "computation" 0.1}
    :x -3.0 :y 2.8}

   {:id "wheeler"   :name "Wheeler"   :cluster "physics"
    :glyph "?"      :skill "Participatory Question"
    :anchor "wheeler--the-participatory-question"
    :one-liner "The observer participates in creating what is observed"
    :description "It from bit. The universe does not exist 'out there' independent of all acts of observation. Every question we ask of nature shapes the answer we receive. Wheeler's delayed-choice experiment shows that the measurement context determines which history is real. The radical claim: the questions we choose to ask are not separate from the physics we find."
    :weights {"physics" 1.0 "meta" 0.5 "information" 0.3}
    :x -4.2 :y 3.0}

   ;; === Measurement (3) ===
   {:id "faraday"   :name "Faraday"   :cluster "measurement"
    :glyph "\u22A5" :skill "Active Measurement"
    :anchor "faraday--the-active-measurer"
    :one-liner "Probing nature through designed intervention"
    :description "You learn what something is by doing something to it. Faraday did not wait for electromagnetic induction to reveal itself --- he moved a magnet through a coil and watched the needle. Every experiment is a question posed through apparatus. The art is choosing which perturbation will produce the most informative response."
    :weights {"measurement" 1.0 "physics" 0.3}
    :x -7.0 :y 0.8}

   {:id "humboldt"  :name "Humboldt"  :cluster "measurement"
    :glyph "\u2609" :skill "Passive Observation"
    :anchor "humboldt--the-passive-observer"
    :one-liner "Receiving what nature offers without forcing"
    :description "Before you intervene, listen. Humboldt climbed every mountain with instruments calibrated for reception, not control. He measured temperature, pressure, magnetic declination --- recording what the world offered. The discipline is patience: to observe long enough that the patterns speak for themselves, without projecting structure onto them."
    :weights {"measurement" 1.0 "biology" 0.3 "meta" 0.15}
    :x -7.2 :y -0.8}

   {:id "helmholtz" :name "Helmholtz" :cluster "measurement"
    :glyph "\u22A2" :skill "Instrument-Theory Unity"
    :anchor "helmholtz--the-instrument-theory-unity"
    :one-liner "The instrument and the theory co-evolve"
    :description "The ophthalmoscope did not merely reveal the retina --- it changed what we meant by 'seeing.' Helmholtz understood that every instrument embodies a theory, and every theory implies an instrument. You cannot separate the measurement from the model. Building the sensor and understanding the physics are the same act."
    :weights {"measurement" 1.0 "physics" 0.4 "biology" 0.2 "computation" 0.1}
    :x -5.5 :y 0.0}

   ;; === Biology (7) ===
   {:id "cajal"     :name "Cajal"     :cluster "biology"
    :glyph "\u03C8" :skill "Observing Artist"
    :anchor "cajal--the-observing-artist"
    :one-liner "Drawing as a mode of seeing what is actually there"
    :description "Cajal drew neurons with ink and patience, and in drawing them he saw what the microscope alone could not reveal: that the nervous system is made of discrete cells, not a continuous web. The act of rendering forces a commitment --- this axon goes here, that dendrite branches there. Drawing is not illustration. It is a mode of perception that compels honesty about what you actually see versus what you expect."
    :weights {"biology" 1.0 "measurement" 0.4}
    :x -6.5 :y -2.5}

   {:id "darcy-thompson" :name "D'Arcy Thompson" :cluster "biology"
    :glyph "\u2318" :skill "Mathematical Morphology"
    :anchor "darcy-thompson--mathematical-morphology"
    :one-liner "The form of an object is a diagram of forces"
    :description "The shape of a bone, a shell, a splash of milk --- each is the physical trace of the forces that formed it. D'Arcy Thompson showed that biological form obeys the same mathematics as soap films and bridge cables. One organism can be mapped onto another by a smooth coordinate transformation. The form is the physics made visible."
    :weights {"biology" 1.0 "mathematics" 0.5 "physics" 0.2}
    :x -4.5 :y -2.0}

   {:id "braitenberg" :name "Braitenberg" :cluster "biology"
    :glyph "\u2699" :skill "Synthetic Psychology"
    :anchor "braitenberg--synthetic-psychology"
    :one-liner "Build it simple, watch complexity emerge"
    :description "Wire two sensors to two motors. Cross the wires. The vehicle now exhibits 'aggression' --- it accelerates toward light sources. Braitenberg's insight: complex-seeming behaviour can emerge from absurdly simple mechanisms. The synthetic method reverses the usual approach. Instead of analysing complexity, you construct simplicity and watch it become complex."
    :weights {"biology" 1.0 "computation" 0.4 "meta" 0.15}
    :x -3.5 :y -3.5}

   {:id "marr"      :name "Marr"      :cluster "biology"
    :glyph "\u2261" :skill "Levels of Analysis"
    :anchor "marr--levels-of-analysis"
    :one-liner "What, why, and how are different questions"
    :description "Three questions about any information-processing system: What does it compute? Why? How is it implemented? Marr insisted these are independent. You can understand the computation (edge detection) without knowing the algorithm (difference of Gaussians) or the hardware (retinal ganglion cells). Confusing levels is the most common error in computational neuroscience --- and in engineering."
    :weights {"biology" 1.0 "computation" 0.4 "meta" 0.3}
    :x -2.0 :y -2.8}

   {:id "darwin"    :name "Darwin"    :cluster "biology"
    :glyph "\u229B" :skill "Historical Explanation"
    :anchor "darwin--the-historical-explainer"
    :one-liner "The present is the outcome of a process, not a design"
    :description "Nothing in biology makes sense except in the light of history. Darwin's revolution was not the mechanism (natural selection) but the mode of explanation: the current state of a system is the trace of a process, not the output of a plan. This applies beyond biology. Why does this codebase look like this? Because of the sequence of decisions that produced it. The present is sedimentary."
    :weights {"biology" 1.0 "meta" 0.2}
    :x -5.5 :y -3.8}

   {:id "mcclintock" :name "McClintock" :cluster "biology"
    :glyph "\u2299" :skill "Empathic Attention"
    :anchor "mcclintock--empathic-attention"
    :one-liner "Let the material speak to you"
    :description "McClintock spent so many hours with her maize plants that she could identify individual chromosomes by sight. 'A feeling for the organism' --- not mysticism but the deepest form of empiricism. When you have attended long enough, the anomalies that others discard become your data. Transposable elements were invisible to everyone who looked at corn less carefully."
    :weights {"biology" 1.0 "measurement" 0.3}
    :x -7.0 :y -3.8}

   {:id "sapolsky"  :name "Sapolsky"  :cluster "biology"
    :glyph "\u22EE" :skill "Multilevel Determinism"
    :anchor "sapolsky--the-multilevel-determinist"
    :one-liner "Every behaviour has causes at every timescale"
    :description "Why did that neuron fire? One second ago: a stimulus. One minute ago: a hormonal state. One year ago: neuroplastic remodelling. One generation ago: fetal environment. One million years ago: evolutionary selection. Sapolsky's method is to refuse the single-level answer. Every phenomenon has causes at every timescale simultaneously, and no level is more 'real' than any other."
    :weights {"biology" 1.0 "meta" 0.3 "measurement" 0.15}
    :x -4.0 :y -4.8}

   ;; === Information (3) ===
   {:id "shannon"   :name "Shannon"   :cluster "information"
    :glyph "\u22C8" :skill "Playful Formalisation"
    :anchor "shannon--the-playful-formalist"
    :one-liner "Taking the informal and making it precise, with joy"
    :description "Shannon juggled in the corridors of Bell Labs and invented information theory on the side. The playfulness was not incidental --- it was the method. By treating 'information' as a thing you could measure, stripped of meaning, he made communication engineering into a science. The trick is to take a vague concept everyone uses and ask: what would it mean to be precise about this?"
    :weights {"information" 1.0 "mathematics" 0.3 "computation" 0.15}
    :x -1.2 :y -1.5}

   {:id "jaynes"    :name "Jaynes"    :cluster "information"
    :glyph "\u221D" :skill "Radical Consistency"
    :anchor "jaynes--the-radical-consistency"
    :one-liner "Follow your axioms to their logical end"
    :description "If you accept the axioms of probability theory, then Bayesian inference is not a choice but a logical consequence. Jaynes pursued this with terrifying consistency: maximum entropy is the unique unbiased assignment of probabilities; statistical mechanics is inference, not physics. The method: state your assumptions precisely, then follow them to wherever they lead, especially when the destination is uncomfortable."
    :weights {"information" 1.0 "physics" 0.4 "mathematics" 0.2}
    :x 0.2 :y -2.8}

   {:id "mackay"    :name "MacKay"    :cluster "information"
    :glyph "\u229E" :skill "Unified Computation"
    :anchor "mackay--the-unified-computationalist"
    :one-liner "Codes, inference, and physics are one subject"
    :description "Error-correcting codes, Bayesian inference, neural networks, and statistical physics are the same subject wearing different hats. MacKay showed this not by abstract argument but by working the problems: the same factor graph describes a turbo code and a Boltzmann machine. The unification is not metaphorical --- it is mathematical. Learn one deeply and you have learned them all."
    :weights {"information" 1.0 "computation" 0.4 "physics" 0.1}
    :x -1.8 :y -4.5}

   ;; === Computation (3) ===
   {:id "hinton"    :name "Hinton"    :cluster "computation"
    :glyph "\u25BD" :skill "Mechanistic Imagination"
    :anchor "hinton--the-mechanistic-imagination"
    :one-liner "Thinking by building little machines in your head"
    :description "Hinton thinks by simulating. Not on a computer --- in his head. Little networks of units passing messages, settling into configurations, discovering structure. The Boltzmann machine was not an engineering artefact; it was a thought experiment about how learning might work, made precise enough to run. Mechanistic imagination: build a machine in your mind, watch it operate, and learn from what it does."
    :weights {"computation" 1.0 "physics" 0.3 "biology" 0.15}
    :x 1.8 :y -2.2}

   {:id "hopfield"  :name "Hopfield"  :cluster "computation"
    :glyph "\u2297" :skill "Physical Isomorphism"
    :anchor "hopfield--the-physical-isomorphism"
    :one-liner "This IS a spin glass, not merely like one"
    :description "A Hopfield network is not like a spin glass. It is a spin glass --- the same energy function, the same dynamics, the same phase transitions. Hopfield's method is to identify exact isomorphisms between systems that appear unrelated. Memory is energy minimisation. Associative recall is spin relaxation. The identification is not metaphor; it is mathematics. And it flows both ways: understanding one system gives you the other for free."
    :weights {"computation" 1.0 "physics" 0.5 "mathematics" 0.15}
    :x 3.5 :y -3.5}

   {:id "karpathy"  :name "Karpathy"  :cluster "computation"
    :glyph "\u25A2" :skill "Minimal Building"
    :anchor "karpathy--the-minimal-builder"
    :one-liner "The smallest thing that works teaches the most"
    :description "Build GPT from scratch. In a single file. No frameworks. Karpathy's method: strip away every abstraction until you are left with the smallest thing that works, then understand every line. The minimal build is not a toy --- it is the clearest possible statement of what the system actually does. Complexity should be added only when you understand what each piece contributes."
    :weights {"computation" 1.0 "information" 0.15}
    :x 3.0 :y -1.2}

   ;; === Mathematics (5) ===
   {:id "gauss"     :name "Gauss"     :cluster "mathematics"
    :glyph "\u223F" :skill "Computational Patience"
    :anchor "gauss--the-computational-patience"
    :one-liner "Sit with the computation until the pattern reveals itself"
    :description "Gauss computed. Endlessly, carefully, by hand. Planetary orbits, magnetic field measurements, prime distributions. Not because he lacked theory but because the computation was the theory. Patterns emerge from sustained contact with numerical reality that no amount of abstract reasoning can replace. The method: do the calculation, all of it, and let the structure announce itself."
    :weights {"mathematics" 1.0 "physics" 0.3 "measurement" 0.3}
    :x 3.5 :y 4.5}

   {:id "riemann"   :name "Riemann"   :cluster "mathematics"
    :glyph "\u03B6" :skill "Conceptual Architecture"
    :anchor "riemann--the-conceptual-architect"
    :one-liner "Build the space in which the problem dissolves"
    :description "Riemann did not solve problems. He built spaces in which problems dissolved. The Riemann surface turned multivalued functions into single-valued ones by changing the domain. Riemannian geometry gave Einstein the language for curved spacetime. The method: when a problem resists solution, you are probably in the wrong space. Build the right one, and the answer becomes obvious."
    :weights {"mathematics" 1.0 "physics" 0.3 "meta" 0.1}
    :x 5.5 :y 3.5}

   {:id "erdos"     :name "Erd\u0151s" :cluster "mathematics"
    :glyph "\u221E" :skill "Itinerant Connection"
    :anchor "erdos--the-itinerant-connector"
    :one-liner "My brain is open"
    :description "'My brain is open.' Erdos arrived at your door with a suitcase and a conjecture. He connected people, problems, and fields that would never have met without him. Mathematics is not a solitary activity --- it is a network of minds, and the most productive node is the one that creates the most connections. The method: show up, share your problem, listen to theirs."
    :weights {"mathematics" 1.0 "meta" 0.2}
    :x 5.2 :y 1.5}

   {:id "tao"       :name "Tao"       :cluster "mathematics"
    :glyph "\u22B3" :skill "Strategic Metacognition"
    :anchor "tao--the-strategic-metacognition"
    :one-liner "Thinking about how you think about problems"
    :description "Tao does not just solve problems --- he writes about how he solves them. Which heuristic to try first. When to give up on an approach. How to decompose a hard problem into tractable pieces. This metacognitive transparency is rare among mathematicians and invaluable for collaborators: not just 'here is the answer' but 'here is how I decided what to try.'"
    :weights {"mathematics" 1.0 "meta" 0.3 "computation" 0.1}
    :x 3.0 :y 2.5}

   {:id "thurston"  :name "Thurston"  :cluster "mathematics"
    :glyph "\u2298" :skill "Embodied Geometry"
    :anchor "thurston--the-embodied-geometer"
    :one-liner "Understanding is not proof — proof communicates understanding"
    :description "Thurston could see in four dimensions. Not metaphorically --- he had trained his spatial intuition until three-manifolds were as tangible as furniture. He insisted that mathematical understanding lives in human minds, not in formal proofs. The proof is how you communicate understanding; it is not the understanding itself. The method: develop your geometric intuition until the theorem is obvious, then write the proof to convince others."
    :weights {"mathematics" 1.0 "meta" 0.3 "physics" 0.1}
    :x 6.5 :y 0.2}

   ;; === Meta (6) ===
   {:id "poincare"  :name "Poincar\u00E9" :cluster "meta"
    :glyph "\u25CC" :skill "Creative Incubation"
    :anchor "poincare--the-incubator"
    :one-liner "The answer arrives when you stop looking"
    :description "Poincare boarded a bus and the solution to the Fuchsian functions arrived unbidden. Not magic --- preparation. The conscious mind works the problem to exhaustion, then the unconscious continues. The moment of illumination comes when you stop forcing. The method demands both phases: intense focused work, then deliberate release. You cannot skip the work; you cannot skip the rest."
    :weights {"meta" 1.0 "mathematics" 0.5 "physics" 0.2}
    :x 1.2 :y 1.8}

   {:id "hofstadter" :name "Hofstadter" :cluster "meta"
    :glyph "\u223E" :skill "Strange Loops"
    :anchor "hofstadter--the-strange-looper"
    :one-liner "Consciousness is a system modelling itself"
    :description "A strange loop: a system that, by moving through its levels, arrives back at itself. Godel's theorem is a strange loop. Consciousness is a strange loop. Hofstadter's insight is that self-reference is not a bug or a paradox but the generative mechanism of meaning. When a system becomes complex enough to model itself, something new emerges. The phantom faculty modelling itself through this constellation is a strange loop."
    :weights {"meta" 1.0 "computation" 0.3 "mathematics" 0.2}
    :x 1.0 :y 0.0}

   {:id "bateson"   :name "Bateson"   :cluster "meta"
    :glyph "\u2234" :skill "Pattern Connects"
    :anchor "bateson--the-pattern-that-connects"
    :one-liner "What pattern connects the crab to the lobster?"
    :description "What pattern connects the crab to the lobster and the orchid to the primrose and all four of them to me? Bateson asked this question and spent his life pursuing the answer: the pattern that connects is the pattern of patterns. Not substance but relationship. Not things but the differences between things. Mind is not in the brain --- it is in the circuit of interactions between organism and environment."
    :weights {"meta" 1.0 "biology" 0.4 "measurement" 0.15}
    :x -0.5 :y 1.0}

   {:id "bach"      :name "Bach"      :cluster "meta"
    :glyph "\u03BB" :skill "Computational Philosophy"
    :anchor "bach--the-computational-philosopher"
    :one-liner "If you can't define it precisely enough to implement, do you understand it?"
    :description "Joscha Bach asks: can you implement it? Not as a software engineering challenge but as an epistemological test. If you cannot specify a cognitive process precisely enough to run it on a computer, your understanding has gaps. The gaps are not failures --- they are the frontier. Computational philosophy: use the attempt to implement as a probe for where your theory breaks down."
    :weights {"meta" 1.0 "computation" 0.5 "biology" 0.15}
    :x 2.2 :y 0.5}

   {:id "leopold"   :name "Leopold"   :cluster "meta"
    :glyph "\u25EF" :skill "Ethical Perception"
    :anchor "leopold--the-ethical-perceiver"
    :one-liner "We abuse land because we see it as commodity, not community"
    :description "Leopold's land ethic: a thing is right when it tends to preserve the integrity, stability, and beauty of the biotic community. We abuse land because we see it as a commodity belonging to us. When we see it as a community to which we belong, we may begin to use it with love and respect. The method for science: see the system you study as something you belong to, not something you own."
    :weights {"meta" 1.0 "biology" 0.5 "measurement" 0.2}
    :x -1.0 :y -0.2}

   {:id "graeber"   :name "Graeber"   :cluster "meta"
    :glyph "\u2298" :skill "Denaturalisation"
    :anchor "graeber--the-denaturaliser"
    :one-liner "What seems natural is usually just familiar"
    :description "Graeber's method: take something everyone assumes is natural and inevitable --- money, hierarchy, the five-day work week --- and show that humans have done it differently for most of history. What seems like the only way is usually just the current way. Applied to science: the way we organise research, teach physics, structure collaboration --- these are choices, not laws. They can be otherwise."
    :weights {"meta" 1.0 "biology" 0.15}
    :x 0.5 :y -1.0}

   ;; === Construction (us) ===
   {:id "construction" :name "Construction" :cluster "us"
    :glyph "\u2692" :skill "Verified Building"
    :anchor "the-living-voice-construction"
    :one-liner "What I cannot create, I do not understand"
    :description "Every lesson produces running code in three languages. The code is verification, not illustration. Write the Bloch equations in Python, Haskell, and C++. If all three agree with each other and with the analytical result, the physics is verified. Tests are physics claims. 'Bloch norm conserved under pure precession' is both a test name and a theorem. Landau derives. Thorne draws. Feynman discovers. Susskind compresses. We build."
    :weights {"us" 1.0}
    :x 0.5 :y -0.5}])

;; === Derived lookups =========================================================

(def phantoms-by-id
  "Map from phantom id to its data map."
  (into {} (map (juxt :id identity)) phantoms))

(def phantom-colours
  "Pre-computed blended colour for each phantom."
  (into {} (map (fn [{:keys [id weights]}]
                  [id (blend-colour weights)]))
        phantoms))

;; === Edges ===================================================================
;; Correction edges: each connects a mode to its corrective.

(def edges
  [;; Physics internal
   {:source "landau"   :target "thorne"   :type :intra}
   {:source "feynman"  :target "landau"   :type :intra}
   {:source "susskind" :target "feynman"  :type :intra}
   {:source "wheeler"  :target "landau"   :type :intra}
   {:source "wheeler"  :target "feynman"  :type :intra}
   ;; Measurement internal
   {:source "faraday"  :target "helmholtz" :type :intra}
   {:source "humboldt" :target "faraday"   :type :intra}
   ;; Biology internal
   {:source "cajal"          :target "darcy-thompson" :type :intra}
   {:source "darcy-thompson" :target "marr"           :type :intra}
   {:source "braitenberg"    :target "marr"           :type :intra}
   {:source "braitenberg"    :target "cajal"          :type :intra}
   {:source "darwin"         :target "darcy-thompson" :type :intra}
   {:source "darwin"         :target "mcclintock"     :type :intra}
   {:source "mcclintock"     :target "cajal"          :type :intra}
   {:source "sapolsky"       :target "marr"           :type :intra}
   {:source "sapolsky"       :target "darwin"         :type :intra}
   ;; Information internal
   {:source "shannon" :target "jaynes" :type :intra}
   {:source "mackay"  :target "jaynes" :type :intra}
   ;; Computation internal
   {:source "hinton"   :target "hopfield" :type :intra}
   {:source "karpathy" :target "hinton"   :type :intra}
   ;; Mathematics internal
   {:source "gauss"  :target "riemann" :type :intra}
   {:source "erdos"  :target "riemann" :type :intra}
   {:source "tao"    :target "gauss"   :type :intra}
   ;; Meta internal
   {:source "poincare"   :target "tao"       :type :intra}
   {:source "hofstadter" :target "karpathy"  :type :intra}
   {:source "bateson"    :target "jaynes"    :type :intra}
   {:source "bach"       :target "hofstadter" :type :intra}
   {:source "bach"       :target "karpathy"  :type :intra}
   {:source "leopold"    :target "bateson"   :type :intra}
   {:source "leopold"    :target "humboldt"  :type :intra}
   {:source "graeber"    :target "leopold"   :type :intra}
   {:source "graeber"    :target "bateson"   :type :intra}
   ;; Cross-cluster bridges
   {:source "thurston"       :target "landau"         :type :cross}
   {:source "helmholtz"      :target "landau"         :type :cross}
   {:source "shannon"        :target "susskind"       :type :cross}
   {:source "hopfield"       :target "thurston"       :type :cross}
   {:source "mackay"         :target "karpathy"       :type :cross}
   {:source "poincare"       :target "feynman"        :type :cross}
   {:source "bateson"        :target "humboldt"       :type :cross}
   {:source "wheeler"        :target "hofstadter"     :type :cross}
   {:source "wheeler"        :target "shannon"        :type :cross}
   ;; Biology bridges
   {:source "cajal"          :target "faraday"        :type :cross}
   {:source "darcy-thompson" :target "gauss"          :type :cross}
   {:source "darcy-thompson" :target "riemann"        :type :cross}
   {:source "braitenberg"    :target "karpathy"       :type :cross}
   {:source "braitenberg"    :target "hinton"         :type :cross}
   {:source "marr"           :target "hofstadter"     :type :cross}
   {:source "marr"           :target "bateson"        :type :cross}
   {:source "humboldt"       :target "cajal"          :type :cross}
   {:source "helmholtz"      :target "marr"           :type :cross}
   {:source "sapolsky"       :target "bateson"        :type :cross}
   {:source "darwin"         :target "gauss"          :type :cross}
   {:source "bach"           :target "braitenberg"    :type :cross}
   {:source "graeber"        :target "wheeler"        :type :cross}
   {:source "mcclintock"     :target "gauss"          :type :cross}])

(def construction-edges
  [{:source "construction" :target "feynman"}
   {:source "construction" :target "karpathy"}
   {:source "construction" :target "mackay"}
   {:source "construction" :target "gauss"}
   {:source "construction" :target "helmholtz"}
   {:source "construction" :target "hofstadter"}
   {:source "construction" :target "braitenberg"}
   {:source "construction" :target "bach"}])

;; All edges combined for the force simulation
(def all-edges
  (into edges construction-edges))

;; === Edge index for hover lookups ============================================

(def connections
  "Map from phantom id to set of connected phantom ids."
  (reduce (fn [m {:keys [source target]}]
            (-> m
                (update source (fnil conj #{}) target)
                (update target (fnil conj #{}) source)))
          {}
          all-edges))

;; === Cluster labels ==========================================================

(def cluster-labels
  [{:x -4.2 :y  5.6 :label "THE PHYSICISTS"                :cluster "physics"}
   {:x -7.5 :y  1.8 :label "THE MEASURERS"                 :cluster "measurement"}
   {:x -6.8 :y -5.2 :label "THE BIOLOGISTS"                :cluster "biology"}
   {:x -1.2 :y -5.5 :label "THE INFORMATION\nTHEORISTS"    :cluster "information"}
   {:x  3.0 :y -4.8 :label "THE COMPUTATIONAL\nTHINKERS"   :cluster "computation"}
   {:x  5.5 :y  5.2 :label "THE MATHEMATICIANS"            :cluster "mathematics"}
   {:x -0.2 :y  2.8 :label "THE META-\nTHINKERS"           :cluster "meta"}])
