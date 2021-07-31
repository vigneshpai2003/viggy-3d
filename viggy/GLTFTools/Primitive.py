from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

from enum import IntEnum

from .Material import Material
from .Accessor import Accessor
from .GLTFObject import getFromJSONDict, createGLTFObject


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
        if "indices" in self.jsonDict:
            self.indices: Accessor = createGLTFObject(file, Accessor, "accessors", self.jsonDict["indices"])
        else:
            self.indices = None

        # material
        if "material" in self.jsonDict:
            self.material: Material = createGLTFObject(file, Material, "materials", self.jsonDict["material"])
        else:
            self.material = None


class Attribute:
    def __init__(self, file, attributeDict: dict):
        self.jsonDict = attributeDict

        # GLTF file format does not specify the keys of attributeDict
        # however all values are accessor indices
        # POSITION, NORMAL, TANGENT, TEXCOORD_n are expected to be present as keys

        if "POSITION" in self.jsonDict:
            self.position = Accessor(file, self.jsonDict["POSITION"])
        else:
            self.position = None

        if "NORMAL" in self.jsonDict:
            self.normal = Accessor(file, self.jsonDict["NORMAL"])
        else:
            self.normal = None

        if "TANGENT" in self.jsonDict:
            self.tangent = Accessor(file, self.jsonDict["TANGENT"])
        else:
            self.tangent = None

        n = 0
        while True:
            if f"TEXCOORD_{n}" in self.jsonDict:
                setattr(self, f"texCoord{n}", Accessor(file, self.jsonDict[f"TEXCOORD_{n}"]))
            else:
                break
            n += 1
