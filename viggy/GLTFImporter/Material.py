from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

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

        if "pbrMetallicRoughness" in self.jsonDict:
            self.pbrInfo: Optional[PBRInfo] = PBRInfo(self.file, self.jsonDict["pbrMetallicRoughness"])
        else:
            self.pbrInfo: Optional[PBRInfo] = None

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
            self.normalTextureInfo: Optional[NormalTextureInfo] = \
                NormalTextureInfo(self.file, self.jsonDict["normalTexture"])
        else:
            self.normalTextureInfo: Optional[NormalTextureInfo] = None

        # occlusion texture map
        # Consider only R value for each texel, indicates how much indirect light (ambient light) should be received
        if "occlusionTexture" in self.jsonDict:
            self.occlusionTextureInfo: Optional[OcclusionTextureInfo] = \
                OcclusionTextureInfo(self.file, self.jsonDict["occlusionTexture"])
        else:
            self.occlusionTextureInfo: Optional[OcclusionTextureInfo] = None

        # emmisive texture map
        if "emissiveTexture" in self.jsonDict:
            self.emissiveTexture: Optional[TextureInfo] = TextureInfo(self.file, self.jsonDict["emissiveTexture"])
        else:
            self.emissiveTexture: Optional[TextureInfo] = None

        # multiply each value with R,G,B from emmisiveTexture Texel
        self.emissiveFactor: List[float, float, float] = self.getFromJSONDict("emissiveFactor", [0, 0, 0])


class PBRInfo:
    def __init__(self, file, pbrDict: dict):
        self.file = file
        self.jsonDict = pbrDict

        # each component is in [0,1]
        self.baseColorFactor: List[float, float, float, float] = getFromJSONDict(self.jsonDict, "baseColorFactor",
                                                                                 [1, 1, 1, 1])
        self.metallicFactor: float = getFromJSONDict(self.jsonDict, "metallicFactor", 1)
        self.roughnessFactor: float = getFromJSONDict(self.jsonDict, "roughnessFactor", 1)

        if "baseColorTexture" in self.jsonDict:
            self.baseColorTextureInfo: Optional[TextureInfo] = TextureInfo(self.file, self.jsonDict["baseColorTexture"])
        else:
            self.baseColorTextureInfo: Optional[TextureInfo] = None

        # for every texel, G corresponds to roughness and B to metalness
        if "metallicRoughnessTexture" in self.jsonDict:
            self.metallicRoughnessTextureInfo: Optional[TextureInfo] = \
                TextureInfo(self.file, self.jsonDict["metallicRoughnessTexture"])
        else:
            self.metallicRoughnessTextureInfo: Optional[TextureInfo] = None
