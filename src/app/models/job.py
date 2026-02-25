from pydantic import BaseModel
from typing import Optional, Any

class GenerateRequest(BaseModel):
    concept: str
    goal: Optional[str] = None
    duration_seconds: int = 35
    max_scenes: int = 4
    fast_mode: Optional[bool] = False
    auto_render: Optional[bool] = False

class JobResponse(BaseModel):
    job_id: str
    status: str
    estimated_time_seconds: int

class StatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    current_step: Optional[str]
    video_url: Optional[str]
    error: Optional[str]
    plan: Optional[Any]
    manim_code: Optional[str]
    understanding: Optional[Any]
