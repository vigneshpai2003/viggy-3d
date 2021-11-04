from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

import os
import io

from .GLTFObject import GLTFObject
from .BufferView import BufferView


class Image(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "images", index)

        self.uri: str = self.getFromJSONDict("uri")

        self.bufferView = self.createFromKey(BufferView, "bufferViews", "bufferView")

        # mime type is defined when bufferView is not None, one of "image/jpeg" or "image/png"
        self.mimeType = self.getFromJSONDict("mimeType")

        # path to image data generally stored as png or jpg
        self.path = self.__getImgPath()

    def __getImgPath(self):
        if self.uri is not None:
            if os.path.isabs(self.uri):
                path = self.uri
            else:
                path = self.file.path.parent.joinpath(self.uri)

            return path

        return io.BytesIO(self.bufferView.buffer.data[self.bufferView.byteOffset:
                                                      self.bufferView.byteOffset + self.bufferView.byteLength])
