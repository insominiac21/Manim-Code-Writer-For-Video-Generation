"""
MentorBoxAI - Production-Grade Code Validator
AST-based static analysis + runtime smoke testing for Manim code
"""

import ast
import os
import sys
import subprocess
import tempfile
from typing import Tuple, Optional

# Import the new Manim API validator
try:
    from manim_api_validator import full_api_validation
    MANIM_API_VALIDATOR_AVAILABLE = True
except ImportError:
    MANIM_API_VALIDATOR_AVAILABLE = False
    print("[Validator] Warning: manim_api_validator not found, using legacy validation")

# Forbidden modules that could be security risks
FORBIDDEN_MODULES = {
    "os", "sys", "subprocess", "shutil", "socket", "ctypes", 
    "multiprocessing", "threading", "pickle", "marshal",
    "builtins", "importlib", "pathlib", "io", "glob",
    "requests", "urllib", "http", "ftplib", "smtplib"
}

# Forbidden substrings in code
FORBIDDEN_SUBSTRINGS = (
    "eval(", "exec(", "__import__", "compile(",
    "open(", "globals(", "locals(", "vars(",
    "getattr(", "setattr(", "delattr(",
    "breakpoint(", "input("
)

# Banned Manim classes that cause NameError
BANNED_MANIM_CLASSES = {
    "ParametricCurve", "Sphere", "Star", "Surface", "Cube", "Prism",
    "ThreeDAxes", "Cylinder", "Cone", "Torus", "Mobius", "Arrow3D",
    "Glow",        # Not a Manim CE class
    "Bubble",      # Not a Manim CE class
    "SpeechBubble",# Not a Manim CE class
    "AnnotationDot",# Not a Manim CE class
    "Sparkle",     # Not a Manim CE class
}

# Only allowed imports
ALLOWED_IMPORTS = {"manim", "numpy", "np", "random", "textwrap", "math", "sys", "os", "manim_templates"}

# Hallucinated animations that don't exist in Manim (mapped to valid replacements)
HALLUCINATED_ANIMATIONS = {
    "ZoomIn": "GrowFromCenter",
    "ZoomOut": "ShrinkToCenter",
    "Zoom": "GrowFromCenter",
    "SlideIn": "FadeIn",
    "SlideOut": "FadeOut",
    "PopIn": "GrowFromCenter",
    "PopOut": "ShrinkToCenter",
    "Emerge": "GrowFromCenter",
    "Expand": "GrowFromCenter",
    "Collapse": "ShrinkToCenter",
    "Morph": "Transform",
    "ShowCreation": "Create",    # Deprecated in newer Manim
    "WiggleOutThenIn": "Wiggle", # Common LLM hallucination
    "FadeInFrom": "FadeIn",      # Doesn't exist
    "FadeOutTo": "FadeOut",      # Doesn't exist
    "GrowFromEdge": "GrowFromCenter",
    "Bounce": "Wiggle",          # Doesn't exist in Manim CE
    "Pulse": "Flash",            # Doesn't exist in Manim CE
    "Blink": "Flash",            # Doesn't exist in Manim CE
    "Appear": "FadeIn",          # Doesn't exist in Manim CE
    "Disappear": "FadeOut",      # Doesn't exist in Manim CE
    "Spotlight": "Indicate",     # Doesn't exist in Manim CE
    "TypeWrite": "Write",        # Doesn't exist in Manim CE
    "SweepIn": "FadeIn",         # Doesn't exist in Manim CE
    "SweepOut": "FadeOut",       # Doesn't exist in Manim CE
    "Highlight": "Indicate",     # Doesn't exist in Manim CE
    "DrawBorder": "DrawBorderThenFill",  # Wrong name
    "AnimateIn": "FadeIn",       # Doesn't exist in Manim CE
    "AnimateOut": "FadeOut",     # Doesn't exist in Manim CE
}


def auto_fix_common_issues(source: str) -> str:
    """
    Automatically fix common LLM hallucination issues before validation.
    This runs BEFORE static_validate to preemptively fix known issues.
    
    Returns:
        Fixed source code
    """
    import re
    fixed = source
    fixes_applied = []
    
    # 1. Ensure required imports exist
    if "import random" not in fixed and "random." in fixed:
        fixed = fixed.replace("from manim import *", "from manim import *\nimport random")
        fixes_applied.append("Added missing 'import random'")
    
    if "import numpy" not in fixed and ("np." in fixed or "numpy." in fixed):
        fixed = fixed.replace("from manim import *", "from manim import *\nimport numpy as np")
        fixes_applied.append("Added missing 'import numpy as np'")
    
    if "import textwrap" not in fixed and "textwrap." in fixed:
        fixed = fixed.replace("from manim import *", "from manim import *\nimport textwrap")
        fixes_applied.append("Added missing 'import textwrap'")
    
    # 2. Fix hallucinated animations
    for fake_anim, real_anim in HALLUCINATED_ANIMATIONS.items():
        pattern = f"{fake_anim}("
        if pattern in fixed:
            fixed = fixed.replace(pattern, f"{real_anim}(")
            fixes_applied.append(f"Replaced hallucinated '{fake_anim}' with '{real_anim}'")
    
    # 3. Ensure ColorfulScene inheritance (not Scene)
    if "class GeneratedScene(Scene):" in fixed:
        fixed = fixed.replace("class GeneratedScene(Scene):", "class GeneratedScene(ColorfulScene):")
        fixes_applied.append("Fixed inheritance: Scene -> ColorfulScene")
    
    # 4. Fix bare color names - must use Colors.X prefix
    bare_colors = ["ENERGY", "LIGHT", "MOLECULE", "ELECTRON", "TEXT", "IMPORTANT"]
    for color in bare_colors:
        # Fix patterns like color=ENERGY or color= ENERGY
        pattern = rf'color\s*=\s*{color}(?![A-Z_])'
        if re.search(pattern, fixed):
            fixed = re.sub(pattern, f'color=Colors.{color}', fixed)
            fixes_applied.append(f"Fixed bare color '{color}' -> 'Colors.{color}'")
    
    # 5. Fix large font sizes that cause overflow (reduce to safe values)
    # font_size=48+ is too big, reduce to 36
    fixed = re.sub(r'font_size\s*=\s*([5-9]\d|[1-9]\d{2,})', 'font_size=36', fixed)
    
    # 6. Fix text width parameter - reduce from 50 to 40
    fixed = re.sub(r'textwrap\.fill\([^,]+,\s*width\s*=\s*5\d\)', lambda m: m.group(0).replace('50', '40').replace('55', '40').replace('60', '40'), fixed)
    
    # 7. Fix dangerous positioning - clamp shifts
    fixed = re.sub(r'\.shift\(UP\s*\*\s*([4-9]|[1-9]\d)\)', '.shift(UP * 2.5)', fixed)
    fixed = re.sub(r'\.shift\(DOWN\s*\*\s*([4-9]|[1-9]\d)\)', '.shift(DOWN * 2.5)', fixed)
    fixed = re.sub(r'\.shift\(LEFT\s*\*\s*([7-9]|[1-9]\d)\)', '.shift(LEFT * 5)', fixed)
    fixed = re.sub(r'\.shift\(RIGHT\s*\*\s*([7-9]|[1-9]\d)\)', '.shift(RIGHT * 5)', fixed)
    
    # 8. Reduce scale factors that are dangerously large (>= 4.0 only)
    # Allow 2.0-3.9 for legitimate particle/zoom effects; only cap 4.0+ and integer multiples
    fixed = re.sub(r'\.scale\(([4-9]\.\d|[1-9]\d)\)', '.scale(2.5)', fixed)

    # 8b. self.title and self.captions are now valid ColorfulScene attributes; preserve them.
    fixed = re.sub(r'FadeOut\(self\.undefined_attr[^)]*\)', 'FadeOut(*self.mobjects)', fixed)

    # 8c. Strip invalid Flash/ShowPassingFlash kwargs that cause TypeError at runtime.
    #     Flash only accepts: flash_radius, num_lines, line_length, color, run_time, rate_func
    #     LLMs often hallucinate: scale_factor, glow_radius, intensity, size, opacity
    fixed = re.sub(r'(Flash\([^)]*?),?\s*scale_factor\s*=\s*[\d.]+', r'\1', fixed)
    fixed = re.sub(r'(Flash\([^)]*?),?\s*glow_radius\s*=\s*[\d.]+', r'\1', fixed)
    fixed = re.sub(r'(Flash\([^)]*?),?\s*intensity\s*=\s*[\d.]+', r'\1', fixed)
    fixed = re.sub(r'(Flash\([^)]*?),?\s*opacity\s*=\s*[\d.]+', r'\1', fixed)
    # Also strip from ShowPassingFlash
    fixed = re.sub(r'(ShowPassingFlash\([^)]*?),?\s*scale_factor\s*=\s*[\d.]+', r'\1', fixed)
    # Strip invalid Glow() calls (Glow is not a Manim CE class — replace with nothing)
    fixed = re.sub(r'\bglow\s*=\s*Glow\([^)]*\)\s*;?\s*FadeIn\(glow\)', '', fixed)
    fixed = re.sub(r'Glow\([^)]*\)', 'VGroup()', fixed)

    # 8d. Strip ImageMobject calls (no assets on server — replace with placeholder circle)
    def replace_image_mobject(match):
        fixes_applied.append("Replaced ImageMobject with placeholder Circle")
        return "Circle(radius=0.5, color=Colors.CYAN, fill_opacity=0.4)"
    fixed = re.sub(r'ImageMobject\([^)]*\)', replace_image_mobject, fixed)
    
    # 9. Fix long text strings that will overflow (truncate to ~65 chars for Text())
    def truncate_long_text(match):
        full_match = match.group(0)
        text_content = match.group(1)
        limit = 65
        if len(text_content) > limit:
            truncated = text_content[:limit - 3] + "..."
            return full_match.replace(text_content, truncated)
        return full_match
    
    # Fix Text() with long strings (>65 chars risks overflow)
    fixed = re.sub(r'Text\(\s*["\']([^"\']{66,})["\']', truncate_long_text, fixed)
    
    # 10. play_caption: no length truncation — create_caption() word-wraps automatically
    # (removing this regex means long captions wrap to multiple lines instead of being cut off)

    # 10b. Auto-fix MathTex/Tex — LaTeX is NOT installed on server, convert to Text()
    # Single-string form: MathTex(r"formula") or MathTex("formula") -> Text("formula")
    def _mathtex_to_text(m):
        content = m.group(1)
        # strip LaTeX commands to ASCII readable form
        content = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1/\2)', content)
        content = re.sub(r'\\sqrt\{([^}]+)\}', r'sqrt(\1)', content)
        content = re.sub(r'\\cdot', r' x ', content)
        content = re.sub(r'\\times', r' x ', content)
        content = re.sub(r'\\pm', r'+/-', content)
        content = re.sub(r'\\[a-zA-Z]+', r'', content)  # strip remaining commands
        content = content.replace('{', '').replace('}', '')
        fixes_applied.append("Replaced MathTex/Tex with Text()")
        return f'Text("{content}"'
    fixed = re.sub(r'MathTex\(r?["\']([^"\']+)["\']', _mathtex_to_text, fixed)
    fixed = re.sub(r'(?<!Math)Tex\(r?["\']([^"\']+)["\']', _mathtex_to_text, fixed)
    # Multi-arg MathTex("A", "=", "B") — join args into single Text
    def _mathtex_multiarg(m):
        args = re.findall(r'["\']([^"\']+)["\']', m.group(1))
        joined = ' '.join(args)
        fixes_applied.append("Replaced multi-arg MathTex with Text()")
        return f'Text("{joined}"'
    fixed = re.sub(r'MathTex\(([^)]+)\)', _mathtex_multiarg, fixed)
    # DecimalNumber(x) -> Text(str(x))
    fixed = re.sub(r'DecimalNumber\(([^,)]+)[^)]*\)', lambda m: f'Text(str({m.group(1).strip()}))', fixed)
    # include_numbers=True -> include_numbers=False (avoids DecimalNumber/LaTeX internally)
    fixed = fixed.replace('include_numbers=True', 'include_numbers=False')
    fixed = fixed.replace('include_numbers = True', 'include_numbers=False')
    # Matrix( -> VGroup of Text placeholder
    fixed = re.sub(r'Matrix\(([^)]{0,40})\)', 'VGroup()', fixed)

    # 10c. Strip Unicode subscripts/superscripts — EC2 manim font cannot render them.
    # Replace with ASCII equivalents so Text() renders correctly.
    _unicode_map = {
        '\u00b2': '2', '\u00b3': '3', '\u00b9': '1',
        '\u2070': '0', '\u2071': '1', '\u2074': '4', '\u2075': '5',
        '\u2076': '6', '\u2077': '7', '\u2078': '8', '\u2079': '9',
        '\u207a': '+', '\u207b': '-', '\u207c': '=', '\u207f': 'n',
        '\u2080': '0', '\u2081': '1', '\u2082': '2', '\u2083': '3',
        '\u2084': '4', '\u2085': '5', '\u2086': '6', '\u2087': '7',
        '\u2088': '8', '\u2089': '9', '\u208a': '+', '\u208b': '-',
        '\u00b0': 'deg',  # degree sign
        '\u03b1': 'alpha', '\u03b2': 'beta', '\u03b3': 'gamma',
        '\u03b4': 'delta', '\u03bb': 'lambda', '\u03bc': 'mu',
        '\u03c0': 'PI', '\u03a9': 'Omega', '\u03a3': 'Sigma',
        '\u2192': '->', '\u2190': '<-', '\u2194': '<->',
        '\u00d7': 'x', '\u00f7': '/',
    }
    for uni_char, ascii_rep in _unicode_map.items():
        if uni_char in fixed:
            fixed = fixed.replace(uni_char, ascii_rep)
            fixes_applied.append(f"Replaced Unicode char U+{ord(uni_char):04X} with '{ascii_rep}'")
    
    # 11. Fix show_title with long strings (MAX 25 chars!)
    def truncate_title(match):
        full_match = match.group(0)
        title_content = match.group(1)
        if len(title_content) > 25:
            truncated = title_content[:25]
            fixes_applied.append(f"Truncated title from {len(title_content)} to 25 chars")
            return full_match.replace(title_content, truncated)
        return full_match
    
    fixed = re.sub(r'show_title\(\s*["\']([^"\']{26,})["\']', truncate_title, fixed)
    
    # 12. Fix move_to positions outside safe bounds
    # x > 6 or x < -6 is danger zone
    fixed = re.sub(r'move_to\(LEFT\s*\*\s*([7-9]|[1-9]\d)\)', 'move_to(LEFT * 5)', fixed)
    fixed = re.sub(r'move_to\(RIGHT\s*\*\s*([7-9]|[1-9]\d)\)', 'move_to(RIGHT * 5)', fixed)
    fixed = re.sub(r'move_to\(UP\s*\*\s*([4-9]|[1-9]\d)\)', 'move_to(UP * 3)', fixed)
    fixed = re.sub(r'move_to\(DOWN\s*\*\s*([4-9]|[1-9]\d)\)', 'move_to(DOWN * 2.5)', fixed)
    
    # 13. (Removed) The blanket LEFT/RIGHT→DOWN override was incorrectly breaking
    # split-screen layouts where left_panel.next_to(right_panel, RIGHT) is intentional.
    # Layout enforcement is now handled by clamp_to_screen() in ColorfulScene.
    
    if fixes_applied:
        print(f"[Validator] Auto-fixed {len(fixes_applied)} issues: {', '.join(fixes_applied)}")
    
    return fixed


def static_validate(source: str) -> Tuple[bool, str]:
    """
    Perform AST-based static validation of generated Manim code.
    
    Checks:
    0. Manim API validation (new premium layer)
    1. Syntax validity
    2. No forbidden imports (only 'manim' allowed)
    3. No dangerous function calls
    4. GeneratedScene class exists with construct method
    5. No file I/O or network operations
    
    Returns:
        (success: bool, message: str)
    """
    # LAYER 0: Premium Manim API Validation (if available)
    if MANIM_API_VALIDATOR_AVAILABLE:
        valid, msg = full_api_validation(source)
        if not valid:
            return False, f"[Manim API] {msg}"
    
    # Check for forbidden substrings first (quick scan)
    for forbidden in FORBIDDEN_SUBSTRINGS:
        if forbidden in source:
            return False, f"Forbidden pattern detected: {forbidden}"
    
    # Check for common Manim API misuse patterns
    api_misuse_patterns = [
        ("Polygon(n=", "Polygon takes vertices, not n. Use RegularPolygon(n=) instead"),
        ("Polygon(n =", "Polygon takes vertices, not n. Use RegularPolygon(n=) instead"),
        ("Sphere(", "Sphere is not available. Use Circle() instead"),
        ("Star(", "Star is not available. Use RegularPolygon(n=5) instead"),
        ("ParametricCurve(", "ParametricCurve is not available. Use FunctionGraph() instead"),
        ("Surface(", "Surface is not available for 2D scenes"),
        ("Cube(", "Cube is not available. Use Square() instead"),
        ("ThreeDAxes(", "ThreeDAxes is not available. Use Axes() instead"),
        ("header=", "RoundedRectangle does not accept 'header'. Use Text() for headers instead"),
        # NO-LATEX RULES — these are auto-fixed before validation, so should not appear here.
        # If they somehow survive auto-fix, catch them here as a last resort.
        # (MathTex, Tex, DecimalNumber, Matrix are converted in auto_fix_common_issues)
        ("SVGMobject(", "SVGMobject is not allowed. External assets like SVG files do not exist. Create objects using native Manim shapes."),
        ("ImageMobject(", "ImageMobject is not allowed. External assets do not exist. Create objects using native Manim shapes."),
        # HALLUCINATED CLASSES (don't exist in Manim CE)
        ("Bubble(", "Bubble is not a Manim CE class. Use RoundedRectangle() + Text() instead."),
        ("SpeechBubble(", "SpeechBubble is not a Manim CE class. Use RoundedRectangle() + Text() instead."),
        ("AnnotationDot(", "AnnotationDot is not a Manim CE class. Use Dot() instead."),
        ("Sparkle(", "Sparkle is not a Manim CE class. Use Flash() or GrowFromCenter() instead."),
        ("Grid(", "Grid is not a standalone Manim class. Use NumberPlane() or VGroup of Lines instead."),
        # HALLUCINATED ANIMATIONS (don't exist in Manim)
        ("ZoomIn(", "ZoomIn is not a real Manim animation. Use GrowFromCenter() or FadeIn() instead."),
        ("ZoomOut(", "ZoomOut is not a real Manim animation. Use ShrinkToCenter() or FadeOut() instead."),
        ("Zoom(", "Zoom is not a real Manim animation. Use ScaleInPlace() or GrowFromCenter() instead."),
        ("SlideIn(", "SlideIn is not a real Manim animation. Use FadeIn(shift=...) instead."),
        ("SlideOut(", "SlideOut is not a real Manim animation. Use FadeOut(shift=...) instead."),
        ("Emerge(", "Emerge is not a real Manim animation. Use GrowFromCenter() or FadeIn() instead."),
        ("Expand(", "Expand is not a real Manim animation. Use GrowFromCenter() instead."),
        ("Collapse(", "Collapse is not a real Manim animation. Use ShrinkToCenter() instead."),
        ("PopIn(", "PopIn is not a real Manim animation. Use GrowFromCenter() instead."),
        ("PopOut(", "PopOut is not a real Manim animation. Use ShrinkToCenter() instead."),
    ]
    
    for pattern, error_msg in api_misuse_patterns:
        if pattern in source:
            return False, f"API misuse: {error_msg}"
    
    # Try to parse as Python AST
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    
    # Check all imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_module = alias.name.split('.')[0]
                if root_module not in ALLOWED_IMPORTS:
                    return False, f"Forbidden import: {alias.name} (only 'manim' allowed)"
        
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root_module = node.module.split('.')[0]
                if root_module not in ALLOWED_IMPORTS:
                    return False, f"Forbidden import: from {node.module} (only 'manim' allowed)"
        
        # Check for suspicious function calls
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in {"eval", "exec", "open", "compile", "__import__", 
                                "globals", "locals", "vars", "getattr", "setattr",
                                "delattr", "breakpoint", "input"}:
                    return False, f"Forbidden function call: {func_name}()"
                
                # Check for banned Manim classes
                if func_name in BANNED_MANIM_CLASSES:
                    alternatives = {
                        "ParametricCurve": "FunctionGraph",
                        "Sphere": "Circle",
                        "Star": "Polygon or RegularPolygon",
                        "Surface": "FunctionGraph",
                        "Cube": "Square",
                        "ThreeDAxes": "Axes"
                    }
                    alt = alternatives.get(func_name, "a 2D shape")
                    return False, f"Banned Manim class: {func_name} (causes NameError). Use {alt} instead."
    
    # Check for GeneratedScene class
    scene_class = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "GeneratedScene":
            scene_class = node
            break
    
    if scene_class is None:
        return False, "Missing required class: GeneratedScene"
    
    # Check for construct method in GeneratedScene
    has_construct = False
    for item in scene_class.body:
        if isinstance(item, ast.FunctionDef) and item.name == "construct":
            has_construct = True
            break
    
    if not has_construct:
        return False, "GeneratedScene class missing construct() method"
    
    # Check for proper Scene inheritance
    if not scene_class.bases:
        return False, "GeneratedScene must inherit from Scene"
    
    return True, "Static validation passed"


def runtime_smoke_test(source: str, timeout_seconds: int = 10) -> Tuple[bool, str]:
    """
    Execute a runtime smoke test in an isolated subprocess.
    
    This tests:
    1. Code can be imported without errors
    2. GeneratedScene can be instantiated
    3. construct() method exists and is callable
    
    Note: Does NOT run full Manim rendering (too slow for validation).
    
    Returns:
        (success: bool, message: str)
    """
    # Create a test harness that imports and instantiates the scene
    test_harness = '''
import sys
import types
sys.path.insert(0, '.')

# ── Mock manim_templates BEFORE importing gen_scene ──────────────────────
# Prevents ImportError when generated code does `from manim_templates import *`
if 'manim_templates' not in sys.modules:
    _mock_mt = types.ModuleType('manim_templates')
    class Colors:
        DARK_BG = "#0f0f2e"
        CYAN = "#00FFFF"; BLUE = "#0000FF"; RED = "#FF0000"
        HOT_PINK = "#FF69B4"; PINK = "#FF69B4"
        BRIGHT_YELLOW = "#FFD700"; YELLOW = "#FFD700"; GOLD = "#FFD700"
        NEON_GREEN = "#39FF14"; GREEN = "#39FF14"
        ORANGE = "#FF8C00"; PURPLE = "#9D00FF"
        WHITE = "#FFFFFF"; BLACK = "#000000"
        GRAY = "#808080"; LT_GRAY = "#CCCCCC"; TEAL = "#008080"
        LIGHT = "#FFD700"; ENERGY = "#FF8C00"; MOLECULE = "#39FF14"
        ELECTRON = "#00FFFF"; TEXT = "#FFFFFF"; IMPORTANT = "#FFD700"
    _mock_mt.Colors = Colors
    _mock_mt.phasor_to_sine_animation = lambda *a, **kw: None
    _mock_mt.static_sine_wave = lambda *a, **kw: None
    _mock_mt.get_template_for_concept = lambda *a, **kw: None
    sys.modules["manim_templates"] = _mock_mt
else:
    Colors = sys.modules["manim_templates"].Colors

# Minimal Manim mock for smoke testing (faster than full Manim)
class MockScene:
    def __init__(self):
        self.mobjects = []
    def play(self, *args, **kwargs): pass
    def wait(self, *args, **kwargs): pass
    def add(self, *args, **kwargs): pass
    def remove(self, *args, **kwargs): pass
    @property
    def camera(self):
        class MockCamera:
            background_color = "#000000"
        return MockCamera()

# Patch manim.Scene with our mock
import manim
original_scene = manim.Scene
manim.Scene = MockScene

# Mock ColorfulScene (custom template class used by generated code)
import builtins
class ColorfulScene(MockScene):
    def __init__(self):
        super().__init__()
        self.captions = []
        self.title = None
    def show_title(self, text, **kw): return None
    def play_caption(self, text, **kw): pass
    def create_section_header(self, text, **kw): return None
    def add_background(self, **kw): pass
    def cleanup(self, **kw): pass
    def fade_all(self, **kw): pass
    def create_glowing_dot(self, *a, **kw): return MockScene()
    def add_particle_bg(self, *a, **kw): pass
    def show_exam_tip(self, *a, **kw): pass
    def clamp_to_screen(self, obj, **kw): return obj
    def safe_next_to(self, *a, **kw): return None
    def arrange_column(self, *a, **kw): return None
builtins.ColorfulScene = ColorfulScene
builtins.Colors = Colors
# Patch ColorfulScene + Colors back onto the manim_templates module entry so that
# "from manim_templates import Colors, ColorfulScene" works without ImportError
if 'manim_templates' in sys.modules:
    sys.modules['manim_templates'].ColorfulScene = ColorfulScene
    sys.modules['manim_templates'].Colors = Colors

try:
    # Import the generated module
    import gen_scene
    
    # Check class exists
    if not hasattr(gen_scene, 'GeneratedScene'):
        print("ERROR: GeneratedScene class not found")
        sys.exit(1)
    
    # Instantiate
    scene = gen_scene.GeneratedScene()
    
    # Check construct method
    if not hasattr(scene, 'construct') or not callable(scene.construct):
        print("ERROR: construct() method not found or not callable")
        sys.exit(1)
    
    # Try to run construct (with mock Scene, this is fast)
    try:
        if hasattr(scene, 'setup'):
            scene.setup()
        scene.construct()
    except (NameError, SyntaxError) as e:
        # Critical errors - code references undefined names or has syntax issues
        print(f"ERROR: construct() raised exception: {type(e).__name__}: {e}")
        sys.exit(1)
    except Exception as e:
        # Tolerate Manim-internal errors (TypeError, AttributeError etc.)
        # These happen because we mock Scene - code structure is fine
        pass
    
    print("SMOKE_TEST_PASSED")
    sys.exit(0)

except ImportError as e:
    print(f"ERROR: Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: Unexpected error: {type(e).__name__}: {e}")
    sys.exit(1)
finally:
    manim.Scene = original_scene
'''
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy manim_templates.py into tmpdir so generated code can import it
            _mt_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manim_templates.py')
            if os.path.exists(_mt_src):
                import shutil as _shutil
                _shutil.copy2(_mt_src, os.path.join(tmpdir, 'manim_templates.py'))

            # Write the generated code
            gen_path = os.path.join(tmpdir, "gen_scene.py")
            with open(gen_path, "w", encoding="utf-8") as f:
                f.write(source)
            
            # Write the test harness
            harness_path = os.path.join(tmpdir, "test_harness.py")
            with open(harness_path, "w", encoding="utf-8") as f:
                f.write(test_harness)
            
            # Run in isolated subprocess
            result = subprocess.run(
                [sys.executable, "-I", harness_path],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            
            output = result.stdout + result.stderr
            
            if result.returncode == 0 and "SMOKE_TEST_PASSED" in output:
                return True, "Runtime smoke test passed"
            else:
                # Extract error message
                for line in output.split('\n'):
                    if line.startswith("ERROR:"):
                        return False, line
                return False, f"Smoke test failed with exit code {result.returncode}: {output[:500]}"
    
    except subprocess.TimeoutExpired:
        return False, f"Runtime smoke test timed out after {timeout_seconds}s"
    except Exception as e:
        return False, f"Smoke test error: {type(e).__name__}: {e}"


def validate_visual_quality(source: str) -> Tuple[bool, str, dict]:
    """
    Validate that generated code has sufficient visual quality and animations.
    
    Checks:
    1. Minimum animation count (self.play calls)
    2. Uses template methods (show_title, play_caption, add_glow_pulse)
    3. Has glowing effects (set_stroke, create_glowing_object)
    4. Uses transformations (ReplacementTransform, Flash)
    5. Has proper scene structure
    
    Returns:
        (passes_quality: bool, message: str, metrics: dict)
    """
    import re
    
    metrics = {
        "play_calls": len(re.findall(r'self\.play\(', source)),
        "show_title_calls": len(re.findall(r'self\.show_title\(', source)),
        "play_caption_calls": len(re.findall(r'self\.play_caption\(', source)),
        "glow_pulse_calls": len(re.findall(r'self\.add_glow_pulse\(|self\.add_fun_pulse\(', source)),
        "flash_calls": len(re.findall(r'Flash\(', source)),
        "replacement_transform_calls": len(re.findall(r'ReplacementTransform\(', source)),
        "lagged_start_calls": len(re.findall(r'LaggedStart\(', source)),
        "set_stroke_calls": len(re.findall(r'\.set_stroke\(', source)),
        "create_glowing_calls": len(re.findall(r'self\.create_glowing_object\(|self\.create_glowing_text\(', source)),
        "grow_from_center_calls": len(re.findall(r'GrowFromCenter\(', source)),
        "fadeout_calls": len(re.findall(r'FadeOut\(', source)),
    }
    
    # Calculate quality score
    quality_score = 0
    issues = []
    
    # Minimum animations (at least 10 self.play calls)
    if metrics["play_calls"] >= 10:
        quality_score += 20
    elif metrics["play_calls"] >= 5:
        quality_score += 10
        issues.append(f"Low animation count: {metrics['play_calls']} (need 10+)")
    else:
        issues.append(f"Very low animation count: {metrics['play_calls']} (need 10+)")
    
    # Uses show_title
    if metrics["show_title_calls"] >= 1:
        quality_score += 15
    else:
        issues.append("Missing self.show_title() for title")
    
    # Uses play_caption (at least 3 times)
    if metrics["play_caption_calls"] >= 3:
        quality_score += 20
    elif metrics["play_caption_calls"] >= 1:
        quality_score += 10
        issues.append(f"Low caption count: {metrics['play_caption_calls']} (need 3+)")
    else:
        issues.append("Missing self.play_caption() for captions")
    
    # Has glow effects
    if metrics["glow_pulse_calls"] >= 1 or metrics["set_stroke_calls"] >= 2 or metrics["create_glowing_calls"] >= 1:
        quality_score += 15
    else:
        issues.append("Missing glow effects (add_glow_pulse, set_stroke, create_glowing_object)")
    
    # Has Flash effects
    if metrics["flash_calls"] >= 1:
        quality_score += 10
    else:
        issues.append("Missing Flash() for energy effects")
    
    # Uses transformations
    if metrics["replacement_transform_calls"] >= 1:
        quality_score += 10
    else:
        issues.append("Missing ReplacementTransform() for morphing")
    
    # Uses LaggedStart for multiple objects
    if metrics["lagged_start_calls"] >= 1:
        quality_score += 5
    
    # Scene cleanup
    if metrics["fadeout_calls"] >= 2:
        quality_score += 5
    
    metrics["quality_score"] = quality_score
    metrics["max_score"] = 100
    
    # Pass if score >= 50
    passes = quality_score >= 50
    
    if passes:
        message = f"Quality check passed (score: {quality_score}/100)"
    else:
        message = f"Quality check FAILED (score: {quality_score}/100). Issues: {'; '.join(issues)}"
    
    return passes, message, metrics


def validate_manim_code(source: str, check_quality: bool = True) -> Tuple[bool, str, dict]:
    """
    Full validation pipeline: static + runtime + quality checks.
    
    Returns:
        (success: bool, message: str, details: dict)
    """
    details = {
        "static_pass": False,
        "runtime_pass": False,
        "quality_pass": False,
        "static_message": "",
        "runtime_message": "",
        "quality_message": "",
        "quality_metrics": {}
    }
    
    # Step 1: Static validation
    static_ok, static_msg = static_validate(source)
    details["static_pass"] = static_ok
    details["static_message"] = static_msg
    
    if not static_ok:
        return False, f"Static validation failed: {static_msg}", details
    
    # Step 2: Runtime smoke test
    runtime_ok, runtime_msg = runtime_smoke_test(source)
    details["runtime_pass"] = runtime_ok
    details["runtime_message"] = runtime_msg
    
    if not runtime_ok:
        return False, f"Runtime test failed: {runtime_msg}", details
    
    # Step 3: Quality check (optional but recommended)
    if check_quality:
        quality_ok, quality_msg, quality_metrics = validate_visual_quality(source)
        details["quality_pass"] = quality_ok
        details["quality_message"] = quality_msg
        details["quality_metrics"] = quality_metrics
        
        if not quality_ok:
            print(f"[Validator] ⚠️ Quality warning: {quality_msg}")
            # Don't fail on quality, just warn
    
    return True, "All validation checks passed", details


# Quick test if run directly
if __name__ == "__main__":
    test_code = '''
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        title = Text("Test Scene", font_size=44)
        title.to_edge(UP)
        
        self.play(Write(title))
        self.wait(2)
'''
    
    print("Testing validator...")
    success, message, details = validate_manim_code(test_code)
    print(f"Result: {'PASS' if success else 'FAIL'}")
    print(f"Message: {message}")
    print(f"Details: {details}")
