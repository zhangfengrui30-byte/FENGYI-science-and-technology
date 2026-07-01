import os
import threading
import time


class AudioPlayer:
    """Simple WAV playback wrapper. Falls back gracefully when simpleaudio is unavailable."""

    def __init__(self):
        self._play_obj = None
        self._loop_thread = None
        self._looping = False
        self.available = True
        try:
            import simpleaudio as sa
            self._sa = sa
        except Exception:
            self._sa = None
            self.available = False

    @property
    def is_playing(self):
        return bool(self._play_obj and self._play_obj.is_playing())

    def play(self, path, loop=False):
        if not self._sa:
            print("simpleaudio is not installed. Audio playback is disabled.")
            return
        if not os.path.exists(path):
            print(f"Audio file not found: {path}")
            return

        self.stop()
        wave_obj = self._sa.WaveObject.from_wave_file(path)
        if loop:
            self._looping = True

            def run_loop():
                while self._looping:
                    self._play_obj = wave_obj.play()
                    while self._looping and self._play_obj.is_playing():
                        time.sleep(0.1)

            self._loop_thread = threading.Thread(target=run_loop, daemon=True)
            self._loop_thread.start()
        else:
            self._play_obj = wave_obj.play()

    def stop(self):
        self._looping = False
        if self._play_obj:
            self._play_obj.stop()
        self._play_obj = None

    def cleanup(self):
        self.stop()

