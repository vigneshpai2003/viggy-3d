from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

from .TextureInfo import NormalTextureInfo, OcclusionTextureInfo, TextureInfo
from .GLTFObject import GLTFObject, getFromJSONDict


class Material(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "materials", index)

        # whether texture is double sided
        self.doubleSided: bool = self.getFromJSONDict("doubleSided", False)

        # alphaMode may be "OPAQUE", "MASK", "BLEND"
        self.alphaMode: str = self.getFromJSONDict("alphaMode", "OPAQUE")

        # applicable only in "MASK" mode
        self.alphaCutoff: float = self.getFromJSONDict("alphaCutoff", 0.5)

        self.pbrInfo = self.__getPBRInfo()

        # normal texture map
        """
        Each texel represents the XYZ components of a normal vector in tangent space. 
        R [0, 255] -> X [-1, 1]
        G [0, 255] -> Y [-1, 1]
        B [128, 255] -> Z [1/255, 1]
        in GLSL, texture() maps RGB to [0, 1]
        vec3 normalVector = normalize(texture(<normalMap>, texCoord) * 2 - 1)
        """
        self.normalTextureInfo = self.__getNormalTextureInfo()

        # occlusion texture map
        # Consider only R value for each texel, indicates how much indirect light (ambient light) should be received
        self.occlusionTextureInfo = self.__getOcclusionTextureInfo()

        # emmisive texture map
        self.emissiveTextureInfo = self.__getEmissiveTextureInfo()

        # multiply each value with R,G,B from emmisiveTexture Texel
        self.emissiveFactor: List[float, float, float] = self.getFromJSONDict("emissiveFactor", [0, 0, 0])

    def __getPBRInfo(self) -> PBRInfo:
        return PBRInfo(self.file, self.jsonDict["pbrMetallicRoughness"])\
            if "pbrMetallicRoughness" in self.jsonDict else None

    def __getNormalTextureInfo(self) -> NormalTextureInfo:
        return NormalTextureInfo(self.file, self.jsonDict["normalTexture"])\
            if "normalTexture" in self.jsonDict else None

    def __getOcclusionTextureInfo(self) -> OcclusionTextureInfo:
        return OcclusionTextureInfo(self.file, self.jsonDict["normalTexture"])\
            if "occlusionTexture" in self.jsonDict else None

    def __getEmissiveTextureInfo(self) -> TextureInfo:
        return TextureInfo(self.file, self.jsonDict["normalTexture"])\
            if "emissiveTexture" in self.jsonDict else None


class PBRInfo:
    def __init__(self, file, pbrDict: dict):
        self.file = file
        self.jsonDict = pbrDict

        # each component is in [0,1]
        self.baseColorFactor: List[float, float, float, float] = getFromJSONDict(self.jsonDict, "baseColorFactor",
                                                                                 [1, 1, 1, 1])
        self.metallicFactor: float = getFromJSONDict(self.jsonDict, "metallicFactor", 1)
        self.roughnessFactor: float = getFromJSONDict(self.jsonDict, "roughnessFactor", 1)

        self.baseColorTextureInfo = self.__getTextureInfo("baseColorTexture")

        # for every texel, G corresponds to roughness and B to metalness
        self.metallicRoughnessTextureInfo = self.__getTextureInfo("metallicRoughnessTexture")

    def __getTextureInfo(self, key):
        return TextureInfo(self.file, self.jsonDict[key]) if key in self.jsonDict else None
