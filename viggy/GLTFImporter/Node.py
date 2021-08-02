from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

import glm

from .GLTFObject import GLTFObject
from .Mesh import Mesh


class Node(GLTFObject):
    def __init__(self, file: GLTFFile, index: int, parent: Node):
        super().__init__(file, "nodes", index)

        self.parent = parent

        # matrix in column major order
        self.matrix: List[float] = self.getFromJSONDict("matrix")

        # translation of each vertex
        self.translation: List[float, float, float] = self.getFromJSONDict("translation", [0, 0, 0])

        # rotation of each vertex as (x,y,z,w) quaternion
        self.rotation: List[float, float, float, float] = self.getFromJSONDict("rotation", [0, 0, 0, 1])

        # scaling of each vertex about each axis
        self.scale: List[float, float, float] = self.getFromJSONDict("scale", [1, 1, 1])

        self.localTransform = self.__getLocalTransform()

        if parent is not None:
            self.globalTransform = parent.globalTransform * self.localTransform
        else:
            self.globalTransform = self.localTransform

        # mesh
        self.mesh = self.createFromKey(Mesh, "meshes", "mesh")

        # children
        self.children = self.createArrayFromKey(Node, "nodes", "children", self)

    def __getLocalTransform(self) -> glm.mat4x4:
        if self.matrix is not None:
            return glm.mat4([self.matrix[:4],
                             self.matrix[4:8],
                             self.matrix[8:12],
                             self.matrix[12:16]])
        else:
            scale = glm.scale(glm.mat4(), self.scale)
            if self.rotation != [0.0, 0.0, 0.0, 1.0]:
                rotation = glm.mat4_cast(glm.quat([self.rotation[-1], *self.rotation[:3]]))
            else:
                rotation = glm.mat4()
            translate = glm.translate(glm.mat4(), self.translation)
            return translate * rotation * scale
