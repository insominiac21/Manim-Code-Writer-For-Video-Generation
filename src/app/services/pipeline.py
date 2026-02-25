# Pipeline service and job management for MentorBoxAI (migrated from backend_local.py)
import os
import json
import re
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

# In-memory job storage
default_jobs = {}
jobs = default_jobs

# Output and media directories (update as needed)
BASE_DIR = Path(os.getenv("BASE_DIR", Path(__file__).resolve().parents[4]))
OUTPUT_DIR = BASE_DIR / "output"
MANIM_DIR = OUTPUT_DIR / "manim"
VIDEO_DIR = OUTPUT_DIR / "videos"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MANIM_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

# Import pipeline layers from their future locations (to be refactored)
# from src.app.services.llm_layers import layer1_understand, layer2_plan, layer3_verify, layer4_generate_code, layer5_refine_code, validate_and_fix_code, render_video


# --- LLM Pipeline Layer Functions (migrated from backend_local.py) ---

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import boto3
from typing import Any, Dict

# Fix Windows Unicode encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()

# AWS Bedrock LLM call (Claude 3 Sonnet)
def call_bedrock(prompt: str, max_tokens: int = 2048, temperature: float = 0.01, model_id: str = None) -> str:
    bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
    model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
    body = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json"
    )
    result = json.loads(response["body"].read())
    return result.get("completion", result)

# Unified LLM call for Bedrock
def call_generator(prompt: str, expect_json: bool = True, system_prompt: str = None) -> str:
    """
    Call the main generator model (AWS Bedrock Claude 3 Sonnet).
    Used for: understanding, planning, code generation.
    """
    if system_prompt:
        prompt = system_prompt + "\n" + prompt
    max_tokens = int(os.getenv("LLM_GENERATOR_MAX_TOKENS", "4096"))
    temperature = float(os.getenv("LLM_GENERATOR_TEMPERATURE", "0.01"))
    model_id = os.getenv("LLM_GENERATOR_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0")
    content = call_bedrock(prompt, max_tokens=max_tokens, temperature=temperature, model_id=model_id)
    print(f"[DEBUG] Bedrock LLM Response (first 500 chars): {str(content)[:500] if content else 'EMPTY'}")
    return content


def layer1_understand(concept: str, goal: str) -> dict:
    """Layer 1: Understand concept"""
    from .prompts import LAYER1_PROMPT
    prompt = LAYER1_PROMPT.format(concept=concept, goal=goal)
    return safe_json_loads(call_generator(prompt, expect_json=True))


def layer2_plan(understanding: dict, duration: int, max_scenes: int) -> dict:
    """Layer 2: Create video plan"""
    from .prompts import LAYER2_PROMPT
    estimated_per_scene = duration // max_scenes if max_scenes > 0 else duration
    prompt = LAYER2_PROMPT.format(
        understanding=json.dumps(understanding, indent=2),
        duration=duration,
        max_scenes=max_scenes,
        estimated_per_scene=estimated_per_scene
    )
    return safe_json_loads(call_generator(prompt, expect_json=True))
def safe_json_loads(text: str) -> dict:
    """Robust JSON parsing with fallback strategies."""
    if not text:
        return {}
    text = text.strip()
    if text.startswith("```"):
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            text = text[start:end+1]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def layer3_verify(concept: str, goal: str, plan: dict) -> dict:
    """Layer 3: Verify accuracy"""
    from .prompts import LAYER3_PROMPT
    prompt = LAYER3_PROMPT.format(
        concept=concept,
        goal=goal,
        plan=json.dumps(plan, indent=2)
    )
    return safe_json_loads(call_generator(prompt, expect_json=True))


def layer4_generate_code(plan: dict, concept: str, goal: str = "") -> str:
    """Layer 4: Generate production-ready Manim code."""
    from .prompts import LAYER4_PROMPT
    from .few_shot_examples import get_few_shot_for_topic
    few_shot = get_few_shot_for_topic(concept)
    prompt = LAYER4_PROMPT.format(
        plan=json.dumps(plan, indent=2),
        concept=concept,
        goal=goal,
        few_shot=few_shot if few_shot else ""
    )
    return call_generator(prompt, expect_json=False)


def layer5_refine_code(code: str) -> str:
    """Layer 5: Refine code for quality issues and fix bounds"""
    from .prompts import LAYER5_PROMPT
    prompt = LAYER5_PROMPT.format(code=code)
    return call_generator(prompt, expect_json=False)


def validate_and_fix_code(code: str, max_attempts: int = 3, concept: str = "") -> tuple:
    """Industry-grade validation pipeline with automatic fix loop."""
    from .prompts import VALIDATION_PROMPT
    attempts = 0
    validation_passed = False
    metrics = {}
    validated_code = code
    while attempts < max_attempts and not validation_passed:
        prompt = VALIDATION_PROMPT.format(code=validated_code, concept=concept)
        result = safe_json_loads(call_generator(prompt, expect_json=True))
        validation_passed = result.get("validation_passed", False)
        metrics = result.get("metrics", {})
        if not validation_passed:
            validated_code = result.get("fixed_code", validated_code)
        attempts += 1
    return validated_code, validation_passed, attempts, metrics


def render_video(job_id: str, manim_file: Path) -> Optional[str]:
    from ...backend_local import render_video as orig_render_video
    return orig_render_video(job_id, manim_file)

def run_pipeline(req) -> Dict[str, Any]:
    """
    Run the production-grade pipeline with validation and auto-fix.
    """
    fast_mode = getattr(req, 'fast_mode', False)
    if fast_mode:
        print(f"[Pipeline] FAST MODE enabled - skipping layers 3 and 5")
    print(f"[Layer 1] Understanding: {req.concept}")
    understanding = layer1_understand(req.concept, req.goal)
    print(f"[Layer 2] Planning video...")
    plan = layer2_plan(understanding, req.duration_seconds, req.max_scenes)
    if not fast_mode:
        print(f"[Layer 3] Verifying accuracy...")
        verification = layer3_verify(req.concept, req.goal, plan)
        final_plan = verification.get("final_plan", plan) if not verification.get("approved", True) else plan
    else:
        print(f"[Layer 3] SKIPPED (fast mode)")
        final_plan = plan
    print(f"[Layer 4] Generating Manim code...")
    raw_code = layer4_generate_code(final_plan, req.concept, req.goal)
    if not fast_mode:
        print(f"[Layer 5] Refining code quality...")
        refined_code = layer5_refine_code(raw_code)
    else:
        print(f"[Layer 5] SKIPPED (fast mode)")
        refined_code = raw_code
    print(f"[Layer 6] Validating and fixing code...")
    validated_code, validation_passed, attempts, metrics = validate_and_fix_code(refined_code, max_attempts=1 if fast_mode else 3, concept=req.concept)
    return {
        "understanding": understanding,
        "plan": final_plan,
        "manim_code": validated_code,
        "approved": True,
        "validation_passed": validation_passed,
        "validation_metrics": metrics if metrics else None
    }
