import math
import time

from ui.components import Button, Card
from screens.base import Screen, TEXTURES


class BreathingScreen(Screen):
    def __init__(self, renderer):
        super().__init__(renderer)
        self.started_at = None
        self.playing = False
        self.saved = False
        self.buttons = [
            Button("Start Video", 96, 628, 190, 54, "start_video", True),
            Button("Pause", 316, 628, 190, 54, "pause_video", False),
            Button("Replay", 536, 628, 190, 54, "replay_video", False),
            Button("Save", 756, 628, 170, 54, "save_resource", False),
            Button("Back Home", 64, 46, 140, 44, "home", False),
        ]

    def elapsed(self):
        if not self.started_at:
            return 0
        return min(60, int(time.time() - self.started_at))

    def draw(self):
        r = self.renderer
        r.draw_gradient(0, 0, 1024, 768, (0.97, 0.95, 0.91, 1), (0.94, 0.91, 0.86, 1))
        Card(54, 34, 916, 694, 38).draw(r, (0.99, 0.98, 0.95, 0.94))

        for button in self.buttons:
            if button.action == "home":
                button.draw(r)

        r.draw_text(232, 62, "Guided Calm Video", 38, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_text(234, 112, "Breathing Exercise", 22, (0.44, 0.48, 0.58, 1))

        video_x, video_y, video_w, video_h = 102, 160, 820, 338
        r.draw_shadow(video_x, video_y, video_w, video_h, 34, 0.08)
        r.draw_texture(str(TEXTURES / "breathing-window.png"), video_x, video_y, video_w, video_h, 1)
        r.draw_rounded_rect(video_x, video_y, video_w, video_h, 34, (0.10, 0.08, 0.06, 0.22))

        elapsed = self.elapsed()
        phase = elapsed % 12
        word = "Inhale" if phase < 4 else "Hold" if phase < 6 else "Exhale"
        scale = 0.88 + 0.22 * (0.5 + 0.5 * math.sin(time.time() * math.pi / 4)) if self.playing else 0.92
        cx, cy = video_x + video_w / 2, video_y + video_h / 2
        r.draw_circle(cx, cy, 106 * scale, (1, 1, 1, 0.22))
        r.draw_circle(cx, cy, 66 * scale, (0.56, 0.66, 0.95, 0.56))
        r.draw_text(cx - 44, cy - 17, word, 29, (0.17, 0.19, 0.25, 0.9), bold=True)

        r.draw_circle(cx, cy + 10, 42, (0.50, 0.62, 0.95, 1))
        if self.playing:
            r.draw_rect(cx - 12, cy - 8, 8, 30, (1, 1, 1, 1))
            r.draw_rect(cx + 6, cy - 8, 8, 30, (1, 1, 1, 1))
        else:
            r.draw_text(cx - 10, cy - 19, "▶", 36, (1, 1, 1, 1), bold=True)

        r.draw_texture(str(TEXTURES / "momo-companion.png"), video_x + video_w - 112, video_y + video_h - 112, 70, 70)
        progress = elapsed / 60
        r.draw_rounded_rect(video_x + 50, video_y + video_h - 58, video_w - 100, 8, 4, (1, 1, 1, 0.50))
        r.draw_rounded_rect(video_x + 50, video_y + video_h - 58, (video_w - 100) * progress, 8, 4, (0.93, 0.64, 0.74, 1))
        r.draw_text(video_x + 50, video_y + video_h - 42, f"0:{elapsed:02d} / 1:00", 18, (1, 1, 1, 1), bold=True)
        r.draw_text(video_x + video_w - 138, video_y + video_h - 42, "Vol   Full", 18, (1, 1, 1, 1), bold=True)

        r.draw_text(102, 532, "1-Minute Guided Breathing", 22, (0.42, 0.50, 0.90, 1), bold=True)
        r.draw_text(102, 566, "Take a soft pause", 34, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_text(102, 608, "Follow the breathing rhythm and let your body slow down for one minute.", 20, (0.43, 0.47, 0.57, 1))

        for button in self.buttons:
            if button.action != "home":
                button.draw(r)

        if self.saved:
            r.draw_rounded_rect(390, 704, 244, 40, 20, (0.18, 0.20, 0.26, 0.92))
            r.draw_text(418, 714, "Saved to your resources", 16, (1, 1, 1, 1), bold=True)

