from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile


from .GLTFObject import GLTFObject
from .Primitive import Primitive


class Mesh(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "meshes", index)

        # the primitives that the mesh contains
        self.primitives = [Primitive(file, primitiveDict) for primitiveDict in self.jsonDict["primitives"]]
