from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Graph import Graph

import glm


class PointLight:
    def __init__(self, graph: Graph, pos: glm.vec3,
                 ambient: glm.vec3, diffuse: glm.vec3, specular: glm.vec3,
                 k: glm.vec3):
        self.graph = graph
        self.graph.addLights(self)
        self.position = pos
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.k = k
