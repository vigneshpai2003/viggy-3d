from enum import IntEnum

from viggy.GLTFTools.GLTFObject import GLTFObject


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
            self.magFilter = TextureMagFilter(self.jsonDict["magFilter"])
        else:
            self.magFilter = None

        if "minFilter" in self.jsonDict:
            self.minFilter = TextureMinFilter(self.jsonDict["minFilter"])
        else:
            self.minFilter = None

        self.wrapS = TextureWrap(self.getFromJSONDict("wrapS", int(TextureWrap.REPEAT)))
        self.wrapT = TextureWrap(self.getFromJSONDict("wrapT", int(TextureWrap.REPEAT)))
