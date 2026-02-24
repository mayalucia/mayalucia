(ns phantom-faculty.components.background
  "Chalk-dust SVG texture layer.
   ~200 tiny rects with low opacity, seeded deterministically.
   Lighter than Python's 4000 particles — SVG elements are costlier.")

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
  "Pre-computed chalk dust particles."
  (let [rng (make-rng 42)
        n 200]
    (vec
      (for [_ (range n)]
        {:x    (- (* (rng) 17.0) 8.5)
         :y    (- (* (rng) 13.0) 6.5)
         :size (+ 0.01 (* (rng) 0.04))
         :a    (+ 0.02 (* (rng) 0.06))}))))

(defn chalk-dust
  "SVG group of faint chalk-dust particles."
  []
  [:g.chalk-dust
   (for [{:keys [x y size a]} dust-particles]
     ^{:key (str x y)}
     [:rect {:x x :y y :width size :height size
             :fill "#e8e4d4" :opacity a}])])
