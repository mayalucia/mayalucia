(ns phantom-faculty.components.node
  "Phantom glyph node: glow + Unicode glyph + name + skill.
   Hover triggers scaling and brightness. Click navigates to anchor."
  (:require
    [phantom-faculty.state :as state]
    [phantom-faculty.data :as data]))

(defn- scroll-to-anchor!
  "Smooth-scroll to a section anchor in the page."
  [anchor]
  (when-let [el (js/document.getElementById anchor)]
    (.scrollIntoView el #js {:behavior "smooth" :block "start"})))

(defn phantom-node
  "Render a single phantom: glow circles, glyph, name label, skill label.
   When a node is hovered:
     - hovered node:    scale 1.5x, full brightness
     - connected nodes: scale 1.15x, high brightness
     - other nodes:     scale 0.85x, heavily dimmed"
  [{:keys [id name glyph skill anchor]}]
  (let [pos        (state/node-position id)
        colour     (get data/phantom-colours id data/chalk)
        hover      @state/!hover
        hovered?   (= id hover)
        connected? (state/connected-to-hover? id)
        dimmed?    (and hover (not hovered?) (not connected?))
        construction? (= id "construction")
        ;; Scale factors
        base-glyph  (if construction? 1.1 0.9)
        base-name   (if construction? 0.38 0.33)
        scale       (cond
                      hovered?   1.5
                      connected? 1.15
                      dimmed?    0.85
                      :else      1.0)
        glyph-size  (* base-glyph scale)
        name-size   (* base-name scale)
        skill-size  (* 0.20 scale)
        ;; Glow radii
        glow-outer  (* (if construction? 0.65 0.50) scale)
        glow-inner  (* (if construction? 0.40 0.32) scale)
        ;; Opacity
        glyph-opacity (cond hovered? 1.0  connected? 0.9  dimmed? 0.18  :else 0.85)
        name-opacity  (cond hovered? 1.0  connected? 0.85 dimmed? 0.12  :else 0.75)
        skill-opacity (cond hovered? 0.8  connected? 0.6  dimmed? 0.08  :else 0.5)
        glow-o-outer  (cond hovered? 0.30 connected? 0.14 dimmed? 0.0   :else 0.06)
        glow-o-inner  (cond hovered? 0.45 connected? 0.20 dimmed? 0.0   :else 0.10)]
    [:g.phantom-node
     {:on-mouse-enter #(reset! state/!hover id)
      :on-mouse-leave #(when (= id @state/!hover)
                         (reset! state/!hover nil))
      :on-click       #(scroll-to-anchor! anchor)
      :style {:cursor "pointer"}}

     ;; Outer glow
     [:circle.glow-outer
      {:cx (:x pos) :cy (:y pos)
       :r  glow-outer
       :fill colour
       :opacity glow-o-outer}]

     ;; Inner glow
     [:circle.glow-inner
      {:cx (:x pos) :cy (:y pos)
       :r  glow-inner
       :fill colour
       :opacity glow-o-inner}]

     ;; The glyph — hide when this node is hovered (tooltip takes over)
     (when-not hovered?
       [:text.glyph
        {:x (:x pos) :y (:y pos)
         :text-anchor "middle"
         :dominant-baseline "central"
         :fill colour
         :opacity glyph-opacity
         :font-size (str glyph-size "px")}
        glyph])

     ;; Name label — hide when hovered
     (when-not hovered?
       [:text.name-label
        {:x (:x pos) :y (+ (:y pos) (* 0.38 scale))
         :text-anchor "middle"
         :fill colour
         :opacity name-opacity
         :font-size (str name-size "px")
         :font-weight "bold"
         :font-family "serif"}
        name])

     ;; Skill label — hide when hovered
     (when-not hovered?
       [:text.skill-label
        {:x (:x pos) :y (+ (:y pos) (* 0.62 scale))
         :text-anchor "middle"
         :fill colour
         :opacity skill-opacity
         :font-size (str skill-size "px")
         :font-style "italic"
         :font-family "serif"}
        skill])]))

(defn all-nodes
  "Render all phantom nodes."
  []
  [:g.nodes
   (for [{:keys [id] :as p} data/phantoms]
     ^{:key id}
     [phantom-node p])])
