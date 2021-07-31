from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import GLTFFile

import os

from .GLTFObject import GLTFObject


class Buffer(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "buffers", index)

        self.byteLength: int = self.jsonDict["byteLength"]
        self.uri: str = self.getFromJSONDict("uri")

        self.data = self.__loadFromUri()

    def __loadFromUri(self):
        if self.uri is None and self.file.isBinary:
            return self.file.binaryData
        if os.path.isabs(self.uri):
            path = self.uri
        else:
            path = self.file.path.parent.joinpath(self.uri)

        with open(path, 'rb') as f:
            return f.read()
