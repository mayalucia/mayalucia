(ns phantom-faculty.components.constellation
  "Root component: two-column layout — SVG constellation (left) + info panel (right)."
  (:require
    [reagent.core :as r]
    [phantom-faculty.state :as state]
    [phantom-faculty.data :as data]
    [phantom-faculty.force :as force]
    [phantom-faculty.components.background :as background]
    [phantom-faculty.components.cluster-label :as cluster-label]
    [phantom-faculty.components.edge :as edge]
    [phantom-faculty.components.node :as node]
    [phantom-faculty.components.tooltip :as tooltip]
    ["d3-zoom" :as d3z]
    ["d3-selection" :as d3sel]))

(defn- attach-zoom!
  "Attach d3-zoom behaviour to the SVG element.
   Writes zoom transform to the ratom; Reagent re-renders."
  [svg-el]
  (try
    (let [zoom-behaviour
          (-> (d3z/zoom)
              (.scaleExtent #js [0.5 5])
              (.on "zoom"
                (fn [event]
                  (let [t (.-transform event)]
                    (reset! state/!zoom-transform
                      {:k (.-k t)
                       :x (.-x t)
                       :y (.-y t)})))))]
      (-> (d3sel/select svg-el)
          (.call zoom-behaviour)))
    (catch js/Error e
      (js/console.error "phantom-faculty: zoom init failed" e))))

(defn root
  "Top-level constellation component: two-column layout."
  []
  (let [svg-ref (r/atom nil)]
    (r/create-class
      {:display-name "phantom-constellation"

       :component-did-mount
       (fn [_this]
         (js/console.log "phantom-faculty: component mounted, svg-ref:" (boolean @svg-ref))
         (try
           (when @svg-ref
             (attach-zoom! @svg-ref))
           (force/init-simulation!)
           (catch js/Error e
             (js/console.error "phantom-faculty: mount failed" e))))

       :component-will-unmount
       (fn [_this]
         (force/stop!))

       :reagent-render
       (fn []
         [:div.phantom-constellation
          {:style {:display "grid"
                   :grid-template-columns "1fr 240px"
                   :gap "0"
                   :background data/slate}}

          ;; Left column: the constellation SVG
          [:div.constellation-left
           {:style {:position "relative"
                    :overflow "hidden"}}
           [:svg.constellation-svg
            {:ref       #(reset! svg-ref %)
             :viewBox   "-8.5 -6.5 17 13"
             :preserveAspectRatio "xMidYMid meet"
             :xmlns     "http://www.w3.org/2000/svg"
             :style     {:width "100%" :height "100%"
                         :display "block"}}

            ;; Background dust
            [background/chalk-dust]

            ;; Zoom group
            [:g.zoom-group
             {:transform (state/zoom-transform-str @state/!zoom-transform)}

             [cluster-label/all-cluster-labels]
             [edge/all-edges]
             [node/all-nodes]]]]

          ;; Right column: info panel
          [tooltip/info-panel]

          ;; noscript fallback (spans both columns)
          [:noscript
           {:style {:grid-column "1 / -1"}}
           [:img {:src "/images/writing/phantom-faculty/the-faculty-assembled.png"
                  :alt "The Phantom Faculty constellation"
                  :loading "lazy"}]]])})))
