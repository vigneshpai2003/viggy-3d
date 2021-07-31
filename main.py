import sys
import math
import time

import glm
import numpy as np
from OpenGL import GL
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QMouseEvent, QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from viggy.Camera import Camera
from viggy.Light import Light
from viggy.importer import Renderer, loadObject
from viggy.Shader import Shader
from viggy.SkyBox import SkyBox
from viggy.vertexData import cubeVertices, cubeIndices


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.resize(600, 600)
        self.setWindowTitle('OpenGL Renderer')

        self.GL_widget = GLWidget()
        self.initializeUI()

        self.key_sensitivity = 0.1

        # main loop that calls draw multiple times
        timer = QTimer(self)
        timer.setInterval(1)  # time between frames in ms
        timer.timeout.connect(self.GL_widget.update)
        timer.start()

    def keyPressEvent(self, event):
        camera = self.GL_widget.renderer.activeCamera

        if event.key() == Qt.Key_Right:
            camera.moveX(self.key_sensitivity)
        if event.key() == Qt.Key_Left:
            camera.moveX(-self.key_sensitivity)
        if event.key() == Qt.Key_Up:
            camera.moveZ(self.key_sensitivity)
        if event.key() == Qt.Key_Down:
            camera.moveZ(-self.key_sensitivity)
        if event.key() == Qt.Key_A:
            camera.setUpAxis(glm.rotate(camera.yAxis, self.GL_widget.mouse_sensitivity, camera.zAxis))
        if event.key() == Qt.Key_D:
            camera.setUpAxis(glm.rotate(camera.yAxis, -self.GL_widget.mouse_sensitivity, camera.zAxis))
        if event.key() == Qt.Key_W:
            camera.fov -= math.radians(1)
        if event.key() == Qt.Key_S:
            camera.fov += math.radians(1)

        camera.setFront(-camera.zAxis)
        event.accept()

    def initializeUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        layout.addWidget(self.GL_widget)

        central_widget.setLayout(layout)


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        """
        creates the renderer here along with non OpenGL objects like cameras and lights
        """
        super(GLWidget, self).__init__(parent=parent)

        # enable multisampling
        sampleFormat = QSurfaceFormat()
        sampleFormat.setSamples(4)
        self.setFormat(sampleFormat)

        # mouse controls
        self.last_x = None
        self.last_y = None
        self.mouse_sensitivity = .005

        self.renderer = Renderer()

        # add cameras
        self.renderer.addCameras(Camera(pos=glm.vec3(0, 2, 2),
                                        fov=math.radians(45),
                                        z_min=0.1, z_max=100.0))

        self.renderer.activeCamera.setTarget(glm.vec3(0, 0, 0))

        # add lights
        self.renderer.addLights(Light(pos=glm.vec3(0.0, 1.3, 0),
                                      ambient=glm.vec3(1, 1, 1),
                                      diffuse=glm.vec3(1, 1, 1),
                                      specular=glm.vec3(1, 1, 1),
                                      k=glm.vec3(2, 0.2, 0.01)))

        print("Initialized widget")

    def mousePressEvent(self, event: QMouseEvent):
        self.last_x = event.x()
        self.last_y = event.y()

    def mouseMoveEvent(self, event: QMouseEvent):
        x_offset = event.x() - self.last_x
        y_offset = event.y() - self.last_y

        self.last_x = event.x()
        self.last_y = event.y()

        camera = self.renderer.activeCamera
        camera.setFront(glm.rotate(-camera.zAxis, -x_offset * self.mouse_sensitivity, camera.yAxis))
        camera.setFront(glm.rotate(-camera.zAxis, -y_offset * self.mouse_sensitivity, camera.xAxis))

        event.accept()

    def initializeGL(self):
        """
        initialize OpenGL and create meshes and shaders
        """
        try:
            self.renderer.enableTools()

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
            sky_box = SkyBox("viggy/shaders/sky_box", "viggy/skyboxes/ocean", "jpg")
            self.renderer.addSkybox(sky_box)

            # initialize meshes
            self.renderer.createMeshes(5)
            light_mesh, box, test_obj, test_obj_mesh, test_obj_normals = self.renderer.meshes

            light_mesh.addVBO(cubeVertices, (0, 1, 2), (3, 2, 3))
            light_mesh.addIBO(cubeIndices)

            box.addVBO(cubeVertices, (0, 1, 2), (3, 2, 3))
            box.addIVBO(box_instances, (3,), (3,), (1,))
            box.addIBO(cubeIndices)
            box.addTexture("textures/woodbox.png")

            test_obj.addVBO(loadObject("viggy/meshes/chibi.obj"), (0, 1, 2), (3, 2, 3))
            test_obj.addIVBO(test_obj_instances, (3,), (3,), (1,))
            test_obj.addTexture("textures/chibi.png")

            test_obj_mesh.addVBO(loadObject("viggy/meshes/chibi.obj", UV=False, normals=False), (0,), (3,))
            test_obj_normals.addVBO(loadObject("viggy/meshes/chibi.obj", UV=False, normals=True), (0, 1), (3, 3))

            # initialize shaders
            self.renderer.addShaders(Shader("viggy/shaders/light", geometry=True),
                                     Shader("viggy/shaders/object", geometry=True),
                                     Shader("viggy/shaders/mesh", geometry=True),
                                     Shader("viggy/shaders/normal", geometry=True))
            shader_light, shader_object, shader_mesh, shader_normal = self.renderer.shaders

            shader_light.addUniforms(("model", "Matrix4fv"),
                                     ("view", "Matrix4fv"),
                                     ("projection", "Matrix4fv"),
                                     ("light_color", "3f"))
            shader_light.setUniform("light_color", (1, 1, 1))

            shader_object.addUniforms(("model", "Matrix4fv"),
                                      ("view", "Matrix4fv"),
                                      ("projection", "Matrix4fv"),
                                      ("camera_pos", "3f"),
                                      ("light", (("position", "3f"),
                                                 ("ambient", "3f"),
                                                 ("diffuse", "3f"),
                                                 ("specular", "3f"),
                                                 ("k", "3f"))),
                                      ("material", (("ambient_strength", "1f"),
                                                    ("diffuse_strength", "1f"),
                                                    ("specular_strength", "1f"),
                                                    ("shininess", "1f"))))
            shader_object.setUniform("material", (1.0, 1.0, 1.0, 16.0))
            shader_object.setUniform("light", (self.renderer.lights[0].position,
                                               self.renderer.lights[0].ambient,
                                               self.renderer.lights[0].diffuse,
                                               self.renderer.lights[0].specular,
                                               self.renderer.lights[0].k))

            shader_mesh.addUniforms(("model", "Matrix4fv"),
                                    ("view", "Matrix4fv"),
                                    ("projection", "Matrix4fv"),
                                    ("color", "3f"))
            shader_mesh.setUniform("color", (1.0, 1.0, 1.0))

            shader_normal.addUniforms(("model", "Matrix4fv"),
                                      ("view", "Matrix4fv"),
                                      ("projection", "Matrix4fv"),
                                      ("color", "3f"),
                                      ("size", "1f"))
            shader_normal.setUniform("color", (1.0, 0.0, 1.0))
            shader_normal.setUniform("size", 0.5)  # size is wrt to object without any scaling

            print("Initialized OpenGL")

        except Exception as e:
            print(e)
            exit()

    def paintGL(self):
        self.renderer.clearBuffers()

        # camera and light
        camera = self.renderer.activeCamera

        self.renderer.lights[0].position.x = math.sin(time.perf_counter())

        view = self.renderer.view
        projection = self.renderer.projection

        # meshes and shaders
        light_mesh, box, test_obj, test_obj_mesh, test_obj_normal = self.renderer.meshes
        shader_light, shader_object, shader_mesh, shader_normal = self.renderer.shaders

        # set the view and projection matrices for all shaders
        shader_light.setUniform("view", glm.value_ptr(view))
        shader_light.setUniform("projection", glm.value_ptr(projection))

        shader_object.setUniform("view", glm.value_ptr(view))
        shader_object.setUniform("projection", glm.value_ptr(projection))

        shader_mesh.setUniform("view", glm.value_ptr(view))
        shader_mesh.setUniform("projection", glm.value_ptr(projection))

        shader_normal.setUniform("view", glm.value_ptr(view))
        shader_normal.setUniform("projection", glm.value_ptr(projection))

        # set lights and camera uniforms
        shader_object.setUniform("camera_pos", camera.position)
        shader_object.setUniform("light.position", self.renderer.lights[0].position)

        # draw skybox first
        self.renderer.drawSkyBox(view, projection)

        # draw light
        model = glm.translate(glm.mat4(1.0), self.renderer.lights[0].position) * \
                glm.scale(glm.mat4(1.0), glm.vec3(0.1, 0.1, 0.1))
        shader_light.setUniform("model", glm.value_ptr(model))
        self.renderer.draw(light_mesh, shader_light, 0)

        # draw box
        model = glm.translate(glm.mat4(1.0), glm.vec3(0, -0.5, 0))
        shader_object.setUniform("model", glm.value_ptr(model))
        self.renderer.draw(box, shader_object, 0)

        # draw test object
        model = glm.rotate(glm.mat4(1.0), 0.3 * time.perf_counter(), glm.vec3(0.0, 1.0, 0.0)) * \
                glm.scale(glm.mat4(1.0), glm.vec3(.1, .1, .1))
        shader_object.setUniform("model", glm.value_ptr(model))
        self.renderer.draw(test_obj, shader_object, 0)

        # draw test object mesh
        shader_mesh.setUniform("model", glm.value_ptr(model))  # same model as test object
        self.renderer.draw(test_obj_mesh, shader_mesh, 0)

        # draw test object normals
        shader_normal.setUniform("model", glm.value_ptr(model))  # same model as test object
        self.renderer.draw(test_obj_normal, shader_normal, 0)

    def resizeGL(self, width, height):
        GL.glViewport(0, 0, width, height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
