from typing import List

import glm

import viggy.GLTFImporter as gltf

from .Mesh import Mesh
from .Shader import Shader
from .Texture import Texture
from .Material import Material


class Model:
    def __init__(self, file: gltf.GLTFFile):
        self.fileData = file
        self.meshes: List[Mesh] = []
        self.meshTransforms: List[glm.mat4x4] = []

        # load all textures into OpenGL
        print(file.textures)
        self.textures: List[Texture] = [Texture(texture) if texture else None for texture in file.textures]

        # each material contains reference to loaded texture
        self.materials: List[Material] = [Material(material, self.textures) for material in file.materials]

        for rootNode in self.fileData.scene.rootNodes:
            self.__processNode(rootNode)

    def __processNode(self, node: gltf.Node):
        if node.mesh:
            self.__processMesh(node.mesh, node.globalTransform)

        if node.children:
            for childNode in node.children:
                self.__processNode(childNode)

    def __processMesh(self, mesh: gltf.Mesh, transform: glm.mat4x4):
        for primitive in mesh.primitives:
            if primitive.mode is gltf.PrimitiveMode.TRIANGLES:
                self.meshes.append(Mesh(primitive.attributes.position.data,
                                        primitive.attributes.normal.data,
                                        primitive.attributes.texCoord0.data,
                                        primitive.indices.data, self.materials[primitive.material.index]))
                self.meshTransforms.append(transform)

    def draw(self, shader: Shader, model: glm.mat4x4):
        for i in range(len(self.meshes)):
            transform = model * self.meshTransforms[i]
            shader.setUniform("model", glm.value_ptr(transform))
            self.meshes[i].draw()
