import math
import sys

import glm
from PySide6.QtWidgets import QApplication

from Graph import Graph
from viggy.Camera import Camera
from viggy.Light import Light

app = QApplication(sys.argv)
graph = Graph()

camera = Camera(pos=glm.vec3(0, 2, 2),
                fov=math.radians(45),
                z_min=0.1, z_max=100.0)
camera.setTarget(glm.vec3(0, 0, 0))

light = Light(pos=glm.vec3(0.0, 1.3, 0),
              ambient=glm.vec3(1, 1, 1),
              diffuse=glm.vec3(1, 1, 1),
              specular=glm.vec3(1, 1, 1),
              k=glm.vec3(2, 0.2, 0.01))

graph.addCameras(camera)
graph.addLights(light)

graph.show()
sys.exit(app.exec())
