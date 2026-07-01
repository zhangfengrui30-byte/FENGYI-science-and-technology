import math
import time

from ui.components import Button
from screens.base import Screen, TEXTURES


class BreathingScreen(Screen):
    """iPhone-style Guided Calm Video page rendered with OpenGL."""

    def __init__(self, renderer):
        super().__init__(renderer)
        self.started_at = None
        self.paused_elapsed = 0
        self.playing = False
        self.saved = False
        self.recording = False
        self.buttons = [
            Button("Start Video", 66, 720, 184, 54, "start_video", True),
            Button("Pause", 270, 720, 184, 54, "pause_video", False),
            Button("Replay", 66, 786, 184, 54, "replay_video", False),
            Button("Save", 270, 786, 184, 54, "save_resource", False),
        ]

    def elapsed(self):
        if not self.playing:
            return min(60, int(self.paused_elapsed))
        return min(60, int(self.paused_elapsed + time.time() - self.started_at))

    def draw_status_bar(self, r):
        r.draw_text(76, 38, "9:41", 18, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_rounded_rect(386, 42, 24, 10, 3, (0.32, 0.34, 0.39, 1))
        r.draw_rounded_rect(417, 42, 22, 10, 5, (0.32, 0.34, 0.39, 1))
        r.draw_rounded_rect(449, 38, 31, 16, 5, (0.32, 0.34, 0.39, 1))
        r.draw_rounded_rect(453, 42, 20, 8, 3, (0.96, 0.94, 0.90, 1))
        r.draw_rounded_rect(482, 43, 3, 7, 2, (0.32, 0.34, 0.39, 1))

    def draw_back_button(self, r):
        r.draw_shadow(54, 112, 56, 56, 28, 0.055)
        r.draw_circle(82, 140, 28, (1, 1, 1, 0.96))
        r.draw_text(72, 119, "‹", 40, (0.18, 0.20, 0.26, 1), bold=True)

    def draw_video(self, r):
        video_x, video_y, video_w, video_h = 54, 206, 412, 306
        r.draw_shadow(video_x, video_y, video_w, video_h, 30, 0.08)
        r.draw_texture(str(TEXTURES / "breathing-window.png"), video_x, video_y, video_w, video_h, 1)
        r.draw_rounded_rect(video_x, video_y, video_w, video_h, 30, (0.12, 0.09, 0.06, 0.20))
        r.draw_rounded_rect(video_x + 18, video_y + 18, 160, 30, 15, (1, 1, 1, 0.28))
        r.draw_text(video_x + 34, video_y + 24, "Guided calm", 13, (1, 1, 1, 0.96), bold=True)

        elapsed = self.elapsed()
        phase = elapsed % 12
        word = "Inhale" if phase < 4 else "Hold" if phase < 6 else "Exhale"
        breathe = 0.84 + 0.22 * (0.5 + 0.5 * math.sin(time.time() * math.pi / 4)) if self.playing else 0.90
        cx, cy = video_x + video_w / 2, video_y + 154

        r.draw_circle(cx, cy, 92 * breathe, (1, 1, 1, 0.24))
        r.draw_circle(cx, cy, 61 * breathe, (0.55, 0.65, 0.94, 0.44))
        r.draw_text(cx - 38, cy - 16, word, 27, (0.18, 0.20, 0.26, 0.92), bold=True)

        r.draw_circle(cx, cy + 10, 72, (1, 1, 1, 0.17))
        r.draw_circle(cx, cy + 10, 43, (0.52, 0.63, 0.94, 1))
        if self.playing:
            r.draw_rect(cx - 12, cy - 6, 8, 28, (1, 1, 1, 1))
            r.draw_rect(cx + 6, cy - 6, 8, 28, (1, 1, 1, 1))
        else:
            r.draw_text(cx - 10, cy - 18, "▶", 34, (1, 1, 1, 1), bold=True)

        r.draw_texture(str(TEXTURES / "momo-companion.png"), video_x + video_w - 86, video_y + video_h - 116, 62, 62)
        r.draw_rounded_rect(video_x + video_w - 88, video_y + video_h - 118, 66, 66, 18, (1, 1, 1, 0.30))

        progress = elapsed / 60
        r.draw_rounded_rect(video_x + 30, video_y + video_h - 60, video_w - 60, 6, 3, (1, 1, 1, 0.52))
        r.draw_rounded_rect(video_x + 30, video_y + video_h - 60, (video_w - 60) * progress, 6, 3, (0.93, 0.65, 0.75, 1))
        r.draw_text(video_x + 30, video_y + video_h - 42, f"0:{elapsed:02d} / 1:00", 17, (1, 1, 1, 1), bold=True)
        r.draw_text(video_x + video_w - 98, video_y + video_h - 42, "Vol  Full", 15, (1, 1, 1, 1), bold=True)

    def draw_feature_card(self, r):
        r.draw_shadow(74, 662, 372, 48, 22, 0.045)
        r.draw_texture(str(TEXTURES / "journal-desk.png"), 74, 662, 372, 48, 0.92)
        r.draw_rounded_rect(74, 662, 372, 48, 22, (0.11, 0.08, 0.05, 0.36))
        r.draw_text(96, 668, "A quiet one-minute guide", 18, (1, 1, 1, 1), bold=True)
        r.draw_text(96, 690, "Designed for the pause before studying again.", 12, (1, 1, 1, 0.90))

    def draw_voice_panel(self, r):
        r.draw_shadow(54, 854, 412, 70, 24, 0.050)
        r.draw_rounded_rect(54, 854, 412, 70, 24, (1, 1, 1, 0.92))
        r.draw_text(78, 866, "Voice check-in", 18, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_text(78, 891, "Record a short feeling note.", 13, (0.44, 0.48, 0.58, 1))
        for i, h in enumerate([8, 16, 24, 14, 28, 18]):
            x = 254 + i * 12
            y = 890 - h / 2
            r.draw_rounded_rect(x, y, 6, h, 3, (0.76, 0.82, 0.98, 0.9))
        pulse = 1.0 + (0.08 * math.sin(time.time() * 8) if self.recording else 0)
        r.draw_circle(420, 890, 28 * pulse, (0.91, 0.55, 0.66, 1))
        r.draw_rounded_rect(411, 870, 18, 26, 9, (1, 1, 1, 1))
        r.draw_rounded_rect(404, 891, 32, 16, 8, (1, 1, 1, 0.96))
        r.draw_rounded_rect(415, 905, 12, 4, 2, (1, 1, 1, 1))

    def draw_bottom_nav(self, r):
        r.draw_rounded_rect(24, 924, 472, 20, 0, (1, 1, 1, 0.70))
        r.draw_circle(96, 914, 6, (0.80, 0.77, 0.72, 1))
        r.draw_circle(192, 914, 6, (0.80, 0.77, 0.72, 1))
        r.draw_circle(288, 914, 6, (0.80, 0.77, 0.72, 1))
        r.draw_rounded_rect(364, 900, 58, 28, 14, (0.88, 0.86, 1.0, 1))
        r.draw_circle(393, 914, 7, (0.51, 0.62, 0.94, 1))

    def draw(self):
        r = self.renderer

        r.draw_gradient(0, 0, 520, 960, (0.91, 0.88, 0.82, 1), (0.98, 0.96, 0.92, 1))
        r.draw_shadow(24, 16, 472, 928, 48, 0.09)
        r.draw_rounded_rect(24, 16, 472, 928, 48, (0.98, 0.96, 0.92, 1))
        r.draw_rounded_rect(28, 20, 464, 920, 44, (0.985, 0.965, 0.925, 0.72))

        self.draw_status_bar(r)
        self.draw_back_button(r)

        r.draw_text(124, 116, "Guided Calm Video", 30, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_text(124, 160, "Breathing Exercise", 20, (0.44, 0.48, 0.58, 1))

        self.draw_video(r)

        r.draw_text(54, 534, "1-Minute Guided Breathing", 19, (0.43, 0.51, 0.90, 1), bold=True)
        r.draw_text(54, 562, "Take a soft pause", 31, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_text(54, 603, "Follow the breathing rhythm and let your body", 18, (0.44, 0.48, 0.58, 1))
        r.draw_text(54, 628, "slow down for one minute.", 18, (0.44, 0.48, 0.58, 1))

        self.draw_feature_card(r)

        for button in self.buttons:
            button.draw(r)

        if self.saved:
            r.draw_rounded_rect(146, 718, 228, 38, 19, (0.18, 0.20, 0.26, 0.92))
            r.draw_text(176, 727, "Saved to your resources", 15, (1, 1, 1, 1), bold=True)

        self.draw_voice_panel(r)
        self.draw_bottom_nav(r)

        r.draw_rounded_rect(178, 934, 164, 5, 3, (0.20, 0.20, 0.20, 0.18))
