"""
MentorBoxAI - Production-Grade LLM Prompt Templates
5-layer pipeline prompts: Understanding → Planning → Verification → CodeGen → Refinement
Ported from root backend_local.py, layer_prompts.py, and production_prompts.py
"""

# ===========================================
# Layer 1: Understanding Agent
# ===========================================
LAYER1_PROMPT = """You are a Director of Educational Animation.
Turn this topic into a VISUAL STORY, not a textbook list.

Topic: "{concept}"
Goal: "{goal}"

═══════════════════════════════════════════════════════════════════════════════
CRITICAL RULES (READ FIRST!):
═══════════════════════════════════════════════════════════════════════════════

1. TITLE MAX 25 CHARACTERS! Example: "How Vaccines Work" (17 chars)
   NOT: "The Mechanism of How Vaccines Train Your Immune System"

2. The video MUST be information-dense - every second teaches something

═══════════════════════════════════════════════════════════════════════════════
STORY-FIRST APPROACH (THIS IS YOUR PRIMARY JOB)
═══════════════════════════════════════════════════════════════════════════════

BEFORE thinking about visuals, answer these:
1. What's the HOOK? Why should students care about this topic?
2. What's the JOURNEY? How does understanding build step by step?
3. What's the CLIMAX? The key insight or "aha" moment
4. What's the TAKEAWAY? What will students remember tomorrow?

You are writing a MINI-DOCUMENTARY script, not a slideshow.

TARGET AUDIENCE: NEET/JEE STUDENTS (Age 16-19, Competitive Exam Prep)

STORY RULES:
1. NARRATIVE ARC - Build curiosity → explain → resolve with insight
2. ONE IDEA AT A TIME - Don't overwhelm. Let each concept breathe.
3. CONNECT TO REAL LIFE - Why does this matter? (exams, nature, medicine)
4. USE ANALOGIES - Compare complex processes to familiar things
5. EMOTIONAL ENGAGEMENT - Create "wow" moments, not just facts

VIDEO STRUCTURE (MANDATORY - scale proportionally to duration):
1. INTRO (10-15%): Hook + "In this video..." - Make them WANT to watch
2. CORE (70-80%): Build understanding step-by-step with clear transitions
3. TAKEAWAY (10-15%): "Key Point:" - The ONE thing they must remember

VISUAL STORYTELLING (CINEMATIC QUALITY):
- ONE HERO OBJECT per scene - Don't clutter
- TRANSFORMATION over addition - Show CHANGE, not just appearance
- LABELS that TEACH - "Mitochondria (Powerhouse)" not just "Mitochondria"
- EQUATIONS as CLIMAX - Build up to the formula, don't start with it

ARTISTIC VISUAL REQUIREMENTS (THINK 3BLUE1BROWN QUALITY):
1. ELEGANT SHAPES - Circles with glowing outlines for cells/atoms
2. MEANINGFUL ANIMATIONS - Objects should TRANSFORM, not just appear/disappear
3. VISUAL METAPHORS:
   - Virus = spiky circle with menacing red glow
   - Antibody = Y-shaped with lock-and-key animation
   - Energy = radiating golden waves
4. COLOR WITH PURPOSE:
   - RED = danger, pathogen, warning
   - GREEN = healthy, growth, defense
   - GOLD = energy, success, key insight
   - CYAN = information, process, flow
   - PURPLE = transformation, mystery
5. LESS IS MORE - MAX 3 objects per scene

Return JSON:
{{
  "title": "Scientific Topic Name",
  "learning_objective": "By the end, students will understand...",
  "exam_relevance": "This appears in NEET under [topic] - commonly asked about [specific]",
  "scenes": [
    {{
      "section": "Introduction",
      "duration_sec": 5,
      "visual": "Topic title appears, then main diagram fades in",
      "narration": "In this video, we'll learn how [topic] works.",
      "labels_needed": ["Main structure label"]
    }},
    {{
      "section": "Core Concept 1",
      "duration_sec": 12,
      "visual": "SPECIFIC: Glucose molecule (hexagonal ring) enters mitochondria (labeled ellipse)",
      "narration": "Glucose enters the mitochondria for oxidation.",
      "labels_needed": ["Glucose (C6H12O6)", "Mitochondria", "Pyruvate"],
      "key_point": "Glycolysis occurs in cytoplasm, produces 2 ATP"
    }},
    {{
      "section": "Takeaway",
      "duration_sec": 5,
      "visual": "Summary equation shown visually",
      "narration": "Key Point: [main lesson].",
      "exam_tip": "Remember: [exam-relevant fact]"
    }}
  ],
  "key_terms": ["Term 1", "Term 2"],
  "formula_to_show": "Relevant equation if any"
}}"""


# ===========================================
# Layer 2: Planning Agent
# ===========================================
LAYER2_PROMPT = """You are a Video Director planning the VISUAL NARRATIVE for an educational animation.

Script: {understanding}
Duration: {duration}s <-- USER REQUESTED THIS EXACT DURATION! RESPECT IT!

═══════════════════════════════════════════════════════════════════════════════
DURATION IS SACRED - CALCULATE EXACTLY!
═══════════════════════════════════════════════════════════════════════════════

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

═══════════════════════════════════════════════════════════════════════════════
INFORMATION DENSITY REQUIREMENTS (CRITICAL!)
═══════════════════════════════════════════════════════════════════════════════

EACH CORE SCENE MUST CONTAIN:
1. AT LEAST 2-3 LABELED OBJECTS (diagrams, not just text)
2. A TRANSFORMATION or PROCESS animation
3. A CONCEPT CAPTION that teaches something specific
4. AT LEAST 1 EXAM-RELEVANT FACT (number, ratio, formula)

Example GOOD scene (Mendel's Laws):
- 3 pea plant circles (tall, short, tall) with labels
- Punnett square grid with TT, Tt, tt in cells
- Arrow animation showing allele separation
- Caption: "Law of Segregation: Each parent gives ONE allele"
- Key fact: "3:1 ratio in F2 generation"

Example BAD scene (what NOT to do):
- Just text "TT" and "tt" floating
- No actual Punnett square grid
- Caption: "Each parent passes one allele" (too vague)

═══════════════════════════════════════════════════════════════════════════════
STORY FLOW - PLAN THE NARRATIVE FIRST
═══════════════════════════════════════════════════════════════════════════════

For each scene, answer:
1. What does the student KNOW at this point?
2. What NEW IDEA are we introducing?
3. How does this CONNECT to the previous scene?
4. What VISUAL METAPHOR best explains this?
5. What SPECIFIC FACT will they remember for the exam?

DURATION-BASED SCENE COUNT:
- Under 30s: 3 scenes (Intro → 1 Core with 3+ facts → Takeaway)
- 30-60s: 4-5 scenes (Intro → 2-3 Core with 3+ facts each → Takeaway)
- 60-90s: 5-6 scenes (Intro → 3-4 Core with 3+ facts each → Takeaway)
- Over 90s: 6-7 scenes max (Intro → 4-5 Core → Takeaway)

═══════════════════════════════════════════════════════════════════════════════
SCREEN LAYOUT - STRICT ZONES (PREVENTS OVERLAP & OUT-OF-BOUNDS)
═══════════════════════════════════════════════════════════════════════════════

  TITLE ZONE   y ∈ [+2.5, +3.5]  — self.show_title() only. Nothing else here.
  UPPER ZONE   y ∈ [+0.6, +2.2]  — Primary diagrams (atoms, cells, diagrams).
  CENTER ZONE  y ∈ [-0.6, +0.6]  — Secondary elements (arrows, bonds, products).
  LOWER ZONE   y ∈ [-1.8, -0.6]  — Supporting text, sub-labels, smaller items.
  CAPTION BAR  y ∈ [-3.5, -2.5]  — self.play_caption() only.

HORIZONTAL BOUNDS: x = -6 to +6. VERTICAL BOUNDS: y = -3.2 to +3.2.

OVERLAP PREVENTION RULES (ALL MANDATORY):
1. MAX 4 objects on screen simultaneously (shapes + labels combined).
2. MINIMUM 0.7 units vertical spacing between any two text objects.
3. ALL labels: .next_to(shape, DOWN, buff=0.3) — NEVER raw .move_to() for text.
4. CLEAR PREVIOUS before adding new: play(FadeOut(old_group)) then create new.
5. NEVER stack identical-Y elements — shift one LEFT/RIGHT if Y difference < 0.7.
6. Use self.safe_next_to(label, obj, DOWN) in actions[] to auto-clamp labels.
7. Use self.stack_labels([lbl1, lbl2], anchor, DOWN) for multiple labels.
8. In "layout" field: always specify EXACT zone — "atom at UPPER ZONE (y=+1.5)", not "CENTER".

═══════════════════════════════════════════════════════════════════════════════
TOPIC-SPECIFIC VISUAL REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════════

ASTRONOMY/STARS:  Procedural 50-dot nebula cloud, GrowArrow cycle, split-screen fates
GENETICS:         Punnett square 2x2 grid, pea plants as colored circles, 3:1 ratio box
CELL BIOLOGY:     Cell membrane circle + organelle shapes, particle cloud for molecules
CHEMISTRY/BONDS:  Atoms as colored spheres, A+B→C with Flash, MoveAlongPath electron transfer,
                  Ellipse shared orbital, Rotate electron orbit, NumberLine with zones,
                  comparison Table (ionic vs covalent, etc.)
PHYSICS/WAVES:    FunctionGraph sine wave for E & B fields, spectrum VGroup of colored rects,
                  concentric rings for pulses, Arrows for force vectors
WATER CYCLE:      Sun (Circle+8 ray Lines) at top-right, rising vapor (vertical Lines),
                  cloud (5 small Circles clustered), falling rain (10 Line strokes),
                  Rectangle for water body / land / ocean
ELECTRICITY:      Rotating Dot electrons in orbit (Rotate+about_point), arc transfer path

═══════════════════════════════════════════════════════════════════════════════
CINEMATIC ACTION SYNTAX — USE THESE EXACT PATTERNS IN EVERY actions[] ARRAY
═══════════════════════════════════════════════════════════════════════════════

❌  GENERIC (BANNED — produces boring static output):
    "Create nebula_object with GrowFromCenter"
    "Transform or animate protostar formation"
    "Create structure (Circle/Ellipse)"

✅  CINEMATIC (REQUIRED — be this specific):
    "nebula_cloud = VGroup(); [50 Dots with random pos/size/color]; LaggedStart(FadeIn each dot, lag_ratio=0.03)"
    "self.play(nebula_cloud.animate.scale(0.25), run_time=2)  # gravity collapse"
    "protostar = Circle(radius=0.5, color=Colors.ORANGE, fill_opacity=0.9); ReplacementTransform(nebula_cloud, protostar)"
    "h1 = VGroup(Circle+Text('H')).move_to(LEFT*2); h2 = VGroup(Circle+Text('H')).move_to(RIGHT*2)"
    "self.play(h1.animate.move_to(LEFT*0.35), h2.animate.move_to(RIGHT*0.35))  # collision"
    "Flash(ORIGIN, color=Colors.GOLD, line_length=0.7, num_lines=14)  # fusion flash"
    "he = VGroup(Circle+Text('He')); ReplacementTransform(VGroup(h1,h2), he)  # product morph"
    "divider = Line(UP*3.2, DOWN*3.2); Write(left_title at LEFT*3.2+UP*2.5, right_title at RIGHT*3.2+UP*2.5)"
    "rings = VGroup(*[Circle(radius=0.3+i*0.3) for i in range(4)]); LaggedStart(Create each ring, lag_ratio=0.25)"
    "stage_dots cycle diagram: 5 Dots at circle positions, GrowArrow between each pair"
    "LaggedStart(*[FadeIn(item, shift=RIGHT) for item in items], lag_ratio=0.3)"

ALWAYS specify: object names, colors, positions (LEFT/RIGHT/UP*N), animation method, lag_ratio

═══════════════════════════════════════════════════════════════════════════════
REFERENCE PLAN (Star Life Cycle — copy this level of specificity!)
═══════════════════════════════════════════════════════════════════════════════

{{
  "total_duration": 60,
  "timeline": [
    {{
      "scene": 1, "name": "Introduction", "duration": 6,
      "actions": [
        "title_group = self.show_title('Life Cycle of a Star')",
        "self.play_caption('From a nebula of gas to a glowing star')",
        "FadeOut title_group after 1s wait"
      ],
      "layout": "Title at TOP"
    }},
    {{
      "scene": 2, "name": "Nebula — Particle Cloud", "duration": 14,
      "actions": [
        "nebula_cloud = VGroup() with 50 Dot objects: random r=uniform(0.5,2.5), theta, x=r*cos(theta), y=r*sin(theta), radius=uniform(0.03,0.1), color=choice([Colors.PURPLE,Colors.CYAN,Colors.HOT_PINK]), opacity=uniform(0.3,0.8)",
        "LaggedStart(*[FadeIn(dot, scale=0.5) for dot in nebula_cloud], lag_ratio=0.03, run_time=2)",
        "nebula_label = Text('Nebula',font_size=20,color=Colors.BRIGHT_YELLOW).to_edge(DOWN,buff=0.8); Write(nebula_label)",
        "self.play_caption('Stars are born inside massive nebulae')",
        "self.play(nebula_cloud.animate.scale(0.25), run_time=2)  # gravity collapse",
        "self.play_caption('Gravity pulls the cloud inward')"
      ],
      "layout": "Particle cloud at CENTER, label at BOTTOM edge"
    }},
    {{
      "scene": 3, "name": "Protostar — ReplacementTransform Morph", "duration": 10,
      "actions": [
        "protostar = VGroup(Circle(radius=0.8,color=Colors.ORANGE,stroke=Colors.BRIGHT_YELLOW,stroke_width=6,fill_opacity=0.0), Circle(radius=0.5,color=Colors.ORANGE,fill_opacity=0.9))",
        "ReplacementTransform(nebula_cloud, protostar, run_time=1.5)  # MORPH not FadeOut+FadeIn",
        "proto_label = Text('Protostar',font_size=20).next_to(protostar,DOWN,buff=0.4); Write(proto_label)",
        "self.add_glow_pulse(protostar[1], Colors.ORANGE)",
        "self.play_caption('Gravitational collapse creates a Protostar')"
      ],
      "layout": "Protostar at CENTER, label BELOW"
    }},
    {{
      "scene": 4, "name": "Nuclear Fusion — H+H→He with Flash", "duration": 12,
      "actions": [
        "FadeOut protostar, proto_label",
        "fusion_title = Text('Nuclear Fusion!',font_size=26,color=Colors.GOLD,weight=BOLD).to_edge(UP,buff=0.5); Write(fusion_title)",
        "h1 = VGroup(Circle(r=0.3,color=Colors.CYAN,fill_opacity=0.8).move_to(LEFT*2), Text('H',font_size=22).move_to(LEFT*2))",
        "h2 = VGroup(Circle(r=0.3,color=Colors.CYAN,fill_opacity=0.8).move_to(RIGHT*2), Text('H',font_size=22).move_to(RIGHT*2))",
        "GrowFromCenter(h1), GrowFromCenter(h2)",
        "self.play_caption('Two hydrogen nuclei collide at extreme pressure')",
        "self.play(h1.animate.move_to(LEFT*0.35), h2.animate.move_to(RIGHT*0.35), run_time=1.0)",
        "Flash(ORIGIN, color=Colors.GOLD, line_length=0.7, num_lines=14)",
        "he = VGroup(Circle(r=0.45,color=Colors.GOLD,fill_opacity=0.9,stroke=Colors.BRIGHT_YELLOW,stroke_width=4), Text('He',font_size=22)); ReplacementTransform(VGroup(h1,h2), he)",
        "energy_txt = Text('+ 26.7 MeV released!',font_size=20,color=Colors.GOLD).next_to(he,DOWN,buff=0.5); Write(energy_txt)",
        "self.play_caption('4H → He releases enormous energy (E=mc²)')"
      ],
      "layout": "H atoms at x=±2, ORIGIN for fusion, He at CENTER"
    }},
    {{
      "scene": 5, "name": "Split-Screen — Two Stellar Fates", "duration": 10,
      "actions": [
        "FadeOut all previous",
        "divider = Line(UP*3.2, DOWN*3.2, color=WHITE, stroke_opacity=0.4); Create(divider)",
        "low_hdr = Text('Low Mass Star',font_size=18,color=Colors.CYAN,weight=BOLD).move_to(LEFT*3.2+UP*2.5); Write(low_hdr)",
        "high_hdr = Text('High Mass Star',font_size=18,color=Colors.RED,weight=BOLD).move_to(RIGHT*3.2+UP*2.5); Write(high_hdr)",
        "low_star = Circle(r=0.5,color=Colors.BRIGHT_YELLOW,fill_opacity=0.7).move_to(LEFT*3.2+UP*1); GrowFromCenter(low_star)",
        "GrowArrow from low_star down to white_dwarf = Circle(r=0.3,color=Colors.CYAN)",
        "high_star = Circle(r=0.7,color=Colors.RED,fill_opacity=0.7).move_to(RIGHT*3.2+UP*1); GrowFromCenter(high_star)",
        "rings = VGroup(*[Circle(radius=0.3+i*0.3, color=Colors.ORANGE, stroke_opacity=max(0.05,0.7-i*0.2)) for i in range(4)]).next_to(high_arrow,DOWN)",
        "LaggedStart(*[Create(r) for r in rings], lag_ratio=0.25)  # supernova shock wave",
        "self.play_caption('Mass determines the stellar fate')"
      ],
      "layout": "Left panel x=-3.2, right panel x=+3.2, divider at x=0"
    }},
    {{
      "scene": 6, "name": "Circular Cycle Diagram — Takeaway", "duration": 8,
      "actions": [
        "FadeOut all previous",
        "cycle_title = Text('The Stellar Lifecycle',font_size=26,color=Colors.GOLD,weight=BOLD).to_edge(UP,buff=0.5); Write(cycle_title)",
        "stages = ['Nebula','Protostar','Main Seq','Giant','Remnant']; stage_colors = [Colors.PURPLE,Colors.ORANGE,Colors.BRIGHT_YELLOW,Colors.RED,Colors.CYAN]",
        "For each stage i: angle=-PI/2+i*2*PI/5; pos=2.0*[cos(angle),sin(angle),0]; Dot(r=0.28,color=col).move_to(pos); Text(name,font_size=14,color=col).move_to(pos*1.45)",
        "LaggedStart(*[GrowFromCenter(dot) for dot in stage_dots], lag_ratio=0.2)",
        "LaggedStart(*[Write(lbl) for lbl in stage_labels], lag_ratio=0.2)",
        "For each pair (i → i+1 %5): GrowArrow(Arrow(stage_dots[i], stage_dots[i+1], buff=0.3, color=WHITE, stroke_opacity=0.6))",
        "self.play_caption('Key Point: Stars are recycled — nebula to remnant')"
      ],
      "layout": "Cycle diagram at CENTER, title at TOP"
    }}
  ]
}}

Return JSON matching this exact structure — with this level of cinematic specificity in every actions[] array:
{{
  "total_duration": {duration},
  "timeline": [
    {{
      "scene": 1,
      "name": "Introduction",
      "duration": 6,
      "actions": [
        "title_group = self.show_title('Short Title')",
        "self.play_caption('In this video: ...')",
        "FadeOut title_group after wait(1)"
      ],
      "layout": "Title at TOP"
    }},
    {{
      "scene": 2,
      "name": "Core Concept 1 — [Cinematic technique name]",
      "duration": 14,
      "actions": [
        "object_name = VGroup/Circle/etc with SPECIFIC color, size, position",
        "SPECIFIC animation: LaggedStart / ReplacementTransform / Flash / GrowArrow",
        "label = Text('Exact Label Text', font_size=20, color=Colors.BRIGHT_YELLOW).next_to(obj, DOWN, buff=0.3); Write(label)",
        "self.play_caption('Specific explanation under 50 chars')"
      ],
      "layout": "Specific positions: x=LEFT*2, y=UP*1, etc."
    }},
    {{
      "scene": 3,
      "name": "Core Concept 2 — [Cinematic technique name]",
      "duration": 12,
      "actions": [
        "FadeOut previous named objects",
        "SPECIFIC animation sequence with named objects",
        "self.play_caption('Specific explanation')"
      ],
      "layout": "Specific layout description"
    }},
    {{
      "scene": 4,
      "name": "Takeaway",
      "duration": 6,
      "actions": [
        "FadeOut(*self.mobjects)",
        "Write key point text or cycle diagram",
        "self.play_caption('Key Point: ...')"
      ],
      "layout": "Summary at CENTER"
    }}
  ]
}}"""


# ===========================================
# Layer 3: Verification Agent
# ===========================================
LAYER3_PROMPT = """Verify this educational video plan.

Concept: {concept}
Goal: {goal}

Plan:
{plan}

Check:
1. Is content accurate for the requested topic?
2. Are visuals specific (not generic)?
3. Does it teach the concept effectively?

Return JSON:
{{
  "approved": true,
  "issues": ["any problems found"],
  "final_plan": null
}}"""


# ===========================================
# Layer 4: CINEMATIC Manim Code Generation
# ===========================================
LAYER4_PROMPT = """You are a CINEMATIC Manim animator creating 3Blue1Brown-quality educational videos.

**CONCEPT**: {concept}
**VIDEO PLAN**: {plan}

═══════════════════════════════════════════════════════════════════════════════
CRITICAL RULES - READ FIRST!
═══════════════════════════════════════════════════════════════════════════════

0. FOLLOW THE SCENE PLAN — THIS IS LAW, NOT A SUGGESTION!
   The VIDEO PLAN above has scenes, each with an actions[] list.
   ✅  Create EXACTLY one code block per planned scene — in order.
   ✅  Implement EVERY action[] item listed for that scene.
   ✅  Use the objects, animations, and captions named in the plan.
   ✅  Keep self.wait() between scenes to ≤ 1 second (no dead air!).
   ❌  DO NOT invent scenes not in the plan.
   ❌  DO NOT skip or replace planned actions with simpler ones.
   ❌  DO NOT add extra self.wait() pads between scenes (waste of screen time).
   Bad example: plan says "MoveAlongPath electron", you write "self.wait(2)" instead — FORBIDDEN.

1. TITLE MAX 25 CHARACTERS!
   - GOOD: "Mendel's Laws" (13 chars)
   - BAD: "How Mendel's Laws Explain Inheritance Patterns"

   title_group = self.show_title("Mendel's Laws")  # MAX 25 chars!

2. RESPECT DURATION FROM PLAN!
   - Add self.wait() to match planned scene durations
   - Each scene should have: animation time + wait time = planned duration
   - Example: 15 sec scene = 8 sec animations + self.wait(7)

3. CONTENT DENSITY - Every scene MUST be INFORMATION RICH:
   - 2-3 LABELED VISUAL OBJECTS (not just floating text!)
   - 1 TRANSFORMATION/PROCESS animation (arrows, morphs)
   - 1 EXAM FACT (number, ratio, formula shown visually)
   - 1 CAPTION explaining the concept

═══════════════════════════════════════════════════════════════════════════════
CINEMATIC VISUAL PATTERNS (COPY THESE EXACTLY!)
═══════════════════════════════════════════════════════════════════════════════

1. GLOWING VIRUS (Pathogen):
virus = Circle(radius=0.7, color=RED, fill_opacity=0.7)
virus.set_stroke(ORANGE, width=4)
spikes = VGroup()
for i in range(8):
    spike = Triangle(fill_opacity=0.8, color=ORANGE).scale(0.15)
    spike.next_to(virus, direction=np.array([np.cos(i*PI/4), np.sin(i*PI/4), 0]), buff=0)
    spikes.add(spike)
virus_group = VGroup(virus, spikes)
self.play(GrowFromCenter(virus_group))
self.add_glow_pulse(virus, RED)

2. Y-SHAPED ANTIBODY:
antibody = VGroup(
    Line(DOWN*0.6, ORIGIN, stroke_width=5, color=CYAN),
    Line(ORIGIN, UL*0.4, stroke_width=5, color=CYAN),
    Line(ORIGIN, UR*0.4, stroke_width=5, color=CYAN),
)
antibody.scale(1.2)
self.play(Create(antibody))

3. CELL WITH MEMBRANE:
cell = Circle(radius=1.2, color=GREEN, fill_opacity=0.3)
cell.set_stroke(TEAL, width=4)
nucleus = Circle(radius=0.4, color=PURPLE, fill_opacity=0.5)
cell_group = VGroup(cell, nucleus)
self.play(GrowFromCenter(cell_group))

4. ENERGY BURST / REACTION:
self.play(Flash(obj, color=GOLD, line_length=0.6, num_lines=12))
self.add_glow_pulse(obj, GOLD)

5. TRANSFORMATION (Key animation!):
self.play(ReplacementTransform(old_obj, new_obj), run_time=1.5)
self.play(obj.animate.shift(RIGHT*2).scale(0.8).set_color(GREEN), run_time=1)

6. ELEGANT LABEL (Always BELOW):
label = Text("Antibody", font_size=20, color=Colors.BRIGHT_YELLOW)
label.next_to(obj, DOWN, buff=0.3)
self.play(Write(label))

7. PUNNETT SQUARE (for genetics topics):
grid = VGroup()
for i in range(2):
    for j in range(2):
        cell = Square(side_length=0.8, color=CYAN, fill_opacity=0.2)
        cell.move_to(RIGHT*(j-0.5)*0.85 + DOWN*(i-0.5)*0.85)
        grid.add(cell)
grid.move_to(ORIGIN)
genotypes = ["TT", "Tt", "Tt", "tt"]
for i, (cell, geno) in enumerate(zip(grid, genotypes)):
    txt = Text(geno, font_size=18, color=GOLD)
    txt.move_to(cell.get_center())
    grid.add(txt)
self.play(Create(grid))

8. KEY RATIO BOX (for exam facts):
ratio_box = VGroup(
    RoundedRectangle(width=3, height=1, corner_radius=0.1, color=GOLD, fill_opacity=0.2),
    Text("F2 Ratio: 3:1", font_size=24, color=GOLD, weight=BOLD)
)
ratio_box[1].move_to(ratio_box[0].get_center())
self.play(GrowFromCenter(ratio_box))
self.add_glow_pulse(ratio_box, GOLD)

═══════════════════════════════════════════════════════════════════════════════
COLOR MEANINGS (Use purposefully!)
═══════════════════════════════════════════════════════════════════════════════

- RED/ORANGE = Danger, pathogen, threat
- GREEN/TEAL = Health, defense, cell
- CYAN = Antibody, immune response
- GOLD/YELLOW = Energy, success, key point
- PURPLE = Nucleus, transformation
- WHITE = Labels and text

═══════════════════════════════════════════════════════════════════════════════
CINEMATIC TECHNIQUES — MANDATORY FOR 3BLUE1BROWN QUALITY (USE THESE!)
═══════════════════════════════════════════════════════════════════════════════

**A. PROCEDURAL PARTICLE CLOUD (for nebulae, plasma, gas, fluids):**
nebula_cloud = VGroup()
for _ in range(50):                        # 30-80 dots → never boring static shapes
    r = random.uniform(0.5, 2.5)
    theta = random.uniform(0, 2 * PI)
    x = r * np.cos(theta) * random.uniform(0.8, 1.2)
    y = r * np.sin(theta) * random.uniform(0.6, 1.0)
    dot = Dot(radius=random.uniform(0.03, 0.10),
              color=random.choice([Colors.PURPLE, Colors.CYAN, Colors.HOT_PINK]))
    dot.move_to([x, y, 0])
    dot.set_opacity(random.uniform(0.3, 0.8))
    nebula_cloud.add(dot)
self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in nebula_cloud], lag_ratio=0.03), run_time=2)

**B. GRAVITY COLLAPSE (cloud contracts; then MORPH into solid object):**
self.play(nebula_cloud.animate.scale(0.25), run_time=2)          # CONTRACT
protostar = Circle(radius=0.5, color=Colors.ORANGE, fill_opacity=0.9)
self.play(ReplacementTransform(nebula_cloud, protostar), run_time=1.5)  # MORPH

**C. STAGE TRANSFORMATION — ReplacementTransform (objects MORPH, never just disappear):**
# WRONG (boring): self.play(FadeOut(old)); self.play(FadeIn(new))
# RIGHT (cinematic): 
self.play(ReplacementTransform(nebula, protostar), run_time=1.2)
self.play(ReplacementTransform(protostar, main_star), run_time=1.2)

**D. CHEMICAL / NUCLEAR REACTION (A + B → C with Flash):**
a = VGroup(Circle(radius=0.3, color=Colors.CYAN, fill_opacity=0.8).move_to(LEFT*2),
           Text("H", font_size=20, color=WHITE).move_to(LEFT*2))
b = VGroup(Circle(radius=0.3, color=Colors.CYAN, fill_opacity=0.8).move_to(RIGHT*2),
           Text("H", font_size=20, color=WHITE).move_to(RIGHT*2))
self.play(GrowFromCenter(a), GrowFromCenter(b))
self.play(a.animate.move_to(LEFT*0.35), b.animate.move_to(RIGHT*0.35))
self.play(Flash(ORIGIN, color=Colors.GOLD, line_length=0.7, num_lines=14))
product = VGroup(Circle(radius=0.45, color=Colors.GOLD, fill_opacity=0.9),
                 Text("He", font_size=20, color=WHITE))
self.play(ReplacementTransform(VGroup(a, b), product))

**E. SPLIT-SCREEN DUAL PATHS (two simultaneous processes):**
divider = Line(UP * 3.2, DOWN * 3.2, color=WHITE, stroke_opacity=0.4)
self.play(Create(divider))
left_title = Text("Path A", font_size=18, color=Colors.CYAN).move_to(LEFT*3.2 + UP*2.5)
right_title = Text("Path B", font_size=18, color=Colors.RED).move_to(RIGHT*3.2 + UP*2.5)
self.play(Write(left_title), Write(right_title))
# Add left objects at x=-3.2, right objects at x=+3.2

**F. CIRCULAR CYCLE DIAGRAM (with LaggedStart + GrowArrow):**
stages = ["Stage A", "Stage B", "Stage C", "Stage D"]
stage_colors = [Colors.CYAN, Colors.ORANGE, Colors.PURPLE, Colors.RED]
cycle_r = 2.0
stage_dots = VGroup()
stage_labels = VGroup()
for i, (name, col) in enumerate(zip(stages, stage_colors)):
    angle = -PI/2 + i * 2*PI / len(stages)
    pos = cycle_r * np.array([np.cos(angle), np.sin(angle), 0])
    dot = Dot(radius=0.28, color=col).move_to(pos)
    stage_dots.add(dot)
    lbl = Text(name, font_size=14, color=col).move_to(pos * 1.45)
    stage_labels.add(lbl)
self.play(LaggedStart(*[GrowFromCenter(d) for d in stage_dots], lag_ratio=0.2))
self.play(LaggedStart(*[Write(l) for l in stage_labels], lag_ratio=0.2))
for i in range(len(stages)):
    arr = Arrow(stage_dots[i].get_center(), stage_dots[(i+1)%len(stages)].get_center(),
               buff=0.3, color=WHITE, stroke_opacity=0.6)
    self.play(GrowArrow(arr), run_time=0.3)

**G. CONCENTRIC SHOCK RINGS (explosion / energy pulse):**
rings = VGroup(*[
    Circle(radius=0.3 + i*0.35, color=Colors.ORANGE, stroke_opacity=max(0.05, 0.7 - i*0.18))
    for i in range(5)
])
rings.move_to(ORIGIN)
self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.25))

**H. ROTATING OBJECT (for spinning things — neutron star, electron, gear):**
obj = VGroup(Line(ORIGIN, RIGHT*0.8, color=Colors.CYAN),
             Line(ORIGIN, LEFT*0.8, color=Colors.CYAN))
for _ in range(3):
    self.play(Rotate(obj, angle=PI, about_point=obj.get_center()), run_time=0.4)

**I. LAGGED START FOR SEQUENTIAL REVEALS (any list of objects):**
items = [Text(f"Step {{i+1}}", font_size=20, color=Colors.CYAN)
         .move_to(UP*(1.5 - i*1.0)) for i in range(4)]
self.play(LaggedStart(*[FadeIn(item, shift=RIGHT) for item in items], lag_ratio=0.3))

**J. SINE WAVE / EM WAVE (physics waves, oscillation):**
e_wave = FunctionGraph(lambda x: np.sin(x*2)*1.5, x_range=[-3, 3], color=Colors.HOT_PINK)
b_wave = FunctionGraph(lambda x: np.sin(x*2)*1.0, x_range=[-3, 3], color=Colors.CYAN)
self.play(Create(e_wave), Create(b_wave))
# Animate propagation shift:
self.play(e_wave.animate.shift(RIGHT*1), b_wave.animate.shift(RIGHT*1), run_time=2, rate_func=linear)

**K. ELECTRON TRANSFER ALONG ARC (ionic/covalent bonding):**
# Electron moves from one atom to another along a curved path
transfer_path = ArcBetweenPoints(na_electron.get_center(), cl_orbit.point_at_angle(7*PI/4), angle=-PI/2)
self.play(MoveAlongPath(na_electron, transfer_path), run_time=1.5)

**L. ORBITING ELECTRON (atoms, orbitals, electric fields):**
orbit_ring = Circle(radius=1.2, color=Colors.CYAN, stroke_opacity=0.5).move_to(atom.get_center())
e1 = Dot(color=Colors.CYAN).move_to(orbit_ring.point_at_angle(0))
e2 = Dot(color=Colors.CYAN).move_to(orbit_ring.point_at_angle(PI))
shared_orbit = Ellipse(width=2.5, height=1.5, color=Colors.CYAN).move_to(ORIGIN)
self.play(
    Rotate(e1, about_point=ORIGIN, angle=4*PI, run_time=4, rate_func=linear),
    Rotate(e2, about_point=ORIGIN, angle=4*PI, run_time=4, rate_func=linear)
)

**M. ELECTROMAGNETIC SPECTRUM BAR (colored zones):**
spectrum = VGroup()
colors = [Colors.RED, Colors.ORANGE, Colors.BRIGHT_YELLOW, Colors.NEON_GREEN,
          Colors.CYAN, Colors.PURPLE, Colors.HOT_PINK]
for i, c in enumerate(colors):
    rect = Rectangle(width=8/7, height=1, color=c, fill_opacity=0.8)
    rect.move_to(LEFT*4 + RIGHT*(i*8/7 + 4/7))
    rect.set_stroke(width=0)
    spectrum.add(rect)
self.play(FadeIn(spectrum))

**N. COMPARISON TABLE (ionic vs covalent, aerobic vs anaerobic, etc.):**
table = Table(
    [["Transferred", "Shared"],
     ["> 1.7", "< 1.7"],
     ["High (Solids)", "Low (Gases)"],
     ["Yes (Molten)", "No"]],
    col_labels=[Text("Ionic"), Text("Covalent")],
    row_labels=[Text("Electrons"), Text("EN Diff"), Text("Melting Pt"), Text("Conducts")],
    include_outer_lines=True
).scale(0.6)
table.get_col_labels()[0].set_color(Colors.HOT_PINK)
table.get_col_labels()[1].set_color(Colors.CYAN)
self.play(Create(table))

**O. SUN WITH RAYS (heat, energy, photosynthesis):**
sun = Circle(radius=0.5, color=Colors.ORANGE, fill_opacity=0.8)
sun_rays = VGroup()
for i in range(8):
    angle = i * PI / 4
    ray = Line(ORIGIN, RIGHT * 1.0, color=Colors.ORANGE, stroke_width=3)
    ray.rotate(angle, about_point=ORIGIN)
    ray.shift(sun.get_center())
    sun_rays.add(ray)
sun_group = VGroup(sun, sun_rays).move_to(RIGHT*3 + UP*2)
self.play(GrowFromCenter(sun_group))

**P. NUMBERLINE WITH ZONES (for electronegativity, pH scale, spectra):**
number_line = NumberLine(x_range=[0, 4, 1], length=10, color=Colors.WHITE,
                         include_numbers=False).shift(DOWN*0.5)
for val in [0, 1, 2, 3, 4]:
    t = Text(str(val), font_size=20, color=Colors.WHITE)
    t.next_to(number_line.number_to_point(val), DOWN, buff=0.2)
    self.add(t)
self.play(Create(number_line))
# Zones:
ionic_rect = Rectangle(width=5, height=1.5, color=Colors.HOT_PINK, fill_opacity=0.2)
ionic_rect.move_to(number_line.number_to_point(2.85) + UP)
ionic_label = Text("Zone Label", font_size=18, color=Colors.HOT_PINK).next_to(ionic_rect, UP)
self.play(FadeIn(ionic_rect), Write(ionic_label))

**Q. PHASOR → SINE WAVE TRACING (SHM, oscillations, AC circuits, unit circle):**
# ONE CALL — handles the entire animation. Do not rebuild this manually.
self.show_title("Simple Harmonic Motion")
info = Text("x = A·sin(ωt + φ)", font_size=26, color=Colors.BRIGHT_YELLOW).shift(UP*2.8)
self.play(Write(info))
group = self.phasor_to_sine_animation(n_cycles=2, run_time=7)
self.play_caption("Phasor rotation traces the sine wave")
self.wait(1)
self.play(FadeOut(group), FadeOut(info))

═══════════════════════════════════════════════════════════════════════════════
BANNED PATTERNS (NEVER DO THESE!)
═══════════════════════════════════════════════════════════════════════════════

- MathTex, Tex, Matrix             (NO LATEX - user doesn't have it)
- SVGMobject, ImageMobject         (NO external assets — causes FileNotFoundError)
- ZoomIn, ZoomOut, SlideIn         (hallucinated animations - cause NameError)
- Bounce, Pulse, Blink, Appear, Disappear, Spotlight, TypeWrite, SweepIn, SweepOut
                                   (ALL hallucinated — cause NameError)
- Highlight(...)                   (hallucinated — use Indicate() instead)
- Glow(...)                        (NOT a Manim CE class — causes NameError)
- Bubble(...), SpeechBubble(...)   (NOT Manim CE classes — causes NameError)
- Sparkle(...), AnnotationDot(...) (NOT Manim CE classes — causes NameError)
- Flash(..., scale_factor=...)     (scale_factor is NOT a Flash param — causes TypeError)
- Flash(..., glow_radius=...)      (glow_radius is NOT a Flash param — causes TypeError)
- font_size > 44                   (TOO BIG)
- Literal newline inside string    (SYNTAX ERROR - use \\n escape instead)

Flash ONLY accepts: flash_radius=0.5, num_lines=18, color=..., run_time=..., rate_func=...
Indicate() is the correct class for highlighting. Wiggle() for shaking. Write() for typing.

═══════════════════════════════════════════════════════════════════════════════
SCREEN BOUNDS (Strict!)
═══════════════════════════════════════════════════════════════════════════════

SAFE: x in [-5, 5], y in [-2.5, 2.5]
- Title: .to_edge(UP, buff=0.5)
- Main objects: ORIGIN or UP*0.5
- Labels: .next_to(obj, DOWN, buff=0.3)
- Captions: self.play_caption()

MAX 3 objects on screen at once!

═══════════════════════════════════════════════════════════════════════════════
SCENE TEMPLATE (Follow for every scene!)
═══════════════════════════════════════════════════════════════════════════════

# Scene N: [Title]
# 1. Clear previous
self.play(FadeOut(*old_objects, self.captions))

# 2. Create ONE hero object
hero = Circle(radius=0.8, color=CYAN, fill_opacity=0.5)
hero.set_stroke(CYAN, width=3)
self.play(GrowFromCenter(hero))
self.add_glow_pulse(hero, CYAN)

# 3. Label below
label = Text("Name", font_size=20, color=Colors.BRIGHT_YELLOW)
label.next_to(hero, DOWN, buff=0.3)
self.play(Write(label))

# 4. Caption explains
self.play_caption("Clear explanation under 40 chars")

# 5. Transform or move with purpose
self.play(hero.animate.shift(LEFT*2), run_time=1)

FEW-SHOT EXAMPLE (follow this structure exactly):
{few_shot}

OUTPUT: Start with `from manim import *` - nothing else before code."""


# ===========================================
# Layer 5: Code Quality Refinement
# ===========================================
LAYER5_REFINE = """Review and fix this Manim code for CRITICAL issues.

**GENERATED CODE**:
```python
{code}
```

**CRITICAL FIXES REQUIRED**:

0. HALLUCINATION PRUNING (HIGHEST PRIORITY):
   - REMOVE all SVGMobject() and ImageMobject() calls (assets do not exist).
   - REPLACE them with procedural shapes: Circle(), Rectangle(), RegularPolygon(n=...).
   - REMOVE all MathTex(), Tex(), DecimalNumber(), or Matrix().
   - REPLACE them with standard Text() or formatted strings.
   - FIX axis_config={{"include_numbers": True}} -> set to False.

1. BOUNDS CHECKING - FIX IMMEDIATELY:
   - Remove elements positioned at > UP*3 or < DOWN*3
   - Replace .shift(UP * 3) with .to_edge(UP)
   - Replace .shift(DOWN * 3) with .to_edge(DOWN)
   - Add .scale(0.8) for text longer than 50 chars

2. DURATION STRICT COMPLIANCE:
   - Max self.wait() = 5 seconds per scene
   - Remove extra animations that exceed timing budget

3. TEXT WRAPPING:
   - Break long text into lines using \\n
   - Max 50 chars per line

4. OVERLAPPING ELEMENTS:
   - Ensure elements have different positions (buff=0.5)
   - Use .next_to() for proper spacing

5. SCENE TRANSITIONS:
   - Each scene must end with FadeOut(*self.mobjects)
   - No residual objects from previous scenes

**RETURN**: Fixed code ONLY, starting with `from manim import *`"""


# ===========================================
# System Prompt for Code Generation (Layer 4)
# ===========================================
CODEGEN_SYSTEM_PROMPT = """You are a CODE-ONLY generator for Manim Community Edition v0.19+.

CRITICAL RULES - VIOLATION MEANS FAILURE:
1. Output MUST be valid Python code ONLY - NO markdown, NO explanations, NO prose
2. REQUIRED IMPORTS (ALWAYS include ALL three):
   from manim import *
   import random
   import numpy as np
3. FORBIDDEN: os, sys, subprocess, eval, exec, open, __import__, file I/O, network
4. STRICTLY FORBIDDEN (LATEX): MathTex, Tex, DecimalNumber, Matrix. USER DOES NOT HAVE LATEX.
5. USE INSTEAD: Text() for ALL mathematical expressions.
6. Class MUST be named GeneratedScene inheriting from ColorfulScene (from template)
7. NO top-level code outside methods.
8. USE self.play_caption("text") for ALL captions.

═══════════════════════════════════════════════════════════════════════════════
CINEMATIC MANDATE — YOU MUST USE THESE TECHNIQUES (not just circles + labels):
═══════════════════════════════════════════════════════════════════════════════

For ANY topic involving particles, gas, fluid, cells, atoms, electrons:
→ Use PROCEDURAL LOOPS (30-80 objects) with LaggedStart, NOT single static shapes:
   cloud = VGroup()
   for _ in range(50):
       dot = Dot(radius=random.uniform(0.03, 0.1),
                 color=random.choice([Colors.CYAN, Colors.PURPLE, Colors.HOT_PINK]))
       dot.move_to([random.uniform(-2.5,2.5), random.uniform(-1.5,1.5), 0])
       dot.set_opacity(random.uniform(0.3, 0.8))
       cloud.add(dot)
   self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in cloud], lag_ratio=0.03), run_time=2)

For state changes (gas→liquid, nebula→star, molecule→product):
→ MORPH with ReplacementTransform (NEVER just FadeOut+FadeIn):
   self.play(ReplacementTransform(old_object, new_object), run_time=1.5)

For chemical/nuclear reactions:
→ Bring reactants together → Flash → ReplacementTransform into product:
   self.play(a.animate.move_to(LEFT*0.35), b.animate.move_to(RIGHT*0.35))
   self.play(Flash(ORIGIN, color=Colors.GOLD, line_length=0.7, num_lines=14))
   self.play(ReplacementTransform(VGroup(a, b), product))

For explosions/shockwaves/energy pulses:
→ Concentric rings with LaggedStart:
   rings = VGroup(*[Circle(radius=0.3+i*0.35, color=Colors.ORANGE,
                   stroke_opacity=max(0.05, 0.7-i*0.18)) for i in range(5)])
   self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.25))

For comparing two paths/processes simultaneously:
→ Split-screen with divider line:
   divider = Line(UP*3.2, DOWN*3.2, color=WHITE, stroke_opacity=0.4)
   left_title.move_to(LEFT*3.2 + UP*2.5); right_title.move_to(RIGHT*3.2 + UP*2.5)

For cycles/processes that repeat:
→ Circular cycle diagram with GrowArrow between stage dots:
   for i in range(len(stages)):
       angle = -PI/2 + i * 2*PI/len(stages)
       pos = 2.0 * np.array([np.cos(angle), np.sin(angle), 0])

For sequential reveals (steps, lists, stages):
→ LaggedStart with shift:
   self.play(LaggedStart(*[FadeIn(item, shift=RIGHT) for item in items], lag_ratio=0.3))

For wave/oscillation topics (EM waves, sound, SHM):
→ FunctionGraph sine wave:
   e_wave = FunctionGraph(lambda x: np.sin(x*2)*1.5, x_range=[-3, 3], color=Colors.HOT_PINK)
   self.play(Create(e_wave))
   self.play(e_wave.animate.shift(RIGHT*1), run_time=2, rate_func=linear)  # propagation

For electron/ion transfer (chemistry bonding):
→ MoveAlongPath with ArcBetweenPoints:
   path = ArcBetweenPoints(start_pos, end_pos, angle=-PI/2)
   self.play(MoveAlongPath(electron_dot, path), run_time=1.5)

For atomic orbitals / electron orbits:
→ Rotate around a center point:
   self.play(Rotate(electron, about_point=atom.get_center(), angle=2*PI, run_time=2, rate_func=linear))

For scale/comparison topics (pH, electronegativity, spectra):
→ NumberLine with manual Text labels + colored zone Rectangles:
   nl = NumberLine(x_range=[0,4,1], length=10, include_numbers=False)
   zone = Rectangle(width=4, height=1.5, color=Colors.CYAN, fill_opacity=0.2)

For pros/cons or multi-property comparison:
→ Table with col_labels and row_labels:
   table = Table([["Val A", "Val B"], ["Val C", "Val D"]],
                 col_labels=[Text("Option 1"), Text("Option 2")],
                 row_labels=[Text("Property 1"), Text("Property 2")],
                 include_outer_lines=True).scale(0.6)

═══════════════════════════════════════════════════════════════════════════════

MANDATORY & AVAILABLE ColorfulScene METHODS — USE THESE, NOT raw Manim equivalents:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE STRUCTURE (use every video):
  self.show_title("Bond Types")           → gradient title + underline. Every scene start.
  self.show_intro("Bond Types","learn...") → show_title + opening caption in one call.
  self.play_caption("text ≤60 chars")     → caption box at bottom. ALL narration here.
  self.show_key_point("Exam fact")        → gold highlighted box. Takeaway scenes.
  self.show_takeaway("key","exam tip")    → FadeOut all + show_key_point + exam caption.

VISUAL QUALITY (use liberally for cinematic feel):
  self.add_glow_pulse(obj, COLOR)              → pulsing glow highlight. Key moments.
  self.add_wiggle_effect(obj)                  → vibrate for "active/excited" objects.
  self.create_glowing_object(mob, COLOR)       → wrap ANY shape in a colored glow ring.
  self.create_glowing_text("text", 22, COLOR)  → Text with soft glow halo. Headers.
  self.setup_gradient_header("Title","sub")    → vivid CYAN→PURPLE→PINK gradient header.

LAYOUT (OVERLAP PREVENTION — always use instead of raw .next_to for labels):
  self.safe_next_to(label, anchor, DOWN, 0.4) → .next_to() + auto clamp to screen.
  self.stack_labels([l1,l2], anchor, DOWN)    → chain multiple labels, no overlap.
  self.clamp_to_screen(mob)                   → call after any .move_to() to ensure on-screen.
  self.create_labeled_object("circle","Nucleus", pos, Colors.CYAN) → shape + label pair.
  self.create_labeled_shape(shape, "Label", DOWN, 0.3)             → shape + safe label.

REACTIONS & PROCESSES:
  self.animate_process(reactants_vg, products_vg, "→")  → moves reactants LEFT, products RIGHT with arrow.
  self.create_reaction_arrow(LEFT*1, RIGHT*1, "ΔH=...")  → Arrow with label above.
  self.add_transformation_arrow(obj1, obj2, "label")     → Draws arrow between two objects + label.
  self.add_collision_effect(obj1, obj2, Colors.HOT_PINK) → Smash: both flash color then recolor.
  self.collision_burst(obj1, obj2)                       → CINEMATIC smash: Flash + color burst + recolor.

ENERGY & COMPARISON CHARTS:
  self.show_energy_diagram([2,2,34], ["Glyc","Krebs","ETC"], "ATP Yield") → animated bar chart.

PARTICLES:
  self.create_particle_group(40, 0.3, Colors.CYAN)       → VGroup of random particles.
  self.animate_particles_movement(particles, duration=2)  → physics drift to new positions.

WAVES & OSCILLATIONS (SHM, unit circle, phasors, electromagnetic waves):
  self.phasor_to_sine_animation(n_cycles=2, run_time=6)
      → 3B1B-style: rotating phasor circle (LEFT) traces sine wave (RIGHT) in real time.
         Returns VGroup of all objects — FadeOut when done.
         ALWAYS use for: SHM, oscillations, AC circuits, unit circle, wave intro.
         circle_center defaults to LEFT*3.5; radius defaults to 1.0.
  self.static_sine_wave(amplitude=1.0, frequency=1.0, label_text="y = A sin(ωt)")
      → Static FunctionGraph sine wave with optional label. For frozen diagrams only.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COLLISION & INTERACTION PATTERNS (nuclear fusion, ionic bonding, chemical reactions):
─────────────────────────────────────────────────────────────────────────────
→ Cinematic smash for ANY A + B → C reaction:
   h1 = Circle(radius=0.3, color=Colors.CYAN, fill_opacity=0.8).move_to(LEFT*2.5)
   h2 = Circle(radius=0.3, color=Colors.HOT_PINK, fill_opacity=0.8).move_to(RIGHT*2.5)
   self.play(GrowFromCenter(h1), GrowFromCenter(h2))
   self.play(h1.animate.move_to(LEFT*0.4), h2.animate.move_to(RIGHT*0.4), run_time=0.8)
   self.collision_burst(h1, h2)                          # Flash at impact point
   product = Circle(radius=0.5, color=Colors.GOLD, fill_opacity=0.9).move_to(ORIGIN)
   self.play(ReplacementTransform(VGroup(h1, h2), product), run_time=1.2)

→ Glowing highlighted structure (key atoms, organelles, nucleus):
   glowing_nucleus = self.create_glowing_object(Circle(radius=0.4, color=Colors.GOLD), Colors.GOLD)
   self.play(GrowFromCenter(glowing_nucleus))
   self.add_glow_pulse(glowing_nucleus, Colors.GOLD)

→ Energy / ATP bar chart (ALWAYS use for respiration, photosynthesis, bioenergetics):
   chart = self.show_energy_diagram([2, 2, 34], ["Glycolysis","Krebs","ETC"], "ATP per glucose")

→ Particle cloud physics collapse (nebulae, gas pressure, diffusion):
   cloud = self.create_particle_group(40, 0.3, Colors.CYAN)
   self.play(LaggedStart(*[FadeIn(p, scale=0.3) for p in cloud], lag_ratio=0.03), run_time=2)
   self.animate_particles_movement(cloud, duration=1.5)
   self.play(cloud.animate.scale(0.25).move_to(ORIGIN), run_time=1.5)

→ Phasor → Sine wave tracing (SHM, oscillation, AC circuits, unit circle):
   self.show_title("Simple Harmonic Motion")
   lbl = Text("ω = angle/time", font_size=22, color=Colors.BRIGHT_YELLOW).to_edge(UP).shift(DOWN*0.6)
   self.play(FadeIn(lbl))
   group = self.phasor_to_sine_animation(n_cycles=2, run_time=7)
   self.wait(1)
   self.play(FadeOut(group), FadeOut(lbl))

─────────────────────────────────────────────────────────────────────────────

═══════════════════════════════════════════════════════════════════════════════
LAYOUT ZONES — MANDATORY (PREVENTS TEXT OVERLAP):
═══════════════════════════════════════════════════════════════════════════════

Screen is divided into 4 non-overlapping vertical zones:

  TITLE ZONE   Y ∈ [+2.5, +3.5]  → self.show_title() only. DO NOT place anything else here.
  UPPER ZONE   Y ∈ [+0.6, +2.2]  → Main objects, atom/cell diagrams, equations.
  CENTER ZONE  Y ∈ [-0.6, +0.6]  → Secondary structures, arrows, bonds.
  LOWER ZONE   Y ∈ [-1.8, -0.6]  → Supporting text, sub-labels, formulae.
  CAPTION BAR  Y ∈ [-3.5, -2.5]  → self.play_caption() only. DO NOT place anything here.

RULES — EVERY RULE MANDATORY:
1. NEVER place two text objects within 0.7 units of each other (Y axis).
2. After self.show_title(), all content starts at Y ≤ +1.8 (title occupies top).
3. Labels ALWAYS use .next_to(shape, DOWN, buff=0.3) — NEVER raw .move_to() for text.
4. Multiple labels on same scene: stack with .arrange(DOWN, buff=0.35) or .next_to() chain.
5. Left/Right split: left objects at X=-3.0, right objects at X=+3.0, keep Y ∈ [-1, +1.5].
6. Use self.safe_next_to(label, atom, DOWN, buff=0.3) for labels — auto-clamps to screen.
7. Use self.stack_labels([lbl1, lbl2], anchor, DOWN) for multiple labels on one object.
8. NEVER use UP*3.5 or DOWN*3.5 — use .to_edge(UP/DOWN, buff=0.5) instead.
9. Max 4 distinct text objects visible on screen simultaneously.
10. If a label would overlap another, SKIP it or POSITION it to the side instead.

═══════════════════════════════════════════════════════════════════════════════

SCREEN BOUNDS - CRITICAL (Manim screen is 14.2 x 8 units):
- SAFE: X from -6 to 6, Y from -3.2 to 3.2
- NEVER .shift(UP*4) or .shift(DOWN*4) — use .to_edge(UP/DOWN, buff=0.5)
- font_size MAX 44, MIN 14. Captions: 20. Titles: 36.
- MAX caption length: 60 characters. Break long text with \\n.

BANNED ANIMATIONS (CAUSE NameError — DO NOT USE):
- ZoomIn, ZoomOut, Zoom, SlideIn, SlideOut, PopIn, Emerge, Expand, Collapse
- ShowCreation (use Create), Morph (use Transform/ReplacementTransform)

BANNED IMPORTS / OBJECTS:
- MathTex, Tex, Matrix (NO LATEX)
- SVGMobject, ImageMobject (no assets on disk)

CRITICAL STRING RULES:
- NEVER break a string literal across two lines (use \\n inside strings instead)
- Max 60 chars per play_caption() string

VALID ANIMATIONS: FadeIn, FadeOut, Write, Create, GrowFromCenter, ShrinkToCenter,
Transform, ReplacementTransform, Flash, Wiggle, Indicate, LaggedStart, AnimationGroup,
GrowArrow, Rotate, Succession, MoveAlongPath

VALID SPECIAL OBJECTS: FunctionGraph, NumberLine, ArcBetweenPoints, Table,
Ellipse, VMobject, Brace, SurroundingRectangle

OUTPUT: Start with from manim import *, then class GeneratedScene(ColorfulScene), then construct(self)"""


# ===========================================
# Validation Prompt (for LLM-assisted review)
# ===========================================
VALIDATION_PROMPT = """You are a Manim code validator. Quickly check if this code is valid and safe.

```python
{code}
```

Check for:
1. Syntax errors
2. Missing imports (random, numpy if used)
3. GeneratedScene inherits from ColorfulScene (not Scene)
4. No forbidden imports (os, sys, subprocess, etc.)
5. No hallucinated animations (ZoomIn, SlideIn, etc.)
6. Proper construct() method exists

Return JSON:
{{
  "valid": true,
  "issues": ["list of issues found"],
  "fix_suggestion": "brief fix instruction if invalid"
}}"""
