
# MentorBoxAI: Production-Grade Educational Video Engine

MentorBoxAI is a robust FastAPI backend for generating professional 3Blue1Brown-style educational animations from a single text prompt. The system implements a 6-layer AI pipeline, **Groq LLM integration** (llama-3.3-70b-versatile) with automatic key rotation, and a modular `src/app` layout for scalability, reliability, and developer productivity.

---

## 🚀 Key Features
- **6-Layer AI Pipeline:** Understanding, Storyboarding, Verification, Code Generation, Refinement, Validation & Auto-Fix
- **Groq LLM (llama-3.3-70b-versatile):** Fast inference with automatic key rotation across 3 API keys
- **Zero-LaTeX Architecture:** Crash-proof, screen-safe visuals using only Text() objects
- **Golden Few-Shot Prompting:** NEET/JEE quality Manim code with biology, physics, chemistry examples
- **Self-Healing Logic:** AST-based static validation + runtime smoke test + Groq-powered auto-fix loop
- **Production-Ready Structure:** Modular src/app layout, versioned API, Docker, scripts, and test coverage
- **AWS Integration:** S3, DynamoDB, Lambda (ap-south-1 Mumbai) — Bedrock NOT used

---

## 🏗️ Project Structure
```
github-ready/
├── src/
│   └── app/
│       ├── api/v1/endpoints.py       # FastAPI endpoints
│       ├── models/job.py             # Pydantic models
│       ├── services/
│       │   ├── groq_client.py        # Groq API client with key rotation
│       │   ├── pipeline.py           # 6-layer pipeline logic
│       │   ├── prompts.py            # All prompt templates (L1-L5 + system)
│       │   ├── few_shot_examples.py  # Golden few-shot examples (NEET quality)
│       │   ├── validator.py          # AST static analysis + runtime smoke test
│       │   └── reviewer.py          # Groq-powered auto-fix for validation errors
│       ├── core/config.py           # Settings (Groq keys, AWS, LLM params)
│       ├── main.py                  # FastAPI app entry
│       └── __init__.py
├── .env.example                     # Groq + AWS config template
├── Dockerfile                       # Production container (python:3.11-slim + ffmpeg)
├── README.md                        # Project documentation
├── requirements.txt                 # Python dependencies
├── bedrock_ping_test.py             # Groq key + AWS service connectivity check
├── scripts/
│   ├── start.sh                     # Server startup (validates keys first)
│   └── deploy_aws.sh               # ECR build + ECS deploy
├── output/
│   ├── manim/                       # Generated Manim scripts
│   └── videos/                      # Rendered MP4 files
└── frontend/                        # Dashboard UI
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

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.10+
- Manim Community Edition (with ffmpeg and sox)
- AWS Account with Bedrock access (Claude 3 Sonnet)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Configuration
- Copy `.env.example` to `.env` and add your AWS Bedrock credentials.

### 4. Launch Backend
```powershell
# Windows PowerShell
.\run-local.ps1
```
- Open browser at: [http://localhost:8000](http://localhost:8000)

---

## 🤖 LLM Integration: AWS Bedrock
- All LLM tasks use Amazon Bedrock (Claude 3 Sonnet recommended)
- Configure region and model in `.env`

---

## 🎥 Rendering Videos (Manim)
- Render scripts in `output/manim/` using Manim CLI
- See README for quality flags and rendering options

---

## 🔧 Troubleshooting
| Issue | Solution |
|-------|----------|
| NameError, ImportError | Validator auto-fixes most issues. Re-run generation. |
| Video too short | Increase `duration_seconds` |
| Text overflow | Title max 25 chars, captions auto-wrapped |
| Render fails on Windows | Use WSL for production renders |

---

## 📚 Further Reading
- See UPDATED_ARCHITECTURE.md for detailed design
- See requirements.md and design.md for hackathon alignment and technical requirements

---

## License
MIT
