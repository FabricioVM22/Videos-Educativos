from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 15


class ProgramacionVisual(Scene):
    def construct(self):
        # ========================================
        # PALETA DE COLORES (corregida)
        # ========================================
        C_BG = "#0B0F19"
        C_SURFACE = "#1E293B"
        C_SURFACE_2 = "#334155"
        C_TEXT = "#F8FAFC"
        C_TEXT_DIM = "#94A3B8"
        C_ACCENT = "#38BDF8"
        C_SUCCESS = "#4ADE80"
        C_WARNING = "#FBBF24"
        C_ERROR = "#F87171"
        C_PURPLE = "#A78BFA"

        # ========================================
        # LAYOUT RESPONSIVE (SAFE AREA + COLUMNAS)
        # ========================================
        FW = config.frame_width
        FH = config.frame_height

        SAFE_MARGIN_X = 0.85
        SAFE_MARGIN_Y = 0.65

        safe = Rectangle(
            width=FW - 2 * SAFE_MARGIN_X,
            height=FH - 2 * SAFE_MARGIN_Y,
        ).move_to(ORIGIN)

        left_area = Rectangle(width=safe.width / 2, height=safe.height).move_to(
            safe.get_left() + RIGHT * (safe.width / 4)
        )
        right_area = Rectangle(width=safe.width / 2, height=safe.height).move_to(
            safe.get_right() + LEFT * (safe.width / 4)
        )

        def anchor_in(area: Mobject, mob: Mobject, x: float, y: float, *, align_edge=ORIGIN) -> Mobject:
            """
            Posiciona mob dentro de 'area' usando coords normalizadas:
              x: 0..1 (izq->der), y: 0..1 (abajo->arriba)
            """
            x = np.clip(x, 0.0, 1.0)
            y = np.clip(y, 0.0, 1.0)
            target = area.get_corner(DL) + RIGHT * (area.width * x) + UP * (area.height * y)

            if align_edge is ORIGIN:
                mob.move_to(target)
                return mob

            if align_edge is UL:
                mob.move_to(target, aligned_edge=UL)
            elif align_edge is UR:
                mob.move_to(target, aligned_edge=UR)
            elif align_edge is DL:
                mob.move_to(target, aligned_edge=DL)
            elif align_edge is DR:
                mob.move_to(target, aligned_edge=DR)
            else:
                mob.move_to(target)
            return mob

        def clamp_to_area(area: Mobject, group: Mobject, padding: float = 0.08) -> Mobject:
            """Asegura que 'group' quede completamente dentro de 'area' (con padding)."""
            left_bound = area.get_left()[0] + padding
            right_bound = area.get_right()[0] - padding
            bottom_bound = area.get_bottom()[1] + padding
            top_bound = area.get_top()[1] - padding

            dx = 0.0
            dy = 0.0

            if group.get_left()[0] < left_bound:
                dx = left_bound - group.get_left()[0]
            if group.get_right()[0] > right_bound:
                dx = right_bound - group.get_right()[0]

            if group.get_bottom()[1] < bottom_bound:
                dy = bottom_bound - group.get_bottom()[1]
            if group.get_top()[1] > top_bound:
                dy = top_bound - group.get_top()[1]

            group.shift(RIGHT * dx + UP * dy)
            return group

        # ========================================
        # FONDO (RESPONSIVE)
        # ========================================
        bg = Rectangle(width=FW, height=FH).set_fill(C_BG, 1).set_stroke(width=0)
        self.add(bg)

        divider = Line(safe.get_top(), safe.get_bottom()).set_stroke(C_TEXT_DIM, 1, 0.03)
        self.add(divider)

        # ========================================
        # FUNCIONES AUXILIARES (RESPONSIVE)
        # ========================================

        def make_title(text: str) -> Text:
            """Título anclado a la esquina superior izquierda del SAFE AREA."""
            t = Text(text, font_size=36, weight=BOLD, color=C_TEXT)
            t.set_max_width(left_area.width * 0.96)
            anchor_in(left_area, t, 0.02, 0.98, align_edge=UL).shift(DOWN * 0.02 + RIGHT * 0.02)
            return t

        def make_subtitle(text: str) -> Text:
            """Subtítulo debajo del título (en la columna izquierda)."""
            s = Text(text, font_size=20, color=C_TEXT_DIM)
            s.set_max_width(left_area.width * 0.96)
            anchor_in(left_area, s, 0.02, 0.90, align_edge=UL).shift(DOWN * 0.02 + RIGHT * 0.02)
            return s

        def make_card(content: Mobject, color: str = C_SURFACE, max_width: float | None = None, position=None) -> VGroup:
            """Tarjeta con límites estrictos (max_width opcional)."""
            padding_x = 0.5
            padding_y = 0.35

            if max_width is not None:
                content.set_max_width(max_width - 2 * padding_x)

            card_rect = RoundedRectangle(
                corner_radius=0.1,
                width=content.width + 2 * padding_x,
                height=content.height + 2 * padding_y
            )
            card_rect.set_fill(color, 0.95).set_stroke(C_TEXT, 1, 0.1)
            card_rect.move_to(content)

            shadow = card_rect.copy()
            shadow.set_fill(BLACK, 0.3).set_stroke(width=0)
            shadow.shift(DOWN * 0.03 + RIGHT * 0.03)
            shadow.z_index = -1

            card = VGroup(shadow, card_rect, content)
            if position is not None:
                card.move_to(position)
            return card

        def make_box(text: str, width: float = 2.2, height: float = 0.65,
                     color: str = C_SURFACE_2, stroke_color: str = C_TEXT,
                     font_size: int = 20) -> VGroup:
            """Caja de proceso."""
            box = RoundedRectangle(corner_radius=0.08, width=width, height=height)
            box.set_fill(color, 1).set_stroke(stroke_color, 1.2, 0.4)
            txt = Text(text, font_size=font_size, color=C_TEXT)
            txt.move_to(box)
            return VGroup(box, txt)

        def make_arrow(start, end, color: str = C_TEXT_DIM, stroke_width: int = 3) -> Arrow:
            """Flecha."""
            return Arrow(start, end, buff=0.1, stroke_width=stroke_width,
                         color=color, tip_length=0.15)

        def make_token(color: str = C_WARNING) -> Dot:
            """Token."""
            return Dot(radius=0.08, color=color).set_stroke(WHITE, 1.2)

        def make_explanation_card(text: str) -> VGroup:
            """Tarjeta de explicación anclada a la columna derecha (responsive)."""
            explanation = Text(text, font_size=18, color=C_TEXT, line_spacing=1.35)
            explanation.set_max_width(right_area.width * 0.92)
            card = make_card(explanation, C_SURFACE, max_width=right_area.width * 0.96)
            anchor_in(right_area, card, 0.50, 0.52, align_edge=ORIGIN)
            return card

        def constrain_to_left_column(group: Mobject) -> Mobject:
            return clamp_to_area(left_area, group, padding=0.10)

        def constrain_to_right_column(group: Mobject) -> Mobject:
            return clamp_to_area(right_area, group, padding=0.10)

        # ========================================
        # INTRODUCCIÓN (RESPONSIVE)
        # ========================================

        main_title = Text("Lógica de Programación", font_size=48, weight=BOLD, color=C_TEXT)
        main_subtitle = Text("Fundamentos visuales para comprender el código",
                             font_size=28, color=C_TEXT_DIM)
        main_subtitle.next_to(main_title, DOWN, buff=0.35)

        intro_group = VGroup(main_title, main_subtitle).move_to(ORIGIN)

        self.play(FadeIn(main_title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(main_subtitle, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(intro_group, shift=UP * 0.5), run_time=0.8)
        self.remove(intro_group)

        # ========================================
        # SECCIÓN 1: CONDICIONALES
        # ========================================

        def section_conditionals():
            title = make_title("1. Estructuras Condicionales")
            subtitle = make_subtitle("El programa toma decisiones")

            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3), run_time=1.0)
            self.wait(0.4)

            # === COLUMNA IZQUIERDA: DIAGRAMA (RESPONSIVE + FLECHAS ALWAYS_REDRAW) ===
            start_box = make_box("Inicio", width=1.8, height=0.6)
            anchor_in(left_area, start_box, 0.18, 0.55)

            token = make_token()
            token.move_to(start_box.get_center())

            decision = Polygon(UP * 0.8, RIGHT * 1.1, DOWN * 0.8, LEFT * 1.1)
            decision.set_fill(C_SURFACE, 1).set_stroke(C_ACCENT, 2, 0.8)
            anchor_in(left_area, decision, 0.52, 0.55)

            decision_text = Text("¿Condición?", font_size=19, color=C_TEXT)
            decision_text.move_to(decision)

            true_box = make_box("Ejecutar A", width=2.0, height=0.6,
                                color="#064E3B", stroke_color=C_SUCCESS)
            anchor_in(left_area, true_box, 0.82, 0.72)

            false_box = make_box("Ejecutar B", width=2.0, height=0.6,
                                 color="#450A0A", stroke_color=C_ERROR)
            anchor_in(left_area, false_box, 0.82, 0.38)

            arrow_start = always_redraw(
                lambda: make_arrow(start_box.get_right(), decision.get_left(), color=C_TEXT_DIM)
            )
            arrow_true = always_redraw(
                lambda: make_arrow(decision.get_corner(UR) + RIGHT * 0.05, true_box.get_left(),
                                   color=C_SUCCESS, stroke_width=3)
            )
            arrow_false = always_redraw(
                lambda: make_arrow(decision.get_corner(DR) + RIGHT * 0.05, false_box.get_left(),
                                   color=C_ERROR, stroke_width=3)
            )

            label_true = always_redraw(lambda: Text("SÍ", font_size=16, color=C_SUCCESS, weight=BOLD).next_to(arrow_true, UP, buff=0.06))
            label_false = always_redraw(lambda: Text("NO", font_size=16, color=C_ERROR, weight=BOLD).next_to(arrow_false, DOWN, buff=0.06))

            diagram = VGroup(
                start_box, token, decision, decision_text,
                true_box, false_box,
                arrow_start, arrow_true, arrow_false,
                label_true, label_false
            )
            diagram = constrain_to_left_column(diagram)

            explanation_card = make_explanation_card(
                "Una condición divide el flujo en caminos exclusivos.\n\n"
                "Solo UN camino se ejecuta en cada evaluación."
            )
            explanation_card = constrain_to_right_column(explanation_card)

            self.play(FadeIn(start_box), FadeIn(token), run_time=0.6)
            self.play(Create(arrow_start), run_time=0.5)
            self.play(FadeIn(decision), FadeIn(decision_text), run_time=0.6)
            self.play(FadeIn(explanation_card, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(0.8)

            self.play(token.animate.move_to(decision.get_center()), run_time=0.8)
            self.wait(0.4)

            self.play(Create(arrow_true), FadeIn(true_box), FadeIn(label_true), run_time=0.8)
            self.play(token.animate.move_to(true_box.get_center()), run_time=1.0)
            self.wait(1.2)

            self.play(token.animate.move_to(decision.get_center()),
                      true_box.animate.set_opacity(0.25), run_time=0.6)

            self.play(Create(arrow_false), FadeIn(false_box), FadeIn(label_false), run_time=0.8)
            self.play(token.animate.move_to(false_box.get_center()), run_time=1.0)
            self.wait(1.5)

            self.play(FadeOut(VGroup(title, subtitle, diagram, explanation_card), shift=UP * 0.5), run_time=0.8)

        section_conditionals()

        # ========================================
        # SECCIÓN 2: CONTROL DE FLUJO
        # ========================================

        def section_flow_control():
            title = make_title("2. Control de Flujo")
            subtitle = make_subtitle("El orden determina el resultado")

            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3), run_time=1.0)
            self.wait(0.4)

            steps = VGroup()
            step_labels = ["Entrada", "Procesamiento", "Validación"]

            for i, label in enumerate(step_labels):
                step = make_box(label, width=2.6, height=0.6)
                anchor_in(left_area, step, 0.25, 0.70 - i * 0.20)
                steps.add(step)

            exit_box = make_box("⚠ Salida", width=2.2, height=0.6,
                                color="#7F1D1D", stroke_color=C_ERROR)
            anchor_in(left_area, exit_box, 0.74, 0.50)

            arrow_1 = always_redraw(lambda: make_arrow(steps[0].get_bottom(), steps[1].get_top(), color=C_TEXT_DIM, stroke_width=3))
            arrow_2 = always_redraw(lambda: make_arrow(steps[1].get_bottom(), steps[2].get_top(), color=C_TEXT_DIM, stroke_width=3))
            arrow_exit = always_redraw(lambda: make_arrow(steps[1].get_right(), exit_box.get_left(), color=C_ERROR, stroke_width=3))

            token = make_token()
            token.move_to(steps[0].get_center())

            diagram = VGroup(steps, exit_box, arrow_1, arrow_2, arrow_exit, token)
            diagram = constrain_to_left_column(diagram)

            explanation_card = make_explanation_card(
                "El flujo sigue un orden definido, pero puede interruptirse ante condiciones excepcionales.\n\n"
                "Esto permite manejar errores o casos especiales."
            )
            explanation_card = constrain_to_right_column(explanation_card)

            self.play(FadeIn(steps, shift=RIGHT * 0.2), run_time=0.8)
            self.play(Create(arrow_1), Create(arrow_2), run_time=0.6)
            self.play(Create(arrow_exit), FadeIn(exit_box), run_time=0.6)
            self.play(FadeIn(token), run_time=0.4)
            self.play(FadeIn(explanation_card, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(0.8)

            self.play(token.animate.move_to(steps[0].get_center()), run_time=0.5)
            self.wait(0.4)
            self.play(token.animate.move_to(steps[1].get_center()), run_time=0.8)
            self.wait(0.6)
            self.play(token.animate.move_to(exit_box.get_center()), run_time=1.0)
            self.wait(1.5)

            self.play(FadeOut(VGroup(title, subtitle, diagram, explanation_card), shift=UP * 0.5), run_time=0.8)

        section_flow_control()

        # ========================================
        # SECCIÓN 3: CICLOS / ITERACIÓN (CORREGIDA)
        # ========================================

        def section_loops():
            title = make_title("3. Iteración (Ciclos)")
            subtitle = make_subtitle("Repetición controlada de tareas")

            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3), run_time=1.2)
            self.wait(0.5)

            # === COLUMNA IZQUIERDA: DIAGRAMA (todo debe estar en LEFT) ===
            counter_label = Text("Iteración:", font_size=24, color=C_TEXT_DIM)
            counter_value = Integer(0, font_size=48, color=C_WARNING)
            counter_value.next_to(counter_label, DOWN, buff=0.2)
            counter_group = VGroup(counter_label, counter_value)
            counter_group.move_to(LEFT * 6.5)  # Más a la izquierda

            # Caja del bucle (CENTRO-IZQUIERDA, no RIGHT)
            loop_box = RoundedRectangle(corner_radius=0.12, width=4.0, height=2.5)
            loop_box.set_fill(C_SURFACE, 1).set_stroke(C_ACCENT, 2, 0.5)
            loop_box.move_to(LEFT * 2.0)  # Cambiado de RIGHT * 1.5 a LEFT * 2.0

            loop_content = Text("Ejecutar Tarea", font_size=24, color=C_TEXT)
            loop_content.move_to(loop_box)

            # Flecha curva de retorno (ajustada)
            loop_arrow = CurvedArrow(
                loop_box.get_bottom() + LEFT * 1.7,
                loop_box.get_top() + LEFT * 1.7,
                angle=TAU * 0.58,
            ).set_stroke(C_WARNING, 4, 0.9)

            # Flecha de salida (más corta, sin cruzar al lado derecho)
            exit_arrow = Arrow(
                loop_box.get_right(),
                loop_box.get_right() + RIGHT * 1.5,
                buff=0.1,
                color=C_SUCCESS,
                stroke_width=4
            )
            exit_label = Text("Salida", font_size=20, color=C_SUCCESS, weight=BOLD)
            exit_label.next_to(exit_arrow, UP, buff=0.1)

            token = make_token(C_WARNING)
            token.move_to(loop_box.get_left() + RIGHT * 0.6)

            # === COLUMNA DERECHA: EXPLICACIÓN ===
            explanation = Text(
                "El ciclo repite mientras la condición\n"
                "sea verdadera. La salida previene\n"
                "bucles infinitos.",
                font_size=22, color=C_TEXT, line_spacing=1.4
            )
            explanation_card = make_card(explanation, C_SURFACE)
            explanation_card.move_to(RIGHT * 4.0)  # Columna derecha

            diagram = VGroup(
                counter_group, loop_box, loop_content, loop_arrow,
                exit_arrow, exit_label, token
            )

            # Asegurar que el diagrama no cruce el centro
            if diagram.get_right()[0] > -0.5:
                diagram.shift(LEFT * (diagram.get_right()[0] + 0.5))

            # Animación de entrada
            self.play(FadeIn(counter_group), run_time=0.8)
            self.play(FadeIn(loop_box), FadeIn(loop_content), run_time=0.8)
            self.play(Create(loop_arrow), run_time=0.8)
            self.play(Create(exit_arrow), FadeIn(exit_label), run_time=0.8)
            self.play(FadeIn(token), run_time=0.5)
            self.play(FadeIn(explanation_card, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(1.0)

            # Animación de iteraciones
            max_iterations = 4
            for i in range(1, max_iterations + 1):
                self.play(token.animate.move_to(loop_box.get_center()), run_time=0.4)
                self.play(counter_value.animate.set_value(i), run_time=0.3)
                self.play(token.animate.move_to(loop_box.get_left() + RIGHT * 0.6), run_time=0.4)
                self.wait(0.2)

            self.play(token.animate.move_to(exit_arrow.get_end()), run_time=1.0)
            self.wait(1.5)

            self.play(
                FadeOut(VGroup(title, subtitle, diagram, explanation_card), shift=UP * 0.5),
                run_time=1.0
            )

        section_loops()

        # ========================================
        # SECCIÓN 4: CLASES Y OBJETOS (CORREGIDA)
        # ========================================

        def section_classes():
            title = make_title("4. Clases y Objetos")
            subtitle = make_subtitle("Moldes e instancias")

            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3), run_time=1.2)
            self.wait(0.5)

            # === COLUMNA IZQUIERDA: DIAGRAMA ===
            class_box = RoundedRectangle(corner_radius=0.12, width=3.8, height=2.8)
            class_box.set_fill("#1E3A8A", 1).set_stroke(C_PURPLE, 2.5, 0.8)
            class_box.move_to(LEFT * 6.0)  # Más a la izquierda

            class_title = Text("CLASE", font_size=28, weight=BOLD, color=C_PURPLE)
            class_title.next_to(class_box.get_top(), DOWN, buff=0.2)

            class_attrs = Text("• Atributos", font_size=22, color=C_TEXT)
            class_attrs.move_to(class_box.get_center() + UP * 0.4)

            class_methods = Text("• Métodos", font_size=22, color=C_TEXT)
            class_methods.move_to(class_box.get_center() + DOWN * 0.4)

            class_group = VGroup(class_box, class_title, class_attrs, class_methods)

            # Objetos (IZQUIERDA-CENTRO, no RIGHT)
            def create_object(name: str, position, color: str) -> VGroup:
                obj_box = RoundedRectangle(corner_radius=0.1, width=2.5, height=0.7)
                obj_box.set_fill(color, 0.85).set_stroke(WHITE, 1, 0.3)
                obj_text = Text(name, font_size=22, color=C_TEXT, weight=BOLD)
                obj_text.move_to(obj_box)
                return VGroup(obj_box, obj_text).move_to(position)

            # Cambiado de RIGHT * 5.0 a LEFT * 1.5/2.5/3.5
            obj_a = create_object("Objeto A", LEFT * 1.5 + UP * 1.6, "#065F46")
            obj_b = create_object("Objeto B", LEFT * 2.5 + DOWN * 0.0, "#5B21B6")
            obj_c = create_object("Objeto C", LEFT * 1.5 + DOWN * 1.6, "#9A3412")

            objects_group = VGroup(obj_a, obj_b, obj_c)

            # Flechas de instanciación (más cortas)
            arrow_a = Arrow(class_box.get_right(), obj_a.get_left(),
                            buff=0.1, color=C_TEXT_DIM, stroke_width=2)
            arrow_b = Arrow(class_box.get_right(), obj_b.get_left(),
                            buff=0.1, color=C_TEXT_DIM, stroke_width=2)
            arrow_c = Arrow(class_box.get_right(), obj_c.get_left(),
                            buff=0.1, color=C_TEXT_DIM, stroke_width=2)

            arrows_group = VGroup(arrow_a, arrow_b, arrow_c)

            # === COLUMNA DERECHA: EXPLICACIÓN ===
            explanation = Text(
                "La CLASE define la estructura.\n"
                "Cada OBJETO es una instancia\n"
                "independiente con su propio estado.",
                font_size=22, color=C_TEXT, line_spacing=1.4
            )
            explanation_card = make_card(explanation, C_SURFACE)
            explanation_card.move_to(RIGHT * 4.0)  # Columna derecha

            diagram = VGroup(class_group, objects_group, arrows_group)

            # Asegurar que el diagrama no cruce el centro
            if diagram.get_right()[0] > -0.5:
                diagram.shift(LEFT * (diagram.get_right()[0] + 0.5))

            # Animación de entrada
            self.play(FadeIn(class_group, shift=LEFT * 0.2), run_time=1.0)
            self.wait(0.5)
            self.play(Create(arrows_group), run_time=0.8)
            self.play(FadeIn(objects_group, shift=RIGHT * 0.2), run_time=1.0)
            self.play(FadeIn(explanation_card, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(1.5)

            # Demostrar independencia
            self.play(obj_a.animate.scale(1.1), run_time=0.5)
            self.wait(0.3)
            self.play(obj_a.animate.scale(1 / 1.1), obj_b.animate.scale(1.1), run_time=0.5)
            self.wait(0.3)
            self.play(obj_b.animate.scale(1 / 1.1), obj_c.animate.scale(1.1), run_time=0.5)
            self.wait(1.2)

            self.play(
                FadeOut(VGroup(title, subtitle, diagram, explanation_card), shift=UP * 0.5),
                run_time=1.0
            )

        section_classes()
        # ========================================
        # SECCIÓN 5: RESUMEN
        # ========================================

        def section_summary():
            title = make_title("Resumen de Conceptos")
            subtitle = make_subtitle("Cuatro pilares fundamentales")

            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3), run_time=1.0)
            self.wait(0.4)

            # === COLUMNA IZQUIERDA: GRID 2x2 ===
            concepts = VGroup()

            # Condicionales
            cond_icon = Polygon(UP * 0.22, RIGHT * 0.35, DOWN * 0.22, LEFT * 0.35)
            cond_icon.set_fill(C_ACCENT, 0.3).set_stroke(C_ACCENT, 2)
            cond_text = Text("Condicionales", font_size=17, color=C_TEXT)
            cond_group = VGroup(cond_icon, cond_text).arrange(DOWN, buff=0.12)
            cond_card = make_card(cond_group, C_SURFACE, max_width=3.0)
            cond_card.move_to(LEFT * 4.2 + UP * 1.1)

            # Flujo
            flow_icon = Rectangle(width=0.7, height=0.5, color=C_TEXT_DIM)
            flow_icon.set_fill(C_TEXT_DIM, 0.3)
            flow_text = Text("Flujo", font_size=17, color=C_TEXT)
            flow_group = VGroup(flow_icon, flow_text).arrange(DOWN, buff=0.12)
            flow_card = make_card(flow_group, C_SURFACE, max_width=3.0)
            flow_card.move_to(LEFT * 0.8 + UP * 1.1)

            # Ciclos
            loop_icon = Circle(radius=0.27, color=C_WARNING)
            loop_icon.set_fill(C_WARNING, 0.3).set_stroke(C_WARNING, 2)
            loop_text = Text("Ciclos", font_size=17, color=C_TEXT)
            loop_group = VGroup(loop_icon, loop_text).arrange(DOWN, buff=0.12)
            loop_card = make_card(loop_group, C_SURFACE, max_width=3.0)
            loop_card.move_to(LEFT * 4.2 + DOWN * 1.1)

            # Objetos
            obj_icon = RoundedRectangle(width=0.65, height=0.65, corner_radius=0.09, color=C_PURPLE)
            obj_icon.set_fill(C_PURPLE, 0.3).set_stroke(C_PURPLE, 2)
            obj_text = Text("Objetos", font_size=17, color=C_TEXT)
            obj_group = VGroup(obj_icon, obj_text).arrange(DOWN, buff=0.12)
            obj_card = make_card(obj_group, C_SURFACE, max_width=3.0)
            obj_card.move_to(LEFT * 0.8 + DOWN * 1.1)

            concepts.add(cond_card, flow_card, loop_card, obj_card)

            concepts = constrain_to_left_column(concepts)

            # === COLUMNA DERECHA: CIERRE ===
            closing = Text(
                "Comprender la lógica es el primer paso\n"
                "para dominar cualquier lenguaje.",
                font_size=19, color=C_TEXT, line_spacing=1.4, weight=BOLD
            )
            closing_card = make_card(closing, C_SURFACE, max_width=6.2)

            anchor_in(right_area, closing_card, 0.50, 0.52)
            closing_card = constrain_to_right_column(closing_card)

            self.play(FadeIn(cond_card, shift=UP * 0.2), run_time=0.6)
            self.wait(0.2)
            self.play(FadeIn(flow_card, shift=UP * 0.2), run_time=0.6)
            self.wait(0.2)
            self.play(FadeIn(loop_card, shift=DOWN * 0.2), run_time=0.6)
            self.wait(0.2)
            self.play(FadeIn(obj_card, shift=DOWN * 0.2), run_time=0.6)
            self.wait(0.4)
            self.play(FadeIn(closing_card, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(3.5)

            self.play(FadeOut(VGroup(title, subtitle, concepts, closing_card), shift=UP * 0.5), run_time=1.2)

        section_summary()

        # ========================================
        # CIERRE
        # ========================================

        end_text = Text("Fin", font_size=52, color=C_TEXT_DIM)
        self.play(FadeIn(end_text), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(end_text), run_time=0.8)