import ctypes
from typing import Tuple

import OpenGL.GL as GL
import numpy as np


class VertexBuffer:
    def __init__(self, array: np.ndarray, indices: Tuple, layout: Tuple):
        """
        :param array: the data of the buffer as a numpy array (need not be 1D)
        :param indices: the index of the vertex attribute in the shader for every attribute in array
        :param layout: the number of elements per vertex attribute
        """
        self.buffer = array.flatten()  # the raw data of the buffer
        self.indices = indices  # the index of the vertex attribute in the shader attribute wise
        self.layout = layout  # the number of elements per vertex attribute
        self.vertexAttributesNo = len(self.layout)  # the number of vertex attributes per vertex
        self.vertexSize = sum(self.layout)  # size of each vertex
        self.vertexNo = int(len(self.buffer) / self.vertexSize)  # total number of vertices

        # create the OpenGL buffer
        self.glBuffer = GL.glGenBuffers(1)
        self.bind()
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.buffer.nbytes, self.buffer, GL.GL_STATIC_DRAW)

        # tell OpenGL the vertex attributes
        for i in range(self.vertexAttributesNo):
            GL.glEnableVertexAttribArray(self.indices[i])
            # (index, length of attribute, type, normalization, stride, (void*)offset)
            GL.glVertexAttribPointer(self.indices[i], self.layout[i], GL.GL_FLOAT, GL.GL_FALSE,
                                     self.vertexSize * self.buffer.itemsize,
                                     ctypes.c_void_p(sum(layout[:i]) * self.buffer.itemsize))

    def bind(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.glBuffer)
