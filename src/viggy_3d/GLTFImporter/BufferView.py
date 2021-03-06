from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

from enum import IntEnum

from .GLTFObject import GLTFObject
from .Buffer import Buffer


class BufferTarget(IntEnum):
    ARRAY_BUFFER = 34962
    ELEMENT_ARRAY_BUFFER = 34963


class BufferView(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "bufferViews", index)

        self.buffer: Buffer = self.createFromKey(Buffer, "buffers", "buffer")

        # the length of data owned in bytes, need not be continuous
        self.byteLength: int = self.jsonDict["byteLength"]

        # the number of bytes into buffer that bufferView starts
        self.byteOffset: int = self.getFromJSONDict("byteOffset", 0)

        self.byteStride: Optional[int] = self.getFromJSONDict("byteStride")

        if "target" in self.jsonDict:
            self.target: Optional[BufferTarget] = BufferTarget(self.jsonDict["target"])
        else:
            self.target: Optional[BufferTarget] = None
