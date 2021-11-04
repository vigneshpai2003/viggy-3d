from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .Texture import Texture

import src.viggy_3d.GLTFImporter as gltf


class Material:
    def __init__(self, material: gltf.Material, textures: List[Texture]):
        """
        material has emissive, occlusion, normal, base and metallic-roughness textures
        """
        self.fileData = material

        if material.emissiveTextureInfo is not None:
            self.emissiveTexture: Optional[Texture] = textures[material.emissiveTextureInfo.texture.index]
        else:
            self.emissiveTexture: Optional[Texture] = None

        if material.occlusionTextureInfo is not None:
            self.occlusionTexture: Optional[Texture] = textures[material.occlusionTextureInfo.texture.index]
        else:
            self.occlusionTexture: Optional[Texture] = None

        if material.normalTextureInfo is not None:
            self.normalTexture: Optional[Texture] = textures[material.normalTextureInfo.texture.index]
        else:
            self.normalTexture: Optional[Texture] = None

        if material.pbrInfo is not None:
            if material.pbrInfo.baseColorTextureInfo is not None:
                self.baseTexture: Optional[Texture] = textures[material.pbrInfo.baseColorTextureInfo.texture.index]
            else:
                self.baseTexture: Optional[Texture] = None

            if material.pbrInfo.metallicRoughnessTextureInfo is not None:
                self.metallicRoughnessTexture: Optional[Texture] = \
                    textures[material.pbrInfo.metallicRoughnessTextureInfo.texture.index]
            else:
                self.metallicRoughnessTexture: Optional[Texture] = None
        else:
            self.baseTexture: Optional[Texture] = None
            self.metallicRoughnessTexture: Optional[Texture] = None
