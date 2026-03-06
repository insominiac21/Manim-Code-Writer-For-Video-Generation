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
from typing import Any, Dict

# Fix Windows Unicode encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()

# Groq LLM client with automatic key rotation
from src.app.services.groq_client import call_groq

def call_generator(prompt: str, expect_json: bool = True, system_prompt: str = None) -> str:
    """
    Call Groq LLM (llama-3.3-70b-versatile) with automatic key rotation.
    Used for: understanding, planning, code generation.
    """
    sys_prompt = system_prompt or (
        "You are an expert educational content creator and Manim animation developer. "
        "Always respond with valid JSON when asked for structured output."
    )
    max_tokens = int(os.getenv("LLM_GENERATOR_MAX_TOKENS", "4096"))
    temperature = float(os.getenv("LLM_GENERATOR_TEMPERATURE", "0.01"))
    content = call_groq(prompt, system_prompt=sys_prompt, max_tokens=max_tokens, temperature=temperature)
    print(f"[DEBUG] Groq LLM Response (first 500 chars): {str(content)[:500] if content else 'EMPTY'}")
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
    """Robust JSON parsing with multiple fallback strategies to handle LLM artifacts."""
    if not text:
        return {}

    # Clean up common markdown block issues
    text = text.strip()
    if text.startswith("```"):
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            text = text[start:end+1]

    # Try 1: Normal parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try 2: Non-strict parse (allows control characters like newlines in strings)
    try:
        return json.loads(text, strict=False)
    except json.JSONDecodeError:
        pass

    # Try 3: Remove problematic control characters manually
    cleaned = "".join(c if ord(c) >= 32 or c in "\n\r\t" else " " for c in text)
    try:
        return json.loads(cleaned, strict=False)
    except Exception:
        try:
            start = cleaned.find('{')
            end = cleaned.rfind('}')
            if start != -1 and end != -1:
                return json.loads(cleaned[start:end+1], strict=False)
        except Exception:
            pass

    # Also try: strip markdown code fences from LLM output
    if "```json" in text or "```" in text:
        match = re.search(r'```(?:json)?\s*\n(.*?)\n```', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except Exception:
                pass

    print(f"[JSON Error] Failed all parsing attempts for: {text[:100]}")
    return {"error": "JSON parse failed", "raw_content": text[:100]}


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
    """
    Layer 4: Generate production-ready Manim code.
    Uses manim_templates first (fastest), then LLM with few-shot examples.
    """
    if not goal:
        goal = f"Educational visualization of {concept}"

    # Try pre-built templates first (most reliable)
    try:
        from src.app.services.manim_templates import get_template_for_concept
        template_code = get_template_for_concept(concept)
        if template_code:
            print(f"[Layer 4] Using pre-built template for: {concept}")
            return template_code
    except (ImportError, Exception) as e:
        print(f"[Layer 4] Template error: {e}, falling back to LLM")

    # Get relevant few-shot example
    try:
        from .few_shot_examples import get_few_shot_for_topic
        few_shot = get_few_shot_for_topic(concept)
        print(f"[Layer 4] Using few-shot example for: {concept}")
    except (ImportError, Exception):
        few_shot = None
        print("[Layer 4] Few-shot examples not available")

    from .prompts import LAYER4_PROMPT, CODEGEN_SYSTEM_PROMPT

    # Truncate few-shot to fit context window
    few_shot_truncated = (few_shot[:3500] + "\n# [truncated]...") if few_shot and len(few_shot) > 3500 else (few_shot or "")

    prompt = LAYER4_PROMPT.format(
        plan=json.dumps(plan, indent=2),
        concept=concept,
        goal=goal,
        few_shot=few_shot_truncated
    )

    print(f"[Layer 4] Generating with Groq LLM (few-shot)...")
    result = call_generator(prompt, expect_json=False, system_prompt=CODEGEN_SYSTEM_PROMPT)

    # Extract code from markdown if present
    if result and "```python" in result:
        match = re.search(r"```python\n(.*?)```", result, re.DOTALL)
        if match:
            code = match.group(1).strip()
        else:
            code = result.strip()
    elif result and "```" in result:
        match = re.search(r"```\n(.*?)```", result, re.DOTALL)
        code = match.group(1).strip() if match else result.strip()
    else:
        code = (result or "").strip()

    # Force correct class inheritance
    if "class GeneratedScene(Scene):" in code:
        print("[Layer 4] Auto-fixing: Scene -> ColorfulScene")
        code = code.replace("class GeneratedScene(Scene):", "class GeneratedScene(ColorfulScene):")

    print("[Layer 4] Code generation complete")
    return code


def layer5_refine_code(code: str) -> str:
    """Layer 5: Refine code for quality issues and fix bounds."""
    from .prompts import LAYER5_REFINE

    # Pre-process: fix self.wait(0) -> self.wait(1)
    wait_zero_count = code.count("self.wait(0)")
    if wait_zero_count > 0:
        print(f"[Layer 5] Auto-fixing {wait_zero_count} self.wait(0) -> self.wait(1)")
        code = code.replace("self.wait(0)", "self.wait(1)")

    # Pre-process: fix unterminated string literals (LLM sometimes breaks at 80-col wrap)
    # Remove any lines that are just a lone closing quote or mismatched fragment
    lines = code.split('\n')
    fixed_lines = []
    for line in lines:
        # Drop lines that are purely a bare triple-quote outside a docstring context
        stripped = line.strip()
        if stripped in ("'''", '"""') and not fixed_lines:
            continue  # skip stray leading quotes
        fixed_lines.append(line)
    code = '\n'.join(fixed_lines)

    # Pre-process: clamp excessive wait times
    code = re.sub(r'self\.wait\((\d+)\)', lambda m: f'self.wait({min(int(m.group(1)), 5)})', code)

    # Pre-process: fix out-of-bounds shifts
    code = code.replace('.shift(UP * 3)', '.to_edge(UP)')
    code = code.replace('.shift(DOWN * 3)', '.to_edge(DOWN)')
    code = code.replace('.shift(UP * 4)', '.shift(UP * 2.5)')
    code = code.replace('.shift(DOWN * 3.5)', '.shift(DOWN * 2)')

    # Strip hallucinated template classes if LLM injected them
    if "class ColorfulScene" in code:
        print("[Layer 5] Stripping hallucinated ColorfulScene class from output")
        code = re.sub(r'class Colors:.*?(?=class)', '', code, flags=re.DOTALL)
        code = re.sub(r'class ColorfulScene\(Scene\):.*?(?=class GeneratedScene)', '', code, flags=re.DOTALL)

    # Run LLM refinement
    prompt = LAYER5_REFINE.format(code=code)
    result = call_generator(prompt, expect_json=False)

    # Extract code from markdown if present
    refined_code = result or code
    if "```python" in refined_code:
        match = re.search(r"```python\n(.*?)```", refined_code, re.DOTALL)
        if match:
            refined_code = match.group(1).strip()
    elif "```" in refined_code:
        match = re.search(r"```\n?(.*?)```", refined_code, re.DOTALL)
        if match:
            refined_code = match.group(1).strip()

    # Ensure ColorfulScene inheritance
    if "class GeneratedScene(Scene)" in refined_code:
        refined_code = refined_code.replace("class GeneratedScene(Scene)", "class GeneratedScene(ColorfulScene)")

    # Final: fix any remaining wait(0)
    refined_code = refined_code.replace("self.wait(0)", "self.wait(1)")

    # ── INJECT IMPORT PREAMBLE ────────────────────────────────────
    # The generated file must import ColorfulScene at the top so it runs standalone.
    # We use a direct import rather than embedding MASTER_TEMPLATE_HEADER (which
    # contains literal \n inside strings that break Python syntax when written to disk).
    refined_code = _inject_preamble(refined_code)

    return refined_code if refined_code else code


def validate_and_fix_code(code: str, max_attempts: int = 3, concept: str = "") -> tuple:
    """
    Industry-grade validation pipeline with automatic fix loop.
    Uses AST-based static validation + runtime smoke test + Groq reviewer for fixes.
    """
    try:
        from .validator import auto_fix_common_issues, static_validate, runtime_smoke_test
        from .reviewer import review_and_fix
        validator_available = True
    except ImportError as e:
        print(f"[Validator] Warning: validator/reviewer not available: {e}")
        validator_available = False

    metrics = {
        "static_passes": 0,
        "static_fails": 0,
        "runtime_passes": 0,
        "runtime_fails": 0,
        "fix_attempts": 0
    }

    current_code = code

    if not validator_available:
        # Fallback: basic class inheritance check only
        if "class GeneratedScene(Scene)" in current_code:
            current_code = current_code.replace("class GeneratedScene(Scene)", "class GeneratedScene(ColorfulScene)")
        return current_code, None, 0, metrics

    # AUTO-FIX: Pre-emptively fix common LLM hallucinations before any validation
    print("[Validator] Running auto-fix for common LLM hallucinations...")
    current_code = auto_fix_common_issues(current_code)

    # CONCEPT VALIDATION: Ensure code actually covers the requested topic
    if concept:
        concept_check = check_concept_match(current_code, concept)
        if not concept_check["matched"]:
            print(f"[Validator] CONCEPT MISMATCH: {concept_check['reason']}")
            from .reviewer import review_and_fix
            fix_msg = (f"CRITICAL: The generated code explains '{concept_check['detected_topic']}' "
                       f"but should explain '{concept}'. Rewrite to cover '{concept}' instead.")
            fixed = review_and_fix(current_code, fix_msg)
            if fixed:
                current_code = fixed
                metrics["fix_attempts"] += 1

    # CRITICAL INHERITANCE CHECK
    if "class GeneratedScene" in current_code and "class GeneratedScene(ColorfulScene)" not in current_code:
        print("[Validator] Auto-fixing: GeneratedScene inheritance -> ColorfulScene")
        current_code = re.sub(r'class GeneratedScene\([^)]+\)', 'class GeneratedScene(ColorfulScene)', current_code)
        metrics["fix_attempts"] += 1

    for attempt in range(max_attempts):
        print(f"[Validator] Attempt {attempt + 1}/{max_attempts}")

        # Step 1: Static validation (AST check)
        static_ok, static_msg = static_validate(current_code)

        if not static_ok:
            metrics["static_fails"] += 1
            print(f"[Validator] Static check failed: {static_msg[:120]}")
            metrics["fix_attempts"] += 1
            fixed = review_and_fix(current_code, static_msg)
            if fixed:
                current_code = fixed
            continue

        metrics["static_passes"] += 1
        print("[Validator] Static check passed")

        # Step 2: Runtime smoke test
        runtime_ok, runtime_msg = runtime_smoke_test(current_code, timeout_seconds=15)

        if not runtime_ok:
            metrics["runtime_fails"] += 1
            print(f"[Validator] Runtime test failed: {runtime_msg[:120]}")
            metrics["fix_attempts"] += 1
            fixed = review_and_fix(current_code, runtime_msg)
            if fixed:
                current_code = fixed
            continue

        metrics["runtime_passes"] += 1
        print("[Validator] Runtime test passed - validation complete!")
        return current_code, True, attempt + 1, metrics

    print(f"[Validator] Max attempts ({max_attempts}) reached")
    return current_code, False, max_attempts, metrics


def check_concept_match(code: str, concept: str) -> dict:
    """
    Validate that generated code actually explains the requested concept.
    Ported from backend_local.py. Checks keyword density + title match.
    """
    concept_lower = concept.lower()
    code_lower = code.lower()

    # Extract title from show_title() call
    title_match = re.search(r'show_title\("([^"]+)"\)', code)
    title = title_match.group(1).lower() if title_match else ""

    concept_keywords: dict = {
        "gravitational force": ["gravity", "gravitational", "force", "newton", "mass", "acceleration"],
        "gravity": ["gravity", "gravitational", "force", "newton", "mass", "acceleration"],
        "newton's laws": ["newton", "law", "inertia", "force", "mass", "acceleration"],
        "mitosis": ["mitosis", "cell", "division", "chromosome", "spindle"],
        "meiosis": ["meiosis", "gamete", "haploid", "diploid", "crossover"],
        "photosynthesis": ["photosynthesis", "light", "chlorophyll", "glucose", "atp"],
        "dna": ["dna", "replication", "nucleotide", "helicase", "strand"],
        "cellular respiration": ["respiration", "atp", "glucose", "oxygen", "mitochondria"],
        "immune": ["immune", "antibody", "virus", "bacteria", "antigen"],
        "mendel": ["mendel", "allele", "dominant", "recessive", "punnett", "ratio"],
    }

    # Find expected keywords for concept
    expected_keywords = []
    for key, kws in concept_keywords.items():
        if key in concept_lower:
            expected_keywords = kws
            break
    if not expected_keywords:
        expected_keywords = [w for w in concept_lower.split() if len(w) > 3]

    found_keywords = [kw for kw in expected_keywords if kw in code_lower]
    missing_keywords = [kw for kw in expected_keywords if kw not in code_lower]
    match_ratio = len(found_keywords) / len(expected_keywords) if expected_keywords else 1.0

    # Title mismatch detection
    title_mismatch = False
    if title:
        if "mitosis" in title and "meiosis" in concept_lower:
            title_mismatch = True
        elif "meiosis" in title and "mitosis" in concept_lower and "meiosis" not in concept_lower:
            title_mismatch = True

    matched = match_ratio >= 0.4 and not title_mismatch
    reason = ""
    if not matched:
        if title_mismatch:
            reason = f"Title '{title}' doesn't match requested concept '{concept}'"
        else:
            reason = f"Low concept match ({int(match_ratio*100)}%): missing {missing_keywords[:3]}"

    return {
        "matched": matched,
        "reason": reason,
        "detected_topic": title or "Unknown",
        "keywords_found": found_keywords,
        "keywords_missing": missing_keywords,
        "match_ratio": match_ratio,
    }


def _inject_preamble(code: str) -> str:
    """
    Prepend a lightweight import preamble so the generated .py file is self-contained.

    Instead of embedding the full MASTER_TEMPLATE_HEADER string (which contains
    literal newlines inside string literals that break syntax when written to disk),
    we inject a simple import that loads Colors, ColorfulScene, and all helpers
    from manim_templates.py.  manim_templates.py must be on the Python path when
    the file is rendered (set via PYTHONPATH in the render subprocess).
    """
    PREAMBLE = (
        "from manim import *\n"
        "import random\nimport numpy as np\nimport textwrap\n"
        "import sys, os as _os\n"
        "# Allow manim_templates to be found relative to this file\n"
        "_mt_dir = _os.path.dirname(_os.path.abspath(__file__))\n"
        "if _mt_dir not in sys.path:\n"
        "    sys.path.insert(0, _mt_dir)\n"
        "# Fallback: try the repo src/app/services directory\n"
        "for _p in [_os.path.join(_mt_dir, '..', '..', '..', 'src', 'app', 'services'),\n"
        "           _os.path.join(_mt_dir, '..', 'services')]:\n"
        "    _p = _os.path.normpath(_p)\n"
        "    if _os.path.isdir(_p) and _p not in sys.path:\n"
        "        sys.path.insert(0, _p)\n"
        "from manim_templates import Colors, ColorfulScene\n"
        "# Re-export common color aliases\n"
        "CYAN=Colors.CYAN; HOT_PINK=Colors.HOT_PINK; BRIGHT_YELLOW=Colors.BRIGHT_YELLOW\n"
        "NEON_GREEN=Colors.NEON_GREEN; ORANGE=Colors.ORANGE; PURPLE=Colors.PURPLE\n"
        "GOLD=Colors.GOLD; WHITE=Colors.WHITE; YELLOW=Colors.YELLOW; RED=Colors.RED\n"
        "GREEN=Colors.GREEN; BLUE=Colors.BLUE; TEAL=Colors.TEAL; PINK=Colors.HOT_PINK\n"
        "GRAY=Colors.GRAY; BLACK=Colors.BLACK; LT_GRAY=Colors.LT_GRAY\n"
    )

    # If the code embeds MASTER_TEMPLATE_HEADER (pre-built templates), strip it.
    # MASTER_TEMPLATE_HEADER always defines class ColorfulScene(Scene) inline,
    # which contains split('\\n') stored as literal newlines — broken when saved.
    # Strategy: keep only the `class GeneratedScene(...)` and later; discard earlier.
    if "class ColorfulScene" in code:
        # Find the start of GeneratedScene class (our actual content to keep)
        gen_match = re.search(r'^class GeneratedScene', code, re.MULTILINE)
        if gen_match:
            code = code[gen_match.start():]
            print("[Pipeline] Stripped MASTER_TEMPLATE_HEADER; keeping GeneratedScene class only")

    # Strip bare imports the LLM added (preamble already has them)
    code = re.sub(r'^from manim import \*\s*\n?', '', code, flags=re.MULTILINE)
    code = re.sub(r'^import random\s*\n?', '', code, flags=re.MULTILINE)
    code = re.sub(r'^import numpy as np\s*\n?', '', code, flags=re.MULTILINE)
    code = re.sub(r'^import textwrap\s*\n?', '', code, flags=re.MULTILINE)
    code = re.sub(r'^from manim_templates import.*\n?', '', code, flags=re.MULTILINE)
    code = code.strip()
    code = PREAMBLE + "\n" + code
    print("[Pipeline] Import preamble injected — file uses manim_templates import")
    return code


def _find_and_copy_video(job_id: str) -> Optional[str]:
    """Find generated video file and copy to serving location."""
    video_search = list((VIDEO_DIR / job_id).rglob("*.mp4"))
    if video_search:
        video_path = video_search[0]
        final_path = VIDEO_DIR / f"{job_id}.mp4"
        shutil.copy(str(video_path), str(final_path))
        print(f"[Render] Success: {final_path}")
        return f"/videos/{job_id}.mp4"
    return None


def _resolve_manim_bin() -> str:
    """Resolve the manim executable: prefer venv, then PATH."""
    # Check venv relative to this file: ../../../../venv/bin/manim (EC2 layout)
    candidates = [
        Path(sys.executable).parent / "manim",          # same venv as running python
        Path("/home/ubuntu/app/venv/bin/manim"),         # EC2 hardcoded fallback
        Path("manim"),                                   # plain PATH
    ]
    for c in candidates:
        if shutil.which(str(c)):
            return str(c)
    return "manim"  # last resort


def _resolve_python_bin() -> str:
    """Return the current Python executable path."""
    return sys.executable or "python3"


def _try_render_direct(job_id: str, manim_file: Path) -> Optional[str]:
    """Try rendering using direct manim command."""
    try:
        services_dir = str(Path(__file__).resolve().parent)
        env = os.environ.copy()
        env["PYTHONPATH"] = services_dir + os.pathsep + env.get("PYTHONPATH", "")
        manim_bin = _resolve_manim_bin()
        print(f"[Render-Direct] Using manim={manim_bin}")
        result = subprocess.run(
            [manim_bin, "-qm", str(manim_file), "GeneratedScene",
             "--media_dir", str(VIDEO_DIR / job_id), "--disable_caching"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
            env=env
        )
        if result.returncode == 0:
            return _find_and_copy_video(job_id)
        print(f"[Render-Direct] Failed (rc={result.returncode}): {result.stderr[:400]}")
        return None
    except FileNotFoundError:
        print("[Render-Direct] manim not in PATH")
        return None
    except subprocess.TimeoutExpired:
        print("[Render-Direct] Timeout")
        return None
    except Exception as e:
        print(f"[Render-Direct] Error: {e}")
        return None


def _try_render_python_module(job_id: str, manim_file: Path) -> Optional[str]:
    """Try rendering using python -m manim (uses same venv as server)."""
    try:
        services_dir = str(Path(__file__).resolve().parent)
        env = os.environ.copy()
        env["PYTHONPATH"] = services_dir + os.pathsep + env.get("PYTHONPATH", "")
        python_bin = _resolve_python_bin()
        print(f"[Render-Python] Using python={python_bin}")
        result = subprocess.run(
            [python_bin, "-m", "manim", "-qm", str(manim_file), "GeneratedScene",
             "--media_dir", str(VIDEO_DIR / job_id), "--disable_caching"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
            env=env
        )
        if result.returncode == 0:
            return _find_and_copy_video(job_id)
        print(f"[Render-Python] Failed (rc={result.returncode}): {result.stderr[:400]}")
        return None
    except Exception as e:
        print(f"[Render-Python] Error: {e}")
        return None


def _try_render_docker(job_id: str, manim_file: Path) -> Optional[str]:
    """Try rendering using Docker (manimcommunity/manim)."""
    try:
        docker_check = subprocess.run(["docker", "--version"], capture_output=True)
        if docker_check.returncode != 0:
            print("[Render-Docker] Docker not available")
            return None
        manim_dir = manim_file.parent.absolute()
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-v", f"{manim_dir}:/manim",
             "-v", f"{VIDEO_DIR.absolute()}:/media",
             "manimcommunity/manim",
             "manim", "-qm", f"/manim/{manim_file.name}", "GeneratedScene",
             "--media_dir", f"/media/{job_id}"],
            capture_output=True, text=True, timeout=180
        )
        if result.returncode == 0:
            return _find_and_copy_video(job_id)
        print(f"[Render-Docker] Failed: {result.stderr[:200]}")
        return None
    except FileNotFoundError:
        print("[Render-Docker] Docker not found")
        return None
    except Exception as e:
        print(f"[Render-Docker] Error: {e}")
        return None


def render_video(job_id: str, manim_file: Path) -> Optional[str]:
    """
    Render Manim code to video.
    Tries multiple methods: direct manim, python -m manim, docker.
    """
    print(f"[Render] Starting render for {job_id}...")

    video_url = _try_render_direct(job_id, manim_file)
    if video_url:
        return video_url

    video_url = _try_render_python_module(job_id, manim_file)
    if video_url:
        return video_url

    video_url = _try_render_docker(job_id, manim_file)
    if video_url:
        return video_url

    print("[Render] All render methods failed. Video not generated.")
    return None

def _format_code(code: str) -> str:
    """Apply code formatting (optional, if black is available).
    NOTE: Disabled — black can split long string literals across lines causing SyntaxErrors
    in the generated Manim scripts (e.g. font='Arial' gets broken onto a new line).
    """
    # Do NOT run black on generated Manim code — it breaks long string literals
    # that appear in MASTER_TEMPLATE_HEADER and the generated GeneratedScene class.
    return code


def run_pipeline(req) -> Dict[str, Any]:
    """
    Run the production-grade pipeline with validation and auto-fix.

    Pipeline FULL MODE (6 layers):
    1. Understanding - Analyze the concept
    2. Planning - Create scene-by-scene plan
    3. Verification - Check accuracy
    4. Code Generation - Generate Manim code with few-shot
    5. Quality Refinement - LLM-based fixes
    6. Validation & Auto-Fix - AST check + runtime smoke test + auto-fix loop

    Pipeline FAST MODE (4 layers - skips 3 and 5):
    1. Understanding, 2. Planning, 4. Code Generation, 6. Validation
    """
    fast_mode = getattr(req, 'fast_mode', False)
    if fast_mode:
        print("[Pipeline] FAST MODE enabled - skipping layers 3 and 5")

    # Layer 1: Understanding
    print(f"[Layer 1] Understanding: {req.concept}")
    understanding = layer1_understand(req.concept, req.goal)

    # Layer 2: Planning
    print("[Layer 2] Planning video...")
    plan = layer2_plan(understanding, req.duration_seconds, req.max_scenes)

    # Layer 3: Verification (SKIP in fast mode)
    verification = {"approved": True, "final_plan": None}
    if not fast_mode:
        print("[Layer 3] Verifying accuracy...")
        verification = layer3_verify(req.concept, req.goal, plan)
        if not verification.get("approved", True) and verification.get("final_plan"):
            final_plan = verification["final_plan"]
        else:
            final_plan = plan
    else:
        print("[Layer 3] SKIPPED (fast mode)")
        final_plan = plan

    # Layer 4: Code Generation
    print("[Layer 4] Generating Manim code...")
    raw_code = layer4_generate_code(final_plan, req.concept, req.goal)

    # Layer 5: Quality Refinement (SKIP in fast mode)
    if not fast_mode:
        print("[Layer 5] Refining code quality...")
        refined_code = layer5_refine_code(raw_code)
    else:
        print("[Layer 5] SKIPPED (fast mode)")
        # Apply basic fixes without LLM call
        refined_code = raw_code
        if "class GeneratedScene(Scene)" in refined_code:
            refined_code = refined_code.replace("class GeneratedScene(Scene)", "class GeneratedScene(ColorfulScene)")
        # Fast mode: still inject preamble so file is self-contained
        refined_code = _inject_preamble(refined_code)

    # Layer 6: Production Validation + Auto-Fix
    print("[Layer 6] Validating and fixing code...")
    try:
        max_attempts = 2 if fast_mode else 3
        validated_code, validation_passed, attempts, metrics = validate_and_fix_code(
            refined_code, max_attempts=max_attempts, concept=req.concept
        )
        print(f"[Layer 6] Validation complete - Passed: {validation_passed}, Attempts: {attempts}")
        print(f"[Layer 6] Metrics: {metrics}")
        final_code = validated_code
    except Exception as e:
        print(f"[Layer 6] Validation error: {e} - using refined code as-is")
        final_code = refined_code
        validation_passed = None
        metrics = {}

    # Final safety: ensure preamble is in place
    # (Layer 6 fix loops might have rewritten the top of the file)
    if "class ColorfulScene" not in final_code and "from src.app.services.manim_templates" not in final_code:
        print("[Pipeline] Final safety: re-injecting preamble")
        final_code = _inject_preamble(final_code)

    # Optional: Format code
    try:
        final_code = _format_code(final_code)
    except Exception:
        pass

    return {
        "understanding": understanding,
        "plan": final_plan,
        "manim_code": final_code,
        "approved": verification.get("approved", True),
        "validation_passed": validation_passed,
        "validation_metrics": metrics if metrics else None
    }
