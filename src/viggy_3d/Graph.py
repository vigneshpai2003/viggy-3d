from __future__ import annotations

import math
import os
from typing import List

import glm
from OpenGL import GL
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QMouseEvent, QSurfaceFormat, QKeyEvent
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from .Camera import Camera
from .Model import Model
from .PointLight import PointLight
from .Shader import Shader
from .colors import fromRGB


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

        self.bgColor = "000000"

        # containers
        self.cameras: List[Camera] = []
        self.lights: List[PointLight] = []
        self.models: List[Model] = []
        self.shaders: List[Shader] = []
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

    def addLights(self, *lights: PointLight):
        self.lights.extend(lights)

    def addModels(self, *models: Model):
        self.models.extend(models)

    def addShaders(self, *shaders: Shader):
        self.shaders.extend(shaders)

    @property
    def view(self) -> glm.mat4:
        return self.activeCamera.view

    @property
    def projection(self) -> glm.mat4:
        viewport_data = GL.glGetIntegerv(GL.GL_VIEWPORT)
        return self.activeCamera.projection((viewport_data[2] - viewport_data[0])  # width
                                            / (viewport_data[3] - viewport_data[1]))  # height

    @staticmethod
    def __setBG(rgb: str):
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

        # shader for all models
        self.modelShader = Shader(os.path.join(os.path.dirname(__file__), "shaders/model"))
        self.skyBoxShader = Shader(os.path.join(os.path.dirname(__file__), "shaders/sky_box"))
        self.addShaders(self.modelShader, self.skyBoxShader)

        self.modelShader.setUniform("material", ((1.0, 1.0, 1.0),
                                                 (1.0, 1.0, 1.0),
                                                 (1.0, 1.0, 1.0),
                                                 32.0))

        self.modelShader.setUniform("baseTexture", 0)

    def paintGL(self):
        # clear buffers
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.__setBG(self.bgColor)

        # set the view and projection matrices for all shaders
        self.setVP()

        # set lights and camera uniforms
        self.modelShader.setUniform("cameraPos", self.activeCamera.position)
        self.modelShader.setUniform("light", (self.lights[0].position,
                                              self.lights[0].ambient,
                                              self.lights[0].diffuse,
                                              self.lights[0].specular,
                                              self.lights[0].k))

        # sky box should be first thing drawn
        if self.skyBox:
            self.skyBoxShader.use()
            self.skyBox.draw()

        for model in self.models:
            model.draw(self.modelShader)
