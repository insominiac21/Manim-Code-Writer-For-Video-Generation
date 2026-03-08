"""
MentorBoxAI - CINEMATIC Few-Shot Examples for Manim Code Generation
3Blue1Brown-quality Manim code with artistic visuals and engaging animations.

These examples demonstrate:
- CINEMATIC visual quality (glows, transformations, purpose)
- Clean INTRO → CORE → TAKEAWAY structure
- Labels ALWAYS below objects (no overlap)
- MAX 3 objects per scene
- Meaningful color usage
"""

# ===========================================
# GOLDEN EXAMPLE: Vaccine Mechanism (CINEMATIC)
# ===========================================
GOLDEN_EXAMPLE_VACCINE = '''from manim import *
import numpy as np

class GeneratedScene(ColorfulScene):
    def construct(self):
        # ═══════════════════════════════════════
        # SCENE 1: Dramatic Introduction
        # ═══════════════════════════════════════
        title_group = self.show_title("How Vaccines Work")
        self.play_caption("Your immune system's secret training program")
        self.wait(1)
        self.play(FadeOut(title_group, self.captions))

        # ═══════════════════════════════════════
        # SCENE 2: The Threat - Menacing Virus
        # ═══════════════════════════════════════
        # Glowing virus with spikes (CINEMATIC)
        virus = Circle(radius=0.9, color=RED, fill_opacity=0.7)
        virus.set_stroke(ORANGE, width=5)
        
        # Menacing spikes
        spikes = VGroup()
        for i in range(8):
            angle = i * PI / 4
            spike = Triangle(fill_opacity=0.9, color=ORANGE).scale(0.18)
            spike.rotate(angle + PI/2)
            spike.shift(virus.point_at_angle(angle) * 1.15)
            spikes.add(spike)
        
        virus_group = VGroup(virus, spikes).move_to(ORIGIN)
        
        # Dramatic entrance
        self.play(GrowFromCenter(virus_group), run_time=1.5)
        self.add_glow_pulse(virus, RED)  # Menacing pulse!
        
        virus_label = Text("Pathogen", font_size=22, color=Colors.BRIGHT_YELLOW)
        virus_label.next_to(virus_group, DOWN, buff=0.4)
        self.play(Write(virus_label))
        self.play_caption("Viruses are dangerous invaders")
        self.wait(1)

        # ═══════════════════════════════════════
        # SCENE 3: The Solution - Vaccine Injection
        # ═══════════════════════════════════════
        # Move virus aside
        self.play(virus_group.animate.shift(LEFT * 3).scale(0.6), 
                  virus_label.animate.shift(LEFT * 3))
        
        # Elegant syringe representation
        syringe_body = RoundedRectangle(width=2.5, height=0.6, corner_radius=0.1, 
                                         color=CYAN, fill_opacity=0.3)
        syringe_body.set_stroke(CYAN, width=3)
        needle = Line(syringe_body.get_right(), syringe_body.get_right() + RIGHT * 0.8, 
                     color=WHITE, stroke_width=4)
        syringe = VGroup(syringe_body, needle).move_to(RIGHT * 2.5)
        
        # Weakened antigen inside (same shape as virus but smaller, lighter)
        mini_antigen = Circle(radius=0.15, color=BLUE, fill_opacity=0.6)
        mini_antigen.move_to(syringe_body.get_center())
        
        syringe_label = Text("Vaccine", font_size=20, color=Colors.BRIGHT_YELLOW)
        syringe_label.next_to(syringe, DOWN, buff=0.3)
        
        self.play(FadeIn(syringe), FadeIn(mini_antigen))
        self.play(Write(syringe_label))
        self.add_glow_pulse(mini_antigen, CYAN)
        self.play_caption("Vaccine = weakened/harmless antigen")
        
        # Clear for next scene
        self.play(FadeOut(virus_group, virus_label, syringe, syringe_label, 
                          mini_antigen, self.captions))

        # ═══════════════════════════════════════
        # SCENE 4: Immune Response - B-Cell Activation
        # ═══════════════════════════════════════
        # B-cell (the hero!)
        b_cell = Circle(radius=1, color=GREEN, fill_opacity=0.4)
        b_cell.set_stroke(TEAL, width=4)
        b_cell.move_to(LEFT * 2)
        
        # Nucleus inside
        nucleus = Circle(radius=0.3, color=PURPLE, fill_opacity=0.6)
        nucleus.move_to(b_cell.get_center())
        
        b_group = VGroup(b_cell, nucleus)
        
        b_label = Text("B-Cell (Defender)", font_size=18, color=Colors.BRIGHT_YELLOW)
        b_label.next_to(b_group, DOWN, buff=0.3)
        
        self.play(GrowFromCenter(b_group))
        self.play(Write(b_label))
        self.play_caption("B-cells recognize the antigen")
        
        # Antigen approaches
        antigen = Circle(radius=0.25, color=BLUE, fill_opacity=0.7).move_to(RIGHT * 3)
        self.play(FadeIn(antigen))
        self.play(antigen.animate.move_to(b_cell.get_right() + RIGHT * 0.3), run_time=1)
        
        # Recognition flash!
        self.play(Flash(b_cell, color=GOLD, line_length=0.5, num_lines=12))
        self.play_caption("Recognition triggers antibody production!")

        # ═══════════════════════════════════════
        # SCENE 5: Antibody Production (The Climax!)
        # ═══════════════════════════════════════
        self.play(FadeOut(antigen))
        
        # Y-shaped antibodies emerge
        def create_antibody(position):
            ab = VGroup(
                Line(DOWN * 0.4, ORIGIN, stroke_width=4, color=GOLD),
                Line(ORIGIN, UL * 0.25, stroke_width=4, color=GOLD),
                Line(ORIGIN, UR * 0.25, stroke_width=4, color=GOLD),
            )
            ab.scale(1.3).move_to(b_cell.get_center())
            return ab
        
        antibodies = VGroup(*[create_antibody(ORIGIN) for _ in range(4)])
        
        # Antibodies burst out!
        self.play(LaggedStart(*[Create(ab) for ab in antibodies], lag_ratio=0.2))
        
        # Spread to defensive positions
        targets = [UP * 1.5 + RIGHT, RIGHT * 2.5, DOWN * 1.5 + RIGHT, RIGHT * 2.5 + DOWN * 0.5]
        self.play(*[ab.animate.move_to(t) for ab, t in zip(antibodies, targets)], run_time=1.5)
        
        ab_label = Text("Antibodies", font_size=18, color=Colors.GOLD)
        ab_label.next_to(antibodies, DOWN, buff=0.3)
        self.play(Write(ab_label))
        self.add_glow_pulse(antibodies[0], GOLD)
        self.play_caption("Antibodies neutralize the threat!")

        # ═══════════════════════════════════════
        # SCENE 6: Takeaway - Memory Cells
        # ═══════════════════════════════════════
        self.play(FadeOut(b_group, b_label, antibodies, ab_label, self.captions))
        
        # Memory cell (star shape for "remember")
        memory = RegularPolygon(n=5, color=PURPLE, fill_opacity=0.5)
        memory.set_stroke(Colors.HOT_PINK, width=4)
        memory.scale(0.8).move_to(ORIGIN)
        
        memory_label = Text("Memory Cell", font_size=22, color=Colors.BRIGHT_YELLOW)
        memory_label.next_to(memory, DOWN, buff=0.4)
        
        self.play(GrowFromCenter(memory))
        self.add_glow_pulse(memory, PURPLE)
        self.play(Write(memory_label))
        
        # Key takeaway box
        takeaway = Text("Key Point: Vaccines teach immunity\\nwithout causing disease!", 
                        font_size=20, color=WHITE)
        takeaway.to_edge(UP, buff=0.8)
        takeaway_box = SurroundingRectangle(takeaway, color=GOLD, buff=0.2, corner_radius=0.1)
        
        self.play(Write(takeaway), Create(takeaway_box))
        self.play_caption("Now you're protected for life!")
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
'''

# ===========================================
# GOLDEN EXAMPLE: Star Life Cycle (CINEMATIC MASTER TEMPLATE)
# Demonstrates ALL advanced techniques:
#   - Procedural particle cloud (50 dots, LaggedStart)
#   - Gravity collapse (.animate.scale())
#   - ReplacementTransform to morph objects between stages
#   - Fusion reaction with Flash
#   - Split-screen dual paths
#   - Circular cycle diagram with GrowArrow
#   - Rotating animations
#   - Concentric ring shock waves
# ===========================================
GOLDEN_EXAMPLE_STAR = '''from manim import *
import random
import numpy as np

class GeneratedScene(ColorfulScene):
    def construct(self):
        # ═══════════════════════════════════════
        # SCENE 1: Introduction
        # ═══════════════════════════════════════
        title_group = self.show_title("Life Cycle of a Star")
        self.play_caption("From a nebula of gas to a glowing star")
        self.wait(1)
        self.play(FadeOut(title_group, self.captions))

        # ═══════════════════════════════════════
        # SCENE 2: Nebula — Procedural Particle Cloud
        # 50 dots with random position, size, opacity, color
        # ═══════════════════════════════════════
        nebula_cloud = VGroup()
        for _ in range(50):
            r = random.uniform(0.5, 2.5)
            theta = random.uniform(0, 2 * PI)
            x = r * np.cos(theta) * random.uniform(0.8, 1.2)
            y = r * np.sin(theta) * random.uniform(0.6, 1.0)
            dot = Dot(
                radius=random.uniform(0.03, 0.10),
                color=random.choice([Colors.PURPLE, Colors.HOT_PINK, Colors.CYAN])
            )
            dot.move_to([x, y, 0])
            dot.set_opacity(random.uniform(0.3, 0.8))
            nebula_cloud.add(dot)

        # LaggedStart: particles appear one by one (cinematic!)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in nebula_cloud], lag_ratio=0.03),
            run_time=2
        )
        nebula_label = Text("Nebula (Gas & Dust Cloud)", font_size=20,
                            color=Colors.BRIGHT_YELLOW)
        nebula_label.to_edge(DOWN, buff=0.8)
        self.play(Write(nebula_label))
        self.play_caption("Stars are born inside massive nebulae")
        self.wait(1)

        # ═══════════════════════════════════════
        # SCENE 3: Gravity Collapse → Protostar
        # Nebula contracts; ReplacementTransform to protostar glow
        # ═══════════════════════════════════════
        self.play_caption("Gravity pulls the cloud inward...")
        # Gravity collapse: scale the entire cloud to a point
        self.play(nebula_cloud.animate.scale(0.25), run_time=2)

        # Protostar: bright glowing core
        protostar_core = Circle(radius=0.5, color=Colors.ORANGE, fill_opacity=0.9)
        protostar_core.set_stroke(Colors.BRIGHT_YELLOW, width=6)
        protostar_glow = Circle(radius=0.8, color=Colors.ORANGE, fill_opacity=0.0)
        protostar_glow.set_stroke(Colors.ORANGE, width=3, opacity=0.5)
        protostar = VGroup(protostar_glow, protostar_core)

        # MORPH nebula cloud → protostar (ReplacementTransform!)
        self.play(ReplacementTransform(nebula_cloud, protostar), run_time=1.5)
        self.play(FadeOut(nebula_label))
        proto_label = Text("Protostar", font_size=20, color=Colors.BRIGHT_YELLOW)
        proto_label.next_to(protostar, DOWN, buff=0.4)
        self.play(Write(proto_label))
        self.add_glow_pulse(protostar_core, Colors.ORANGE)
        self.play_caption("Gravitational collapse creates a Protostar")
        self.wait(1)

        # ═══════════════════════════════════════
        # SCENE 4: Nuclear Fusion — H + H → He
        # ═══════════════════════════════════════
        self.play(FadeOut(protostar, proto_label, self.captions))

        fusion_title = Text("Nuclear Fusion Ignites!", font_size=26,
                            color=Colors.GOLD, weight=BOLD)
        fusion_title.to_edge(UP, buff=0.5)
        self.play(Write(fusion_title))

        # Two hydrogen nuclei approach
        h1_dot = Circle(radius=0.3, color=Colors.CYAN, fill_opacity=0.8).move_to(LEFT * 2)
        h1_lbl = Text("H", font_size=22, color=WHITE).move_to(LEFT * 2)
        h2_dot = Circle(radius=0.3, color=Colors.CYAN, fill_opacity=0.8).move_to(RIGHT * 2)
        h2_lbl = Text("H", font_size=22, color=WHITE).move_to(RIGHT * 2)
        h1 = VGroup(h1_dot, h1_lbl)
        h2 = VGroup(h2_dot, h2_lbl)

        self.play(GrowFromCenter(h1), GrowFromCenter(h2))
        self.play_caption("Two hydrogen nuclei collide at extreme temperatures")
        # Collision
        self.play(h1.animate.move_to(LEFT * 0.35), h2.animate.move_to(RIGHT * 0.35),
                  run_time=1.0)
        # Explosion flash!
        self.play(Flash(ORIGIN, color=Colors.GOLD, line_length=0.7, num_lines=14))

        # Helium product
        he_dot = Circle(radius=0.45, color=Colors.GOLD, fill_opacity=0.9)
        he_dot.set_stroke(Colors.BRIGHT_YELLOW, width=4)
        he_lbl = Text("He", font_size=22, color=WHITE).move_to(ORIGIN)
        he = VGroup(he_dot, he_lbl)

        # MORPH the two H atoms into one He atom
        self.play(ReplacementTransform(VGroup(h1, h2), he), run_time=1.0)
        self.add_glow_pulse(he_dot, Colors.GOLD)

        energy_txt = Text("+ 26.7 MeV energy released!", font_size=20, color=Colors.GOLD)
        energy_txt.next_to(he, DOWN, buff=0.5)
        self.play(Write(energy_txt))
        self.play_caption("4H → He releases enormous energy (E = mc²)")
        self.wait(1.5)

        # ═══════════════════════════════════════
        # SCENE 5: Split-Screen — Two Stellar Fates
        # ═══════════════════════════════════════
        self.play(FadeOut(fusion_title, he, energy_txt, self.captions))

        # Vertical divider
        divider = Line(UP * 3.2, DOWN * 3.2, color=WHITE, stroke_opacity=0.4)
        self.play(Create(divider))

        # Left: Low-Mass → White Dwarf
        low_hdr = Text("Low Mass Star", font_size=18, color=Colors.CYAN, weight=BOLD)
        low_hdr.move_to(LEFT * 3.2 + UP * 2.5)
        self.play(Write(low_hdr))

        low_star = Circle(radius=0.5, color=Colors.BRIGHT_YELLOW, fill_opacity=0.7)
        low_star.move_to(LEFT * 3.2 + UP * 1.0)
        low_star_lbl = Text("Main Sequence\nStar", font_size=14, color=Colors.BRIGHT_YELLOW)
        low_star_lbl.next_to(low_star, DOWN, buff=0.2)
        self.play(GrowFromCenter(low_star), Write(low_star_lbl))

        low_arrow = Arrow(low_star.get_bottom(), low_star.get_bottom() + DOWN * 1.0,
                          color=Colors.CYAN)
        self.play(GrowArrow(low_arrow))

        white_dwarf = Circle(radius=0.3, color=Colors.CYAN, fill_opacity=0.8)
        white_dwarf.next_to(low_arrow, DOWN, buff=0.1)
        wd_lbl = Text("White Dwarf", font_size=14, color=Colors.CYAN)
        wd_lbl.next_to(white_dwarf, DOWN, buff=0.2)
        self.play(GrowFromCenter(white_dwarf), Write(wd_lbl))

        # Right: High-Mass → Black Hole
        high_hdr = Text("High Mass Star", font_size=18, color=Colors.RED, weight=BOLD)
        high_hdr.move_to(RIGHT * 3.2 + UP * 2.5)
        self.play(Write(high_hdr))

        high_star = Circle(radius=0.7, color=Colors.RED, fill_opacity=0.7)
        high_star.move_to(RIGHT * 3.2 + UP * 1.0)
        high_star_lbl = Text("Giant Star", font_size=14, color=Colors.RED)
        high_star_lbl.next_to(high_star, DOWN, buff=0.2)
        self.play(GrowFromCenter(high_star), Write(high_star_lbl))

        high_arrow = Arrow(high_star.get_bottom(), high_star.get_bottom() + DOWN * 1.0,
                           color=Colors.RED)
        self.play(GrowArrow(high_arrow))

        # Concentric shock-wave rings for supernova
        rings = VGroup(*[
            Circle(radius=0.3 + i * 0.3, color=Colors.ORANGE,
                   stroke_opacity=max(0.05, 0.7 - i * 0.2))
            for i in range(4)
        ])
        rings.next_to(high_arrow, DOWN, buff=0.1)
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.25))

        bh_lbl = Text("Black Hole", font_size=14, color=Colors.HOT_PINK)
        bh_lbl.next_to(rings, DOWN, buff=0.2)
        self.play(Write(bh_lbl))
        self.play_caption("Mass determines the stellar fate")
        self.wait(1.5)

        # ═══════════════════════════════════════
        # SCENE 6: Takeaway — Circular Cycle Diagram
        # ═══════════════════════════════════════
        self.play(FadeOut(*self.mobjects))

        cycle_title = Text("The Stellar Lifecycle", font_size=26,
                           color=Colors.GOLD, weight=BOLD)
        cycle_title.to_edge(UP, buff=0.5)
        self.play(Write(cycle_title))

        stages = ["Nebula", "Protostar", "Main\nSequence", "Giant", "Remnant"]
        stage_colors = [Colors.PURPLE, Colors.ORANGE, Colors.BRIGHT_YELLOW,
                        Colors.RED, Colors.CYAN]
        cycle_radius = 2.0

        stage_dots = VGroup()
        stage_labels = VGroup()
        for i, (name, col) in enumerate(zip(stages, stage_colors)):
            angle = -PI / 2 + i * 2 * PI / len(stages)
            pos = cycle_radius * np.array([np.cos(angle), np.sin(angle), 0])
            dot = Dot(radius=0.28, color=col)
            dot.move_to(pos)
            stage_dots.add(dot)
            lbl = Text(name, font_size=14, color=col)
            lbl.move_to(pos * 1.45)
            stage_labels.add(lbl)

        self.play(LaggedStart(*[GrowFromCenter(d) for d in stage_dots], lag_ratio=0.2))
        self.play(LaggedStart(*[Write(l) for l in stage_labels], lag_ratio=0.2))

        # Arrows connecting stages
        for i in range(len(stages)):
            a = stage_dots[i].get_center()
            b = stage_dots[(i + 1) % len(stages)].get_center()
            mid = (a + b) / 2
            direction = b - a
            arr = Arrow(a, b, buff=0.3, color=WHITE, stroke_opacity=0.6)
            self.play(GrowArrow(arr), run_time=0.3)

        self.play_caption("Key Point: Stars are recycled — nebula to remnant")
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
'''

# ===========================================
# GOLDEN EXAMPLE: Cellular Respiration (NEET Biology)
# ===========================================
GOLDEN_EXAMPLE_RESPIRATION = '''from manim import *
import numpy as np

class GeneratedScene(ColorfulScene):
    def construct(self):
        # ═══════════════════════════════════════
        # SCENE 1: Introduction
        # ═══════════════════════════════════════
        title_group = self.show_title("Cellular Respiration")
        self.play_caption("In this video: How cells convert glucose to ATP")
        self.wait(1)
        self.play(FadeOut(title_group, self.captions))

        # ═══════════════════════════════════════
        # SCENE 2: Glucose Molecule
        # ═══════════════════════════════════════
        # Simple hexagonal representation
        glucose = RegularPolygon(n=6, color=Colors.NEON_GREEN, fill_opacity=0.4)
        glucose.set_stroke(Colors.NEON_GREEN, width=3)
        glucose.scale(1.2)
        glucose.move_to(LEFT * 3)
        
        # Label BELOW
        glucose_label = Text("Glucose (C6H12O6)", font_size=18, color=Colors.BRIGHT_YELLOW)
        glucose_label.next_to(glucose, DOWN, buff=0.3)
        
        self.play(GrowFromCenter(glucose), Write(glucose_label))
        self.add_glow_pulse(glucose, Colors.NEON_GREEN)
        self.play_caption("Glucose is the primary fuel for cellular respiration")

        # ═══════════════════════════════════════
        # SCENE 3: Glycolysis (Cytoplasm)
        # ═══════════════════════════════════════
        # Cytoplasm box
        cyto_box = Rectangle(width=4, height=3, color=Colors.CYAN, fill_opacity=0.1)
        cyto_box.set_stroke(Colors.CYAN, width=2)
        cyto_box.move_to(ORIGIN)
        
        cyto_label = Text("Cytoplasm", font_size=16, color=Colors.CYAN)
        cyto_label.next_to(cyto_box, UP, buff=0.2)
        
        self.play(FadeIn(cyto_box), Write(cyto_label))
        
        # Move glucose into cytoplasm
        self.play(glucose.animate.move_to(LEFT * 1), glucose_label.animate.next_to(LEFT * 1 + DOWN * 1.5, DOWN, buff=0.1))
        
        # Split into pyruvate
        pyruvate1 = RegularPolygon(n=3, color=Colors.ORANGE, fill_opacity=0.5).scale(0.6)
        pyruvate2 = RegularPolygon(n=3, color=Colors.ORANGE, fill_opacity=0.5).scale(0.6)
        pyruvate1.move_to(RIGHT * 0.5 + UP * 0.5)
        pyruvate2.move_to(RIGHT * 0.5 + DOWN * 0.5)
        
        pyr_label = Text("2 Pyruvate", font_size=16, color=Colors.ORANGE)
        pyr_label.next_to(VGroup(pyruvate1, pyruvate2), DOWN, buff=0.3)
        
        self.play(Flash(glucose, color=Colors.GOLD, line_length=0.3))
        self.play(ReplacementTransform(glucose, VGroup(pyruvate1, pyruvate2)))
        self.play(FadeOut(glucose_label), Write(pyr_label))
        
        # ATP produced
        atp_text = Text("+2 ATP", font_size=20, color=Colors.GOLD, weight=BOLD)
        atp_text.next_to(cyto_box, RIGHT, buff=0.3)
        self.play(Write(atp_text))
        self.play_caption("Glycolysis: Glucose → 2 Pyruvate + 2 ATP")

        # ═══════════════════════════════════════
        # SCENE 4: Mitochondria (Krebs + ETC)
        # ═══════════════════════════════════════
        # Mitochondria
        mito = Ellipse(width=3.5, height=1.8, color=Colors.ORANGE, fill_opacity=0.2)
        mito.set_stroke(Colors.ORANGE, width=3)
        mito.move_to(RIGHT * 3)
        
        # Inner membrane folds (cristae)
        cristae = VGroup(*[
            Line(RIGHT * 2.2 + UP * (0.4 * i - 0.4), RIGHT * 3.5 + UP * (0.4 * i - 0.4), 
                 color=Colors.RED, stroke_width=2)
            for i in range(3)
        ])
        
        mito_label = Text("Mitochondria", font_size=16, color=Colors.ORANGE)
        mito_label.next_to(mito, DOWN, buff=0.3)
        
        self.play(FadeIn(mito), Create(cristae), Write(mito_label))
        
        # Pyruvate enters mitochondria
        self.play(
            pyruvate1.animate.move_to(mito.get_center() + UP * 0.3),
            pyruvate2.animate.move_to(mito.get_center() + DOWN * 0.3),
            FadeOut(pyr_label, cyto_box, cyto_label)
        )
        self.play_caption("Pyruvate enters mitochondria for Krebs cycle")
        
        # Krebs cycle produces more ATP
        krebs_atp = Text("+2 ATP", font_size=18, color=Colors.GOLD)
        krebs_atp.next_to(mito, UP, buff=0.3)
        
        etc_atp = Text("+34 ATP", font_size=20, color=Colors.GOLD, weight=BOLD)
        etc_atp.next_to(mito, RIGHT, buff=0.3)
        
        self.play(Write(krebs_atp))
        self.play_caption("Krebs Cycle: 2 ATP + electron carriers")
        
        self.play(Flash(mito, color=Colors.GOLD, line_length=0.5))
        self.play(Write(etc_atp))
        self.play_caption("ETC: 32-34 ATP (most energy here!)")

        # ═══════════════════════════════════════
        # SCENE 5: Takeaway - Summary Equation
        # ═══════════════════════════════════════
        self.play(FadeOut(mito, cristae, mito_label, pyruvate1, pyruvate2, 
                         atp_text, krebs_atp, etc_atp, self.captions))
        
        # Summary equation
        eq = Text("C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + 36-38 ATP", 
                 font_size=24, color=Colors.GOLD)
        eq.move_to(UP * 1)
        
        eq_box = SurroundingRectangle(eq, color=Colors.GOLD, buff=0.2, corner_radius=0.1)
        
        self.play(Write(eq), Create(eq_box))
        
        # Key point
        key_point = Text("Key Point: Glycolysis=2, Krebs=2, ETC=34 ATP", 
                        font_size=20, color=Colors.CYAN)
        key_point.next_to(eq_box, DOWN, buff=0.5)
        
        self.play(Write(key_point))
        self.play_caption("NEET Tip: Most ATP comes from Electron Transport Chain!")
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
'''


# ===========================================
# GOLDEN EXAMPLE: Nuclear Fusion (NEET Physics)
# ===========================================
GOLDEN_EXAMPLE_FUSION = '''from manim import *
import numpy as np

class GeneratedScene(ColorfulScene):
    def construct(self):
        # ═══════════════════════════════════════
        # SCENE 1: Introduction
        # ═══════════════════════════════════════
        title_group = self.show_title("Nuclear Fusion in Stars")
        self.play_caption("In this video: How stars produce energy through fusion")
        self.wait(1)
        self.play(FadeOut(title_group, self.captions))

        # ═══════════════════════════════════════
        # SCENE 2: The Star's Core
        # ═══════════════════════════════════════
        # Star core (circle with glow)
        core = Circle(radius=2, color=Colors.BRIGHT_YELLOW, fill_opacity=0.3)
        core.set_stroke(Colors.ORANGE, width=5)
        
        # Label BELOW
        core_label = Text("Star Core (15 million °C)", font_size=18, color=Colors.BRIGHT_YELLOW)
        core_label.next_to(core, DOWN, buff=0.3)
        
        self.play(GrowFromCenter(core))
        self.play(Write(core_label))
        self.add_glow_pulse(core, Colors.ORANGE)
        self.play_caption("Stars have extremely hot cores where fusion occurs")
        
        self.play(FadeOut(core, core_label, self.captions))

        # ═══════════════════════════════════════
        # SCENE 3: Proton-Proton Chain
        # ═══════════════════════════════════════
        step_label = Text("Proton-Proton Chain", font_size=24, color=Colors.CYAN, weight=BOLD)
        step_label.to_edge(UP, buff=0.4)
        self.play(Write(step_label))
        
        # Two protons
        proton1 = Circle(radius=0.4, color=Colors.RED, fill_opacity=0.7)
        proton1.set_stroke(Colors.ORANGE, width=3)
        p1_label = Text("H⁺", font_size=18, color=Colors.WHITE)
        p1_group = VGroup(proton1, p1_label)
        p1_group.move_to(LEFT * 3)
        
        proton2 = Circle(radius=0.4, color=Colors.RED, fill_opacity=0.7)
        proton2.set_stroke(Colors.ORANGE, width=3)
        p2_label = Text("H⁺", font_size=18, color=Colors.WHITE)
        p2_group = VGroup(proton2, p2_label)
        p2_group.move_to(RIGHT * 3)
        
        # Labels below
        left_label = Text("Proton 1", font_size=14, color=Colors.BRIGHT_YELLOW)
        left_label.next_to(p1_group, DOWN, buff=0.3)
        right_label = Text("Proton 2", font_size=14, color=Colors.BRIGHT_YELLOW)
        right_label.next_to(p2_group, DOWN, buff=0.3)
        
        self.play(GrowFromCenter(p1_group), GrowFromCenter(p2_group))
        self.play(Write(left_label), Write(right_label))
        self.play_caption("Two hydrogen nuclei (protons) approach each other")
        
        # Collision
        self.play(
            p1_group.animate.move_to(LEFT * 0.3),
            p2_group.animate.move_to(RIGHT * 0.3),
            FadeOut(left_label, right_label),
            run_time=1.5
        )
        
        # Flash for collision
        self.play(Flash(ORIGIN, color=Colors.BRIGHT_YELLOW, line_length=0.6))
        
        # Deuterium forms
        deuterium = Circle(radius=0.5, color=Colors.PURPLE, fill_opacity=0.7)
        deuterium.set_stroke(Colors.HOT_PINK, width=3)
        d_label_inner = Text("²H", font_size=20, color=Colors.WHITE)
        d_group = VGroup(deuterium, d_label_inner)
        d_group.move_to(ORIGIN)
        
        d_label = Text("Deuterium", font_size=16, color=Colors.BRIGHT_YELLOW)
        d_label.next_to(d_group, DOWN, buff=0.3)
        
        self.play(ReplacementTransform(VGroup(p1_group, p2_group), d_group))
        self.play(Write(d_label))
        self.play_caption("Fusion creates deuterium and releases energy!")
        
        # Equation
        eq = Text("H + H → ²H + energy", font_size=20, color=Colors.GOLD)
        eq.to_edge(DOWN, buff=1)
        self.play(Write(eq))
        self.wait(1)
        
        self.play(FadeOut(step_label, d_group, d_label, eq, self.captions))

        # ═══════════════════════════════════════
        # SCENE 4: Takeaway
        # ═══════════════════════════════════════
        # Final equation
        final_eq = Text("4H → He + 26.7 MeV", font_size=28, color=Colors.GOLD)
        final_eq.move_to(UP * 0.5)
        
        eq_box = SurroundingRectangle(final_eq, color=Colors.GOLD, buff=0.2, corner_radius=0.1)
        
        self.play(Write(final_eq), Create(eq_box))
        
        key_point = Text("Key Point: Mass converts to energy (E=mc²)", 
                        font_size=20, color=Colors.CYAN)
        key_point.next_to(eq_box, DOWN, buff=0.5)
        
        self.play(Write(key_point))
        self.play_caption("NEET Tip: Mass defect = Energy released in fusion")
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
'''

# ===========================================
# Example 1: Physics - Simple Harmonic Motion
# ===========================================
EXAMPLE_PHYSICS_SHM = '''from manim import *

class GeneratedScene(ColorfulScene):
    def construct(self):
        self.add_background_particles()
        
        # ═══════════════════════════════════════
        # SCENE 1: Title and Introduction
        # ═══════════════════════════════════════
        title_group = self.setup_gradient_header("Simple Harmonic Motion", "The Physics of Oscillation")
        self.play(FadeIn(title_group, shift=DOWN))
        self.play_caption("SHM is a type of periodic motion where the restoring force is proportional to the displacement.")
        self.play(FadeOut(title_group))
        
        # ═══════════════════════════════════════
        # SCENE 2: Spring-Mass System
        # ═══════════════════════════════════════
        self.next_section("Spring System")
        scene_title = self.create_glowing_text("Spring-Mass System", font_size=36, color=Colors.TEAL)
        scene_title.to_edge(UP)
        self.play(Write(scene_title))
        
        # Fixed wall
        wall = Rectangle(width=0.3, height=2, color=Colors.GRAY, fill_opacity=0.8)
        wall.move_to(LEFT * 4)
        
        # Spring visualization (zigzag line)
        spring_points = [LEFT * 3.7]
        for i in range(8):
            offset = UP * 0.3 if i % 2 == 0 else DOWN * 0.3
            spring_points.append(LEFT * (3.7 - (i + 1) * 0.3) + offset)
        spring_points.append(LEFT * 0.5)
        spring = VMobject(color=Colors.BLUE)
        spring.set_points_as_corners(spring_points)
        
        # Mass block
        mass = Square(side_length=0.8, color=Colors.RED, fill_opacity=0.7)
        mass.move_to(LEFT * 0.1)
        mass_label = Text("m", font_size=24, color=Colors.WHITE).move_to(mass.get_center())
        mass_group = VGroup(mass, mass_label)
        
        # Equip line
        eq_line = DashedLine(UP * 1.5, DOWN * 1.5, color=Colors.YELLOW)
        eq_line.move_to(ORIGIN)
        eq_label = Text("Equilibrium", font_size=18, color=Colors.YELLOW).next_to(eq_line, DOWN, buff=0.3)
        
        self.play(Create(wall), Create(spring), Create(mass_group))
        self.play(Create(eq_line), Write(eq_label))
        
        self.play_caption("A mass attached to a spring oscillates back and forth around its equilibrium position.")
        
        # Animate oscillation
        self.play(
            mass_group.animate.shift(RIGHT * 1.5),
            rate_func=there_and_back,
            run_time=2
        )
        self.add_wiggle_effect(mass_group) # Visualize energy
        
        self.wait(1)
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 3: The Equation
        # ═══════════════════════════════════════
        # NO MathTex - Use Text/Glow
        header = self.create_glowing_text("Equation: x(t) = A cos(wt + p)", font_size=36, color=Colors.CYAN)
        header.to_edge(UP, buff=1.0)
        self.play(Write(header))
        self.add_fun_pulse(header)
        
        variables = VGroup(
            Text("A = Amplitude (Distance)", font_size=24, color=Colors.WHITE),
            Text("w = Angular Frequency", font_size=24, color=Colors.WHITE),
            Text("t = Time", font_size=24, color=Colors.WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        variables.next_to(header, DOWN, buff=1.0)
        
        for var in variables:
            self.play(FadeIn(var, shift=RIGHT))
            self.wait(0.5)
            
        self.play_caption("The position x changes over time t, described by a cosine wave.")
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
'''


# ===========================================
# Example 2: Biology - Cell Division (Mitosis)
# ===========================================
EXAMPLE_BIOLOGY_MITOSIS = '''from manim import *

class GeneratedScene(ColorfulScene):
    def construct(self):
        self.add_background_particles()
        
        # ═══════════════════════════════════════
        # SCENE 1: Introduction
        # ═══════════════════════════════════════
        title_group = self.setup_gradient_header("Mitosis: Cell Division", "How Life Replicates")
        self.play(FadeIn(title_group))
        self.play_caption("Mitosis is the process where a single cell divides into two identical daughter cells.")
        self.play(FadeOut(title_group))
        
        # ═══════════════════════════════════════
        # SCENE 2: The Cell (Interphase)
        # ═══════════════════════════════════════
        cell = Circle(radius=2, color=Colors.NEON_GREEN, stroke_width=4)
        nucleus = Circle(radius=0.8, color=Colors.CYAN, fill_opacity=0.3)
        nucleus.move_to(cell.get_center())
        
        # DNA strands
        dna1 = Line(LEFT*0.3, RIGHT*0.3, color=Colors.HOT_PINK).move_to(nucleus.get_center() + UP*0.1)
        dna2 = Line(LEFT*0.3, RIGHT*0.3, color=Colors.HOT_PINK).move_to(nucleus.get_center() + DOWN*0.1)
        dna_group = VGroup(dna1, dna2)
        
        self.play(GrowFromCenter(cell), FadeIn(nucleus), Create(dna_group))
        self.add_glow_pulse(nucleus, color=Colors.CYAN)
        
        self.play_caption("In Interphase, the cell grows and duplicates its DNA inside the nucleus.")
        
        # Duplication
        dna_copy = dna_group.copy().set_color(Colors.ORANGE)
        self.play(
            dna_group.animate.shift(LEFT*0.2),
            dna_copy.animate.shift(RIGHT*0.2)
        )
        self.play_caption("We now have two sets of genetic material ready to split.")
        self.wait(1)
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 3: Chromosome Alignment
        # ═══════════════════════════════════════
        chromosomes = VGroup()
        for i in range(4):
            c = VGroup(
                Line(UP*0.4, DOWN*0.4, color=Colors.HOT_PINK, stroke_width=6),
                Line(UP*0.4, DOWN*0.4, color=Colors.HOT_PINK, stroke_width=6).rotate(PI/2)
            ).rotate(PI/4)
            c.move_to(UP*(1.5 - i) + LEFT*random.uniform(-0.5, 0.5))
            chromosomes.add(c)
            
        self.play(Create(chromosomes))
        self.play_caption("The DNA condenses into visible chromosomes.")
        
        # Alignment
        self.play(chromosomes.animate.arrange(DOWN, buff=0.5))
        self.add_fun_pulse(chromosomes)
        self.play_caption("During Metaphase, chromosomes align in the center of the cell.")
        
        # Split (Anaphase)
        left_side = chromosomes.copy().shift(LEFT*2)
        right_side = chromosomes.copy().shift(RIGHT*2)
        
        self.play(
            Transform(chromosomes, VGroup(left_side, right_side)),
            run_time=2
        )
        self.play_caption("Finally, they are pulled apart to opposite sides.")
        self.wait(2)
'''


# ===========================================
# Example 3: Math - Quadratic Functions
# ===========================================
EXAMPLE_MATH_QUADRATIC = '''from manim import *

class GeneratedScene(ColorfulScene):
    def construct(self):
        self.add_background_particles()
        
        # ═══════════════════════════════════════
        # SCENE 1: Introduction
        # ═══════════════════════════════════════
        title = self.setup_gradient_header("Quadratic Functions", "The Shape of Parabolas")
        self.play(Write(title))
        self.play_caption("A quadratic function creates a U-shaped curve called a Parabola.")
        self.play(FadeOut(title))
        
        # ═══════════════════════════════════════
        # SCENE 2: The Graph
        # ═══════════════════════════════════════
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 9, 2],
            x_length=6, y_length=5,
            axis_config={"color": Colors.WHITE}
        ).scale(0.9)
        
        labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(labels))
        
        # Plot y = x^2
        graph = axes.plot(lambda x: x**2, color=Colors.CYAN, x_range=[-3, 3])
        graph_label = Text("y = x^2", font_size=24, color=Colors.CYAN).next_to(graph, UP)
        
        self.play(Create(graph), Write(graph_label))
        self.add_glow_pulse(graph, color=Colors.CYAN)
        
        # Vertex
        vertex = Dot(axes.c2p(0, 0), color=Colors.HOT_PINK)
        v_label = Text("Vertex (0,0)", font_size=20, color=Colors.HOT_PINK).next_to(vertex, DOWN)
        
        self.play(GrowFromCenter(vertex), Write(v_label))
        self.play_caption("The vertex is the turning point. Here, it is the minimum value.")
        
        # Transformation
        graph2 = axes.plot(lambda x: x**2 + 2, color=Colors.ORANGE, x_range=[-2.5, 2.5])
        vertex2 = Dot(axes.c2p(0, 2), color=Colors.ORANGE)
        
        self.play(
            Transform(graph, graph2),
            Transform(vertex, vertex2),
            Transform(v_label, Text("Vertex (0,2)", font_size=20, color=Colors.ORANGE).next_to(vertex2, RIGHT))
        )
        self.play_caption("Adding a constant shifts the parabola up.")
        
        self.wait(2)
'''


# ===========================================
# Example 4: Epic Biology - Virus Attack (Refined)
# ===========================================
EXAMPLE_EPIC_BIOLOGY = '''from manim import *
import random
import numpy as np

class GeneratedScene(ColorfulScene):
    def construct(self):
        # 1. SETUP ATMOSPHERE
        self.add_background_particles() # MANDATORY: Dynamic background
        
        # ═══════════════════════════════════════
        # SCENE 1: The Invasion (Cinematic Intro)
        # ═══════════════════════════════════════
        # Gradient Header
        title_group = self.setup_gradient_header("Viral Invasion", "The Cellular Mechanisms of Infection")
        self.play(FadeIn(title_group, shift=DOWN))
        self.play_caption("A virus is a microscopic hijacker that needs a host cell to survive.")
        self.play(FadeOut(title_group, shift=UP))
        
        # ═══════════════════════════════════════
        # SCENE 2: The Virus (Hero Object)
        # ═══════════════════════════════════════
        scene_title = self.create_glowing_text("The Adversary: Bacteriophage", font_size=32, color=Colors.CYAN)
        scene_title.to_edge(UP)
        self.play(Write(scene_title))

        # Build Virus (Complex shape)
        head = RegularPolygon(n=6, color=Colors.CYAN, fill_opacity=0.5).scale(1.2)
        dna_core = SpiralIn(circles_color=Colors.HOT_PINK, circles_opacity=0.8).scale(0.5).move_to(head)
        tail = Line(head.get_bottom(), head.get_bottom() + DOWN*2, color=Colors.CYAN, stroke_width=5)
        legs = VGroup(*[
            Line(tail.get_end(), tail.get_end() + DOWN*0.5 + RIGHT*0.5*i, color=Colors.CYAN)
            for i in [-1, 1]
        ])
        virus = VGroup(head, dna_core, tail, legs).move_to(ORIGIN)
        
        # Dynamic entrance
        self.play(GrowFromCenter(head), Create(tail), Create(legs))
        self.add_fun_pulse(head, color=Colors.CYAN) # Pulse effect
        
        # Label with Glow
        label = self.create_glowing_text("Bacteriophage", font_size=28, color=Colors.CYAN)
        label.next_to(virus, UP, buff=0.5)
        self.play(Write(label))
        
        self.play_caption("This is a Bacteriophage. It specifically targets bacteria.")
        self.play(FadeOut(*self.mobjects))

        # ═══════════════════════════════════════
        # SCENE 3: The Attack (Action Sequence)
        # ═══════════════════════════════════════
        # Cell Surface (Curved line)
        cell_surface = Arc(radius=10, angle=PI/4, color=Colors.NEON_GREEN, stroke_width=8).move_to(DOWN*4)
        surface_label = self.create_glowing_text("Host Cell Membrane", font_size=24, color=Colors.NEON_GREEN)
        surface_label.next_to(cell_surface, DOWN, buff=0.5)
        
        self.play(Create(cell_surface), Write(surface_label))
        
        # Virus Landing (Motion Path)
        virus.move_to(UP*3 + LEFT*2)
        target_point = cell_surface.point_from_proportion(0.5)
        
        self.play(virus.animate.move_to(target_point + UP*2), run_time=1.5)
        self.play(virus.animate.move_to(target_point), run_time=0.5) # Docking
        
        # Injection
        rna_stream = DashedLine(virus.get_center(), target_point + DOWN*3, color=Colors.HOT_PINK, stroke_width=4)
        self.play(Create(rna_stream), run_time=1)
        self.add_fun_pulse(rna_stream)
        
        action_text = self.create_glowing_text("Injecting Viral DNA!", font_size=32, color=Colors.HOT_PINK)
        action_text.to_edge(UP)
        self.play(Write(action_text))
        
        self.play_caption("The virus injects its genetic material, taking control of the cell's machinery.")
        self.wait(2)
'''


# ===========================================
# Golden Example: SHM / Oscillations / Phasor
# ===========================================
GOLDEN_EXAMPLE_SHM = '''from manim import *
from app.services.manim_templates import ColorfulScene, Colors

class GeneratedScene(ColorfulScene):
    def construct(self):
        self.add_background_particles()

        # ── SCENE 1: Title ──────────────────────────────────────────────────────
        self.show_title("Simple Harmonic Motion")
        self.play_caption("Oscillation — the heartbeat of physics")
        self.wait(0.8)

        # ── SCENE 2: Key equation ────────────────────────────────────────────────
        eq = Text("x  =  A · sin(ωt + φ)", font_size=30, color=Colors.BRIGHT_YELLOW)
        eq.shift(UP * 0.5)
        labels = VGroup(
            Text("A = amplitude", font_size=18, color=Colors.CYAN),
            Text("ω = angular frequency", font_size=18, color=Colors.NEON_GREEN),
            Text("φ = phase", font_size=18, color=Colors.HOT_PINK),
        )
        self.arrange_column(labels[0], labels[1], labels[2], start_y=-0.8, spacing=0.55)
        self.play(Write(eq), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.25))
        self.play_caption("Three parameters completely define any oscillation")
        self.wait(1)
        self.play(FadeOut(eq), FadeOut(labels))

        # ── SCENE 3: Phasor → Sine wave tracing ────────────────────────────────
        intro = Text("Phasor → Sine Wave", font_size=24, color=Colors.GOLD).shift(UP * 3.0)
        self.play(FadeIn(intro))
        self.play_caption("A rotating phasor traces the sine curve")
        group = self.phasor_to_sine_animation(n_cycles=2, run_time=7)
        self.wait(0.5)
        self.play(FadeOut(group), FadeOut(intro))

        # ── SCENE 4: Real-world examples ────────────────────────────────────────
        self.show_title("Where SHM Appears")
        examples = [
            ("Pendulum",    Colors.CYAN,         LEFT*3.5),
            ("Spring-Mass", Colors.NEON_GREEN,    ORIGIN),
            ("LC Circuit",  Colors.HOT_PINK,      RIGHT*3.5),
        ]
        icons = VGroup()
        lbls  = VGroup()
        for name, col, pos in examples:
            icon = Circle(radius=0.5, color=col, fill_opacity=0.7).move_to(pos)
            lbl  = Text(name, font_size=18, color=col).next_to(icon, DOWN, buff=0.3)
            icons.add(icon)
            lbls.add(lbl)
        self.play(LaggedStart(*[GrowFromCenter(i) for i in icons], lag_ratio=0.3))
        self.play(LaggedStart(*[Write(l) for l in lbls], lag_ratio=0.3))
        self.play_caption("Pendulums, springs, and circuits all follow x = A·sin(ωt)")
        self.wait(2)
        self.play(FadeOut(icons), FadeOut(lbls))
        self.play(FadeOut(*self.mobjects))
'''


# ===========================================
# Combined Few-Shot Examples String
# ===========================================
FEW_SHOT_EXAMPLES = f"""
### EXAMPLE 1: Biology Animation (Cinematic)
```python
{EXAMPLE_EPIC_BIOLOGY}
```

### EXAMPLE 2: Physics Animation (SHM)
```python
{EXAMPLE_PHYSICS_SHM}
```

### EXAMPLE 3: Mathematics (Quadratic)
```python
{EXAMPLE_MATH_QUADRATIC}
```
"""


# ===========================================
# Short Example for Context-Limited Prompts
# ===========================================
SHORT_EXAMPLE = '''from manim import *

class GeneratedScene(ColorfulScene):
    def construct(self):
        self.add_background_particles()
        
        # SCENE 1: Title
        title = self.setup_gradient_header("Topic Title", "Brief description")
        self.play(Write(title))
        self.play_caption("This is an example explanation centered at the bottom.")
        self.play(FadeOut(title))
        
        # SCENE 2: Main Content
        visual = Circle(radius=1, color=Colors.BLUE, fill_opacity=0.5)
        self.play(Create(visual))
        self.add_fun_pulse(visual)
        
        label = self.create_glowing_text("Element", color=Colors.WHITE)
        label.next_to(visual, DOWN)
        self.play(Write(label))
        
        self.wait(3)
'''


def get_few_shot_for_topic(topic: str) -> str:
    """Return the most relevant few-shot example for a topic.

    Examples (cinematic quality, all use ColorfulScene):
    - GOLDEN_EXAMPLE_STAR:        ← PRIMARY DEFAULT — shows ALL cinematic techniques:
                                    particle cloud, LaggedStart, ReplacementTransform,
                                    gravity collapse, fusion reaction, split-screen,
                                    cycle diagram, concentric rings
    - GOLDEN_EXAMPLE_VACCINE:     immunity, vaccines, antibodies, pathogens
    - GOLDEN_EXAMPLE_RESPIRATION: cellular processes, ATP, metabolism
    - GOLDEN_EXAMPLE_FUSION:      nuclear physics, stars, energy
    - GOLDEN_EXAMPLE_SHM:         SHM, oscillations, phasors, waves, unit circle, AC circuits

    MANDATORY structure:
    INTRO (10%) → CORE CONTENT (70-80%) → TAKEAWAY (10%)
    """
    topic_lower = topic.lower()

    # PRIORITY 1: Vaccine/Immunity Topics
    if any(kw in topic_lower for kw in ['vaccine', 'immun', 'antibod', 'antigen', 'pathogen',
                                         'virus infect', 'immune system', 'lymphocyte',
                                         'b cell', 't cell', 'white blood', 'infection']):
        return GOLDEN_EXAMPLE_VACCINE

    # PRIORITY 2: Cellular Processes
    elif any(kw in topic_lower for kw in ['respiration', 'atp', 'mitochondria', 'glucose',
                                           'glycolysis', 'krebs', 'electron transport',
                                           'photosynthesis', 'chloroplast', 'metabolism']):
        return GOLDEN_EXAMPLE_RESPIRATION

    # PRIORITY 3: Stars / Astronomy / Lifecycle / Cycle diagrams
    elif any(kw in topic_lower for kw in ['star', 'nebula', 'galaxy', 'astrono', 'cosmos',
                                           'solar', 'lifecycle', 'life cycle', 'cycle',
                                           'nuclear', 'fusion', 'fission', 'radioactiv',
                                           'sun', 'hydrogen', 'helium', 'proton']):
        return GOLDEN_EXAMPLE_STAR  # Best cinematic example for visual richness

    # PRIORITY 4: SHM / Oscillations / Waves / Phasors
    elif any(kw in topic_lower for kw in ['simple harmonic', 'shm', 'oscillat', 'pendulum',
                                           'phasor', 'sine wave', 'angular frequency',
                                           'amplitude', 'vibrat', 'resonan', 'spring mass',
                                           'ac circuit', 'unit circle', 'wave motion']):
        return GOLDEN_EXAMPLE_SHM

    # PRIORITY 5: Physics (general forces, motion, optics)
    elif any(kw in topic_lower for kw in ['physics', 'motion', 'force', 'wave', 'space',
                                           'energy', 'electric', 'magnet', 'circuit',
                                           'light', 'optic']):
        return GOLDEN_EXAMPLE_STAR  # Star example demos particle/transform patterns well

    # PRIORITY 6: Biology (cells, organs, processes)
    elif any(kw in topic_lower for kw in ['biology', 'cell', 'dna', 'mitos', 'bacteria',
                                           'enzyme', 'protein', 'digestion', 'blood',
                                           'heart', 'nerve', 'brain', 'organ', 'meiosis',
                                           'genetics', 'mendel', 'chromosome']):
        return GOLDEN_EXAMPLE_RESPIRATION  # Biochem process → Respiration template

    # PRIORITY 7: Chemistry
    elif any(kw in topic_lower for kw in ['chemistry', 'bond', 'molecule', 'atom', 'reaction',
                                           'ionic', 'covalent', 'acid', 'base', 'ph',
                                           'oxidation', 'reduction', 'electrolysis']):
        return GOLDEN_EXAMPLE_STAR  # Fusion example covers A + B → C reactions

    # PRIORITY 8: Math
    elif any(kw in topic_lower for kw in ['math', 'quadrat', 'function', 'graph', 'equation',
                                           'calculus', 'trigonometry', 'algebra', 'geometry']):
        return EXAMPLE_MATH_QUADRATIC

    else:
        # DEFAULT: Star lifecycle — richest visuals, best cinematic template
        return GOLDEN_EXAMPLE_STAR
