(ns project-constellation.components.tooltip
  "Right-column info panel. Shows details of the hovered or selected entity.
   Type-aware: different detail layouts for phases, modules, anchors, threads."
  (:require
    [project-constellation.state :as state]
    [project-constellation.data :as data]))

(defn- empty-state
  "Shown when no entity is focused."
  []
  [:div {:style {:color data/chalk-dim
                 :font-family "Georgia, serif"
                 :font-size "12px"
                 :font-style "italic"
                 :padding-top "24px"}}
   "Hover a node to explore the constellation"])

(defn- type-label [type]
  (case type
    :phase     "CYCLE PHASE"
    :module    "MODULE"
    :domain    "DOMAIN"
    :infra     "INFRASTRUCTURE"
    :anchor    "FOUNDATION"
    :vision    "PLANNED"
    :thread    "ACTIVE THREAD"
    :lesson    "LESSON"
    :impl      "IMPLEMENTATION"
    :artifact  "ARTIFACT"
    :component "COMPONENT"
    :crystal   "CENTRAL CRYSTAL"
    ""))

(defn- status-label [status]
  (case status
    :active    "Active"
    :dormant   "Dormant"
    :completed "Completed"
    :waiting   "Waiting"
    :planned   "Planned"
    nil))

(defn- entity-detail
  "Full detail view of a focused entity."
  [id]
  (let [entity (get data/entities-by-id id)
        colour (get data/entity-colours id data/chalk)
        {:keys [name glyph subtitle one-liner description
                type status tech-stack url]} entity]
    [:div

     ;; Glyph + Name row
     [:div {:style {:display "flex"
                    :align-items "center"
                    :gap "8px"
                    :margin-bottom "4px"}}
      [:span {:style {:color colour
                      :font-size "28px"
                      :text-shadow "0 0 8px rgba(0,0,0,0.6)"}}
       glyph]
      [:div
       [:div {:style {:color colour
                      :font-family "Georgia, serif"
                      :font-size "15px"
                      :font-weight "bold"}}
        name]
       [:div {:style {:color data/chalk-dim
                      :font-family "'SF Mono', 'Fira Code', Consolas, monospace"
                      :font-size "9px"
                      :letter-spacing "0.06em"
                      :text-transform "uppercase"}}
        (type-label type)]]]

     ;; Subtitle
     [:div {:style {:color data/chalk
                    :font-family "Georgia, serif"
                    :font-size "12px"
                    :font-style "italic"
                    :margin-bottom "6px"}}
      subtitle]

     ;; One-liner
     [:div {:style {:color data/chalk
                    :font-family "Georgia, serif"
                    :font-size "11px"
                    :font-style "italic"
                    :line-height "1.5"
                    :margin-bottom "10px"}}
      one-liner]

     ;; Status badge (for modules, domains, threads)
     (when status
       [:div {:style {:color data/chalk-dim
                      :font-family "'SF Mono', 'Fira Code', Consolas, monospace"
                      :font-size "9px"
                      :letter-spacing "0.06em"
                      :margin-bottom "8px"}}
        (str "Status: " (status-label status))])

     ;; Tech stack (for modules, domains)
     (when (seq tech-stack)
       [:div {:style {:margin-bottom "8px"}}
        (for [tech tech-stack]
          ^{:key tech}
          [:span {:style {:display "inline-block"
                          :background "rgba(232,228,212,0.08)"
                          :color data/chalk-dim
                          :font-family "'SF Mono', 'Fira Code', Consolas, monospace"
                          :font-size "9px"
                          :padding "2px 6px"
                          :margin-right "4px"
                          :margin-bottom "3px"
                          :border-radius "3px"}}
           tech])])

     ;; Description
     (when description
       [:div {:style {:color data/chalk-dim
                      :font-family "Georgia, serif"
                      :font-size "11px"
                      :line-height "1.6"
                      :margin-top "4px"}}
        description])

     ;; URL link
     (when url
       [:div {:style {:margin-top "10px"}}
        [:a {:href url
             :style {:color colour
                     :font-family "'SF Mono', 'Fira Code', Consolas, monospace"
                     :font-size "10px"
                     :text-decoration "none"
                     :opacity 0.7}
             :on-mouse-over #(set! (.. % -target -style -opacity) "1.0")
             :on-mouse-out  #(set! (.. % -target -style -opacity) "0.7")}
         (str "\u2192 " url)]])]))

(defn- breadcrumb
  "Navigation breadcrumb for the info panel header."
  []
  (let [view @state/!view]
    (when (= :child (:level view))
      [:div {:style {:margin-bottom "12px"
                     :padding-bottom "8px"
                     :border-bottom "1px solid rgba(232,228,212,0.06)"}}
       [:span {:style {:color data/chalk-dim
                       :font-family "Georgia, serif"
                       :font-size "11px"
                       :cursor "pointer"
                       :opacity 0.6}
               :on-mouse-over #(set! (.. % -target -style -opacity) "1.0")
               :on-mouse-out  #(set! (.. % -target -style -opacity) "0.6")
               :on-click (fn [e]
                           (.stopPropagation e)
                           (state/navigate-up!))}
        "\u2190 Back to constellation"]])))

(defn info-panel
  "Right-column info panel component."
  []
  (fn []
    [:div.constellation-info-panel
     {:style {:background data/slate
              :border-left "1px solid rgba(232,228,212,0.08)"
              :padding "16px 14px"
              :overflow-y "auto"}}
     [breadcrumb]
     (if-let [id (state/active-detail-id)]
       [entity-detail id]
       [empty-state])]))
