"""
MentorBoxAI - CINEMATIC Few-Shot Examples for Manim Code Generation
3Blue1Brown-quality Manim code with artistic visuals and engaging animations.
"""

# GOLDEN_EXAMPLE_VACCINE and other examples
GOLDEN_EXAMPLE_VACCINE = '''from manim import *
import numpy as np

class GeneratedScene(ColorfulScene):
    def construct(self):
        # ...existing code...
'''

# Add additional examples and helper functions as needed

def get_few_shot_for_topic(topic: str):
    # Example mapping logic
    if "vaccine" in topic.lower():
        return GOLDEN_EXAMPLE_VACCINE
    # ...add more mappings...
    return None

SHORT_EXAMPLE = GOLDEN_EXAMPLE_VACCINE[:1000]
