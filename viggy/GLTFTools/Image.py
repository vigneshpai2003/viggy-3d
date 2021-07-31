from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

import os
import io

import PIL.Image

from .GLTFObject import GLTFObject
from .BufferView import BufferView


class Image(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "images", index)

        self.uri: str = self.getFromJSONDict("uri")

        if "bufferView" in self.jsonDict:
            self.bufferView = self.createGLTFObject(BufferView, "bufferViews", self.jsonDict["bufferView"])
        else:
            self.bufferView = None

        # mime type is defined when bufferView is not None, one of "image/jpeg" or "image/png"
        self.mimeType = self.getFromJSONDict("mimeType")

        self.data = self.__convertImgToBytes(self.__getImgPath())

    @staticmethod
    def __convertImgToBytes(path):
        with PIL.Image.open(path) as img:
            return img.transpose(PIL.Image.FLIP_TOP_BOTTOM).tobytes()

    def __getImgPath(self):
        if self.uri is not None:
            if os.path.isabs(self.uri):
                path = self.uri
            else:
                path = self.file.path.parent.joinpath(self.uri)

            return path

        return io.BytesIO(self.bufferView.buffer.data[self.bufferView.byteOffset:
                                                      self.bufferView.byteOffset + self.bufferView.byteLength])
