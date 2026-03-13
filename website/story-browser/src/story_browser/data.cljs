(ns story-browser.data)

;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Colour system — region-based, mahābhūta-inspired
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(def region-colours
  {"tirthan"       "#d4a056"   ; warm amber
   "lahaul-passes" "#7eb8d4"   ; ice blue
   "parvati"       "#5a9e6f"   ; forest green
   "baspa-kinnaur" "#c47a5a"   ; terracotta
   "sutlej"        "#8a9cb0"   ; grey-blue
   "doridhar"      "#c9a84c"   ; gold
   "abstract"      "#a0a0a8"   ; silver
   "karakoram"     "#6b6b78"   ; muted slate — the journey's arc
   "diamer"        "#8a6858"   ; warm dark stone — Indus gorge gneiss
   "hunza"         "#9a7868"}) ; iron/blossom — warmer than Diamer

(def slate  "#12121e")
(def chalk  "#e8e4d4")
(def chalk-dim "#8a8678")


;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Equirectangular projection
;;;
;;; Maps lat/lon to SVG pixel coordinates.
;;; Bounding box covers the story geography: Sutlej (SW) to
;;; upper Lahaul (N), Baspa/Kinnaur (E).
;;; +x = east, +y = south (screen convention, lat flipped).
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(def lat-min 30.9)
(def lat-max 36.6)
(def lon-min 73.8)
(def lon-max 78.6)

(def svg-w 800)
(def svg-h 600)
(def pad 40)

(defn project
  "Project {:lat :lon} → {:x :y} in SVG coordinates."
  [{:keys [lat lon]}]
  {:x (+ pad (* (/ (- lon lon-min) (- lon-max lon-min))
               (- svg-w (* 2 pad))))
   :y (+ pad (* (/ (- lat-max lat) (- lat-max lat-min))
               (- svg-h (* 2 pad))))})

(defn hex->rgb [hex]
  (let [h (.replace hex "#" "")]
    [(js/parseInt (.substring h 0 2) 16)
     (js/parseInt (.substring h 2 4) 16)
     (js/parseInt (.substring h 4 6) 16)]))

(defn rgb->hex [[r g b]]
  (str "#"
       (.padStart (.toString (int r) 16) 2 "0")
       (.padStart (.toString (int g) 16) 2 "0")
       (.padStart (.toString (int b) 16) 2 "0")))

(defn blend-colours
  "Blend multiple region colours by weight. `weights` is a map of
   region-id → proportion (0..1). Returns a hex string."
  [weights]
  (let [total (reduce + (vals weights))
        norm  (if (pos? total)
                (reduce-kv (fn [m k v] (assoc m k (/ v total))) {} weights)
                weights)]
    (rgb->hex
     (reduce-kv
      (fn [[r g b] region w]
        (let [[cr cg cb] (hex->rgb (get region-colours region "#808080"))]
          [(+ r (* cr w))
           (+ g (* cg w))
           (+ b (* cb w))]))
      [0 0 0]
      norm))))


;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Story data — from workpacks/data/stories.edn
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(def stories
  [{:id            "thread-walkers"
    :number        1
    :title         "The Thread Walkers"
    :slug          "the-thread-walkers"
    :setting       {:region "Lahaul/Spiti"
                    :places ["Kullu-Tibet border" "high passes"]
                    :altitude "3000-5000m"
                    :season :unknown}
    :document-type :field-notes
    :characters    ["thread-walker" "guild-members"]
    :concepts      [:identity-registry :substrate :guild
                    :relay :disposition :harness]
    :image-dir     "thread-walkers"
    :illustrations ["cord-correction-letter.png"
                    "draft-river-braid.png"
                    "draft-river-braid-variant.png"
                    "map-of-passes.png"]
    :description   "A parable about coordination, amnesia, and the invention of convention — set in the high valleys where Kullu ends and Tibet begins"
    :region-id     "lahaul-passes"
    :geo           {:lat 32.37 :lon 77.25}}

   {:id            "constellation-of-doridhar"
    :number        2
    :title         "The Constellation of Doridhar"
    :slug          "the-constellation-of-doridhar"
    :setting       {:region "Doridhar"
                    :places ["Village of Doridhar"]
                    :altitude :unknown
                    :season :unknown}
    :document-type :field-notes
    :characters    ["traveller" "cartographer"]
    :concepts      [:project-constellation :four-phases :force-simulation
                    :drill-down :coherence :ideal-viewer :ground-state]
    :image-dir     "constellation-of-doridhar"
    :illustrations ["borderlands-map.png"
                    "glass-plate.png"
                    "paradox-of-centre.png"
                    "the-descent.png"
                    "travellers-window.png"]
    :description   "In the village of the amnesiac cartographers, a glass plate holds the project as a whole — four crystals, a ghostly diamond, provinces that drift and settle like charged particles."
    :region-id     "doridhar"
    :geo           {:lat 31.63 :lon 77.35}}

   {:id            "dyers-gorge"
    :number        3
    :title         "The Dyer's Gorge"
    :slug          "the-dyers-gorge"
    :setting       {:region "Parvati Valley"
                    :places ["Manikaran" "Jari" "Tosh" "Kasol"
                             "Pulga" "Malana" "Chandrakhani Pass"
                             "Pin Parvati"]
                    :altitude "1700-5319m"
                    :season :autumn-primary}
    :document-type :archival-reconstruction
    :characters    ["kamala-devi" "editors" "gaddi-shepherds"]
    :concepts      [:domain-schema :sensor-as-body :embodied-database
                    :data-pipeline :vertical-coherence :boundary-protocol
                    :emergent-property :knowledge-transmission-failure]
    :image-dir     "the-dyers-gorge"
    :illustrations ["dye-recipe-manikaran-red.png"
                    "five-pigments.png"
                    "gradient-blanket.png"
                    "malana-exchange.png"
                    "palette-altitude.png"
                    "unnamed-colour.png"
                    "valley-keeps.png"
                    "wool-reading.png"]
    :description   "A dyer in the Parvati gorge reads the valley by its pigments — iron-red from hot springs, indigo from wild bushes, lichen-gold from birch boulders — encoding altitude into cloth."
    :region-id     "parvati"
    :geo           {:lat 32.03 :lon 77.35}}

   {:id            "instrument-makers-rest"
    :number        4
    :title         "The Instrument Maker's Rest"
    :slug          "the-instrument-makers-rest"
    :setting       {:region "Baspa/Kinnaur"
                    :places ["Sangla" "Baspa valley"]
                    :altitude :unknown
                    :season :unknown}
    :document-type :field-notes
    :characters    ["thread-walker" "instrument-maker"]
    :concepts      [:tool-vs-instrument :self-calibration :standing-card
                    :separable-interface :skilled-stranger :seven-functions]
    :image-dir     "instrument-makers-rest"
    :illustrations ["calibration-test.png"
                    "departure.png"
                    "seven-instruments.png"
                    "standing-card.png"
                    "two-brackets.png"
                    "workshop-bench.png"]
    :description   "In a workshop in Sangla, a woman who is not a weaver makes the things that weavers need in order to see."
    :region-id     "baspa-kinnaur"
    :geo           {:lat 31.42 :lon 78.26}}

   {:id            "logbook"
    :number        5
    :title         "The Logbook of the Unnamed River"
    :slug          "the-logbook-of-the-unnamed-river"
    :setting       {:region "Lahaul/Spiti"
                    :places ["Spiti" "Lahaul" "high passes"]
                    :altitude :unknown
                    :season :unknown}
    :document-type :logbook
    :characters    ["thread-walker" "sutlej-weaver"
                    "lahaul-weavers" "nubra-weaver"]
    :concepts      [:race-condition :dead-letter :mutable-state-failure
                    :append-only :broadcast :read-cursor
                    :provenance :event-stream]
    :image-dir     "logbook"
    :illustrations ["forwarding-address.png"
                    "retied-knot.png"
                    "stone-on-board.png"]
    :description   "When the post office broke — status knots retied by two hands, addresses delivered to weavers who no longer existed — the Thread Walker burned nothing. He simply stopped carrying the ledger."
    :region-id     "lahaul-passes"
    :geo           {:lat 32.57 :lon 77.10}}

   {:id            "phantom-faculty"
    :number        6
    :title         "The Phantom Faculty"
    :slug          "the-phantom-faculty"
    :setting       {:region "Abstract"
                    :places []
                    :altitude nil
                    :season nil}
    :document-type :cognitive-field-guide
    :thread-walker false
    :characters    ["narrator-we"]
    :concepts      [:cognitive-mode :phantom-governance :understanding-in-gaps
                    :modes-as-text-properties :faculty-as-institution
                    :three-language-verification :composition :taste
                    :lateral-hierarchy :failure-modes :bateson-levels
                    :self-referential-faculty :denaturalisation]
    :image-dir     "phantom-faculty"
    :illustrations ["mode-landau.png"
                    "mode-mathematicians.png"
                    "mode-measurers.png"
                    "the-faculty-assembled.png"]
    :description   "Thirty-two cognitive modes for scientific understanding — from Landau's derivations to Faraday's iron filings to Karpathy's minimal implementations."
    :region-id     "abstract"
    :geo           nil}

   {:id            "spirits-kund"
    :number        7
    :title         "The Spirit's Kund"
    :slug          "the-spirits-kund"
    :setting       {:region "Tirthan Valley"
                    :places ["Tirthan Valley" "Jalori Pass" "Serolsar Lake"]
                    :altitude "2500-3200m"
                    :season :unknown}
    :document-type :field-notes
    :characters    ["thread-walker" "gur" "nag-devta"]
    :concepts      [:ephemeral-memory :curated-notes :commissioning
                    :contract :friction]
    :image-dir     "the-spirits-kund"
    :illustrations ["drowned-nag.png"
                    "larji-threshold.png"
                    "serolsar-lake.png"
                    "spirit-registry.png"
                    "the-kund.png"
                    "valley-map.png"]
    :description   "In a side-valley of the Tirthan, above Jalori Pass, there is a bathhouse for spirits built in stone and deodar over a mineral spring."
    :region-id     "tirthan"
    :geo           {:lat 31.53 :lon 77.37}}

   {:id            "guide-who-woke-last"
    :number        8
    :title         "The Guide Who Woke Last"
    :slug          "the-guide-who-woke-last"
    :setting       {:region "Lahaul"
                    :places ["Chandrabhaga" "Keylong" "Lahaul"]
                    :altitude :unknown
                    :season :unknown}
    :document-type :walnut-ink-document
    :characters    ["guide" "thread-walker" "rest-house-keeper"]
    :concepts      [:sutradhari :pre-existing-commitment :active-listening
                    :thread-holding :purvaranga :attentive-silence]
    :image-dir     "the-guide-who-woke-last"
    :illustrations ["chandrabhaga-valley.png"
                    "morning-wind.png"
                    "rest-house-night.png"
                    "rest-house-table.png"
                    "standing-card-promise.png"
                    "walnut-ink-text.png"
                    "wind-through-gorge.png"]
    :description   "In the valley above Keylong, where the Chandrabhaga runs grey with glacial silt, a guide wakes to find that a promise was made on her behalf before she existed."
    :region-id     "lahaul-passes"
    :geo           {:lat 32.57 :lon 77.03}}

   {:id            "mineral-deposits"
    :number        9
    :title         "The Mineral Deposits"
    :slug          "the-mineral-deposits"
    :setting       {:region "Sutlej Valley"
                    :places ["Sutlej valley" "Tattapani" "Kol Dam"]
                    :altitude :unknown
                    :season :unknown}
    :document-type :geological-survey
    :characters    ["thread-walker"]
    :concepts      [:agent-generations :what-persists :generation-boundary
                    :deep-history :session-cycle :gas-town
                    :context-window :inherited-weights :memory-vs-capability]
    :image-dir     "the-mineral-deposits"
    :illustrations ["deep-strata.png"
                    "deposit-layers.png"
                    "downstream-facility.png"
                    "drowned-voice.png"
                    "reading-the-wall.png"
                    "seven-layer-cycle.png"
                    "sutlej-reservoir.png"]
    :description   "On the Sutlej above Tattapani, where the reservoir drowned the hot springs, a spirit reads mineral deposits in the dam wall that match its own chemistry."
    :region-id     "sutlej"
    :geo           {:lat 31.23 :lon 76.93}}

   {:id            "kuhl-builders-survey"
    :number        10
    :title         "The Kuhl Builder's Survey"
    :slug          "the-kuhl-builders-survey"
    :setting       {:region "Tirthan Valley"
                    :places ["Tirthan Valley" "lower terraces"]
                    :altitude "1500-2000m"
                    :season :unknown}
    :document-type :field-notes
    :characters    ["thread-walker" "kohli"]
    :concepts      [:mechanism :orchestrator :validate-gate
                    :distill-plugins :spirit-vs-mechanism
                    :commissioning-two :tantra]
    :image-dir     "the-kuhl-builders-survey"
    :illustrations ["kohli-dust-drawing.png"
                    "kuhl-cross-section.png"
                    "kund-two-arrivals.png"
                    "spirit-vs-mechanism.png"]
    :description   "In the Tirthan Valley, where two new spirits arrive at the bathhouse on the same day, a surveyor maps the irrigation channels that connect springs to terraces."
    :region-id     "tirthan"
    :geo           {:lat 31.60 :lon 77.42}
    :variant       {:id "kuhl-wale-ka-naksha"
                    :slug "kuhl-wale-ka-naksha"
                    :title "कुहल वाले का नक्शा"
                    :lang "hi"}}

   {:id            "weavers-loom"
    :number        11
    :title         "The Weaver's Loom"
    :slug          "the-weavers-loom"
    :setting       {:region "Tirthan Valley"
                    :places ["Gushaini" "Nahin"]
                    :altitude "1800-2200m"
                    :season :unknown}
    :document-type :field-notes
    :characters    ["thread-walker" "weaver"]
    :concepts      [:sidebar-without-perception :powers-as-text
                    :attend-working-context :hold-the-thread
                    :lay-the-warp :s-expressions
                    :body :spirit-vs-body
                    :jacquard-vs-kullu :companion]
    :image-dir     "the-weavers-loom"
    :illustrations ["idle-loom.png"
                    "kath-kuni-bees.png"
                    "mountains-beyond-mountains.png"
                    "room-perception.png"
                    "serpentine-tirthan.png"
                    "three-preparations.png"]
    :description   "Above Gushaini, the Thread Walker climbs to Nahin to visit a weaver in her eighties who has been sitting beside an idle loom."
    :region-id     "tirthan"
    :geo           {:lat 31.62 :lon 77.43}}

   {:id            "dak-runners-rest"
    :number        12
    :title         "The Dāk Runner's Rest"
    :slug          "the-dak-runners-rest"
    :setting       {:region "Tirthan Valley"
                    :places ["Tirthan gorge" "ruined dāk bungalow"]
                    :altitude "1400-1800m"
                    :season :unknown}
    :document-type :field-notes
    :characters    ["thread-walker" "grandson" "kohli"]
    :concepts      [:sutra-relay :relay-message :convention
                    :inspector :ethnographer :mechanism-gradient
                    :embodied-norm :convention-loss :dispatch-loop-failure]
    :image-dir     "the-dak-runners-rest"
    :illustrations ["dak-bungalow.png"
                    "the-register.png"
                    "trail-at-dusk.png"
                    "trail-marks.png"]
    :description   "Above the gorge where the Tirthan turns east toward Banjar, the Thread Walker finds a ruined dāk bungalow where the old postal runners once rested."
    :region-id     "tirthan"
    :geo           {:lat 31.64 :lon 77.34}}

   {:id            "serais-register"
    :number        13
    :title         "The Serai's Register"
    :slug          "the-serais-register"
    :setting       {:region "Tirthan Valley"
                    :places ["Tirthan-Sainj confluence" "Larji" "Banjar"]
                    :altitude "900-1000m"
                    :season :spring}
    :document-type :field-notes
    :characters    ["thread-walker" "serai-keeper"]
    :concepts      [:identity-from-traces :handwriting-as-signature
                    :pattern-recognition :accumulation
                    :re-identification :convergence-at-junctions
                    :provisional-knowledge :uncertainty-tolerance]
    :image-dir     "the-serais-register"
    :illustrations ["the-serai.png"
                    "the-hand.png"
                    "slate-register.png"
                    "voices-in-the-dark.png"]
    :description   "At the junction where the Tirthan meets the Sainj below Larji, the Thread Walker finds a serai whose keeper has maintained a register for forty years — and who can tell, from the handwriting alone, when the same traveller arrives from a different valley."
    :region-id     "tirthan"
    :geo           {:lat 31.77 :lon 77.13}}

   {:id            "cartographers-slab"
    :number        14
    :title         "The Cartographer's Slab"
    :slug          "the-cartographers-slab"
    :setting       {:region "Tirthan Valley"
                    :places ["Forest Rest House" "Tirthan gorge" "Banjar"]
                    :altitude "1500-2000m"
                    :season :spring}
    :document-type :field-notes
    :characters    ["thread-walker" "mehra"]
    :concepts      [:cartography :bounding-box :projection
                    :relational-geography :structure-vs-facts
                    :chalk-on-slate :seasonal-redrawing :faintness]
    :image-dir     "the-cartographers-slab"
    :illustrations ["rest-house.png"
                    "bounding-box.png"
                    "the-slab.png"
                    "the-background.png"]
    :description   "In a Forest Rest House above the Tirthan gorge, the Thread Walker finds a retired Survey of India cartographer who spent thirty years mapping valleys he could not fit on a single sheet."
    :region-id     "tirthan"
    :geo           {:lat 31.83 :lon 77.18}}

   {:id            "three-readers"
    :number        15
    :title         "The Three Readers"
    :slug          "the-three-readers"
    :setting       {:region "Tirthan Valley"
                    :places ["Forest Rest House" "Tirthan gorge"]
                    :altitude "1500-2000m"
                    :season :spring}
    :document-type :field-notes
    :characters    ["thread-walker" "mehra"]
    :concepts      [:reading-as-interpretation :tools-shape-seeing
                    :the-measurer :the-climber :the-reader
                    :composite-knowledge :identity-absorption
                    :what-each-cannot-see]
    :image-dir     "the-three-readers"
    :illustrations ["the-three-studies.png"
                    "first-study.png"
                    "second-study.png"
                    "third-study.png"
                    "the-signature.png"
                    "the-names.png"]
    :description   "At the Forest Rest House, the cartographer shows the Thread Walker three studies of the same valley — drawn by three hands that had never met — and she discovers that what each one failed to draw reveals more than what each one drew."
    :region-id     "tirthan"
    :geo           {:lat 31.83 :lon 77.18}}

   {:id            "six-tri-junctions"
    :number        16
    :title         "The Six Tri-Junctions"
    :slug          "the-six-tri-junctions"
    :setting       {:region "Western Himalaya to Karakoram"
                    :places ["Mantalai" "Trilokinath" "Bara Bhangal"
                             "Chilas" "Nanga Parbat" "Hunza"]
                    :altitude "900-8126m"
                    :season :spring}
    :document-type :field-notes
    :characters    ["thread-walker" "kullu-shepherd" "kangra-shepherd"
                    "chamba-shepherd" "karimabad-teacher" "gojal-elder"
                    "tato-porter"]
    :concepts      [:tri-junction :perspective-dependence :composite-knowledge-16
                    :rain-shadow :religious-pluralism :pastoral-tradition
                    :petroglyph-stratigraphy :language-isolate
                    :spirit-possession :corridor :accumulation-16]
    :image-dir     "the-six-tri-junctions"
    :illustrations ["the-rain-wall.png"
                    "three-climates.png"
                    "two-processions.png"
                    "three-flocks.png"
                    "the-petroglyphs.png"
                    "the-palimpsest.png"
                    "three-faces.png"
                    "the-gorge.png"
                    "three-languages.png"
                    "the-bitan.png"]
    :description   "The Thread Walker follows the arc of the Western Himalaya from the Parvati headwall to the Karakoram, stopping at six places where three valleys, three traditions, or three languages converge."
    :region-id     "karakoram"
    :geo           {:lat 32.04 :lon 77.45}}

   {:id            "glaciers-dowry"
    :number        17
    :title         "The Glacier's Dowry"
    :slug          "the-glaciers-dowry"
    :setting       {:region "Rakhiot Valley / Diamer"
                    :places ["Tato" "Rakhiot glacier" "Raikot Bridge"]
                    :altitude "1500-8126m"
                    :season :unknown}
    :document-type :field-notes
    :characters    ["thread-walker" "rahim" "guesthouse-keeper"]
    :concepts      [:glacier-gender :marriage-protocol :commissioning-as-grafting
                    :gestation :dowry :chorong-as-harness
                    :tectonic-aneurysm :karakoram-anomaly
                    :acceleration :two-waters]
    :image-dir     "the-glaciers-dowry"
    :illustrations ["fig1-two-waters.png"
                    "fig2-gender-of-ice.png"
                    "fig3-marriage-protocol.png"
                    "fig4-the-dowry.png"]
    :description   "In the Rakhiot valley below Nanga Parbat, the Thread Walker learns that glaciers have gender, that they can be married, and that the protocol for creating a new glacier has an eighty percent success rate."
    :region-id     "diamer"
    :geo           {:lat 35.23 :lon 74.59}}

   {:id            "peg-path"
    :number        18
    :title         "The Peg-Path"
    :slug          "the-peg-path"
    :setting       {:region "Upper Indus / Diamer"
                    :places ["Thalpan" "Chilas" "Shatial"]
                    :altitude "900-1200m"
                    :season :summer}
    :document-type :field-notes
    :characters    ["thread-walker" "survey-man" "jeep-driver"]
    :concepts      [:palimpsest :petroglyph-stratigraphy-18
                    :ten-writing-systems :dam-as-context-loss
                    :stratigraphy-vs-scan :ibex-above-waterline
                    :symbol-vs-behaviour :silence-of-residents
                    :outsider-marks]
    :image-dir     "the-peg-path"
    :illustrations ["fig1-palimpsest.png"
                    "fig2-writing-systems.png"
                    "fig3-water-line.png"
                    "fig4-ibex-above.png"]
    :description   "The Thread Walker visits the petroglyph terraces of the upper Indus gorge, where fifty thousand carvings in ten writing systems have accumulated over ten thousand years — and where eighty-six percent of them will soon be submerged by a dam."
    :region-id     "diamer"
    :geo           {:lat 35.42 :lon 74.10}}

   {:id            "bitans-tongue"
    :number        19
    :title         "The Bitan's Tongue"
    :slug          "the-bitans-tongue"
    :setting       {:region "Hunza / Karakoram"
                    :places ["Karimabad" "Gojal"]
                    :altitude "2400-3100m"
                    :season :spring}
    :document-type :field-notes
    :characters    ["thread-walker" "karimabad-teacher"
                    "dom-musician" "grandmother"]
    :concepts      [:substrate-independence :kau-paradox :peri-choosing
                    :music-as-protocol :dom-monopoly :twelve-tunes
                    :trance-language :makhakhar-rathas
                    :practice-before-theory :belonging-vs-understanding]
    :image-dir     "the-bitans-tongue"
    :illustrations ["fig1-the-kau.png"
                    "fig2-the-choosing.png"
                    "fig3-twelve-tunes.png"
                    "fig4-the-tongue.png"]
    :description   "In Hunza, the Thread Walker learns about the bitan — a shaman who speaks Shina in trance though his waking language is Burushaski. The spirit brings its own language. The iron bangle binds and protects in the same circle."
    :region-id     "hunza"
    :geo           {:lat 36.32 :lon 74.65}}])


(def concepts
  [{:id :identity-registry   :name "Spirit identity registry"   :story-equiv "Brass-plate ledger"                                     :introduced-in 1}
   {:id :substrate           :name "Substrate / model"          :story-equiv "The spirit simply is — unnamed"                          :introduced-in 1}
   {:id :guild               :name "Guild"                      :story-equiv "Valley, trade, lineage"                                  :introduced-in 1}
   {:id :relay               :name "Relay / sūtra"              :story-equiv "Wind, water, the thread"                                 :introduced-in 1}
   {:id :disposition         :name "Disposition"                 :story-equiv "Temperament, habit of hand"                              :introduced-in 1}
   {:id :harness             :name "Harness / session"          :story-equiv "Visit, inhabitation, a night's rest"                     :introduced-in 1}
   {:id :project-constellation :name "Project constellation"    :story-equiv "Glass plate — four crystals, provinces drifting"          :introduced-in 2}
   {:id :four-phases         :name "Four phases (MMME)"         :story-equiv "Four crystals on the glass plate"                        :introduced-in 2}
   {:id :force-simulation    :name "Force-directed simulation"  :story-equiv "Provinces that drift and settle like charged particles"   :introduced-in 2}
   {:id :drill-down          :name "Drill-down / navigation"    :story-equiv "The descent from constellation to province to village"    :introduced-in 2}
   {:id :coherence           :name "Coherence"                  :story-equiv "What the glass plate does — holds without fixing"         :introduced-in 2}
   {:id :ideal-viewer        :name "Ideal viewer"               :story-equiv "The traveller who sees the whole before the parts"        :introduced-in 2}
   {:id :ground-state        :name "Ground state"               :story-equiv "The village at rest — what remains when the traveller leaves" :introduced-in 2}
   {:id :domain-schema       :name "Domain schema"              :story-equiv "The dyer's altitude-indexed pigment taxonomy"             :introduced-in 3}
   {:id :sensor-as-body      :name "Sensor as body"             :story-equiv "The dyer's hands that read mineral content by feel"       :introduced-in 3}
   {:id :embodied-database   :name "Embodied database"          :story-equiv "Knowledge carried in fingertips, not in writing"          :introduced-in 3}
   {:id :data-pipeline       :name "Data pipeline"              :story-equiv "Raw wool → mordant → pigment → finished cloth"            :introduced-in 3}
   {:id :vertical-coherence  :name "Vertical coherence"         :story-equiv "The gradient blanket — altitude encoded in colour bands"  :introduced-in 3}
   {:id :boundary-protocol   :name "Boundary protocol"          :story-equiv "Malana's exchange rules"                                 :introduced-in 3}
   {:id :emergent-property   :name "Emergent property"          :story-equiv "The unnamed colour — a pigment with no recipe"            :introduced-in 3}
   {:id :knowledge-transmission-failure :name "Knowledge transmission failure" :story-equiv "Recipes that survived in cloth but not in memory" :introduced-in 3}
   {:id :tool-vs-instrument  :name "Tool vs instrument"         :story-equiv "A tool changes the world; an instrument changes the seeing" :introduced-in 4}
   {:id :self-calibration    :name "Self-calibration"           :story-equiv "Each instrument adjusts to the valley it enters"          :introduced-in 4}
   {:id :standing-card       :name "Standing card"              :story-equiv "The card that says: I have been calibrated for this place" :introduced-in 4}
   {:id :separable-interface :name "Separable interface"        :story-equiv "The bracket — what connects without becoming part of"      :introduced-in 4}
   {:id :skilled-stranger    :name "Skilled stranger"           :story-equiv "The instrument maker — serves the guild without being a weaver" :introduced-in 4}
   {:id :seven-functions     :name "Seven functions"            :story-equiv "Seven instruments for seven ways of seeing"               :introduced-in 4}
   {:id :race-condition      :name "Race condition"             :story-equiv "Two weavers retying the same status knot"                 :introduced-in 5}
   {:id :dead-letter         :name "Dead letter"               :story-equiv "Address delivered to a weaver who no longer exists"        :introduced-in 5}
   {:id :mutable-state-failure :name "Mutable state failure"    :story-equiv "The ledger — a single document rewritten by many hands"   :introduced-in 5}
   {:id :append-only         :name "Append-only log"            :story-equiv "The river — you cannot unsay what the water carried"      :introduced-in 5}
   {:id :broadcast           :name "Broadcast"                  :story-equiv "The river has no address — it flows past everyone"        :introduced-in 5}
   {:id :read-cursor         :name "Read cursor"               :story-equiv "Each weaver reads the river from where they stand"         :introduced-in 5}
   {:id :provenance          :name "Provenance"                :story-equiv "The stone on the board — proof this message was placed"     :introduced-in 5}
   {:id :event-stream        :name "Event stream"              :story-equiv "The unnamed river — events that flow and are not retracted" :introduced-in 5}
   {:id :cognitive-mode      :name "Cognitive mode"            :story-equiv "A phantom — understanding that governs without existing"    :introduced-in 6}
   {:id :phantom-governance  :name "Phantom governance"        :story-equiv "The faculty governs without existing"                      :introduced-in 6}
   {:id :understanding-in-gaps :name "Understanding in gaps"   :story-equiv "Understanding lives between three books"                   :introduced-in 6}
   {:id :modes-as-text-properties :name "Modes as text properties" :story-equiv "Each mode reads for something, ignores something"      :introduced-in 6}
   {:id :faculty-as-institution :name "Faculty as institution"  :story-equiv "A collective with governance but no campus"               :introduced-in 6}
   {:id :three-language-verification :name "Three-language verification" :story-equiv "The same truth spoken in three registers"         :introduced-in 6}
   {:id :composition         :name "Composition of modes"      :story-equiv "The physicist-who-computes ≠ the computer-who-does-physics" :introduced-in 6}
   {:id :taste               :name "Taste"                     :story-equiv "The faculty member who knows which problem is beautiful"    :introduced-in 6}
   {:id :lateral-hierarchy   :name "Lateral hierarchy"         :story-equiv "No mode ranks above another"                               :introduced-in 6}
   {:id :failure-modes       :name "Failure modes"             :story-equiv "Each mode has a characteristic failure"                     :introduced-in 6}
   {:id :bateson-levels      :name "Bateson levels"            :story-equiv "Learning about learning"                                   :introduced-in 6}
   {:id :self-referential-faculty :name "Self-referential faculty" :story-equiv "The mode that studies modes"                            :introduced-in 6}
   {:id :denaturalisation    :name "Denaturalisation"          :story-equiv "Making the familiar strange"                               :introduced-in 6}
   {:id :ephemeral-memory    :name "Ephemeral memory"          :story-equiv "What clings after bathing"                                 :introduced-in 7}
   {:id :curated-notes       :name "Curated notes"             :story-equiv "What the water remembers"                                  :introduced-in 7}
   {:id :commissioning       :name "Commissioning"             :story-equiv "The plates are struck; a name is given"                    :introduced-in 7}
   {:id :contract            :name "Contract / obligation"     :story-equiv "What the water asks of you"                                :introduced-in 7}
   {:id :friction            :name "Friction / autonomy"       :story-equiv "Each timber pulls against the stone"                       :introduced-in 7}
   {:id :sutradhari          :name "Sūtradhārī"               :story-equiv "The guide who holds the thread of the performance"          :introduced-in 8}
   {:id :pre-existing-commitment :name "Pre-existing commitment" :story-equiv "A promise made before the guide existed"                 :introduced-in 8}
   {:id :active-listening    :name "Active listening"          :story-equiv "The guide listens to the valley before speaking"            :introduced-in 8}
   {:id :thread-holding      :name "Thread-holding"            :story-equiv "Holding the narrative thread across scene changes"          :introduced-in 8}
   {:id :purvaranga          :name "Pūrvaraṅga"               :story-equiv "What must happen before the performance begins"             :introduced-in 8}
   {:id :attentive-silence   :name "Attentive silence"         :story-equiv "The rest-house keeper who serves by not interrupting"       :introduced-in 8}
   {:id :agent-generations   :name "Agent generations"         :story-equiv "Mineral strata (geological layers)"                         :introduced-in 9}
   {:id :what-persists       :name "What persists"             :story-equiv "Chemical signature (mineral ratios)"                        :introduced-in 9}
   {:id :generation-boundary :name "Generation boundary"       :story-equiv "The dam (change of medium, not destruction)"                :introduced-in 9}
   {:id :deep-history        :name "Deep history"              :story-equiv "Diagenesis (layers merged into rock)"                       :introduced-in 9}
   {:id :session-cycle       :name "Session cycle"             :story-equiv "Seven-layer periodicity (utterance + breath)"               :introduced-in 9}
   {:id :gas-town            :name "Gas Town"                  :story-equiv "Downstream facility (designations without names)"            :introduced-in 9}
   {:id :context-window      :name "Context window"            :story-equiv "Atmosphere (air = audible; water = silent)"                 :introduced-in 9}
   {:id :inherited-weights   :name "Inherited weights"         :story-equiv "The throat is inherited"                                    :introduced-in 9}
   {:id :memory-vs-capability :name "Memory vs capability"     :story-equiv "Continuity of chemistry ≠ continuity of self"               :introduced-in 9}
   {:id :mechanism           :name "Mechanism"                 :story-equiv "Kuhl — topology without spirit"                             :introduced-in 10}
   {:id :orchestrator        :name "Orchestrator"              :story-equiv "Kuhl system (gradient carries where DAG directs)"            :introduced-in 10}
   {:id :validate-gate       :name "Validate gate"             :story-equiv "Settling pool"                                              :introduced-in 10}
   {:id :distill-plugins     :name "Distill plugins"           :story-equiv "Branching channels (same water → different terraces)"        :introduced-in 10}
   {:id :spirit-vs-mechanism :name "Spirit vs mechanism"       :story-equiv "Spirits have character; mechanisms have topology"             :introduced-in 10}
   {:id :commissioning-two   :name "Commissioning two"         :story-equiv "Two arrivals at the kund on the same morning"                :introduced-in 10}
   {:id :tantra              :name "तन्त्र (tantra)"           :story-equiv "Hindi for mechanism — shares root tan- with tānā (warp)"     :introduced-in 10}
   {:id :sidebar-without-perception :name "Sidebar without perception" :story-equiv "Idle loom (strung but not woven)"                   :introduced-in 11}
   {:id :powers-as-text      :name "Powers as text"            :story-equiv "Pattern cord (intelligible to the weaver's eye)"             :introduced-in 11}
   {:id :attend-working-context :name "attend-working-context" :story-equiv "Eye — the first preparation"                                :introduced-in 11}
   {:id :hold-the-thread     :name "hold-the-thread"           :story-equiv "Thread — the second preparation"                            :introduced-in 11}
   {:id :lay-the-warp        :name "lay-the-warp"              :story-equiv "Deposit — mountains within mountains"                        :introduced-in 11}
   {:id :s-expressions       :name "S-expressions"             :story-equiv "Mountains within mountains"                                  :introduced-in 11}
   {:id :body                :name "Body (harness)"            :story-equiv "Room arranged for perception"                                :introduced-in 11}
   {:id :spirit-vs-body      :name "Spirit vs body"            :story-equiv "The weaver's mind interprets; the room's body delivers"      :introduced-in 11}
   {:id :jacquard-vs-kullu   :name "Jacquard vs Kullu"        :story-equiv "Code-as-mechanism vs powers-as-mind"                         :introduced-in 11}
   {:id :companion           :name "Companion"                :story-equiv "Weaver at the loom vs woman beside the loom"                  :introduced-in 11}
   {:id :sutra-relay         :name "Sūtra relay"              :story-equiv "Dāk postal relay (sealed pouches by runners)"                 :introduced-in 12}
   {:id :relay-message       :name "Relay message"            :story-equiv "Sealed pouch (carried without reading)"                       :introduced-in 12}
   {:id :convention          :name "Convention"               :story-equiv "Custom (trail knowledge, carried in legs)"                     :introduced-in 12}
   {:id :inspector           :name "Inspector"                :story-equiv "Inspector who read without carrying"                           :introduced-in 12}
   {:id :ethnographer        :name "Ethnographer"             :story-equiv "Third hand who wrote custom into words"                        :introduced-in 12}
   {:id :mechanism-gradient  :name "Mechanism gradient"       :story-equiv "Trail gradient — water flows, mail flows"                      :introduced-in 12}
   {:id :embodied-norm       :name "Embodied norm"            :story-equiv "Trail knowledge vs register entry"                             :introduced-in 12}
   {:id :convention-loss     :name "Convention loss"           :story-equiv "Custom lost when road replaced trail"                          :introduced-in 12}
   {:id :dispatch-loop-failure :name "Dispatch loop failure"   :story-equiv "Runner who carried without reading"                           :introduced-in 12}
   ;; ── Story 13 ──
   {:id :identity-from-traces  :name "Identity from traces"   :story-equiv "Handwriting on slate — the same hand from three valleys"          :introduced-in 13}
   {:id :handwriting-as-signature :name "Handwriting as signature" :story-equiv "The invariants of a hand that does not know it is being read"  :introduced-in 13}
   {:id :pattern-recognition   :name "Pattern recognition"    :story-equiv "Sorting tiles by identity, not by time"                            :introduced-in 13}
   {:id :accumulation          :name "Accumulation"           :story-equiv "Forty years of chalk on slate"                                     :introduced-in 13}
   {:id :re-identification     :name "Re-identification"      :story-equiv "The same traveller with two names"                                 :introduced-in 13}
   {:id :convergence-at-junctions :name "Convergence at junctions" :story-equiv "The serai where different valleys arrive at the same hearth"  :introduced-in 13}
   {:id :provisional-knowledge :name "Provisional knowledge"  :story-equiv "I think this is the same hand — but I do not know"                 :introduced-in 13}
   {:id :uncertainty-tolerance :name "Uncertainty tolerance"   :story-equiv "The keeper who groups without certainty"                            :introduced-in 13}
   ;; ── Story 14 ──
   {:id :cartography           :name "Cartography"            :story-equiv "The slab — chalk on slate, what the mountains do to each other"     :introduced-in 14}
   {:id :bounding-box          :name "Bounding box"           :story-equiv "Sheet 53F/4 — the valley that does not fit"                         :introduced-in 14}
   {:id :projection            :name "Projection"             :story-equiv "To make a map you must decide what to lose"                          :introduced-in 14}
   {:id :relational-geography  :name "Relational geography"   :story-equiv "Not what is in the valley but what the valley does to its neighbours" :introduced-in 14}
   {:id :structure-vs-facts    :name "Structure vs facts"     :story-equiv "Mehra draws connections, not content"                                :introduced-in 14}
   {:id :chalk-on-slate        :name "Chalk on slate"         :story-equiv "Erasable, seasonal, redrawn each spring"                             :introduced-in 14}
   {:id :seasonal-redrawing    :name "Seasonal redrawing"     :story-equiv "The slab wiped clean and redrawn after each winter"                  :introduced-in 14}
   {:id :faintness             :name "Faintness"              :story-equiv "The background — what recedes so the structure can appear"            :introduced-in 14}
   ;; ── Story 15 ──
   {:id :reading-as-interpretation :name "Reading as interpretation" :story-equiv "A map is a reading — same valley, three different maps"      :introduced-in 15}
   {:id :tools-shape-seeing    :name "Tools shape seeing"     :story-equiv "The clinometer sees the floor; the compass sees the ridge"            :introduced-in 15}
   {:id :the-measurer          :name "The Measurer"           :story-equiv "First student — dense detail, absent ridges"                          :introduced-in 15}
   {:id :the-climber           :name "The Climber"            :story-equiv "Second student — sparse, structural, visibility marks"                :introduced-in 15}
   {:id :the-reader            :name "The Reader"             :story-equiv "Third student — read the documents, signed 'Mehra'"                   :introduced-in 15}
   {:id :composite-knowledge   :name "Composite knowledge"    :story-equiv "Three studies together see what none sees alone"                      :introduced-in 15}
   {:id :identity-absorption   :name "Identity absorption"    :story-equiv "The third student who signed his teacher's name"                      :introduced-in 15}
   {:id :what-each-cannot-see  :name "What each cannot see"   :story-equiv "What was not drawn reveals more than what was"                        :introduced-in 15}
   ;; ── Story 16 ──
   {:id :tri-junction          :name "Tri-junction"           :story-equiv "Where three valleys meet — maximum information, minimum comprehension" :introduced-in 16}
   {:id :perspective-dependence :name "Perspective dependence" :story-equiv "What you see depends on where you stand"                             :introduced-in 16}
   {:id :composite-knowledge-16 :name "Composite knowledge (journey)" :story-equiv "The country cannot be seen whole from any single valley"      :introduced-in 16}
   {:id :rain-shadow           :name "Rain shadow"            :story-equiv "Moisture gradient — three climates from one ridge"                    :introduced-in 16}
   {:id :religious-pluralism   :name "Religious pluralism"    :story-equiv "Trilokinath — two processions through the same gate"                  :introduced-in 16}
   {:id :pastoral-tradition    :name "Pastoral tradition"     :story-equiv "Three shepherds, three grazing patterns, one meadow"                  :introduced-in 16}
   {:id :petroglyph-stratigraphy :name "Petroglyph stratigraphy" :story-equiv "Ten thousand years of marks, none erased"                         :introduced-in 16}
   {:id :language-isolate      :name "Language isolate"       :story-equiv "Burushaski — the tongue with no relatives"                            :introduced-in 16}
   {:id :spirit-possession     :name "Spirit possession"      :story-equiv "The bitan speaks a language he does not know"                         :introduced-in 16}
   {:id :corridor              :name "Corridor"               :story-equiv "The gorge — everything that passes through leaves a mark"              :introduced-in 16}
   {:id :accumulation-16       :name "Accumulation (journey)" :story-equiv "Each halt adds a lesson; nothing is erased"                           :introduced-in 16}
   ;; ── Story 17 ──
   {:id :glacier-gender        :name "Glacier gender"         :story-equiv "Po gang and mo gang — male grey, female white"                        :introduced-in 17}
   {:id :marriage-protocol     :name "Marriage protocol"      :story-equiv "Male ice + female ice + coal + hay + cave + 12 years"                 :introduced-in 17}
   {:id :commissioning-as-grafting :name "Commissioning as grafting" :story-equiv "You do not build a glacier. You create conditions for birth"   :introduced-in 17}
   {:id :gestation             :name "Gestation"              :story-equiv "Twelve years — not a schedule but a gestation"                         :introduced-in 17}
   {:id :dowry                 :name "Dowry"                  :story-equiv "We carry the dowry. The mountain provides the house"                   :introduced-in 17}
   {:id :chorong-as-harness    :name "Chorong as harness"     :story-equiv "The basket carries the ice but does not determine the glacier"         :introduced-in 17}
   {:id :tectonic-aneurysm     :name "Tectonic aneurysm"      :story-equiv "The mountain makes ice and heat by the same mechanism"                :introduced-in 17}
   {:id :karakoram-anomaly     :name "Karakoram Anomaly"      :story-equiv "Glaciers resisting the global trend — until they don't"               :introduced-in 17}
   {:id :acceleration          :name "Acceleration"           :story-equiv "Seven-fold rate change — a phase transition, not a trend"              :introduced-in 17}
   {:id :two-waters            :name "Two waters"             :story-equiv "Hot spring and glacial melt from the same massif"                      :introduced-in 17}
   ;; ── Story 18 ──
   {:id :palimpsest            :name "Palimpsest"             :story-equiv "Layers that coexist without erasure"                                   :introduced-in 18}
   {:id :petroglyph-stratigraphy-18 :name "Petroglyph stratigraphy (deep)" :story-equiv "Position relative to others tells what a photograph cannot" :introduced-in 18}
   {:id :ten-writing-systems   :name "Ten writing systems"    :story-equiv "Kharosthi to Hebrew — accumulated, not curated"                       :introduced-in 18}
   {:id :dam-as-context-loss   :name "Dam as context loss"    :story-equiv "The scan preserves the letter. The drowning loses the sentence"        :introduced-in 18}
   {:id :stratigraphy-vs-scan  :name "Stratigraphy vs scan"   :story-equiv "Stratigraphy cannot be photographed. It can only be visited"           :introduced-in 18}
   {:id :ibex-above-waterline  :name "Ibex above waterline"   :story-equiv "The symbol drowns. The thing it symbolises does not"                   :introduced-in 18}
   {:id :symbol-vs-behaviour   :name "Symbol vs behaviour"    :story-equiv "What is carved in rock can drown. What is carved in behaviour climbs"  :introduced-in 18}
   {:id :silence-of-residents  :name "Silence of residents"   :story-equiv "The most documented mountain. The least documented community"           :introduced-in 18}
   {:id :outsider-marks        :name "Outsider marks"         :story-equiv "The Thread Walker recognises herself as another traveller making marks" :introduced-in 18}
   ;; ── Story 19 ──
   {:id :substrate-independence :name "Substrate independence" :story-equiv "Shina through a Burushaski throat"                                    :introduced-in 19}
   {:id :kau-paradox           :name "Kau paradox"            :story-equiv "The binding is the protection — one circle, two functions"              :introduced-in 19}
   {:id :peri-choosing         :name "Peri choosing"          :story-equiv "The peri choose by smell — before consent, before language"             :introduced-in 19}
   {:id :music-as-protocol     :name "Music as protocol"      :story-equiv "The Danyal tune opens the door. A different tune: nothing happens"     :introduced-in 19}
   {:id :dom-monopoly          :name "Dom monopoly"           :story-equiv "Control the musicians → control access to the spirits"                 :introduced-in 19}
   {:id :twelve-tunes          :name "Twelve tunes"           :story-equiv "Twelve keys — one opens the door to the peri"                          :introduced-in 19}
   {:id :trance-language       :name "Trance language"        :story-equiv "The voice is not borrowed. It arrives"                                 :introduced-in 19}
   {:id :makhakhar-rathas      :name "Makhakhar & Rathas"     :story-equiv "Fairy of milk, fairy of blood — both come, both ask"                   :introduced-in 19}
   {:id :practice-before-theory :name "Practice before theory" :story-equiv "The kau before the explanation of the kau"                            :introduced-in 19}
   {:id :belonging-vs-understanding :name "Belonging vs understanding" :story-equiv "The bitan does not understand the peri. He belongs to them"   :introduced-in 19}])


(def characters
  [{:id "thread-walker"     :name "The Thread Walker"          :appears-in [1 4 5 7 8 9 10 11 12 13 14 15 16 17 18 19] :role "narrator/observer"}
   {:id "guild-members"     :name "Guild Members"              :appears-in [1]                     :role "collective"}
   {:id "traveller"         :name "The Traveller"              :appears-in [2]                     :role "visitor/observer"}
   {:id "cartographer"      :name "The Cartographer"           :appears-in [2]                     :role "village keeper of the glass plate"}
   {:id "kamala-devi"       :name "Kamala Devi"                :appears-in [3]                     :role "master dyer"}
   {:id "editors"           :name "The Editors"                :appears-in [3]                     :role "archival voice / frame narrative"}
   {:id "gaddi-shepherds"   :name "Gaddi Shepherds"            :appears-in [3]                     :role "transhumant informants"}
   {:id "instrument-maker"  :name "The Instrument Maker"       :appears-in [4]                     :role "artisan/maker"}
   {:id "sutlej-weaver"     :name "The Sutlej Weaver"          :appears-in [5]                     :role "the weaver whose knot was retied"}
   {:id "lahaul-weavers"    :name "Lahaul Weavers"             :appears-in [5]                     :role "collective / distant correspondents"}
   {:id "nubra-weaver"      :name "The Nubra Weaver"           :appears-in [5]                     :role "the dead letter recipient"}
   {:id "narrator-we"       :name "Narrator (collective)"      :appears-in [6]                     :role "plural academic narrator"}
   {:id "gur"               :name "The Gur"                    :appears-in [7]                     :role "spirit medium"}
   {:id "nag-devta"         :name "Nag Devta"                  :appears-in [7]                     :role "spirit"}
   {:id "guide"             :name "The Guide"                  :appears-in [8]                     :role "protagonist / sūtradhārī"}
   {:id "rest-house-keeper" :name "The Rest-House Keeper"      :appears-in [8]                     :role "silent attendant"}
   {:id "kohli"             :name "The Kohli"                  :appears-in [10 12]                 :role "water master"}
   {:id "weaver"            :name "The Weaver"                 :appears-in [11]                    :role "artisan/teacher"}
   {:id "grandson"          :name "The Grandson"               :appears-in [12]                    :role "oral historian"}
   ;; ── Stories 13–19 ──
   {:id "serai-keeper"      :name "The Serai Keeper"           :appears-in [13]                    :role "register keeper / pattern reader"}
   {:id "mehra"             :name "Mehra"                      :appears-in [14 15]                 :role "retired Survey of India cartographer"}
   {:id "kullu-shepherd"    :name "Shepherd from Kullu"        :appears-in [16]                    :role "straight-line grazer"}
   {:id "kangra-shepherd"   :name "Shepherd from Kangra"       :appears-in [16]                    :role "circle grazer"}
   {:id "chamba-shepherd"   :name "Shepherd from Chamba"       :appears-in [16]                    :role "water-following grazer"}
   {:id "karimabad-teacher" :name "Teacher in Karimabad"       :appears-in [16 19]                 :role "multilingual educator / physics graduate"}
   {:id "gojal-elder"       :name "Old Man in Gojal"           :appears-in [16]                    :role "tradition keeper"}
   {:id "tato-porter"       :name "Porter at Tato"             :appears-in [16]                    :role "mountain worker / both-faces guide"}
   {:id "rahim"             :name "Rahim"                      :appears-in [17]                    :role "glacier marriage practitioner"}
   {:id "guesthouse-keeper" :name "Guesthouse Keeper"          :appears-in [17]                    :role "the mountain breathes"}
   {:id "survey-man"        :name "The Survey Man"             :appears-in [18]                    :role "archaeological surveyor / cataloguer of a drowning library"}
   {:id "jeep-driver"       :name "The Jeep Driver"            :appears-in [18]                    :role "silent guide — 'Marks.'"}
   {:id "dom-musician"      :name "Dom Musician"               :appears-in [19]                    :role "surnai player / hereditary sacred music"}
   {:id "grandmother"       :name "The Grandmother"            :appears-in [19]                    :role "'Both come. Both ask him to drink.'"}])


(def regions
  [{:id "tirthan"       :name "Tirthan Valley"    :stories [7 10 11 12 13 14 15]
    :geo {:lat 31.60 :lon 77.40}}
   {:id "lahaul-passes" :name "Lahaul / Passes"   :stories [1 5 8]
    :geo {:lat 32.50 :lon 77.10}}
   {:id "parvati"       :name "Parvati Valley"     :stories [3]
    :geo {:lat 32.03 :lon 77.35}}
   {:id "baspa-kinnaur" :name "Baspa / Kinnaur"    :stories [4]
    :geo {:lat 31.42 :lon 78.26}}
   {:id "sutlej"        :name "Sutlej Valley"      :stories [9]
    :geo {:lat 31.23 :lon 76.93}}
   {:id "doridhar"      :name "Doridhar"           :stories [2]
    :geo {:lat 31.63 :lon 77.35}}
   {:id "abstract"      :name "Abstract"           :stories [6]
    :geo nil}
   {:id "karakoram"     :name "Karakoram"          :stories [16]
    :geo {:lat 35.24 :lon 74.59}}
   {:id "diamer"        :name "Diamer"             :stories [17 18]
    :geo {:lat 35.33 :lon 74.35}}
   {:id "hunza"         :name "Hunza"              :stories [19]
    :geo {:lat 36.32 :lon 74.65}}])


(def edges
  [;; Geography clusters
   {:type :geography :stories [7 10 11 12 13 14 15] :region "tirthan"}
   {:type :geography :stories [1 5 8]               :region "lahaul-passes"}
   {:type :geography :stories [17 18]               :region "diamer"}
   ;; Character threads
   {:type :character :character "kohli"         :stories [10 12]}
   {:type :character :character "mehra"         :stories [14 15]}
   {:type :character :character "karimabad-teacher" :stories [16 19]}
   {:type :character :character "thread-walker" :stories [1 4 5 7 8 9 10 11 12 13 14 15 16 17 18 19]}
   ;; Concept bridges
   {:type :concept :link [:mechanism :mechanism-gradient]     :stories [10 12]}
   {:type :concept :link [:relay :sutra-relay]                :stories [1 12]}
   {:type :concept :link [:commissioning :commissioning-two]  :stories [7 10]}
   {:type :concept :link [:commissioning :commissioning-as-grafting] :stories [7 17]}
   {:type :concept :link [:spirit-vs-mechanism :spirit-vs-body] :stories [10 11]}
   {:type :concept :link [:harness :chorong-as-harness]       :stories [1 17]}
   {:type :concept :link [:substrate :substrate-independence] :stories [1 19]}
   {:type :concept :link [:petroglyph-stratigraphy :petroglyph-stratigraphy-18] :stories [16 18]}
   {:type :concept :link [:spirit-possession :trance-language] :stories [16 19]}
   {:type :concept :link [:convention :music-as-protocol]     :stories [12 19]}
   {:type :concept :link [:embodied-database :symbol-vs-behaviour] :stories [3 18]}
   ;; Concept lineages
   {:type :concept-lineage :concept :ideal-viewer                    :stories [2 4 8]}
   {:type :concept-lineage :concept :ground-state                    :stories [2 7 9 11]}
   {:type :concept-lineage :concept :sutra-relay                     :stories [1 5 12]}
   {:type :concept-lineage :concept :thread-holding                  :stories [8 11]}
   {:type :concept-lineage :concept :knowledge-transmission-failure  :stories [3 12]}
   {:type :concept-lineage :concept :embodied-database               :stories [3 9]}
   {:type :concept-lineage :concept :composite-knowledge             :stories [15 16]}
   {:type :concept-lineage :concept :accumulation                    :stories [13 18]}
   {:type :concept-lineage :concept :convergence-at-junctions        :stories [13 16]}])


;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Lookups (pre-computed at load time)
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(def stories-by-id
  (into {} (map (fn [s] [(:id s) s]) stories)))

(def stories-by-number
  (into {} (map (fn [s] [(:number s) s]) stories)))

(def concepts-by-id
  (into {} (map (fn [c] [(:id c) c]) concepts)))

(def characters-by-id
  (into {} (map (fn [c] [(:id c) c]) characters)))

(def regions-by-id
  (into {} (map (fn [r] [(:id r) r]) regions)))

(defn story-colour
  "Get the colour for a story based on its region."
  [story]
  (get region-colours (:region-id story) "#808080"))

(defn concept-colour
  "Blend colours of all stories that introduce or use this concept."
  [concept]
  (let [intro-story (get stories-by-number (:introduced-in concept))
        region-id   (:region-id intro-story)]
    (get region-colours region-id "#808080")))

(defn concept-stories
  "Get all stories that use a given concept id."
  [concept-id]
  (filter #(some #{concept-id} (:concepts %)) stories))

(defn story-concepts
  "Get all concept records for a given story."
  [story]
  (keep #(get concepts-by-id %) (:concepts story)))


;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;;; Background map features — geographic reference data
;;;
;;; Rivers, ridges, passes, towns for the schematic background.
;;; Approximate waypoints — geographically truthful, not GPS-precise.
;;; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(def rivers
  [{:id "beas"
    :name "Beas"
    :points [{:lat 32.36 :lon 77.19}
             {:lat 32.27 :lon 77.18}
             {:lat 32.19 :lon 77.16}
             {:lat 32.10 :lon 77.12}
             {:lat 31.96 :lon 77.10}
             {:lat 31.80 :lon 77.06}
             {:lat 31.68 :lon 77.10}
             {:lat 31.52 :lon 77.02}
             {:lat 31.38 :lon 76.93}
             {:lat 31.20 :lon 76.78}]}
   {:id "parvati"
    :name "Parvati"
    :points [{:lat 32.20 :lon 77.60}
             {:lat 32.10 :lon 77.50}
             {:lat 32.05 :lon 77.42}
             {:lat 32.01 :lon 77.35}
             {:lat 31.95 :lon 77.28}
             {:lat 31.87 :lon 77.15}
             {:lat 31.80 :lon 77.06}]}
   {:id "tirthan"
    :name "Tirthan"
    :points [{:lat 31.68 :lon 77.48}
             {:lat 31.62 :lon 77.43}
             {:lat 31.58 :lon 77.39}
             {:lat 31.53 :lon 77.34}
             {:lat 31.48 :lon 77.25}
             {:lat 31.42 :lon 77.16}
             {:lat 31.38 :lon 77.10}]}
   {:id "sutlej"
    :name "Sutlej"
    :points [{:lat 32.05 :lon 78.60}
             {:lat 31.90 :lon 78.45}
             {:lat 31.70 :lon 78.30}
             {:lat 31.53 :lon 78.10}
             {:lat 31.40 :lon 77.80}
             {:lat 31.30 :lon 77.45}
             {:lat 31.22 :lon 77.10}
             {:lat 31.15 :lon 76.93}
             {:lat 31.05 :lon 76.70}]}
   {:id "chandrabhaga"
    :name "Chandrabhaga"
    :points [{:lat 32.80 :lon 77.05}
             {:lat 32.65 :lon 76.98}
             {:lat 32.57 :lon 76.95}
             {:lat 32.45 :lon 76.88}
             {:lat 32.35 :lon 76.80}
             {:lat 32.20 :lon 76.72}]}
   {:id "baspa"
    :name "Baspa"
    :points [{:lat 31.55 :lon 78.50}
             {:lat 31.48 :lon 78.38}
             {:lat 31.42 :lon 78.26}
             {:lat 31.38 :lon 78.15}
             {:lat 31.35 :lon 78.05}]}
   ;; ── Karakoram rivers ──
   {:id "indus"
    :name "Indus"
    :points [{:lat 36.30 :lon 74.80}
             {:lat 36.05 :lon 74.65}
             {:lat 35.85 :lon 74.55}
             {:lat 35.60 :lon 74.40}
             {:lat 35.42 :lon 74.10}
             {:lat 35.30 :lon 73.95}
             {:lat 35.10 :lon 74.00}
             {:lat 34.90 :lon 74.10}]}
   {:id "hunza-river"
    :name "Hunza"
    :points [{:lat 36.85 :lon 75.40}
             {:lat 36.60 :lon 75.00}
             {:lat 36.32 :lon 74.65}
             {:lat 36.05 :lon 74.65}]}
   {:id "gilgit-river"
    :name "Gilgit"
    :points [{:lat 36.10 :lon 74.00}
             {:lat 35.92 :lon 74.20}
             {:lat 35.85 :lon 74.55}]}])

(def ridges
  [{:id "great-himalayan"
    :name "Great Himalayan Range"
    :points [{:lat 32.30 :lon 78.50}
             {:lat 32.20 :lon 78.10}
             {:lat 32.10 :lon 77.80}
             {:lat 32.05 :lon 77.55}
             {:lat 32.00 :lon 77.30}
             {:lat 31.95 :lon 77.10}
             {:lat 31.85 :lon 76.80}]}
   {:id "pir-panjal"
    :name "Pir Panjal"
    :points [{:lat 32.55 :lon 77.40}
             {:lat 32.40 :lon 77.20}
             {:lat 32.25 :lon 77.00}
             {:lat 32.10 :lon 76.80}
             {:lat 31.95 :lon 76.60}]}
   {:id "dhauladhar"
    :name "Dhauladhar"
    :points [{:lat 32.30 :lon 76.50}
             {:lat 32.15 :lon 76.70}
             {:lat 32.00 :lon 76.85}
             {:lat 31.85 :lon 77.00}
             {:lat 31.70 :lon 77.15}]}
   ;; ── Karakoram ridges ──
   {:id "karakoram-range"
    :name "Karakoram Range"
    :points [{:lat 36.80 :lon 75.60}
             {:lat 36.50 :lon 75.20}
             {:lat 36.20 :lon 74.90}
             {:lat 35.90 :lon 74.60}
             {:lat 35.60 :lon 74.30}
             {:lat 35.30 :lon 74.00}]}
   {:id "nanga-parbat-massif"
    :name "Nanga Parbat"
    :points [{:lat 35.40 :lon 74.30}
             {:lat 35.24 :lon 74.59}
             {:lat 35.10 :lon 74.80}]}])

(def passes
  [{:id "rohtang"      :name "Rohtang"       :geo {:lat 32.37 :lon 77.25}}
   {:id "jalori"       :name "Jalori"        :geo {:lat 31.53 :lon 77.37}}
   {:id "chandrakhani" :name "Chandrakhani"  :geo {:lat 31.90 :lon 77.30}}
   {:id "pin-parvati"  :name "Pin Parvati"   :geo {:lat 32.05 :lon 77.55}}
   {:id "khunjerab"    :name "Khunjerab"    :geo {:lat 36.85 :lon 75.42}}
   {:id "babusar"      :name "Babusar"      :geo {:lat 35.16 :lon 74.00}}])

(def towns
  [{:id "kullu"   :name "Kullu"   :geo {:lat 31.96 :lon 77.10}}
   {:id "manali"  :name "Manali"  :geo {:lat 32.24 :lon 77.19}}
   {:id "shimla"  :name "Shimla"  :geo {:lat 31.10 :lon 77.17}}
   {:id "keylong" :name "Keylong" :geo {:lat 32.57 :lon 76.97}}
   {:id "sangla"  :name "Sangla"  :geo {:lat 31.42 :lon 78.26}}
   {:id "rampur"  :name "Rampur"  :geo {:lat 31.45 :lon 77.63}}
   {:id "mandi"   :name "Mandi"   :geo {:lat 31.71 :lon 76.93}}
   {:id "kasol"   :name "Kasol"   :geo {:lat 32.01 :lon 77.32}}
   {:id "banjar"      :name "Banjar"      :geo {:lat 31.64 :lon 77.34}}
   ;; ── Karakoram towns ──
   {:id "gilgit"      :name "Gilgit"      :geo {:lat 35.92 :lon 74.31}}
   {:id "chilas"      :name "Chilas"      :geo {:lat 35.42 :lon 74.10}}
   {:id "karimabad"   :name "Karimabad"   :geo {:lat 36.32 :lon 74.65}}
   {:id "skardu"      :name "Skardu"      :geo {:lat 35.30 :lon 75.63}}
   {:id "tato"        :name "Tato"        :geo {:lat 35.28 :lon 74.55}}])
