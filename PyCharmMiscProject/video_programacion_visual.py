from manim import *


# ==========================================
# CONFIGURACIÓN DE ESTILO PRO
# ==========================================
class Style:
    BG = "#0B0E14"
    ACCENT = "#38BDF8"  # Azul brillante (Lógica/Secuencia)
    SUCCESS = "#22C55E"  # Verde (Verdadero/Éxito)
    ERROR = "#EF4444"  # Rojo (Falso/Error)
    WARNING = "#FBBF24"  # Ámbar (Switch/Variables)
    PURPLE = "#A78BFA"  # Violeta (Bucles)
    ORANGE = "#FB923C"  # Naranja (Anidamiento)
    TEXT_MAIN = "#F8FAFC"  # Blanco roto
    TEXT_DESC = "#94A3B8"  # Gris azulado


# ==========================================
# COMPONENTES DE UI MEJORADOS
# ==========================================
class DetailedExplanation(VGroup):
    """Genera bloques de texto extremadamente detallados para la derecha"""

    def __init__(self, title, paragraphs):
        super().__init__()
        title_text = Text(title, font="Orbitron", weight=BOLD, color=Style.ACCENT, font_size=28)
        title_text.to_edge(UP).shift(RIGHT * 3.0)  # <-- antes 3.5 (movido un poco a la izquierda)

        full_content = VGroup()
        for p in paragraphs:
            txt = Text(p, font_size=16, line_spacing=1.4, color=Style.TEXT_MAIN, t2c={
                "VERDADERO": Style.SUCCESS, "FALSO": Style.ERROR, "mientras": Style.PURPLE,
                "SWITCH": Style.WARNING, "colecciones": Style.SUCCESS
            })
            txt.width = 5.5  # Ancho máximo para la columna derecha
            full_content.add(txt)

        full_content.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        full_content.next_to(title_text, DOWN, buff=0.6).align_to(title_text, LEFT)

        self.add(title_text, full_content)


class LogicNode(VGroup):
    """Nodos visuales para el laboratorio de la izquierda"""

    def __init__(self, label, color=Style.ACCENT):
        super().__init__()
        rect = RoundedRectangle(corner_radius=0.15, width=2.2, height=1.1)
        rect.set_fill(Style.BG, 1).set_stroke(color, 2)
        txt = Text(label, font="Monospace", font_size=18, color=color)
        self.add(rect, txt)


# ==========================================
# ESCENA PRINCIPAL (2 MINUTOS DE DURACIÓN)
# ==========================================
class DetailedProgrammingLogic(Scene):
    def construct(self):
        self.camera.background_color = Style.BG

        # --- 0. INTRODUCCIÓN (0:00 - 0:05) ---
        intro_title = Text("LOGIC_DECODER", font="Monospace").scale(1.2)
        intro_sub = Text("Arquitectura del Pensamiento Computacional", font_size=20, color=Style.TEXT_DESC)
        VGroup(intro_title, intro_sub).arrange(DOWN)

        self.play(Write(intro_title), run_time=1.5)
        self.play(FadeIn(intro_sub, shift=UP), run_time=1)
        self.wait(2)
        self.play(FadeOut(intro_title, intro_sub))

        # --- 1. SECUENCIA (0:05 - 0:15) ---
        expl1 = DetailedExplanation("01. SECUENCIA", [
            "Es la base fundamental de todo algoritmo.",
            "Consiste en ejecutar instrucciones de forma\nlineal, una tras otra, sin saltos.",
            "Como una receta: no puedes freír un huevo\nsin antes haberlo roto."
        ])

        nodes = VGroup(
            LogicNode("PASO 1: INPUT"),
            LogicNode("PASO 2: PROCESS"),
            LogicNode("PASO 3: OUTPUT")
        ).arrange(DOWN, buff=0.7).shift(LEFT * 4.5)

        arrows = VGroup(*[Arrow(nodes[i], nodes[i + 1], color=Style.TEXT_DESC) for i in range(2)])
        token = Dot(color=Style.ACCENT).move_to(nodes[0])

        self.play(FadeIn(expl1), Create(nodes), Create(arrows))
        self.play(token.animate.move_to(nodes[1]), run_time=2)
        self.play(token.animate.move_to(nodes[2]), run_time=2)
        self.wait(2)
        self.play(FadeOut(expl1, nodes, arrows, token))

        # --- 2. CONDICIONALES IF/ELSE (0:15 - 0:35) ---
        expl2 = DetailedExplanation("02. CONDICIONALES", [
            "Las estructuras de control permiten bifurcar\nel flujo del programa basándose en datos.",
            "IF: Si la condición es VERDADERA,\nejecuta el bloque A.",
            "ELSE: Si es FALSA, ejecuta el bloque B.\nEsto asegura que siempre haya una respuesta."
        ])

        diamond = Polygon(UP, RIGHT * 1.5, DOWN, LEFT * 1.5).set_stroke(Style.WARNING, 2).shift(LEFT * 3.5 + UP * 1.8)
        q_text = Text("¿EDAD >= 18?", font_size=16).move_to(diamond)

        path_a = LogicNode("ACCESO PERMITIDO", Style.SUCCESS).shift(LEFT * 5 + DOWN * 1)
        path_b = LogicNode("ACCESO DENEGADO", Style.ERROR).shift(LEFT * 2 + DOWN * 1)

        l1 = Line(diamond.get_left(), path_a.get_top(), color=Style.SUCCESS)
        l2 = Line(diamond.get_right(), path_b.get_top(), color=Style.ERROR)

        self.play(FadeIn(expl2), Create(diamond), Write(q_text))
        self.wait(1)
        self.play(Create(l1), Create(l2), FadeIn(path_a), FadeIn(path_b))

        # Simulación de decisión
        token = Dot(color=Style.TEXT_MAIN).move_to(diamond)
        self.play(token.animate.move_to(path_a), run_time=2)  # Elige el camino verde
        self.play(path_a.animate.scale(1.1).set_stroke(opacity=1), run_time=0.5)
        self.wait(3)
        self.play(FadeOut(expl2, diamond, q_text, path_a, path_b, l1, l2, token))

        # --- 3. BUCLES: WHILE (0:50 - 1:10) ---
        expl3 = DetailedExplanation("03. BUCLE WHILE", [
            "Se utiliza cuando NO sabemos de antemano\ncuántas veces debemos repetir una tarea.",
            "La estructura 'mientras' reevalúa la condición\nen cada ciclo.",
            "¡Peligro!: Si la condición nunca es FALSA,\nel programa caerá en un bucle infinito."
        ])

        bucket = RoundedRectangle(width=2, height=2.5, corner_radius=0.1).shift(LEFT * 3.5)
        water = Rectangle(width=1.9, height=0.1, fill_color=Style.PURPLE, fill_opacity=0.8).move_to(
            bucket.get_bottom()).shift(UP * 0.1)

        cond_box = Text("¿ESTÁ VACÍO?", font_size=18, color=Style.PURPLE).next_to(bucket, UP)

        self.play(FadeIn(expl3), Create(bucket), Create(water), Write(cond_box))

        # Animación de llenado (mientras no esté lleno)
        for i in range(1, 6):
            self.play(water.animate.stretch_to_fit_height(0.4 * i).move_to(bucket.get_bottom()).shift(UP * (0.2 * i)),
                      run_time=0.6)
            self.play(Indicate(cond_box))

        self.wait(2)
        self.play(FadeOut(expl3, bucket, water, cond_box))

        # --- 4. BUCLES: FOR EACH (1:25 - 1:40) ---
        expl4 = DetailedExplanation("04. FOR EACH", [
            "Especializado en recorrer 'colecciones'.",
            "Procesa automáticamente cada ítem de una\nlista de principio a fin.",
            "Es más seguro y legible porque evita errores\nen el manejo de índices manuales."
        ])

        items = VGroup(*[Circle(radius=0.3, color=Style.ACCENT) for _ in range(5)]).arrange(RIGHT, buff=0.4).shift(
            LEFT * 3.5)
        scanner = Square(side_length=0.8, color=Style.SUCCESS).move_to(items[0])

        self.play(FadeIn(expl4), Create(items))
        self.play(Create(scanner))

        for item in items:
            self.play(scanner.animate.move_to(item), run_time=0.5)
            self.play(item.animate.set_fill(Style.SUCCESS, opacity=0.8), run_time=0.3)

        self.wait(2)
        self.play(FadeOut(expl4, items, scanner))

        # --- 5. ANIDAMIENTO (1:40 - 1:55) ---
        expl5 = DetailedExplanation("05. ANIDAMIENTO", [
            "Es la técnica de colocar una estructura\ndentro de otra para resolver problemas complejos.",
            "Ejemplo: Un bucle que recorre una lista,\ny un condicional que filtra ciertos elementos.",
            "Regla de oro: No anides más de 3 niveles\nsi quieres mantener tu código legible."
        ])

        outer_box = Rectangle(width=4, height=3, color=Style.ORANGE, stroke_width=4).shift(LEFT * 3.5)
        inner_circle = Circle(radius=0.7, color=Style.PURPLE).move_to(outer_box)
        inner_txt = Text("LOOP", font_size=14).move_to(inner_circle)
        outer_txt = Text("IF", font_size=14).next_to(outer_box, UP, buff=-0.3)

        self.play(FadeIn(expl5), Create(outer_box), Write(outer_txt))
        self.play(Create(inner_circle), Write(inner_txt), run_time=1.5)

        # Efecto de rotación para mostrar actividad
        self.play(Rotate(inner_circle, angle=TAU), run_time=2)
        self.wait(2)
        self.play(FadeOut(expl5, outer_box, inner_circle, inner_txt, outer_txt))

        # --- 6. CIERRE (1:55 - 2:05) ---
        final_logo = Text("LOGIC_DECODER", font="Monospace", color=Style.ACCENT).scale(1.2)
        final_msg = Text("La sintaxis cambia, la lógica permanece.", font_size=22, color=Style.TEXT_DESC)
        VGroup(final_logo, final_msg).arrange(DOWN, buff=0.5)

        self.play(Write(final_logo))
        self.play(FadeIn(final_msg, shift=UP))
        self.play(Flash(final_logo, color=Style.SUCCESS, line_length=0.5))
        self.wait(4)