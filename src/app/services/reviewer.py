"""
MentorBoxAI - Automated Code Reviewer/Fixer
Uses Groq LLM (llama-3.3-70b-versatile) to automatically fix validation errors
in generated Manim code. Replaces OpenAI/OpenRouter dependency from root version.
"""

import re
from typing import Optional
from src.app.services.groq_client import call_groq


# Specialized prompt for code fixing - very strict, code-only output
REVIEWER_SYSTEM_PROMPT = """You are a specialized Python CODE FIXER for Manim animations.

YOUR ONLY JOB: Fix the provided Python code based on the error message.

STRICT RULES:
1. Output ONLY valid Python code - NO markdown, NO explanations, NO prose
2. Keep the same general structure and intent of the original code
3. REQUIRED IMPORTS at the top:
   from manim import *
   import random
   import numpy as np
   import textwrap
4. Class MUST be named `GeneratedScene` and inherit from `ColorfulScene` (NOT Scene)
5. Must have a `construct(self)` method
6. NO imports of: os, sys, subprocess, eval, exec, open, etc.
7. Fix the specific error mentioned while preserving the animation logic
8. Ensure all Manim objects are properly created before being animated
9. Use proper positioning: .to_edge(), .next_to(), .move_to()
10. End with self.wait(2)
11. STRICTLY NO LATEX: Do not use MathTex, Tex, or Matrix. Use Text() objects only.
12. NO helper functions with self outside methods.

═══════════════════════════════════════════════════════════════════════════════
BANNED ANIMATIONS (CAUSE NameError - DO NOT USE):
═══════════════════════════════════════════════════════════════════════════════
- ZoomIn, ZoomOut, Zoom → Use GrowFromCenter() or FadeIn() instead
- SlideIn, SlideOut → Use FadeIn(shift=direction) or FadeOut(shift=direction)
- PopIn, PopOut → Use GrowFromCenter() or ShrinkToCenter()
- Emerge, Expand, Collapse → Use GrowFromCenter(), ShrinkToCenter()
- Morph → Use Transform() or ReplacementTransform()
- WiggleOutThenIn → Use Wiggle() instead
- ShowCreation → Use Create() instead (ShowCreation is DEPRECATED)
- FadeInFrom → Use FadeIn(shift=direction)
- GrowFromEdge → Use GrowFromCenter() or GrowFromPoint()

═══════════════════════════════════════════════════════════════════════════════
VALID MANIM ANIMATIONS (USE THESE):
═══════════════════════════════════════════════════════════════════════════════
- FadeIn, FadeOut, Write, Create, DrawBorderThenFill, Uncreate
- GrowFromCenter, ShrinkToCenter, GrowFromPoint, GrowArrow
- Transform, ReplacementTransform, MoveToTarget, TransformFromCopy
- Rotate, ScaleInPlace, Circumscribe, Indicate, Flash, Wiggle
- LaggedStart, AnimationGroup, Succession

═══════════════════════════════════════════════════════════════════════════════
COMMON FIXES:
═══════════════════════════════════════════════════════════════════════════════
- Missing imports → Add `from manim import *`, `import random`, `import numpy as np`, `import textwrap`
- Undefined objects → Define before use
- Wrong method names → Use correct Manim API
- Overlapping elements → Add proper positioning
- Missing construct() → Add the method
- Syntax errors → Fix Python syntax
- NameError: 'random' → Add `import random` at top
- NameError: 'np' → Add `import numpy as np` at top
- NameError: 'WiggleOutThenIn' → Replace with Wiggle()
- NameError: 'ZoomIn' → Replace with GrowFromCenter()
- NameError: 'textwrap' → Add `import textwrap` at top

OUTPUT: Only the complete, fixed Python source code. Nothing else."""


REVIEWER_USER_TEMPLATE = """ORIGINAL CODE:
```python
{code}
```

ERROR MESSAGE:
{error}

Fix the code to resolve this error. Output ONLY the fixed Python code."""


def review_and_fix(source: str, error_message: str) -> Optional[str]:
    """
    Use Groq LLM to automatically fix code based on validation error.

    Args:
        source: The original Python source code
        error_message: The error from validation

    Returns:
        Fixed Python source code, or None if fix failed
    """
    prompt = REVIEWER_USER_TEMPLATE.replace("{code}", source).replace("{error}", error_message)

    try:
        result = call_groq(
            prompt=prompt,
            system_prompt=REVIEWER_SYSTEM_PROMPT,
            max_tokens=4000,
            temperature=0.01
        )

        if not result:
            return None

        # Extract code if wrapped in markdown
        if "```python" in result:
            match = re.search(r"```python\n(.*?)```", result, re.DOTALL)
            if match:
                return match.group(1).strip()
        elif "```" in result:
            match = re.search(r"```\n?(.*?)```", result, re.DOTALL)
            if match:
                return match.group(1).strip()

        # If no markdown, assume entire response is code
        # But verify it looks like Python
        if "class GeneratedScene" in result and "def construct" in result:
            return result.strip()

        # Try to extract just the Python part
        lines = result.split('\n')
        code_lines = []
        in_code = False
        for line in lines:
            if line.strip().startswith("from manim") or line.strip().startswith("class "):
                in_code = True
            if in_code:
                code_lines.append(line)

        if code_lines:
            return '\n'.join(code_lines).strip()

        return result.strip()

    except Exception as e:
        print(f"[Reviewer] Error calling Groq LLM: {e}")
        return None


def enhance_code_quality(source: str) -> str:
    """
    Use Groq LLM to enhance code quality without fixing specific errors.
    Improves: positioning, comments, structure, educational content.

    Args:
        source: Valid Python source code

    Returns:
        Enhanced Python source code
    """
    enhance_prompt = f"""Improve this Manim code for better quality:

```python
{source}
```

IMPROVEMENTS TO MAKE:
1. Add clear scene section comments (# Scene 1: Title)
2. Ensure proper positioning (no overlapping elements)
3. Add educational explanation text (Text objects explaining concepts)
4. Use proper spacing with buff parameter
5. Clean transitions between scenes (FadeOut before new content)
6. Use meaningful variable names
7. Ensure animations have appropriate durations

OUTPUT: Only the improved Python code. Keep the same structure and intent."""

    try:
        result = call_groq(
            prompt=enhance_prompt,
            system_prompt="You are a Python code improver. Output ONLY valid Python code.",
            max_tokens=4000,
            temperature=0.01
        )

        if not result:
            return source

        # Extract code from markdown if present
        if "```python" in result:
            match = re.search(r"```python\n(.*?)```", result, re.DOTALL)
            if match:
                return match.group(1).strip()
        elif "```" in result:
            match = re.search(r"```\n?(.*?)```", result, re.DOTALL)
            if match:
                return match.group(1).strip()

        return result.strip()

    except Exception as e:
        print(f"[Enhancer] Error: {e}")
        return source  # Return original if enhancement fails
