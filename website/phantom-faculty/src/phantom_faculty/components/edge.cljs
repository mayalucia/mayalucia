(ns phantom-faculty.components.edge
  "Correction edge lines. Hidden by default. On hover, show only
   edges connected to the hovered node, subtly."
  (:require
    [phantom-faculty.state :as state]
    [phantom-faculty.data :as data]))

(defn correction-edge
  "Render a single correction edge. Only visible when one endpoint is hovered."
  [{:keys [source target]}]
  (let [hover   @state/!hover
        active? (or (= source hover) (= target hover))
        src-pos (state/node-position source)
        tgt-pos (state/node-position target)]
    (when active?
      [:line {:x1 (:x src-pos) :y1 (:y src-pos)
              :x2 (:x tgt-pos) :y2 (:y tgt-pos)
              :stroke data/chalk-dim
              :stroke-width 0.025
              :opacity 0.25}])))

(defn all-edges
  "Render all correction and construction edges."
  []
  [:g.edges
   (for [{:keys [source target] :as e} data/all-edges]
     ^{:key (str source "-" target)}
     [correction-edge e])])
