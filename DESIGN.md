
# MentorBoxAI: Design Document

---

## 🎯 Purpose & Vision

MentorBoxAI is an AI-powered backend for generating cinematic educational videos using a 6-layer pipeline, AWS Bedrock LLM, and Manim CE. The new structure is modular, robust, and optimized for hackathon and production use, with a focus on reliability, clarity, and developer productivity.

---

## 🧠 Layered Pipeline Overview

| Layer | Stage | Purpose |
| :--- | :--- | :--- |
| **1** | **Understanding** | Deconstructs topic into scientific key facts and a cinematic script |
| **2** | **Storyboarding** | Maps the script into a multi-scene visual plan (Scene layout, objects, timings) |
| **3** | **Verification** | Validates the plan against technical requirements (No-LaTeX, Screen Bounds, Cognitive Load) |
| **4** | **Code Generation** | Translates the storyboard into Manim Python code using Few-Shot Template logic |
| **5** | **Refinement** | Injects high-end visual treatments (Glowing pulses, particle backgrounds, smooth transitions) |
| **6** | **Validation & Fix** | Performs Static AST checking and a Runtime Smoke Test. If it fails, an LLM Reviewer auto-patches the code |

---

## 🏗️ Component Roles & Responsibilities

- **src/app/services/pipeline.py**: Main orchestrator for all pipeline layers, manages job flow, integrates LLM calls, and handles validation.
- **src/app/services/prompts.py**: Prompt engineering templates for each pipeline layer, optimized for exam content and information density.
- **src/app/services/few_shot_examples.py**: Golden few-shot examples for Manim code generation, ensuring consistent quality and style.
- **src/app/api/v1/endpoints.py**: FastAPI endpoints for job creation, status, and health checks.
- **src/app/models/job.py**: Pydantic models for requests/responses, ensuring robust validation and API clarity.
- **output/manim/**: Generated Manim scripts for each job, ready for rendering.
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
