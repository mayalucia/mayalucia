(ns project-constellation.core
  "Entry point: find the mount element, render the constellation.
   Called by shadow-cljs :init-fn on page load."
  (:require
    [reagent.dom.client :as rdc]
    [project-constellation.components.constellation :as constellation]))

(defonce !root (atom nil))

(defn ^:export init!
  "Mount the interactive constellation into the DOM.
   Looks for #project-constellation — if not found (wrong page),
   does nothing silently."
  []
  (js/console.log "project-constellation: init! called")
  (if-let [el (js/document.getElementById "project-constellation")]
    (do
      (js/console.log "project-constellation: mount element found")
      (when-let [loading (.querySelector el ".constellation-loading")]
        (.remove loading))
      (try
        (let [root (rdc/create-root el)]
          (reset! !root root)
          (rdc/render root [constellation/root]))
        (js/console.log "project-constellation: render called successfully")
        (catch js/Error e
          (js/console.error "project-constellation: render failed" e))))
    (js/console.log "project-constellation: mount element NOT found")))
