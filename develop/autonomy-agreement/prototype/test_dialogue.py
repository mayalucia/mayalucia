"""Tests for the dialogue parser, validator, and protocol logic."""

from pathlib import Path
from dialogue import (
    parse_dialogue, validate_dialogue, render_summary,
    render_autonomy_timeline, Voice, AutonomyLevel, Turn,
)


EXAMPLE_PATH = Path(__file__).parent / "example-dialogue.org"


def test_parse_turns():
    """Parser extracts all 13 turns from the example dialogue."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    assert len(d.turns) == 13
    assert d.title == "Bloch RWA Breakdown — When Does the Approximation Fail?"


def test_turn_numbering():
    """Turns are numbered sequentially 1-13."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    numbers = [t.number for t in d.turns]
    assert numbers == list(range(1, 14))


def test_voice_assignment():
    """Human and machine voices are correctly assigned."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    human_turns = d.turns_by_voice(Voice.HUMAN)
    machine_turns = d.turns_by_voice(Voice.MACHINE)
    # Turns: 1(H), 2(M), 3(H), 4(M), 5(H), 6(M), 7(H), 8(M), 9(H), 10(M), 11(M), 12(H), 13(M)
    assert len(human_turns) == 6   # 1, 3, 5, 7, 9, 12
    assert len(machine_turns) == 7  # 2, 4, 6, 8, 10, 11, 13
    assert d.turns[0].voice == Voice.HUMAN
    assert d.turns[1].voice == Voice.MACHINE
    assert d.turns[4].voice == Voice.HUMAN


def test_move_types():
    """Moves are correctly parsed."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    assert d.turns[0].move == "question"
    assert d.turns[1].move == "derivation"
    assert d.turns[3].move == "delegate"
    assert d.turns[4].move == "accept"
    assert d.turns[7].move == "conjecture"
    assert d.turns[10].move == "pull-back"
    assert d.turns[12].move == "close"


def test_meta_turns():
    """Meta turns (autonomy negotiation) are identified."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    meta = d.meta_turns()
    meta_moves = [t.move for t in meta]
    assert "delegate" in meta_moves
    assert "accept" in meta_moves
    assert "pull-back" in meta_moves
    assert "close" in meta_moves


def test_autonomy_transitions():
    """Autonomy transitions are extracted in order."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    transitions = d.autonomy_transitions()
    assert len(transitions) == 3  # delegate, accept, pull-back
    assert transitions[0].move == "delegate"
    assert transitions[1].move == "accept"
    assert transitions[2].move == "pull-back"


def test_refs():
    """Turn references are parsed correctly."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    # Turn 6 refs turns 4 and 5
    assert 4 in d.turns[5].refs
    assert 5 in d.turns[5].refs
    # Turn 10 refs turns 10 refs turn 9
    assert 9 in d.turns[9].refs


def test_artifacts():
    """Artifact paths are parsed from turn properties."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    # Turn 6 has artifacts
    assert len(d.turns[5].artifacts) == 2
    assert "artifacts/turn-06-rwa-sweep.py" in d.turns[5].artifacts


def test_validation_passes():
    """The example dialogue passes validation."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    issues = validate_dialogue(d)
    assert len(issues) == 0


def test_validation_catches_bad_delegation():
    """Validator catches a delegation not followed by accept/reject."""
    text = """#+title: Bad Dialogue

* Propose delegation
:PROPERTIES:
:TURN: 1
:VOICE: machine
:MOVE: delegate
:TIMESTAMP: 2026-01-01T00:00:00
:END:

Let me take over.

* Unrelated observation
:PROPERTIES:
:TURN: 2
:VOICE: machine
:MOVE: observation
:TIMESTAMP: 2026-01-01T00:01:00
:END:

Something else entirely.
"""
    d = parse_dialogue(text)
    issues = validate_dialogue(d)
    warnings = [i for i in issues if "delegation" in i.message]
    assert len(warnings) > 0


def test_validation_catches_missing_title():
    """Validator catches missing title."""
    text = """* A turn
:PROPERTIES:
:TURN: 1
:VOICE: human
:MOVE: question
:TIMESTAMP: 2026-01-01T00:00:00
:END:

Hello.
"""
    d = parse_dialogue(text)
    issues = validate_dialogue(d)
    errors = [i for i in issues if i.severity == "error"]
    assert any("title" in i.message for i in errors)


def test_autonomy_level_ordering():
    """Autonomy levels have a meaningful ordering."""
    assert AutonomyLevel.APPRENTICE < AutonomyLevel.COLLEAGUE
    assert AutonomyLevel.COLLEAGUE < AutonomyLevel.DELEGATE
    assert AutonomyLevel.DELEGATE < AutonomyLevel.COLLABORATOR
    assert not (AutonomyLevel.COLLABORATOR < AutonomyLevel.APPRENTICE)


def test_render_summary():
    """Summary renderer produces non-empty output."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    summary = render_summary(d)
    assert "Bloch RWA Breakdown" in summary
    assert "Turns: 13" in summary
    assert "delegate" in summary


def test_render_timeline():
    """Timeline renderer shows autonomy transitions."""
    text = EXAMPLE_PATH.read_text()
    d = parse_dialogue(text)
    timeline = render_autonomy_timeline(d)
    assert "delegate" in timeline
    assert "accept" in timeline
    assert "pull-back" in timeline


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
