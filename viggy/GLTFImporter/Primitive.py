from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

from enum import IntEnum

from .Material import Material
from .Accessor import Accessor
from .GLTFObject import getFromJSONDict, createFromKey


class PrimitiveMode(IntEnum):
    POINTS = 0
    LINES = 1
    LINE_LOOP = 2
    LINE_STRIP = 3
    TRIANGLES = 4
    TRIANGLE_STRIP = 5
    TRIANGLE_FAN = 6


class Primitive:
    def __init__(self, file: GLTFFile, primitiveDict: dict):
        self.jsonDict = primitiveDict

        self.attributes = Attribute(file, self.jsonDict["attributes"])

        self.mode = PrimitiveMode(getFromJSONDict(self.jsonDict, "mode", 4))

        # index buffer
        self.indices = createFromKey(file, Accessor, "accessors", self.jsonDict, "indices")

        # material
        self.material: Material = createFromKey(file, Material, "materials", self.jsonDict, "material")


class Attribute:
    def __init__(self, file, attributeDict: dict):
        self.jsonDict = attributeDict

        # GLTF file format does not specify the keys of attributeDict
        # however all values are accessor indices
        # POSITION, NORMAL, TANGENT, TEXCOORD_n are expected to be present as keys

        self.position = self.__getAttribute(file, "POSITION")
        self.normal = self.__getAttribute(file, "NORMAL")
        self.tangent = self.__getAttribute(file, "TANGENT")

        n = 0
        while True:
            if f"TEXCOORD_{n}" in self.jsonDict:
                setattr(self, f"texCoord{n}", Accessor(file, self.jsonDict[f"TEXCOORD_{n}"]))
            else:
                break
            n += 1

    def __getAttribute(self, file, attribute: str) -> Accessor:
        return Accessor(file, self.jsonDict[attribute]) if attribute in self.jsonDict else None
