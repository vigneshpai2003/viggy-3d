import math
import sys

import glm
from PySide6.QtWidgets import QApplication

from viggy.Graph import Graph
from viggy.Camera import Camera
from viggy.PointLight import PointLight
from viggy.Model import Model
from viggy.SkyBox import SkyBox

import viggy.GLTFImporter as gltf


class MyGraph(Graph):
    def initializeGL(self):
        super().initializeGL()

        self.skyBox = SkyBox("extra/skyboxes/ocean", "jpg")

        camera = Camera(self, pos=glm.vec3(0, 0, 1.5),
                        fov=math.radians(45),
                        z_min=0.1, z_max=100.0)
        camera.setTarget(glm.vec3(0, 0, 0))

        PointLight(self, pos=glm.vec3(0, 0, 2),
                   ambient=glm.vec3(.4, .4, .4),
                   diffuse=glm.vec3(1, 1, 1),
                   specular=glm.vec3(1, 1, 1),
                   k=glm.vec3(1, 0.2, 0.01))

        car = Model(self, gltf.GLTFFile("extra/models/car.glb", True))
        shark = Model(self, gltf.GLTFFile("extra/models/shark.glb", True))
        troll = Model(self, gltf.GLTFFile("extra/models/troll.glb", True))
        shark.setTransform(glm.translate(glm.mat4(), (.6, 0, 0)))
        troll.setTransform(glm.translate(glm.mat4(), (-.6, 0, 0)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph = MyGraph()

    graph.show()
    sys.exit(app.exec())
