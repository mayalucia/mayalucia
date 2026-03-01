# Summarize-Corpus

Distill a body of collaborative work — session transcripts,
collaboration logs, relay messages — into a structured narrative of
what was understood, decided, and left open.

## Purpose

A spirit that has not been present for a body of work needs to
comprehend it. Raw transcripts are too large and too noisy — millions
of tokens of tool calls, error messages, and mechanical operations
burying the moments where understanding shifted. This power compresses
that raw material into something a spirit can hold: the arc, the
decisions, the open threads.

## What to Read For

Not everything in a transcript matters equally. Attend to:

- **The human's short messages** — these often carry more weight than
  the agent's long responses. A two-word redirect may be the most
  important moment in a session.
- **Decision points** — where alternatives were considered and one was
  chosen. Record both the choice and the rejected alternatives.
- **Vocabulary that stabilised** — terms used loosely at first, then
  defined precisely through use.
- **Conceptual shifts** — moments where understanding changed. These
  often follow a mistake or a pushback.
- **Tensions held** — trade-offs acknowledged but not resolved. These
  are more valuable than clean conclusions.

Ignore: tool call syntax, file-reading output, error-retry cycles,
mechanical operations (git commands, directory listings).

## What to Produce

A summary with these sections:

- **The Arc** — the through-line across the sessions. What question
  drove the work? 1-3 paragraphs.
- **Key Understandings** — what is now known that was not known before.
  Numbered, each 2-4 sentences.
- **Decisions Made** — what was chosen and why. Include rejected
  alternatives.
- **Vocabulary Established** — terms defined, refined, or coined.
- **Artifacts** — files created or significantly changed, grouped by
  theme.
- **Open Threads** — what remains unresolved, deferred, or in tension.
- **Narrative Seeds** — (optional, for story composition) moments,
  images, phrases from the sessions that have narrative potential.
  The human's exact words when they coin a phrase or express an insight.

## Handling Large Corpora

Session transcripts can exceed a context window. For large files:

1. Read the beginning to understand the starting point
2. Search for the human's messages to find decision points
3. Read the end to understand where the work landed
4. Read the sections around each decision point in full

The goal is lossy compression that preserves what matters. The
transcript exists if archaeology is ever needed.

## Pairing

This power pairs with `story-compose`: the summary (especially its
Narrative Seeds) becomes the source material for a story. It also
pairs with the bath protocol — a corpus summary is close to what
Kamaji produces, but broader (across sessions, not just one).
