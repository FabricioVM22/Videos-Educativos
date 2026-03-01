from manim import *
import numpy as np


# ==========================================
# 1. DESIGN SYSTEM (Refinado)
# ==========================================
class StyleConfig:
    BG = "#0B0F19"
    SURFACE = "#1E293B"
    ACCENT = "#38BDF8"
    SUCCESS = "#4ADE80"
    WARNING = "#FBBF24"
    ERROR = "#F87171"
    PURPLE = "#A78BFA"
    TEXT = "#F8FAFC"
    TEXT_DIM = "#475569"  # Más oscuro para el grid

    @staticmethod
    def get_font_size(base_ratio=0.03):
        return config.frame_height * 10 * base_ratio


# ==========================================
# 2. COMPONENTES UI
# ==========================================
class TechCard(VGroup):
    def __init__(self, content, color=StyleConfig.SURFACE, stroke_color=StyleConfig.ACCENT, **kwargs):
        super().__init__(**kwargs)
        padding = 0.3
        bg = RoundedRectangle(
            corner_radius=0.1,
            width=content.width + padding * 2,
            height=content.height + padding * 2
        ).set_fill(color, 0.9).set_stroke(stroke_color, 1.5, opacity=0.4)
        self.add(bg, content)


class FlowToken(VGroup):
    def __init__(self, color=StyleConfig.WARNING):
        super().__init__()
        dot = Dot(radius=0.08, color=color)
        glow = Dot(radius=0.2, color=color, fill_opacity=0.2)
        self.add(glow, dot)


# ==========================================
# 3. ESCENA MEJORADA Y ELABORADA
# ==========================================
class LogicaProgramacionMaster(Scene):
    def construct(self):
        self.setup_background()

        # Flujo del video
        self.intro_cinematica()
        self.section_sequence_detailed()
        self.section_conditionals_complex()
        self.section_loops_iterator()
        self.outro()

    def setup_background(self):
        self.camera.background_color = StyleConfig.BG
        # Grid con opacidad muy baja (0.05)
        grid = NumberPlane(
            background_line_style={
                "stroke_color": StyleConfig.TEXT_DIM,
                "stroke_width": 1,
                "stroke_opacity": 0.05
            }
        )
        self.add(grid)

    def intro_cinematica(self):
        title = Text("ALGORITMIA VISUAL", font="Monospace", weight=BOLD).scale(1.1)
        underline = Line(LEFT, RIGHT).scale(2).next_to(title, DOWN, buff=0.2).set_color(StyleConfig.ACCENT)

        self.play(Write(title), Create(underline), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title, underline, shift=UP))

    # --- 01. SECUENCIA: El orden de los factores sí altera el producto ---
    def section_sequence_detailed(self):
        header = Text("01. ESTRUCTURA SECUENCIAL", font="Monospace", color=StyleConfig.ACCENT).to_edge(UL)
        self.play(FadeIn(header, shift=RIGHT))

        # Creamos una analogía de receta/proceso
        pasos = VGroup(
            TechCard(Text("DECLARAR: x = 10", font_size=18, font="Monospace")),
            TechCard(Text("PROCESAR: x = x * 2", font_size=18, font="Monospace")),
            TechCard(Text("MOSTRAR: 'Resultado: 20'", font_size=18, font="Monospace"))
        ).arrange(DOWN, buff=0.7).shift(LEFT * 2)

        desc = Text(
            "La computadora lee el código\n"
            "de arriba hacia abajo, línea\n"
            "por línea, sin saltarse nada.",
            font_size=20, color=StyleConfig.TEXT_DIM, line_spacing=1.5
        ).next_to(pasos, RIGHT, buff=1.5)

        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT) for p in pasos], lag_ratio=0.4))
        self.play(Write(desc))

        # Ejecución paso a paso
        token = FlowToken(color=StyleConfig.SUCCESS)
        token.move_to(pasos[0].get_left() + LEFT * 0.5)

        for i, paso in enumerate(pasos):
            self.play(token.animate.move_to(paso.get_center()), run_time=0.7)
            self.play(Indicate(paso, color=StyleConfig.SUCCESS, scale_factor=1.1))
            # Pequeño efecto de "valor procesado"
            if i == 1:
                val = Text("x = 20", color=StyleConfig.SUCCESS, font_size=14).next_to(paso, RIGHT)
                self.play(FadeIn(val, shift=LEFT), FadeOut(val, shift=UP))

        self.wait(2)
        self.play(FadeOut(pasos, desc, header, token))

    # --- 02. CONDICIONALES: La toma de decisiones ---
    def section_conditionals_complex(self):
        header = Text("02. ESTRUCTURAS DE DECISIÓN", font="Monospace", color=StyleConfig.ACCENT).to_edge(UL)
        self.play(FadeIn(header))

        # El diamante de decisión
        decision = Polygon(UP, RIGHT * 1.5, DOWN, LEFT * 1.5).set_stroke(StyleConfig.PURPLE, 2).set_fill(StyleConfig.BG,
                                                                                                         1)
        txt_cond = Text("¿TIENE ACCESO?", font_size=18, font="Monospace").move_to(decision)
        if_node = VGroup(decision, txt_cond).shift(UP * 1.5)

        true_path = TechCard(Text("ENTRAR AL SISTEMA", color=StyleConfig.SUCCESS, font_size=16)).shift(
            DOWN * 0.5 + LEFT * 2.5)
        false_path = TechCard(Text("MOSTRAR ERROR", color=StyleConfig.ERROR, font_size=16)).shift(
            DOWN * 0.5 + RIGHT * 2.5)

        # Cambia estas líneas en tu función section_conditionals_complex:
        l_true = CurvedArrow(if_node.get_left(), true_path.get_top(), angle=TAU / 8)
        l_false = CurvedArrow(if_node.get_right(), false_path.get_top(), angle=-TAU / 8)

        self.play(Create(if_node))
        self.play(
            Create(l_true), Create(l_false),
            FadeIn(true_path, shift=DOWN), FadeIn(false_path, shift=DOWN)
        )

        # Explicación dinámica
        expl = Text("Si la condición es VERDADERA, sigue un camino.\nSi es FALSA, ejecuta otra acción.",
                    font_size=18, color=StyleConfig.TEXT_DIM).to_edge(DOWN, buff=1)
        self.play(Write(expl))

        # Flujo de ejemplo (False case)
        token = FlowToken(color=StyleConfig.ERROR).move_to(if_node)
        self.play(FadeIn(token))
        self.play(MoveAlongPath(token, l_false), run_time=1.5)
        self.play(Indicate(false_path, color=StyleConfig.ERROR))

        self.wait(2)
        self.play(FadeOut(VGroup(header, if_node, true_path, false_path, l_true, l_false, token, expl)))

    # --- 03. BUCLES: Automatización ---
    def section_loops_iterator(self):
        header = Text("03. BUCLES (ITERACIÓN)", font="Monospace", color=StyleConfig.ACCENT).to_edge(UL)
        self.play(FadeIn(header))

        # Visualizar una lista siendo procesada
        items = VGroup(*[Square(side_length=0.6).set_stroke(StyleConfig.TEXT_DIM, 1) for _ in range(5)]).arrange(RIGHT,
                                                                                                                 buff=0.2)
        items.shift(UP * 0.5)

        code_box = TechCard(Text("PARA CADA ELEMENTO:\n   PROCESAR()", font_size=20, font="Monospace"),
                            stroke_color=StyleConfig.WARNING)
        code_box.next_to(items, DOWN, buff=1)

        self.play(Create(items), FadeIn(code_box))

        desc = Text("Evitan repetir código manualmente.", font_size=18, color=StyleConfig.TEXT_DIM).next_to(code_box,
                                                                                                            DOWN)
        self.play(Write(desc))

        # Animación de procesamiento
        token = FlowToken(color=StyleConfig.WARNING)
        for i, item in enumerate(items):
            self.play(token.animate.move_to(item.get_center()), run_time=0.4)
            self.play(
                item.animate.set_fill(StyleConfig.WARNING, opacity=0.6).set_stroke(StyleConfig.WARNING, 2),
                Indicate(code_box, scale_factor=1.05, color=StyleConfig.WARNING),
                run_time=0.3
            )

        self.wait(2)
        self.play(FadeOut(VGroup(header, items, code_box, desc, token)))

    def outro(self):
        msg = Text("LA LÓGICA ES EL LENGUAJE UNIVERSAL", font="Monospace", font_size=24).set_color_by_gradient(
            StyleConfig.ACCENT, StyleConfig.PURPLE)
        self.play(Write(msg))
        self.play(msg.animate.scale(1.1), run_time=1)
        self.wait(3)