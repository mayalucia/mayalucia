(ns project-constellation.components.edge
  "Multi-type edge renderer. Different visual styles per edge type.
   Cycle-flow and refine-arc edges are always visible.
   Other edges appear on hover."
  (:require
    [project-constellation.state :as state]
    [project-constellation.data :as data]))

(defn- refine-arc-path
  "SVG path from source to target, curving outward from origin."
  [src-pos tgt-pos]
  (let [mx (/ (+ (:x src-pos) (:x tgt-pos)) 2)
        my (/ (+ (:y src-pos) (:y tgt-pos)) 2)
        dist (js/Math.sqrt (+ (* mx mx) (* my my)))
        factor (if (pos? dist) (/ 2.0 dist) 1.0)
        cx (* mx (+ 1.0 factor))
        cy (* my (+ 1.0 factor))]
    (str "M" (:x src-pos) "," (:y src-pos)
         " Q" cx "," cy
         " " (:x tgt-pos) "," (:y tgt-pos))))

(defn- slightly-curved-path
  "SVG path from source to target with a gentle curve."
  [src-pos tgt-pos]
  (let [mx (/ (+ (:x src-pos) (:x tgt-pos)) 2)
        my (/ (+ (:y src-pos) (:y tgt-pos)) 2)
        ;; Perpendicular offset for gentle curve
        dx (- (:x tgt-pos) (:x src-pos))
        dy (- (:y tgt-pos) (:y src-pos))
        cx (- mx (* 0.15 dy))
        cy (+ my (* 0.15 dx))]
    (str "M" (:x src-pos) "," (:y src-pos)
         " Q" cx "," cy
         " " (:x tgt-pos) "," (:y tgt-pos))))

(defn entity-edge
  "Render a single edge. Visibility and style depend on :type."
  [{:keys [source target type]}]
  (let [hover   @state/!hover
        focus   (or hover @state/!selected)
        active? (or (= source focus) (= target focus))
        src-pos (state/node-position source)
        tgt-pos (state/node-position target)
        always? (contains? #{:cycle-flow :refine-arc :thread-touches} type)]
    (cond
      ;; Cycle-flow: always visible, thick, with arrowhead
      (= type :cycle-flow)
      [:path {:d (slightly-curved-path src-pos tgt-pos)
              :stroke data/chalk-dim
              :stroke-width 0.05
              :fill "none"
              :opacity (if active? 0.5 0.25)
              :marker-end "url(#arrow)"}]

      ;; Refine-arc: always visible, dashed, curved outward
      (= type :refine-arc)
      [:path {:d (refine-arc-path src-pos tgt-pos)
              :stroke data/chalk-dim
              :stroke-width 0.03
              :fill "none"
              :opacity (if active? 0.4 0.15)
              :stroke-dasharray "0.15 0.08"}]

      ;; Thread-touches: visible when thread is active
      (= type :thread-touches)
      (let [src-entity (get data/entities-by-id source)]
        ;; Note: entities-by-id still used for lookup — it includes all levels
        (when (= :active (:status src-entity))
          [:line {:x1 (:x src-pos) :y1 (:y src-pos)
                  :x2 (:x tgt-pos) :y2 (:y tgt-pos)
                  :stroke (get data/cluster-colours "thread" data/chalk-dim)
                  :stroke-width 0.02
                  :opacity (if active? 0.5 0.2)
                  :stroke-dasharray "0.08 0.05"}]))

      ;; Serves, depends, embodies: only on hover
      active?
      (let [style (case type
                    :serves   {:width 0.025 :opacity 0.3 :dash nil}
                    :depends  {:width 0.025 :opacity 0.3 :dash "0.04 0.04"}
                    :embodies {:width 0.02  :opacity 0.2 :dash nil}
                    {:width 0.025 :opacity 0.25 :dash nil})]
        [:line {:x1 (:x src-pos) :y1 (:y src-pos)
                :x2 (:x tgt-pos) :y2 (:y tgt-pos)
                :stroke data/chalk-dim
                :stroke-width (:width style)
                :opacity (:opacity style)
                :stroke-dasharray (:dash style)}])

      :else nil)))

(defn all-edges
  "Render all edges."
  []
  [:g.edges
   (for [{:keys [source target] :as e} (state/current-edges)]
     ^{:key (str source "-" target)}
     [entity-edge e])])
