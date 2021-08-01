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

        self.sampler = self.createFromKey(Sampler, "samplers", "sampler")

        self.image = self.createFromKey(Image, "images", "source")
