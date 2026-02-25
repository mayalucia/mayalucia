(ns project-constellation.state
  "Reactive state: ratoms for view, hover, selected, zoom, node positions.
   View-aware accessors route to root or child data depending on !view."
  (:require
    [reagent.core :as r]
    [project-constellation.data :as data]))

;; === View navigation ==========================================================
;; :level is :root or :child. When :child, :id and :name identify the parent.

(defonce !view (r/atom {:level :root}))

(defn at-root? [] (= :root (:level @!view)))

(defn current-entities
  "Entities for the current view level."
  []
  (if (at-root?)
    data/entities
    (get-in data/entities-by-id [(:id @!view) :children :entities])))

(defn current-edges
  "Edges for the current view level."
  []
  (if (at-root?)
    data/edges
    (get-in data/entities-by-id [(:id @!view) :children :edges])))

(defn current-cluster-labels
  "Cluster labels for the current view level."
  []
  (if (at-root?)
    data/cluster-labels
    (get-in data/entities-by-id [(:id @!view) :children :cluster-labels])))

(defn current-connections
  "Connection index for the current view level."
  []
  (let [edges (current-edges)]
    (reduce (fn [m {:keys [source target]}]
              (-> m
                  (update source (fnil conj #{}) target)
                  (update target (fnil conj #{}) source)))
            {}
            edges)))

;; === Node positions ==========================================================

(defonce !node-positions
  (r/atom
    (into {} (map (fn [{:keys [id x y]}] [id {:x x :y y}]))
          data/entities)))

(defn node-position
  "Current position of an entity by id."
  [id]
  (get @!node-positions id {:x 0 :y 0}))

(defn reset-positions!
  "Reset node positions from a vector of entities."
  [entities]
  (reset! !node-positions
    (into {} (map (fn [{:keys [id x y]}] [id {:x x :y y}]))
          entities)))

;; === Hover state =============================================================

(defonce !hover (r/atom nil))

(defn hovered? [id] (= id @!hover))

(defn connected-to-hover?
  "Is this node directly connected to the currently hovered node?"
  [id]
  (when-let [h @!hover]
    (contains? (get (current-connections) h) id)))

;; === Selected state ==========================================================

(defonce !selected (r/atom nil))

(defn active-detail-id
  "Which entity to show in the info panel. Hover takes precedence over selected."
  []
  (or @!hover @!selected))

(defn node-visual-state
  "Returns :hovered, :connected, :dimmed, or :default for a given node id."
  [id]
  (let [focus (or @!hover @!selected)]
    (cond
      (nil? focus)                                             :default
      (= id focus)                                             :hovered
      (contains? (get (current-connections) focus #{}) id)      :connected
      :else                                                    :dimmed)))

;; === Zoom transform ==========================================================

(defonce !zoom-transform (r/atom {:k 1 :x 0 :y 0}))

(defn zoom-transform-str
  "CSS transform string from zoom state."
  [{:keys [k x y]}]
  (str "translate(" x "," y ") scale(" k ")"))

;; === View transitions ========================================================

(defn drill-down!
  "Transition to a child view. Resets interaction state."
  [id name]
  (reset! !view {:level :child :id id :name name})
  (reset! !hover nil)
  (reset! !selected nil)
  (reset! !zoom-transform {:k 1 :x 0 :y 0})
  (let [children (get-in data/entities-by-id [id :children :entities])]
    (when children
      (reset-positions! children))))

(defn navigate-up!
  "Return to root view. Resets interaction state."
  []
  (reset! !view {:level :root})
  (reset! !hover nil)
  (reset! !selected nil)
  (reset! !zoom-transform {:k 1 :x 0 :y 0})
  (reset-positions! data/entities))
