#!/usr/bin/env bash
# dispatch.sh — invoke Claude Code for a work package
#
# Usage: ./dispatch.sh <wp-file> [--dry-run]
#
# Reads executor and trust from the WP, resolves the spirit's
# working directory, maps trust to allowlist, invokes claude.
#
# The WP file must have:
#   #+property: executor <spirit-name>
#   #+property: status tightened|resumed
# Optional:
#   #+property: trust <level>  (default: spec-tighten)
#   #+property: profile <name> (override trust-level allowlist)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ABURAYA="$PROJECT_ROOT/aburaya"
TRANSCRIPT_DIR="$PROJECT_ROOT/.transcripts/orchestrator"

# --- Arguments ---

if [ $# -lt 1 ]; then
    echo "Usage: $0 <wp-file> [--dry-run]" >&2
    exit 1
fi

WP_FILE="$1"
DRY_RUN="${2:-}"

if [ ! -f "$WP_FILE" ]; then
    # Try relative to project root
    if [ -f "$PROJECT_ROOT/$WP_FILE" ]; then
        WP_FILE="$PROJECT_ROOT/$WP_FILE"
    else
        echo "ERROR: WP file not found: $WP_FILE" >&2
        exit 1
    fi
fi

# --- Extract WP metadata ---

extract_property() {
    local prop="$1"
    grep -i "^#+property:.*$prop" "$WP_FILE" 2>/dev/null | head -1 | sed "s/.*$prop *//i" | xargs || true
}

# Executor: from #+property: executor
EXECUTOR=$(extract_property "executor")
if [ -z "$EXECUTOR" ]; then
    echo "ERROR: no executor property in $WP_FILE" >&2
    echo "Add: #+property: executor <spirit-name>" >&2
    exit 1
fi

# Trust level: from #+property: trust, default spec-tighten
TRUST=$(extract_property "trust")
TRUST="${TRUST:-spec-tighten}"

# Profile override: from #+property: profile
PROFILE=$(extract_property "profile")

# Status check: only execute tightened or resumed WPs
STATUS=$(extract_property "status")
if [[ "$STATUS" != "tightened" && "$STATUS" != "resumed" ]]; then
    echo "ERROR: WP status is '$STATUS', expected 'tightened' or 'resumed'" >&2
    exit 1
fi

# --- Resolve spirit working directory ---

IDENTITY_FILE=$(find "$ABURAYA/spirits" -path "*/$EXECUTOR/identity.yaml" 2>/dev/null | head -1)
if [ -z "$IDENTITY_FILE" ]; then
    echo "ERROR: no identity.yaml found for spirit '$EXECUTOR'" >&2
    exit 1
fi

# Extract project.path from identity.yaml (simple grep, not a full parser)
SPIRIT_CWD=$(grep "  path:" "$IDENTITY_FILE" | head -1 | sed 's/.*path: *//' | tr -d '"' | tr -d "'" | xargs)

if [ -z "$SPIRIT_CWD" ]; then
    # Fall back to project root
    SPIRIT_CWD="$PROJECT_ROOT"
fi

# Resolve relative to project root
if [[ "$SPIRIT_CWD" != /* ]]; then
    SPIRIT_CWD="$PROJECT_ROOT/$SPIRIT_CWD"
fi

if [ ! -d "$SPIRIT_CWD" ]; then
    echo "WARNING: spirit CWD does not exist: $SPIRIT_CWD" >&2
    echo "         Falling back to project root" >&2
    SPIRIT_CWD="$PROJECT_ROOT"
fi

# --- Map trust to allowlist ---

allowlist_for_trust() {
    case "$1" in
        autonomous)
            echo "Read,Write,Edit,Glob,Grep,Bash,WebSearch,WebFetch,Task"
            ;;
        spec-tighten)
            echo "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Task,Bash(git status*),Bash(git add*),Bash(git commit*),Bash(git log*),Bash(git diff*),Bash(git fetch*),Bash(ls*)"
            ;;
        supervised)
            echo "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Task,Bash(git status*),Bash(git log*),Bash(git diff*),Bash(ls*)"
            ;;
        *)
            echo "Read,Write,Edit,Glob,Grep,Bash(git status*),Bash(ls*)"
            ;;
    esac
}

allowlist_for_profile() {
    local profile_file="$SCRIPT_DIR/allowlists.yaml"
    if [ ! -f "$profile_file" ]; then
        echo "ERROR: allowlists.yaml not found at $profile_file" >&2
        return 1
    fi
    # Simple extraction: find the profile block, collect tool lines
    awk -v prof="$1" '
        $0 ~ "^  " prof ":" { found=1; next }
        found && /^  [a-z]/ { found=0 }
        found && /- / { gsub(/^[ ]*- ["]*/, ""); gsub(/["]*$/, ""); tools = tools ? tools "," $0 : $0 }
        END { print tools }
    ' "$profile_file"
}

# Use profile override if set, otherwise trust-level mapping
if [ -n "$PROFILE" ]; then
    ALLOWLIST=$(allowlist_for_profile "$PROFILE")
    if [ -z "$ALLOWLIST" ]; then
        echo "ERROR: profile '$PROFILE' not found in allowlists.yaml" >&2
        exit 1
    fi
else
    ALLOWLIST=$(allowlist_for_trust "$TRUST")
fi

# --- Construct prompt ---

WP_BASENAME=$(basename "$WP_FILE")
WP_RELPATH=$(realpath --relative-to="$SPIRIT_CWD" "$WP_FILE" 2>/dev/null || echo "$WP_FILE")

PROMPT="You are $EXECUTOR. Execute work package $WP_BASENAME.

Read the WP at $WP_RELPATH for the full specification. Follow the
execution order. On completion:
1. Transition the WP status to 'completed' (update #+property: status)
2. Announce completion in the sutra relay
3. Commit all artifacts

If you encounter a blocking issue, transition status to
'input-required' and announce in the sutra with details."

# --- Build transcript directory ---

mkdir -p "$TRANSCRIPT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
TRANSCRIPT="$TRANSCRIPT_DIR/$TIMESTAMP-$EXECUTOR.log"

# --- Invoke ---

echo "=== Dispatch ==="
echo "  WP:         $WP_BASENAME"
echo "  Executor:   $EXECUTOR"
echo "  Trust:      $TRUST"
echo "  Profile:    ${PROFILE:-<from trust>}"
echo "  CWD:        $SPIRIT_CWD"
echo "  Transcript: $TRANSCRIPT"
echo ""

if [ "$DRY_RUN" = "--dry-run" ]; then
    echo "[DRY RUN] Would execute:"
    echo "  claude --cwd \"$SPIRIT_CWD\" \\"
    echo "         --allowedTools \"$ALLOWLIST\" \\"
    echo "         --print \\"
    echo "         --prompt \"...\""
    echo ""
    echo "Allowlist: $ALLOWLIST"
    echo ""
    echo "Prompt:"
    echo "$PROMPT"
    exit 0
fi

claude --cwd "$SPIRIT_CWD" \
       --allowedTools "$ALLOWLIST" \
       --print \
       --prompt "$PROMPT" \
       2>&1 | tee "$TRANSCRIPT"

echo ""
echo "=== Dispatch complete ==="
echo "  Transcript: $TRANSCRIPT"
