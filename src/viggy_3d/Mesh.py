from OpenGL import GL

from .IndexBuffer import IndexBuffer
from .VertexBuffer import VertexBuffer
from .Material import Material


class Mesh:
    def __init__(self, vertices, normals, texCoord, indices, material: Material):
        self.VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.VAO)
        self.VBO = VertexBuffer(vertices, normals, texCoord)
        self.IBO = IndexBuffer(indices)

        self.material = material

    def draw(self):
        """
        draws mesh, user must ensure that the right shader is bound
        """
        self.material.baseTexture.bind(0)
        GL.glBindVertexArray(self.VAO)
        GL.glDrawElements(GL.GL_TRIANGLES, self.IBO.length * 3, GL.GL_UNSIGNED_INT, None)
