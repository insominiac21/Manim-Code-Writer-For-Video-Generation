# Prompt templates for MentorBoxAI pipeline

LAYER1_PROMPT = """Analyze the concept and goal for educational video generation.
Concept: {concept}
Goal: {goal}
"""

LAYER2_PROMPT = """You are a Video Director planning the VISUAL NARRATIVE for an educational animation.
Script: {understanding}
Duration: {duration}s (USER REQUESTED THIS EXACT DURATION! RESPECT IT!)

======================================================================
DURATION IS SACRED - CALCULATE EXACTLY!
======================================================================

For {duration} seconds, calculate:
- Intro: 5-8 seconds (title + hook + visual teaser)
- Core Content: {duration} - 15 seconds (main teaching with RICH visuals)
- Takeaway: 7-10 seconds (key point + formula/summary)

SUM OF ALL SCENE DURATIONS MUST EQUAL {duration} SECONDS!

Example for 60s video:
- Scene 1 (Intro): 8 sec
- Scene 2 (Core 1): 15 sec
- Scene 3 (Core 2): 15 sec
- Scene 4 (Core 3): 12 sec
- Scene 5 (Takeaway): 10 sec
- TOTAL: 60 sec

======================================================================
INFORMATION DENSITY REQUIREMENTS (CRITICAL!)
======================================================================

EACH CORE SCENE MUST CONTAIN:
1. AT LEAST 2-3 LABELED OBJECTS (diagrams, not just text)
2. A TRANSFORMATION or PROCESS animation
3. A CONCEPT CAPTION that teaches something specific
4. AT LEAST 1 EXAM-RELEVANT FACT (number, ratio, formula)

...existing code...
"""


LAYER3_PROMPT = """Verify this educational video plan.\n\nConcept: {concept}\nGoal: {goal}\n\nPlan:\n{plan}\n\nCheck:\n1. Is content accurate for the requested topic?\n2. Are visuals specific (not generic)?\n3. Does it teach the concept effectively?\n\nReturn JSON:\n{{\n  \"approved\": true/false,\n  \"issues\": [\"any problems\"],\n  \"final_plan\": {{ corrected plan if needed }}\n}}"""

LAYER4_PROMPT = """You are a CINEMATIC Manim animator creating 3Blue1Brown-quality educational videos.\n\n**CONCEPT**: {concept}\n**VIDEO PLAN**: {plan}\n\n======================================================================\nCRITICAL RULES - READ FIRST!\n======================================================================\n\n1. TITLE MAX 25 CHARACTERS!\n   - GOOD: \"Mendel's Laws\" (13 chars)\n   - BAD: \"How Mendel's Laws Explain Inheritance Patterns\"\n\n   title_group = self.show_title(\"Mendel's Laws\")  # MAX 25 chars!\n\n2. RESPECT DURATION FROM PLAN!\n   - Add self.wait() to match planned scene durations\n   - Each scene should have: animation time + wait time = planned duration\n   - Example: 15 sec scene = 8 sec animations + self.wait(7)\n\n3. CONTENT DENSITY - Every scene MUST be INFORMATION RICH:\n   - 2-3 LABELED VISUAL OBJECTS (not just floating text!)\n   - 1 TRANSFORMATION/PROCESS animation (arrows, morphs)\n   - 1 EXAM FACT (number, ratio, formula shown visually)\n   - 1 CAPTION explaining the concept\n\n...existing code...\n"""
