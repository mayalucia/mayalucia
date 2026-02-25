(ns project-constellation.components.node
  "Multi-type node renderer. Dispatches on :type for distinct visual treatment.
   Phase nodes render as 3D crystals; other types use glow circles."
  (:require
    [project-constellation.state :as state]
    [project-constellation.data :as data]))

;; === SVG geometry utilities ====================================================

(defn- points-str
  "Convert [[x y] ...] to SVG points attribute string."
  [pts]
  (apply str (interpose " " (map (fn [[x y]] (str x "," y)) pts))))

(defn- navigate! [url]
  (when url (set! (.-location js/window) url)))

;; === One crystal, four lights =================================================
;; Brilliant-cut diamond viewed from above. Vertices point at cardinals
;; (toward phases). The same geometry serves both the central diamond at (0,0)
;; and the four outer phase projections — identical shape, different lighting.
;; Light from the center illuminates the inward-facing quadrant of each
;; outer crystal; the remaining facets fall into shadow.

(def ^:private phase-cycle
  ["measure" "model" "manifest" "evaluate"])

(defn- cycle-distance
  "Steps between two phases in the 4-phase ring (0, 1, or 2)."
  [a b]
  (let [ia (.indexOf phase-cycle a)
        ib (.indexOf phase-cycle b)]
    (when (and (>= ia 0) (>= ib 0))
      (min (mod (- ib ia) 4) (mod (- ia ib) 4)))))

;; --- Shared diamond geometry (unit coordinates, centered at origin) ----------
;; Table octagon: vertices at i*45° (vertex 0=right, 2=down, 4=left, 6=up).
;; Kite tips at cardinals (outermost reach toward each phase).
;; Star tips at intercardinals (between phases).

(def ^:private unit-diamond
  "Unit diamond vertices. Scale by `s` and translate by (cx, cy) for use."
  (let [r-t 0.38   ;; table octagon radius
        r-k 1.40   ;; kite tip radius (cardinal — toward phases)
        r-s 0.90   ;; star tip radius (intercardinal — between phases)
        table (vec (for [i (range 8)]
                     (let [a (* (/ js/Math.PI 180) (* i 45))]
                       [(* r-t (js/Math.cos a))
                        (* r-t (js/Math.sin a))])))
        ;; Kite tips at cardinals (outermost, pointing at phases)
        kites {:right [r-k 0]     :down [0 r-k]
               :left [(- r-k) 0]  :up [0 (- r-k)]}
        ;; Star tips at intercardinals
        ss (* r-s (/ (js/Math.sqrt 2) 2))
        stars {:ur [ss (- ss)]   :dr [ss ss]
               :dl [(- ss) ss]   :ul [(- ss) (- ss)]}]
    {:table table :kites kites :stars stars}))

;; Facet definitions: [quadrant-phase, table-idx-a, table-idx-b,
;;   outer-vertex-key-1, outer-vertex-key-2, primary?]
;; Each quadrant straddles a table vertex pointing at that phase.
;; Vertex 0 = right (Manifest), 2 = down (Evaluate),
;; 4 = left (Measure), 6 = up (Model).
;;
;; Quadrant "manifest" (right, between star-ur and star-dr):
;;   Facet A: T7, T0, kite-right, star-ur  (upper half)
;;   Facet B: T0, T1, star-dr, kite-right  (lower half)

(def ^:private diamond-facet-defs
  [;; Manifest quadrant (right, around T0)
   ["manifest" 7 0 :s-ur :k-right true]
   ["manifest" 0 1 :k-right :s-dr  false]
   ;; Evaluate quadrant (bottom, around T2)
   ["evaluate" 1 2 :s-dr :k-down  true]
   ["evaluate" 2 3 :k-down :s-dl  false]
   ;; Measure quadrant (left, around T4)
   ["measure"  3 4 :s-dl :k-left  true]
   ["measure"  4 5 :k-left :s-ul  false]
   ;; Model quadrant (top, around T6)
   ["model"    5 6 :s-ul :k-up    true]
   ["model"    6 7 :k-up :s-ur    false]])

(defn- resolve-vertex
  "Look up a vertex key from unit-diamond."
  [v {:keys [table kites stars]}]
  (cond
    (number? v)   (nth table v)
    (= :k-right v) (:right kites)
    (= :k-down v)  (:down kites)
    (= :k-left v)  (:left kites)
    (= :k-up v)    (:up kites)
    (= :s-ur v)    (:ur stars)
    (= :s-dr v)    (:dr stars)
    (= :s-dl v)    (:dl stars)
    (= :s-ul v)    (:ul stars)))

(defn- translate-scale
  "Translate and scale a [x y] point."
  [[x y] cx cy s]
  [(+ cx (* x s)) (+ cy (* y s))])

;; --- Central diamond (at origin) -------------------------------------------

(defn diamond
  "The central brilliant-cut diamond at (0,0). Only at root view.
   8 crown facets + table octagon. Brightens toward hovered phase."
  []
  (when (state/at-root?)
    (let [geo        unit-diamond
          {:keys [table kites]} geo
          hover      @state/!hover
          phase-ids  #{"measure" "model" "manifest" "evaluate"}
          self-hov?  (= hover "diamond-center")
          phase-hov? (or self-hov? (contains? phase-ids hover))
          r-sight    3.4
          phase-dirs [["measure"  [-1  0] :k-left]
                      ["model"    [ 0 -1] :k-up]
                      ["manifest" [ 1  0] :k-right]
                      ["evaluate" [ 0  1] :k-down]]]
      [:g.diamond
       {:style {:cursor "pointer"}
        :on-mouse-enter #(reset! state/!hover "diamond-center")
        :on-mouse-leave #(when (= "diamond-center" @state/!hover)
                           (reset! state/!hover nil))
        :on-click       (fn [e]
                          (.stopPropagation e)
                          (navigate! "/projects/one-crystal-four-lights/"))}
       ;; Ambient glow
       [:circle {:cx 0 :cy 0 :r 1.8
                 :fill "url(#diamond-glow)"
                 :opacity (if phase-hov? 0.18 0.08)}]

       ;; Table octagon
       [:polygon {:points (points-str table)
                  :fill "url(#diamond-table)"
                  :opacity (if phase-hov? 0.25 0.10)
                  :stroke data/chalk
                  :stroke-width 0.008
                  :stroke-opacity (if phase-hov? 0.15 0.06)}]

       ;; 8 crown facets
       (for [[pid ti-a ti-b outer-a outer-b primary?] diamond-facet-defs]
         (let [pts [(nth table ti-a) (nth table ti-b)
                    (resolve-vertex outer-b geo)
                    (resolve-vertex outer-a geo)]
               grad (if primary? "top" "left")
               op  (cond
                     (not phase-hov?)  (if primary? 0.18 0.14)
                     self-hov?         (if primary? 0.45 0.35)
                     :else
                     (case (cycle-distance hover pid)
                       0 (if primary? 0.65 0.50)
                       1 (if primary? 0.30 0.22)
                       2 (if primary? 0.16 0.12)
                       (if primary? 0.18 0.14)))]
           ^{:key (str "diamond-" pid "-" ti-a)}
           [:polygon {:points (points-str pts)
                      :fill (str "url(#crystal-" grad "-" pid ")")
                      :opacity op}]))

       ;; Kite-tip ridge lines (center to each phase vertex)
       (for [[pid _ k-key] phase-dirs]
         (let [tip (resolve-vertex k-key geo)
               op  (cond
                     (not phase-hov?) 0.08
                     self-hov?        0.25
                     (= hover pid)    0.35
                     (= 1 (cycle-distance hover pid)) 0.15
                     :else 0.08)]
           ^{:key (str "diamond-ridge-" pid)}
           [:line {:x1 0 :y1 0
                   :x2 (first tip) :y2 (second tip)
                   :stroke "#ffffff"
                   :stroke-width 0.012
                   :opacity op}]))

       ;; Sight lines from kite tips toward outer crystals
       (for [[pid [dx dy] k-key] phase-dirs]
         (let [tip   (resolve-vertex k-key geo)
               sight [(* dx r-sight) (* dy r-sight)]
               op    (cond
                       (not phase-hov?) 0.07
                       self-hov?        0.18
                       (= hover pid)    0.25
                       (= 1 (cycle-distance hover pid)) 0.12
                       :else 0.07)]
           ^{:key (str "diamond-sight-" pid)}
           [:line {:x1 (first tip) :y1 (second tip)
                   :x2 (first sight) :y2 (second sight)
                   :stroke (get data/cluster-colours pid)
                   :stroke-width 0.018
                   :stroke-dasharray "0.08 0.12"
                   :opacity op}]))

       ;; Central convergence point
       [:circle {:cx 0 :cy 0 :r 0.05
                 :fill data/chalk
                 :opacity (if phase-hov? 0.6 0.25)}]])))

;; --- Outer phase crystals (same diamond, directional lighting) ---------------
;; Each outer crystal is the same brilliant-cut form, translated to (cx,cy)
;; and scaled by s. The quadrant facing the center is brightly lit;
;; adjacent quadrants get medium light; the far side is in deep shadow.

(def ^:private phase-lit-quadrant
  "Which quadrant faces the center (light source) for each phase."
  {"measure"  "manifest"    ;; Measure at left, lit from right → manifest quadrant
   "model"    "evaluate"    ;; Model at top, lit from below → evaluate quadrant
   "manifest" "measure"     ;; Manifest at right, lit from left → measure quadrant
   "evaluate" "model"})     ;; Evaluate at bottom, lit from above → model quadrant

(defn- crystal-view
  "Render the shared diamond geometry at (cx, cy) scaled by s.
   `id` is the phase this crystal represents.
   `op` is the base opacity.
   Facets in the lit quadrant (facing center) are bright;
   adjacent quadrants medium; far quadrant dark."
  [cx cy s id op]
  (let [geo  unit-diamond
        lit  (get phase-lit-quadrant id)
        ts   (fn [v] (translate-scale (resolve-vertex v geo) cx cy s))
        {:keys [table]} geo
        t    (fn [i] (translate-scale (nth table i) cx cy s))]
    [:<>
     ;; Table octagon (small, faint)
     [:polygon {:points (points-str (mapv #(translate-scale % cx cy s) table))
                :fill (str "url(#crystal-top-" id ")")
                :filter "url(#phase-shadow)"
                :opacity (* op 0.3)}]
     ;; 8 crown facets with directional lighting
     (for [[pid ti-a ti-b outer-a outer-b primary?] diamond-facet-defs]
       (let [pts   [(t ti-a) (t ti-b) (ts outer-b) (ts outer-a)]
             ;; How far is this facet's quadrant from the lit quadrant?
             dist  (cycle-distance pid lit)
             grad  (case dist
                     0 "top"     ;; lit face — brightest
                     1 "left"    ;; side faces — medium
                     2 "right")  ;; far face — darkest
             fop   (* op (case dist 0 1.0  1 0.7  2 0.35  0.5))]
         ^{:key (str "cv-" id "-" ti-a)}
         [:polygon {:points (points-str pts)
                    :fill (str "url(#crystal-" grad "-" id ")")
                    :opacity fop}]))
     ;; Edge highlights on the two lit-quadrant ridge lines
     (let [lit-kite-key (case lit
                          "manifest" :k-right  "evaluate" :k-down
                          "measure"  :k-left   "model"    :k-up)]
       [:line {:x1 cx :y1 cy
               :x2 (first (ts lit-kite-key))
               :y2 (second (ts lit-kite-key))
               :stroke "#ffffff"
               :stroke-width (* 0.015 s)
               :opacity (* op 0.3)}])]))

(defn entity-node
  "Render a single entity node. Visual treatment varies by :type."
  [{:keys [id name glyph subtitle type status url] :as entity}]
  (let [pos        (state/node-position id)
        colour     (get data/entity-colours id data/chalk)
        hover      @state/!hover
        hovered?   (= id hover)
        connected? (state/connected-to-hover? id)
        dimmed?    (and hover (not hovered?) (not connected?))
        dormant?   (= status :dormant)
        phase?     (= type :phase)
        thread?    (= type :thread)
        anchor?    (= type :anchor)
        drillable? (and (state/at-root?) (data/drillable? entity))
        ;; Scale depends on type and hover state
        base-scale (cond phase?  1.2
                         thread? 0.7
                         anchor? 0.85
                         :else   1.0)
        hover-scale (cond hovered?   1.4
                          connected? 1.1
                          dimmed?    0.85
                          :else      1.0)
        scale       (* base-scale hover-scale)
        ;; Glyph and label sizes
        glyph-size (* 0.9 scale)
        name-size  (* 0.28 scale)
        sub-size   (* 0.18 scale)
        ;; Glow radii
        glow-outer (* 0.50 scale)
        glow-inner (* 0.32 scale)
        ;; Opacity
        min-opacity (if phase? 0.4 0.0)
        glyph-opacity (cond hovered?  1.0
                             connected? 0.9
                             dimmed?    (max 0.18 min-opacity)
                             dormant?   0.4
                             :else      0.85)
        name-opacity  (cond hovered?  1.0
                             connected? 0.85
                             dimmed?    (max 0.12 min-opacity)
                             dormant?   0.3
                             :else      0.75)
        sub-opacity   (cond hovered?  0.8
                             connected? 0.6
                             dimmed?    (max 0.08 min-opacity)
                             dormant?   0.2
                             :else      0.5)
        glow-o-outer  (cond hovered?  0.30
                             connected? 0.14
                             dimmed?    0.0
                             :else      0.06)
        glow-o-inner  (cond hovered?  0.45
                             connected? 0.20
                             dimmed?    0.0
                             :else      0.10)
        ;; Phase nodes: ring instead of glow
        phase-ring?   (and phase? (not hovered?))
        ;; Thread nodes: smaller, different style
        thread-r      (* 0.15 scale)]
    [:g.entity-node
     {:on-mouse-enter #(reset! state/!hover id)
      :on-mouse-leave #(when (= id @state/!hover)
                         (reset! state/!hover nil))
      :on-click       (fn [e]
                        (.stopPropagation e)
                        (cond
                          drillable? (state/drill-down! id name)
                          url        (navigate! url)
                          :else      (reset! state/!selected
                                       (if (= id @state/!selected) nil id))))
      :style {:cursor "pointer"}}

     ;; Phase nodes: same diamond form, lit from center
     (when phase?
       (let [s    (* 0.55 base-scale hover-scale)
             cx   (:x pos)
             cy   (:y pos)
             op   (cond hovered? 0.95 dimmed? 0.25 :else 0.80)]
         [crystal-view cx cy s id op]))

     ;; Non-phase nodes: glow circles
     (when-not phase?
       [:<>
        [:circle.glow-outer
         {:cx (:x pos) :cy (:y pos)
          :r glow-outer
          :fill colour
          :opacity glow-o-outer}]
        [:circle.glow-inner
         {:cx (:x pos) :cy (:y pos)
          :r glow-inner
          :fill colour
          :opacity glow-o-inner}]])

     ;; Thread nodes: additional pulsing dot
     (when thread?
       [:circle.thread-dot
        {:cx (:x pos) :cy (:y pos)
         :r thread-r
         :fill colour
         :opacity (if (= status :active) 0.8 0.3)}])

     ;; Glyph (hidden for phase nodes — the crystal is the glyph)
     (when (and (not hovered?) (not phase?))
       [:text.glyph
        {:x (:x pos) :y (:y pos)
         :text-anchor "middle"
         :dominant-baseline "central"
         :fill colour
         :opacity glyph-opacity
         :font-size (str glyph-size "px")}
        glyph])

     ;; Name label (hidden for phase nodes — cluster label serves this role)
     (when (and (not hovered?) (not phase?))
       [:text.name-label
        {:x (:x pos) :y (+ (:y pos) (* 0.38 scale))
         :text-anchor "middle"
         :fill colour
         :opacity name-opacity
         :font-size (str name-size "px")
         :font-weight (if anchor? "normal" "bold")
         :font-style (if anchor? "italic" "normal")
         :font-family "serif"}
        name])

     ;; Subtitle label
     (when (and (not hovered?) (not thread?))
       [:text.subtitle-label
        {:x (:x pos) :y (+ (:y pos) (* 0.58 scale))
         :text-anchor "middle"
         :fill colour
         :opacity sub-opacity
         :font-size (str sub-size "px")
         :font-style "italic"
         :font-family "serif"}
        subtitle])

     ;; Drillable indicator
     (when (and drillable? (not dimmed?))
       [:text {:x (:x pos) :y (+ (:y pos) (* 0.78 scale))
               :text-anchor "middle"
               :fill colour
               :opacity (if hovered? 0.7 0.3)
               :font-size (str (* 0.16 scale) "px")}
        "\u25BC"])]))

(defn all-nodes
  "Render all entity nodes."
  []
  [:g.nodes
   (for [{:keys [id] :as e} (state/current-entities)]
     ^{:key id}
     [entity-node e])])
