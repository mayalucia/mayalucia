# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
dixa.verify — orchestrate initiation of a newly commissioned spirit.

Usage:
    uv run verify.py <spirit-name> [--project-root <path>] [--all]

Phase 1: birth_certificate (schema, cross-references) — runs here.
Phase 2: first_breath (agentic, requires a live harness session) — documented,
         human-administered for now.

Options:
    --all           Validate all spirits in aburaya/spirits/
    --project-root  Override project root detection
"""

from __future__ import annotations

import sys
from pathlib import Path

from birth_certificate import validate_spirit, Report


def find_project_root(start: Path) -> Path:
    """Walk up to find project root (directory containing aburaya/)."""
    root = start.resolve()
    while root != root.parent:
        if (root / "aburaya").exists():
            return root
        root = root.parent
    return start


def list_spirits(project_root: Path) -> list[str]:
    """List all spirit directories in aburaya/spirits/."""
    spirits_dir = project_root / "aburaya" / "spirits"
    if not spirits_dir.exists():
        return []
    return sorted(
        d.name
        for d in spirits_dir.iterdir()
        if d.is_dir() and (d / "identity.yaml").exists()
    )


def main() -> int:
    project_root = find_project_root(Path.cwd())

    if "--project-root" in sys.argv:
        idx = sys.argv.index("--project-root")
        project_root = Path(sys.argv[idx + 1]).resolve()

    validate_all = "--all" in sys.argv

    if validate_all:
        spirits = list_spirits(project_root)
        if not spirits:
            print("No spirits found in aburaya/spirits/")
            return 1

        print(f"Validating {len(spirits)} spirits...\n")
        reports: list[Report] = []
        for name in spirits:
            report = validate_spirit(name, project_root)
            report.print()
            reports.append(report)

        # Summary
        passed = sum(1 for r in reports if r.passed)
        total = len(reports)
        print(f"\n{'='*50}")
        print(f"Summary: {passed}/{total} spirits passed")
        if passed < total:
            failed = [r.spirit_name for r in reports if not r.passed]
            print(f"Failed: {', '.join(failed)}")
        return 0 if passed == total else 1

    # Single spirit
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("Usage: uv run verify.py <spirit-name> [--all] [--project-root <path>]")
        print("\nPhase 1: birth_certificate (schema + cross-references)")
        print("Phase 2: first_breath (see nature/first_breath.org)")
        return 1

    spirit_name = args[0]
    report = validate_spirit(spirit_name, project_root)
    report.print()

    if report.passed:
        print("\nPhase 1 (birth certificate): PASSED")
        print("Phase 2 (first breath): requires a live harness session.")
        print("See: aburaya/spirits/dixa/nature/first_breath.org")
    else:
        print("\nPhase 1 (birth certificate): FAILED")
        print("Fix the issues above before proceeding to first breath.")

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
