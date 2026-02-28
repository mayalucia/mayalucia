"""
Dialogue parser and validator for the Autonomy Agreement protocol.

Parses structured org-mode dialogue files into a list of typed turns,
validates the structure, and provides query/rendering capabilities.

This is a minimal prototype — enough to demonstrate that the format
is machine-readable and the autonomy protocol is enforceable.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


# --- Enums ---

class Voice(Enum):
    HUMAN = "human"
    MACHINE = "machine"


class AutonomyLevel(Enum):
    APPRENTICE = "apprentice"
    COLLEAGUE = "colleague"
    DELEGATE = "delegate"
    COLLABORATOR = "collaborator"

    def __lt__(self, other):
        order = [self.APPRENTICE, self.COLLEAGUE, self.DELEGATE, self.COLLABORATOR]
        return order.index(self) < order.index(other)

    def __le__(self, other):
        return self == other or self < other


# Substantive moves
SUBSTANTIVE_MOVES = {
    "conjecture", "challenge", "derivation", "computation",
    "observation", "synthesis", "question", "answer",
}

# Meta moves (autonomy negotiation)
META_MOVES = {
    "orient", "delegate", "accept", "reject",
    "pull-back", "interrupt", "reflect", "close",
}

# Creative moves
CREATIVE_MOVES = {
    "compose", "critique", "variation", "surprise",
}

ALL_MOVES = SUBSTANTIVE_MOVES | META_MOVES | CREATIVE_MOVES


# --- Data structures ---

@dataclass
class Turn:
    """A single turn in a dialogue."""
    number: int
    summary: str
    voice: Voice
    move: str
    timestamp: str
    body: str
    provenance: Optional[str] = None
    level: Optional[AutonomyLevel] = None
    refs: list[int] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)

    @property
    def is_meta(self) -> bool:
        return self.move in META_MOVES

    @property
    def is_escalation(self) -> bool:
        return self.move == "delegate"

    @property
    def is_deescalation(self) -> bool:
        return self.move == "pull-back"

    @property
    def is_session_boundary(self) -> bool:
        return self.move in ("orient", "close")


@dataclass
class Dialogue:
    """A complete structured dialogue."""
    title: str
    dialogue_id: str
    domain: str
    created: str
    turns: list[Turn] = field(default_factory=list)
    properties: dict[str, str] = field(default_factory=dict)

    @property
    def current_turn(self) -> Optional[Turn]:
        return self.turns[-1] if self.turns else None

    def turns_by_voice(self, voice: Voice) -> list[Turn]:
        return [t for t in self.turns if t.voice == voice]

    def meta_turns(self) -> list[Turn]:
        return [t for t in self.turns if t.is_meta]

    def autonomy_transitions(self) -> list[Turn]:
        return [t for t in self.turns
                if t.move in ("delegate", "accept", "reject", "pull-back")]

    def session_boundaries(self) -> list[Turn]:
        return [t for t in self.turns if t.is_session_boundary]


# --- Parser ---

# Matches a top-level org heading: "* Summary text"
HEADING_RE = re.compile(r"^\*\s+(.+)$")

# Matches a property line: ":KEY: value"
PROP_RE = re.compile(r"^:(\w[\w-]*):\s*(.+)$")

# Matches the property drawer boundaries
PROP_START_RE = re.compile(r"^:PROPERTIES:\s*$")
PROP_END_RE = re.compile(r"^:END:\s*$")

# Matches file-level properties: "#+KEY: value"
FILE_PROP_RE = re.compile(r"^#\+(\w[\w_]*):\s*(.+)$", re.IGNORECASE)


def parse_dialogue(text: str) -> Dialogue:
    """Parse an org-mode dialogue into a Dialogue object."""
    lines = text.split("\n")
    file_props = {}
    title = ""

    # First pass: extract file-level properties
    for line in lines:
        m = FILE_PROP_RE.match(line)
        if m:
            key = m.group(1).lower()
            val = m.group(2).strip()
            if key == "title":
                title = val
            else:
                file_props[key.replace(" ", "_")] = val

    # Second pass: extract turns
    turns = []
    i = 0
    while i < len(lines):
        m = HEADING_RE.match(lines[i])
        if m:
            summary = m.group(1).strip()
            # Strip org tags like :meta: from summary
            summary = re.sub(r"\s+:[\w:]+:\s*$", "", summary)
            i += 1

            # Parse property drawer
            props = {}
            if i < len(lines) and PROP_START_RE.match(lines[i]):
                i += 1
                while i < len(lines) and not PROP_END_RE.match(lines[i]):
                    pm = PROP_RE.match(lines[i])
                    if pm:
                        props[pm.group(1).upper()] = pm.group(2).strip()
                    i += 1
                i += 1  # skip :END:

            # Parse body (everything until next heading or EOF)
            body_lines = []
            while i < len(lines) and not HEADING_RE.match(lines[i]):
                body_lines.append(lines[i])
                i += 1
            body = "\n".join(body_lines).strip()

            # Only treat as a turn if it has TURN property
            if "TURN" in props:
                turn = Turn(
                    number=int(props["TURN"]),
                    summary=summary,
                    voice=Voice(props.get("VOICE", "machine").lower()),
                    move=props.get("MOVE", "observation").lower(),
                    timestamp=props.get("TIMESTAMP", ""),
                    body=body,
                    provenance=props.get("PROVENANCE"),
                    level=AutonomyLevel(props["LEVEL"].lower()) if "LEVEL" in props else None,
                    refs=_parse_refs(props.get("REFS", "")),
                    artifacts=props.get("ARTIFACTS", "").split() if "ARTIFACTS" in props else [],
                )
                turns.append(turn)
        else:
            i += 1

    return Dialogue(
        title=title,
        dialogue_id=file_props.get("dialogue_id", ""),
        domain=file_props.get("domain", ""),
        created=file_props.get("created", ""),
        turns=turns,
        properties=file_props,
    )


def _parse_refs(refs_str: str) -> list[int]:
    """Parse space-separated turn numbers (ignoring commit hashes)."""
    refs = []
    for token in refs_str.split():
        try:
            refs.append(int(token))
        except ValueError:
            pass  # commit hash, skip for now
    return refs


# --- Validator ---

@dataclass
class ValidationIssue:
    turn: Optional[int]
    severity: str  # "error" or "warning"
    message: str

    def __str__(self):
        loc = f"turn {self.turn}" if self.turn else "file"
        return f"[{self.severity}] {loc}: {self.message}"


def validate_dialogue(dialogue: Dialogue) -> list[ValidationIssue]:
    """Validate a dialogue for structural and protocol correctness."""
    issues = []

    if not dialogue.title:
        issues.append(ValidationIssue(None, "error", "missing #+title"))

    # Check turn numbering
    expected = 1
    for turn in dialogue.turns:
        if turn.number != expected:
            issues.append(ValidationIssue(
                turn.number, "warning",
                f"expected turn {expected}, got {turn.number}"))
        expected = turn.number + 1

        # Check move is recognized
        if turn.move not in ALL_MOVES:
            issues.append(ValidationIssue(
                turn.number, "warning",
                f"unrecognized move: {turn.move}"))

        # Check refs point to existing turns
        existing = {t.number for t in dialogue.turns}
        for ref in turn.refs:
            if ref not in existing:
                issues.append(ValidationIssue(
                    turn.number, "warning",
                    f"references non-existent turn {ref}"))

        # Check timestamp exists
        if not turn.timestamp:
            issues.append(ValidationIssue(
                turn.number, "warning", "missing timestamp"))

    # Protocol checks
    issues.extend(_validate_autonomy_protocol(dialogue))

    return issues


def _validate_autonomy_protocol(dialogue: Dialogue) -> list[ValidationIssue]:
    """Check that autonomy transitions follow the consent protocol."""
    issues = []

    for i, turn in enumerate(dialogue.turns):
        # A 'delegate' (escalation request) should be followed by accept/reject
        if turn.move == "delegate" and i + 1 < len(dialogue.turns):
            next_turn = dialogue.turns[i + 1]
            if next_turn.move not in ("accept", "reject", "interrupt"):
                issues.append(ValidationIssue(
                    turn.number, "warning",
                    "delegation proposal not followed by accept/reject"))

        # 'accept' should reference a prior delegation
        if turn.move == "accept":
            delegation_turns = [t.number for t in dialogue.turns[:i]
                                if t.move == "delegate"]
            if not any(ref in delegation_turns for ref in turn.refs):
                # Might reference implicitly (the immediately prior turn)
                if i > 0 and dialogue.turns[i - 1].move != "delegate":
                    issues.append(ValidationIssue(
                        turn.number, "warning",
                        "accept without reference to a delegation proposal"))

        # 'pull-back' is valid from any party at any time (no constraint)
        # 'interrupt' should have a body explaining what invariant fired
        if turn.move == "interrupt" and len(turn.body) < 10:
            issues.append(ValidationIssue(
                turn.number, "warning",
                "interrupt with minimal explanation — should describe "
                "which invariant was triggered"))

    return issues


# --- Renderers ---

def render_summary(dialogue: Dialogue) -> str:
    """Render a concise summary of the dialogue."""
    lines = [
        f"Dialogue: {dialogue.title}",
        f"ID: {dialogue.dialogue_id}",
        f"Domain: {dialogue.domain}",
        f"Turns: {len(dialogue.turns)}",
        f"Sessions: {len([t for t in dialogue.turns if t.move == 'orient']) + 1}",
        "",
        "Autonomy transitions:",
    ]

    transitions = dialogue.autonomy_transitions()
    if transitions:
        for t in transitions:
            lines.append(
                f"  Turn {t.number} [{t.voice.value}]: {t.move}"
                f"{f' (level: {t.level.value})' if t.level else ''}"
                f" — {t.summary[:60]}")
    else:
        lines.append("  (none)")

    lines.extend(["", "Turn sequence:"])
    for t in dialogue.turns:
        marker = "●" if t.is_meta else "○"
        voice = "H" if t.voice == Voice.HUMAN else "M"
        lines.append(f"  {marker} {t.number:3d} [{voice}] {t.move:12s} {t.summary[:50]}")

    return "\n".join(lines)


def render_autonomy_timeline(dialogue: Dialogue) -> str:
    """Render the autonomy negotiation timeline."""
    lines = ["Autonomy Timeline", "=" * 40]

    for turn in dialogue.turns:
        if turn.is_meta:
            voice = "HUMAN" if turn.voice == Voice.HUMAN else "MACHINE"
            level_str = f" [{turn.level.value}]" if turn.level else ""
            lines.append(
                f"\n  Turn {turn.number} | {voice} | {turn.move}{level_str}"
                f"\n  {turn.summary}"
            )
            # Show first 2 lines of body for context
            body_preview = "\n".join(turn.body.split("\n")[:2])
            if body_preview:
                lines.append(f"  > {body_preview}")

    return "\n".join(lines)


# --- CLI ---

def main():
    if len(sys.argv) < 2:
        print("Usage: python dialogue.py <dialogue.org> [validate|summary|timeline]")
        sys.exit(1)

    path = Path(sys.argv[1])
    command = sys.argv[2] if len(sys.argv) > 2 else "summary"

    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    text = path.read_text()
    dialogue = parse_dialogue(text)

    if command == "validate":
        issues = validate_dialogue(dialogue)
        if issues:
            for issue in issues:
                print(issue)
            print(f"\n{len(issues)} issue(s) found.")
            sys.exit(1 if any(i.severity == "error" for i in issues) else 0)
        else:
            print("No issues found.")

    elif command == "summary":
        print(render_summary(dialogue))

    elif command == "timeline":
        print(render_autonomy_timeline(dialogue))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
