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
        glucose_label = Text("Glucose (C₆H₁₂O₆)", font_size=18, color=Colors.BRIGHT_YELLOW)
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
    
    NEET-Quality Examples:
    - GOLDEN_EXAMPLE_VACCINE: For immunity, vaccines, antibodies, pathogens
    - GOLDEN_EXAMPLE_RESPIRATION: For cellular processes, ATP, metabolism
    - GOLDEN_EXAMPLE_FUSION: For physics, nuclear, stars, energy
    
    All examples follow MANDATORY structure:
    INTRO (10%) → CORE CONTENT (70-80%) → TAKEAWAY (10%)
    """
    topic_lower = topic.lower()
    
    # PRIORITY 1: Vaccine/Immunity Topics (GOLDEN_EXAMPLE_VACCINE)
    if any(kw in topic_lower for kw in ['vaccine', 'immun', 'antibod', 'antigen', 'pathogen', 
                                         'virus infect', 'immune system', 'lymphocyte', 
                                         'b cell', 't cell', 'white blood', 'infection']):
        return GOLDEN_EXAMPLE_VACCINE
    
    # PRIORITY 2: Cellular Processes (GOLDEN_EXAMPLE_RESPIRATION)
    elif any(kw in topic_lower for kw in ['respiration', 'atp', 'mitochondria', 'glucose', 
                                           'glycolysis', 'krebs', 'electron transport', 
                                           'photosynthesis', 'chloroplast', 'metabolism']):
        return GOLDEN_EXAMPLE_RESPIRATION
    
    # PRIORITY 3: Nuclear/Stellar Physics (GOLDEN_EXAMPLE_FUSION)
    elif any(kw in topic_lower for kw in ['fusion', 'star', 'nuclear', 'sun', 'hydrogen', 
                                           'helium', 'proton', 'fission', 'radioactiv']):
        return GOLDEN_EXAMPLE_FUSION
    
    # FALLBACK by subject area
    elif any(kw in topic_lower for kw in ['biology', 'cell', 'dna', 'mitos', 'bacteria', 
                                           'enzyme', 'protein', 'digestion', 'blood', 
                                           'heart', 'nerve', 'brain', 'organ']):
        return GOLDEN_EXAMPLE_RESPIRATION  # Biology → Respiration template
    
    elif any(kw in topic_lower for kw in ['physics', 'motion', 'force', 'wave', 'oscillat', 
                                           'pendulum', 'space', 'astronomy', 'energy', 
                                           'electric', 'magnet', 'circuit', 'light']):
        return GOLDEN_EXAMPLE_FUSION  # Physics → Fusion template
    
    elif any(kw in topic_lower for kw in ['chemistry', 'bond', 'molecule', 'atom', 'reaction', 
                                           'ionic', 'covalent', 'acid', 'base', 'ph', 
                                           'oxidation', 'reduction', 'electrolysis']):
        return GOLDEN_EXAMPLE_FUSION  # Chemistry → Fusion template
    
    elif any(kw in topic_lower for kw in ['math', 'quadrat', 'function', 'graph', 'equation', 
                                           'calculus', 'trigonometry', 'algebra', 'geometry']):
        return EXAMPLE_MATH_QUADRATIC
    
    else:
        return GOLDEN_EXAMPLE_VACCINE  # Default to newest high-quality example
