from __future__ import annotations
import math
import time
from typing import List

import glm
import numpy as np
from OpenGL import GL
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QMouseEvent, QSurfaceFormat, QKeyEvent
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from viggy.Camera import Camera
from viggy.Light import Light
from viggy.Mesh import Mesh
from viggy.Model import Model
from viggy.Texture import Texture
from viggy.importer import loadObject
from viggy.Shader import Shader
from viggy.SkyBox import SkyBox
from viggy.colors import fromRGB
from viggy.vertexData import cubeVertices, cubeIndices


class Graph(QOpenGLWidget):
    def __init__(self, parent=None):
        """
        creates the renderer here along with non OpenGL objects like cameras and lights
        """
        super().__init__(parent=parent)

        # Camera controls
        self.keySensitivity = 0.1
        self.mouseSensitivity = 0.005
        self.lastX = None
        self.lastY = None

        # containers
        self.cameras: List[Camera] = []
        self.lights: List[Light] = []
        self.meshes: List[Mesh] = []
        self.shaders: List[Shader] = []
        self.textures: List[Texture] = []
        self.skyBox = None
        self.activeCameraIndex = 0  # change to change to the active camera

        # main loop that calls paintGL multiple times
        timer = QTimer(self)
        timer.setInterval(1)  # time between frames in ms
        timer.timeout.connect(self.update)
        timer.start()

        self.setSamples(4)

    @property
    def activeCamera(self) -> Camera:
        return self.cameras[self.activeCameraIndex]

    def addCameras(self, *cameras: Camera):
        self.cameras.extend(cameras)

    def addLights(self, *lights: Light):
        self.lights.extend(lights)

    def createMeshes(self, n: int):
        self.meshes.extend([Mesh() for _ in range(n)])

    def addMeshes(self, *meshes: Mesh):
        self.meshes.extend(meshes)

    def addShaders(self, *shaders: Shader):
        self.shaders.extend(shaders)

    def addTextures(self, *textures: Texture):
        self.textures.extend(textures)

    @property
    def view(self) -> glm.mat4:
        return self.activeCamera.view

    @property
    def projection(self) -> glm.mat4:
        viewport_data = GL.glGetIntegerv(GL.GL_VIEWPORT)
        return self.activeCamera.projection((viewport_data[2] - viewport_data[0])  # width
                                            / (viewport_data[3] - viewport_data[1]))  # height

    @staticmethod
    def setBG(rgb: str):
        GL.glClearColor(*fromRGB(rgb), 1.0)

    def keyPressEvent(self, event: QKeyEvent):
        camera = self.activeCamera

        if event.key() == Qt.Key_Right:
            camera.moveX(self.keySensitivity)
        if event.key() == Qt.Key_Left:
            camera.moveX(-self.keySensitivity)
        if event.key() == Qt.Key_Up:
            camera.moveZ(self.keySensitivity)
        if event.key() == Qt.Key_Down:
            camera.moveZ(-self.keySensitivity)
        if event.key() == Qt.Key_A:
            camera.setUpAxis(glm.rotate(camera.yAxis, self.mouseSensitivity, camera.zAxis))
        if event.key() == Qt.Key_D:
            camera.setUpAxis(glm.rotate(camera.yAxis, -self.mouseSensitivity, camera.zAxis))
        if event.key() == Qt.Key_W:
            camera.fov -= math.radians(1)
            if camera.fov <= math.radians(0):
                camera.fov = math.radians(1)
        if event.key() == Qt.Key_S:
            camera.fov += math.radians(1)
            if camera.fov >= math.radians(90):
                camera.fov = math.radians(89)

        camera.setFront(-camera.zAxis)

        event.accept()

    def mousePressEvent(self, event: QMouseEvent):
        self.lastX = event.x()
        self.lastY = event.y()

    def mouseMoveEvent(self, event: QMouseEvent):
        xOffset = event.x() - self.lastX
        yOffset = event.y() - self.lastY

        self.lastX = event.x()
        self.lastY = event.y()

        camera = self.activeCamera
        camera.setFront(glm.rotate(-camera.zAxis, -xOffset * self.mouseSensitivity, camera.yAxis))
        camera.setFront(glm.rotate(-camera.zAxis, -yOffset * self.mouseSensitivity, camera.xAxis))

        event.accept()

    def setSamples(self, n: int):
        """
        must call GL.glEnable(GL.GL_MULTISAMPLE) in initializeGL
        :param n: number of samples for multisampling
        """
        sampleFormat = QSurfaceFormat()
        sampleFormat.setSamples(n)
        self.setFormat(sampleFormat)

    def setVP(self):
        """
        set view and projection matrix for all shaders
        """
        # create local variables in order to pass pointers
        # if local variables are not used then glm.value_ptr will point to deallocated memory
        view = self.view
        projection = self.projection

        for shader in self.shaders:
            shader.setUniform("view", glm.value_ptr(view))
            shader.setUniform("projection", glm.value_ptr(projection))

    def resizeGL(self, width, height):
        GL.glViewport(0, 0, width, height)

    def initializeGL(self):
        """
        initialize OpenGL and create meshes and shaders
        """
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        # box instance arrays
        box_instances = []
        for i in range(-30, 31):
            for j in range(-30, 31):
                box_instances.extend([i, 0, j])

        box_instances = np.array(box_instances, dtype=np.float32)

        # test_obj instance arrays
        test_obj_instances = []
        for i in range(-3, 4):
            for j in range(-3, 4):
                test_obj_instances.extend([i, 0, j])

        test_obj_instances = 3 * np.array(test_obj_instances, dtype=np.float32)

        # skybox
        self.skyBox = SkyBox("viggy/skyboxes/ocean", "jpg")

        self.car = Model("backpack/backpack.obj")

        # initialize meshes
        self.createMeshes(5)
        light_mesh, box, test_obj, test_obj_mesh, test_obj_normals = self.meshes

        light_mesh.addVBO(cubeVertices, (0, 1, 2), (3, 2, 3))
        light_mesh.addIBO(cubeIndices)

        box.addVBO(cubeVertices, (0, 1, 2), (3, 2, 3))
        box.addIVBO(box_instances, (3,), (3,), (1,))
        box.addIBO(cubeIndices)

        test_obj.addVBO(loadObject("viggy/meshes/chibi.obj"), (0, 1, 2), (3, 2, 3))
        test_obj.addIVBO(test_obj_instances, (3,), (3,), (1,))

        test_obj_mesh.addVBO(loadObject("viggy/meshes/chibi.obj", UV=False, normals=False), (0,), (3,))
        test_obj_normals.addVBO(loadObject("viggy/meshes/chibi.obj", UV=False, normals=True), (0, 1), (3, 3))

        # initialize shaders
        self.addShaders(Shader("viggy/shaders/light"),
                        Shader("viggy/shaders/object"),
                        Shader("viggy/shaders/mesh"),
                        Shader("viggy/shaders/normal"),
                        Shader("viggy/shaders/sky_box"))

        shader_light, shader_object, shader_mesh, shader_normal, shader_sky_box = self.shaders

        shader_light.setUniform("light_color", (1, 1, 1))

        shader_object.setUniform("material", (1.0, 1.0, 1.0, 16.0))
        shader_object.setUniform("light", (self.lights[0].position,
                                           self.lights[0].ambient,
                                           self.lights[0].diffuse,
                                           self.lights[0].specular,
                                           self.lights[0].k))

        shader_mesh.setUniform("color", (1.0, 1.0, 1.0))

        shader_normal.setUniform("color", (1.0, 0.0, 1.0))
        shader_normal.setUniform("size", 0.5)  # size is wrt to object without any scaling

        # initialize textures
        box_texture = Texture("viggy/textures/woodbox.png")
        test_obj_texture = Texture("viggy/textures/chibi.png")
        self.addTextures(box_texture, test_obj_texture)

    def paintGL(self):
        # clear buffers
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # meshes and shaders and textures
        light_mesh, box, test_obj, test_obj_mesh, test_obj_normal = self.meshes
        shader_light, shader_object, shader_mesh, shader_normal, shader_sky_box = self.shaders
        box_texture, test_obj_texture = self.textures

        # set the view and projection matrices for all shaders
        self.setVP()

        # light position
        self.lights[0].position.x = math.sin(time.perf_counter())

        # set lights and camera uniforms
        shader_object.setUniform("camera_pos", self.activeCamera.position)
        shader_object.setUniform("light.position", self.lights[0].position)

        # draw skybox first
        shader_sky_box.use()
        self.skyBox.draw()

        # draw light
        model = glm.translate(glm.mat4(1.0), self.lights[0].position) * \
                glm.scale(glm.mat4(1.0), glm.vec3(0.1, 0.1, 0.1))
        shader_light.setUniform("model", glm.value_ptr(model))
        light_mesh.draw()

        # draw box
        box_texture.bind(0)
        model = glm.translate(glm.mat4(1.0), glm.vec3(0, -0.5, 0))
        shader_object.setUniform("model", glm.value_ptr(model))
        shader_object.setUniform("texture", 0)
        box.draw()

        # model for test object, mesh and normal
        model = glm.rotate(glm.mat4(1.0), 0.3 * time.perf_counter(), glm.vec3(0.0, 1.0, 0.0)) * \
                glm.scale(glm.mat4(1.0), glm.vec3(.1, .1, .1))

        # draw test object
        test_obj_texture.bind(0)
        shader_object.setUniform("model", glm.value_ptr(model))
        shader_object.setUniform("texture", 0)
        test_obj.draw()

        # draw test object mesh
        shader_mesh.setUniform("model", glm.value_ptr(model))
        test_obj_mesh.draw()

        # draw test object normals
        shader_normal.setUniform("model", glm.value_ptr(model))
        test_obj_normal.draw()

        model = glm.translate(glm.mat4(), glm.vec3(0, 3, 0))  # * glm.scale(glm.mat4(), glm.vec3(0.1, 0.1, 0.1))
        shader_object.setUniform("model", glm.value_ptr(model))
        self.car.draw()
