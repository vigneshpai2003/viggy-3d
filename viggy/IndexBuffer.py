import numpy as np
import OpenGL.GL as GL


class IndexBuffer:
    def __init__(self, array: np.ndarray):
        """
        :param array:  shape(n,3), dtype(uint)
        """
        self.length = array.shape[0]
        self.buffer = array.flatten()  # is passed to OpenGL flattened
        self.glBuffer = GL.glGenBuffers(1)
        self.bind()
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffer.nbytes, self.buffer, GL.GL_STATIC_DRAW)

    def bind(self):
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.glBuffer)
