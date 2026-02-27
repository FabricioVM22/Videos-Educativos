from manim import *

class ProgramacionVisual(Scene):
    def construct(self):
        # ========================================
        # PALETA DE COLORES (Tema Universitario Moderno)
        # ========================================
        C_BG = "#0B0F19"  # Fondo principal (azul muy oscuro)
        C_SURFACE = "#cfd5e8"  # Superficies/tarjetas
        C_SURFACE_2 = "#1E293B"  # Superficies secundarias
        C_TEXT = "#F8FAFC"  # Texto principal
        C_TEXT_DIM = "#94A3B8"  # Texto secundario
        C_ACCENT = "#38BDF8"  # Azul cielo (destacados)
        C_SUCCESS = "#4ADE80"  # Verde (éxito/verdadero)
        C_WARNING = "#FBBF24"  # Ámbar (atención)
        C_ERROR = "#F87171"  # Rojo suave (error/falso)
        C_PURPLE = "#A78BFA"  # Violeta (clases/objetos)

        # ========================================
        # CONFIGURACIÓN DE ESPACIADO
        # ========================================
        MARGIN_X = 2.0  # Margen horizontal seguro
        MARGIN_Y = 1.8  # Margen vertical seguro
        ELEM_SPACING = 0.8  # Espacio entre elementos

        # ========================================
        # FONDO Y MARCO
        # ========================================
        bg = Rectangle(width=16, height=9).set_fill(C_BG, 1).set_stroke(width=0)

        # Marco decorativo sutil (no invade el contenido)
        frame = Rectangle(
            width=16 - 2 * MARGIN_X,
            height=9 - 2 * MARGIN_Y
        ).set_fill(opacity=0).set_stroke(C_TEXT_DIM, 1, 0.08)
        frame.move_to(ORIGIN)

        self.add(bg, frame)

        # ========================================
        # FUNCIONES AUXILIARES
        # ========================================

        def make_title(text: str) -> Text:
            """Título principal de sección"""
            t = Text(text, font_size=48, weight=BOLD, color=C_TEXT)
            t.set_max_width(16 - 2 * MARGIN_X - 1)
            return t.to_edge(UP).shift(DOWN * MARGIN_Y * 0.6)

        def make_subtitle(text: str) -> Text:
            """Subtítulo descriptivo"""
            s = Text(text, font_size=28, color=C_TEXT_DIM)
            s.set_max_width(16 - 2 * MARGIN_X - 1)
            return s.to_edge(UP).shift(DOWN * MARGIN_Y * 0.6 + DOWN * 0.6)

        def make_card(content: Mobject, color: str = C_SURFACE) -> VGroup:
            """
            Tarjeta con padding generoso.
            El contenido NUNCA toca los bordes.
            """
            padding_x = 1.0
            padding_y = 0.6

            card_rect = RoundedRectangle(
                corner_radius=0.12,
                width=content.width + 2 * padding_x,
                height=content.height + 2 * padding_y
            )
            card_rect.set_fill(color, 0.95).set_stroke(C_TEXT, 1, 0.12)
            card_rect.move_to(content)

            # Sombra sutil para profundidad
            shadow = card_rect.copy()
            shadow.set_fill(BLACK, 0.3).set_stroke(width=0)
            shadow.shift(DOWN * 0.05 + RIGHT * 0.05)
            shadow.z_index = -1

            return VGroup(shadow, card_rect, content)

        def make_box(text: str, width: float = 3.0, height: float = 1.0,
                     color: str = C_SURFACE_2, stroke_color: str = C_TEXT,
                     font_size: int = 28) -> VGroup:
            """Caja de proceso con texto centrado"""
            box = RoundedRectangle(corner_radius=0.1, width=width, height=height)
            box.set_fill(color, 1).set_stroke(stroke_color, 1.5, 0.4)
            txt = Text(text, font_size=font_size, color=C_TEXT)
            txt.move_to(box)
            return VGroup(box, txt)

        def make_arrow(start: np.ndarray, end: np.ndarray,
                       color: str = C_TEXT_DIM, stroke_width: int = 4) -> Arrow:
            """Flecha con espacio (buff) para evitar superposiciones"""
            return Arrow(start, end, buff=0.15, stroke_width=stroke_width, color=color)

        def make_token(color: str = C_WARNING) -> Dot:
            """Token animado que representa el flujo"""
            return Dot(radius=0.12, color=color).set_stroke(WHITE, 2)

        # ========================================
        # SECUENCIA DE INTRODUCCIÓN
        # ========================================

        # Título del video
        main_title = Text("Lógica de Programación", font_size=64, weight=BOLD, color=C_TEXT)
        main_subtitle = Text("Fundamentos visuales para comprender el código",
                             font_size=36, color=C_TEXT_DIM)
        main_subtitle.next_to(main_title, DOWN, buff=0.5)

        intro_group = VGroup(main_title, main_subtitle).move_to(ORIGIN)

        self.play(FadeIn(main_title, shift=UP * 0.3), run_time=1.2)
        self.play(FadeIn(main_subtitle, shift=UP * 0.3), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(intro_group, shift=UP * 0.5), run_time=1.0)
        self.remove(intro_group)

        # ========================================
        # SECCIÓN 1: CONDICIONALES
        # ========================================

        def section_conditionals():
            title = make_title("1. Estructuras Condicionales")
            subtitle = make_subtitle("El programa toma decisiones según condiciones")

            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3), run_time=1.2)
            self.wait(0.5)

            # Layout: Izquierda (inicio) -> Centro (decisión) -> Derecha (ramas separadas)
            # Usamos todo el ancho disponible con márgenes claros

            # Nodo de inicio
            start_box = make_box("Inicio", width=2.5, height=0.9,
                                 color=C_SURFACE_2, stroke_color=C_TEXT_DIM)
            start_box.move_to(LEFT * 6.0)

            # Token de flujo
            token = make_token(C_WARNING)
            token.move_to(start_box.get_center())

            # Rombo de decisión (centro)
            decision = Polygon(
                UP * 1.4, RIGHT * 2.2, DOWN * 1.4, LEFT * 2.2
            )
            decision.set_fill(C_SURFACE, 1).set_stroke(C_ACCENT, 2.5, 0.8)
            decision.move_to(RIGHT * 0.5)

            decision_text = Text("¿Condición\nVerdadera?", font_size=30,
                                 color=C_TEXT, line_spacing=1.3)
            decision_text.move_to(decision)

            # Rama VERDADERA (arriba a la derecha)
            true_box = make_box("Ejecutar A", width=3.2, height=1.0,
                                color="#064E3B", stroke_color=C_SUCCESS)
            true_box.move_to(RIGHT * 5.5 + UP * 2.2)

            # Rama FALSA (abajo a la derecha)
            false_box = make_box("Ejecutar B", width=3.2, height=1.0,
                                 color="#450A0A", stroke_color=C_ERROR)
            false_box.move_to(RIGHT * 5.5 + DOWN * 2.2)

            # Flechas de conexión (con espacio adecuado)
            arrow_start = make_arrow(
                start_box.get_right(),
                decision.get_left(),
                color=C_TEXT_DIM
            )

            arrow_true = make_arrow(
                decision.get_corner(UR) + RIGHT * 0.1,
                true_box.get_left(),
                color=C_SUCCESS,
                stroke_width=5
            )

            arrow_false = make_arrow(
                decision.get_corner(DR) + RIGHT * 0.1,
                false_box.get_left(),
                color=C_ERROR,
                stroke_width=5
            )

            # Etiquetas de las flechas
            label_true = Text("SÍ", font_size=26, color=C_SUCCESS, weight=BOLD)
            label_true.next_to(arrow_true, UP, buff=0.15)

            label_false = Text("NO", font_size=26, color=C_ERROR, weight=BOLD)
            label_false.next_to(arrow_false, DOWN, buff=0.15)

            # Tarjeta explicativa (parte superior, sin invadir diagrama)
            explanation = Text(
                "Una condición divide el flujo en caminos exclusivos.\n"
                "Solo UN camino se ejecuta en cada evaluación.",
                font_size=26, color=C_TEXT, line_spacing=1.4
            )
            explanation_card = make_card(explanation, C_SURFACE)
            explanation_card.to_edge(UP).shift(DOWN * 2.3)

            # Construir grupo completo
            diagram = VGroup(
                start_box, token, decision, decision_text,
                true_box, false_box,
                arrow_start, arrow_true, arrow_false,
                label_true, label_false
            )

            # Animación de entrada (escalonada para claridad)
            self.play(FadeIn(start_box), FadeIn(token), run_time=0.8)
            self.play(Create(arrow_start), run_time=0.6)
            self.play(FadeIn(decision), FadeIn(decision_text), run_time=0.8)
            self.play(FadeIn(explanation_card, shift=UP * 0.2), run_time=0.8)
            self.wait(1.0)

            # Animación del flujo - Camino VERDADERO
            self.play(token.animate.move_to(decision.get_center()), run_time=1.0)
            self.wait(0.5)

            self.play(
                Create(arrow_true),
                FadeIn(true_box),
                FadeIn(label_true),
                run_time=1.0
            )
            self.play(token.animate.move_to(true_box.get_center()), run_time=1.2)
            self.wait(1.5)

            # Regresar y mostrar camino FALSO
            self.play(
                token.animate.move_to(decision.get_center()),
                true_box.animate.set_opacity(0.25),
                run_time=0.8
            )

            self.play(
                Create(arrow_false),
                FadeIn(false_box),
                FadeIn(label_false),
                run_time=1.0
            )
            self.play(token.animate.move_to(false_box.get_center()), run_time=1.2)
            self.wait(2.0)

            # Limpieza
            self.play(
                FadeOut(VGroup(title, subtitle, diagram, explanation_card), shift=UP * 0.5),
                run_time=1.0
            )

        section_conditionals()

        # ========================================
        # SECCIÓN 2: CONTROL DE FLUJO
        # ========================================

        def section_flow_control():
            title = make_title("2. Control de Flujo")
            subtitle = make_subtitle("El orden de ejecución determina el resultado")

            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3), run_time=1.2)
            self.wait(0.5)

            # Layout: Secuencia vertical a la izquierda, salida lateral a la derecha
            # Espacio generoso entre cada paso

            steps = VGroup()
            step_labels = ["1. Entrada", "2. Procesamiento", "3. Validación"]

            for i, label in enumerate(step_labels):
                step = make_box(label, width=4.0, height=0.95,
                                color=C_SURFACE_2, stroke_color=C_TEXT_DIM)
                step.move_to(LEFT * 5.0 + DOWN * (i * 2.0))
                steps.add(step)

            # Salida temprana (lado derecho, alineada con paso 2)
            exit_box = make_box("⚠ Salida Temprana", width=4.5, height=0.95,
                                color="#7F1D1D", stroke_color=C_ERROR)
            exit_box.move_to(RIGHT * 4.5 + DOWN * 2.0)

            # Flechas de secuencia
            arrow_1 = make_arrow(steps[0].get_bottom(), steps[1].get_top(),
                                 color=C_TEXT_DIM, stroke_width=4)
            arrow_2 = make_arrow(steps[1].get_bottom(), steps[2].get_top(),
                                 color=C_TEXT_DIM, stroke_width=4)

            # Flecha de salida (desde paso 2 hacia la derecha)
            arrow_exit = make_arrow(steps[1].get_right(), exit_box.get_left(),
                                    color=C_ERROR, stroke_width=5)

            # Token
            token = make_token(C_WARNING)
            token.move_to(steps[0].get_center())

            # Tarjeta explicativa
            explanation = Text(
                "El flujo sigue un orden definido, pero puede\n"
                "interruptirse ante condiciones excepcionales.",
                font_size=26, color=C_TEXT, line_spacing=1.4
            )
            explanation_card = make_card(explanation, C_SURFACE)
            explanation_card.to_edge(UP).shift(DOWN * 2.3)

            diagram = VGroup(steps, exit_box, arrow_1, arrow_2, arrow_exit, token)

            # Animación de entrada
            self.play(FadeIn(steps, shift=RIGHT * 0.2), run_time=1.0)
            self.play(Create(arrow_1), Create(arrow_2), run_time=0.8)
            self.play(Create(arrow_exit), FadeIn(exit_box), run_time=0.8)
            self.play(FadeIn(token), run_time=0.5)
            self.play(FadeIn(explanation_card, shift=UP * 0.2), run_time=0.8)
            self.wait(1.0)

            # Animación del flujo normal hasta paso 2
            self.play(token.animate.move_to(steps[0].get_center()), run_time=0.6)
            self.wait(0.5)
            self.play(token.animate.move_to(steps[1].get_center()), run_time=1.0)
            self.wait(0.8)

            # Desvío hacia salida temprana
            self.play(token.animate.move_to(exit_box.get_center()), run_time=1.2)
            self.wait(2.0)

            # Limpieza
            self.play(
                FadeOut(VGroup(title, subtitle, diagram, explanation_card), shift=UP * 0.5),
                run_time=1.0
            )

        section_flow_control()

        # ========================================
        # SECCIÓN 3: CICLOS / ITERACIÓN
        # ========================================

        def section_loops():
            title = make_title("3. Iteración (Ciclos)")
            subtitle = make_subtitle("Repetición controlada de tareas")

            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3), run_time=1.2)
            self.wait(0.5)

            # Layout: Contador a la izquierda, bucle al centro-derecha, salida a la extrema derecha
            # Esto evita superposiciones y da espacio a la animación

            # Contador (izquierda, espacio dedicado)
            counter_label = Text("Iteración:", font_size=32, color=C_TEXT_DIM)
            counter_value = Integer(0, font_size=72, color=C_WARNING)
            counter_value.scale(1.05)
            counter_value.next_to(counter_label, DOWN, buff=0.3)
            counter_group = VGroup(counter_label, counter_value)
            counter_group.move_to(LEFT * 6.0)

            # Caja del bucle (centro-derecha)
            loop_box = RoundedRectangle(corner_radius=0.15, width=5.5, height=3.2)
            loop_box.set_fill(C_SURFACE, 1).set_stroke(C_ACCENT, 2, 0.5)
            loop_box.move_to(RIGHT * 1.5)

            loop_content = Text("Ejecutar Tarea", font_size=34, color=C_TEXT)
            loop_content.move_to(loop_box)

            # Flecha curva de retorno (izquierda del bucle)
            loop_arrow = CurvedArrow(
                loop_box.get_bottom() + LEFT * 2.2,
                loop_box.get_top() + LEFT * 2.2,
                angle=TAU * 0.58,
            ).set_stroke(C_WARNING, 5, 0.9)

            # Flecha de salida (derecha del bucle)
            exit_arrow = make_arrow(
                loop_box.get_right(),
                loop_box.get_right() + RIGHT * 3.0,
                color=C_SUCCESS,
                stroke_width=6
            )

            exit_label = Text("Condición de Salida", font_size=28, color=C_SUCCESS, weight=BOLD)
            exit_label.next_to(exit_arrow, UP, buff=0.2)

            # Token dentro del bucle
            token = make_token(C_WARNING)
            token.move_to(loop_box.get_left() + RIGHT * 0.8)

            # Tarjeta explicativa
            explanation = Text(
                "El ciclo repite mientras la condición sea verdadera.\n"
                "La condición de salida previene bucles infinitos.",
                font_size=26, color=C_TEXT, line_spacing=1.4
            )
            explanation_card = make_card(explanation, C_SURFACE)
            explanation_card.to_edge(UP).shift(DOWN * 2.3)

            diagram = VGroup(
                counter_group, loop_box, loop_content, loop_arrow,
                exit_arrow, exit_label, token
            )

            # Animación de entrada
            self.play(FadeIn(counter_group), run_time=0.8)
            self.play(FadeIn(loop_box), FadeIn(loop_content), run_time=0.8)
            self.play(Create(loop_arrow), run_time=0.8)
            self.play(Create(exit_arrow), FadeIn(exit_label), run_time=0.8)
            self.play(FadeIn(token), run_time=0.5)
            self.play(FadeIn(explanation_card, shift=UP * 0.2), run_time=0.8)
            self.wait(1.0)

            # Animación de iteraciones (más lento para claridad)
            max_iterations = 5
            for i in range(1, max_iterations + 1):
                # Token entra al centro (ejecución)
                self.play(token.animate.move_to(loop_box.get_center()), run_time=0.5)
                # Actualizar contador
                self.play(counter_value.animate.set_value(i), run_time=0.4)
                # Token regresa al inicio del bucle
                self.play(token.animate.move_to(loop_box.get_left() + RIGHT * 0.8), run_time=0.5)
                self.wait(0.3)

            # Salida del bucle
            self.play(token.animate.move_to(exit_arrow.get_end()), run_time=1.2)
            self.wait(2.0)

            # Limpieza
            self.play(
                FadeOut(VGroup(title, subtitle, diagram, explanation_card), shift=UP * 0.5),
                run_time=1.0
            )

        section_loops()

        # ========================================
        # SECCIÓN 4: CLASES Y OBJETOS
        # ========================================

        def section_classes():
            title = make_title("4. Clases y Objetos")
            subtitle = make_subtitle("Moldes e instancias en programación")

            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3), run_time=1.2)
            self.wait(0.5)

            # Layout: Clase a la izquierda, objetos a la derecha (verticalmente distribuidos)
            # Espacio amplio entre clase y cada objeto

            # Plano/Clase (izquierda)
            class_box = RoundedRectangle(corner_radius=0.15, width=5.0, height=3.5)
            class_box.set_fill("#1E3A8A", 1).set_stroke(C_PURPLE, 2.5, 0.8)
            class_box.move_to(LEFT * 4.5)

            class_title = Text("CLASE", font_size=36, weight=BOLD, color=C_PURPLE)
            class_title.next_to(class_box.get_top(), DOWN, buff=0.25)

            class_attrs = Text("• Atributos (datos)", font_size=28, color=C_TEXT)
            class_attrs.move_to(class_box.get_center() + UP * 0.5)

            class_methods = Text("• Métodos (acciones)", font_size=28, color=C_TEXT)
            class_methods.move_to(class_box.get_center() + DOWN * 0.5)

            class_group = VGroup(class_box, class_title, class_attrs, class_methods)

            # Objetos (derecha, distribuidos verticalmente con espacio)
            def create_object(name: str, position: np.ndarray, color: str) -> VGroup:
                obj_box = RoundedRectangle(corner_radius=0.1, width=3.5, height=0.95)
                obj_box.set_fill(color, 0.85).set_stroke(WHITE, 1, 0.3)
                obj_text = Text(name, font_size=30, color=C_TEXT, weight=BOLD)
                obj_text.move_to(obj_box)
                return VGroup(obj_box, obj_text).move_to(position)

            obj_a = create_object("Objeto A", RIGHT * 5.0 + UP * 2.0, "#065F46")
            obj_b = create_object("Objeto B", RIGHT * 5.0 + UP * 0.0, "#5B21B6")
            obj_c = create_object("Objeto C", RIGHT * 5.0 + DOWN * 2.0, "#9A3412")

            objects_group = VGroup(obj_a, obj_b, obj_c)

            # Flechas de instanciación (desde clase hacia cada objeto)
            arrow_a = make_arrow(class_box.get_right(), obj_a.get_left(),
                                 color=C_TEXT_DIM, stroke_width=3)
            arrow_b = make_arrow(class_box.get_right(), obj_b.get_left(),
                                 color=C_TEXT_DIM, stroke_width=3)
            arrow_c = make_arrow(class_box.get_right(), obj_c.get_left(),
                                 color=C_TEXT_DIM, stroke_width=3)

            arrows_group = VGroup(arrow_a, arrow_b, arrow_c)

            # Tarjeta explicativa
            explanation = Text(
                "La CLASE define la estructura.\n"
                "Cada OBJETO es una instancia independiente con su propio estado.",
                font_size=26, color=C_TEXT, line_spacing=1.4
            )
            explanation_card = make_card(explanation, C_SURFACE)
            explanation_card.to_edge(UP).shift(DOWN * 2.3)

            diagram = VGroup(class_group, objects_group, arrows_group)

            # Animación de entrada
            self.play(FadeIn(class_group, shift=LEFT * 0.2), run_time=1.0)
            self.wait(0.5)
            self.play(Create(arrows_group), run_time=0.8)
            self.play(FadeIn(objects_group, shift=RIGHT * 0.2), run_time=1.0)
            self.play(FadeIn(explanation_card, shift=UP * 0.2), run_time=0.8)
            self.wait(1.5)

            # Demostrar independencia de objetos (cada uno puede cambiar sin afectar a los demás)
            self.play(obj_a.animate.scale(1.15), run_time=0.6)
            self.wait(0.4)
            self.play(obj_a.animate.scale(1 / 1.15), obj_b.animate.scale(1.15), run_time=0.6)
            self.wait(0.4)
            self.play(obj_b.animate.scale(1 / 1.15), obj_c.animate.scale(1.15), run_time=0.6)
            self.wait(1.5)

            # Limpieza
            self.play(
                FadeOut(VGroup(title, subtitle, diagram, explanation_card), shift=UP * 0.5),
                run_time=1.0
            )

        section_classes()

        # ========================================
        # SECCIÓN 5: RESUMEN INTEGRADOR
        # ========================================

        def section_summary():
            title = make_title("Resumen de Conceptos")
            subtitle = make_subtitle("Cuatro pilares de la lógica de programación")

            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3), run_time=1.2)
            self.wait(0.5)

            # Layout: Grid 2x2 con espacio generoso entre cada concepto
            # Cada celda tiene su propia tarjeta

            concepts = VGroup()

            # Concepto 1: Condicionales (arriba-izquierda)
            cond_icon = Diamond(color=C_ACCENT).set_fill(C_ACCENT, 0.3).set_stroke(C_ACCENT, 2)
            cond_text = Text("Condicionales", font_size=30, color=C_TEXT, weight=BOLD)
            cond_desc = Text("Decisiones y bifurcaciones", font_size=24, color=C_TEXT_DIM)
            cond_group = VGroup(cond_icon, cond_text, cond_desc).arrange(DOWN, buff=0.25)
            cond_card = make_card(cond_group, C_SURFACE)
            cond_card.move_to(LEFT * 4.0 + UP * 1.5)

            # Concepto 2: Flujo (arriba-derecha)
            flow_icon = Rectangle(width=1.2, height=0.8, color=C_TEXT_DIM).set_fill(C_TEXT_DIM, 0.3)
            flow_text = Text("Control de Flujo", font_size=30, color=C_TEXT, weight=BOLD)
            flow_desc = Text("Orden y secuencia", font_size=24, color=C_TEXT_DIM)
            flow_group = VGroup(flow_icon, flow_text, flow_desc).arrange(DOWN, buff=0.25)
            flow_card = make_card(flow_group, C_SURFACE)
            flow_card.move_to(RIGHT * 4.0 + UP * 1.5)

            # Concepto 3: Ciclos (abajo-izquierda)
            loop_icon = Circle(radius=0.5, color=C_WARNING).set_fill(C_WARNING, 0.3).set_stroke(C_WARNING, 2)
            loop_text = Text("Iteración", font_size=30, color=C_TEXT, weight=BOLD)
            loop_desc = Text("Repetición controlada", font_size=24, color=C_TEXT_DIM)
            loop_group = VGroup(loop_icon, loop_text, loop_desc).arrange(DOWN, buff=0.25)
            loop_card = make_card(loop_group, C_SURFACE)
            loop_card.move_to(LEFT * 4.0 + DOWN * 1.5)

            # Concepto 4: Objetos (abajo-derecha)
            obj_icon = RoundedRectangle(width=1.0, height=1.0, corner_radius=0.15,
                                        color=C_PURPLE).set_fill(C_PURPLE, 0.3).set_stroke(C_PURPLE, 2)
            obj_text = Text("Clases y Objetos", font_size=30, color=C_TEXT, weight=BOLD)
            obj_desc = Text("Abstracción y modelado", font_size=24, color=C_TEXT_DIM)
            obj_group = VGroup(obj_icon, obj_text, obj_desc).arrange(DOWN, buff=0.25)
            obj_card = make_card(obj_group, C_SURFACE)
            obj_card.move_to(RIGHT * 4.0 + DOWN * 1.5)

            concepts.add(cond_card, flow_card, loop_card, obj_card)

            # Tarjeta final de cierre
            closing = Text(
                "Comprender la lógica es el primer paso\n"
                "para dominar cualquier lenguaje de programación.",
                font_size=32, color=C_TEXT, line_spacing=1.5, weight=BOLD
            )
            closing_card = make_card(closing, C_SURFACE_2)
            closing_card.to_edge(DOWN).shift(UP * MARGIN_Y * 0.7)

            # Animación de entrada (una por una para énfasis)
            self.play(FadeIn(cond_card, shift=UP * 0.3), run_time=0.8)
            self.wait(0.3)
            self.play(FadeIn(flow_card, shift=UP * 0.3), run_time=0.8)
            self.wait(0.3)
            self.play(FadeIn(loop_card, shift=DOWN * 0.3), run_time=0.8)
            self.wait(0.3)
            self.play(FadeIn(obj_card, shift=DOWN * 0.3), run_time=0.8)
            self.wait(1.0)
            self.play(FadeIn(closing_card, shift=UP * 0.3), run_time=1.0)
            self.wait(4.0)

            # Fade out final
            self.play(
                FadeOut(VGroup(title, subtitle, concepts, closing_card), shift=UP * 0.5),
                run_time=1.5
            )

        section_summary()

        # ========================================
        # CIERRE
        # ========================================

        end_text = Text("Fin", font_size=72, color=C_TEXT_DIM)
        self.play(FadeIn(end_text), run_time=1.5)
        self.wait(2.0)
        self.play(FadeOut(end_text), run_time=1.0)