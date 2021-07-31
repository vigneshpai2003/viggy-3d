from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .Node import Node
    from .Mesh import Mesh
    from .Material import Material
    from .Texture import Texture
    from .Sampler import Sampler
    from .Image import Image
    from .Accessor import Accessor
    from .BufferView import BufferView
    from .Buffer import Buffer

import json
import pathlib

from .Scene import Scene


class GLTFFile:
    def __init__(self, path, binary=False):
        """
        only two types of files are allowed, a stand alone binary .glb or a JSON .gltf file
        """
        self.isBinary: bool = binary

        self.path: pathlib.Path = pathlib.Path(path)

        if binary:
            with open(path, 'rb') as f:
                # header
                assert str(f.read(4), 'utf-8') == "glTF"  # magic
                assert int.from_bytes(f.read(4), 'little') == 2  # version
                int.from_bytes(f.read(4), 'little')  # length of entire file

                # json chunk
                chunk0Length = int.from_bytes(f.read(4), 'little')  # length of jsonData
                assert str(f.read(4), 'utf-8') == "JSON"  # first chunk must be json
                self.jsonData: dict = json.loads(str(f.read(chunk0Length), 'utf-8'))

                # binary chunk
                chunk1Length = int.from_bytes(f.read(4), 'little')  # length of binaryData
                tpe = str(f.read(4), "utf-8")  # = "BIN" + "" for some reason
                assert tpe[:3] == "BIN"  # second chunk must be binary
                self.binaryData: bytes = f.read(chunk1Length)

        else:
            with open(path, 'r') as f:
                self.jsonData: dict = json.load(f)

        self.scenes: List[Scene] = self.__makeArray("scenes")
        self.nodes: List[Node] = self.__makeArray("nodes")
        self.meshes: List[Mesh] = self.__makeArray("meshes")
        self.materials: List[Material] = self.__makeArray("materials")
        self.textures: List[Texture] = self.__makeArray("textures")
        self.samplers: List[Sampler] = self.__makeArray("samplers")
        self.images: List[Image] = self.__makeArray("images")
        self.accessors: List[Accessor] = self.__makeArray("accessors")
        self.bufferViews: List[BufferView] = self.__makeArray("bufferViews")
        self.buffers: List[Buffer] = self.__makeArray("buffers")

        for i in range(len(self.jsonData["scenes"])):
            Scene(self, i)

    def __makeArray(self, key: str) -> Optional[list]:
        if key in self.jsonData:
            return [None] * len(self.jsonData[key])
        else:
            return None
