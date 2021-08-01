from enum import IntEnum

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

        self.magFilter = self.__getMagFilter()
        self.minFilter = self.__getMinFilter()

        self.wrapS = TextureWrap(self.getFromJSONDict("wrapS", int(TextureWrap.REPEAT)))
        self.wrapT = TextureWrap(self.getFromJSONDict("wrapT", int(TextureWrap.REPEAT)))

    def __getMagFilter(self):
        return TextureMagFilter(self.jsonDict["magFilter"]) if "magFilter" in self.jsonDict else None

    def __getMinFilter(self):
        return TextureMinFilter(self.jsonDict["minFilter"]) if "minFilter" in self.jsonDict else None

