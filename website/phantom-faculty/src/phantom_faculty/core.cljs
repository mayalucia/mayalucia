(ns phantom-faculty.core
  "Entry point: find the mount element, render the constellation.
   Called by shadow-cljs :init-fn on page load."
  (:require
    [reagent.dom.client :as rdc]
    [phantom-faculty.components.constellation :as constellation]))

(defonce !root (atom nil))

(defn ^:export init!
  "Mount the interactive constellation into the DOM.
   Looks for #phantom-faculty-constellation — if not found (wrong page),
   does nothing silently."
  []
  (js/console.log "phantom-faculty: init! called")
  (if-let [el (js/document.getElementById "phantom-faculty-constellation")]
    (do
      (js/console.log "phantom-faculty: mount element found")
      ;; Clear the loading message
      (when-let [loading (.querySelector el ".constellation-loading")]
        (.remove loading))
      ;; Mount Reagent via React 18+ createRoot API
      (try
        (let [root (rdc/create-root el)]
          (reset! !root root)
          (rdc/render root [constellation/root]))
        (js/console.log "phantom-faculty: render called successfully")
        (catch js/Error e
          (js/console.error "phantom-faculty: render failed" e))))
    (js/console.log "phantom-faculty: mount element NOT found")))
