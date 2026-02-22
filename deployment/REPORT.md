# MayaLucIA Infrastructure Report

## Live Sites

| URL | Technology | Status |
|-----|------------|--------|
| vishalsood.dev | FastAPI + Jinja2 + HTMX + Pico CSS | Live |
| mayalucia.dev | Hugo + PaperMod (static) | Live |
| devgeni.mayalucia.dev | Hugo + PaperMod (static) | Live |
| comptoir.mayalucia.dev | Streamlit + Anthropic API | Live |
| portal.mayalucia.dev | 301 redirect → mayalucia.dev | Live |

## Container Architecture

```
Hetzner VPS (46.225.191.36)
└── Docker Compose (project: vishalsood-dev)
    ├── caddy        (ports 80/443) → auto-TLS for all domains
    ├── web          (port 8000)    → vishalsood.dev (FastAPI)
    └── comptoir     (port 8501)    → comptoir.mayalucia.dev (Streamlit)

    Static files served directly by Caddy:
    ├── /srv/mayalucia/   → mayalucia.dev
    └── /srv/mayadevgeni/ → devgeni.mayalucia.dev
```

## VPS Layout

```
/opt/vishalsood-dev/
├── Caddyfile              # Routing for all domains
├── docker-compose.yml     # Service orchestration
├── .env                   # Secrets (ANTHROPIC_API_KEY, PASSCODES, COACH_PASSCODE)
├── vishalsood-web/        # FastAPI app source (built on VPS)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
├── comptoir/              # Streamlit app source (built on VPS)
│   ├── app/
│   │   ├── Dockerfile
│   │   └── ...
│   └── simulation/
├── mayalucia-public/      # Hugo output (static, served by Caddy)
└── mayadevgeni-public/    # Hugo output (static, served by Caddy)
```

## Deployment Topology

```
User's Browser
     │
     ▼
Cloudflare DNS (free) — A records for vishalsood.dev + mayalucia.dev
     │
     ▼ DNS only, no proxy
     │
Hetzner CPX22 (46.225.191.36)
     │
     ▼ Port 80/443
     │
┌────┴──────────────────────────────────────────┐
│  Caddy (automatic HTTPS via Let's Encrypt)    │
│                                               │
│  vishalsood.dev           → web:8000          │
│  mayalucia.dev            → /srv/mayalucia/   │
│  devgeni.mayalucia.dev    → /srv/mayadevgeni/ │
│  comptoir.mayalucia.dev   → comptoir:8501     │
│  portal.mayalucia.dev     → redirect          │
└───────────────────────────────────────────────┘
     │              │
     ▼              ▼
┌─────────┐  ┌───────────┐
│ FastAPI  │  │ Streamlit │
│ (Python) │  │ (Python)  │──→ Anthropic API
│          │──→ Anthropic │     (Claude Haiku)
│ uvicorn  │   API        │
└─────────┘  └───────────┘
```

## Monthly Cost

| Item | Cost |
|------|------|
| Hetzner CPX22 | EUR 6.48/month |
| Domains (amortized) | ~EUR 2/month |
| Anthropic API (usage) | ~EUR 5-10/month |
| **Total** | **~EUR 13-18/month** |

## Source Repo Map

| Repo | Location | What It Provides |
|------|----------|-----------------|
| vishal-website | `~/Dropbox/work/vishal-website/` | FastAPI app + Dockerfile |
| mayalucia | `~/Darshan/.../mayalucia/` | Hugo source (mayalucia.dev) + deployment/ |
| mayadevgeni | `~/Darshan/.../mayadevgeni/website/` | Hugo source (devgeni.mayalucia.dev) |
| mayacarya | `~/Darshan/.../mayacarya/` | Streamlit app + Dockerfile (comptoir) |
