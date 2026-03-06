
# MentorBoxAI: Design Document

---

## 🎯 Purpose & Vision

MentorBoxAI is an AI-powered backend for generating cinematic educational videos using a 6-layer pipeline, **Groq LLM** (llama-3.3-70b-versatile), and Manim CE. The system is modular, robust, and optimized for hackathon and production use on AWS.

---

## 🧠 Layered Pipeline Overview

| Layer | Stage | Purpose |
| :--- | :--- | :--- |
| **1** | **Understanding** | Deconstructs topic into scientific key facts and a cinematic script |
| **2** | **Storyboarding** | Maps the script into a multi-scene visual plan (Scene layout, objects, timings) |
| **3** | **Verification** | Validates the plan against technical requirements (No-LaTeX, Screen Bounds, Cognitive Load) |
| **4** | **Code Generation** | Translates the storyboard into Manim Python code using Few-Shot Template logic |
| **5** | **Refinement** | Injects high-end visual treatments (Glowing pulses, particle backgrounds, smooth transitions) |
| **6** | **Validation & Fix** | Performs Static AST checking and a Runtime Smoke Test. If it fails, Groq Reviewer auto-patches the code |

---

## 🏗️ Component Roles & Responsibilities

- **src/app/services/groq_client.py**: Groq API client with automatic key rotation across GROQ_API_KEY1/2/3. Retries on 401/403/429.
- **src/app/services/pipeline.py**: Main orchestrator for all 6 pipeline layers, manages job flow, integrates LLM calls, validation, and rendering.
- **src/app/services/prompts.py**: Full prompt engineering templates for all 5 layers + CODEGEN_SYSTEM_PROMPT + VALIDATION_PROMPT. No placeholders.
- **src/app/services/few_shot_examples.py**: 7 golden few-shot examples (Vaccine, Respiration, Fusion, SHM, Mitosis, Quadratic, Epic Biology) with topic-routing function.
- **src/app/services/validator.py**: AST-based static analysis, HALLUCINATED_ANIMATIONS auto-fix, runtime smoke test, visual quality scoring.
- **src/app/services/reviewer.py**: Groq-powered code fixer — given an error message, returns corrected Manim code.
- **src/app/api/v1/endpoints.py**: FastAPI endpoints: POST /api/generate, GET /api/status/{job_id}, GET /health.
- **src/app/models/job.py**: Pydantic models (GenerateRequest, JobResponse, StatusResponse).
- **src/app/core/config.py**: Settings class — Groq keys, AWS region (ap-south-1), LLM params, CORS.
- **bedrock_ping_test.py**: Connectivity test — pings all 3 Groq keys + S3 + DynamoDB + Lambda + STS.
- **scripts/start.sh**: Validates Groq keys before starting uvicorn server.
- **scripts/deploy_aws.sh**: Builds Docker image, pushes to ECR, updates ECS service.

---

## 🔑 LLM Configuration

- **Provider**: Groq (https://api.groq.com/openai/v1/chat/completions)
- **Model**: llama-3.3-70b-versatile
- **Key rotation**: GROQ_API_KEY1 → GROQ_API_KEY2 → GROQ_API_KEY3 (auto-retry on failure)
- **AWS Bedrock**: NOT used (blocked on AISPL accounts without international credit card)
- **AWS services used**: S3 (video storage), DynamoDB (job persistence), Lambda (async triggers)
- **Region**: ap-south-1 (Mumbai)

---

## ✨ Design Principles & Achievements

- **Zero-LaTeX Architecture**: Custom ColorfulScene uses Unicode/Text rendering with advanced styling, making it crash-proof in cloud/local environments.
- **Screen-Safe Layouts**: Text-wrapping caption engine and boundary-checking logic prevent overlapping UI elements.
- **Procedural Visuals**: All visuals are built using Manim primitives for high-resolution scalability.
- **Self-Healing Logic**: Layer 6 detects errors and invokes Groq Reviewer to auto-patch code before user sees it.
- **Information Density**: Each core scene contains 2-3 labeled objects, a transformation/process animation, a concept caption, and at least one exam-relevant fact.
- **NEET/JEE Focused**: Prompts optimized for Indian competitive exam content with exam tips and key ratios.
- **Developer-Friendly**: Modular, testable, and scalable backend structure for rapid extension and CI/CD.

---

## 🏆 Hackathon Alignment & Acceptance Criteria

- Meets requirements for learning acceleration, reliability, clarity, and scalability.
- Self-healing pipeline ensures zero runtime crashes and rapid iteration.
- Information-dense visuals and screen-safe layouts optimize learning outcomes.
- See requirements.md for full acceptance criteria and technical requirements.

---

## 🔄 Workflow Summary

1. User submits topic and parameters via dashboard or API.
2. Backend processes through 6-layer pipeline, each layer adding structure, checks, and enhancements.
3. Manim renders animation, video is previewed/downloaded.
4. Validator and reviewer ensure crash-free output.

---

## 📚 Further Reading
- See UPDATED_ARCHITECTURE.md for system architecture and data flow.
- See requirements.md for technical requirements and hackathon alignment.

---

## License
MIT
