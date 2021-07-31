from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import GLTFFile

from enum import IntEnum
import struct

from .GLTFObject import GLTFObject
from .BufferView import BufferView


class ComponentType(IntEnum):
    BYTE = 5120
    UNSIGNED_BYTE = 5121
    SHORT = 5122
    UNSIGNED_SHORT = 5123
    INT = 5124
    UNSIGNED_INT = 5125
    FLOAT = 5126


def componentSize(componentType: ComponentType) -> int:
    if componentType in (ComponentType.BYTE, ComponentType.UNSIGNED_BYTE):
        return 1
    elif componentType in (ComponentType.SHORT, ComponentType.UNSIGNED_SHORT):
        return 2
    elif componentType in (ComponentType.UNSIGNED_INT, ComponentType.FLOAT):
        return 4


numComponent = {"SCALAR": 1,
                "VEC2": 2,
                "VEC3": 3,
                "VEC4": 4,
                "MAT2": 4,
                "MAT3": 9,
                "MAT4": 16}


class Accessor(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "accessors", index)

        if "bufferView" in self.jsonDict:
            self.bufferView: BufferView = self.createGLTFObject(BufferView, "bufferViews", self.jsonDict["bufferView"])
        else:
            self.bufferView = None

        # type of the component as an int directly corresponding to OpenGL datatypes
        self.componentType = ComponentType(self.jsonDict["componentType"])

        # type of attribute stored in bufferView
        self.type: str = self.jsonDict["type"]

        # the number of attribute values owned by accessor
        self.count: int = self.jsonDict["count"]

        # the number of bytes into the bufferView that the accessor starts
        self.byteOffset: int = self.getFromJSONDict("byteOffset", 0)

        self.normalized: bool = self.getFromJSONDict("normalized", False)

        self.min = self.getFromJSONDict("min")
        self.max = self.getFromJSONDict("max")

        self.data = self.__getData()

    @property
    def componentSize(self) -> int:
        return componentSize(self.componentType)

    @property
    def numComponent(self) -> int:
        return numComponent[self.type]

    @property
    def stride(self) -> int:
        if self.bufferView.byteStride is not None:
            return self.bufferView.byteStride
        else:
            return self.componentSize * self.numComponent

    def __getData(self):
        if self.bufferView is None:
            return None

        data = []

        offset = self.byteOffset + self.bufferView.byteOffset

        if self.componentType == ComponentType.BYTE:
            formatChar = 'c'
        elif self.componentType == ComponentType.UNSIGNED_BYTE:
            formatChar = 'B'
        elif self.componentType == ComponentType.SHORT:
            formatChar = 'h'
        elif self.componentType == ComponentType.UNSIGNED_SHORT:
            formatChar = 'H'
        elif self.componentType == ComponentType.INT:
            formatChar = 'i'
        elif self.componentType == ComponentType.UNSIGNED_INT:
            formatChar = 'I'
        else:  # elif self.componentType == ComponentType.FLOAT:
            formatChar = 'f'

        for _ in range(self.count):
            data.append(struct.unpack_from(
                        '<' + formatChar * self.numComponent,
                        self.bufferView.buffer.data[offset: offset + self.componentSize * self.numComponent]))
            offset += self.stride

        return data
