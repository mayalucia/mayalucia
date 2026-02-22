# Deployment Guide

Centralized deployment for all MayaLucIA infrastructure: vishalsood.dev, mayalucia.dev, devgeni.mayalucia.dev, comptoir.mayalucia.dev, and portal.mayalucia.dev.

## Prerequisites

- **VPS**: Hetzner CPX22 (Ubuntu 24.04, Docker installed)
- **SSH key**: `~/.ssh/id_ed25519_hetzner`
- **Hugo**: >= 0.146.0 (installed locally for static site builds)
- **Domains**: vishalsood.dev + mayalucia.dev (Cloudflare DNS, A records pointing to VPS)

## Architecture

```
Local machine                          VPS (46.225.191.36)
─────────────                          ────────────────────
vishal-website/    ──rsync──►  /opt/vishalsood-dev/vishalsood-web/
mayacarya/         ──rsync──►  /opt/vishalsood-dev/comptoir/
Hugo sites         ──build+rsync──►  /opt/vishalsood-dev/{mayalucia,mayadevgeni}-public/
deployment/        ──rsync──►  /opt/vishalsood-dev/{Caddyfile,docker-compose.yml}
```

Docker images are built **on the VPS** after rsyncing source.

## Source Repositories

| Site | Source Repo | Technology |
|------|------------|------------|
| vishalsood.dev | `~/Dropbox/work/vishal-website/` | FastAPI + Jinja2 + HTMX |
| mayalucia.dev | `~/Darshan/.../mayalucia/modules/mayaportal/web/sites/` | Hugo + PaperMod |
| devgeni.mayalucia.dev | `~/Darshan/.../mayadevgeni/website/` | Hugo + PaperMod |
| comptoir.mayalucia.dev | `~/Darshan/.../mayacarya/` | Streamlit + Anthropic API |
| portal.mayalucia.dev | Caddyfile (301 redirect) | — |

## First-Time VPS Setup

```bash
# 1. SSH in
ssh -i ~/.ssh/id_ed25519_hetzner root@46.225.191.36

# 2. Install Docker (if not already)
curl -fsSL https://get.docker.com | sh
apt install -y docker-compose-plugin

# 3. Create deploy directory
mkdir -p /opt/vishalsood-dev/{vishalsood-web,comptoir}

# 4. Create .env with secrets
cat > /opt/vishalsood-dev/.env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-your-key-here
PASSCODES=comma,separated,codes
COACH_PASSCODE=your-coach-code
EOF
chmod 600 /opt/vishalsood-dev/.env
```

## Deploying

From this directory (`deployment/`):

```bash
# Deploy everything (Hugo build + rsync all + Docker build + verify)
./deploy.sh

# Deploy only specific components
./deploy.sh hugo       # Rebuild and deploy Hugo sites
./deploy.sh web        # Deploy FastAPI app
./deploy.sh comptoir   # Deploy Streamlit app
./deploy.sh config     # Deploy Caddyfile + docker-compose.yml
./deploy.sh verify     # Check all endpoints
```

## DNS Configuration

### vishalsood.dev (Cloudflare)
| Type | Name | Value |
|------|------|-------|
| A | @ | 46.225.191.36 |
| A | www | 46.225.191.36 |

### mayalucia.dev (Cloudflare)
| Type | Name | Value |
|------|------|-------|
| A | @ | 46.225.191.36 |
| A | comptoir | 46.225.191.36 |
| A | devgeni | 46.225.191.36 |
| A | portal | 46.225.191.36 |

## Troubleshooting

**Caddy can't get certificate**: DNS hasn't propagated. Wait 5 minutes, then `docker compose restart caddy` on VPS.

**Comptoir returns error**: Check API key: `docker compose exec comptoir env | grep ANTHROPIC`

**Check logs**: `ssh -i ~/.ssh/id_ed25519_hetzner root@46.225.191.36 "cd /opt/vishalsood-dev && docker compose logs -f --tail=50"`

**Check resource usage**: `docker compose stats` on VPS.
