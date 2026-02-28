(ns project-constellation.components.constellation
  "Root component: two-column layout — SVG constellation (left) + info panel (right)."
  (:require
    [reagent.core :as r]
    [project-constellation.state :as state]
    [project-constellation.data :as data]
    [project-constellation.force :as force]
    [project-constellation.components.background :as background]
    [project-constellation.components.cluster-label :as cluster-label]
    [project-constellation.components.edge :as edge]
    [project-constellation.components.node :as node]
    [project-constellation.components.tooltip :as tooltip]
    ["d3-zoom" :as d3z]
    ["d3-selection" :as d3sel]))

(defn- attach-zoom!
  "Attach d3-zoom behaviour to the SVG element."
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
      (js/console.error "project-constellation: zoom init failed" e))))

(defn root
  "Top-level constellation component: two-column layout."
  []
  (let [svg-ref (r/atom nil)]
    (r/create-class
      {:display-name "project-constellation"

       :component-did-mount
       (fn [_this]
         (js/console.log "project-constellation: component mounted")
         (try
           (when @svg-ref
             (attach-zoom! @svg-ref))
           (force/init-simulation! (state/current-entities) (state/current-edges))
           ;; Watch for view changes to restart simulation
           (add-watch state/!view ::view-change
             (fn [_ _ old-v new-v]
               (when (not= (:level old-v) (:level new-v))
                 (js/setTimeout
                   #(force/restart-with!
                      (state/current-entities) (state/current-edges))
                   50))))
           (catch js/Error e
             (js/console.error "project-constellation: mount failed" e))))

       :component-will-unmount
       (fn [_this]
         (remove-watch state/!view ::view-change)
         (force/stop!))

       :reagent-render
       (fn []
         [:div.project-constellation
          {:style {:background data/slate}
           :on-click (fn [e]
                       ;; Click on background clears selection
                       (when (= (.-target e) (.-currentTarget e))
                         (reset! state/!selected nil)))}

          ;; Left column: the constellation SVG + breadcrumb
          [:div.constellation-left
           {:style {:position "relative"
                    :overflow "hidden"}}

           ;; Breadcrumb overlay
           (when-not (state/at-root?)
             [:div {:style {:position "absolute"
                            :top "8px" :left "12px"
                            :z-index 10
                            :font-family "Georgia, serif"
                            :font-size "13px"
                            :pointer-events "auto"}}
              [:span {:style {:color data/chalk-dim
                              :cursor "pointer"
                              :opacity 0.7}
                      :on-mouse-over #(set! (.. % -target -style -opacity) "1.0")
                      :on-mouse-out  #(set! (.. % -target -style -opacity) "0.7")
                      :on-click (fn [e]
                                  (.stopPropagation e)
                                  (state/navigate-up!))}
               "MāyāLucIA"]
              [:span {:style {:color data/chalk-dim :opacity 0.4
                              :margin "0 6px"}} "\u203A"]
              [:span {:style {:color (get data/entity-colours
                                         (:id @state/!view) data/chalk)}}
               (:name @state/!view)]])

           [:svg.constellation-svg
            {:ref       #(reset! svg-ref %)
             :viewBox   "-7 -6 14 12"
             :preserveAspectRatio "xMidYMid meet"
             :xmlns     "http://www.w3.org/2000/svg"
             :style     {:width "100%" :height "100%"
                         :display "block"}
             :on-click  (fn [e]
                          ;; Click on SVG background clears selection
                          (when (= "svg" (.. e -target -tagName))
                            (reset! state/!selected nil)))}

            ;; SVG defs: arrowheads, phase sphere gradients, drop shadow
            [:defs
             [:marker {:id "arrow" :markerWidth "6" :markerHeight "4"
                       :refX "5" :refY "2" :orient "auto"
                       :markerUnits "strokeWidth"}
              [:path {:d "M0,0 L6,2 L0,4" :fill data/chalk-dim}]]

             ;; Drop shadow for phase crystals
             [:filter {:id "phase-shadow" :x "-50%" :y "-50%"
                       :width "200%" :height "200%"}
              [:feGaussianBlur {:in "SourceAlpha" :stdDeviation "0.08"
                                :result "blur"}]
              [:feOffset {:in "blur" :dx "0.03" :dy "0.06"
                          :result "shadow"}]
              [:feFlood {:flood-color "#000" :flood-opacity "0.4"
                         :result "color"}]
              [:feComposite {:in "color" :in2 "shadow"
                             :operator "in" :result "colorShadow"}]
              [:feMerge
               [:feMergeNode {:in "colorShadow"}]
               [:feMergeNode {:in "SourceGraphic"}]]]

             ;; Subtle inner glow filter for crystal edges
             [:filter {:id "crystal-glow" :x "-30%" :y "-30%"
                       :width "160%" :height "160%"}
              [:feGaussianBlur {:in "SourceGraphic" :stdDeviation "0.04"
                                :result "glow"}]
              [:feMerge
               [:feMergeNode {:in "glow"}]
               [:feMergeNode {:in "SourceGraphic"}]]]

             ;; Linear gradients for crystal facets: light/mid/dark per phase
             ;; Light source: upper-left → top facet brightest, right darkest
             (for [[phase-id base-hex]
                   [["measure"  "#d4a574"]
                    ["model"    "#7eb8da"]
                    ["manifest" "#c4836a"]
                    ["evaluate" "#a8d4a0"]]]
               ^{:key (str "crystal-grads-" phase-id)}
               [:<>
                ;; Top/lit facet — brightest, gradient from white highlight to base
                [:linearGradient {:id (str "crystal-top-" phase-id)
                                  :x1 "0.2" :y1 "0" :x2 "0.8" :y2 "1"}
                 [:stop {:offset "0%"   :stop-color "#ffffff" :stop-opacity "0.7"}]
                 [:stop {:offset "50%"  :stop-color base-hex  :stop-opacity "0.95"}]
                 [:stop {:offset "100%" :stop-color base-hex  :stop-opacity "0.85"}]]
                ;; Left facet — medium, slight highlight at top
                [:linearGradient {:id (str "crystal-left-" phase-id)
                                  :x1 "0" :y1 "0" :x2 "1" :y2 "1"}
                 [:stop {:offset "0%"   :stop-color base-hex  :stop-opacity "0.85"}]
                 [:stop {:offset "100%" :stop-color "#1a1a2e" :stop-opacity "0.5"}]]
                ;; Right facet — darkest, in shadow
                [:linearGradient {:id (str "crystal-right-" phase-id)
                                  :x1 "1" :y1 "0" :x2 "0" :y2 "1"}
                 [:stop {:offset "0%"   :stop-color base-hex  :stop-opacity "0.6"}]
                 [:stop {:offset "100%" :stop-color "#0a0a16" :stop-opacity "0.7"}]]])

             ;; Diamond ambient glow — soft radial blend
             [:radialGradient {:id "diamond-glow" :cx "0.5" :cy "0.5" :r "0.5"}
              [:stop {:offset "0%"   :stop-color "#e8e4d4" :stop-opacity "0.6"}]
              [:stop {:offset "40%"  :stop-color "#c4a87e" :stop-opacity "0.3"}]
              [:stop {:offset "100%" :stop-color "#12121e" :stop-opacity "0.0"}]]

             ;; Diamond table — central octagon fill
             [:radialGradient {:id "diamond-table" :cx "0.5" :cy "0.5" :r "0.5"}
              [:stop {:offset "0%"   :stop-color "#e8e4d4" :stop-opacity "0.15"}]
              [:stop {:offset "60%"  :stop-color "#8a8678" :stop-opacity "0.10"}]
              [:stop {:offset "100%" :stop-color "#12121e" :stop-opacity "0.05"}]]]

            ;; Background dust
            [background/chalk-dust]

            ;; Zoom group
            [:g.zoom-group
             {:transform (state/zoom-transform-str @state/!zoom-transform)}

             [cluster-label/all-cluster-labels]
             [edge/all-edges]
             [node/all-nodes]
             [node/diamond]]]]

          ;; Right column: info panel
          [tooltip/info-panel]

          ;; noscript fallback
          [:noscript
           {:style {:grid-column "1 / -1"
                    :color data/chalk-dim
                    :font-family "Georgia, serif"
                    :padding "2em"
                    :text-align "center"}}
           [:p "Enable JavaScript to explore the interactive project constellation."]]])})))
