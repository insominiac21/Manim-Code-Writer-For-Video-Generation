
# MentorBoxAI: Updated System Architecture & Component Purpose

---

## 🎨 Architecture Overview

MentorBoxAI is a cinematic, modular FastAPI backend that transforms any topic into a professional educational animation using a 6-layer AI pipeline. The new structure is optimized for reliability, scalability, and developer productivity, with AWS Bedrock LLM integration and Manim CE rendering.

---

## 🧠 The 6-Layer Pipeline (Visual)

| Layer | Stage | Purpose |
| :--- | :--- | :--- |
| **1** | **Understanding** | Deconstructs topic into scientific key facts and a cinematic script. |
| **2** | **Storyboarding** | Maps the script into a multi-scene visual plan (Scene layout, objects, timings). |
| **3** | **Verification** | Validates the plan against technical requirements (No-LaTeX, Screen Bounds, Cognitive Load). |
| **4** | **Code Generation** | Translates the storyboard into Manim Python code using Few-Shot Template logic. |
| **5** | **Refinement** | Injects high-end visual treatments (Glowing pulses, particle backgrounds, smooth transitions). |
| **6** | **Validation & Fix** | Performs Static AST checking and a Runtime Smoke Test. If it fails, an LLM Reviewer auto-patches the code. |

---

## 🔗 Data Flow Pipeline

```
User Input (Topic, Duration)
         │
         ▼
┌─────────────────────────────┐
│  Layer 1: Understanding     │──→ understanding.json
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Layer 2: Storyboarding     │──→ plan.json
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Layer 3: Verification      │──→ verified_plan.json
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Layer 4: Code Generation   │──→ scene.py (draft)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Layer 5: Refinement        │──→ scene.py (enhanced)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Layer 6: Validation & Fix  │──→ scene.py (final)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Manim Render               │──→ video.mp4
└─────────────────────────────┘
```

---

## 🏗️ Component Map & Roles

- **src/app/services/pipeline.py**: Orchestrates all pipeline layers, manages job flow, and integrates LLM calls.
- **src/app/services/prompts.py**: Prompt engineering templates for each pipeline layer.
- **src/app/services/few_shot_examples.py**: Golden few-shot examples for consistent Manim code quality.
- **src/app/api/v1/endpoints.py**: FastAPI endpoints for job creation, status, and health checks.
- **src/app/models/job.py**: Pydantic models for request/response validation.
- **output/manim/**: Generated Manim scripts for each job.
- **output/videos/**: Rendered MP4 files, ready for preview/download.
- **frontend/**: Dashboard UI for job queuing, preview, and download.

---

## ✨ Design Principles & Achievements

- **Zero-LaTeX Architecture**: Custom ColorfulScene uses Unicode/Text rendering with advanced styling, making it crash-proof in cloud/local environments.
- **Screen-Safe Layouts**: Text-wrapping caption engine and boundary-checking logic prevent overlapping UI elements.
- **Procedural Visuals**: All visuals are built using Manim primitives for high-resolution scalability.
- **Self-Healing Logic**: Layer 6 detects errors and invokes LLM Reviewer to auto-patch code before user sees it.
- **Information Density**: Each core scene contains 2-3 labeled objects, a transformation/process animation, a concept caption, and at least one exam-relevant fact.
- **NEET/JEE Focused**: Prompts optimized for Indian competitive exam content with exam tips and key ratios.
- **Developer-Friendly**: Modular, testable, and scalable backend structure for rapid extension and CI/CD.

---

## 🏆 Hackathon Alignment & Workflow

- Meets requirements for learning acceleration, reliability, clarity, and scalability.
- User submits topic and parameters via dashboard.
- Backend processes through 6-layer pipeline, each layer adding structure, checks, and enhancements.
- Manim renders animation, video is previewed/downloaded.
- Validator and reviewer ensure crash-free output.

---

## 📚 Further Reading
- See requirements.md and design.md for full hackathon alignment and technical requirements.
- See README.md for quickstart and troubleshooting.

---

## License
MIT
