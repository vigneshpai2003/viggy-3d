from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np

import ctypes

import OpenGL.GL as GL


class VertexBuffer:
    def __init__(self, vertices: np.ndarray, normals: np.ndarray, texCoord: np.ndarray):
        # create the OpenGL buffer
        self.glBuffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.glBuffer)

        # allocate memory
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes + normals.nbytes + texCoord.nbytes, None, GL.GL_STATIC_DRAW)

        # fill memory
        GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
        GL.glBufferSubData(GL.GL_ARRAY_BUFFER, vertices.nbytes, normals.nbytes, normals)
        GL.glBufferSubData(GL.GL_ARRAY_BUFFER, vertices.nbytes + normals.nbytes, texCoord.nbytes, texCoord)

        # glVertexAttribPointer(index, length of attribute, type, normalization, stride, (void*)offset)

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * 4, ctypes.c_void_p(0))

        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * 4, ctypes.c_void_p(vertices.nbytes))

        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(
            2, 2, GL.GL_FLOAT, GL.GL_FALSE, 2 * 4, ctypes.c_void_p(vertices.nbytes + normals.nbytes))
