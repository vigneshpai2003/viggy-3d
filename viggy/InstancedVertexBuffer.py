from typing import Tuple

import OpenGL.GL as GL
import numpy as np

from .VertexBuffer import VertexBuffer


class InstancedVertexBuffer(VertexBuffer):
    def __init__(self, array: np.ndarray, indices: Tuple, layout: Tuple, divisors: Tuple):
        """
        :param array:
        :param indices:
        :param layout:
        :param divisors: the divisor for each index, tells OpenGL when to update the vertex attribute
                0: update for every iteration of vertex shader
                n: update for after every n instance drawings
        """
        super().__init__(array, indices, layout)

        self.divisors = divisors

        for i in range(self.vertexAttributesNo):
            GL.glVertexAttribDivisor(self.indices[i], self.divisors[i])
