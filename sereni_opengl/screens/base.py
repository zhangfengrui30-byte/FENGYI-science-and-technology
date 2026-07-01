from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXTURES = ROOT / "assets" / "textures"
SOUNDS = ROOT / "assets" / "sounds"


class Screen:
    def __init__(self, renderer):
        self.renderer = renderer
        self.buttons = []

    def update_hover(self, x, y):
        for button in self.buttons:
            button.set_hover(x, y)

    def handle_click(self, x, y):
        for button in self.buttons:
            if button.contains(x, y):
                return button.action
        return None

