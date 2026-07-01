class Button:
    def __init__(self, label, x, y, width, height, action, primary=False):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.primary = primary
        self.hovered = False

    def contains(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def set_hover(self, x, y):
        self.hovered = self.contains(x, y)

    def draw(self, renderer):
        if self.primary:
            color = (0.50, 0.62, 0.95, 1.0) if not self.hovered else (0.57, 0.69, 1.0, 1.0)
            text = (1, 1, 1, 1)
        else:
            color = (1, 1, 1, 0.95) if not self.hovered else (0.95, 0.97, 1.0, 1.0)
            text = (0.34, 0.40, 0.72, 1)
        radius = self.height / 2
        renderer.draw_shadow(self.x, self.y, self.width, self.height, radius, 0.055)
        renderer.draw_rounded_rect(self.x, self.y, self.width, self.height, radius, color)
        if self.primary:
            renderer.draw_rounded_rect(self.x + 8, self.y + 5, self.width - 16, 14, 7, (1, 1, 1, 0.18))
            renderer.draw_rounded_rect(self.x + 10, self.y + self.height - 7, self.width - 20, 3, 2, (0.35, 0.45, 0.84, 0.28))
        else:
            renderer.draw_rounded_rect(self.x + 10, self.y + self.height - 6, self.width - 20, 3, 2, (0.50, 0.62, 0.95, 0.22))
        text_w, text_h = renderer.measure_text(self.label, 18, bold=True)
        renderer.draw_text(
            self.x + (self.width - text_w) / 2,
            self.y + (self.height - text_h) / 2,
            self.label,
            18,
            text,
            bold=True,
        )


class Card:
    def __init__(self, x, y, width, height, radius=26):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius

    def draw(self, renderer, color=(1, 1, 1, 0.92)):
        renderer.draw_shadow(self.x, self.y, self.width, self.height, self.radius, 0.07)
        renderer.draw_rounded_rect(self.x, self.y, self.width, self.height, self.radius, color)
