from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

from .GLTFObject import createGLTFObject, getFromJSONDict
from .Texture import Texture


class TextureInfo:
    def __init__(self, file: GLTFFile, infoDict: dict):
        self.jsonDict = infoDict

        self.texture = createGLTFObject(file, Texture, "textures", self.jsonDict["index"])
        self.texCoord: int = getFromJSONDict(self.jsonDict, "texCoord", 0)


class NormalTextureInfo(TextureInfo):
    def __init__(self, file: GLTFFile, infoDict: dict):
        super().__init__(file, infoDict)
        self.scale: int = getFromJSONDict(self.jsonDict, "scale", 1)


class OcclusionTextureInfo(TextureInfo):
    def __init__(self, file: GLTFFile, infoDict: dict):
        super().__init__(file, infoDict)
        self.strength: int = getFromJSONDict(self.jsonDict, "strength", 1)
