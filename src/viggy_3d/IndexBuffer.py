from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np

import OpenGL.GL as GL


class IndexBuffer:
    def __init__(self, array: np.ndarray):
        self.buffer = array
        self.length = array.size // 3  # number of faces
        self.glBuffer = GL.glGenBuffers(1)
        self.bind()
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffer.nbytes, self.buffer, GL.GL_STATIC_DRAW)

    def bind(self):
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.glBuffer)
