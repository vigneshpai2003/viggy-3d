from OpenGL import GL

from .IndexBuffer import IndexBuffer
from .InstancedVertexBuffer import InstancedVertexBuffer
from .VertexBuffer import VertexBuffer


class Mesh:
    def __init__(self):
        self.VAO = GL.glGenVertexArrays(1)
        self.VBO = None
        self.IVBO = None
        self.IBO = None

    def addVBO(self, array, indices, layout):
        GL.glBindVertexArray(self.VAO)
        self.VBO = VertexBuffer(array, indices, layout)

    def addIVBO(self, array, indices, layout, divisors):
        GL.glBindVertexArray(self.VAO)
        self.IVBO = InstancedVertexBuffer(array, indices, layout, divisors)

    def addIBO(self, indices):
        GL.glBindVertexArray(self.VAO)
        self.IBO = IndexBuffer(indices)

    def draw(self):
        """
        draws mesh, user must ensure that the right shader is bound
        """
        GL.glBindVertexArray(self.VAO)

        instance_count = self.IVBO.vertexNo if self.IVBO else 1

        if self.IBO:
            GL.glDrawElementsInstanced(GL.GL_TRIANGLES, self.IBO.length * 3, GL.GL_UNSIGNED_INT, None, instance_count)
        else:
            GL.glDrawArraysInstanced(GL.GL_TRIANGLES, 0, self.VBO.vertexNo * 3, instance_count)
