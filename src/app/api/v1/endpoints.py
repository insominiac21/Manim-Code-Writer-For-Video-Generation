# API endpoints for MentorBoxAI (migrated from backend_local.py)
from fastapi import APIRouter

router = APIRouter()

from fastapi import HTTPException
from datetime import datetime
from typing import Optional

from src.app.services.pipeline import jobs, run_pipeline
from src.app.models.job import GenerateRequest, JobResponse, StatusResponse

# Health check endpoint
@router.get("/health")
def health():
	return {"status": "ok", "version": "4.0.0-production", "timestamp": datetime.now().isoformat()}

# Generate job endpoint
@router.post("/api/generate", response_model=JobResponse)
def create_job(request: GenerateRequest):
	import re
	from datetime import datetime
	from pathlib import Path
	import json
	import os

	# Create readable job ID: topic_timestamp
	safe_concept = re.sub(r'[^a-zA-Z0-9\s]', '', request.concept)
	safe_concept = safe_concept.lower().replace(' ', '_')[:30]
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	job_id = f"{safe_concept}_{timestamp}"

	# Initialize job status
	jobs[job_id] = {
		"job_id": job_id,
		"status": "processing",
		"progress": 10,
		"current_step": "understanding",
		"video_url": None,
		"error": None,
		"plan": None,
		"manim_code": None,
		"understanding": None,
		"concept": request.concept,
		"created_at": datetime.now().isoformat()
	}

	try:
		# Run pipeline
		result = run_pipeline(request)

		# Save files (output and manim dirs must exist)
		BASE_DIR = Path(os.getenv("BASE_DIR", Path(__file__).resolve().parents[4]))
		OUTPUT_DIR = BASE_DIR / "output"
		MANIM_DIR = OUTPUT_DIR / "manim"
		plan_file = OUTPUT_DIR / f"{job_id}_plan.json"
		understanding_file = OUTPUT_DIR / f"{job_id}_understanding.json"
		manim_file = MANIM_DIR / f"{job_id}.py"

		with open(plan_file, "w", encoding='utf-8') as f:
			json.dump(result["plan"], f, indent=2)
		with open(understanding_file, "w", encoding='utf-8') as f:
			json.dump(result["understanding"], f, indent=2)
		with open(manim_file, "w", encoding='utf-8') as f:
			f.write(result["manim_code"])

		# Update job status
		jobs[job_id].update({
			"status": "rendering" if request.auto_render else "done",
			"progress": 70 if request.auto_render else 100,
			"current_step": "rendering" if request.auto_render else "completed",
			"plan": result["plan"],
			"manim_code": result["manim_code"],
			"understanding": result["understanding"]
		})

		# Auto-render if enabled (stub)
		video_url = None
		if request.auto_render:
			# video_url = render_video(job_id, manim_file)
			video_url = None

		jobs[job_id].update({
			"status": "done",
			"progress": 100,
			"current_step": "completed",
			"video_url": video_url
		})
	except Exception as e:
		import traceback
		traceback.print_exc()
		jobs[job_id].update({
			"status": "failed",
			"progress": 0,
			"current_step": None,
			"error": str(e)
		})

	return JobResponse(
		job_id=job_id,
		status=jobs[job_id]["status"],
		estimated_time_seconds=30 if request.auto_render else 15
	)

# Status endpoint
@router.get("/api/status/{job_id}", response_model=StatusResponse)
def get_status(job_id: str):
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
