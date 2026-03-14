
# MentorBoxAI: AI Educational Video Engine

MentorBoxAI converts any topic into a 3Blue1Brown-style educational animation using a 6-layer AI pipeline. Type a concept, get a rendered 1080p MP4 — no animation experience needed.

**Stack:** FastAPI · Groq (llama-3.3-70b-versatile) · Manim CE v0.19 · AWS EC2 (Ubuntu, ap-south-1)

---

## AWS Services

| Service | How it's used |
| :--- | :--- |
| **EC2** (ap-south-1 Mumbai) | Hosts the FastAPI server (port 8000) and runs the Manim renderer. All code generation and video rendering happens here. Manim requires Linux (Cairo, Pango, ffmpeg) — EC2 Ubuntu 22.04 provides this cleanly. |
| **S3** (mentorbocai-videos) | Configured for video upload and CDN delivery. Credentials wired in `.env`. Not yet called in pipeline code — planned for next release. |
| **DynamoDB** | Configured for persistent job history. Planned for next release. |
| **Bedrock** | **Not used.** LLM inference moved to Groq for lower latency and free-tier availability. |

### Why EC2 and not Lambda?
Manim render jobs take 30–240 seconds and require persistent filesystem access (writing `.py` files, reading back `.mp4`). Lambda's 15-minute limit and ephemeral `/tmp` are unsuitable. EC2 gives full control over the rendering environment.

---

## Key Features
- **6-Layer AI Pipeline:** Understanding → Storyboarding → Verification → Code Generation → Refinement → Validation & Auto-Fix
- **Groq LLM (llama-3.3-70b-versatile):** Fast inference with cooldown-aware multi-key rotation across up to 4 API keys
- **Zero-LaTeX:** All visuals use `Text()` — crash-proof on any Linux server, no TeX installation needed
- **22 Template Helpers:** Pre-built `ColorfulScene` methods the LLM calls directly (phasor animation, particle physics, energy charts, collision bursts, layout zones)
- **Golden Few-Shot Examples:** NEET/JEE quality examples for biology, physics, chemistry, and maths
- **Self-Healing:** AST static check → subprocess smoke test → Groq-powered auto-patch before the user sees any error
- **1080p Output:** All renders at `-qh` (1920×1080), 240s timeout

---

## 🏗️ Project Structure
```
github-ready/
├── src/
│   └── app/
│       ├── api/v1/endpoints.py       # FastAPI endpoints: generate, status, health
│       ├── models/job.py             # Request/response models
│       ├── services/
│       │   ├── groq_client.py        # Groq client with key rotation + cooldown tracking
│       │   ├── pipeline.py           # Main 6-layer generation pipeline
│       │   ├── prompts.py            # Layer prompts + system instructions
│       │   ├── validator.py          # Static/runtime validation and auto-fixes
│       │   ├── reviewer.py           # LLM-powered repair pass for bad code
│       │   └── manim_templates.py    # Shared scene helpers and visual utilities
│       └── main.py                   # FastAPI app entry; serves frontend/
├── frontend/                         # Primary web app served by FastAPI at /
│   ├── index.html                    # Dashboard UI shell
│   ├── app.js                        # Client-side polling, modals, speaker notes
│   └── style.css                     # Frontend styles
├── docs/                             # Static copy of the frontend for GitHub Pages
│   ├── index.html
│   ├── app.js
│   └── style.css
├── output/
│   ├── manim/                        # Generated temporary Manim scripts
│   └── videos/                       # Rendered MP4 outputs
├── scripts/
│   ├── start.sh                      # Linux/EC2 startup helper
│   └── deploy_aws.sh                 # Deployment helper
├── tests/                            # Test and validation scripts
├── alembic/                          # DB migration scaffolding (future persistence work)
├── .env.example                      # Environment template
├── Dockerfile                        # Production container
├── requirements.txt                  # Python dependencies
├── bedrock_ping_test.py              # Legacy connectivity script name; currently used for service checks
├── DESIGN.md                         # Product/design notes
├── PROJECT_NOTES.md                  # Build and deployment notes
├── UPDATED_ARCHITECTURE.md           # Expanded system architecture write-up
└── README.md                         # Project documentation
```

---

## 🧠 The 6-Layer Pipeline
| Layer | Stage | Purpose |
| :--- | :--- | :--- |
| **1** | **Understanding** | Deconstructs topic into key facts and cinematic script |
| **2** | **Storyboarding** | Maps script into visual plan (scenes, objects, timings) |
| **3** | **Verification** | Validates plan against technical and pedagogical constraints |
| **4** | **Code Generation** | Translates storyboard into Manim Python code using few-shot templates |
| **5** | **Refinement** | Enhances visuals with effects and quality improvements |
| **6** | **Validation & Fix** | Static and runtime validation, auto-patching for crash-free output |

---

## ✨ System Architecture
```
User Input (Topic, Duration)
		 │
		 ▼
┌─────────────────┐
│  Layer 1:       │
│  Understanding  │──→ understanding.json
└────────┬────────┘
		 │
		 ▼
┌─────────────────┐
│  Layer 2:       │
│  Storyboarding  │──→ plan.json
└────────┬────────┘
		 │
		 ▼
┌─────────────────┐
│  Layer 3:       │
│  Verification   │──→ verified_plan.json
└────────┬────────┘
		 │
		 ▼
┌─────────────────┐
│  Layer 4:       │
│  Code Generation│──→ scene.py (draft)
└────────┬────────┘
		 │
		 ▼
┌─────────────────┐
│  Layer 5:       │
│  Refinement     │──→ scene.py (enhanced)
└────────┬────────┘
		 │
		 ▼
┌─────────────────┐
│  Layer 6:       │
│  Validation     │──→ scene.py (final)
└────────┬────────┘
		 │
		 ▼
┌─────────────────┐
│  Manim Render   │──→ video.mp4
└─────────────────┘
```

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- Manim Community Edition v0.19+ with ffmpeg and sox (**Linux/WSL only** for rendering)
- Groq API key (free at [console.groq.com](https://console.groq.com))
- AWS account for EC2 deployment (optional for local dev)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Configuration
Copy `.env.example` to `.env` and fill in:
```env
GROQ_API_KEY1=gsk_...
GROQ_API_KEY2=gsk_...   # optional, for rate-limit rotation
GROQ_API_KEY3=gsk_...   # optional
GROQ_API_KEY4=gsk_...   # optional
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET=mentorbocai-videos
```

### 4. Launch (EC2 / Linux)
```bash
cd /home/ubuntu/app
venv/bin/uvicorn src.app.main:app --host 0.0.0.0 --port 8000
```

### 4. Launch (local dev — Windows, no rendering)
```powershell
.\run-local.ps1
```
Open [http://localhost:8000](http://localhost:8000)

> **Note:** Manim rendering only works on Linux. On Windows, code generation and pipeline layers work, but the render step will fail unless you have WSL with Manim installed.

---

## Generating a Video

```bash
curl -X POST http://<EC2_IP>:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"concept":"simple harmonic motion","goal":"explain for JEE","duration_seconds":60,"max_scenes":5,"auto_render":true}'
```

Poll for completion:
```bash
curl http://<EC2_IP>:8000/api/status/<job_id>
```

---

## LLM: Groq (not AWS Bedrock)
All LLM calls go through **Groq** (`llama-3.3-70b-versatile`), not AWS Bedrock. Groq was chosen for:
- **~10× lower latency** than Bedrock for this model size
- Free tier sufficient for development and demo
- Simple REST API with Python SDK

### How round-robin API-key rotation works

The client in `src/app/services/groq_client.py` supports **up to 4 Groq API keys** (`GROQ_API_KEY1` ... `GROQ_API_KEY4`).

It does not blindly spam one key until failure. Instead:

1. It loads all configured keys from `.env`.
2. On each LLM call, it tries every key that is **not currently in cooldown**.
3. If a key gets `HTTP 429`, it reads `retry-after` / `x-ratelimit-reset-requests` and marks that key unavailable until that cooldown expires.
4. If a key gets `401` or `403`, it is put into a long cooldown to avoid wasting retries on a bad key.
5. If all keys are cooling down, the client waits for the **soonest available key**, then retries.
6. On success, the cooldown for that key is cleared and the response is returned immediately.

This gives us a practical **round-robin + failover** strategy:
- spreads traffic across multiple keys,
- avoids hammering a rate-limited key,
- survives temporary 429s during heavy 6-layer runs,
- and prevents startup-time quota waste because keys are tested lazily only when first used.

The client also logs Groq rate-limit response headers so we can monitor remaining request/token budget during real runs.

---

## Troubleshooting
| Issue | Solution |
|-------|----------|
| `NameError` / `ImportError` in render | Validator auto-fixes most issues. Re-run generation. |
| Video too short | Increase `duration_seconds` |
| Text overflow / overlap | Title max 25 chars, captions auto-wrapped at 40 chars |
| Render fails | Must run on Linux (EC2/WSL). Windows render is not supported. |
| Groq rate limit | Add extra keys as `GROQ_API_KEY2`, `GROQ_API_KEY3`, `GROQ_API_KEY4`; the client rotates and waits on cooldown automatically |
| EC2 port 8000 unreachable | Check Security Group inbound rule: TCP 8000, source 0.0.0.0/0 |

---

## Further Reading
- [UPDATED_ARCHITECTURE.md](UPDATED_ARCHITECTURE.md) — full pipeline and component map
- [DESIGN.md](DESIGN.md) — product/design rationale
- [requirements.md](requirements.md) — feature requirements
- [PROJECT_NOTES.md](PROJECT_NOTES.md) — deployment and implementation notes

---

## License
MIT
