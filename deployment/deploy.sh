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
#   ./deploy.sh cruvin     # build and deploy cruvin.mayalucia.dev (Next.js)
#   ./deploy.sh cruvin-api # deploy api.cruvin.mayalucia.dev (FastAPI + LiteLLM)
#   ./deploy.sh config     # deploy Caddyfile + docker-compose.yml only
#   ./deploy.sh verify     # check all endpoints
# =============================================================================

# === Configuration ============================================================

VPS_HOST="root@46.225.191.36"
VPS_DEPLOY_DIR="/opt/vishalsood-dev"
SSH_KEY="$HOME/.ssh/id_ed25519_hetzner"
SSH="ssh -i $SSH_KEY -o IdentitiesOnly=yes"

# This script's directory (deployment/)
DEPLOY_DIR="$(cd "$(dirname "$0")" && pwd)"

# Local source paths
VISHAL_WEBSITE="$HOME/Library/CloudStorage/Dropbox/work/vishal-website"
MAYALUCIA_HUGO="$DEPLOY_DIR/../website"
MAYADEVGENI_HUGO="$HOME/Darshan/research/develop/agentic/mayadevgeni/website"
MAYACARYA="$HOME/Darshan/research/develop/agentic/mayacarya"
CRUVIN="$DEPLOY_DIR/../commissions/cruvin"

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
    rsync -avz --delete -e "ssh -i $SSH_KEY -o IdentitiesOnly=yes" \
        "$STAGING/mayalucia-public/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/mayalucia-public/"

    rsync -avz --delete -e "ssh -i $SSH_KEY -o IdentitiesOnly=yes" \
        "$STAGING/mayadevgeni-public/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/mayadevgeni-public/"
}

deploy_config() {
    echo "=== Deploying Caddyfile + docker-compose.yml ==="
    rsync -avz -e "ssh -i $SSH_KEY -o IdentitiesOnly=yes" \
        "$DEPLOY_DIR/Caddyfile" \
        "$DEPLOY_DIR/docker-compose.yml" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/"

    $SSH "$VPS_HOST" "cd $VPS_DEPLOY_DIR && docker compose up -d caddy"
}

deploy_web() {
    echo "=== Deploying vishalsood.dev (FastAPI) ==="
    rsync -avz --delete -e "ssh -i $SSH_KEY -o IdentitiesOnly=yes" \
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
    rsync -avz --delete -e "ssh -i $SSH_KEY -o IdentitiesOnly=yes" \
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

    rsync -avz --delete -e "ssh -i $SSH_KEY -o IdentitiesOnly=yes" \
        --exclude='__pycache__' --exclude='.git' \
        "$BENCH_STAGING/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/bench/"

    $SSH "$VPS_HOST" "cd $VPS_DEPLOY_DIR && docker compose up -d --build bench"
}

build_cruvin() {
    echo "=== Building CruVin (Next.js static export) ==="
    (cd "$CRUVIN" && npm run build)
}

deploy_cruvin() {
    echo "=== Deploying cruvin.mayalucia.dev ==="
    rsync -avz --delete -e "ssh -i $SSH_KEY -o IdentitiesOnly=yes" \
        "$CRUVIN/out/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/cruvin-public/"

    # Ensure Caddy can see it
    $SSH "$VPS_HOST" "ln -sfn $VPS_DEPLOY_DIR/cruvin-public /srv/cruvin"
}

deploy_hatti() {
    echo "=== Deploying hatti.mayalucia.dev ==="
    HATTI="$DEPLOY_DIR/../commissions/punjab-retail/site"

    $SSH "$VPS_HOST" "mkdir -p $VPS_DEPLOY_DIR/hatti-public"

    rsync -avz --delete -e "ssh -i $SSH_KEY -o IdentitiesOnly=yes" \
        "$HATTI/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/hatti-public/"
}

deploy_hatti_api() {
    echo "=== Deploying api.hatti.mayalucia.dev (FastAPI + LiteLLM) ==="
    HATTI_API="$DEPLOY_DIR/../commissions/punjab-retail/services/hatti-api"

    rsync -avz --delete -e "ssh -i $SSH_KEY -o IdentitiesOnly=yes" \
        --exclude='__pycache__' --exclude='.git' --exclude='.env' \
        --exclude='data' \
        "$HATTI_API/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/hatti-api/"

    $SSH "$VPS_HOST" "cd $VPS_DEPLOY_DIR && docker compose up -d --build hatti-api"
}

deploy_cruvin_api() {
    echo "=== Deploying api.cruvin.mayalucia.dev (FastAPI + LiteLLM) ==="
    rsync -avz --delete -e "ssh -i $SSH_KEY -o IdentitiesOnly=yes" \
        --exclude='__pycache__' --exclude='.git' --exclude='.env' \
        "$CRUVIN/services/cruvin-api/" \
        "$VPS_HOST:$VPS_DEPLOY_DIR/cruvin-api/"

    $SSH "$VPS_HOST" "cd $VPS_DEPLOY_DIR && docker compose up -d --build cruvin-api"
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
        https://bench.mayalucia.dev \
        https://cruvin.mayalucia.dev \
        https://hatti.mayalucia.dev \
        https://api.cruvin.mayalucia.dev/api/v1/health \
        https://api.hatti.mayalucia.dev/health; do
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
    cruvin)
        build_cruvin
        deploy_cruvin
        ;;
    hatti)
        deploy_hatti
        deploy_config
        ;;
    cruvin-api)
        deploy_cruvin_api
        ;;
    hatti-api)
        deploy_hatti_api
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
        build_cruvin
        deploy_cruvin
        deploy_cruvin_api
        deploy_hatti
        deploy_hatti_api
        verify
        ;;
    *)
        echo "Usage: $0 {all|hugo|web|comptoir|bench|cruvin|cruvin-api|hatti|hatti-api|config|verify}"
        exit 1
        ;;
esac

echo ""
echo "=== Done ==="
