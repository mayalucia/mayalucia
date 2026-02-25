(ns project-constellation.components.background
  "Subtle particle texture layer.
   ~200 tiny rects with low opacity, seeded deterministically.")

;; Simple seeded PRNG (mulberry32)
(defn- make-rng [seed]
  (let [state (atom seed)]
    (fn []
      (swap! state #(bit-or (+ % 0x6D2B79F5) 0))
      (let [t (js/Math.imul (bit-xor @state (unsigned-bit-shift-right @state 15))
                            (bit-or @state 1))
            t (+ t (js/Math.imul (bit-xor t (unsigned-bit-shift-right t 7))
                                 (bit-or t 61)))]
        (/ (unsigned-bit-shift-right (bit-xor t (unsigned-bit-shift-right t 14))
                                     0)
           4294967296.0)))))

(def ^:private dust-particles
  "Pre-computed particles for the background."
  (let [rng (make-rng 73)
        n 150]
    (vec
      (for [_ (range n)]
        {:x    (- (* (rng) 14.0) 7.0)
         :y    (- (* (rng) 12.0) 6.0)
         :size (+ 0.01 (* (rng) 0.03))
         :a    (+ 0.01 (* (rng) 0.04))}))))

(defn chalk-dust
  "SVG group of faint particles."
  []
  [:g.chalk-dust
   (for [{:keys [x y size a]} dust-particles]
     ^{:key (str x y)}
     [:rect {:x x :y y :width size :height size
             :fill "#e8e4d4" :opacity a}])])
