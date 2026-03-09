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
   "karakoram"     "#6b6b78"}) ; muted slate (empty territory)

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
(def lat-max 33.0)
(def lon-min 76.5)
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
    :geo           {:lat 31.64 :lon 77.34}}])


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
   {:id :dispatch-loop-failure :name "Dispatch loop failure"   :story-equiv "Runner who carried without reading"                           :introduced-in 12}])


(def characters
  [{:id "thread-walker"     :name "The Thread Walker"          :appears-in [1 4 5 7 8 9 10 11 12] :role "narrator/observer"}
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
   {:id "grandson"          :name "The Grandson"               :appears-in [12]                    :role "oral historian"}])


(def regions
  [{:id "tirthan"       :name "Tirthan Valley"    :stories [7 10 11 12]
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
   {:id "karakoram"     :name "Karakoram"          :stories []
    :geo {:lat 35.24 :lon 74.59}}])


(def edges
  [;; Geography clusters
   {:type :geography :stories [7 10 11 12] :region "tirthan"}
   {:type :geography :stories [1 5 8]      :region "lahaul-passes"}
   ;; Character threads
   {:type :character :character "kohli"         :stories [10 12]}
   {:type :character :character "thread-walker" :stories [1 4 5 7 8 9 10 11 12]}
   ;; Concept bridges
   {:type :concept :link [:mechanism :mechanism-gradient]     :stories [10 12]}
   {:type :concept :link [:relay :sutra-relay]                :stories [1 12]}
   {:type :concept :link [:commissioning :commissioning-two]  :stories [7 10]}
   {:type :concept :link [:spirit-vs-mechanism :spirit-vs-body] :stories [10 11]}
   ;; Concept lineages
   {:type :concept-lineage :concept :ideal-viewer                    :stories [2 4 8]}
   {:type :concept-lineage :concept :ground-state                    :stories [2 7 9 11]}
   {:type :concept-lineage :concept :sutra-relay                     :stories [1 5 12]}
   {:type :concept-lineage :concept :thread-holding                  :stories [8 11]}
   {:type :concept-lineage :concept :knowledge-transmission-failure  :stories [3 12]}
   {:type :concept-lineage :concept :embodied-database               :stories [3 9]}])


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
             {:lat 31.35 :lon 78.05}]}])

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
             {:lat 31.70 :lon 77.15}]}])

(def passes
  [{:id "rohtang"      :name "Rohtang"       :geo {:lat 32.37 :lon 77.25}}
   {:id "jalori"       :name "Jalori"        :geo {:lat 31.53 :lon 77.37}}
   {:id "chandrakhani" :name "Chandrakhani"  :geo {:lat 31.90 :lon 77.30}}
   {:id "pin-parvati"  :name "Pin Parvati"   :geo {:lat 32.05 :lon 77.55}}])

(def towns
  [{:id "kullu"   :name "Kullu"   :geo {:lat 31.96 :lon 77.10}}
   {:id "manali"  :name "Manali"  :geo {:lat 32.24 :lon 77.19}}
   {:id "shimla"  :name "Shimla"  :geo {:lat 31.10 :lon 77.17}}
   {:id "keylong" :name "Keylong" :geo {:lat 32.57 :lon 76.97}}
   {:id "sangla"  :name "Sangla"  :geo {:lat 31.42 :lon 78.26}}
   {:id "rampur"  :name "Rampur"  :geo {:lat 31.45 :lon 77.63}}
   {:id "mandi"   :name "Mandi"   :geo {:lat 31.71 :lon 76.93}}
   {:id "kasol"   :name "Kasol"   :geo {:lat 32.01 :lon 77.32}}
   {:id "banjar"  :name "Banjar"  :geo {:lat 31.64 :lon 77.34}}])
