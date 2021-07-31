from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

from .GLTFObject import GLTFObject
from .Node import Node


class Scene(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "scenes", index)

        # root nodes
        if "nodes" in self.jsonDict:
            self.nodes: List[Node] = [self.createGLTFObject(Node, "nodes", i) for i in self.jsonDict["nodes"]]
        else:
            self.nodes = None
