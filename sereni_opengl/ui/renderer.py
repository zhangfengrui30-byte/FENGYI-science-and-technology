import math
import os

from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageDraw, ImageFont


class Renderer:
    """OpenGL 2D renderer for the Sereni desktop prototype."""

    def __init__(self, width=1024, height=768):
        self.width = width
        self.height = height
        self.text_cache = {}
        self.texture_cache = {}
        self.font_regular = "/System/Library/Fonts/Supplemental/Arial.ttf"
        self.font_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)

    def clear(self):
        glClearColor(0.953, 0.933, 0.902, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def draw_rect(self, x, y, width, height, color):
        glDisable(GL_TEXTURE_2D)
        glColor4f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()
        glEnable(GL_TEXTURE_2D)

    def draw_gradient(self, x, y, width, height, top, bottom):
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glColor4f(*top)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glColor4f(*bottom)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()
        glEnable(GL_TEXTURE_2D)

    def draw_circle(self, cx, cy, radius, color, segments=72):
        glDisable(GL_TEXTURE_2D)
        glColor4f(*color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx, cy)
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            glVertex2f(cx + radius * math.cos(angle), cy + radius * math.sin(angle))
        glEnd()
        glEnable(GL_TEXTURE_2D)

    def draw_triangle(self, points, color):
        glDisable(GL_TEXTURE_2D)
        glColor4f(*color)
        glBegin(GL_TRIANGLES)
        for x, y in points:
            glVertex2f(x, y)
        glEnd()
        glEnable(GL_TEXTURE_2D)

    def draw_rounded_rect(self, x, y, width, height, radius, color, segments=18):
        radius = min(radius, width / 2, height / 2)
        glDisable(GL_TEXTURE_2D)
        glColor4f(*color)

        def corner(cx, cy, start, end):
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(cx, cy)
            for i in range(segments + 1):
                a = start + (end - start) * i / segments
                glVertex2f(cx + math.cos(a) * radius, cy + math.sin(a) * radius)
            glEnd()

        self.draw_rect(x + radius, y, width - radius * 2, height, color)
        self.draw_rect(x, y + radius, width, height - radius * 2, color)
        glDisable(GL_TEXTURE_2D)
        corner(x + radius, y + radius, math.pi, math.pi * 1.5)
        corner(x + width - radius, y + radius, math.pi * 1.5, math.pi * 2)
        corner(x + width - radius, y + height - radius, 0, math.pi * 0.5)
        corner(x + radius, y + height - radius, math.pi * 0.5, math.pi)
        glEnable(GL_TEXTURE_2D)

    def draw_shadow(self, x, y, width, height, radius=24, alpha=0.08):
        for i in range(6):
            self.draw_rounded_rect(
                x - i * 1.5,
                y + i * 3,
                width + i * 3,
                height + i * 1.5,
                radius + i,
                (0.12, 0.10, 0.08, alpha / (i + 1)),
            )

    def load_texture(self, path):
        path = os.path.abspath(path)
        if path in self.texture_cache:
            return self.texture_cache[path]

        image = Image.open(path).convert("RGBA")
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        data = image.tobytes()
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        self.texture_cache[path] = (tex, image.width, image.height)
        return self.texture_cache[path]

    def draw_texture(self, path, x, y, width, height, alpha=1.0):
        tex, _, _ = self.load_texture(path)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex)
        glColor4f(1, 1, 1, alpha)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(x, y)
        glTexCoord2f(1, 1)
        glVertex2f(x + width, y)
        glTexCoord2f(1, 0)
        glVertex2f(x + width, y + height)
        glTexCoord2f(0, 0)
        glVertex2f(x, y + height)
        glEnd()

    def _font(self, size, bold=False):
        path = self.font_bold if bold else self.font_regular
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            return ImageFont.load_default()

    def measure_text(self, text, size=18, bold=False):
        font = self._font(size, bold)
        bbox = font.getbbox(text)
        return max(1, bbox[2] - bbox[0] + 8), max(1, bbox[3] - bbox[1] + 8)

    def draw_text(self, x, y, text, size=18, color=(0.18, 0.20, 0.26, 1), bold=False):
        key = (text, size, color, bold)
        if key not in self.text_cache:
            font = self._font(size, bold)
            bbox = font.getbbox(text)
            width = max(1, bbox[2] - bbox[0] + 8)
            height = max(1, bbox[3] - bbox[1] + 8)
            image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)
            rgba = tuple(int(c * 255) for c in color)
            draw.text((4 - bbox[0], 4 - bbox[1]), text, font=font, fill=rgba)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            tex = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image.tobytes())
            self.text_cache[key] = (tex, width, height)

        tex, width, height = self.text_cache[key]
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex)
        glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(x, y)
        glTexCoord2f(1, 1)
        glVertex2f(x + width, y)
        glTexCoord2f(1, 0)
        glVertex2f(x + width, y + height)
        glTexCoord2f(0, 0)
        glVertex2f(x, y + height)
        glEnd()
        return width, height
