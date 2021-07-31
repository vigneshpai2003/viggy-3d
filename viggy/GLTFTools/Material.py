from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

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

        # pbr details
        if "pbrMetallicRoughness" in self.jsonDict:
            self.pbrInfo = PBRInfo(file, self.jsonDict["pbrMetallicRoughness"])
        else:
            self.pbrInfo = None

        # normal texture map
        """
        Each texel represents the XYZ components of a normal vector in tangent space. 
        R [0, 255] -> X [-1, 1]
        G [0, 255] -> Y [-1, 1]
        B [128, 255] -> Z [1/255, 1]
        in GLSL, texture() maps RGB to [0, 1]
        vec3 normalVector = normalize(texture(<normalMap>, texCoord) * 2 - 1)
        """
        if "normalTexture" in self.jsonDict:
            self.normalTextureInfo = NormalTextureInfo(file, self.jsonDict["normalTexture"])
        else:
            self.normalTextureInfo = None

        # occlusion texture map
        # Consider only R value for each texel, indicates how much indirect light (ambient light) should be received
        if "occlusionTexture" in self.jsonDict:
            self.occlusionTextureInfo = OcclusionTextureInfo(file, self.jsonDict["occlusionTexture"])
        else:
            self.occlusionTextureInfo = None

        # emmisive texture map
        if "emissiveTexture" in self.jsonDict:
            self.emissiveTextureInfo = TextureInfo(file, self.jsonDict["emissiveTexture"])
        else:
            self.emissiveTextureInfo = None

        # multiply each value with R,G,B from emmisiveTexture Texel
        self.emissiveFactor: Optional[List[float, float, float]] = self.getFromJSONDict("emissiveFactor", [0, 0, 0])


class PBRInfo:
    def __init__(self, file, pbrDict: dict):
        self.jsonDict = pbrDict

        # each component is in [0,1]
        self.baseColorFactor: List[float, float, float, float] = getFromJSONDict(self.jsonDict, "baseColorFactor",
                                                                                 [1, 1, 1, 1])
        self.metallicFactor: float = getFromJSONDict(self.jsonDict, "metallicFactor", 1)
        self.roughnessFactor: float = getFromJSONDict(self.jsonDict, "roughnessFactor", 1)

        if "baseColorTexture" in self.jsonDict:
            self.baseColorTextureInfo = TextureInfo(file, self.jsonDict["baseColorTexture"])
        else:
            self.baseColorTextureInfo = None

        # for every texel, G corresponds to roughness and B to metalness
        if "metallicRoughnessTexture" in self.jsonDict:
            self.metallicRoughnessTextureInfo = TextureInfo(file, self.jsonDict["metallicRoughnessTexture"])
        else:
            self.metallicRoughnessTextureInfo = None
