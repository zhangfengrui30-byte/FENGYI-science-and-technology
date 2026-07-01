import time

from ui.components import Button, Card
from screens.base import Screen, TEXTURES


class HomeScreen(Screen):
    def __init__(self, renderer):
        super().__init__(renderer)
        self.buttons = [
            Button("Start Reflection", 362, 332, 300, 54, "reflection", True),
            Button("Breathing Guide", 362, 404, 300, 54, "breathing", False),
            Button("Campus Resources", 362, 476, 300, 54, "resources", False),
        ]

    def draw(self):
        r = self.renderer
        r.draw_gradient(0, 0, 1024, 768, (0.93, 0.95, 0.99, 1), (0.98, 0.94, 0.90, 1))
        r.draw_circle(870, 118, 72, (0.75, 0.86, 0.95, 0.28))
        r.draw_circle(150, 650, 82, (0.78, 0.72, 0.92, 0.18))

        card = Card(252, 96, 520, 560, 34)
        card.draw(r, (1, 1, 1, 0.82))
        r.draw_texture(str(TEXTURES / "journal-desk.png"), 292, 122, 440, 148, 0.88)
        r.draw_rounded_rect(292, 122, 440, 148, 24, (0.20, 0.17, 0.13, 0.18))

        pulse = 0.82 + 0.18 * abs((time.time() % 4) - 2)
        r.draw_circle(512, 246, 58 * pulse, (0.55, 0.65, 0.94, 0.25))
        r.draw_circle(512, 246, 33 * pulse, (0.74, 0.88, 0.84, 0.42))

        r.draw_text(430, 174, "Sereni", 48, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_text(366, 234, "Guided Calm for Students", 22, (0.43, 0.47, 0.57, 1))
        r.draw_text(338, 292, "Choose a gentle support path for study stress.", 17, (0.50, 0.54, 0.63, 1))

        for button in self.buttons:
            button.draw(r)

        r.draw_text(362, 606, "OpenGL visual prototype with calming audio", 15, (0.48, 0.51, 0.58, 1))

