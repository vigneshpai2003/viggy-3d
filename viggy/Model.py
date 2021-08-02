from typing import List

import glm

import viggy.GLTFImporter as gltf

from .Mesh import Mesh
from .Shader import Shader
from .Texture import Texture


class Model:
    def __init__(self, path, binary=False):
        self.root = gltf.GLTFFile(path, binary)
        self.meshes: List[Mesh] = []
        self.textures: List[Texture] = []
        self.transforms: List[glm.mat4x4] = []

        for rootNode in self.root.scene.rootNodes:
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
                                        primitive.indices.data))
                self.textures.append(Texture(primitive.material.pbrInfo.baseColorTextureInfo.texture.image.data))
                self.transforms.append(transform)

    def draw(self, shader: Shader, model: glm.mat4x4):
        for i in range(len(self.meshes)):
            self.textures[i].bind(0)
            transform = model * self.transforms[i]
            shader.setUniform("model", glm.value_ptr(transform))
            self.meshes[i].draw()
