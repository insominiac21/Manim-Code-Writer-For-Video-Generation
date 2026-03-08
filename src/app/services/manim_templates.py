"""
MentorBoxAI - Manim Code Templates
Pre-built, tested templates for common educational visualizations.
Inspired by: https://github.com/rohitg00/manim-video-generator

These templates ensure consistent, high-quality animations for common topics.
"""

import random
import textwrap
from typing import Optional, Dict, Callable

# ===========================================
# Template Mappings
# ===========================================
TEMPLATE_KEYWORDS = {
    "pythagorean": ["pythagoras", "pythagorean", "right triangle", "hypotenuse", "a^2 + b^2"],
    "quadratic": ["quadratic", "parabola", "x squared", "x^2", "polynomial"],
    "derivative": ["derivative", "differentiation", "slope", "rate of change", "tangent line"],
    "integral": ["integration", "integral", "area under curve", "antiderivative"],
    "trigonometry": ["sine", "cosine", "trigonometry", "trig", "unit circle", "sin", "cos"],
    "gravity": ["gravity", "gravitational", "falling", "projectile", "free fall"],
    "newton": ["newton", "force", "mass", "acceleration", "f=ma", "motion"],
    "dna": ["dna", "replication", "helicase", "double helix", "nucleotide"],
    "photosynthesis": ["photosynthesis", "chloroplast", "light reaction", "plant energy"],
    "cell_division": ["mitosis", "meiosis", "cell division", "chromosome"],
    "wave": ["wave", "frequency", "amplitude", "wavelength", "oscillation"],
    "electric_circuit": ["circuit", "voltage", "current", "resistance", "ohm"],
    "chemical_bond": ["chemical bond", "ionic", "covalent", "electronegativity", "electron sharing", "bonding"],
}


def calculate_match_score(concept: str, keywords: list) -> float:
    """Calculate how well a concept matches template keywords."""
    lower_concept = concept.lower().strip()
    words = lower_concept.split()
    
    matched = 0
    for keyword in keywords:
        if keyword in lower_concept:
            matched += 1
    
    if not keywords:
        return 0.0
    
    return matched / len(keywords)


def select_template(concept: str) -> Optional[str]:
    """
    Select appropriate template based on concept.
    Returns template name if match score > 0.5, else None.
    """
    best_score = 0.0
    best_template = None
    
    # Direct match check
    if concept.lower() in TEMPLATE_KEYWORDS:
        return concept.lower()

    for template_name, keywords in TEMPLATE_KEYWORDS.items():
        score = calculate_match_score(concept, keywords)
        if score > best_score:
            best_score = score
            best_template = template_name
    
    # Lower threshold to catch any single keyword match
    if best_score > 0.0:
        return best_template
    return None


# ===========================================
# Template Generators
# ===========================================


# ===========================================
# MASTER TEMPLATE HEADER (Vibrant Style)
# ===========================================
MASTER_TEMPLATE_HEADER = '''from manim import *
import random
import numpy as np
import textwrap

# ==========================================
# COLOR PALETTE
# ==========================================
class Colors:
    DARK_BG = "#0f0f2e"  # Dark blue-purple background
    CYAN = "#00FFFF"
    HOT_PINK = "#FF69B4"
    BRIGHT_YELLOW = "#FFD700"
    NEON_GREEN = "#39FF14"
    ORANGE = "#FF8C00"
    PURPLE = "#9D00FF"
    GOLD = "#FFD700"
    WHITE = "#FFFFFF"
    
    # Semantic colors
    LIGHT = BRIGHT_YELLOW
    ENERGY = ORANGE
    MOLECULE = NEON_GREEN
    ELECTRON = CYAN
    TEXT = WHITE
    IMPORTANT = GOLD
    
    # Standard Manim Aliases (Safe-guard against AI hallucinations)
    # The AI often writes Colors.YELLOW even if we didn't define it.
    # Map them to our palette or standard Manim colors.
    YELLOW = BRIGHT_YELLOW
    RED = "#FF0000"
    GREEN = NEON_GREEN
    BLUE = "#0000FF"
    TEAL = "#008080"
    PINK = HOT_PINK
    GRAY = "#808080"
    BLACK = "#000000"
    LT_GRAY = "#CCCCCC"

# Global Color Aliases (Safe-guard against NameError)
CYAN = Colors.CYAN
HOT_PINK = Colors.HOT_PINK
BRIGHT_YELLOW = Colors.BRIGHT_YELLOW
NEON_GREEN = Colors.NEON_GREEN
ORANGE = Colors.ORANGE
PURPLE = Colors.PURPLE
GOLD = Colors.GOLD
WHITE = Colors.WHITE
YELLOW = Colors.YELLOW
RED = Colors.RED
GREEN = Colors.GREEN
BLUE = Colors.BLUE
TEAL = Colors.TEAL
PINK = Colors.PINK
GRAY = Colors.GRAY
BLACK = Colors.BLACK
LT_GRAY = Colors.LT_GRAY

# ==========================================
# MASTER TEMPLATE SCENE
# ==========================================
class ColorfulScene(Scene):
    """
    Base class with colorful styling, fixed caption positioning,
    and fun animation helpers.
    """
    def setup(self):
        self.camera.background_color = Colors.DARK_BG
        self.captions = VGroup()
        self.title = VGroup()   # so FadeOut(self.title) never crashes
        self.add_background_particles()

    def add_background_particles(self):
        """Rich deep-space starfield with drifting nebula particles."""
        # --- Static distant stars (60 tiny dots, varied brightness) ---
        star_colors = [Colors.WHITE, Colors.LT_GRAY, Colors.CYAN, "#FFE4B5", "#AACCFF"]
        for _ in range(60):
            star = Dot(radius=random.uniform(0.008, 0.032),
                       color=random.choice(star_colors))
            star.move_to(np.array([
                random.uniform(-7.2, 7.2),
                random.uniform(-4.2, 4.2), 0]))
            star.set_opacity(random.uniform(0.10, 0.65))
            self.add(star)

        # --- Drifting nebula particles (20 larger, slowly moving) ---
        drift_colors = [Colors.CYAN, Colors.PURPLE, Colors.HOT_PINK, "#5555FF"]
        for _ in range(20):
            d = Dot(radius=random.uniform(0.025, 0.060),
                    color=random.choice(drift_colors))
            d.move_to(np.array([
                random.uniform(-7, 7),
                random.uniform(-4, 4), 0]))
            d.set_opacity(random.uniform(0.06, 0.18))
            d.velocity = np.array([
                random.uniform(-0.04, 0.04),
                random.uniform(-0.03, 0.03), 0])
            def _drift(mob, dt):
                mob.shift(mob.velocity * dt)
                if mob.get_x() > 7.5:  mob.set_x(-7.5)
                if mob.get_x() < -7.5: mob.set_x(7.5)
                if mob.get_y() > 4.5:  mob.set_y(-4.5)
                if mob.get_y() < -4.5: mob.set_y(4.5)
            d.add_updater(_drift)
            self.add(d)

        # --- Twinkling bright accent stars (5, pulsing opacity) ---
        for _ in range(5):
            bright = Dot(radius=random.uniform(0.04, 0.08), color=Colors.WHITE)
            bright.move_to(np.array([
                random.uniform(-6, 6),
                random.uniform(-3.5, 3.5), 0]))
            bright.t_offset = random.uniform(0, 6.28)
            bright.t = 0.0
            def _twinkle(mob, dt):
                mob.t += dt
                mob.set_opacity(0.25 + 0.30 * np.sin(mob.t * 1.8 + mob.t_offset))
            bright.add_updater(_twinkle)
            self.add(bright)

    def create_caption(self, text_str, font_size=20, color=Colors.WHITE, position=DOWN):
        """
        Create a caption for educational explanations.
        NEET-focused: Clear, readable, properly bounded.
        """
        # Word-wrap at 50 chars. textwrap.fill never breaks mid-word.
        # No line cap — all content must show; create_caption scales down if needed.
        wrapped_text = textwrap.fill(str(text_str), width=50)
        
        # Create caption with clear font
        caption = Text(wrapped_text, font_size=font_size, color=color, font="Arial", line_spacing=0.9)
        
        # CRITICAL: Scale down if too wide (max 13 units width)
        if caption.width > 13:
            caption.scale(13 / caption.width)
        
        # Add background box for readability
        bg = SurroundingRectangle(caption, color=Colors.DARK_BG, fill_color=Colors.DARK_BG, fill_opacity=0.92, buff=0.12)
        bg.set_stroke(Colors.CYAN, 1)
        caption_group = VGroup(bg, caption)
        
        # Position at bottom with safe margin
        caption_group.to_edge(DOWN, buff=0.25)
        
        # SAFETY: Ensure it's within horizontal bounds
        if caption_group.get_left()[0] < -6.8:
            caption_group.shift(RIGHT * (-6.8 - caption_group.get_left()[0]))
        if caption_group.get_right()[0] > 6.8:
            caption_group.shift(LEFT * (caption_group.get_right()[0] - 6.8))
            
        return caption_group

    def play_caption(self, text_str, duration=2.0):
        """
        Play a caption with smooth transition. Duration slightly longer for reading.
        """
        new_caption = self.create_caption(text_str)
        
        anims = [FadeIn(new_caption, shift=UP * 0.15)]
        
        # Fade out previous captions
        if self.captions:
            anims.append(FadeOut(self.captions, shift=UP * 0.15))
            
        self.play(*anims, run_time=0.4)
        self.captions = new_caption
        self.wait(duration)

    def show_title(self, text_str):
        """Show a professional title - NEET/JEE academic style."""
        # STRICT: Truncate to 25 chars MAX to prevent overflow
        title_text = str(text_str)[:25]
        
        title = Text(title_text, font_size=36, font="Arial", weight=BOLD)
        title.set_color_by_gradient(Colors.CYAN, Colors.GOLD)  # More professional gradient
        
        # CRITICAL: Scale down aggressively if still too wide
        if title.width > 10:
            title.scale(10 / title.width)
        
        # Scale down if too wide
        if title.width > 13:
            title.scale(13 / title.width)
        
        title.to_edge(UP, buff=0.4)
        
        # Add decorative line - thinner, more elegant
        line = Line(LEFT * min(5, title.width/2 + 0.3), RIGHT * min(5, title.width/2 + 0.3), color=Colors.GOLD)
        line.set_stroke(width=2)
        line.next_to(title, DOWN, buff=0.15)
        
        self.play(Write(title), GrowFromCenter(line), run_time=1)
        self.wait(0.3)
        title_group = VGroup(title, line)
        self.title = title_group   # store so generated code can do FadeOut(self.title)
        return title_group

    def add_fun_pulse(self, mobject, color=Colors.HOT_PINK, scale_factor=1.15):
        """Standard pulse scaling effect - SMALLER scale to avoid overflow."""
        self.play(
            mobject.animate.scale(scale_factor).set_color(color),
            rate_func=there_and_back,
            run_time=0.4
        )

    def add_glow_pulse(self, mobject, color=Colors.CYAN):
        """A richer pulsing effect that adds a temporary glow."""
        glow = mobject.copy().set_color(color).set_opacity(0.4).scale(1.2)
        self.add(glow)
        self.play(
            mobject.animate.scale(1.1).set_color(color),
            glow.animate.scale(1.4).set_opacity(0),
            run_time=0.8,
            rate_func=rush_from
        )
        self.remove(glow)
        self.play(mobject.animate.scale(1/1.1).set_color(mobject.get_color()), run_time=0.2)

    def add_wiggle_effect(self, mobject, scale_value=1.1, rotation_angle=0.1):
        """Adds a high-energy wiggle/vibration effect (good for excitation)."""
        self.play(
            Wiggle(mobject, scale_value=scale_value, rotation_angle=rotation_angle),
            run_time=0.6
        )

    # ═══════════════════════════════════════════════════════════
    # LAYOUT HELPERS — Prevent text/object overlap
    # ═══════════════════════════════════════════════════════════

    def clamp_to_screen(self, mob, x_margin=0.5, y_margin=0.4):
        """Shift mob so it stays within screen bounds. Returns mob."""
        xl, xr = -7.1 + x_margin, 7.1 - x_margin
        yb, yt = -4.0 + y_margin, 4.0 - y_margin
        if mob.get_left()[0] < xl:   mob.shift(RIGHT * (xl - mob.get_left()[0]))
        if mob.get_right()[0] > xr:  mob.shift(LEFT  * (mob.get_right()[0] - xr))
        if mob.get_bottom()[1] < yb: mob.shift(UP    * (yb - mob.get_bottom()[1]))
        if mob.get_top()[1] > yt:    mob.shift(DOWN  * (mob.get_top()[1] - yt))
        if mob.width > 13.0:  mob.scale(13.0 / mob.width)
        if mob.height > 7.0:  mob.scale(7.0  / mob.height)
        return mob

    def safe_next_to(self, mob, anchor, direction=DOWN, buff=0.4):
        """next_to + clamp. Always use instead of raw .next_to for labels."""
        mob.next_to(anchor, direction, buff=buff)
        return self.clamp_to_screen(mob)

    def arrange_column(self, *mobjects, start_y=1.5, spacing=0.65, center_x=0.0):
        """
        Place mobjects in a vertical column, top-down from start_y.
        Guarantees no vertical overlap. Returns VGroup.
        group = self.arrange_column(label1, label2, label3, start_y=1.8)
        """
        mobs = list(mobjects)
        y = start_y
        for i, mob in enumerate(mobs):
            mob.move_to([center_x, y, 0])
            self.clamp_to_screen(mob)
            if i + 1 < len(mobs):
                y -= mob.height / 2 + spacing + mobs[i + 1].height / 2
        return VGroup(*mobs)

    def stack_labels(self, labels, anchor_obj, direction=DOWN, buff=0.35, spacing=0.35):
        """
        Stack a list of Text/VGroup labels below (or above) anchor_obj,
        each spaced by `spacing`. Clamps each to screen.
        Returns VGroup of labels.
        """
        group = VGroup()
        prev = anchor_obj
        for lbl in labels:
            lbl.next_to(prev, direction, buff=buff if prev is anchor_obj else spacing)
            self.clamp_to_screen(lbl)
            group.add(lbl)
            prev = lbl
        return group

    def create_labeled_shape(self, shape, label_text, label_direction=DOWN, buff=0.3):
        """
        Create a shape with a properly positioned label that won't overlap.
        CRITICAL: Always use this for labeled objects to prevent overlap!
        
        Args:
            shape: The Manim object (Circle, Ellipse, etc.)
            label_text: Text for the label
            label_direction: Where to place label (DOWN, UP, LEFT, RIGHT)
            buff: Spacing between shape and label
        
        Returns:
            VGroup containing shape and label
        """
        label = Text(str(label_text)[:25], font_size=18, color=Colors.BRIGHT_YELLOW, font="Arial")
        
        # Scale label if too wide
        if label.width > 3:
            label.scale(3 / label.width)
        
        label.next_to(shape, label_direction, buff=buff)
        
        # Ensure label stays on screen
        if label.get_left()[0] < -6:
            label.shift(RIGHT * (-6 - label.get_left()[0]))
        if label.get_right()[0] > 6:
            label.shift(LEFT * (label.get_right()[0] - 6))
        if label.get_top()[1] > 3.5:
            label.shift(DOWN * (label.get_top()[1] - 3.5))
        if label.get_bottom()[1] < -3.5:
            label.shift(UP * (-3.5 - label.get_bottom()[1]))
        
        return VGroup(shape, label)

    def connect_with_beam(self, obj1, obj2, color=Colors.CYAN):
        """Creates a beam/line connecting two objects."""
        if isinstance(obj1, VGroup): start = obj1.get_center()
        else: start = obj1.get_center()
        
        if isinstance(obj2, VGroup): end = obj2.get_center()
        else: end = obj2.get_center()
        
        return Line(start, end, color=color).set_stroke(width=3)

    # ═══════════════════════════════════════════════════════════
    # NEET/JEE EDUCATIONAL HELPERS
    # ═══════════════════════════════════════════════════════════

    def show_intro(self, title_str, learning_objective):
        """
        Show introduction scene - MANDATORY for every video.
        Returns title_group for later FadeOut.
        """
        title_group = self.show_title(title_str)
        self.play_caption(f"In this video: {learning_objective}", duration=2)
        return title_group

    def show_takeaway(self, key_point, exam_tip=None):
        """
        Show takeaway/conclusion scene - MANDATORY for every video.
        """
        # Clear screen first
        self.play(FadeOut(*self.mobjects), run_time=0.5)
        
        # Show key point
        point = self.show_key_point(key_point)
        self.play(GrowFromCenter(point), run_time=0.8)
        self.wait(1.5)
        
        if exam_tip:
            self.play_caption(f"Exam Tip: {exam_tip}", duration=2)
        else:
            self.wait(1)

    def create_labeled_diagram(self, shapes_and_labels, arrangement="horizontal", spacing=2.5):
        """
        Create multiple labeled shapes arranged properly.
        
        Args:
            shapes_and_labels: List of tuples (shape_type, label, color)
                              e.g., [("circle", "Nucleus", Colors.CYAN), ("ellipse", "Cell", Colors.GREEN)]
            arrangement: "horizontal" or "vertical"
            spacing: Space between objects
        
        Returns:
            VGroup of all labeled objects
        """
        objects = VGroup()
        
        for i, (shape_type, label, color) in enumerate(shapes_and_labels):
            obj = self.create_labeled_object(shape_type, label, ORIGIN, color, size=0.8)
            objects.add(obj)
        
        # Arrange
        if arrangement == "horizontal":
            objects.arrange(RIGHT, buff=spacing)
        else:
            objects.arrange(DOWN, buff=spacing)
        
        # Ensure stays on screen
        if objects.width > 12:
            objects.scale(12 / objects.width)
        if objects.height > 5:
            objects.scale(5 / objects.height)
        
        objects.move_to(ORIGIN)
        return objects

    def animate_process(self, reactants, products, arrow_label=""):
        """
        Animate a simple reaction: Reactants → Products
        Both reactants and products should be VGroups or Mobjects.
        """
        # Position reactants left, products right
        reactants.move_to(LEFT * 3)
        products.move_to(RIGHT * 3)
        
        # Show reactants
        self.play(FadeIn(reactants), run_time=0.8)
        self.wait(0.5)
        
        # Arrow
        arrow = self.create_reaction_arrow(LEFT * 1, RIGHT * 1, arrow_label)
        self.play(Create(arrow), run_time=0.5)
        
        # Transform to products
        self.play(
            ReplacementTransform(reactants.copy(), products),
            run_time=1
        )
        self.wait(0.5)
        
        return VGroup(reactants, arrow, products)


    def setup_gradient_header(self, text, subtitle=None):
        """Creates a vibrant gradient header with optional subtitle - BOUNDED."""
        header_group = VGroup()
        
        # Truncate if too long
        title_text = str(text)[:35]
        
        # Main Title
        title = Text(title_text, font_size=36, font="Arial", weight=BOLD)
        title.set_color_by_gradient(Colors.CYAN, Colors.PURPLE, Colors.HOT_PINK)
        
        # Scale down if too wide
        if title.width > 11:
            title.scale(11 / title.width)
        
        title.to_edge(UP, buff=0.5)
        header_group.add(title)
        
        # Subtitle
        if subtitle:
            sub_text = str(subtitle)[:50]
            sub = Text(sub_text, font_size=20, color=Colors.LT_GRAY, font="Arial")
            if sub.width > 10:
                sub.scale(10 / sub.width)
            sub.next_to(title, DOWN, buff=0.2)
            header_group.add(sub)
        
        # Glow effect behind
        glow = title.copy().set_color(Colors.PURPLE).set_opacity(0.3).scale(1.05)
        self.add(glow)
        header_group.add(glow)
        
        return header_group

    def create_glowing_text(self, text, font_size=22, color=Colors.WHITE):
        """Creates text with a faint glow behind it - BOUNDED to screen."""
        # Truncate long text
        text_str = str(text)[:30]
        
        main_text = Text(text_str, font_size=font_size, color=color, font="Arial")
        
        # Scale down if too wide
        if main_text.width > 6:
            main_text.scale(6 / main_text.width)
        
        glow = main_text.copy().set_color(color).set_opacity(0.3).scale(1.1)
        
        # Add background box for readability
        bg = SurroundingRectangle(main_text, color=Colors.DARK_BG, fill_color=Colors.DARK_BG, fill_opacity=0.85, buff=0.08)
        bg.set_stroke(width=0)
        
        return VGroup(bg, glow, main_text)

    def create_glowing_object(self, mobject, color=None):
        """Adds a glowing effect to any object."""
        if color is None: color = mobject.get_color()
        glow = mobject.copy().set_color(color).set_opacity(0.6)
        glow.set_stroke(color, width=8, opacity=0.5)
        return VGroup(glow, mobject)

    def create_labeled_object(self, shape_type, label, position, color=Colors.NEON_GREEN, size=1.0):
        """Create shape with label BELOW - for educational diagrams."""
        if shape_type == "circle":
            shape = Circle(radius=size, color=color, fill_opacity=0.3)
        elif shape_type == "rectangle":
            shape = Rectangle(width=size*2, height=size, color=color, fill_opacity=0.3)
        elif shape_type == "ellipse":
            shape = Ellipse(width=size*2, height=size, color=color, fill_opacity=0.3)
        else:
            shape = Dot(radius=size, color=color)
        
        shape.set_stroke(color, width=2)
        shape.move_to(position)
        
        # Label ALWAYS below with proper spacing
        label_text = str(label)[:20]  # Truncate long labels
        label_obj = Text(label_text, font_size=18, color=Colors.BRIGHT_YELLOW, font="Arial")
        label_obj.next_to(shape, DOWN, buff=0.25)
        
        # Ensure label stays on screen
        if label_obj.get_bottom()[1] < -3.5:
            label_obj.next_to(shape, UP, buff=0.25)  # Move above if too low
        
        group = VGroup(shape, label_obj)
        return group

    def create_equation(self, equation_str, color=Colors.WHITE, font_size=24):
        """Create a properly formatted equation for NEET/JEE content."""
        eq = Text(equation_str, font_size=font_size, color=color, font="Arial")
        
        # Scale if too wide
        if eq.width > 10:
            eq.scale(10 / eq.width)
        
        return eq

    def show_key_point(self, text_str, color=Colors.GOLD):
        """Display a key takeaway point - for exam tips."""
        # Format as "Key Point: ..."
        full_text = f"Key Point: {text_str}"[:60]
        
        point = Text(full_text, font_size=22, color=color, font="Arial", weight=BOLD)
        
        if point.width > 12:
            point.scale(12 / point.width)
        
        # Add highlight box
        box = SurroundingRectangle(point, color=Colors.GOLD, fill_color=Colors.DARK_BG, 
                                   fill_opacity=0.9, buff=0.2, corner_radius=0.1)
        
        group = VGroup(box, point)
        group.move_to(ORIGIN)
        
        return group

    def create_reaction_arrow(self, start_pos, end_pos, label_text="", color=Colors.WHITE):
        """Create a labeled reaction arrow (A → B style)."""
        arrow = Arrow(start_pos, end_pos, color=color, buff=0.1)
        arrow.set_stroke(width=3)
        
        if label_text:
            label = Text(str(label_text)[:15], font_size=16, color=Colors.BRIGHT_YELLOW, font="Arial")
            label.next_to(arrow, UP, buff=0.1)
            return VGroup(arrow, label)
        
        return arrow

    def create_particle_group(self, num_particles=15, radius=0.3, color=Colors.CYAN):
        """Create a VGroup of particles for molecular/cloud effects. Safe screen bounds."""
        particles = VGroup()
        for _ in range(num_particles):
            dot = Dot(radius=random.uniform(0.03, 0.09), color=color)
            dot.set_opacity(random.uniform(0.4, 0.85))
            dot.move_to([
                random.uniform(-5.0, 5.0),
                random.uniform(-2.8, 2.8), 0])
            particles.add(dot)
        return particles

    def animate_particles_movement(self, particles, duration=3):
        """Animate particles drifting to new random safe positions (physics simulation)."""
        animations = []
        for particle in particles:
            new_pos = [
                random.uniform(-5.0, 5.0),
                random.uniform(-2.8, 2.8), 0]
            animations.append(particle.animate.move_to(new_pos))
        self.play(*animations, run_time=duration)

    # ═══════════════════════════════════════════════════════════
    # MATHEMATICAL / PHYSICS ANIMATION HELPERS
    # ═══════════════════════════════════════════════════════════

    def phasor_to_sine_animation(self, n_cycles=2, run_time=6,
                                  circle_center=None, radius=1.0):
        """
        3Blue1Brown-style: rotating phasor circle on LEFT traces sine wave on RIGHT.
        The dot on the circle casts a 'shadow' that draws the sine curve in real time.

        Usage:
            group = self.phasor_to_sine_animation(n_cycles=2, run_time=6)
            self.wait(1)
            self.play(FadeOut(group))
        """
        if circle_center is None:
            circle_center = np.array([-3.5, 0.0, 0.0])
        else:
            circle_center = np.array(circle_center)

        total_angle = n_cycles * 2 * np.pi
        # x_scale maps angle (radians) to horizontal screen units
        wave_x_start = circle_center[0] + radius + 0.6
        wave_width = 5.5  # screen units for full 2 cycles
        x_scale = wave_width / total_angle

        # --- Static elements ---
        circle = Circle(radius=radius, color=Colors.CYAN, stroke_width=2)
        circle.move_to(circle_center)
        center_dot = Dot(circle_center, radius=0.05, color=Colors.WHITE)

        # Horizontal axis for the wave
        x_axis = Arrow(
            np.array([wave_x_start, circle_center[1], 0]),
            np.array([wave_x_start + wave_width + 0.3, circle_center[1], 0]),
            color=Colors.LT_GRAY, stroke_width=2, buff=0, tip_length=0.18
        )
        # Amplitude guide lines
        amp_top = DashedLine(
            np.array([wave_x_start - 0.2, circle_center[1] + radius, 0]),
            np.array([wave_x_start + wave_width, circle_center[1] + radius, 0]),
            color=Colors.GRAY, stroke_width=1, stroke_opacity=0.4
        )
        amp_bot = DashedLine(
            np.array([wave_x_start - 0.2, circle_center[1] - radius, 0]),
            np.array([wave_x_start + wave_width, circle_center[1] - radius, 0]),
            color=Colors.GRAY, stroke_width=1, stroke_opacity=0.4
        )

        self.play(
            Create(circle), FadeIn(center_dot),
            Create(x_axis), Create(amp_top), Create(amp_bot),
            run_time=1.0
        )

        # --- ValueTracker drives everything ---
        t = ValueTracker(0.001)  # start just above 0 to avoid empty range

        # Phasor arm (line from center to dot on circle)
        phasor_arm = always_redraw(lambda: Line(
            circle_center,
            circle_center + np.array([
                radius * np.cos(t.get_value()),
                radius * np.sin(t.get_value()), 0]),
            color=Colors.GOLD, stroke_width=3
        ))

        # Phasor dot (bright dot on circle edge)
        phasor_dot = always_redraw(lambda: Dot(
            circle_center + np.array([
                radius * np.cos(t.get_value()),
                radius * np.sin(t.get_value()), 0]),
            radius=0.12, color=Colors.GOLD
        ))

        # Connecting dashed line: phasor dot → point on sine wave
        connector = always_redraw(lambda: DashedLine(
            circle_center + np.array([
                radius * np.cos(t.get_value()),
                radius * np.sin(t.get_value()), 0]),
            np.array([
                wave_x_start + t.get_value() * x_scale,
                circle_center[1] + radius * np.sin(t.get_value()), 0]),
            color=Colors.GRAY, stroke_width=1.5, stroke_opacity=0.55
        ))

        # Traced sine curve: ParametricFunction rebuilt each frame up to t
        sine_trace = always_redraw(lambda: ParametricFunction(
            lambda s: np.array([
                wave_x_start + s * x_scale,
                circle_center[1] + radius * np.sin(s), 0
            ]),
            t_range=[0, max(0.001, t.get_value())],
            color=Colors.HOT_PINK,
            stroke_width=3
        ))

        # Current wave-front dot
        wave_dot = always_redraw(lambda: Dot(
            np.array([
                wave_x_start + t.get_value() * x_scale,
                circle_center[1] + radius * np.sin(t.get_value()), 0]),
            radius=0.09, color=Colors.HOT_PINK
        ))

        self.add(phasor_arm, phasor_dot, sine_trace, connector, wave_dot)
        self.play(
            t.animate.set_value(total_angle),
            run_time=run_time, rate_func=linear
        )
        self.remove(connector)  # clean up updater objects before FadeOut

        return VGroup(circle, center_dot, x_axis, amp_top, amp_bot,
                      phasor_arm, phasor_dot, sine_trace, wave_dot)

    def static_sine_wave(self, amplitude=1.0, frequency=1.0, phase=0.0,
                          x_range=None, color=None, label_text=""):
        """
        Draw a static sine wave with optional label.
        For animation use phasor_to_sine_animation instead.

        Usage:
            wave = self.static_sine_wave(amplitude=1.2, label_text="y = A sin(ωt)")
            self.play(Create(wave))
        """
        if x_range is None:
            x_range = [-5, 5]
        if color is None:
            color = Colors.HOT_PINK
        wave = FunctionGraph(
            lambda x: amplitude * np.sin(frequency * x + phase),
            x_range=x_range, color=color, stroke_width=3
        )
        if label_text:
            lbl = Text(str(label_text)[:30], font_size=16,
                       color=Colors.BRIGHT_YELLOW, font="Arial")
            self.safe_next_to(lbl, wave, UP, buff=0.25)
            return VGroup(wave, lbl)
        return wave

    def add_collision_effect(self, obj1, obj2, color=Colors.HOT_PINK):
        """Create collision/interaction between two objects showing reaction."""
        self.play(
            obj1.animate.set_color(color).scale(1.2),
            obj2.animate.set_color(color).scale(1.2),
            run_time=0.5
        )
        self.wait(0.3)
        self.play(
            obj1.animate.set_color(Colors.NEON_GREEN).scale(1/1.2),
            obj2.animate.set_color(Colors.ORANGE).scale(1/1.2),
            run_time=0.5
        )

    def collision_burst(self, obj1, obj2, burst_color=Colors.GOLD):
        """
        CINEMATIC collision: objects smash → Flash at midpoint → concentric rings → recolor.
        Use for nuclear fusion, ionic bonding, chemical reactions.
        Call AFTER moving obj1 and obj2 close together.
        """
        mid = (obj1.get_center() + obj2.get_center()) / 2
        # Impact glow burst
        self.play(
            obj1.animate.set_color(burst_color).scale(1.3),
            obj2.animate.set_color(burst_color).scale(1.3),
            run_time=0.25
        )
        self.play(Flash(mid, color=burst_color, line_length=0.8, num_lines=18, flash_radius=0.5))
        # Concentric shock rings
        rings = VGroup(*[
            Circle(radius=0.2 + i * 0.28, color=burst_color,
                   stroke_opacity=max(0.05, 0.7 - i * 0.22))
            .move_to(mid) for i in range(5)
        ])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), run_time=0.6)
        self.play(FadeOut(rings), run_time=0.3)
        # Settle to product colors
        self.play(
            obj1.animate.set_color(Colors.NEON_GREEN).scale(1/1.3),
            obj2.animate.set_color(Colors.ORANGE).scale(1/1.3),
            run_time=0.4
        )

    def add_transformation_arrow(self, start_obj, end_obj, label_text="", color=Colors.CYAN):
        """Draw arrow showing transformation/reaction."""
        arrow = Arrow(start_obj.get_right(), end_obj.get_left(), color=color, buff=0.3)
        self.play(Create(arrow))
        if label_text:
            label = Text(label_text, font_size=18, color=Colors.BRIGHT_YELLOW, font="Arial")
            label.next_to(arrow, UP, buff=0.2)
            self.play(Write(label))
            self.wait(1)
            return VGroup(arrow, label)
        self.wait(1)
        return arrow

    def show_energy_diagram(self, values, labels, title_text):
        """Show bar chart of energy levels or comparison. Handles any number of bars safely."""
        n = len(values)
        max_val = max(values) if values else 1
        bar_width = min(0.9, 9.0 / max(n, 1) - 0.2)
        spacing = min(2.0, 10.0 / max(n, 1))
        start_x = -(n - 1) * spacing / 2

        bars = VGroup()
        for i, (val, label) in enumerate(zip(values, labels)):
            height = max(0.15, val / max_val * 2.8)
            bar = Rectangle(width=bar_width, height=height,
                            color=Colors.ORANGE, fill_opacity=0.7)
            bar.move_to([start_x + i * spacing, height / 2 - 1.5, 0])
            bar.set_stroke(Colors.GOLD, width=1.5)
            label_obj = Text(str(label)[:12], font_size=14, color=Colors.BRIGHT_YELLOW, font="Arial")
            label_obj.next_to(bar, DOWN, buff=0.15)
            value_obj = Text(str(val), font_size=13, color=Colors.GOLD)
            value_obj.next_to(bar, UP, buff=0.1)
            bars.add(bar, label_obj, value_obj)

        title = Text(str(title_text)[:30], font_size=22, color=Colors.CYAN, font="Arial")
        title.to_edge(UP, buff=0.5)
        if title.width > 12: title.scale(12 / title.width)

        self.play(Write(title))
        self.play(LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.15), run_time=1.5)
        self.wait(1.5)
        return VGroup(title, bars)

    def show_title(self, text_str):
        """
        Show a title with vibrant gradient or color.
        STRICT: Max 25 characters to prevent overflow!
        """
        # Truncate to 25 chars
        title_text = str(text_str)[:25]
        
        title = Text(title_text, font_size=36, font="Arial", weight=BOLD)
        title.set_color_by_gradient(Colors.CYAN, Colors.PURPLE)
        
        # Scale if too wide
        if title.width > 10:
            title.scale(10 / title.width)
            
        title.to_edge(UP, buff=0.5)
        
        # Add decorative line - sized to title
        line = Line(LEFT * min(4, title.width/2 + 0.3), RIGHT * min(4, title.width/2 + 0.3), color=Colors.HOT_PINK)
        line.next_to(title, DOWN, buff=0.2)
        
        self.play(Write(title), GrowFromCenter(line))
        self.wait(1)
        return VGroup(title, line)
'''

# ============================================================
# MODULE-LEVEL exec: make Colors, ColorfulScene, and all
# color aliases importable from this module.
# MASTER_TEMPLATE_HEADER is a self-contained Python script;
# exec-ing it populates globals() with Colors and ColorfulScene.
# ============================================================
try:
    exec(MASTER_TEMPLATE_HEADER, globals())  # type: ignore[arg-type]
except Exception as _e:
    # Fallback if manim is not installed (e.g. CI, server startup)
    class Colors:  # type: ignore
        DARK_BG = "#0f0f2e"
        CYAN = "#00FFFF"
        HOT_PINK = "#FF69B4"
        BRIGHT_YELLOW = "#FFD700"
        NEON_GREEN = "#39FF14"
        ORANGE = "#FF8C00"
        PURPLE = "#9D00FF"
        GOLD = "#FFD700"
        WHITE = "#FFFFFF"
        YELLOW = BRIGHT_YELLOW
        RED = "#FF0000"
        GREEN = NEON_GREEN
        BLUE = "#0000FF"
        TEAL = "#008080"
        PINK = HOT_PINK
        GRAY = "#808080"
        BLACK = "#000000"
        LT_GRAY = "#CCCCCC"

    class ColorfulScene:  # type: ignore
        pass

# ===========================================
# Template Generators
# ===========================================

def generate_pythagorean() -> str:
    """Pythagorean theorem visualization."""
    return '''from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # ═══════════════════════════════════════
        # SCENE 1: Title
        # ═══════════════════════════════════════
        title = Text("Pythagorean Theorem", font_size=44, color=WHITE)
        title.to_edge(UP)
        subtitle = Text("a² + b² = c²", font_size=32, color=TEAL)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # ═══════════════════════════════════════
        # SCENE 2: Right Triangle
        # ═══════════════════════════════════════
        scene_title = Text("The Right Triangle", font_size=36, color=TEAL)
        scene_title.to_edge(UP)
        
        # Create triangle
        triangle = Polygon(
            ORIGIN, RIGHT * 3, RIGHT * 3 + UP * 4,
            color=WHITE, fill_opacity=0.1
        )
        triangle.move_to(ORIGIN)
        
        # Labels
        a_label = Text("a = 3", font_size=24, color=BLUE)
        a_label.next_to(triangle, DOWN, buff=0.3)
        
        b_label = Text("b = 4", font_size=24, color=GREEN)
        b_label.next_to(triangle, RIGHT, buff=0.3)
        
        c_label = Text("c = ?", font_size=24, color=RED)
        c_label.next_to(triangle.get_center(), UP + LEFT, buff=0.3)
        
        explanation = Text("Find the hypotenuse (c)", font_size=26, color=GRAY)
        explanation.to_edge(DOWN)
        
        self.play(Write(scene_title))
        self.play(Create(triangle), run_time=1.5)
        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.play(FadeIn(explanation))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 3: Formula and Calculation
        # ═══════════════════════════════════════
        scene_title = Text("Applying the Formula", font_size=36, color=TEAL)
        scene_title.to_edge(UP)
        
        formula = Text("a^2 + b^2 = c^2", font_size=40)
        formula.move_to(UP * 1)
        
        step1 = Text("3^2 + 4^2 = c^2", font_size=36)
        step1.next_to(formula, DOWN, buff=0.5)
        
        step2 = Text("9 + 16 = c^2", font_size=36)
        step2.next_to(step1, DOWN, buff=0.3)
        
        step3 = Text("25 = c^2", font_size=36)
        step3.next_to(step2, DOWN, buff=0.3)
        
        step4 = Text("c = 5", font_size=40, color=GREEN)
        step4.next_to(step3, DOWN, buff=0.5)
        
        self.play(Write(scene_title))
        self.play(Write(formula))
        self.wait(1)
        self.play(Write(step1))
        self.wait(0.5)
        self.play(Write(step2))
        self.wait(0.5)
        self.play(Write(step3))
        self.wait(0.5)
        self.play(Write(step4))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 4: Summary
        # ═══════════════════════════════════════
        summary = Text("The hypotenuse c = 5", font_size=40, color=GREEN)
        summary.move_to(ORIGIN)
        
        self.play(Write(summary))
        self.wait(3)
'''


def generate_derivative() -> str:
    """Derivative/calculus visualization."""
    return '''from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # ═══════════════════════════════════════
        # SCENE 1: Title
        # ═══════════════════════════════════════
        title = Text("Understanding Derivatives", font_size=44, color=WHITE)
        title.to_edge(UP)
        subtitle = Text("The slope at any point", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # ═══════════════════════════════════════
        # SCENE 2: Function Graph
        # ═══════════════════════════════════════
        scene_title = Text("The Function f(x) = x²", font_size=36, color=TEAL)
        scene_title.to_edge(UP)
        
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 2],
            axis_config={"include_tip": True, "color": WHITE}
        ).scale(0.7)
        axes.move_to(ORIGIN)
        
        x_label = Text("x", font_size=22).next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("y", font_size=22).next_to(axes.y_axis.get_end(), UP)
        
        graph = axes.plot(lambda x: x**2, color=BLUE, x_range=[-2.5, 2.5])
        graph_label = Text("f(x) = x²", font_size=24, color=BLUE)
        graph_label.to_corner(UL).shift(DOWN * 1.5)
        
        explanation = Text("A parabola - the slope changes at every point", font_size=24)
        explanation.to_edge(DOWN)
        
        self.play(Write(scene_title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(graph), Write(graph_label))
        self.play(FadeIn(explanation))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 3: Tangent Line
        # ═══════════════════════════════════════
        scene_title = Text("The Tangent Line", font_size=36, color=TEAL)
        scene_title.to_edge(UP)
        
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 2],
            axis_config={"include_tip": True, "color": WHITE}
        ).scale(0.7)
        axes.move_to(ORIGIN)
        
        graph = axes.plot(lambda x: x**2, color=BLUE, x_range=[-2.5, 2.5])
        
        # Tangent at x=1
        x_val = 1
        tangent = axes.plot(lambda x: 2*x - 1, color=RED, x_range=[-0.5, 2.5])
        
        dot = Dot(axes.c2p(x_val, x_val**2), color=YELLOW)
        
        explanation = Text("At x=1, the slope (derivative) = 2", font_size=24)
        explanation.to_edge(DOWN)
        
        self.play(Write(scene_title))
        self.play(Create(axes), Create(graph))
        self.play(Create(dot))
        self.play(Create(tangent))
        self.play(FadeIn(explanation))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 4: Derivative Formula
        # ═══════════════════════════════════════
        scene_title = Text("The Derivative", font_size=36, color=TEAL)
        scene_title.to_edge(UP)
        
        original = Text("f(x) = x^2", font_size=40, color=BLUE)
        original.move_to(UP * 1)
        
        arrow = Arrow(UP * 0.5, DOWN * 0.5, color=WHITE)
        arrow.next_to(original, DOWN, buff=0.3)
        
        derivative = Text("f'(x) = 2x", font_size=40, color=GREEN)
        derivative.next_to(arrow, DOWN, buff=0.3)
        
        explanation = Text("The derivative gives the slope at any x", font_size=24)
        explanation.to_edge(DOWN)
        
        self.play(Write(scene_title))
        self.play(Write(original))
        self.play(GrowArrow(arrow))
        self.play(Write(derivative))
        self.play(FadeIn(explanation))
        self.wait(3)
'''


def generate_newton_laws() -> str:
    """Newton's Laws of Motion visualization (Color Template)."""
    return MASTER_TEMPLATE_HEADER + '''
class GeneratedScene(ColorfulScene):
    def construct(self):
        title_group = self.show_title("Newton's Laws")
        self.play(FadeOut(title_group))
        
        # --- FIRST LAW: INERTIA ---
        floor = Line(LEFT*6, RIGHT*6, color=Colors.WHITE).shift(DOWN*2)
        ball = Circle(radius=0.5, color=Colors.CYAN, fill_opacity=0.8).move_to(LEFT*4 + DOWN*1.5)
        
        self.play(Create(floor), Create(ball))
        self.play_caption("Law 1: Inertia. An object stays at rest...")
        self.wait(1)
        
        # Force application
        hand = Text("✋", font_size=40).next_to(ball, LEFT)
        self.play(FadeIn(hand, shift=RIGHT))
        self.play(hand.animate.shift(RIGHT*0.5), run_time=0.2)
        self.play(hand.animate.shift(LEFT*0.5), run_time=0.2)
        self.play(FadeOut(hand))
        
        # Ball moves
        self.play(ball.animate.shift(RIGHT*8), run_time=2, rate_func=linear)
        self.play_caption("...until acted upon by a force!")
        
        self.play(FadeOut(ball), FadeOut(floor))
        
        # --- SECOND LAW: F=ma ---
        f_txt = Text("F", font_size=72, color=Colors.HOT_PINK).move_to(LEFT*1.5)
        eq_txt = Text("=", font_size=72, color=Colors.WHITE).move_to(ORIGIN)
        m_txt = Text("m", font_size=72, color=Colors.CYAN).move_to(RIGHT*1.2)
        a_txt = Text("a", font_size=72, color=Colors.NEON_GREEN).move_to(RIGHT*2.4)
        formula = VGroup(f_txt, eq_txt, m_txt, a_txt)

        self.play(Write(formula))
        self.add_fun_pulse(f_txt)
        self.play_caption("Law 2: Force = Mass x Acceleration")

        # Demonstrate relationship
        self.play(
            f_txt.animate.scale(1.5),
            a_txt.animate.scale(1.5),
            run_time=1
        )
        self.play_caption("More Force = More Acceleration")
        self.wait(2)
'''


def generate_photosynthesis() -> str:
    """Photosynthesis process visualization (Color Template)."""
    return MASTER_TEMPLATE_HEADER + '''
class GeneratedScene(ColorfulScene):
    def construct(self):
        # --- TITLE SCENE ---
        title_group = self.show_title("Photosynthesis")
        self.play_caption("How plants convert sunlight into energy!")
        self.play(FadeOut(title_group))

        # --- SCENE 1: CHLOROPLAST STRUCTURE ---
        # Draw Chloroplast
        chloroplast = Ellipse(width=5, height=3, color=Colors.NEON_GREEN, fill_opacity=0.2)
        chloroplast.set_stroke(Colors.NEON_GREEN, width=4)
        
        # Thylakoid stacks (Grana)
        grana = VGroup()
        for i in range(3):
            stack = VGroup(*[
                RoundedRectangle(corner_radius=0.1, width=0.8, height=0.2, color=Colors.NEON_GREEN, fill_opacity=0.6)
                for _ in range(4)
            ]).arrange(UP, buff=0.05)
            grana.add(stack)
        grana.arrange(RIGHT, buff=1).move_to(chloroplast)
        
        labels = VGroup(
            Text("Chloroplast", font_size=20, color=Colors.NEON_GREEN).next_to(chloroplast, UP),
            Text("Thylakoids", font_size=20, color=Colors.NEON_GREEN).next_to(grana, DOWN)
        )

        self.play(DrawBorderThenFill(chloroplast))
        self.play(Create(grana), Write(labels))
        self.play_caption("Inside plant cells, chloroplasts contain thylakoid stacks.")

        # --- SCENE 2: LIGHT REACTION ---
        # Photon beams
        photons = VGroup(*[
            Arrow(
                start=UP*4 + LEFT*2 + RIGHT*i, 
                end=grana[i].get_top(), 
                color=Colors.BRIGHT_YELLOW, 
                buff=0.1,
                max_stroke_width_to_length_ratio=5
            ) for i in range(3)
        ])
        
        self.play(LaggedStart(*[GrowArrow(p) for p in photons], lag_ratio=0.2))
        self.add_fun_pulse(grana, color=Colors.BRIGHT_YELLOW)
        
        # Water splitting
        h2o = Text("H₂O", color=Colors.CYAN, font_size=30).move_to(LEFT*3)
        o2 = Text("O₂", color=Colors.CYAN, font_size=30).move_to(LEFT*3 + UP*1)
        
        self.play(Write(h2o))
        self.play(h2o.animate.move_to(grana[0].get_left()))
        self.play(ReplacementTransform(h2o, o2))
        self.play(o2.animate.move_to(LEFT*4 + UP*2).set_opacity(0)) # Float away
        
        self.play_caption("Light energy splits water and releases Oxygen.")

        # Energy carriers
        atp = Text("ATP", color=Colors.ENERGY, font_size=24, weight=BOLD).next_to(grana, RIGHT)
        nadph = Text("NADPH", color=Colors.ENERGY, font_size=24, weight=BOLD).next_to(atp, DOWN)
        
        self.play(Flash(grana, color=Colors.ENERGY))
        self.play(Write(atp), Write(nadph))
        
        self.play_caption("Generated Energy: ATP & NADPH")
        self.wait(1)
        
        # Clean up for next scene
        self.play(FadeOut(photons), FadeOut(labels), FadeOut(grana), FadeOut(chloroplast), FadeOut(atp), FadeOut(nadph))

        # --- SCENE 3: CALVIN CYCLE ---
        cycle_circle = Circle(radius=2, color=Colors.WHITE).set_opacity(0)
        arrows = VGroup(*[
            CurvedArrow(
                start_point=cycle_circle.point_at_angle(i*PI/3 + 0.5),
                end_point=cycle_circle.point_at_angle((i+1)*PI/3 - 0.5),
                color=Colors.NEON_GREEN
            ) for i in range(6)
        ])
        
        rubisco = Text("RuBisCO", font_size=20, color=Colors.HOT_PINK).move_to(UP*2.5)
        co2_in = Text("CO₂", font_size=24, color=Colors.WHITE).next_to(rubisco, UP)
        glucose_out = Text("Glucose", font_size=24, color=Colors.GOLD).move_to(DOWN*2.5)
        
        self.play(Create(arrows))
        self.play(Write(rubisco), FadeIn(co2_in, shift=DOWN))
        self.add_fun_pulse(rubisco)
        
        # Spin cycle
        self.play(Rotate(arrows, angle=2*PI, run_time=3, rate_func=linear))
        self.play(FadeIn(glucose_out, shift=UP))
        self.add_fun_pulse(glucose_out, color=Colors.GOLD, scale_factor=1.5)
        
        self.play_caption("The Calvin Cycle uses energy to turn CO₂ into Sugar (Glucose).")
        self.wait(2)
'''


def generate_gravity() -> str:
    """Gravity visualization."""
    return '''from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # ═══════════════════════════════════════
        # SCENE 1: Title
        # ═══════════════════════════════════════
        title = Text("Understanding Gravity", font_size=44, color=WHITE)
        title.to_edge(UP)
        subtitle = Text("The force that keeps us grounded", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # ═══════════════════════════════════════
        # SCENE 2: Falling Objects
        # ═══════════════════════════════════════
        scene_title = Text("Objects Fall at the Same Rate", font_size=36, color=TEAL)
        scene_title.to_edge(UP)
        
        # Ground line
        ground = Line(LEFT * 5, RIGHT * 5, color=GRAY)
        ground.move_to(DOWN * 2.5)
        
        # Two objects
        ball = Circle(radius=0.3, color=RED, fill_opacity=0.8)
        ball.move_to(LEFT * 2 + UP * 2)
        
        box = Square(side_length=0.5, color=BLUE, fill_opacity=0.8)
        box.move_to(RIGHT * 2 + UP * 2)
        
        explanation = Text("In a vacuum, all objects fall at 9.8 m/s²", font_size=24)
        explanation.to_edge(DOWN)
        
        self.play(Write(scene_title))
        self.play(Create(ground))
        self.play(Create(ball), Create(box))
        self.wait(1)
        self.play(FadeIn(explanation))
        
        # Animate falling
        self.play(
            ball.animate.move_to(LEFT * 2 + DOWN * 2.2),
            box.animate.move_to(RIGHT * 2 + DOWN * 2.2),
            run_time=1.5,
            rate_func=rate_functions.ease_in_quad
        )
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 3: Gravitational Formula
        # ═══════════════════════════════════════
        scene_title = Text("Newton's Law of Gravitation", font_size=36, color=TEAL)
        scene_title.to_edge(UP)
        
        formula = Text("F = G * (m1 * m2) / r^2", font_size=36)
        formula.move_to(UP * 0.5)
        
        # Labels
        labels = VGroup(
            Text("F = Gravitational Force", font_size=20),
            Text("G = Gravitational Constant", font_size=20),
            Text("m1, m2 = Masses of objects", font_size=20),
            Text("r = Distance between centers", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        labels.move_to(DOWN * 1.5)
        
        self.play(Write(scene_title))
        self.play(Write(formula))
        self.wait(1)
        for label in labels:
            self.play(FadeIn(label), run_time=0.5)
        self.wait(3)
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 4: Earth and Moon
        # ═══════════════════════════════════════
        scene_title = Text("Gravity in Space", font_size=36, color=TEAL)
        scene_title.to_edge(UP)
        
        # Earth
        earth = Circle(radius=1, color=BLUE, fill_opacity=0.7)
        earth.move_to(LEFT * 2)
        earth_label = Text("Earth", font_size=20).next_to(earth, DOWN, buff=0.3)
        
        # Moon
        moon = Circle(radius=0.3, color=GRAY, fill_opacity=0.7)
        moon.move_to(RIGHT * 2)
        moon_label = Text("Moon", font_size=20).next_to(moon, DOWN, buff=0.3)
        
        # Gravity arrow
        arrow = Arrow(earth.get_right(), moon.get_left(), color=YELLOW, buff=0.1)
        arrow_label = Text("Gravity", font_size=18, color=YELLOW).next_to(arrow, UP, buff=0.2)
        
        explanation = Text("Gravity keeps the Moon in orbit around Earth", font_size=24)
        explanation.to_edge(DOWN)
        
        self.play(Write(scene_title))
        self.play(Create(earth), Write(earth_label))
        self.play(Create(moon), Write(moon_label))
        self.play(GrowArrow(arrow), Write(arrow_label))
        self.play(FadeIn(explanation))
        self.wait(3)
'''


def generate_chemical_bonding() -> str:
    """Ionic vs Covalent bonding visualizer."""
    return MASTER_TEMPLATE_HEADER + '''
class GeneratedScene(ColorfulScene):
    def construct(self):
        # --- TITLE SCENE ---
        title_group = self.show_title("Chemical Bonding Types")
        self.play_caption("Distinguishing Ionic vs Covalent bonds using Electronegativity")
        self.play(FadeOut(title_group))
        
        # ═══════════════════════════════════════
        # SCENE 1: Electronegativity Scale
        # ═══════════════════════════════════════
        self.next_section("Electronegativity Scale")
        
        # Create Number Line
        number_line = NumberLine(
            x_range=[0, 4, 1],
            length=10,
            color=Colors.LT_GRAY,
            include_numbers=False, # LaTeX disabled
            label_direction=UP,
        ).shift(DOWN * 0.5)

        # Add manual Text labels (Safe)
        for val in [0, 1, 2, 3, 4]:
            t = Text(str(val), font_size=20, color=Colors.WHITE)
            t.next_to(number_line.number_to_point(val), DOWN, buff=0.2)
            self.add(t)
        
        ax_label = Text("Electronegativity Difference", font_size=20, color=Colors.LT_GRAY).next_to(number_line, DOWN, buff=0.8)
        
        self.play(Create(number_line), Write(ax_label))
        
        # Zones
        # Ionic (> 1.7)
        ionic_rect = Rectangle(width=5.75, height=2, color=Colors.HOT_PINK, fill_opacity=0.2).move_to(number_line.number_to_point(2.85) + UP)
        ionic_label = Text("IONIC (>1.7)", color=Colors.HOT_PINK, font_size=20).next_to(ionic_rect, UP)
        
        # Covalent (< 0.5)
        cov_rect = Rectangle(width=1.25, height=2, color=Colors.CYAN, fill_opacity=0.2).move_to(number_line.number_to_point(0.25) + UP)
        cov_label = Text("COVALENT (<0.5)", color=Colors.CYAN, font_size=20).next_to(cov_rect, UP)
        
        # Polar Covalent (0.5 - 1.7)
        polar_rect = Rectangle(width=3, height=2, color=Colors.YELLOW, fill_opacity=0.2).move_to(number_line.number_to_point(1.1) + UP)
        polar_label = Text("POLAR (0.5-1.7)", color=Colors.YELLOW, font_size=20).next_to(polar_rect, UP)
        # Using a VGroup to display these so we can organize overlapping checks if needed, 
        # but manual positioning here is safer.
        
        self.play(
            FadeIn(ionic_rect), Write(ionic_label),
            FadeIn(cov_rect), Write(cov_label),
            FadeIn(polar_rect), Write(polar_label)
        )
        
        # Plot Elements (Staggered to prevent overlap)
        # Na(0.9), Cl(3.0), C(2.5), H(2.1)
        
        def plot_val(name, val, color, y_offset=0):
            arrow = Arrow(start=UP*0.5, end=DOWN*0.1, color=color).next_to(number_line.number_to_point(val), UP, buff=0)
            lbl = Text(f"{name}({val})", font_size=18, color=color).next_to(arrow, UP)
            lbl.shift(UP * y_offset) # Stagger vertically
            return VGroup(arrow, lbl)
            
        na = plot_val("Na", 0.93, Colors.WHITE, y_offset=0) # Real Na is 0.93 roughly plotting at 0.9
        cl = plot_val("Cl", 3.16, Colors.WHITE, y_offset=0) # Real Cl is 3.16
        
        # Calculate diff for NaCl: 3.16 - 0.93 = 2.23 (Ionic)
        diff_marker = Arrow(start=number_line.number_to_point(0.93), end=number_line.number_to_point(3.16), color=Colors.HOT_PINK, buff=0)
        diff_marker.shift(DOWN*0.2)
        diff_lbl = Text("Δ = 2.23 (Ionic)", font_size=24, color=Colors.HOT_PINK, weight=BOLD).next_to(diff_marker, UP)
        
        self.play(Create(na), Create(cl))
        self.play(GrowArrow(diff_marker))
        self.play(Write(diff_lbl))
        self.add_fun_pulse(diff_lbl)
        
        self.play_caption("Large difference (>1.7) creates Ionic Bonds.")
        self.wait(2)
        
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 2: Sodium Chloride (Ionic)
        # ═══════════════════════════════════════
        self.next_section("Ionic Bonding")
        scene_title = Text("Ionic Bonding: Na + Cl", font_size=30, color=Colors.HOT_PINK).to_edge(UP, buff=0.3)
        if scene_title.width > 11: scene_title.scale(11 / scene_title.width)
        self.play(Write(scene_title))
        
        # Atoms — use ASCII labels (Unicode superscripts don't render on server fonts)
        na_circ = Circle(radius=0.5, color=Colors.LT_GRAY, fill_opacity=0.5).move_to(LEFT * 3)
        na_lbl  = Text("Na", font_size=22, color=Colors.WHITE).move_to(na_circ.get_center())
        na_atom = VGroup(na_circ, na_lbl)
        
        na_electron = Dot(color=Colors.CYAN).move_to(na_circ.get_center() + RIGHT*1.2)
        na_orbit = Circle(radius=1.2, color=Colors.LT_GRAY, stroke_opacity=0.5).move_to(na_circ.get_center())
        na_group = VGroup(na_atom, na_orbit, na_electron)
        
        cl_circ = Circle(radius=0.7, color=Colors.NEON_GREEN, fill_opacity=0.5).move_to(RIGHT * 3)
        cl_lbl  = Text("Cl", font_size=22, color=Colors.WHITE).move_to(cl_circ.get_center())
        cl_atom = VGroup(cl_circ, cl_lbl)
        # Cl has 7 valence, show open spot
        cl_orbit = Circle(radius=1.4, color=Colors.NEON_GREEN, stroke_opacity=0.5).move_to(cl_circ.get_center())
        cl_electrons = VGroup(*[
             Dot(color=Colors.CYAN).move_to(cl_orbit.point_at_angle(a)) 
             for a in [0, PI/4, PI/2, 3*PI/4, PI, 5*PI/4, 3*PI/2]
        ])
        cl_group = VGroup(cl_atom, cl_orbit, cl_electrons)

        self.play(FadeIn(na_group), FadeIn(cl_group))
        self.play_caption("Sodium has 1 extra electron. Chlorine needs 1.")
        
        # Electron Transfer
        transfer_path = ArcBetweenPoints(na_electron.get_center(), cl_orbit.point_at_angle(7*PI/4), angle=-PI/2)
        self.play(MoveAlongPath(na_electron, transfer_path, run_time=1.5), run_time=1.5)
        
        # Change charges
        na_plus = Text("Na⁺", font_size=32, color=Colors.HOT_PINK).move_to(na_atom)
        cl_minus = Text("Cl⁻", font_size=32, color=Colors.CYAN).move_to(cl_atom)
        
        self.play(
            ReplacementTransform(na_atom[1], na_plus),
            ReplacementTransform(cl_atom[1], cl_minus),
            na_atom[0].animate.set_color(Colors.HOT_PINK),
            cl_atom[0].animate.set_color(Colors.CYAN)
        )
        self.add_fun_pulse(na_plus)
        self.add_fun_pulse(cl_minus, color=Colors.CYAN)
        
        self.play_caption("Direct Electron Transfer = Electrostatic Attraction")
        
        # Bond
        self.play(
            na_group.animate.shift(RIGHT*1.5),
            cl_group.animate.shift(LEFT*1.5),
            na_plus.animate.shift(RIGHT*1.5),
            cl_minus.animate.shift(LEFT*1.5),
        )
        
        bond_text = Text("Ionic Bond", font_size=28, color=Colors.GOLD).next_to(VGroup(na_group, cl_group), DOWN)
        self.play(Write(bond_text))
        self.wait(2)
        
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 3: Covalent (H2)
        # ═══════════════════════════════════════
        self.next_section("Covalent Bonding")
        scene_title = Text("Covalent Bonding: H₂", font_size=36, color=Colors.CYAN).to_edge(UP)
        self.play(Write(scene_title))
        
        h1 = VGroup(Circle(0.3, color=Colors.WHITE), Text("H", font_size=20))
        h1.move_to(LEFT * 2)
        e1 = Dot(color=Colors.CYAN).next_to(h1, RIGHT, buff=0.1)
        
        h2 = VGroup(Circle(0.3, color=Colors.WHITE), Text("H", font_size=20))
        h2.move_to(RIGHT * 2)
        e2 = Dot(color=Colors.CYAN).next_to(h2, LEFT, buff=0.1)
        
        self.play(Create(h1), Create(e1), Create(h2), Create(e2))
        self.play_caption("Two Hydrogen atoms. Similar electronegativity.")
        
        # Sharing
        self.play(
            h1.animate.shift(RIGHT * 1.2),
            e1.animate.shift(RIGHT * 0.8),
            h2.animate.shift(LEFT * 1.2),
            e2.animate.shift(LEFT * 0.8),
        )
        
        # Orbit ring around both
        shared_orbit = Ellipse(width=2.5, height=1.5, color=Colors.CYAN).move_to(ORIGIN)
        self.play(Create(shared_orbit))
        
        # Electrons rotate around both
        self.play(
            Rotate(e1, about_point=ORIGIN, angle=4*PI, run_time=4, rate_func=linear),
            Rotate(e2, about_point=ORIGIN, angle=4*PI, run_time=4, rate_func=linear),
            run_time=4
        )
        self.play_caption("Electrons overlap and are SHARED.")
        
        self.wait(1)
        self.play(FadeOut(*self.mobjects))
        
        # ═══════════════════════════════════════
        # SCENE 4: Comparison Table
        # ═══════════════════════════════════════
        self.next_section("Comparison")
        
        # Create Table
        table = Table(
            [["Transferred", "Shared"],
             ["> 1.7", "< 1.7"],
             ["High (Solids)", "Low (Liquids/Gas)"],
             ["Yes (Molten)", "No"]],
            col_labels=[Text("Ionic"), Text("Covalent")],
            row_labels=[Text("Electrons"), Text("Diff"), Text("Melting Pt"), Text("Conducts")],
            include_outer_lines=True
        ).scale(0.6)
        
        # Style
        table.get_col_labels()[0].set_color(Colors.HOT_PINK)
        table.get_col_labels()[1].set_color(Colors.CYAN)
        table.get_rows()[1].set_color(Colors.NEON_GREEN) # Content
        
        self.play(Create(table))
        self.play_caption("Summary: Differences in Bonding properties")
        
        self.wait(3)
'''

# ===========================================
# Template Registry
# ===========================================
TEMPLATES: Dict[str, Callable[[], str]] = {
    "pythagorean": generate_pythagorean,
    "quadratic": generate_pythagorean,  # Similar structure
    "derivative": generate_derivative,
    "integral": generate_derivative,  # Similar structure
    "newton": generate_newton_laws,
    "gravity": generate_gravity,
    "photosynthesis": generate_photosynthesis,
    "chemical_bond": generate_chemical_bonding,
}


def get_template_code(template_name: str) -> Optional[str]:
    """Get the code for a specific template."""
    generator = TEMPLATES.get(template_name)
    if generator:
        return generator()
    return None


def get_template_for_concept(concept: str) -> Optional[str]:
    """
    Get template code if a good match exists.
    Returns None if no suitable template found.
    """
    template_name = select_template(concept)
    if template_name:
        return get_template_code(template_name)
    return None
