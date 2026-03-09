(ns story-browser.components.concepts
  "Concept graph view — force-directed graph of translation keys.
   Stories as larger nodes, concepts as smaller nodes, edges between them.
   Hover a concept → highlight all stories that translate it."
  (:require [reagent.core :as r]
            [story-browser.state :as state]
            [story-browser.data :as data]
            [story-browser.force :as force]
            [story-browser.components.edge :as edge]
            [story-browser.components.node :as node]
            ["d3-zoom" :as d3z]
            ["d3-selection" :as d3sel]))

(defn- attach-zoom! [svg-el]
  (let [zoom (-> (d3z/zoom)
                 (.scaleExtent #js [0.3 4])
                 (.on "zoom"
                      (fn [^js event]
                        (let [t (.-transform event)]
                          (reset! state/!zoom-transform
                                  {:k (.-k t)
                                   :x (.-x t)
                                   :y (.-y t)})))))]
    (-> (d3sel/select svg-el)
        (.call zoom))))

(defn concept-view []
  (let [svg-ref (r/atom nil)]
    (r/create-class
     {:display-name "concept-view"

      :component-did-mount
      (fn [_this]
        (force/init-simulation!)
        (when @svg-ref
          (attach-zoom! @svg-ref)))

      :component-will-unmount
      (fn [_this]
        (force/stop!))

      :reagent-render
      (fn []
        (let [transform @state/!zoom-transform]
          [:svg.concept-view
           {:ref       #(when % (reset! svg-ref %))
            :viewBox   "-400 -300 800 600"
            :width     "100%"
            :height    "100%"
            :style     {:background data/slate
                        :border-radius "4px"}}
           ;; Zoom group
           [:g {:transform (state/zoom-transform-str transform)}
            ;; Edges first (underneath)
            [edge/all-edges]
            ;; Concept nodes (smaller, behind)
            [node/all-concept-nodes]
            ;; Story nodes (larger, on top)
            [node/all-story-nodes]]]))})))
