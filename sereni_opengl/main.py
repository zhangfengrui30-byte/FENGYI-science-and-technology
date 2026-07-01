#!/usr/bin/env python3
"""
Sereni - Guided Calm Desktop Prototype
Built with Python, GLFW, and OpenGL for an HCI high-fidelity alpha prototype.
"""

import sys


try:
    import glfw
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: glfw. Install with:\n"
        "  pip install -r sereni_opengl/requirements.txt"
    ) from exc

from audio.player import AudioPlayer
from screens.base import SOUNDS
from screens.breathing import BreathingScreen
from screens.home import HomeScreen
from screens.reflection import ReflectionScreen
from screens.resources import ResourcesScreen
from ui.renderer import Renderer
from ui.window import Window


class SereniApp:
    def __init__(self):
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        self.window = Window(1024, 768, "Sereni - Guided Calm OpenGL Prototype")
        self.renderer = Renderer(1024, 768)
        self.audio = AudioPlayer()
        self.screens = {
            "home": HomeScreen(self.renderer),
            "reflection": ReflectionScreen(self.renderer),
            "breathing": BreathingScreen(self.renderer),
            "resources": ResourcesScreen(self.renderer),
        }
        self.current = "home"
        self.window.set_mouse_button_callback(self.on_mouse_button)
        self.window.set_cursor_pos_callback(self.on_cursor)
        self.window.set_key_callback(self.on_key)

    def switch(self, name):
        if name in self.screens:
            if self.current == "breathing" and name != "breathing":
                self.screens["breathing"].playing = False
                self.audio.stop()
            self.current = name

    def on_cursor(self, _window, x, y):
        self.screens[self.current].update_hover(x, y)

    def on_key(self, _window, key, _scancode, action, _mods):
        if action != glfw.PRESS:
            return
        if key == glfw.KEY_ESCAPE:
            if self.current == "home":
                self.window.close()
            else:
                self.switch("home")
        if key == glfw.KEY_SPACE and self.current == "breathing":
            self.handle_action("start_video")

    def on_mouse_button(self, _window, button, action, _mods):
        if button != glfw.MOUSE_BUTTON_LEFT or action != glfw.PRESS:
            return
        x, y = self.window.get_cursor_pos()
        action_name = self.screens[self.current].handle_click(x, y)
        if action_name:
            self.handle_action(action_name)

    def handle_action(self, action_name):
        breathing = self.screens["breathing"]
        if action_name in self.screens:
            self.switch(action_name)
            return
        if action_name == "home":
            self.switch("home")
            return
        if action_name == "start_video":
            self.switch("breathing")
            breathing.playing = True
            if not breathing.started_at:
                import time
                breathing.started_at = time.time()
            self.audio.play(str(SOUNDS / "calm_music.wav"), loop=True)
        elif action_name == "pause_video":
            breathing.playing = False
            self.audio.stop()
        elif action_name == "replay_video":
            import time
            breathing.started_at = time.time()
            breathing.playing = True
            self.audio.play(str(SOUNDS / "calm_music.wav"), loop=True)
        elif action_name == "save_resource":
            breathing.saved = True

    def run(self):
        while not self.window.should_close():
            self.renderer.clear()
            self.screens[self.current].draw()
            self.window.swap_buffers()
            glfw.poll_events()
        self.cleanup()

    def cleanup(self):
        self.audio.cleanup()
        glfw.terminate()


if __name__ == "__main__":
    app = SereniApp()
    try:
        app.run()
    except KeyboardInterrupt:
        app.cleanup()
        sys.exit(0)

