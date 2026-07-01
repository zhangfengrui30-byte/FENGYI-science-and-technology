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
            Button("Start Video", 66, 728, 184, 54, "start_video", True),
            Button("Pause", 270, 728, 184, 54, "pause_video", False),
            Button("Replay", 66, 798, 184, 54, "replay_video", False),
            Button("Save", 270, 798, 184, 54, "save_resource", False),
        ]

    def elapsed(self):
        if not self.playing:
            return min(60, int(self.paused_elapsed))
        return min(60, int(self.paused_elapsed + time.time() - self.started_at))

    def draw_status_bar(self, r):
        r.draw_text(76, 38, "9:41", 18, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_rounded_rect(390, 42, 22, 10, 3, (0.32, 0.34, 0.39, 1))
        r.draw_rounded_rect(421, 42, 20, 10, 5, (0.32, 0.34, 0.39, 1))
        r.draw_rounded_rect(452, 38, 30, 16, 5, (0.32, 0.34, 0.39, 1))
        r.draw_rounded_rect(456, 42, 20, 8, 3, (0.96, 0.94, 0.90, 1))

    def draw_back_button(self, r):
        r.draw_shadow(54, 112, 58, 58, 29, 0.055)
        r.draw_circle(83, 141, 29, (1, 1, 1, 0.96))
        r.draw_text(72, 119, "‹", 42, (0.18, 0.20, 0.26, 1), bold=True)

    def draw_video(self, r):
        video_x, video_y, video_w, video_h = 54, 210, 412, 300
        r.draw_shadow(video_x, video_y, video_w, video_h, 30, 0.08)
        r.draw_texture(str(TEXTURES / "breathing-window.png"), video_x, video_y, video_w, video_h, 1)
        r.draw_rounded_rect(video_x, video_y, video_w, video_h, 30, (0.12, 0.09, 0.06, 0.20))

        elapsed = self.elapsed()
        phase = elapsed % 12
        word = "Inhale" if phase < 4 else "Hold" if phase < 6 else "Exhale"
        breathe = 0.84 + 0.22 * (0.5 + 0.5 * math.sin(time.time() * math.pi / 4)) if self.playing else 0.90
        cx, cy = video_x + video_w / 2, video_y + 154

        r.draw_circle(cx, cy, 92 * breathe, (1, 1, 1, 0.24))
        r.draw_circle(cx, cy, 61 * breathe, (0.55, 0.65, 0.94, 0.44))
        r.draw_text(cx - 38, cy - 16, word, 27, (0.18, 0.20, 0.26, 0.92), bold=True)

        r.draw_circle(cx, cy + 10, 43, (0.52, 0.63, 0.94, 1))
        if self.playing:
            r.draw_rect(cx - 12, cy - 6, 8, 28, (1, 1, 1, 1))
            r.draw_rect(cx + 6, cy - 6, 8, 28, (1, 1, 1, 1))
        else:
            r.draw_text(cx - 10, cy - 18, "▶", 34, (1, 1, 1, 1), bold=True)

        r.draw_texture(str(TEXTURES / "momo-companion.png"), video_x + video_w - 86, video_y + video_h - 116, 62, 62)
        r.draw_rounded_rect(video_x + video_w - 88, video_y + video_h - 118, 66, 66, 18, (1, 1, 1, 0.24))

        progress = elapsed / 60
        r.draw_rounded_rect(video_x + 30, video_y + video_h - 60, video_w - 60, 6, 3, (1, 1, 1, 0.52))
        r.draw_rounded_rect(video_x + 30, video_y + video_h - 60, (video_w - 60) * progress, 6, 3, (0.93, 0.65, 0.75, 1))
        r.draw_text(video_x + 30, video_y + video_h - 42, f"0:{elapsed:02d} / 1:00", 17, (1, 1, 1, 1), bold=True)
        r.draw_text(video_x + video_w - 98, video_y + video_h - 42, "Vol  Full", 15, (1, 1, 1, 1), bold=True)

    def draw_feature_card(self, r):
        r.draw_shadow(74, 658, 372, 54, 24, 0.045)
        r.draw_texture(str(TEXTURES / "journal-desk.png"), 74, 658, 372, 54, 0.92)
        r.draw_rounded_rect(74, 658, 372, 54, 24, (0.11, 0.08, 0.05, 0.34))
        r.draw_text(96, 666, "A quiet one-minute guide", 19, (1, 1, 1, 1), bold=True)
        r.draw_text(96, 689, "Designed for the pause before studying again.", 12, (1, 1, 1, 0.90))

    def draw_voice_panel(self, r):
        r.draw_shadow(54, 864, 412, 64, 24, 0.050)
        r.draw_rounded_rect(54, 864, 412, 64, 24, (1, 1, 1, 0.92))
        r.draw_text(78, 878, "Voice check-in", 18, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_text(78, 902, "Record a short feeling note.", 13, (0.44, 0.48, 0.58, 1))
        pulse = 1.0 + (0.08 * math.sin(time.time() * 8) if self.recording else 0)
        r.draw_circle(420, 896, 28 * pulse, (0.91, 0.55, 0.66, 1))
        r.draw_rounded_rect(411, 876, 18, 26, 9, (1, 1, 1, 1))
        r.draw_rounded_rect(404, 897, 32, 16, 8, (1, 1, 1, 0.96))
        r.draw_rounded_rect(415, 911, 12, 4, 2, (1, 1, 1, 1))

    def draw(self):
        r = self.renderer

        r.draw_gradient(0, 0, 520, 960, (0.91, 0.88, 0.82, 1), (0.98, 0.96, 0.92, 1))
        r.draw_shadow(24, 16, 472, 928, 48, 0.08)
        r.draw_rounded_rect(24, 16, 472, 928, 48, (0.98, 0.96, 0.92, 1))

        self.draw_status_bar(r)
        self.draw_back_button(r)

        r.draw_text(132, 116, "Guided Calm Video", 30, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_text(132, 164, "Breathing Exercise", 20, (0.44, 0.48, 0.58, 1))

        self.draw_video(r)

        r.draw_text(54, 532, "1-Minute Guided Breathing", 19, (0.43, 0.51, 0.90, 1), bold=True)
        r.draw_text(54, 560, "Take a soft pause", 31, (0.18, 0.20, 0.26, 1), bold=True)
        r.draw_text(54, 602, "Follow the breathing rhythm and let your body", 18, (0.44, 0.48, 0.58, 1))
        r.draw_text(54, 628, "slow down for one minute.", 18, (0.44, 0.48, 0.58, 1))

        self.draw_feature_card(r)

        for button in self.buttons:
            button.draw(r)

        if self.saved:
            r.draw_rounded_rect(146, 826, 228, 40, 20, (0.18, 0.20, 0.26, 0.92))
            r.draw_text(176, 836, "Saved to your resources", 15, (1, 1, 1, 1), bold=True)

        self.draw_voice_panel(r)

        r.draw_rounded_rect(178, 930, 164, 5, 3, (0.20, 0.20, 0.20, 0.18))
