from manim import *
import numpy as np


# ==========================================
# 1. DESIGN SYSTEM (Configuración Centralizada)
# ==========================================
class StyleConfig:
    # Colores Semánticos
    BG = "#0B0F19"
    SURFACE = "#1E293B"
    SURFACE_2 = "#334155"
    SURFACE_3 = "#475569"
    TEXT = "#F8FAFC"
    TEXT_DIM = "#94A3B8"
    ACCENT = "#38BDF8"
    SUCCESS = "#4ADE80"
    WARNING = "#FBBF24"
    ERROR = "#F87171"
    PURPLE = "#A78BFA"
    ORANGE = "#FB923C"
    PINK = "#F472B6"

    # Espaciado Relativo
    PADDING_SM = 0.2
    PADDING_MD = 0.4
    PADDING_LG = 0.8

    @staticmethod
    def get_font_size(base_ratio=0.05):
        """Tamaño de fuente escalable según resolución"""
        # Cambiamos frame_height por pixel_height
        return config.pixel_height * base_ratio


# ==========================================
# 2. LAYOUT ENGINE (Sistema de Grilla Responsive)
# ==========================================
class ResponsiveLayout:
    def __init__(self):
        self.frame_w = config.frame_width
        self.frame_h = config.frame_height

        # Márgenes de seguridad (10% del frame)
        self.margin_x = self.frame_w * 0.1
        self.margin_y = self.frame_h * 0.1

        # Área útil
        self.safe_area = Rectangle(
            width=self.frame_w - 2 * self.margin_x,
            height=self.frame_h - 2 * self.margin_y
        ).move_to(ORIGIN)

        # División 50/50 para columnas
        self.col_width = self.safe_area.width / 2
        self.col_height = self.safe_area.height

        self.left_col = Rectangle(
            width=self.col_width, height=self.col_height
        ).move_to(self.safe_area.get_center() + LEFT * self.col_width / 2)

        self.right_col = Rectangle(
            width=self.col_width, height=self.col_height
        ).move_to(self.safe_area.get_center() + RIGHT * self.col_width / 2)

    def get_pos(self, column: str, x: float, y: float):
        """Posición normalizada (0-1) dentro de una columna"""
        col = self.left_col if column == "left" else self.right_col
        return col.get_corner(DL) + RIGHT * (col.width * x) + UP * (col.height * y)


# ==========================================
# 3. COMPONENTES UI (Reutilizables)
# ==========================================
class Card(VGroup):
    """Tarjeta con sombra y bordes redondeados"""

    def __init__(self, content, color=StyleConfig.SURFACE, **kwargs):
        super().__init__(**kwargs)
        padding = StyleConfig.PADDING_MD

        bg = RoundedRectangle(
            corner_radius=0.1,
            width=content.width + 2 * padding,
            height=content.height + 2 * padding
        )
        bg.set_fill(color, 0.95).set_stroke(StyleConfig.TEXT, 1, 0.1)

        shadow = bg.copy().set_fill(BLACK, 0.3).set_stroke(width=0)
        shadow.shift(DOWN * 0.05 + RIGHT * 0.05)
        shadow.z_index = -1

        self.add(shadow, bg, content)
        self.move_to(content)


class Node(VGroup):
    """Nodo de proceso rectangular"""

    def __init__(self, text, layout, color=StyleConfig.SURFACE_2,
                 width_ratio=0.25, height_ratio=0.06, **kwargs):
        super().__init__(**kwargs)

        w = layout.col_width * width_ratio
        h = layout.col_height * height_ratio

        box = RoundedRectangle(corner_radius=0.08, width=w, height=h)
        box.set_fill(color, 1).set_stroke(StyleConfig.TEXT, 1.2, 0.4)

        fs = StyleConfig.get_font_size(0.022)
        txt = Text(text, font_size=fs, color=StyleConfig.TEXT)
        txt.move_to(box)

        self.add(box, txt)


class DecisionNode(VGroup):
    """Nodo de decisión (rombo)"""

    def __init__(self, text, layout, color=StyleConfig.SURFACE, **kwargs):
        super().__init__(**kwargs)

        size = layout.col_width * 0.25

        diamond = Polygon(
            UP * size * 0.6, RIGHT * size * 0.8,
            DOWN * size * 0.6, LEFT * size * 0.8
        )
        diamond.set_fill(color, 1).set_stroke(StyleConfig.ACCENT, 2, 0.8)

        fs = StyleConfig.get_font_size(0.02)
        txt = Text(text, font_size=fs, color=StyleConfig.TEXT)
        txt.move_to(diamond)

        self.add(diamond, txt)


class LoopNode(VGroup):
    """Nodo de ciclo (hexágono)"""

    def __init__(self, text, layout, color=StyleConfig.SURFACE, **kwargs):
        super().__init__(**kwargs)

        w = layout.col_width * 0.3
        h = layout.col_height * 0.08

        hexagon = RegularPolygon(n=6, radius=w / 2)
        hexagon.set_fill(color, 1).set_stroke(StyleConfig.WARNING, 2, 0.8)
        hexagon.stretch_to_fit_width(w)
        hexagon.stretch_to_fit_height(h)

        fs = StyleConfig.get_font_size(0.022)
        txt = Text(text, font_size=fs, color=StyleConfig.TEXT)
        txt.move_to(hexagon)

        self.add(hexagon, txt)


class Connection(Arrow):
    """Flecha de conexión entre nodos"""

    def __init__(self, start, end, color=StyleConfig.TEXT_DIM, **kwargs):
        super().__init__(
            start.get_right(), end.get_left(),
            buff=0.15, stroke_width=3, color=color,
            tip_length=0.15, **kwargs
        )


class FlowToken(Dot):
    """Token que representa el flujo de ejecución"""

    def __init__(self, color=StyleConfig.WARNING):
        super().__init__(radius=0.12, color=color)
        self.set_stroke(WHITE, 1.5)


# ==========================================
# 4. ESCENA PRINCIPAL
# ==========================================
class LogicaDeProgramacionVisual(Scene):
    def construct(self):
        # Inicializar sistema
        self.layout = ResponsiveLayout()

        # Fondo
        bg = Rectangle(width=config.frame_width, height=config.frame_height)
        bg.set_fill(StyleConfig.BG, 1).set_stroke(width=0)
        self.add(bg)

        # Línea divisoria
        divider = Line(
            self.layout.safe_area.get_top(),
            self.layout.safe_area.get_bottom()
        )
        divider.set_stroke(StyleConfig.TEXT_DIM, 1, 0.03)
        self.add(divider)

        # Ejecutar secciones
        self.intro()
        self.section_sequential()
        self.section_conditionals()
        self.section_loops()
        self.section_functions()
        self.section_data_flow()
        self.summary()
        self.end_screen()

    def clear_section(self):
        """Limpia la escena entre secciones"""
        self.wait(1)
        self.clear()
        # Re-agregar fondo y divider
        bg = Rectangle(width=config.frame_width, height=config.frame_height)
        bg.set_fill(StyleConfig.BG, 1).set_stroke(width=0)
        divider = Line(
            self.layout.safe_area.get_top(),
            self.layout.safe_area.get_bottom()
        )
        divider.set_stroke(StyleConfig.TEXT_DIM, 1, 0.03)
        self.add(bg, divider)

    # ========================================
    # INTRODUCCIÓN
    # ========================================
    def intro(self):
        fs_title = StyleConfig.get_font_size(0.065)
        fs_subtitle = StyleConfig.get_font_size(0.035)

        title = Text(
            "Lógica de Programación",
            font_size=fs_title,
            weight=BOLD,
            color=StyleConfig.TEXT
        )

        subtitle = Text(
            "Estructuras de control visuales",
            font_size=fs_subtitle,
            color=StyleConfig.TEXT_DIM
        )
        subtitle.next_to(title, DOWN, buff=0.5)

        tagline = Text(
            "Aprende a pensar como programador",
            font_size=fs_subtitle * 0.8,
            color=StyleConfig.ACCENT
        )
        tagline.next_to(subtitle, DOWN, buff=0.3)

        group = VGroup(title, subtitle, tagline).move_to(ORIGIN)

        # Animación de entrada
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1)
        self.play(FadeIn(tagline, shift=UP * 0.3), run_time=1)

        self.wait(2)

        # Animación de salida
        self.play(
            FadeOut(group, shift=UP * 0.5),
            run_time=1
        )
        self.remove(group)
        self.clear_section()

    # ========================================
    # SECCIÓN 1: SECUENCIA
    # ========================================
    def section_sequential(self):
        # Títulos
        fs_title = StyleConfig.get_font_size(0.04)
        title = Text("1. Secuencia", font_size=fs_title, weight=BOLD, color=StyleConfig.TEXT)
        title.move_to(self.layout.get_pos("left", 0.05, 0.92))
        title.align_to(self.layout.left_col, LEFT).shift(RIGHT * 0.3)

        subtitle = Text(
            "Ejecución paso a paso",
            font_size=fs_title * 0.6,
            color=StyleConfig.TEXT_DIM
        )
        subtitle.next_to(title, DOWN, aligned_edge=LEFT)

        self.play(Write(title), FadeIn(subtitle), run_time=1)

        # Diagrama de secuencia (3 pasos)
        steps = ["Inicio", "Proceso", "Fin"]
        nodes = VGroup()

        for i, label in enumerate(steps):
            node = Node(label, self.layout, color=StyleConfig.SURFACE_2)
            y_pos = 0.75 - (i * 0.25)
            node.move_to(self.layout.get_pos("left", 0.35, y_pos))
            nodes.add(node)

        # Flechas entre pasos
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrow = always_redraw(
                lambda s=nodes[i], e=nodes[i + 1]: Connection(s, e)
            )
            arrows.add(arrow)

        # Token de flujo
        token = FlowToken()
        token.move_to(nodes[0])

        # Explicación (derecha)
        exp_text = Text(
            "La secuencia es el flujo básico.\n"
            "Las instrucciones se ejecutan\n"
            "en orden, una después de otra.\n\n"
            "Como seguir una receta de cocina:\n"
            "1. Preparar ingredientes\n"
            "2. Cocinar\n"
            "3. Servir",
            font_size=StyleConfig.get_font_size(0.022),
            color=StyleConfig.TEXT,
            line_spacing=1.6
        )
        exp_card = Card(exp_text)
        exp_card.move_to(self.layout.right_col.get_center())

        # Animaciones
        diagram = VGroup(nodes, arrows)
        self.play(FadeIn(nodes), Create(arrows), run_time=1.5)
        self.play(FadeIn(exp_card, shift=RIGHT), run_time=1)
        self.play(FadeIn(token), run_time=0.5)

        # Animar flujo
        for i in range(len(nodes)):
            self.play(token.animate.move_to(nodes[i]), run_time=1)
            nodes[i].set_fill(StyleConfig.SUCCESS, 1)
            self.wait(0.5)
            if i < len(nodes) - 1:
                nodes[i].set_fill(StyleConfig.SURFACE_2, 1)

        self.wait(2)
        self.clear_section()

    # ========================================
    # SECCIÓN 2: CONDICIONALES
    # ========================================
    def section_conditionals(self):
        # Títulos
        fs_title = StyleConfig.get_font_size(0.04)
        title = Text("2. Condicionales", font_size=fs_title, weight=BOLD, color=StyleConfig.TEXT)
        title.move_to(self.layout.get_pos("left", 0.05, 0.92))
        title.align_to(self.layout.left_col, LEFT).shift(RIGHT * 0.3)

        subtitle = Text(
            "Tomar decisiones",
            font_size=fs_title * 0.6,
            color=StyleConfig.TEXT_DIM
        )
        subtitle.next_to(title, DOWN, aligned_edge=LEFT)

        self.play(Write(title), FadeIn(subtitle), run_time=1)

        # Diagrama condicional
        start = Node("Inicio", self.layout)
        start.move_to(self.layout.get_pos("left", 0.2, 0.75))

        decision = DecisionNode("¿Condición?", self.layout)
        decision.move_to(self.layout.get_pos("left", 0.5, 0.75))

        true_path = Node("Camino A", self.layout, color="#064E3B")
        true_path.move_to(self.layout.get_pos("left", 0.8, 0.85))

        false_path = Node("Camino B", self.layout, color="#450A0A")
        false_path.move_to(self.layout.get_pos("left", 0.8, 0.65))

        end = Node("Fin", self.layout)
        end.move_to(self.layout.get_pos("left", 0.5, 0.35))

        # Flechas
        arrow_start = always_redraw(lambda: Connection(start, decision))
        arrow_true = always_redraw(
            lambda: Connection(decision, true_path).set_color(StyleConfig.SUCCESS)
        )
        arrow_false = always_redraw(
            lambda: Connection(decision, false_path).set_color(StyleConfig.ERROR)
        )
        arrow_end_true = always_redraw(
            lambda: Connection(true_path, end).set_color(StyleConfig.SUCCESS)
        )
        arrow_end_false = always_redraw(
            lambda: Connection(false_path, end).set_color(StyleConfig.ERROR)
        )

        # Etiquetas SI/NO
        label_yes = Text("SÍ", font_size=StyleConfig.get_font_size(0.02), color=StyleConfig.SUCCESS)
        label_yes.next_to(arrow_true, UP, buff=0.1)

        label_no = Text("NO", font_size=StyleConfig.get_font_size(0.02), color=StyleConfig.ERROR)
        label_no.next_to(arrow_false, DOWN, buff=0.1)

        # Token
        token = FlowToken()
        token.move_to(start)

        # Explicación
        exp_text = Text(
            "Las condicionales permiten\n"
            "elegir entre diferentes caminos.\n\n"
            "Solo UN camino se ejecuta:\n"
            "• Si la condición es VERDADERA → Camino A\n"
            "• Si la condición es FALSA → Camino B\n\n"
            "Ejemplo: ¿Tienes paraguas?\n"
            "SÍ → No te mojas\n"
            "NO → Te mojas",
            font_size=StyleConfig.get_font_size(0.02),
            color=StyleConfig.TEXT,
            line_spacing=1.5
        )
        exp_card = Card(exp_text)
        exp_card.move_to(self.layout.right_col.get_center())

        # Animaciones
        diagram = VGroup(start, decision, true_path, false_path, end)
        self.play(FadeIn(start), FadeIn(token), run_time=0.8)
        self.play(Create(arrow_start), token.animate.move_to(decision), run_time=1)
        self.play(FadeIn(decision), run_time=0.5)
        self.play(FadeIn(exp_card, shift=RIGHT), run_time=1)

        # Mostrar camino verdadero
        self.play(
            Create(arrow_true), FadeIn(label_yes), FadeIn(true_path),
            run_time=1
        )
        self.play(token.animate.move_to(true_path), run_time=1)
        self.wait(1)

        # Retroceder y mostrar falso
        self.play(
            token.animate.move_to(decision),
            true_path.animate.set_opacity(0.3),
            run_time=0.8
        )
        self.play(
            Create(arrow_false), FadeIn(label_no), FadeIn(false_path),
            run_time=1
        )
        self.play(token.animate.move_to(false_path), run_time=1)

        # Converger al fin
        self.play(
            token.animate.move_to(end),
            Create(arrow_end_false),
            false_path.animate.set_opacity(0.3),
            true_path.animate.set_opacity(1),
            run_time=1
        )
        self.play(Create(arrow_end_true), run_time=0.5)

        self.wait(2)
        self.clear_section()

    # ========================================
    # SECCIÓN 3: CICLOS
    # ========================================
    def section_loops(self):
        # Títulos
        fs_title = StyleConfig.get_font_size(0.04)
        title = Text("3. Ciclos (Iteración)", font_size=fs_title, weight=BOLD, color=StyleConfig.TEXT)
        title.move_to(self.layout.get_pos("left", 0.05, 0.92))
        title.align_to(self.layout.left_col, LEFT).shift(RIGHT * 0.3)

        subtitle = Text(
            "Repetir tareas eficientemente",
            font_size=fs_title * 0.6,
            color=StyleConfig.TEXT_DIM
        )
        subtitle.next_to(title, DOWN, aligned_edge=LEFT)

        self.play(Write(title), FadeIn(subtitle), run_time=1)

        # Contador
        counter_label = Text(
            "Iteración:",
            font_size=StyleConfig.get_font_size(0.025),
            color=StyleConfig.TEXT_DIM
        )
        counter_value = Integer(
            0,
            font_size=StyleConfig.get_font_size(0.05),
            color=StyleConfig.WARNING
        )
        counter_value.next_to(counter_label, DOWN, buff=0.15)
        counter_group = VGroup(counter_label, counter_value)
        counter_group.move_to(self.layout.get_pos("left", 0.15, 0.8))

        # Caja del ciclo
        loop_box = RoundedRectangle(
            corner_radius=0.1,
            width=self.layout.col_width * 0.5,
            height=self.layout.col_height * 0.35
        )
        loop_box.set_fill(StyleConfig.SURFACE, 1).set_stroke(StyleConfig.ACCENT, 2.5)
        loop_box.move_to(self.layout.get_pos("left", 0.5, 0.55))

        loop_text = Text(
            "Ejecutar Tarea",
            font_size=StyleConfig.get_font_size(0.028),
            color=StyleConfig.TEXT
        )
        loop_text.move_to(loop_box)

        # Flecha de retorno
        loop_arrow = CurvedArrow(
            loop_box.get_bottom() + LEFT * 0.8,
            loop_box.get_top() + LEFT * 0.8,
            angle=TAU * 0.6
        ).set_stroke(StyleConfig.WARNING, 4)

        # Flecha de salida
        exit_arrow = Arrow(
            loop_box.get_right(),
            loop_box.get_right() + RIGHT * 1.5,
            buff=0.1,
            color=StyleConfig.SUCCESS,
            stroke_width=4
        )
        exit_label = Text(
            "Salida",
            font_size=StyleConfig.get_font_size(0.022),
            color=StyleConfig.SUCCESS,
            weight=BOLD
        )
        exit_label.next_to(exit_arrow, UP, buff=0.15)

        # Token
        token = FlowToken(StyleConfig.WARNING)
        token.move_to(loop_box.get_left() + RIGHT * 0.5)

        # Explicación
        exp_text = Text(
            "Los ciclos repiten una tarea\n"
            "mientras se cumpla una condición.\n\n"
            "Tipos comunes:\n"
            "• FOR: Repite N veces conocidas\n"
            "• WHILE: Repite mientras sea verdadero\n\n"
            "Ejemplo: Comer 5 manzanas\n"
            "Repetir hasta contar 5",
            font_size=StyleConfig.get_font_size(0.02),
            color=StyleConfig.TEXT,
            line_spacing=1.5
        )
        exp_card = Card(exp_text)
        exp_card.move_to(self.layout.right_col.get_center())

        # Animaciones
        self.play(FadeIn(counter_group), run_time=0.8)
        self.play(FadeIn(loop_box), FadeIn(loop_text), run_time=1)
        self.play(Create(loop_arrow), run_time=0.8)
        self.play(Create(exit_arrow), FadeIn(exit_label), run_time=0.8)
        self.play(FadeIn(token), FadeIn(exp_card, shift=RIGHT), run_time=1)

        # Animar iteraciones
        for i in range(1, 5):
            self.play(
                token.animate.move_to(loop_box.get_center()),
                run_time=0.5
            )
            self.play(
                counter_value.animate.set_value(i),
                run_time=0.4
            )
            self.play(
                token.animate.move_to(loop_box.get_left() + RIGHT * 0.5),
                run_time=0.5
            )
            self.wait(0.3)

        # Salida del ciclo
        self.play(
            token.animate.move_to(exit_arrow.get_end()),
            run_time=1.2
        )

        self.wait(2)
        self.clear_section()

    # ========================================
    # SECCIÓN 4: FUNCIONES
    # ========================================
    def section_functions(self):
        # Títulos
        fs_title = StyleConfig.get_font_size(0.04)
        title = Text("4. Funciones", font_size=fs_title, weight=BOLD, color=StyleConfig.TEXT)
        title.move_to(self.layout.get_pos("left", 0.05, 0.92))
        title.align_to(self.layout.left_col, LEFT).shift(RIGHT * 0.3)

        subtitle = Text(
            "Reutilizar lógica",
            font_size=fs_title * 0.6,
            color=StyleConfig.TEXT_DIM
        )
        subtitle.next_to(title, DOWN, aligned_edge=LEFT)

        self.play(Write(title), FadeIn(subtitle), run_time=1)

        # Caja de función (molde)
        func_box = RoundedRectangle(
            corner_radius=0.12,
            width=self.layout.col_width * 0.45,
            height=self.layout.col_height * 0.45
        )
        func_box.set_fill("#1E3A8A", 1).set_stroke(StyleConfig.PURPLE, 2.5)
        func_box.move_to(self.layout.get_pos("left", 0.25, 0.55))

        func_header = Text(
            "FUNCIÓN",
            font_size=StyleConfig.get_font_size(0.028),
            weight=BOLD,
            color=StyleConfig.PURPLE
        )
        func_header.next_to(func_box.get_top(), DOWN, buff=0.25)

        func_input = Text(
            "→ Entrada (Parámetros)",
            font_size=StyleConfig.get_font_size(0.02),
            color=StyleConfig.TEXT
        )
        func_input.move_to(func_box.get_center() + UP * 0.35)

        func_process = Text(
            "⚙ Proceso Interno",
            font_size=StyleConfig.get_font_size(0.02),
            color=StyleConfig.TEXT
        )
        func_process.move_to(func_box.get_center())

        func_output = Text(
            "← Salida (Retorno)",
            font_size=StyleConfig.get_font_size(0.02),
            color=StyleConfig.TEXT
        )
        func_output.move_to(func_box.get_center() + DOWN * 0.35)

        # Llamadas a la función (instancias)
        call_boxes = VGroup()
        call_colors = ["#065F46", "#5B21B6", "#9A3412"]

        for i in range(3):
            call = RoundedRectangle(
                corner_radius=0.08,
                width=self.layout.col_width * 0.25,
                height=self.layout.col_height * 0.08
            )
            call.set_fill(call_colors[i], 0.85).set_stroke(WHITE, 1, 0.3)

            call_text = Text(
                f"Llamada {i + 1}",
                font_size=StyleConfig.get_font_size(0.018),
                color=StyleConfig.TEXT
            )
            call_text.move_to(call)

            call_group = VGroup(call, call_text)
            y_pos = 0.75 - (i * 0.22)
            call_group.move_to(self.layout.get_pos("left", 0.7, y_pos))
            call_boxes.add(call_group)

        # Flechas de llamada
        arrows = VGroup()
        for call in call_boxes:
            arrow = Arrow(
                func_box.get_right(),
                call.get_left(),
                buff=0.15,
                color=StyleConfig.TEXT_DIM,
                stroke_width=2
            )
            arrows.add(arrow)

        # Token que representa la ejecución
        token = FlowToken(StyleConfig.PURPLE)
        token.move_to(call_boxes[0])

        # Explicación
        exp_text = Text(
            "Una función es un bloque de lógica\n"
            "reutilizable que realiza una tarea.\n\n"
            "Ventajas:\n"
            "• Evita repetir código\n"
            "• Organiza el programa\n"
            "• Facilita mantenimiento\n\n"
            "Ejemplo: Función 'sumar'\n"
            "Se puede llamar muchas veces\n"
            "con diferentes números",
            font_size=StyleConfig.get_font_size(0.02),
            color=StyleConfig.TEXT,
            line_spacing=1.5
        )
        exp_card = Card(exp_text)
        exp_card.move_to(self.layout.right_col.get_center())

        # Animaciones
        func_group = VGroup(func_box, func_header, func_input, func_process, func_output)
        self.play(FadeIn(func_group, shift=LEFT * 0.3), run_time=1.5)
        self.play(Create(arrows), run_time=1)
        self.play(FadeIn(call_boxes, shift=RIGHT * 0.3), run_time=1)
        self.play(FadeIn(exp_card, shift=RIGHT), run_time=1)
        self.play(FadeIn(token), run_time=0.5)

        # Animar llamadas
        for i in range(3):
            self.play(token.animate.move_to(call_boxes[i]), run_time=0.8)
            call_boxes[i].set_fill(call_colors[i], 1)
            self.wait(0.4)
            if i < 2:
                call_boxes[i].set_fill(call_colors[i], 0.85)

        # Mostrar token volviendo a la función
        self.play(
            token.animate.move_to(func_box),
            run_time=1
        )

        self.wait(2)
        self.clear_section()

    # ========================================
    # SECCIÓN 5: FLUJO DE DATOS
    # ========================================
    def section_data_flow(self):
        # Títulos
        fs_title = StyleConfig.get_font_size(0.04)
        title = Text("5. Flujo de Datos", font_size=fs_title, weight=BOLD, color=StyleConfig.TEXT)
        title.move_to(self.layout.get_pos("left", 0.05, 0.92))
        title.align_to(self.layout.left_col, LEFT).shift(RIGHT * 0.3)

        subtitle = Text(
            "Transformación de información",
            font_size=fs_title * 0.6,
            color=StyleConfig.TEXT_DIM
        )
        subtitle.next_to(title, DOWN, aligned_edge=LEFT)

        self.play(Write(title), FadeIn(subtitle), run_time=1)

        # Pipeline de datos
        stages = ["Entrada", "Proceso", "Salida"]
        stage_colors = [StyleConfig.ACCENT, StyleConfig.PURPLE, StyleConfig.SUCCESS]

        pipeline = VGroup()
        for i, stage in enumerate(stages):
            box = RoundedRectangle(
                corner_radius=0.1,
                width=self.layout.col_width * 0.25,
                height=self.layout.col_height * 0.1
            )
            box.set_fill(stage_colors[i], 0.9).set_stroke(WHITE, 1.5)

            text = Text(
                stage,
                font_size=StyleConfig.get_font_size(0.022),
                color=StyleConfig.TEXT,
                weight=BOLD
            )
            text.move_to(box)

            group = VGroup(box, text)
            x_pos = 0.15 + (i * 0.35)
            group.move_to(self.layout.get_pos("left", x_pos, 0.55))
            pipeline.add(group)

        # Flechas entre etapas
        pipe_arrows = VGroup()
        for i in range(len(pipeline) - 1):
            arrow = Arrow(
                pipeline[i].get_right(),
                pipeline[i + 1].get_left(),
                buff=0.15,
                color=StyleConfig.TEXT_DIM,
                stroke_width=3
            )
            pipe_arrows.add(arrow)

        # Datos que fluyen
        data_packets = VGroup()
        for i in range(3):
            packet = Circle(radius=0.15, color=StyleConfig.WARNING, fill_opacity=0.8)
            packet.set_fill(StyleConfig.WARNING, 0.8)
            data_packets.add(packet)

        # Explicación
        exp_text = Text(
            "Los datos fluyen a través del programa\n"
            "transformándose en cada etapa.\n\n"
            "Proceso típico:\n"
            "1. ENTRADA: Recibir datos\n"
            "2. PROCESO: Transformar datos\n"
            "3. SALIDA: Mostrar resultados\n\n"
            "Ejemplo: Calculadora\n"
            "Números → Operación → Resultado",
            font_size=StyleConfig.get_font_size(0.02),
            color=StyleConfig.TEXT,
            line_spacing=1.5
        )
        exp_card = Card(exp_text)
        exp_card.move_to(self.layout.right_col.get_center())

        # Animaciones
        self.play(FadeIn(pipeline), Create(pipe_arrows), run_time=1.5)
        self.play(FadeIn(exp_card, shift=RIGHT), run_time=1)

        # Animar flujo de datos
        for i, packet in enumerate(data_packets):
            packet.move_to(pipeline[0].get_left() + LEFT * 0.5)
            self.play(FadeIn(packet), run_time=0.5)
            self.play(
                packet.animate.move_to(pipeline[0]),
                run_time=0.8
            )
            self.play(
                packet.animate.move_to(pipeline[1]),
                run_time=0.8
            )
            packet.set_fill(StyleConfig.PURPLE, 0.8)
            self.play(
                packet.animate.move_to(pipeline[2]),
                run_time=0.8
            )
            packet.set_fill(StyleConfig.SUCCESS, 0.8)
            self.wait(0.3)
            self.play(FadeOut(packet), run_time=0.3)

        self.wait(2)
        self.clear_section()

    # ========================================
    # RESUMEN
    # ========================================
    def summary(self):
        fs_title = StyleConfig.get_font_size(0.05)
        title = Text("Resumen", font_size=fs_title, weight=BOLD, color=StyleConfig.TEXT)
        title.move_to(ORIGIN + UP * 2)

        self.play(Write(title), run_time=1)

        # Grid 2x3 de conceptos - POSICIONES 3D CORRECTAS
        concepts = [
            ("Secuencia", StyleConfig.ACCENT, "→"),
            ("Condicionales", StyleConfig.SUCCESS, "◊"),
            ("Ciclos", StyleConfig.WARNING, "⟳"),
            ("Funciones", StyleConfig.PURPLE, "⚡"),
            ("Datos", StyleConfig.ORANGE, "◉"),
            ("Control", StyleConfig.PINK, "⌬"),
        ]

        cards = VGroup()
        # ✅ Coordenadas 3D (x, y, z)
        positions = [
            (-2.5, 0.8, 0), (0, 0.8, 0), (2.5, 0.8, 0),
            (-2.5, -0.8, 0), (0, -0.8, 0), (2.5, -0.8, 0),
        ]

        for i, (name, color, icon) in enumerate(concepts):
            icon_shape = Text(icon, font_size=60, color=color)
            label = Text(name, font_size=StyleConfig.get_font_size(0.025), color=StyleConfig.TEXT)
            label.next_to(icon_shape, DOWN, buff=0.3)

            content = VGroup(icon_shape, label)
            card = Card(content, color=StyleConfig.SURFACE)
            card.move_to(positions[i])  # ✅ Ahora es un array 3D
            cards.add(card)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.3) for c in cards],
                lag_ratio=0.15
            ),
            run_time=2.5
        )

        # Mensaje final
        final_msg = Text(
            "Dominar estos conceptos es la base\n"
            "para aprender cualquier lenguaje",
            font_size=StyleConfig.get_font_size(0.025),
            color=StyleConfig.TEXT_DIM
        )
        final_msg.next_to(cards, DOWN, buff=0.8)

        self.play(FadeIn(final_msg, shift=UP * 0.3), run_time=1.5)

        self.wait(3)
        self.clear_section()


    # ========================================
    # PANTALLA FINAL
    # ========================================
    def end_screen(self):
        end_text = Text(
            "Fin",
            font_size=StyleConfig.get_font_size(0.12),
            color=StyleConfig.TEXT_DIM
        )

        credit = Text(
            "Lógica de Programación Visual",
            font_size=StyleConfig.get_font_size(0.03),
            color=StyleConfig.ACCENT
        )
        credit.next_to(end_text, DOWN, buff=0.5)

        self.play(FadeIn(end_text), run_time=1.5)
        self.play(FadeIn(credit), run_time=1)
        self.wait(2)


# ==========================================
# 5. CONFIGURACIÓN DE RENDER
# ==========================================
if __name__ == "__main__":
    # Configurar resolución y calidad
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 30
    config.background_color = StyleConfig.BG