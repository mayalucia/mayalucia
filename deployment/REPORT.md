# MayaLucIA Infrastructure Report

# Live Sites

| Domain | Technology | Status |
|----|----|----|
| [vishalsood.dev](https://vishalsood.dev) | FastAPI + Jinja2 + HTMX + Pico CSS | Live |
| [mayalucia.dev](https://mayalucia.dev) | Hugo + PaperMod (static) | Live |
| [devgeni.mayalucia.dev](https://devgeni.mayalucia.dev) | Hugo + PaperMod (static) | Live |
| [comptoir.mayalucia.dev](https://comptoir.mayalucia.dev) | Streamlit + Anthropic API | Live |
| [portal.mayalucia.dev](https://portal.mayalucia.dev) | 301 redirect → mayalucia.dev | Live |

# Source Repositories

Each site is built from its own repo. Deployment orchestration lives here in `mayalucia/deployment/`.

| Repo | Location | Remote | Serves |
|----|----|----|----|
| vishal-website | `~/Dropbox/work/vishal-website/` | `github:mayalucia/vishal-website` | vishalsood.dev |
| mayalucia | `~/Darshan/.../agentic/mayalucia/` | `github:mayalucia/mayalucia` | mayalucia.dev |
| mayadevgeni | `~/Darshan/.../agentic/mayadevgeni/` | `github:mayalucia/mayadevgeni` | devgeni.mayalucia.dev |
| mayacarya | `~/Darshan/.../agentic/mayacarya/` | `github:mayalucia/mayacarya` | comptoir.mayalucia.dev |

## What each repo contributes

- **vishal-website** — FastAPI application (`app/`), Dockerfile, `requirements.txt`. Python web app with Jinja2 templates, HTMX interactivity, AI chat (Claude Haiku), PDF generation, multi-language support.

- **mayalucia** — Hugo source for mayalucia.dev (in `website/`) and the `deployment/` directory that orchestrates all domains.

- **mayadevgeni** — Hugo source for devgeni.mayalucia.dev (in `website/`). MayaDevGenI framework documentation and 8-chapter tutorial on system-prompt craft.

- **mayacarya** — Streamlit application for comptoir.mayalucia.dev (in `app/`). Multi-candidate AI career coaching platform with 9 agents, job matching, trilingual support (EN/FR/DE), tiered access, coach dashboard.

# Container Architecture

```
Hetzner VPS (46.225.191.36)
└── Docker Compose (project: vishalsood-dev)
    ├── caddy        (ports 80/443)  → auto-TLS for all domains
    ├── web          (port 8000)     → vishalsood.dev (FastAPI)
    └── comptoir     (port 8501)     → comptoir.mayalucia.dev (Streamlit)

    Static files served directly by Caddy:
    ├── /srv/mayalucia/   → mayalucia.dev
    └── /srv/mayadevgeni/ → devgeni.mayalucia.dev
```

# Deployment Topology

```
Browser
  │
  ▼
Cloudflare DNS (free) ── A records for vishalsood.dev + mayalucia.dev
  │
  ▼  DNS only, no proxy
  │
Hetzner CPX22 (46.225.191.36)
  │
  ▼  Port 80/443
  │
┌─┴────────────────────────────────────────────┐
│  Caddy (automatic HTTPS via Let's Encrypt)   │
│                                              │
│  vishalsood.dev         → web:8000           │
│  mayalucia.dev          → /srv/mayalucia/    │
│  devgeni.mayalucia.dev  → /srv/mayadevgeni/  │
│  comptoir.mayalucia.dev → comptoir:8501      │
│  portal.mayalucia.dev   → 301 redirect       │
└──────────────────────────────────────────────┘
  │              │
  ▼              ▼
┌─────────┐  ┌───────────┐
│ FastAPI  │  │ Streamlit │
│ uvicorn  │  │           │──→ Anthropic API
│          │──→ Anthropic │    (Claude Haiku)
│          │   API        │
└─────────┘  └───────────┘
```

# VPS Layout

```
/opt/vishalsood-dev/
├── Caddyfile              # Routing for all domains
├── docker-compose.yml     # Service orchestration
├── .env                   # Secrets (ANTHROPIC_API_KEY, PASSCODES, COACH_PASSCODE)
├── vishalsood-web/        # FastAPI source (Docker-built on VPS)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
├── comptoir/              # Streamlit source (Docker-built on VPS)
│   ├── app/
│   │   ├── Dockerfile
│   │   └── ...
│   └── simulation/
├── mayalucia-public/      # Hugo output (static, served by Caddy)
└── mayadevgeni-public/    # Hugo output (static, served by Caddy)
```

# Deployment Flow

All deployment is driven by `deploy.sh` in this directory.

```
./deploy.sh {all|hugo|web|comptoir|config|verify}

  all       Build Hugo sites, rsync everything, rebuild Docker, verify
  hugo      Build Hugo locally, rsync static output to VPS
  web       Rsync vishal-website source, Docker build on VPS, restart
  comptoir  Rsync mayacarya source, Docker build on VPS, restart
  config    Rsync Caddyfile + docker-compose.yml, reload Caddy
  verify    Check all endpoints and container status
```

## Data flow per component

- **Hugo sites** — built locally (`hugo --source`), output staged in `deployment/.staging/`, rsynced to VPS. Caddy serves static files directly — no container restart needed.

- **FastAPI (web)** — source rsynced to `vishalsood-web/` on VPS, `docker compose up -d --build web` rebuilds and restarts.

- **Streamlit (comptoir)** — source rsynced to `comptoir/` on VPS, `docker compose up -d --build comptoir` rebuilds and restarts.

- **Config** — Caddyfile + docker-compose.yml rsynced, Caddy reloads automatically on config change.

Docker images are built **on the VPS** (Docker is not installed locally).

# Monthly Cost

| Item                  | Cost                 |
|-----------------------|----------------------|
| Hetzner CPX22         | EUR 6.48/month       |
| Domains (amortized)   | ~EUR 2/month         |
| Anthropic API (usage) | ~EUR 5-10/month      |
| **Total**             | **~EUR 13-18/month** |

# DNS Configuration

## vishalsood.dev (Cloudflare)

| Type | Name | Value         |
|------|------|---------------|
| A    | @    | 46.225.191.36 |
| A    | www  | 46.225.191.36 |

## mayalucia.dev (Cloudflare)

| Type | Name     | Value         |
|------|----------|---------------|
| A    | @        | 46.225.191.36 |
| A    | comptoir | 46.225.191.36 |
| A    | devgeni  | 46.225.191.36 |
| A    | portal   | 46.225.191.36 |
