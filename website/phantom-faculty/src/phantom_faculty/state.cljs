(ns phantom-faculty.state
  "Reactive state: ratoms for hover, zoom, node positions.
   All components read from these; force and zoom write to them."
  (:require
    [reagent.core :as r]
    [phantom-faculty.data :as data]))

;; === Node positions ==========================================================
;; Initialised from hand-tuned data. Force simulation may update these.

(defonce !node-positions
  (r/atom
    (into {} (map (fn [{:keys [id x y]}] [id {:x x :y y}]))
          data/phantoms)))

(defn node-position
  "Current position of a phantom by id."
  [id]
  (get @!node-positions id {:x 0 :y 0}))

;; === Hover state =============================================================

(defonce !hover (r/atom nil))

(defn hovered? [id] (= id @!hover))

(defn connected-to-hover?
  "Is this node directly connected to the currently hovered node?"
  [id]
  (when-let [h @!hover]
    (contains? (get data/connections h) id)))

;; === Zoom transform ==========================================================
;; Written by d3-zoom, read by the SVG zoom-group transform.

(defonce !zoom-transform (r/atom {:k 1 :x 0 :y 0}))

(defn zoom-transform-str
  "CSS transform string from zoom state."
  [{:keys [k x y]}]
  (str "translate(" x "," y ") scale(" k ")"))
