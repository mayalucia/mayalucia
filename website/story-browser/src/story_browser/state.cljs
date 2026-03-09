(ns story-browser.state
  (:require [reagent.core :as r]
            [story-browser.data :as data]))

;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Core ratoms
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(def !view
  "Current view: :geography or :concept"
  (r/atom :geography))

(def !hover
  "Currently hovered node — {:type :story|:concept, :id ...} or nil"
  (r/atom nil))

(def !selected
  "Currently selected story id (string) or nil"
  (r/atom nil))

(def !node-positions
  "Map of node-key → {:x :y}. Keys are story ids (strings) or
   concept ids (keywords). Updated by force simulation tick."
  (r/atom {}))

(def !zoom-transform
  "Current d3-zoom transform: {:k scale, :x tx, :y ty}"
  (r/atom {:k 1 :x 0 :y 0}))


;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Derived state
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(defn active-detail
  "The story to show in the info panel. Hover takes precedence."
  []
  (let [hover @!hover
        sel   @!selected]
    (cond
      (and hover (= (:type hover) :story))
      (get data/stories-by-id (:id hover))

      sel
      (get data/stories-by-id sel)

      (and hover (= (:type hover) :concept))
      (let [concept (get data/concepts-by-id (:id hover))]
        {:concept concept
         :stories (data/concept-stories (:id concept))})

      :else nil)))

(defn hovered-concept-stories
  "When hovering a concept node, returns set of story numbers that
   translate that concept."
  []
  (when-let [h @!hover]
    (when (= (:type h) :concept)
      (set (map :number (data/concept-stories (:id h)))))))

(defn node-visual-state
  "Returns :hovered, :connected, :dimmed, or :default for a node."
  [node-type node-id]
  (let [hover @!hover]
    (cond
      (and hover
           (= (:type hover) node-type)
           (= (:id hover) node-id))
      :hovered

      ;; When hovering a concept, stories that use it are :connected
      (and hover
           (= (:type hover) :concept)
           (= node-type :story))
      (let [stories (hovered-concept-stories)]
        (let [story (get data/stories-by-id node-id)]
          (if (contains? stories (:number story))
            :connected
            :dimmed)))

      ;; When hovering a story, concepts it uses are :connected
      (and hover
           (= (:type hover) :story)
           (= node-type :concept))
      (let [story (get data/stories-by-id (:id hover))]
        (if (some #{node-id} (:concepts story))
          :connected
          :dimmed))

      ;; When hovering a story, other stories in same region are :connected
      (and hover
           (= (:type hover) :story)
           (= node-type :story))
      (let [hover-story (get data/stories-by-id (:id hover))
            this-story  (get data/stories-by-id node-id)]
        (if (= (:region-id hover-story) (:region-id this-story))
          :connected
          :dimmed))

      ;; No hover active
      hover :dimmed
      :else :default)))


;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Navigation
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(defn switch-view! [view-key]
  (reset! !view view-key)
  (reset! !hover nil))

(defn select-story! [story-id]
  (if (= @!selected story-id)
    (reset! !selected nil)
    (reset! !selected story-id)))

(defn zoom-transform-str [{:keys [k x y]}]
  (str "translate(" x "," y ") scale(" k ")"))
