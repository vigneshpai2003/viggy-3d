from ctypes import *

import numpy as np

from .Mesh import Mesh
from .GLTFTools import *


class Model:
    def __init__(self, path, binary=False):
        self.root = GLTFFile(path, binary)

        for rootNode in self.root.scene.nodes:
            self.__processNode()

    def __processNode(self, node):
        for nodeMesh in node.meshes:
            mesh = Mesh()

            # vertex buffer
            vertexData = []
            for i in range(len(nodeMesh.vertices)):
                vertexData.extend(nodeMesh.vertices[i])
                vertexData.extend(nodeMesh.texturecoords[0][i][:2])
                vertexData.extend(nodeMesh.normals[i])
            vertexData = np.array(vertexData)
            mesh.addVBO(vertexData, (0, 1, 2), (3, 2, 3))

            # index buffer
            mesh.addIBO(nodeMesh.faces)

            self.printTextures(nodeMesh.material)

            properties = nodeMesh.material.contents.mProperties
            n = nodeMesh.material.contents.mNumProperties

            index = 0

            for i in range(n):
                materialProperty = POINTER(MaterialProperty).from_address(
                    addressof(properties.contents) + i * sizeof(POINTER(MaterialProperty))).contents
                print(f"""
mData: {materialProperty.mData.contents.value}
mDataLength: {materialProperty.mDataLength}
mIndex: {materialProperty.mIndex}
mKey: {materialProperty.mKey.data}
mSemantic: {materialProperty.mSemantic}
mType: {materialProperty.mType}
""")

            self.meshes.append((mesh, index))

        for childNode in node.children:
            self.__processNode(childNode)

    def draw(self):
        for mesh, textureIndex in self.meshes:
            self.textures[textureIndex].bind(0)
            mesh.draw()
