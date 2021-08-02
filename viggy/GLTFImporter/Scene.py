from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

from .GLTFObject import GLTFObject
from .Node import Node


class Scene(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "scenes", index)

        self.rootNodes = self.createArrayFromKey(Node, "nodes", "nodes", None)
