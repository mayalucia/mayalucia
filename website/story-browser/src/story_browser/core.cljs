(ns story-browser.core
  (:require [reagent.core :as r]
            ["react-dom/client" :as rdom-client]
            [story-browser.state :as state]
            [story-browser.data :as data]
            [story-browser.components.geography :as geography]
            [story-browser.components.concepts :as concepts]
            [story-browser.components.info-panel :as info-panel]))

(defn view-tab [label view-key]
  (let [active? (= @state/!view view-key)]
    [:button
     {:on-click #(state/switch-view! view-key)
      :style    {:padding "6px 16px"
                 :border "none"
                 :border-bottom (if active?
                                  (str "2px solid " data/chalk)
                                  "2px solid transparent")
                 :background "transparent"
                 :color (if active? data/chalk data/chalk-dim)
                 :font-family "serif"
                 :font-size "13px"
                 :cursor "pointer"
                 :letter-spacing "0.5px"}}
     label]))

(defn app []
  [:div.story-browser
   {:style {:display "grid"
            :grid-template-columns "1fr 260px"
            :grid-template-rows "auto 1fr"
            :height "100vh"
            :background data/slate
            :color data/chalk
            :font-family "system-ui, -apple-system, sans-serif"}}

   ;; Top bar — view tabs
   [:div.tabs
    {:style {:grid-column "1 / -1"
             :display "flex"
             :gap "4px"
             :padding "8px 16px"
             :border-bottom "1px solid rgba(232,228,212,0.1)"}}
    [view-tab "Geography" :geography]
    [view-tab "Concepts" :concept]
    [:div {:style {:flex 1}}]
    [:span {:style {:font-size "11px"
                    :color data/chalk-dim
                    :align-self "center"
                    :font-style "italic"}}
     "MāyāLucIA Story Browser"]]

   ;; Main view
   [:div.main-view
    {:style {:overflow "hidden"
             :position "relative"}}
    (case @state/!view
      :geography [geography/geography-view]
      :concept   [concepts/concept-view]
      [geography/geography-view])]

   ;; Info panel
   [:div.panel
    {:style {:border-left "1px solid rgba(232,228,212,0.1)"
             :overflow-y "auto"}}
    [info-panel/info-panel]]])

(defonce !root (atom nil))

(defn ^:export init! []
  (let [root-el (.getElementById js/document "story-browser-root")]
    (when root-el
      (when-let [loading (.querySelector root-el ".loading")]
        (.remove loading))
      (let [root (rdom-client/createRoot root-el)]
        (reset! !root root)
        (.render root (r/as-element [app]))))))
