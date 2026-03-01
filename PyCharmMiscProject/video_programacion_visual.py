from manim import *


# ==========================================
# 1. DESIGN SYSTEM
# ==========================================
class Style:
    BG = "#05070A"
    SURFACE = "#111827"
    ACCENT = "#38BDF8"  # Cyan
    SUCCESS = "#22C55E"  # Verde
    WARNING = "#EAB308"  # Amarillo
    ERROR = "#EF4444"  # Rojo
    PURPLE = "#8B5CF6"  # Violeta
    TEXT = "#F8FAFC"
    TEXT_SIDE = "#94A3B8"


# ==========================================
# 2. COMPONENTES UI
# ==========================================
class ExplanationBox(VGroup):
    """Caja de texto para el lado derecho"""

    def __init__(self, title, description):
        super().__init__()
        t = Text(title, font="Monospace", color=Style.ACCENT, font_size=24).to_edge(UP).shift(RIGHT * 3.5)
        d = Text(description, font_size=18, line_spacing=1.5, t2c={'"': Style.WARNING})
        d.width = 5  # Ancho fijo para que no invada la animación
        d.next_to(t, DOWN, buff=0.5).shift(RIGHT * 0.2)
        self.add(t, d)


class TechNode(VGroup):
    """Nodos para diagramas en el lado izquierdo"""

    def __init__(self, label, color=Style.SURFACE, stroke=Style.ACCENT):
        super().__init__()
        txt = Text(label, font_size=18, font="Monospace")
        rect = RoundedRectangle(corner_radius=0.1, width=2, height=1)
        rect.set_fill(color, 1).set_stroke(stroke, 2)
        self.add(rect, txt)


# ==========================================
# 3. ESCENA PRINCIPAL
# ==========================================
class LogicDecoderPro(Scene):
    def construct(self):
        self.camera.background_color = Style.BG

        # 0. INTRO (0:00 - 0:05)
        self.intro_cinematica()

        # 1. SECUENCIA (0:05 - 0:15)
        self.show_sequence()

        # 2. CONDICIONALES (0:15 - 0:50)
        self.show_conditionals()

        # 3. BUCLES (0:50 - 1:40)
        self.show_loops()

        # 4. ANIDAMIENTO & OUTRO (1:40 - 2:05)
        self.show_nesting_and_outro()

    def intro_cinematica(self):
        logo = Text("LOGIC_DECODER", font="Monospace", weight=BOLD).scale(1.5)
        self.play(Write(logo), run_time=2)
        self.play(Indicate(logo, color=Style.ACCENT))
        self.wait(1)
        self.play(FadeOut(logo, shift=UP))

    def show_sequence(self):
        # Texto Derecha
        info = ExplanationBox("01. SECUENCIA",
                              "Es el orden natural donde cada\ninstrucción se ejecuta línea tras\nlínea, como una receta paso a paso.")

        # Animación Izquierda
        nodes = VGroup(
            TechNode("INPUT"), TechNode("PROCESS"), TechNode("OUTPUT")
        ).arrange(DOWN, buff=0.8).shift(LEFT * 3.5)
        arrows = VGroup(*[Arrow(nodes[i], nodes[i + 1], color=Style.TEXT_SIDE) for i in range(2)])

        self.play(FadeIn(info), LaggedStart(*[Create(n) for n in nodes], lag_ratio=0.3))
        self.play(Create(arrows))

        dot = Dot(color=Style.SUCCESS).move_to(nodes[0])
        self.play(dot.animate.move_to(nodes[1]), run_time=1.5)
        self.play(dot.animate.move_to(nodes[2]), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(info, nodes, arrows, dot))

    def show_conditionals(self):
        # --- IF / ELSE ---
        info = ExplanationBox("02. CONDICIONALES",
                              'El "IF" evalúa: si es verdadero,\ntoma un camino. Con "ELSE", siempre\nhay un plan B.')

        diamond = Polygon(UP, RIGHT * 1.5, DOWN, LEFT * 1.5).set_stroke(Style.PURPLE, 2).shift(LEFT * 3.5 + UP * 1.5)
        lbl = Text("¿X > 5?", font_size=16).move_to(diamond)

        true_box = TechNode("TRUE", color=Style.SUCCESS).shift(LEFT * 5 + DOWN * 1)
        false_box = TechNode("FALSE", color=Style.ERROR).shift(LEFT * 2 + DOWN * 1)

        a1 = CurvedArrow(diamond.get_left(), true_box.get_top(), angle=TAU / 8)
        a2 = CurvedArrow(diamond.get_right(), false_box.get_top(), angle=-TAU / 8)

        self.play(FadeIn(info), Create(diamond), Write(lbl))
        self.play(Create(a1), Create(a2), FadeIn(true_box), FadeIn(false_box))

        # Token elige TRUE
        dot = Dot(color=Style.SUCCESS).move_to(diamond)
        self.play(MoveAlongPath(dot, a1), run_time=2)
        self.wait(2)
        self.play(FadeOut(diamond, lbl, true_box, false_box, a1, a2, dot, info))

        # --- SWITCH ---
        info = ExplanationBox("02. SWITCH",
                              'Compara un valor contra varios\ncasos y envía el flujo directamente\nal destino correcto.')

        center = TechNode("SWITCH", stroke=Style.WARNING).shift(LEFT * 3.5 + UP * 1.5)
        cases = VGroup(*[TechNode(f"CASE {i}", color=Style.BG) for i in range(1, 4)]).arrange(RIGHT, buff=0.2).shift(
            LEFT * 3.5 + DOWN * 1.5)
        lines = VGroup(*[Line(center.get_bottom(), c.get_top(), stroke_opacity=0.5) for c in cases])

        self.play(FadeIn(info), FadeIn(center), Create(lines), FadeIn(cases))
        dot = Dot(color=Style.WARNING).move_to(center)
        self.play(dot.animate.move_to(cases[2]), run_time=2)  # Salto al Case 3
        self.wait(2)
        self.play(FadeOut(info, center, cases, lines, dot))

    def show_loops(self):
        # --- WHILE ---
        info = ExplanationBox("03. BUCLES: WHILE",
                              'Se ejecuta "mientras" la condición\nsea cierta. Útil cuando no sabes\ncuántas veces repetirás.')

        loop_rect = TechNode("REPETIR", stroke=Style.PURPLE).shift(LEFT * 3.5)
        arrow_loop = CurvedArrow(loop_rect.get_bottom(), loop_rect.get_top(), angle=-TAU / 1.5,
                                 color=Style.PURPLE).shift(RIGHT * 1)

        self.play(FadeIn(info), Create(loop_rect), Create(arrow_loop))
        dot = Dot(color=Style.PURPLE).move_to(loop_rect)
        for _ in range(3):
            self.play(Rotate(dot, about_point=loop_rect.get_right(), angle=TAU), run_time=1)

        self.play(FadeOut(info, loop_rect, arrow_loop, dot))

        # --- FOR EACH ---
        info = ExplanationBox("03. FOR EACH",
                              "Recorre colecciones elemento por\nelemento. Perfecto para procesar\nlistas o conjuntos de datos.")

        boxes = VGroup(*[Square(side_length=0.5).set_stroke(Style.ACCENT) for _ in range(5)]).arrange(RIGHT,
                                                                                                      buff=0.2).shift(
            LEFT * 3.5)

        self.play(FadeIn(info), Create(boxes))
        dot = Dot(color=Style.SUCCESS)
        for box in boxes:
            self.play(dot.animate.move_to(box), run_time=0.5)
            self.play(box.animate.set_fill(Style.SUCCESS, 0.5), run_time=0.2)

        self.wait(2)
        self.play(FadeOut(info, boxes, dot))

    def show_nesting_and_outro(self):
        # --- ANIDAMIENTO ---
        info = ExplanationBox("04. ANIDAMIENTO",
                              'Combinar estructuras: un bucle\ndentro de un condicional. ¡Cuidado\ncon la complejidad!')

        outer = RoundedRectangle(width=3, height=2, color=Style.ACCENT).shift(LEFT * 3.5)
        inner = Circle(radius=0.5, color=Style.WARNING).move_to(outer)

        self.play(FadeIn(info), Create(outer))
        self.play(Create(inner), run_time=2)
        self.play(Indicate(inner))
        self.wait(2)
        self.play(FadeOut(info, outer, inner))

        # --- OUTRO ---
        final_txt = Text("LA LÓGICA PERMANECE.", font="Monospace", color=Style.SUCCESS).scale(0.8)
        triangulo = Triangle().set_stroke(Style.ACCENT, 4).scale(2)

        self.play(Create(triangulo), Write(final_txt))
        self.play(Flash(triangulo, color=Style.SUCCESS))
        self.wait(3)