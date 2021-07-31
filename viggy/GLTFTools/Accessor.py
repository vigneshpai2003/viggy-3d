from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

from enum import IntEnum
import struct

import numpy as np

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


componentSize = {ComponentType.BYTE: 1,
                 ComponentType.UNSIGNED_BYTE: 1,
                 ComponentType.SHORT: 2,
                 ComponentType.UNSIGNED_SHORT: 2,
                 ComponentType.INT: 4,
                 ComponentType.UNSIGNED_INT: 4,
                 ComponentType.FLOAT: 4}

componentFormat = {ComponentType.BYTE: 'c',
                   ComponentType.UNSIGNED_BYTE: 'B',
                   ComponentType.SHORT: 'h',
                   ComponentType.UNSIGNED_SHORT: 'H',
                   ComponentType.INT: 'i',
                   ComponentType.UNSIGNED_INT: 'I',
                   ComponentType.FLOAT: 'f'}

componentNumpyType = {ComponentType.BYTE: np.byte,
                      ComponentType.UNSIGNED_BYTE: np.ubyte,
                      ComponentType.SHORT: np.short,
                      ComponentType.UNSIGNED_SHORT: np.ushort,
                      ComponentType.INT: np.intc,
                      ComponentType.UNSIGNED_INT: np.uintc,
                      ComponentType.FLOAT: np.single}

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

        self.bufferView = self.createFromKey(BufferView, "bufferViews", "bufferView")

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

        self.data = np.array(self.__getDataBuffer(), dtype=componentNumpyType[self.componentType])

    @property
    def componentSize(self) -> int:
        return componentSize[self.componentType]

    @property
    def numComponent(self) -> int:
        return numComponent[self.type]

    @property
    def stride(self) -> int:
        if self.bufferView.byteStride is not None:
            return self.bufferView.byteStride
        else:
            return self.componentSize * self.numComponent

    def __getDataBuffer(self):
        if self.bufferView is None:
            return None

        data = []

        offset = self.byteOffset + self.bufferView.byteOffset

        for _ in range(self.count):
            dataArray = struct.unpack_from('<' + componentFormat[self.componentType] * self.numComponent,
                                           self.bufferView.buffer.data[
                                           offset: offset + self.componentSize * self.numComponent])
            if self.numComponent == 1:
                data.extend(dataArray)
            else:
                data.append(dataArray)
            offset += self.stride

        return data
