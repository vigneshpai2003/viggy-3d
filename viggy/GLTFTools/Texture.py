from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile

from .GLTFObject import GLTFObject
from .Sampler import Sampler
from .Image import Image


class Texture(GLTFObject):
    def __init__(self, file: GLTFFile, index: int):
        super().__init__(file, "textures", index)

        if "sampler" in self.jsonDict:
            self.sampler: Sampler = self.createGLTFObject(Sampler, "samplers", self.jsonDict["sampler"])
        else:
            self.sampler = None

        if "source" in self.jsonDict:
            self.image: Image = self.createGLTFObject(Image, "images", self.jsonDict["source"])
        else:
            self.image = None
