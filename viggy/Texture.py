import OpenGL.GL as GL
from PIL import Image


class Texture:
    def __init__(self, f_path: str):
        self.texture = GL.glGenTextures(1)

        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

        # define texture image details
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)

        img = Image.open(f_path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # needed due to internal storage format in GLSL

        # send data to OpenGL
        # (texture_type, 0, internal format, width, height, border, OpenGL format, type, data)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, img.width, img.height,
                        0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE,
                        img.convert("RGBA").tobytes())
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)  # needed because of GL_LINEAR_MIPMAP_LINEAR

    def bind(self, unit: int):
        """
        bind to unit before drawing
        """
        GL.glActiveTexture(eval(f"GL.GL_TEXTURE{unit}"))
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
