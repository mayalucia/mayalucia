# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
dixa.birth_certificate — schema validation for organisational artifacts.

Validates spirit identity.yaml and guild YAML files against schemas,
checks cross-references between spirits and guilds, and verifies
filesystem consistency.

Usage:
    uv run birth_certificate.py <spirit-name> [--project-root <path>]

Output: structured report (pass/fail per check, messages for failures).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml


# --- Report ---


@dataclass
class Check:
    name: str
    passed: bool
    message: str = ""


@dataclass
class Report:
    spirit_name: str
    checks: list[Check] = field(default_factory=list)

    def add(self, name: str, passed: bool, message: str = "") -> None:
        self.checks.append(Check(name, passed, message))

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    def print(self) -> None:
        total = len(self.checks)
        passed = sum(1 for c in self.checks if c.passed)
        failed = total - passed

        print(f"\n=== Birth Certificate: {self.spirit_name} ===\n")
        for c in self.checks:
            mark = "PASS" if c.passed else "FAIL"
            print(f"  [{mark}] {c.name}")
            if c.message:
                for line in c.message.split("\n"):
                    print(f"         {line}")
        print(f"\n  {passed}/{total} passed", end="")
        if failed:
            print(f", {failed} failed")
        else:
            print()


# --- Schema loading ---


def load_schema(schema_path: Path) -> dict:
    with open(schema_path) as f:
        return yaml.safe_load(f)


def load_yaml(path: Path) -> dict | None:
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        return None


# --- Validators ---


def validate_field(
    data: dict,
    field_name: str,
    spec: dict,
    path_prefix: str,
    report: Report,
) -> None:
    """Validate a single field against its schema spec."""
    check_name = f"{path_prefix}.{field_name}"
    value = data.get(field_name)

    if value is None:
        if spec.get("required", False):
            report.add(check_name, False, "required but missing")
        return

    expected_type = spec.get("type", "string")

    # Type check
    type_ok = True
    if expected_type == "string" and not isinstance(value, str):
        report.add(check_name, False, f"expected string, got {type(value).__name__}")
        type_ok = False
    elif expected_type == "list" and not isinstance(value, list):
        report.add(check_name, False, f"expected list, got {type(value).__name__}")
        type_ok = False
    elif expected_type == "mapping" and not isinstance(value, dict):
        report.add(check_name, False, f"expected mapping, got {type(value).__name__}")
        type_ok = False

    if not type_ok:
        return

    # Allowed values
    allowed = spec.get("allowed_values")
    if allowed and value not in allowed:
        report.add(check_name, False, f"'{value}' not in {allowed}")
        return

    # must_include (for lists)
    must_include = spec.get("must_include")
    if must_include and isinstance(value, list):
        missing = [m for m in must_include if m not in value]
        if missing:
            report.add(check_name, False, f"missing required entries: {missing}")
            return

    # Recurse into children
    children = spec.get("children")
    if children and isinstance(value, dict):
        for child_name, child_spec in children.items():
            validate_field(value, child_name, child_spec, check_name, report)
        return

    # If we got here, field is present and valid
    report.add(check_name, True)


def validate_against_schema(
    data: dict, schema: dict, report: Report
) -> None:
    """Validate a YAML document against a schema."""
    top_level = schema.get("top_level", {})
    for field_name, spec in top_level.items():
        validate_field(data, field_name, spec, "", report)


# --- Cross-reference checks ---


def check_spirit_cross_refs(
    spirit_data: dict,
    spirit_name: str,
    aburaya: Path,
    project_root: Path,
    report: Report,
) -> None:
    """Check cross-references between spirit and filesystem."""

    # true-name matches directory name
    true_name = spirit_data.get("true-name", "")
    if true_name != spirit_name:
        report.add(
            "xref.true-name-matches-dir",
            False,
            f"true-name '{true_name}' != directory '{spirit_name}'",
        )
    else:
        report.add("xref.true-name-matches-dir", True)

    # guild exists
    role = spirit_data.get("role", {})
    guild_name = role.get("guild", "")
    if guild_name:
        guild_file = aburaya / "guilds" / f"{guild_name}.yaml"
        if guild_file.exists():
            report.add("xref.guild-file-exists", True)

            # spirit listed in guild
            guild_data = load_yaml(guild_file)
            if guild_data:
                guild_spirits = guild_data.get("spirits", [])
                if spirit_name in guild_spirits:
                    report.add("xref.spirit-in-guild", True)
                else:
                    report.add(
                        "xref.spirit-in-guild",
                        False,
                        f"'{spirit_name}' not in {guild_name}.yaml spirits: {guild_spirits}",
                    )
        else:
            report.add(
                "xref.guild-file-exists",
                False,
                f"guild file not found: {guild_file}",
            )

    # bath_notes directory
    memory = spirit_data.get("memory", {})
    bath_notes = memory.get("bath_notes", "")
    if bath_notes:
        notes_path = project_root / bath_notes
        if notes_path.exists():
            report.add("xref.bath-notes-exists", True)
        else:
            report.add(
                "xref.bath-notes-exists",
                False,
                f"bath_notes path not found: {notes_path}",
            )

    # project.path exists (or is plausible)
    project = spirit_data.get("project", {})
    proj_path_str = project.get("path", "")
    if proj_path_str:
        proj_path = project_root / proj_path_str
        if proj_path.exists():
            report.add("xref.project-path-exists", True)
        else:
            report.add(
                "xref.project-path-exists",
                False,
                f"project.path not found: {proj_path}",
            )


def check_guild_cross_refs(
    guild_data: dict,
    guild_name: str,
    aburaya: Path,
    project_root: Path,
    report: Report,
) -> None:
    """Check cross-references within a guild file."""

    # name matches filename
    file_name = guild_data.get("name", "")
    if file_name != guild_name:
        report.add(
            "guild-xref.name-matches-file",
            False,
            f"name '{file_name}' != filename '{guild_name}'",
        )
    else:
        report.add("guild-xref.name-matches-file", True)

    # all listed spirits have identity files
    spirits = guild_data.get("spirits", [])
    for s in spirits:
        identity = aburaya / "spirits" / s / "identity.yaml"
        if identity.exists():
            report.add(f"guild-xref.spirit-exists.{s}", True)
        else:
            report.add(
                f"guild-xref.spirit-exists.{s}",
                False,
                f"identity.yaml not found: {identity}",
            )

    # all listed projects exist
    projects = guild_data.get("projects", [])
    for p in projects:
        proj_path = project_root / p
        if proj_path.exists():
            report.add(f"guild-xref.project-exists.{p}", True)
        else:
            report.add(
                f"guild-xref.project-exists.{p}",
                False,
                f"project path not found: {proj_path}",
            )


# --- Main ---


def validate_spirit(
    spirit_name: str, project_root: Path
) -> Report:
    """Run the full birth certificate for a spirit."""
    report = Report(spirit_name)
    aburaya = project_root / "aburaya"
    schemas_dir = (
        aburaya / "spirits" / "dixa" / "nature" / "schemas"
    )

    # Load spirit identity
    identity_path = aburaya / "spirits" / spirit_name / "identity.yaml"
    if not identity_path.exists():
        report.add("file.identity-exists", False, str(identity_path))
        return report
    report.add("file.identity-exists", True)

    spirit_data = load_yaml(identity_path)
    if spirit_data is None:
        report.add("file.identity-parseable", False, "YAML parse error")
        return report
    report.add("file.identity-parseable", True)

    # Validate against schema
    spirit_schema = load_schema(schemas_dir / "spirit.yaml")
    validate_against_schema(spirit_data, spirit_schema, report)

    # Cross-reference checks
    check_spirit_cross_refs(
        spirit_data, spirit_name, aburaya, project_root, report
    )

    # Also validate the spirit's guild
    role = spirit_data.get("role", {})
    guild_name = role.get("guild", "")
    if guild_name:
        guild_path = aburaya / "guilds" / f"{guild_name}.yaml"
        if guild_path.exists():
            guild_data = load_yaml(guild_path)
            if guild_data:
                guild_schema = load_schema(schemas_dir / "guild.yaml")
                validate_against_schema(guild_data, guild_schema, report)
                check_guild_cross_refs(
                    guild_data, guild_name, aburaya, project_root, report
                )

    return report


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: uv run birth_certificate.py <spirit-name> [--project-root <path>]")
        return 1

    spirit_name = sys.argv[1]

    project_root = Path.cwd()
    if "--project-root" in sys.argv:
        idx = sys.argv.index("--project-root")
        project_root = Path(sys.argv[idx + 1])

    # Walk up to find project root (look for aburaya/)
    root = project_root
    while root != root.parent:
        if (root / "aburaya").exists():
            project_root = root
            break
        root = root.parent

    report = validate_spirit(spirit_name, project_root)
    report.print()

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
