from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .core import GLTFFile

from .GLTFObject import GLTFObject
from .Mesh import Mesh


class Node(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "nodes", index)

        # matrix in column major order
        self.matrix: List[float] = self.getFromJSONDict("matrix", [1, 0, 0, 0,
                                                                   0, 1, 0, 0,
                                                                   0, 0, 1, 0,
                                                                   0, 0, 0, 1])

        # translation of each vertex
        self.translation: List[float, float, float] = self.getFromJSONDict("translation", [0, 0, 0])

        # rotation of each vertex as (x,y,z,w) quaternion
        self.rotation: List[float, float, float, float] = self.getFromJSONDict("rotation", [0, 0, 0, 1])

        # scaling of each vertex about each axis
        self.scale: List[float, float, float] = self.getFromJSONDict("scale", [1, 1, 1])

        # model = matrix * T * R * S

        # mesh
        if "mesh" in self.jsonDict:
            self.mesh: Mesh = self.createGLTFObject(Mesh, "meshes", self.jsonDict["mesh"])
        else:
            self.mesh = None

        # children
        if "children" in self.jsonDict:
            self.children: List[Node] = [self.createGLTFObject(Node, "nodes", i) for i in self.jsonDict["children"]]
        else:
            self.children = None
