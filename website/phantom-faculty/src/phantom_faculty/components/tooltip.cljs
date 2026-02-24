(ns phantom-faculty.components.tooltip
  "Right-column info panel. Shows details of the hovered phantom.
   Empty state when nothing is hovered."
  (:require
    [phantom-faculty.state :as state]
    [phantom-faculty.data :as data]))

(defn- empty-state
  "Shown when no phantom is hovered."
  []
  [:div {:style {:color data/chalk-dim
                 :font-family "Georgia, serif"
                 :font-size "12px"
                 :font-style "italic"
                 :padding-top "24px"}}
   "Hover a phantom to explore"])

(defn- phantom-detail
  "Full detail view of a hovered phantom."
  [id]
  (let [phantom (get data/phantoms-by-id id)
        colour  (get data/phantom-colours id data/chalk)]
    [:div

     ;; Glyph + Name row
     [:div {:style {:display "flex"
                    :align-items "center"
                    :gap "8px"
                    :margin-bottom "4px"}}
      [:span {:style {:color colour
                      :font-size "28px"
                      :text-shadow "0 0 8px rgba(0,0,0,0.6)"}}
       (:glyph phantom)]
      [:div
       [:div {:style {:color colour
                      :font-family "Georgia, serif"
                      :font-size "15px"
                      :font-weight "bold"}}
        (:name phantom)]
       [:div {:style {:color data/chalk-dim
                      :font-family "'SF Mono', 'Fira Code', Consolas, monospace"
                      :font-size "9px"
                      :letter-spacing "0.06em"
                      :text-transform "uppercase"}}
        (:cluster phantom)]]]

     ;; Skill
     [:div {:style {:color data/chalk
                    :font-family "Georgia, serif"
                    :font-size "12px"
                    :font-style "italic"
                    :margin-bottom "6px"}}
      (:skill phantom)]

     ;; One-liner
     [:div {:style {:color data/chalk
                    :font-family "Georgia, serif"
                    :font-size "11px"
                    :font-style "italic"
                    :line-height "1.5"
                    :margin-bottom "10px"}}
      (:one-liner phantom)]

     ;; Description
     (when-let [desc (:description phantom)]
       [:div {:style {:color data/chalk-dim
                      :font-family "Georgia, serif"
                      :font-size "11px"
                      :line-height "1.6"}}
        desc])]))

(defn info-panel
  "Right-column info panel component."
  []
  (fn []
    [:div.constellation-info-panel
     {:style {:background data/slate
              :border-left "1px solid rgba(232,228,212,0.08)"
              :padding "16px 12px"}}
     (if-let [id @state/!hover]
       [phantom-detail id]
       [empty-state])]))
