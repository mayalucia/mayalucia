(ns project-constellation.force
  "D3-force interop: simulation setup, tick -> ratom.
   D3 computes positions; Reagent owns the DOM.
   Typed link distances vary by edge type.
   Parameterised: accepts entities/edges for hierarchical drill-down."
  (:require
    [project-constellation.state :as state]
    ["d3-force" :as d3f]))

(defonce !simulation (atom nil))

(def ^:private link-distances
  "Target distance by edge type."
  {:cycle-flow     4.0
   :refine-arc     4.0
   :serves         2.0
   :depends        1.5
   :embodies       2.5
   :thread-touches 1.5
   :flow           2.0
   :related        1.5})

(def ^:private link-strengths
  "Pull strength by edge type."
  {:cycle-flow     0.3
   :refine-arc     0.1
   :serves         0.15
   :depends        0.2
   :embodies       0.05
   :thread-touches 0.1
   :flow           0.15
   :related        0.1})

(defn init-simulation!
  "Create a d3-force simulation from given entities and edges.
   All nodes start pinned at hand-tuned positions."
  [entities edges]
  (when-let [old @!simulation]
    (.stop old))
  (let [nodes (into-array
                (mapv (fn [{:keys [id x y]}]
                        #js {:id id :x x :y y :fx x :fy y})
                      entities))
        links (into-array
                (mapv (fn [{:keys [source target type]}]
                        #js {:source source :target target
                             :edge-type (name type)})
                      edges))
        sim   (-> (d3f/forceSimulation nodes)
                  (.force "link"
                    (-> (d3f/forceLink links)
                        (.id (fn [d] (.-id d)))
                        (.distance
                          (fn [^js link]
                            (let [t (keyword (.-edge-type link))]
                              (get link-distances t 2.0))))
                        (.strength
                          (fn [^js link]
                            (let [t (keyword (.-edge-type link))]
                              (get link-strengths t 0.1))))))
                  (.force "charge"
                    (-> (d3f/forceManyBody)
                        (.strength -0.3)))
                  (.force "center"
                    (d3f/forceCenter 0 0))
                  (.force "collide"
                    (-> (d3f/forceCollide)
                        (.radius 0.6)))
                  (.alphaDecay 0.02))]
    (.on sim "tick"
      (fn []
        (let [positions (into {}
                          (map (fn [n]
                                 [(.-id n) {:x (.-x n) :y (.-y n)}]))
                          nodes)]
          (reset! state/!node-positions positions))))
    (reset! !simulation sim)))

(defn restart-with!
  "Stop current simulation and start a new one with given entities and edges."
  [entities edges]
  (init-simulation! entities edges))

(defn unpin-all!
  "Release non-phase nodes — let the force simulation find equilibrium."
  []
  (when-let [sim @!simulation]
    (let [phase-ids #{"measure" "model" "manifest" "evaluate"}]
      (doseq [n (.nodes sim)]
        (when-not (contains? phase-ids (.-id n))
          (set! (.-fx n) nil)
          (set! (.-fy n) nil))))
    (.alpha sim 0.3)
    (.restart sim)))

(defn stop!
  "Stop the simulation."
  []
  (when-let [sim @!simulation]
    (.stop sim)))
