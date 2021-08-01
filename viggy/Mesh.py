from OpenGL import GL

from .IndexBuffer import IndexBuffer
from .VertexBuffer import VertexBuffer


class Mesh:
    def __init__(self, vertices, normals, texCoord, indices):
        self.VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.VAO)
        self.VBO = VertexBuffer(vertices, normals, texCoord)
        self.IBO = IndexBuffer(indices)

    def draw(self):
        """
        draws mesh, user must ensure that the right shader is bound
        """
        GL.glBindVertexArray(self.VAO)
        GL.glDrawElements(GL.GL_TRIANGLES, self.IBO.length * 3, GL.GL_UNSIGNED_INT, None)
