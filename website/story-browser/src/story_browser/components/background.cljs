(ns story-browser.components.background
  "Schematic background map layer for the geography view.
   Chalk-on-slate aesthetic: rivers as flowing paths, ridges as
   subtle dashed lines, passes as symbols, towns as reference dots.
   All projected through the same equirectangular projection as
   the story pins."
  (:require [clojure.string :as str]
            [story-browser.data :as data]))

;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Style constants
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(def river-opacity  0.15)
(def ridge-opacity  0.08)
(def pass-opacity   0.12)
(def town-opacity   0.10)
(def label-opacity  0.10)

;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Projection helpers
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(defn- points->svg-string
  "Convert a vector of {:lat :lon} into an SVG polyline points string."
  [coords]
  (str/join " "
    (map (fn [c]
           (let [{:keys [x y]} (data/project c)]
             (str x "," y)))
         coords)))

(defn- points->smooth-path
  "Convert a vector of {:lat :lon} into a smooth SVG path using
   quadratic Bézier curves. Gives rivers a flowing quality."
  [coords]
  (let [pts (mapv data/project coords)]
    (when (>= (count pts) 2)
      (let [first-pt (first pts)]
        (str "M" (:x first-pt) "," (:y first-pt)
             (str/join ""
               (map-indexed
                (fn [i pt]
                  (let [prev (nth pts i)]
                    (str " Q" (:x prev) "," (:y prev)
                         " " (/ (+ (:x prev) (:x pt)) 2)
                         "," (/ (+ (:y prev) (:y pt)) 2))))
                (rest pts)))
             (let [last-pt (last pts)]
               (str " L" (:x last-pt) "," (:y last-pt))))))))

;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Feature components
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(defn- river-line [{:keys [id name points]}]
  (let [path-d (points->smooth-path points)]
    (when path-d
      [:g {:key id}
       [:path {:d path-d
               :fill "none"
               :stroke data/chalk-dim
               :stroke-width 0.8
               :stroke-linecap "round"
               :stroke-linejoin "round"
               :opacity river-opacity}]
       ;; River name label near midpoint
       (let [mid-idx (quot (count points) 2)
             mid-pt  (data/project (nth points mid-idx))]
         [:text {:x (:x mid-pt)
                 :y (- (:y mid-pt) 4)
                 :text-anchor "middle"
                 :fill data/chalk-dim
                 :font-size 6
                 :font-family "serif"
                 :font-style "italic"
                 :opacity label-opacity}
          name])])))

(defn- ridge-line [{:keys [id name points]}]
  [:g {:key id}
   [:polyline {:points (points->svg-string points)
               :fill "none"
               :stroke data/chalk-dim
               :stroke-width 0.5
               :stroke-dasharray "2,3"
               :stroke-linecap "round"
               :opacity ridge-opacity}]
   ;; Ridge name near midpoint
   (let [mid-idx (quot (count points) 2)
         label-pt (data/project (nth points mid-idx))]
     [:text {:x (:x label-pt)
             :y (- (:y label-pt) 3)
             :text-anchor "middle"
             :fill data/chalk-dim
             :font-size 5
             :font-family "serif"
             :font-style "italic"
             :opacity (* label-opacity 0.7)}
      name])])

(defn- pass-marker [{:keys [id name geo]}]
  (let [{:keys [x y]} (data/project geo)]
    [:g {:key id}
     ;; Small × symbol
     [:line {:x1 (- x 3) :y1 (- y 3)
             :x2 (+ x 3) :y2 (+ y 3)
             :stroke data/chalk-dim
             :stroke-width 0.5
             :opacity pass-opacity}]
     [:line {:x1 (+ x 3) :y1 (- y 3)
             :x2 (- x 3) :y2 (+ y 3)
             :stroke data/chalk-dim
             :stroke-width 0.5
             :opacity pass-opacity}]
     [:text {:x (+ x 5) :y (+ y 1)
             :text-anchor "start"
             :fill data/chalk-dim
             :font-size 5.5
             :font-family "serif"
             :opacity pass-opacity}
      name]]))

(defn- town-dot [{:keys [id name geo]}]
  (let [{:keys [x y]} (data/project geo)]
    [:g {:key id}
     [:circle {:cx x :cy y :r 1.5
               :fill data/chalk-dim
               :opacity town-opacity}]
     [:text {:x (+ x 4) :y (+ y 1)
             :text-anchor "start"
             :fill data/chalk-dim
             :font-size 5
             :font-family "serif"
             :opacity town-opacity}
      name]]))

;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Public component
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(defn background-map
  "SVG group containing all background geographic features.
   Rendered behind story pins, inside the zoom group."
  []
  [:g.background-map
   ;; Ridges first (most receding)
   [:g.ridges
    (for [r data/ridges]
      ^{:key (:id r)}
      [ridge-line r])]
   ;; Rivers (slightly more visible)
   [:g.rivers
    (for [r data/rivers]
      ^{:key (:id r)}
      [river-line r])]
   ;; Passes
   [:g.passes
    (for [p data/passes]
      ^{:key (:id p)}
      [pass-marker p])]
   ;; Towns
   [:g.towns
    (for [t data/towns]
      ^{:key (:id t)}
      [town-dot t])]])
