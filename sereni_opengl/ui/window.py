import glfw


class Window:
    """GLFW window and input event bridge."""

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        if hasattr(glfw, "COCOA_RETINA_FRAMEBUFFER"):
            glfw.window_hint(glfw.COCOA_RETINA_FRAMEBUFFER, glfw.FALSE)
        self._window = glfw.create_window(width, height, title, None, None)
        if not self._window:
            raise RuntimeError("Failed to create GLFW window")

        glfw.make_context_current(self._window)
        glfw.swap_interval(1)
        glfw.set_window_pos(self._window, 120, 80)
        glfw.show_window(self._window)
        glfw.focus_window(self._window)

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
        x, y = glfw.get_cursor_pos(self._window)
        return self.map_cursor_pos(x, y)

    def map_cursor_pos(self, x, y):
        window_width, window_height = glfw.get_window_size(self._window)
        if window_width and window_height:
            x = x * self.width / window_width
            y = y * self.height / window_height
        return x, y
