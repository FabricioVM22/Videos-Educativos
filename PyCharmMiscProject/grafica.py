from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


class VideoProgramacionVisual(Scene):
    def construct(self):
        # Estilo base (fondo + margen “académico”)
        bg = Rectangle(width=16, height=9).set_fill(color=BLACK, opacity=1).set_stroke(width=0)
        self.add(bg)

        top_rule = Line(LEFT * 7.2, RIGHT * 7.2).set_stroke(WHITE, 1, opacity=0.25).to_edge(UP).shift(DOWN * 0.95)
        bottom_rule = Line(LEFT * 7.2, RIGHT * 7.2).set_stroke(WHITE, 1, opacity=0.25).to_edge(DOWN).shift(UP * 0.95)
        self.add(top_rule, bottom_rule)

        # Ritmo base (apunta a ~3 min total ajustando estos valores)
        PACE = 1.15  # >1 más lento, <1 más rápido

        def section_title(txt: str) -> Mobject:
            t = Text(txt, font_size=54, weight=BOLD)
            t.scale_to_fit_width(13.6)
            return t.to_edge(UP).shift(DOWN * 0.25)

        def caption(txt: str) -> Mobject:
            c = Text(txt, font_size=34)
            c.scale_to_fit_width(13.6)
            return c.to_edge(DOWN).shift(UP * 0.25)

        def clear_mobjects(*mobs: Mobject, run_time: float = 0.8):
            """FadeOut consistente y evita que se queden objetos 'vivos' encima."""
            mobs = [m for m in mobs if m is not None]
            if mobs:
                self.play(FadeOut(VGroup(*mobs)), run_time=run_time * PACE)

        # ----------------------------
        # 1) Intro
        # ----------------------------
        t1 = section_title("Lógica de programación (sin código)")
        s1 = caption("Condicionales · Control · Ciclos · Clases")
        self.play(Write(t1), FadeIn(s1, shift=UP), run_time=1.4 * PACE)
        self.wait(3.0 * PACE)
        self.play(FadeOut(s1), run_time=0.8 * PACE)

        # Un “flujo” base: Inicio -> (secciones)
        start = RoundedRectangle(corner_radius=0.25, width=3.2, height=1.0).set_fill("#1f2937", 1).set_stroke(WHITE, 2)
        start_text = Text("INICIO", font_size=36, weight=BOLD).move_to(start)
        start_group = VGroup(start, start_text).move_to(LEFT * 4 + DOWN * 1)

        token = Circle(radius=0.22).set_fill(YELLOW, 1).set_stroke(BLACK, 0).move_to(start_group.get_center() + RIGHT * 1.6)
        self.play(FadeIn(start_group), FadeIn(token), run_time=0.9 * PACE)
        self.wait(1.0 * PACE)

        # ----------------------------
        # 2) Condicionales (IF / ELSE visual)
        # ----------------------------
        t2 = section_title("1) Condicionales: elegir un camino")
        self.play(Transform(t1, t2), run_time=0.9 * PACE)

        decision = Polygon(UP * 1.0, RIGHT * 1.8, DOWN * 1.0, LEFT * 1.8).set_fill("#0b1220", 1).set_stroke(WHITE, 2)
        decision.move_to(RIGHT * 1.5 + DOWN * 0.6)
        d_text = Text("¿Condición?", font_size=32).move_to(decision)

        true_box = RoundedRectangle(corner_radius=0.2, width=3.6, height=1.1).set_fill("#052e1a", 1).set_stroke(GREEN, 2)
        true_label = Text("VERDADERO", font_size=30, weight=BOLD, color=GREEN).move_to(true_box)
        true_group = VGroup(true_box, true_label).move_to(RIGHT * 5.3 + UP * 1.6)

        false_box = RoundedRectangle(corner_radius=0.2, width=3.6, height=1.1).set_fill("#2a0a0a", 1).set_stroke(RED, 2)
        false_label = Text("FALSO", font_size=30, weight=BOLD, color=RED).move_to(false_box)
        false_group = VGroup(false_box, false_label).move_to(RIGHT * 5.3 + DOWN * 2.2)

        arrow_in = Arrow(start_group.get_right(), decision.get_left(), buff=0.2).set_stroke(WHITE, 2)
        arrow_true = Arrow(decision.get_right(), true_group.get_left(), buff=0.2).set_stroke(GREEN, 3)
        arrow_false = Arrow(decision.get_right(), false_group.get_left(), buff=0.2).set_stroke(RED, 3)

        tag_true = Text("Sí", font_size=28, color=GREEN).next_to(arrow_true, UP, buff=0.1)
        tag_false = Text("No", font_size=28, color=RED).next_to(arrow_false, DOWN, buff=0.1)

        c_if = caption("Una condición evalúa una idea: si se cumple, tomas una rama; si no, otra.")
        self.play(FadeIn(c_if), run_time=0.7 * PACE)

        self.play(Create(arrow_in), FadeIn(decision), FadeIn(d_text), run_time=1.1 * PACE)
        self.play(Create(arrow_true), FadeIn(true_group), FadeIn(tag_true), run_time=1.0 * PACE)
        self.play(Create(arrow_false), FadeIn(false_group), FadeIn(tag_false), run_time=1.0 * PACE)
        self.wait(1.2 * PACE)

        # Token elige camino (primero “verdadero”, luego “falso”)
        self.play(token.animate.move_to(decision.get_center()), run_time=0.8 * PACE)
        self.play(token.animate.move_to(true_group.get_center()), run_time=1.1 * PACE)
        self.wait(0.8 * PACE)
        self.play(token.animate.move_to(decision.get_center()), run_time=0.9 * PACE)
        self.play(token.animate.move_to(false_group.get_center()), run_time=1.1 * PACE)
        self.wait(1.2 * PACE)

        # Limpieza COMPLETA de la sección (evita overlays)
        clear_mobjects(
            c_if,
            true_group, false_group, tag_true, tag_false,
            arrow_true, arrow_false,
            decision, d_text,
        )
        # Mantén start_group, arrow_in y token como “hilo conductor”

        # ----------------------------
        # 3) Estructuras de control (secuencia, decisión, fin temprano)
        # ----------------------------
        t3 = section_title("2) Control del flujo: secuencia y salida")
        self.play(Transform(t1, t3), run_time=0.9 * PACE)

        step1 = RoundedRectangle(corner_radius=0.2, width=4.0, height=1.0).set_fill("#111827", 1).set_stroke(WHITE, 2)
        step1_t = Text("Paso 1", font_size=34).move_to(step1)
        step1_g = VGroup(step1, step1_t).move_to(LEFT * 1.5 + UP * 1.6)

        step2 = RoundedRectangle(corner_radius=0.2, width=4.0, height=1.0).set_fill("#111827", 1).set_stroke(WHITE, 2)
        step2_t = Text("Paso 2", font_size=34).move_to(step2)
        step2_g = VGroup(step2, step2_t).move_to(LEFT * 1.5 + DOWN * 0.1)

        stop = RoundedRectangle(corner_radius=0.5, width=4.0, height=1.0).set_fill("#0b1220", 1).set_stroke(YELLOW, 2)
        stop_t = Text("FIN TEMPRANO", font_size=30, weight=BOLD, color=YELLOW).move_to(stop)
        stop_g = VGroup(stop, stop_t).move_to(LEFT * 1.5 + DOWN * 2.0)

        a12 = Arrow(step1_g.get_bottom(), step2_g.get_top(), buff=0.15).set_stroke(WHITE, 2)
        a2stop = Arrow(step2_g.get_bottom(), stop_g.get_top(), buff=0.15).set_stroke(WHITE, 2)

        c_flow = caption("El orden importa: la lógica recorre pasos. A veces una regla permite terminar antes.")
        self.play(FadeIn(c_flow), run_time=0.7 * PACE)

        self.play(FadeIn(step1_g), FadeIn(step2_g), FadeIn(stop_g), Create(a12), Create(a2stop), run_time=1.3 * PACE)

        self.play(token.animate.move_to(step1_g.get_center()), run_time=0.9 * PACE)
        self.wait(0.6 * PACE)
        self.play(token.animate.move_to(step2_g.get_center()), run_time=0.9 * PACE)
        self.wait(0.6 * PACE)
        self.play(token.animate.move_to(stop_g.get_center()), run_time=1.0 * PACE)
        self.wait(1.5 * PACE)

        clear_mobjects(c_flow, step1_g, step2_g, stop_g, a12, a2stop)

        # ----------------------------
        # 4) Ciclos (LOOP)
        # ----------------------------
        t4 = section_title("3) Ciclos: repetir con condición de salida")
        self.play(Transform(t1, t4), run_time=0.9 * PACE)

        loop_box = RoundedRectangle(corner_radius=0.25, width=6.2, height=3.0).set_fill("#0b1220", 1).set_stroke(WHITE, 2)
        loop_box.move_to(RIGHT * 1.8 + DOWN * 0.3)
        loop_title = Text("Bucle", font_size=40, weight=BOLD).next_to(loop_box.get_top(), DOWN, buff=0.2)
        loop_body = Text("Ejecutar tarea", font_size=34).move_to(loop_box.get_center() + UP * 0.2)

        counter_label = Text("Iteraciones:", font_size=30).move_to(LEFT * 5.2 + UP * 0.8)
        counter_value = Integer(0, font_size=54, color=YELLOW).next_to(counter_label, DOWN, buff=0.2).align_to(counter_label, LEFT)

        loop_arrow = CurvedArrow(loop_box.get_bottom() + LEFT * 2.2, loop_box.get_top() + LEFT * 2.2, angle=TAU * 0.62).set_stroke(YELLOW, 4)
        exit_arrow = Arrow(loop_box.get_right(), loop_box.get_right() + RIGHT * 2.5, buff=0.2).set_stroke(GREEN, 4)
        exit_label = Text("Salir", font_size=30, color=GREEN).next_to(exit_arrow, UP, buff=0.1)

        c_loop = caption("Un ciclo repite. La variable de control cambia, y una condición decide cuándo salir.")
        self.play(FadeIn(c_loop), run_time=0.7 * PACE)

        self.play(
            FadeIn(loop_box), FadeIn(loop_title), FadeIn(loop_body),
            Create(loop_arrow),
            FadeIn(counter_label), FadeIn(counter_value),
            run_time=1.4 * PACE
        )
        self.play(Create(exit_arrow), FadeIn(exit_label), run_time=0.9 * PACE)

        token.move_to(loop_box.get_left() + RIGHT * 1.0)
        self.play(token.animate.set_opacity(1.0), run_time=0.1)

        # Simular iteraciones (más pausadas para didáctica)
        for i in range(1, 7):
            self.play(token.animate.move_to(loop_box.get_center()), run_time=0.45 * PACE)
            self.play(counter_value.animate.set_value(i), run_time=0.45 * PACE)
            self.play(token.animate.move_to(loop_box.get_left() + RIGHT * 1.0), run_time=0.45 * PACE)
            self.wait(0.15 * PACE)

        self.play(token.animate.move_to(exit_arrow.get_end()), run_time=1.1 * PACE)
        self.wait(1.2 * PACE)

        clear_mobjects(
            c_loop,
            loop_box, loop_title, loop_body,
            loop_arrow, exit_arrow, exit_label,
            counter_label, counter_value,
        )

        # ----------------------------
        # 5) Clases y objetos (blueprint -> instancias)
        # ----------------------------
        t5 = section_title("4) Clases y objetos: molde e instancias")
        self.play(Transform(t1, t5), run_time=0.9 * PACE)

        blueprint = RoundedRectangle(corner_radius=0.2, width=6.4, height=3.6).set_fill("#0b2a4a", 1).set_stroke("#7dd3fc", 3)
        blueprint.move_to(LEFT * 2.4)
        bp_title = Text("CLASE (molde)", font_size=34, weight=BOLD, color="#7dd3fc").next_to(blueprint.get_top(), DOWN, buff=0.25)
        attrs = Text("Estado: datos", font_size=30).move_to(blueprint.get_center() + UP * 0.6)
        methods = Text("Comportamiento: acciones", font_size=30).move_to(blueprint.get_center() + DOWN * 0.5)
        bp_group = VGroup(blueprint, bp_title, attrs, methods)

        o1 = RoundedRectangle(corner_radius=0.25, width=3.8, height=1.2).set_fill("#111827", 1).set_stroke(WHITE, 2).move_to(RIGHT * 4.4 + UP * 1.2)
        o1_t = Text("OBJETO A", font_size=32, weight=BOLD).move_to(o1)
        o2 = RoundedRectangle(corner_radius=0.25, width=3.8, height=1.2).set_fill("#111827", 1).set_stroke(WHITE, 2).move_to(RIGHT * 4.4 + DOWN * 0.6)
        o2_t = Text("OBJETO B", font_size=32, weight=BOLD).move_to(o2)
        o3 = RoundedRectangle(corner_radius=0.25, width=3.8, height=1.2).set_fill("#111827", 1).set_stroke(WHITE, 2).move_to(RIGHT * 4.4 + DOWN * 2.4)
        o3_t = Text("OBJETO C", font_size=32, weight=BOLD).move_to(o3)

        make_arrow1 = Arrow(blueprint.get_right(), o1.get_left(), buff=0.2).set_stroke(YELLOW, 3)
        make_arrow2 = Arrow(blueprint.get_right(), o2.get_left(), buff=0.2).set_stroke(YELLOW, 3)
        make_arrow3 = Arrow(blueprint.get_right(), o3.get_left(), buff=0.2).set_stroke(YELLOW, 3)

        c_class = caption("Una clase describe una estructura. Un objeto es una instancia concreta con su propio estado.")
        self.play(FadeIn(c_class), run_time=0.7 * PACE)

        self.play(FadeIn(bp_group), run_time=1.0 * PACE)
        self.play(
            FadeIn(VGroup(o1, o1_t)), FadeIn(VGroup(o2, o2_t)), FadeIn(VGroup(o3, o3_t)),
            Create(make_arrow1), Create(make_arrow2), Create(make_arrow3),
            run_time=1.4 * PACE
        )
        self.wait(0.8 * PACE)

        # “Estado distinto” de cada objeto (más lento)
        self.play(
            o1.animate.set_fill("#064e3b", 1),
            o2.animate.set_fill("#3b0764", 1),
            o3.animate.set_fill("#7c2d12", 1),
            run_time=1.1 * PACE
        )
        self.wait(1.2 * PACE)
        self.play(
            o1.animate.set_fill("#111827", 1),
            o2.animate.set_fill("#111827", 1),
            o3.animate.set_fill("#111827", 1),
            run_time=0.9 * PACE
        )
        self.wait(1.0 * PACE)

        clear_mobjects(
            c_class,
            bp_group,
            VGroup(o1, o1_t, o2, o2_t, o3, o3_t),
            make_arrow1, make_arrow2, make_arrow3,
        )

        # ----------------------------
        # 6) Cierre (resumen)
        # ----------------------------
        t6 = section_title("Resumen (idea central)")
        self.play(Transform(t1, t6), run_time=0.9 * PACE)

        bullets = VGroup(
            Text("• Condicionales: decidir entre caminos", font_size=34),
            Text("• Control del flujo: secuencia y salidas", font_size=34),
            Text("• Ciclos: repetir con regla de salida", font_size=34),
            Text("• Clases/objetos: molde e instancias", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.2)

        bullets.scale_to_fit_width(13.6)

        closing = caption("Siguiente: aplicar esto a problemas reales y analizar su comportamiento.")
        self.play(Write(bullets), FadeIn(closing), run_time=1.6 * PACE)
        self.wait(6.0 * PACE)

        clear_mobjects(closing, bullets, t1, start_group, arrow_in, token, run_time=1.0)