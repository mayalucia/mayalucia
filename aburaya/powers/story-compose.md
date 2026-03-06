# Story-Compose

Translate conceptual understanding into the MāyāLucIA narrative world.
The story reads as a found document from the Western Himalaya — not as
a description of the work that produced it.

## Purpose

The project's stories are not documentation. They are a parallel
register — the same structural insights expressed through geography,
craft, and observation rather than through code and configuration.
Writing a story is an act of understanding: if the concept can survive
translation into the valley's language, it is understood.

## Prerequisites

Before composing:

1. **Source material** — a `summarize-corpus` output, or direct
   understanding of what the story should convey.
2. **Voice examples** — read at least two existing stories to absorb
   the register. The most recent story is the best reference.
3. **World-building reference** — the Western Himalaya geography,
   the Miyazaki→Himalaya translation key, and the fourth-wall rule
   (see below, and the storytelling notes in the spirit's memory).

## The Voice

### Found-document framing
Every story is narrated through artefacts: field notes, ledgers,
logbooks, brass plates, woven patterns, instrument readings. Never
omniscient narration. The reader discovers the story as the narrator
discovered it — incompletely, with gaps acknowledged.

### The Thread Walker
Recurring observer-narrator. She carries instruments, keeps notebooks,
does not explain what she does not understand. Precise observations,
tentative interpretations. Present enough to witness, absent enough
not to be the subject.

### Precise geographic detail
Real places across the transborder Western Himalaya. The stories
range across interconnected valleys and high passes:

- **Parvati Valley**: Manikaran gorge, Tosh, Pin Parvati glacier
- **Tirthan Valley**: Larji gorge, Jalori Pass, Serolsar Lake, Chehni Kothi
- **Baspa Valley**: Sangla, Kinnaur
- **Spiti and Lahaul**: high desert, passes connecting to Kullu
- **High passes**: where Kullu ends and Tibet begins

Real geology (gneiss, magnetite, slate, travertine), real flora
(deodar, cedar, lichen at altitude), Pahari and Kinnauri vocabulary.
If a detail is not known, leave it out rather than fabricate.

### Technical-yet-poetic register
Scientific vocabulary for aesthetic effect. Measurements stated
precisely. Poetry emerges from precision, not ornament.

### Weaving/archive/notation motifs
Patterns in cloth, data, stone. The act of recording is itself a
theme.

## The Fourth-Wall Rule

Project infrastructure vocabulary must never appear in story text.
No model names, no file formats, no configuration syntax, no spirit
names from the registry. The story world and the system world share
deep structure but different surfaces.

### Translation table

The canonical translation table — all keys from all 12 stories, with
provenance — lives in `develop/story-development.org` (section: The
Global Translation Table). Per-story keys live in `stories/<slug>/keys.org`.

Consult the full table before composing. Never cross the fourth wall.

### The Miyazaki → Himalaya key

| Spirited Away | Western Himalaya |
|--------------|----------------|
| Kami | Devtas (living gods, 534 in Kullu) |
| Onsen | Kund (hot spring pool) |
| Kamikakushi | Devta ka aavesh (gur trance) |
| Yubaba (name-taker) | Kardar (bathhouse keeper) |
| Zeniba (name-keeper) | Buddhi Nagin (Serolsar Lake) |
| No-Face | Pret (hungry ghost) |
| Haku (river spirit) | Nag devta |
| Soot sprites | Bajantris (musicians) |
| Aburaya | The Kund |

## Existing Stories (geography)

The full table with document types lives in `develop/story-development.org`.

| Story | Setting |
|-------|---------|
| The Thread Walkers | High valleys, Kullu–Tibet border |
| The Constellation of Doridhar | Village of Doridhar |
| The Dyer's Gorge | Parvati gorge, Manikaran, Pin Parvati |
| The Instrument Maker's Rest | Sangla, Baspa valley (Kinnaur) |
| The Logbook of the Unnamed River | Spiti, Lahaul, high passes |
| The Phantom Faculty | Abstract |
| The Spirit's Kund | Tirthan Valley, Jalori Pass, Serolsar Lake |
| The Guide Who Woke Last | Chandrabhaga, Keylong, Lahaul |
| The Mineral Deposits | Sutlej valley, Tattapani, Kol Dam |
| The Kuhl Builder's Survey | Tirthan Valley, lower terraces |
| The Weaver's Loom | Tirthan Valley, Gushaini, Nahin |
| The Dāk Runner's Rest | Tirthan gorge, ruined dāk bungalow |

Each story opens new territory. The Karakoram — Diamer, Nanga Parbat,
the Indus gorge — has not yet appeared. The Thread Walker moves.

## Story Workspace

Each story has a development workspace at `stories/<slug>/` containing
`notes.org` (development record), `keys.org` (translation keys), and
`generate_images.py` (illustrations). See `develop/story-development.org`
for the full convention.

## Composing

### 1. Find the core tension
Every story holds a question without necessarily resolving it. The
tension should emerge from the source material — not imposed, found.

### 2. Choose the document type
Field notes, ledger entries, logbook, gur's testimony, woven record,
or hybrid. Match to content: ledgers suit registries, field notes
suit discoveries, testimony suits revelation.

### 3. Map concepts to geography
Layered identity → Kath-Kuni construction (stone and timber holding
each other through gravity). Ephemeral computation → the hot spring
(water passes through, leaves mineral traces, moves on). Memory →
mineral deposition in the kund.

### 4. Draft
Sections headed with Roman numerals. Begin with a prefatory note.
Include: Thread Walker notebook quotations, local testimony, sensory
detail, a moment where measurement and mystery coexist.

### 5. Fourth-wall check
Read the draft for system vocabulary that leaked through. Common
failures: spirit names, technical terms in computing sense, references
to sessions or contexts, diagrams that look like architecture.

## Pairing

This power takes input from `summarize-corpus`. The Narrative Seeds
section of a corpus summary is designed as raw material for
story-compose.
