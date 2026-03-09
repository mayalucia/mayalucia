(ns story-browser.components.edge
  "Edge rendering for concept view.
   Forked from project-constellation edge.cljs — adapted for
   story↔concept, concept-bridge, and concept-lineage edge types."
  (:require [story-browser.state :as state]
            [story-browser.data :as data]))

(defn- slightly-curved-path
  "Gentle Bézier curve between two points."
  [x1 y1 x2 y2]
  (let [mx (/ (+ x1 x2) 2)
        my (/ (+ y1 y2) 2)
        dx (- x2 x1)
        dy (- y2 y1)
        ;; Perpendicular offset for gentle curve
        ox (* -0.1 dy)
        oy (* 0.1 dx)]
    (str "M" x1 "," y1
         " Q" (+ mx ox) "," (+ my oy)
         " " x2 "," y2)))

(def edge-styles
  {:story-concept   {:stroke-width 0.8
                     :stroke-dasharray nil
                     :base-opacity 0.08
                     :hover-opacity 0.35}
   :concept-bridge  {:stroke-width 1.2
                     :stroke-dasharray "4,3"
                     :base-opacity 0.15
                     :hover-opacity 0.5}
   :concept-lineage {:stroke-width 1.0
                     :stroke-dasharray "8,4"
                     :base-opacity 0.12
                     :hover-opacity 0.45}})

(defn concept-edge
  "Render a single edge in the concept graph."
  [{:keys [source target edge-type]}]
  (let [positions @state/!node-positions
        src-pos   (get positions source)
        tgt-pos   (get positions target)
        hover     @state/!hover
        style     (get edge-styles edge-type (:story-concept edge-styles))
        ;; Show brighter if either endpoint is hovered
        active?   (and hover
                       (or (= (:id hover) source)
                           (= (:id hover) target)))
        opacity   (if active?
                    (:hover-opacity style)
                    (:base-opacity style))]
    (when (and src-pos tgt-pos)
      [:path
       {:d (slightly-curved-path
            (:x src-pos) (:y src-pos)
            (:x tgt-pos) (:y tgt-pos))
        :stroke data/chalk-dim
        :stroke-width (:stroke-width style)
        :stroke-dasharray (:stroke-dasharray style)
        :fill "none"
        :opacity opacity
        :style {:transition "opacity 0.2s"}}])))

(defn all-edges
  "Render all edges for the concept graph view."
  []
  (let [story-concept-edges
        (for [s data/stories
              c (:concepts s)]
          {:source (:id s)
           :target c
           :edge-type :story-concept})
        bridge-edges
        (for [e data/edges
              :when (= (:type e) :concept)
              :let [[c1 c2] (:link e)]]
          {:source c1
           :target c2
           :edge-type :concept-bridge})
        lineage-edges
        (for [e data/edges
              :when (= (:type e) :concept-lineage)
              :let [concept (:concept e)]
              s (:stories e)]
          {:source concept
           :target (:id (get data/stories-by-number s))
           :edge-type :concept-lineage})]
    [:g.edges
     (for [[i edge] (map-indexed vector
                      (concat story-concept-edges
                              bridge-edges
                              lineage-edges))]
       ^{:key (str "edge-" i)}
       [concept-edge edge])]))
