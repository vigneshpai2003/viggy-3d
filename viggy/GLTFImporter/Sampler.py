from enum import IntEnum
from typing import Optional

from viggy.GLTFImporter.GLTFObject import GLTFObject


class TextureMagFilter(IntEnum):
    NEAREST = 9728
    LINEAR = 9729


class TextureMinFilter(IntEnum):
    NEAREST = 9728
    LINEAR = 9729
    NEAREST_MIPMAP_NEAREST = 9984
    LINEAR_MIPMAP_NEAREST = 9985
    NEAREST_MIPMAP_LINEAR = 9986
    LINEAR_MIPMAP_LINEAR = 9987


class TextureWrap(IntEnum):
    CLAMP_TO_EDGE = 33071
    MIRRORED_REPEAT = 33648
    REPEAT = 10497


class Sampler(GLTFObject):
    def __init__(self, file, index: int):
        super().__init__(file, "samplers", index)

        if "magFilter" in self.jsonDict:
            self.magFilter: Optional[TextureMagFilter] = TextureMagFilter(self.jsonDict["magFilter"])
        else:
            self.magFilter: Optional[TextureMagFilter] = None

        if "minFilter" in self.jsonDict:
            self.minFilter: Optional[TextureMinFilter] = TextureMinFilter(self.jsonDict["minFilter"])
        else:
            self.minFilter: Optional[TextureMinFilter] = None

        self.wrapS = TextureWrap(self.getFromJSONDict("wrapS", int(TextureWrap.REPEAT)))
        self.wrapT = TextureWrap(self.getFromJSONDict("wrapT", int(TextureWrap.REPEAT)))

    def __getMagFilter(self):
        return

    def __getMinFilter(self):
        return
