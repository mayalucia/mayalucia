(ns story-browser.components.geography
  "Geography view — schematic SVG map of the Western Himalaya.
   Stories rendered as pins at their real geographic locations.
   Projection shared with background via data/project."
  (:require [clojure.string :as str]
            [reagent.core :as r]
            [story-browser.state :as state]
            [story-browser.data :as data]
            [story-browser.components.background :as background]
            ["d3-zoom" :as d3z]
            ["d3-selection" :as d3sel]))

;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Story positions — with collision avoidance
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(defn story-position
  "Project a story's geo coordinates into SVG space.
   Abstract stories (no geo) go to the top-left margin."
  [story]
  (if-let [geo (:geo story)]
    (data/project geo)
    {:x 60 :y 40}))

(def ^:private pin-min-distance 24)

(defn- spread-overlapping
  "Iterative force-push to separate overlapping pins.
   Input: vector of {:id :x :y}. Returns same with adjusted positions."
  [pins iterations]
  (loop [ps (vec pins)
         i  0]
    (if (>= i iterations)
      ps
      (recur
       (reduce
        (fn [acc idx]
          (reduce
           (fn [acc2 jdx]
             (if (= idx jdx)
               acc2
               (let [a  (nth acc2 idx)
                     b  (nth acc2 jdx)
                     dx (- (:x a) (:x b))
                     dy (- (:y a) (:y b))
                     dist (js/Math.sqrt (+ (* dx dx) (* dy dy)))]
                 (if (< dist pin-min-distance)
                   (let [overlap (/ (- pin-min-distance dist) 2)
                         angle   (if (zero? dist)
                                   (* idx 0.5)
                                   (js/Math.atan2 dy dx))
                         px (* overlap (js/Math.cos angle))
                         py (* overlap (js/Math.sin angle))]
                     (-> acc2
                         (update-in [idx :x] + px)
                         (update-in [idx :y] + py)
                         (update-in [jdx :x] - px)
                         (update-in [jdx :y] - py)))
                   acc2))))
           acc
           (range (count acc))))
        ps
        (range (count ps)))
       (inc i)))))

(def spread-positions
  "Pre-computed spread positions for story pins. Map of story-id → {:x :y}."
  (let [raw    (mapv (fn [s] (merge {:id (:id s)} (story-position s)))
                     data/stories)
        spread (spread-overlapping raw 12)]
    (into {} (map (fn [{:keys [id x y]}] [id {:x x :y y}]) spread))))

(defn- pin-position
  "Look up the spread-adjusted position for a story."
  [story]
  (get spread-positions (:id story) (story-position story)))


;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Components
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(defn- region-label [region]
  (when-let [geo (:geo region)]
    (let [pos    (data/project geo)
          colour (get data/region-colours (:id region) "#808080")]
      [:text {:x (:x pos)
              :y (- (:y pos) 25)
              :text-anchor "middle"
              :fill colour
              :font-size 11
              :font-weight "bold"
              :font-family "serif"
              :opacity 0.4}
       (:name region)])))

(defn- story-pin [story]
  (let [pos     (pin-position story)
        colour  (data/story-colour story)
        vs      (state/node-visual-state :story (:id story))
        opacity (case vs
                  :hovered   1.0
                  :connected 0.85
                  :dimmed    0.15
                  :default   0.7)]
    [:g.story-pin
     {:transform (str "translate(" (:x pos) "," (:y pos) ")")
      :style     {:cursor "pointer"
                  :transition "opacity 0.2s"}
      :opacity   opacity
      :on-mouse-enter #(reset! state/!hover {:type :story :id (:id story)})
      :on-mouse-leave #(reset! state/!hover nil)
      :on-click       #(state/select-story! (:id story))}
     ;; Pin drop shadow
     [:circle {:r 10 :fill colour :opacity 0.2 :cy 2}]
     ;; Pin circle
     [:circle {:r 8 :fill colour
               :stroke "rgba(255,255,255,0.3)" :stroke-width 1}]
     ;; Story number
     [:text {:text-anchor "middle"
             :dominant-baseline "central"
             :fill "white"
             :font-size 8
             :font-weight "bold"
             :font-family "serif"
             :pointer-events "none"}
      (str (:number story))]]))

(defn- thread-walker-path
  "Draw the Thread Walker's route connecting her stories."
  []
  (let [tw-stories (sort-by :number
                    (filter (fn [s] (some #{"thread-walker"} (:characters s)))
                            data/stories))
        positions  (map pin-position tw-stories)]
    (when (> (count positions) 1)
      [:polyline
       {:points (str/join " "
                 (map (fn [{:keys [x y]}] (str x "," y)) positions))
        :fill "none"
        :stroke data/chalk-dim
        :stroke-width 1
        :stroke-dasharray "4,4"
        :opacity 0.25}])))

;; karakoram-territory placeholder removed — Karakoram now has stories

(defn- abstract-zone
  "Small label for the Abstract region (Phantom Faculty)."
  []
  [:text {:x 60 :y 28
          :text-anchor "middle"
          :fill (get data/region-colours "abstract")
          :font-size 9
          :font-style "italic"
          :font-family "serif"
          :opacity 0.3}
   "Abstract"])

(defn- attach-zoom! [svg-el]
  (let [zoom (-> (d3z/zoom)
                 (.scaleExtent #js [0.5 5])
                 (.on "zoom"
                      (fn [^js event]
                        (let [t (.-transform event)]
                          (reset! state/!zoom-transform
                                  {:k (.-k t)
                                   :x (.-x t)
                                   :y (.-y t)})))))]
    (-> (d3sel/select svg-el)
        (.call zoom))))

(defn geography-view []
  (let [svg-ref (r/atom nil)]
    (r/create-class
     {:display-name "geography-view"

      :component-did-mount
      (fn [_this]
        (when @svg-ref
          (attach-zoom! @svg-ref)))

      :reagent-render
      (fn []
        (let [transform @state/!zoom-transform]
          [:svg.geography-view
           {:ref       #(when % (reset! svg-ref %))
            :viewBox   (str "0 0 " data/svg-w " " data/svg-h)
            :width     "100%"
            :height    "100%"
            :style     {:background data/slate
                        :border-radius "4px"}}
           ;; Zoom group
           [:g {:transform (state/zoom-transform-str transform)}
            ;; Background map — rivers, ridges, passes, towns (most receding)
            [background/background-map]
            ;; Region labels
            (for [region data/regions]
              ^{:key (:id region)}
              [region-label region])
            ;; Abstract zone label
            [abstract-zone]
            ;; Thread Walker's path
            [thread-walker-path]
            ;; (karakoram-territory placeholder removed)
            ;; Story pins (on top)
            (for [s data/stories]
              ^{:key (:id s)}
              [story-pin s])]]))})))
