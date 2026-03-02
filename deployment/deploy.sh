#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# deploy.sh — Build and deploy all sites to the VPS
#
# Usage:
#   ./deploy.sh          # deploy everything
#   ./deploy.sh hugo     # rebuild and deploy Hugo sites only
#   ./deploy.sh web      # deploy vishalsood.dev (FastAPI) only
#   ./deploy.sh comptoir # deploy comptoir.mayalucia.dev (Streamlit) only
#   ./deploy.sh config   # deploy Caddyfile + docker-compose.yml only
#   ./deploy.sh verify   # check all endpoints
# =============================================================================

# === Configuration ============================================================

VPS_HOST="root@46.225.191.36"
VPS_DEPLOY_DIR="/opt/vishalsood-dev"
SSH_KEY="$HOME/.ssh/id_ed25519_hetzner"
SSH="ssh -i $SSH_KEY"

# This script's directory (deployment/)
DEPLOY_DIR="$(cd "$(dirname "$0")" && pwd)"

# Local source paths
VISHAL_WEBSITE="$HOME/Library/CloudStorage/Dropbox/work/vishal-website"
MAYALUCIA_HUGO="$DEPLOY_DIR/../website"
MAYADEVGENI_HUGO="$HOME/Darshan/research/develop/agentic/mayadevgeni/website"
MAYACARYA="$HOME/Darshan/research/develop/agentic/mayacarya"

# Hugo build output (gitignored staging area)
STAGING="$DEPLOY_DIR/.staging"

# === Functions ================================================================

build_hugo() {
    echo "=== Building Hugo sites ==="
    mkdir -p "$STAGING/mayalucia-public" "$STAGING/mayadevgeni-public"

    echo "  mayalucia.dev ..."
    hugo --source "$MAYALUCIA_HUGO" \
         --destination "$STAGING/mayalucia-public" \
         --cleanDestinationDir

    echo "  devgeni.mayalucia.dev ..."
    hugo --source "$MAYADEVGENI_HUGO" \
         --destination "$STAGING/mayadevgeni-public" \
         --cleanDestinationDir
}

deploy_hugo() {
    echo "=== Deploying Hugo sites ==="
    rsync -avz --delete -e "ssh -i $SSH_KEY" \
        "$STAGING/mayalucia-public/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/mayalucia-public/"

    rsync -avz --delete -e "ssh -i $SSH_KEY" \
        "$STAGING/mayadevgeni-public/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/mayadevgeni-public/"
}

deploy_config() {
    echo "=== Deploying Caddyfile + docker-compose.yml ==="
    rsync -avz -e "ssh -i $SSH_KEY" \
        "$DEPLOY_DIR/Caddyfile" \
        "$DEPLOY_DIR/docker-compose.yml" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/"

    $SSH "$VPS_HOST" "cd $VPS_DEPLOY_DIR && docker compose up -d caddy"
}

deploy_web() {
    echo "=== Deploying vishalsood.dev (FastAPI) ==="
    rsync -avz --delete -e "ssh -i $SSH_KEY" \
        --exclude='.venv' --exclude='__pycache__' --exclude='.git' \
        --exclude='.env' --exclude='.claude' --exclude='.agent-shell' \
        --exclude='sessions' --exclude='content-pipeline' \
        --exclude='mayalucia-public' --exclude='mayadevgeni-public' \
        --include='Dockerfile' --include='requirements.txt' \
        --include='app/***' \
        --exclude='*' \
        "$VISHAL_WEBSITE/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/vishalsood-web/"

    $SSH "$VPS_HOST" "cd $VPS_DEPLOY_DIR && docker compose up -d --build web"
}

deploy_comptoir() {
    echo "=== Deploying comptoir.mayalucia.dev (Streamlit) ==="
    rsync -avz --delete -e "ssh -i $SSH_KEY" \
        --exclude='.venv' --exclude='__pycache__' --exclude='.git' \
        --exclude='.env' --exclude='.claude' --exclude='.agent-shell' \
        --exclude='sessions' --exclude='develop' \
        --exclude='app/data' --exclude='app/.streamlit/secrets.toml' \
        --include='app/***' --include='simulation/***' \
        --exclude='*' \
        "$MAYACARYA/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/comptoir/"

    $SSH "$VPS_HOST" "cd $VPS_DEPLOY_DIR && docker compose up -d --build comptoir"
}

deploy_bench() {
    echo "=== Deploying bench.mayalucia.dev (Streamlit) ==="

    # dmt-eval lives at modules/dmt-eval relative to the project root
    DMT_EVAL="$DEPLOY_DIR/../modules/dmt-eval"

    # Stage bench build context: needs bench/, src/, Dockerfile, requirements.txt
    BENCH_STAGING="$STAGING/bench"
    rm -rf "$BENCH_STAGING"
    mkdir -p "$BENCH_STAGING/bench" "$BENCH_STAGING/src"

    cp -r "$DMT_EVAL/bench/"* "$BENCH_STAGING/bench/"
    cp -r "$DMT_EVAL/src/"* "$BENCH_STAGING/src/"
    cp "$DMT_EVAL/bench/Dockerfile" "$BENCH_STAGING/Dockerfile"
    cp "$DMT_EVAL/bench/requirements.txt" "$BENCH_STAGING/requirements.txt"

    rsync -avz --delete -e "ssh -i $SSH_KEY" \
        --exclude='__pycache__' --exclude='.git' \
        "$BENCH_STAGING/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/bench/"

    $SSH "$VPS_HOST" "cd $VPS_DEPLOY_DIR && docker compose up -d --build bench"
}

verify() {
    echo "=== Verifying ==="
    $SSH "$VPS_HOST" "cd $VPS_DEPLOY_DIR && docker compose ps"
    echo ""
    echo "Testing endpoints..."
    for url in \
        https://vishalsood.dev \
        https://mayalucia.dev \
        https://devgeni.mayalucia.dev \
        https://comptoir.mayalucia.dev \
        https://bench.mayalucia.dev; do
        status=$(curl -sI "$url" | head -1)
        echo "  $url → $status"
    done
    # Redirect check
    location=$(curl -sI https://portal.mayalucia.dev | grep -i '^location:' | tr -d '\r')
    echo "  https://portal.mayalucia.dev → 301 $location"
}

# === Main =====================================================================

case "${1:-all}" in
    hugo)
        build_hugo
        deploy_hugo
        ;;
    web)
        deploy_web
        ;;
    comptoir)
        deploy_comptoir
        ;;
    bench)
        deploy_bench
        ;;
    config)
        deploy_config
        ;;
    verify)
        verify
        ;;
    all)
        build_hugo
        deploy_config
        deploy_hugo
        deploy_web
        deploy_comptoir
        deploy_bench
        verify
        ;;
    *)
        echo "Usage: $0 {all|hugo|web|comptoir|bench|config|verify}"
        exit 1
        ;;
esac

echo ""
echo "=== Done ==="
