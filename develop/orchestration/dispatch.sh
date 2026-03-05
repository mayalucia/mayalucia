#!/usr/bin/env bash
# dispatch.sh — invoke Claude Code for a work package
#
# Usage: ./dispatch.sh <wp-file> [options]
#
# Options:
#   --task <letter>     Execute only this task of a composite WP
#   --executor <name>   Override executor (for coalition task dispatch)
#   --trust <level>     Override trust level
#   --impression <text> Override the default prompt with a custom impression
#   --dry-run           Show what would happen without executing
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
    echo "Usage: $0 <wp-file> [--task <letter>] [--executor <name>] [--trust <level>] [--impression <text>] [--dry-run]" >&2
    exit 1
fi

WP_FILE="$1"
shift

TASK=""
EXECUTOR_OVERRIDE=""
TRUST_OVERRIDE=""
CWD_OVERRIDE=""
IMPRESSION_OVERRIDE=""
DRY_RUN=""

while [ $# -gt 0 ]; do
    case "$1" in
        --task)
            TASK="$2"
            shift 2
            ;;
        --executor)
            EXECUTOR_OVERRIDE="$2"
            shift 2
            ;;
        --trust)
            TRUST_OVERRIDE="$2"
            shift 2
            ;;
        --cwd)
            CWD_OVERRIDE="$2"
            shift 2
            ;;
        --impression)
            IMPRESSION_OVERRIDE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN="yes"
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

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

# Executor: override > WP property
EXECUTOR="${EXECUTOR_OVERRIDE:-$(extract_property "executor")}"
if [ -z "$EXECUTOR" ]; then
    echo "ERROR: no executor — set #+property: executor in the WP or use --executor" >&2
    exit 1
fi

# Trust level: override > WP property > default
TRUST="${TRUST_OVERRIDE:-$(extract_property "trust")}"
TRUST="${TRUST:-spec-tighten}"

# Profile override: from #+property: profile
PROFILE=$(extract_property "profile")

# Status check: only execute tightened or resumed WPs
STATUS=$(extract_property "status")
if [[ "$STATUS" != "tightened" && "$STATUS" != "resumed" && "$STATUS" != "drafted" ]]; then
    echo "ERROR: WP status is '$STATUS', expected 'tightened', 'resumed', or 'drafted'" >&2
    exit 1
fi

# --- Resolve spirit working directory ---

resolve_spirit_cwd() {
    local spirit="$1"
    local identity_file
    identity_file=$(find "$ABURAYA/spirits" -path "*/$spirit/identity.yaml" 2>/dev/null | head -1)

    if [ -z "$identity_file" ]; then
        echo "$PROJECT_ROOT"
        return
    fi

    local cwd
    cwd=$(grep "  path:" "$identity_file" | head -1 | sed 's/.*path: *//' | tr -d '"' | tr -d "'" | xargs)

    if [ -z "$cwd" ]; then
        echo "$PROJECT_ROOT"
        return
    fi

    if [[ "$cwd" != /* ]]; then
        cwd="$PROJECT_ROOT/$cwd"
    fi

    if [ ! -d "$cwd" ]; then
        echo "$PROJECT_ROOT"
        return
    fi

    echo "$cwd"
}

# CWD: override > identity resolution
if [ -n "$CWD_OVERRIDE" ]; then
    if [[ "$CWD_OVERRIDE" != /* ]]; then
        CWD_OVERRIDE="$PROJECT_ROOT/$CWD_OVERRIDE"
    fi
    SPIRIT_CWD="$CWD_OVERRIDE"
else
    SPIRIT_CWD=$(resolve_spirit_cwd "$EXECUTOR")
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
        pair)
            # Interactive — human present, broad tools
            echo "Read,Write,Edit,Glob,Grep,Bash,WebSearch,WebFetch,Task"
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

# --- Determine interactive mode ---

# pair trust = interactive (no --print)
INTERACTIVE=""
if [ "$TRUST" = "pair" ]; then
    INTERACTIVE="yes"
fi

# --- Construct prompt ---

WP_BASENAME=$(basename "$WP_FILE")
WP_RELPATH=$(realpath --relative-to="$SPIRIT_CWD" "$WP_FILE" 2>/dev/null || echo "$WP_FILE")

if [ -n "$IMPRESSION_OVERRIDE" ]; then
    PROMPT="You are $EXECUTOR. $IMPRESSION_OVERRIDE

The full WP is at $WP_RELPATH for reference."
elif [ -n "$TASK" ]; then
    PROMPT="You are $EXECUTOR. Execute Task $TASK of work package $WP_BASENAME.

Read the WP at $WP_RELPATH for the full specification of Task $TASK.
Execute only this task. On completion:
1. Announce completion in the sutra relay
2. Commit all artifacts

If you encounter a blocking issue, announce in the sutra with details."
else
    PROMPT="You are $EXECUTOR. Execute work package $WP_BASENAME.

Read the WP at $WP_RELPATH for the full specification. Follow the
execution order. On completion:
1. Transition the WP status to 'completed' (update #+property: status)
2. Announce completion in the sutra relay
3. Commit all artifacts

If you encounter a blocking issue, transition status to
'input-required' and announce in the sutra with details."
fi

# --- Build transcript directory ---

mkdir -p "$TRANSCRIPT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
TRANSCRIPT="$TRANSCRIPT_DIR/$TIMESTAMP-$EXECUTOR.log"

# --- Invoke ---

echo "=== Dispatch ==="
echo "  WP:         $WP_BASENAME${TASK:+ (Task $TASK)}"
echo "  Executor:   $EXECUTOR"
echo "  Trust:      $TRUST"
echo "  Profile:    ${PROFILE:-<from trust>}"
echo "  CWD:        $SPIRIT_CWD"
echo "  Interactive: ${INTERACTIVE:-no}"
echo "  Transcript: $TRANSCRIPT"
echo ""

if [ -n "$DRY_RUN" ]; then
    echo "[DRY RUN] Would execute:"
    if [ -n "$INTERACTIVE" ]; then
        echo "  claude --cwd \"$SPIRIT_CWD\" \\"
        echo "         --allowedTools \"$ALLOWLIST\" \\"
        echo "         --prompt \"...\""
    else
        echo "  claude --cwd \"$SPIRIT_CWD\" \\"
        echo "         --allowedTools \"$ALLOWLIST\" \\"
        echo "         --print \\"
        echo "         --prompt \"...\""
    fi
    echo ""
    echo "Allowlist: $ALLOWLIST"
    echo ""
    echo "Prompt:"
    echo "$PROMPT"
    exit 0
fi

if [ -n "$INTERACTIVE" ]; then
    # Interactive mode for pair trust — no --print, no tee
    claude --cwd "$SPIRIT_CWD" \
           --allowedTools "$ALLOWLIST" \
           --prompt "$PROMPT"
else
    claude --cwd "$SPIRIT_CWD" \
           --allowedTools "$ALLOWLIST" \
           --print \
           --prompt "$PROMPT" \
           2>&1 | tee "$TRANSCRIPT"
fi

echo ""
echo "=== Dispatch complete ==="
echo "  Transcript: $TRANSCRIPT"
