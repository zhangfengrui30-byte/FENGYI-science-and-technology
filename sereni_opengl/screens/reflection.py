from ui.components import Button, Card
from screens.base import Screen, TEXTURES


class ReflectionScreen(Screen):
    def __init__(self, renderer):
        super().__init__(renderer)
        self.buttons = [
            Button("Back Home", 64, 46, 140, 44, "home", False),
            Button("Try Breathing Exercise", 350, 604, 324, 56, "breathing", True),
        ]

    def draw(self):
        r = self.renderer
        r.draw_gradient(0, 0, 1024, 768, (0.95, 0.96, 0.99, 1), (0.96, 0.93, 0.90, 1))
        for button in self.buttons:
            if button.action == "home":
                button.draw(r)
        r.draw_text(246, 78, "AI Reflection Result", 38, (0.18, 0.20, 0.26, 1), bold=True)
        Card(160, 150, 704, 390, 34).draw(r, (1, 1, 1, 0.90))
        r.draw_texture(str(TEXTURES / "journal-desk.png"), 194, 178, 232, 156, 0.92)
        r.draw_text(460, 186, "You seem mentally overloaded", 28, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_text(462, 232, "Your reflection mentions study pressure, group work,", 18, (0.44, 0.48, 0.58, 1))
        r.draw_text(462, 260, "and difficulty slowing down after class.", 18, (0.44, 0.48, 0.58, 1))
        r.draw_rounded_rect(460, 316, 326, 86, 22, (0.92, 0.95, 1.0, 1))
        r.draw_text(484, 338, "Recommended next step", 18, (0.38, 0.48, 0.84, 1), bold=True)
        r.draw_text(484, 368, "Take a one-minute guided breathing pause.", 18, (0.33, 0.37, 0.48, 1))
        r.draw_text(218, 460, "This screen demonstrates system feedback, recognition, and a clear recovery path.", 16, (0.47, 0.50, 0.58, 1))
        for button in self.buttons:
            if button.action != "home":
                button.draw(r)

