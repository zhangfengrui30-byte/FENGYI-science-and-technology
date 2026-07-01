from ui.components import Button, Card
from screens.base import Screen, TEXTURES


class ResourcesScreen(Screen):
    def __init__(self, renderer):
        super().__init__(renderer)
        self.buttons = [
            Button("Back Home", 64, 46, 140, 44, "home", False),
            Button("Open Breathing Guide", 362, 628, 300, 54, "breathing", True),
        ]

    def draw(self):
        r = self.renderer
        r.draw_gradient(0, 0, 1024, 768, (0.97, 0.95, 0.91, 1), (0.92, 0.96, 0.94, 1))
        for button in self.buttons:
            if button.action == "home":
                button.draw(r)
        r.draw_text(278, 78, "Campus Wellbeing Resources", 36, (0.18, 0.20, 0.26, 1), bold=True)

        cards = [
            ("Counselling Centre", "Book a confidential support session.", "breathing-window.png"),
            ("Quiet Study Pause", "Use a soft reset before returning to work.", "journal-desk.png"),
            ("Saved Breathing Guide", "Replay your guided calm video anytime.", "momo-companion.png"),
        ]
        y = 166
        for title, body, img in cards:
            Card(172, y, 680, 120, 26).draw(r, (1, 1, 1, 0.92))
            r.draw_texture(str(TEXTURES / img), 198, y + 20, 92, 80, 0.95)
            r.draw_text(322, y + 26, title, 24, (0.18, 0.20, 0.26, 1), bold=True)
            r.draw_text(322, y + 66, body, 18, (0.44, 0.48, 0.58, 1))
            y += 144

        for button in self.buttons:
            if button.action != "home":
                button.draw(r)

