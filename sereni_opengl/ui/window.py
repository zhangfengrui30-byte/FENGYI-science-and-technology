import glfw


class Window:
    """GLFW window and input event bridge."""

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self._window = glfw.create_window(width, height, title, None, None)
        if not self._window:
            raise RuntimeError("Failed to create GLFW window")

        glfw.make_context_current(self._window)
        glfw.swap_interval(1)

    def set_mouse_button_callback(self, callback):
        glfw.set_mouse_button_callback(self._window, callback)

    def set_cursor_pos_callback(self, callback):
        glfw.set_cursor_pos_callback(self._window, callback)

    def set_key_callback(self, callback):
        glfw.set_key_callback(self._window, callback)

    def should_close(self):
        return glfw.window_should_close(self._window)

    def close(self):
        glfw.set_window_should_close(self._window, True)

    def swap_buffers(self):
        glfw.swap_buffers(self._window)

    def get_cursor_pos(self):
        return glfw.get_cursor_pos(self._window)

