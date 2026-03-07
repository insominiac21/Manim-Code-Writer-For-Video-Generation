# Main MentorBoxAI endpoints (migrated)
import threading
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional
from src.app.services.pipeline import jobs, run_pipeline, render_video
from src.app.models.job import GenerateRequest, JobResponse, StatusResponse

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "version": "4.0.0-production", "timestamp": datetime.now().isoformat()}


def _run_pipeline_bg(job_id: str, request: GenerateRequest):
    """Background thread: run pipeline then render video, updating jobs dict throughout."""
    import re, json, os, time
    from pathlib import Path
    BASE_DIR = Path(os.getenv("BASE_DIR", Path(__file__).resolve().parents[5]))
    OUTPUT_DIR = BASE_DIR / "output"
    MANIM_DIR = OUTPUT_DIR / "manim"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIM_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # ── LLM pipeline ────────────────────────────────────────────────────
        jobs[job_id].update({"current_step": "understanding", "progress": 10})
        result = run_pipeline(request)

        plan_file = OUTPUT_DIR / f"{job_id}_plan.json"
        understanding_file = OUTPUT_DIR / f"{job_id}_understanding.json"
        manim_file = MANIM_DIR / f"{job_id}.py"

        with open(plan_file, "w", encoding="utf-8") as f:
            json.dump(result["plan"], f, indent=2)
        with open(understanding_file, "w", encoding="utf-8") as f:
            json.dump(result["understanding"], f, indent=2)
        with open(manim_file, "w", encoding="utf-8") as f:
            f.write(result["manim_code"])

        jobs[job_id].update({
            "status": "rendering",
            "progress": 70,
            "current_step": "rendering",
            "plan": result["plan"],
            "manim_code": result["manim_code"],
            "understanding": result["understanding"],
        })

        # ── Render ───────────────────────────────────────────────────────────
        video_url = None
        if request.auto_render:
            try:
                video_url = render_video(job_id, manim_file)
                print(f"[BG] Render result: {video_url}")
                # Append cache-buster so browser never plays a stale cached file
                if video_url:
                    video_url = f"{video_url}?t={int(time.time())}"
            except Exception as render_err:
                print(f"[BG] Render error: {render_err}")

        jobs[job_id].update({
            "status": "done",
            "progress": 100,
            "current_step": "completed",
            "video_url": video_url,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        jobs[job_id].update({
            "status": "failed",
            "progress": 0,
            "current_step": None,
            "error": str(e),
        })


@router.post("/api/generate", response_model=JobResponse)
def create_job(request: GenerateRequest):
    import re
    print(f"[API] POST /api/generate concept='{request.concept}' auto_render={request.auto_render} fast_mode={request.fast_mode}")
    safe_concept = re.sub(r'[^a-zA-Z0-9\s]', '', request.concept)
    safe_concept = safe_concept.lower().replace(' ', '_')[:30]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    job_id = f"{safe_concept}_{timestamp}"

    jobs[job_id] = {
        "job_id": job_id,
        "status": "processing",
        "progress": 5,
        "current_step": "queued",
        "video_url": None,
        "error": None,
        "plan": None,
        "manim_code": None,
        "understanding": None,
        "concept": request.concept,
        "created_at": datetime.now().isoformat(),
    }

    # Start pipeline in background — respond immediately
    t = threading.Thread(target=_run_pipeline_bg, args=(job_id, request), daemon=True)
    t.start()

    return JobResponse(
        job_id=job_id,
        status="processing",
        estimated_time_seconds=120 if request.auto_render else 45,
    )

@router.get("/api/status/{job_id}", response_model=StatusResponse)
def get_status(job_id: str):
    print(f"[API] GET /api/status/{job_id}")
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    job = jobs[job_id]
    return StatusResponse(
        job_id=job["job_id"],
        status=job["status"],
        progress=job["progress"],
        current_step=job["current_step"],
        video_url=job["video_url"],
        error=job["error"],
        plan=job.get("plan"),
        manim_code=job.get("manim_code"),
        understanding=job.get("understanding")
    )
