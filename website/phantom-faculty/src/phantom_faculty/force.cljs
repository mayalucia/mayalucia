(ns phantom-faculty.force
  "D3-force interop: simulation setup, tick -> ratom.
   D3 computes positions; Reagent owns the DOM."
  (:require
    [phantom-faculty.state :as state]
    [phantom-faculty.data :as data]
    ["d3-force" :as d3f]))

(defonce !simulation (atom nil))

(defn init-simulation!
  "Create a d3-force simulation. Nodes start pinned at hand-tuned positions
   (fx/fy set), so the initial view matches the static PNG exactly.
   Future: call unpin-all! to release for force-directed exploration."
  []
  (let [;; d3-force mutates these JS objects (adds .x .y .vx .vy)
        nodes (into-array
                (mapv (fn [{:keys [id x y]}]
                        #js {:id id :x x :y y :fx x :fy y})
                      data/phantoms))
        links (into-array
                (mapv (fn [{:keys [source target]}]
                        #js {:source source :target target})
                      data/all-edges))
        sim   (-> (d3f/forceSimulation nodes)
                  (.force "link"
                    (-> (d3f/forceLink links)
                        (.id (fn [d] (.-id d)))
                        (.distance 1.5)
                        (.strength 0.1)))
                  (.force "charge"
                    (-> (d3f/forceManyBody)
                        (.strength -0.5)))
                  (.force "center"
                    (d3f/forceCenter 0 0))
                  (.force "collide"
                    (-> (d3f/forceCollide)
                        (.radius 0.8)))
                  (.alphaDecay 0.02))]
    ;; Tick: read mutated node positions, write to ratom
    (.on sim "tick"
      (fn []
        (let [positions (into {}
                          (map (fn [n]
                                 [(.-id n) {:x (.-x n) :y (.-y n)}]))
                          nodes)]
          (reset! state/!node-positions positions))))
    (reset! !simulation sim)))

(defn unpin-all!
  "Release all pinned positions — let the force simulation find equilibrium.
   Future Tier 2 feature."
  []
  (when-let [sim @!simulation]
    (doseq [n (.nodes sim)]
      (set! (.-fx n) nil)
      (set! (.-fy n) nil))
    (.alpha sim 0.3)
    (.restart sim)))

(defn stop!
  "Stop the simulation."
  []
  (when-let [sim @!simulation]
    (.stop sim)))
