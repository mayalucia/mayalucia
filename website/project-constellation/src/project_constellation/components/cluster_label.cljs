(ns project-constellation.components.cluster-label
  "Faint, large cluster/region labels."
  (:require
    [clojure.string :as str]
    [project-constellation.data :as data]
    [project-constellation.state :as state]))

(defn cluster-label
  "Render a single cluster label."
  [{:keys [x y label cluster]}]
  (let [colour (get data/cluster-colours cluster data/chalk-dim)
        lines  (str/split label #"\n")]
    [:g.cluster-label {:key label}
     (for [[i line] (map-indexed vector lines)]
       ^{:key i}
       [:text {:x x :y (+ y (* i 0.55))
               :text-anchor "middle"
               :dominant-baseline "central"
               :fill colour
               :opacity 0.25
               :font-size "0.42px"
               :font-weight "bold"
               :font-family "serif"}
        line])]))

(defn all-cluster-labels
  "Render all cluster labels."
  []
  [:g.cluster-labels
   (for [cl (state/current-cluster-labels)]
     ^{:key (:label cl)}
     [cluster-label cl])])
