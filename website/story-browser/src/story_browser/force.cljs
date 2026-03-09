(ns story-browser.force
  "D3 force simulation for the concept graph view.
   Forked from project-constellation/force.cljs — same pattern:
   D3 owns the math, Reagent owns the DOM."
  (:require [story-browser.state :as state]
            [story-browser.data :as data]
            ["d3-force" :as d3f]))

(defonce !simulation (atom nil))

;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Force parameters
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(def story-charge  -80)
(def concept-charge -30)
(def link-distance   60)
(def link-strength    0.15)
(def collision-radius 20)

;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Build simulation nodes and links from stories.edn
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(defn build-nodes
  "Create nodes for concepts and stories. Each node has:
   :node-id, :node-type (:story|:concept), :label"
  []
  (let [concept-nodes
        (mapv (fn [c]
                #js {:id       (str "c:" (name (:id c)))
                     :nodeId   (:id c)
                     :nodeType "concept"
                     :label    (:name c)
                     :storyNum (:introduced-in c)})
              data/concepts)
        story-nodes
        (mapv (fn [s]
                #js {:id       (str "s:" (:id s))
                     :nodeId   (:id s)
                     :nodeType "story"
                     :label    (:title s)
                     :storyNum (:number s)})
              data/stories)]
    (into-array (concat concept-nodes story-nodes))))

(defn build-links
  "Create links: story→concept for each concept a story uses.
   Also concept-bridge and concept-lineage edges."
  []
  (let [story-concept-links
        (for [s data/stories
              c (:concepts s)]
          #js {:source (str "s:" (:id s))
               :target (str "c:" (name c))
               :type   "story-concept"})
        bridge-links
        (for [e data/edges
              :when (= (:type e) :concept)
              :let [[c1 c2] (:link e)]]
          #js {:source (str "c:" (name c1))
               :target (str "c:" (name c2))
               :type   "concept-bridge"})
        lineage-links
        (for [e data/edges
              :when (= (:type e) :concept-lineage)
              :let [concept-key (str "c:" (name (:concept e)))]
              s (:stories e)]
          #js {:source concept-key
               :target (str "s:" (:id (get data/stories-by-number s)))
               :type   "concept-lineage"})]
    (into-array (concat story-concept-links bridge-links lineage-links))))

;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Simulation lifecycle
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(defn- update-positions!
  "Read node positions from the simulation and write to ratom."
  []
  (when-let [sim @!simulation]
    (let [nodes (.nodes sim)
          pos   (reduce
                 (fn [m ^js node]
                   (let [nid (.-nodeId node)]
                     (assoc m nid {:x (.-x node) :y (.-y node)})))
                 {}
                 nodes)]
      (reset! state/!node-positions pos))))

(defn init-simulation!
  "Create a fresh D3 force simulation for the concept graph."
  []
  (when-let [old @!simulation] (.stop old))
  (let [nodes (build-nodes)
        links (build-links)
        sim   (-> (d3f/forceSimulation nodes)
                  (.force "link"
                          (-> (d3f/forceLink links)
                              (.id (fn [d] (.-id d)))
                              (.distance link-distance)
                              (.strength link-strength)))
                  (.force "charge"
                          (-> (d3f/forceManyBody)
                              (.strength
                               (fn [^js d]
                                 (if (= (.-nodeType d) "story")
                                   story-charge
                                   concept-charge)))))
                  (.force "center" (d3f/forceCenter 0 0))
                  (.force "collide"
                          (-> (d3f/forceCollide)
                              (.radius collision-radius)))
                  (.alphaDecay 0.02))]
    (reset! !simulation sim)
    (.on sim "tick" update-positions!)
    sim))

(defn stop! []
  (when-let [sim @!simulation]
    (.stop sim)
    (reset! !simulation nil)))
