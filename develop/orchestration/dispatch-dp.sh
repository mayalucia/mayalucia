#!/usr/bin/env bash
# dispatch-dp.sh — read a Dispatch Plan, print the dispatch board,
#                   optionally dispatch a ready WP
#
# Usage:
#   dispatch-dp.sh <dp-file>                     # print board
#   dispatch-dp.sh <dp-file> --dispatch <ref>    # dispatch a ready WP
#   dispatch-dp.sh <dp-file> --dispatch next     # dispatch first ready WP
#   dispatch-dp.sh <dp-file> --dry-run <ref>     # dry-run a specific WP
#   dispatch-dp.sh <dp-file> --mark-done <ref>   # mark a WP ref as completed
#
# DP files must have:
#   #+property: wps <comma-separated WP refs>
#   #+property: edges <comma-separated from>to edges>
#
# WP refs: NNNN (whole WP) or NNNNT (task T of WP NNNN)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DISPATCH_SH="$SCRIPT_DIR/dispatch.sh"
ABURAYA="$PROJECT_ROOT/aburaya"

# DP-local state file: tracks per-ref completion within a DP
# Lives alongside the DP file as .<dp-basename>.state
dp_state_file() {
    local dp_dir dp_base
    dp_dir="$(dirname "$1")"
    dp_base="$(basename "$1" .org)"
    echo "$dp_dir/.$dp_base.state"
}

# --- Arguments ---

if [ $# -lt 1 ]; then
    echo "Usage: $0 <dp-file> [--dispatch <ref>|next] [--dry-run <ref>] [--mark-done <ref>]" >&2
    exit 1
fi

DP_FILE="$1"
shift

ACTION="board"  # board | dispatch | dry-run | mark-done
TARGET=""

while [ $# -gt 0 ]; do
    case "$1" in
        --dispatch)
            ACTION="dispatch"
            TARGET="$2"
            shift 2
            ;;
        --dry-run)
            ACTION="dry-run"
            TARGET="$2"
            shift 2
            ;;
        --mark-done)
            ACTION="mark-done"
            TARGET="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

if [ ! -f "$DP_FILE" ]; then
    if [ -f "$PROJECT_ROOT/$DP_FILE" ]; then
        DP_FILE="$PROJECT_ROOT/$DP_FILE"
    else
        echo "ERROR: DP file not found: $DP_FILE" >&2
        exit 1
    fi
fi

STATE_FILE=$(dp_state_file "$DP_FILE")

# --- Extract DP metadata ---

extract_dp_property() {
    local prop="$1"
    grep -i "^#+property:.*$prop" "$DP_FILE" 2>/dev/null | head -1 | sed "s/.*$prop *//i" | xargs || true
}

DP_TITLE=$(grep -i "^#+title:" "$DP_FILE" 2>/dev/null | head -1 | sed 's/^#+title: *//i')
DP_STATUS=$(extract_dp_property "status")
WPS_RAW=$(extract_dp_property "wps")
EDGES_RAW=$(extract_dp_property "edges")

if [ -z "$WPS_RAW" ]; then
    echo "ERROR: no #+property: wps in $DP_FILE" >&2
    exit 1
fi

# Parse WP refs into array
IFS=',' read -ra WP_REFS <<< "$WPS_RAW"

# Parse edges into associative arrays
declare -A UPSTREAM_OF  # UPSTREAM_OF[ref] = "dep1 dep2 ..."
for ref in "${WP_REFS[@]}"; do
    ref=$(echo "$ref" | xargs)
    UPSTREAM_OF["$ref"]=""
done

if [ -n "$EDGES_RAW" ]; then
    IFS=',' read -ra EDGES <<< "$EDGES_RAW"
    for edge in "${EDGES[@]}"; do
        edge=$(echo "$edge" | xargs)
        from="${edge%%>*}"
        to="${edge##*>}"
        from=$(echo "$from" | xargs)
        to=$(echo "$to" | xargs)
        existing="${UPSTREAM_OF[$to]:-}"
        if [ -n "$existing" ]; then
            UPSTREAM_OF["$to"]="$existing $from"
        else
            UPSTREAM_OF["$to"]="$from"
        fi
    done
fi

# --- Resolve WP ref to file and metadata ---

# ref_status: check DP-local state first, then WP file
ref_status() {
    local ref="$1"

    # Check DP-local state file
    if [ -f "$STATE_FILE" ]; then
        local local_status
        local_status=$(grep "^$ref:" "$STATE_FILE" 2>/dev/null | head -1 | sed 's/^[^:]*: *//')
        if [ -n "$local_status" ]; then
            echo "$local_status"
            return
        fi
    fi

    # Fall back to WP file status
    local wp_file
    wp_file=$(ref_to_file "$ref")
    if [ -n "$wp_file" ] && [ -f "$wp_file" ]; then
        grep -i "^#+property:.*status" "$wp_file" 2>/dev/null | head -1 | sed "s/.*status *//i" | xargs || echo "unknown"
    else
        echo "unknown"
    fi
}

ref_to_file() {
    local ref="$1"
    # Strip task letter: 0004A -> 0004
    local wp_num="${ref%%[A-Z]*}"
    # Find the WP file
    local found
    found=$(find "$PROJECT_ROOT/workpacks" -maxdepth 1 -name "${wp_num}-*.org" 2>/dev/null | head -1)
    echo "$found"
}

ref_task() {
    local ref="$1"
    # Extract task letter: 0004A -> A, 0009 -> ""
    local task="${ref##*[0-9]}"
    # Only return if it's a single uppercase letter
    if [[ "$task" =~ ^[A-Z]$ ]]; then
        echo "$task"
    fi
}

# Per-ref DP property: #+property: <ref>.<key> <value>
extract_ref_property() {
    local ref="$1" key="$2"
    grep -i "^#+property:.*${ref}\.${key}" "$DP_FILE" 2>/dev/null | head -1 | sed "s/.*${ref}\.${key} *//i" | xargs || true
}

ref_executor() {
    local ref="$1"
    # DP per-ref override first
    local dp_val
    dp_val=$(extract_ref_property "$ref" "executor")
    if [ -n "$dp_val" ]; then
        echo "$dp_val"
        return
    fi
    # Fall back to WP file
    local wp_file
    wp_file=$(ref_to_file "$ref")
    if [ -n "$wp_file" ] && [ -f "$wp_file" ]; then
        grep -i "^#+property:.*executor" "$wp_file" 2>/dev/null | head -1 | sed "s/.*executor *//i" | xargs || true
    fi
}

ref_trust() {
    local ref="$1"
    # DP per-ref override first
    local dp_val
    dp_val=$(extract_ref_property "$ref" "trust")
    if [ -n "$dp_val" ]; then
        echo "$dp_val"
        return
    fi
    # Fall back to WP file
    local wp_file
    wp_file=$(ref_to_file "$ref")
    if [ -n "$wp_file" ] && [ -f "$wp_file" ]; then
        local trust
        trust=$(grep -i "^#+property:.*trust" "$wp_file" 2>/dev/null | head -1 | sed "s/.*trust *//i" | xargs || true)
        echo "${trust:-spec-tighten}"
    else
        echo "spec-tighten"
    fi
}

ref_dir() {
    local ref="$1"
    # DP per-ref override first
    local dp_val
    dp_val=$(extract_ref_property "$ref" "dir")
    if [ -n "$dp_val" ]; then
        if [[ "$dp_val" != /* ]]; then
            dp_val="$PROJECT_ROOT/$dp_val"
        fi
        echo "$dp_val"
        return
    fi
    # Fall back to spirit identity resolution
    local executor
    executor=$(ref_executor "$ref")
    resolve_spirit_cwd "$executor"
}

ref_title() {
    local ref="$1"
    local wp_file
    wp_file=$(ref_to_file "$ref")
    if [ -n "$wp_file" ] && [ -f "$wp_file" ]; then
        local title
        title=$(grep -i "^#+title:" "$wp_file" 2>/dev/null | head -1 | sed 's/^#+title: *//i')
        local task
        task=$(ref_task "$ref")
        if [ -n "$task" ]; then
            echo "$title (Task $task)"
        else
            echo "$title"
        fi
    else
        echo "WP-$ref"
    fi
}

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

# --- Evaluate DAG ---

is_ready() {
    local ref="$1"
    local status
    status=$(ref_status "$ref")

    # Must be tightened or resumed (or drafted for pair trust)
    local trust
    trust=$(ref_trust "$ref")
    if [ "$trust" = "pair" ]; then
        if [[ "$status" != "tightened" && "$status" != "resumed" && "$status" != "drafted" ]]; then
            return 1
        fi
    else
        if [[ "$status" != "tightened" && "$status" != "resumed" ]]; then
            return 1
        fi
    fi

    # All upstream must be completed
    local deps="${UPSTREAM_OF[$ref]:-}"
    if [ -n "$deps" ]; then
        for dep in $deps; do
            local dep_status
            dep_status=$(ref_status "$dep")
            if [ "$dep_status" != "completed" ]; then
                return 1
            fi
        done
    fi

    return 0
}

is_completed() {
    local ref="$1"
    local status
    status=$(ref_status "$ref")
    [ "$status" = "completed" ]
}

is_blocked() {
    local ref="$1"
    ! is_ready "$ref" && ! is_completed "$ref"
}

# --- Mark done ---

mark_ref_done() {
    local ref="$1"
    if [ -f "$STATE_FILE" ]; then
        # Update or append
        if grep -q "^$ref:" "$STATE_FILE" 2>/dev/null; then
            sed -i "s/^$ref:.*/$ref: completed/" "$STATE_FILE"
        else
            echo "$ref: completed" >> "$STATE_FILE"
        fi
    else
        echo "$ref: completed" > "$STATE_FILE"
    fi
    echo "Marked $ref as completed in $(basename "$STATE_FILE")"
}

# --- Print dispatch board ---

print_board() {
    local has_ready=false
    local has_blocked=false
    local has_completed=false
    local ready_refs=()
    local blocked_refs=()
    local completed_refs=()

    for ref in "${WP_REFS[@]}"; do
        ref=$(echo "$ref" | xargs)
        if is_completed "$ref"; then
            has_completed=true
            completed_refs+=("$ref")
        elif is_ready "$ref"; then
            has_ready=true
            ready_refs+=("$ref")
        else
            has_blocked=true
            blocked_refs+=("$ref")
        fi
    done

    echo "=== $DP_TITLE ==="
    echo "    Status: $DP_STATUS"
    echo ""

    # Completed
    if $has_completed; then
        for ref in "${completed_refs[@]}"; do
            local title
            title=$(ref_title "$ref")
            echo "── WP-$ref: $title (completed) ──"
        done
        echo ""
    fi

    # Ready
    if $has_ready; then
        for ref in "${ready_refs[@]}"; do
            local title executor trust cwd wp_file task
            title=$(ref_title "$ref")
            executor=$(ref_executor "$ref")
            trust=$(ref_trust "$ref")
            cwd=$(ref_dir "$ref")
            wp_file=$(ref_to_file "$ref")
            task=$(ref_task "$ref")

            # Look up guild from executor identity
            local guild="—"
            local identity_file
            identity_file=$(find "$ABURAYA/spirits" -path "*/$executor/identity.yaml" 2>/dev/null | head -1)
            if [ -n "$identity_file" ]; then
                guild=$(grep "  guild:" "$identity_file" 2>/dev/null | head -1 | sed 's/.*guild: *//' | xargs || echo "—")
            fi

            local rel_cwd
            rel_cwd=$(realpath --relative-to="$PROJECT_ROOT" "$cwd" 2>/dev/null || echo "$cwd")
            local rel_wp
            rel_wp=$(realpath --relative-to="$PROJECT_ROOT" "$wp_file" 2>/dev/null || echo "$wp_file")

            echo "── WP-$ref: $title ──────────────────────────────"
            echo "Spirit:  $executor"
            echo "Guild:   $guild"
            echo "Trust:   $trust"
            echo "Dir:     $rel_cwd"
            echo "WP:      $rel_wp${task:+ (Task $task)}"
            echo ""
            echo "  agent-shell-spawn \"$executor\" \"$rel_cwd\" \"Execute${task:+ Task $task of} $title\""
            echo ""
        done
    fi

    # Blocked
    if $has_blocked; then
        for ref in "${blocked_refs[@]}"; do
            local title
            title=$(ref_title "$ref")
            local waiting=""
            local deps="${UPSTREAM_OF[$ref]:-}"
            for dep in $deps; do
                local dep_status
                dep_status=$(ref_status "$dep")
                if [ "$dep_status" != "completed" ]; then
                    if [ -n "$waiting" ]; then
                        waiting="$waiting, WP-$dep"
                    else
                        waiting="WP-$dep"
                    fi
                fi
            done
            local status
            status=$(ref_status "$ref")
            echo "── WP-$ref: $title (blocked) ────────────────────"
            echo "Waiting: ${waiting:-<status: $status>}"
            echo ""
        done
    fi

    if ! $has_ready && ! $has_blocked; then
        echo "All WPs completed. DP is done."
    fi

    if ! $has_ready && $has_blocked; then
        echo "No WPs ready — all remaining are blocked."
    fi
}

# --- Dispatch ---

dispatch_ref() {
    local ref="$1"
    local dry_run_flag="$2"

    if ! is_ready "$ref"; then
        echo "ERROR: WP-$ref is not ready (status: $(ref_status "$ref"), check upstream)" >&2
        return 1
    fi

    local wp_file task executor trust cwd
    wp_file=$(ref_to_file "$ref")
    task=$(ref_task "$ref")
    executor=$(ref_executor "$ref")
    trust=$(ref_trust "$ref")
    cwd=$(ref_dir "$ref")

    if [ -z "$wp_file" ] || [ ! -f "$wp_file" ]; then
        echo "ERROR: cannot resolve WP file for ref $ref" >&2
        return 1
    fi

    local dispatch_args=("$wp_file")
    if [ -n "$task" ]; then
        dispatch_args+=(--task "$task")
    fi
    if [ -n "$executor" ]; then
        dispatch_args+=(--executor "$executor")
    fi
    if [ -n "$trust" ]; then
        dispatch_args+=(--trust "$trust")
    fi
    if [ -n "$cwd" ]; then
        dispatch_args+=(--cwd "$cwd")
    fi
    if [ -n "$dry_run_flag" ]; then
        dispatch_args+=(--dry-run)
    fi

    "$DISPATCH_SH" "${dispatch_args[@]}"
}

find_first_ready() {
    for ref in "${WP_REFS[@]}"; do
        ref=$(echo "$ref" | xargs)
        if is_ready "$ref"; then
            echo "$ref"
            return
        fi
    done
}

# --- Main ---

case "$ACTION" in
    board)
        print_board
        ;;
    mark-done)
        mark_ref_done "$TARGET"
        echo ""
        print_board
        ;;
    dispatch|dry-run)
        if [ "$TARGET" = "next" ]; then
            TARGET=$(find_first_ready)
            if [ -z "$TARGET" ]; then
                echo "No ready WPs to dispatch." >&2
                echo ""
                print_board
                exit 1
            fi
            echo "Next ready: WP-$TARGET"
            echo ""
        fi

        echo "--- Board before dispatch ---"
        print_board
        echo ""
        echo "--- Dispatching WP-$TARGET ---"
        echo ""

        if [ "$ACTION" = "dry-run" ]; then
            dispatch_ref "$TARGET" "yes"
        else
            dispatch_ref "$TARGET" ""
            echo ""
            echo "--- Board after dispatch ---"
            print_board
        fi
        ;;
esac
