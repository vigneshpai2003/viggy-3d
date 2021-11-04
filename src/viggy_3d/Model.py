from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .Graph import Graph

import glm

from .GLTFImporter import GLTFFile, Node, Mesh as gltfMesh, PrimitiveMode
from .Mesh import Mesh
from .Shader import Shader
from .Texture import Texture
from .Material import Material


class Model:
    def __init__(self, graph: Graph, file: GLTFFile):
        self.graph = graph
        self.graph.addModels(self)

        self.fileData = file
        self.meshes: List[Mesh] = []
        self.meshTransforms: List[glm.mat4x4] = []

        # load all textures into OpenGL
        self.textures: List[Texture] = [Texture(texture) if texture else None for texture in file.textures]

        # each material contains reference to loaded texture
        self.materials: List[Material] = [Material(material, self.textures) for material in file.materials]

        for rootNode in self.fileData.scene.rootNodes:
            self.__processNode(rootNode)

        self.transform = glm.mat4()

    def setTransform(self, transform: glm.mat4):
        self.transform = transform

    def __processNode(self, node: Node):
        if node.mesh:
            self.__processMesh(node.mesh, node.globalTransform)

        if node.children:
            for childNode in node.children:
                self.__processNode(childNode)

    def __processMesh(self, mesh: gltfMesh, transform: glm.mat4x4):
        for primitive in mesh.primitives:
            if primitive.mode is PrimitiveMode.TRIANGLES:
                self.meshes.append(Mesh(primitive.attributes.position.data,
                                        primitive.attributes.normal.data,
                                        primitive.attributes.texCoord0.data,
                                        primitive.indices.data, self.materials[primitive.material.index]))
                self.meshTransforms.append(transform)

    def draw(self, shader: Shader):
        for i in range(len(self.meshes)):
            transform = self.transform * self.meshTransforms[i]
            shader.setUniform("model", glm.value_ptr(transform))
            self.meshes[i].draw()
