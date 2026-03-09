(ns story-browser.components.info-panel
  "Right-column info panel showing story or concept details."
  (:require [story-browser.state :as state]
            [story-browser.data :as data]))

(def doc-type-labels
  {:field-notes             "Field Notes"
   :logbook                 "Logbook"
   :archival-reconstruction "Archival Reconstruction"
   :cognitive-field-guide   "Cognitive Field Guide"
   :geological-survey       "Geological Survey"
   :walnut-ink-document     "Walnut-Ink Document"})

(defn- illustration-url [story filename]
  (str "/images/writing/" (:image-dir story) "/" filename))

(defn- story-detail [story]
  [:div.story-detail
   ;; Header
   [:div {:style {:margin-bottom "16px"}}
    [:div {:style {:font-size "11px"
                   :text-transform "uppercase"
                   :letter-spacing "1.5px"
                   :color (data/story-colour story)
                   :margin-bottom "4px"}}
     (get doc-type-labels (:document-type story) "Document")]
    [:h2 {:style {:margin "0 0 4px 0"
                  :font-family "serif"
                  :font-size "20px"
                  :color data/chalk}}
     (str "§" (:number story) " — " (:title story))]
    (when-let [variant (:variant story)]
      [:div {:style {:font-style "italic"
                     :color data/chalk-dim
                     :font-size "13px"}}
       (str "Also: " (:title variant) " (" (:lang variant) ")")])]

   ;; Setting
   [:div {:style {:margin-bottom "12px"
                  :font-size "12px"
                  :color data/chalk-dim}}
    [:strong "Setting: "]
    (get-in story [:setting :region])
    (when-let [alt (get-in story [:setting :altitude])]
      (when (string? alt)
        (str " · " alt)))]

   ;; Description
   [:p {:style {:font-size "13px"
                :line-height "1.5"
                :color data/chalk
                :margin "0 0 12px 0"}}
    (:description story)]

   ;; Illustration thumbnails
   (when (seq (:illustrations story))
     [:div {:style {:display "flex"
                    :flex-wrap "wrap"
                    :gap "6px"
                    :margin-bottom "12px"}}
      (for [img (:illustrations story)]
        ^{:key img}
        [:img {:src (illustration-url story img)
               :alt img
               :style {:width "60px"
                       :height "60px"
                       :object-fit "cover"
                       :border-radius "4px"
                       :opacity 0.8}}])])

   ;; Characters
   (when (seq (:characters story))
     [:div {:style {:margin-bottom "12px"}}
      [:div {:style {:font-size "10px"
                     :text-transform "uppercase"
                     :letter-spacing "1px"
                     :color data/chalk-dim
                     :margin-bottom "4px"}}
       "Characters"]
      [:div {:style {:display "flex" :flex-wrap "wrap" :gap "4px"}}
       (for [char-id (:characters story)
             :let [c (get data/characters-by-id char-id)]]
         ^{:key char-id}
         [:span {:style {:font-size "12px"
                         :padding "2px 8px"
                         :border-radius "10px"
                         :background "rgba(232,228,212,0.08)"
                         :color data/chalk}}
          (or (:name c) char-id)])]])

   ;; Translation keys
   (let [story-concepts (data/story-concepts story)]
     (when (seq story-concepts)
       [:div {:style {:margin-bottom "12px"}}
        [:div {:style {:font-size "10px"
                       :text-transform "uppercase"
                       :letter-spacing "1px"
                       :color data/chalk-dim
                       :margin-bottom "4px"}}
         "Translation Keys"]
        [:div
         (for [c story-concepts]
           ^{:key (name (:id c))}
           [:div {:style {:font-size "11px"
                          :padding "3px 0"
                          :border-bottom "1px solid rgba(232,228,212,0.06)"}}
            [:span {:style {:color (data/concept-colour c)}}
             (:name c)]
            [:span {:style {:color data/chalk-dim
                            :margin-left "8px"
                            :font-style "italic"}}
             (str "→ " (:story-equiv c))]])]]))

   ;; Link to full story
   [:a {:href (str "/writing/" (:slug story) "/")
        :style {:font-size "12px"
                :color (data/story-colour story)
                :text-decoration "none"
                :display "block"
                :margin-top "8px"}}
    "Read the full story →"]])

(defn- concept-detail [{:keys [concept stories]}]
  [:div.concept-detail
   [:div {:style {:font-size "11px"
                  :text-transform "uppercase"
                  :letter-spacing "1.5px"
                  :color data/chalk-dim
                  :margin-bottom "4px"}}
    "Translation Key"]
   [:h2 {:style {:margin "0 0 4px 0"
                 :font-family "serif"
                 :font-size "18px"
                 :color (data/concept-colour concept)}}
    (:name concept)]
   [:p {:style {:font-style "italic"
                :font-size "13px"
                :color data/chalk
                :margin "0 0 12px 0"}}
    (:story-equiv concept)]
   [:div {:style {:font-size "10px"
                  :text-transform "uppercase"
                  :letter-spacing "1px"
                  :color data/chalk-dim
                  :margin-bottom "6px"}}
    (str "Appears in " (count stories) " stor" (if (= 1 (count stories)) "y" "ies"))]
   (for [s (sort-by :number stories)]
     ^{:key (:id s)}
     [:div {:style {:font-size "12px"
                    :padding "4px 0"
                    :cursor "pointer"
                    :color data/chalk
                    :border-bottom "1px solid rgba(232,228,212,0.06)"}
            :on-click #(state/select-story! (:id s))}
      (str "§" (:number s) " " (:title s))])])

(defn info-panel []
  (fn []
    (let [detail (state/active-detail)]
      [:div.info-panel
       {:style {:padding "14px"
                :height "100%"
                :overflow-y "auto"
                :background "rgba(18,18,30,0.95)"}}
       (cond
         (and (map? detail) (:concept detail))
         [concept-detail detail]

         (map? detail)
         [story-detail detail]

         :else
         [:div {:style {:color data/chalk-dim
                        :font-size "13px"
                        :font-style "italic"
                        :padding-top "40px"
                        :text-align "center"}}
          "Hover a node to explore..."
          [:br]
          [:span {:style {:font-size "11px" :opacity 0.6}}
           "Click to pin the selection"]])])))
