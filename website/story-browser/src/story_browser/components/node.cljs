(ns story-browser.components.node
  "Node rendering for both views.
   Story nodes: circles coloured by region.
   Concept nodes: smaller circles with text labels."
  (:require [story-browser.state :as state]
            [story-browser.data :as data]))

(def story-radius 12)
(def concept-radius 6)

(defn- opacity-for-state [visual-state]
  (case visual-state
    :hovered   1.0
    :connected 0.85
    :dimmed    0.15
    :default   0.7))

(defn- scale-for-state [visual-state]
  (case visual-state
    :hovered   1.15
    :connected 1.0
    :dimmed    0.9
    :default   1.0))

(defn story-node
  "Render a story as a circle with number label."
  [story]
  (let [positions @state/!node-positions
        pos       (get positions (:id story))
        vs        (state/node-visual-state :story (:id story))
        colour    (data/story-colour story)
        opacity   (opacity-for-state vs)
        scale     (scale-for-state vs)]
    (when pos
      [:g.story-node
       {:transform (str "translate(" (:x pos) "," (:y pos) ")"
                        " scale(" scale ")")
        :style     {:cursor "pointer"
                    :transition "opacity 0.2s, transform 0.2s"}
        :opacity   opacity
        :on-mouse-enter #(reset! state/!hover {:type :story :id (:id story)})
        :on-mouse-leave #(reset! state/!hover nil)
        :on-click       #(state/select-story! (:id story))}
       ;; Outer glow
       [:circle {:r (* story-radius 1.4)
                 :fill colour
                 :opacity 0.15}]
       ;; Main circle
       [:circle {:r story-radius
                 :fill colour
                 :stroke "rgba(255,255,255,0.3)"
                 :stroke-width 1}]
       ;; Story number
       [:text {:text-anchor "middle"
               :dominant-baseline "central"
               :fill "white"
               :font-size 9
               :font-weight "bold"
               :font-family "serif"
               :pointer-events "none"}
        (str (:number story))]])))

(defn concept-node
  "Render a concept as a small circle with label."
  [concept]
  (let [positions @state/!node-positions
        pos       (get positions (:id concept))
        vs        (state/node-visual-state :concept (:id concept))
        colour    (data/concept-colour concept)
        opacity   (opacity-for-state vs)
        scale     (scale-for-state vs)]
    (when pos
      [:g.concept-node
       {:transform (str "translate(" (:x pos) "," (:y pos) ")"
                        " scale(" scale ")")
        :style     {:cursor "pointer"
                    :transition "opacity 0.2s, transform 0.2s"}
        :opacity   opacity
        :on-mouse-enter #(reset! state/!hover {:type :concept :id (:id concept)})
        :on-mouse-leave #(reset! state/!hover nil)}
       ;; Main circle
       [:circle {:r concept-radius
                 :fill colour
                 :opacity 0.6
                 :stroke colour
                 :stroke-width 0.5
                 :stroke-opacity 0.3}]
       ;; Label (offset below)
       [:text {:y (+ concept-radius 10)
               :text-anchor "middle"
               :fill data/chalk-dim
               :font-size 7
               :font-family "serif"
               :pointer-events "none"
               :opacity (if (= vs :hovered) 1.0 0.5)}
        (:name concept)]])))

(defn all-story-nodes []
  [:g.story-nodes
   (for [s data/stories]
     ^{:key (:id s)}
     [story-node s])])

(defn all-concept-nodes []
  [:g.concept-nodes
   (for [c data/concepts]
     ^{:key (name (:id c))}
     [concept-node c])])
