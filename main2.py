import sys
from typing import Callable
import math

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtOpenGL import QGLWidget, QGLFormat

from viggy.importer import *


def get_func_vertex_data(func: Callable[[float, float], float],
                         x_range: Tuple[float, float], y_range: Tuple[float, float],
                         x_step: float, y_step: float) -> np.ndarray:
    vertices = []

    def get_vector(_x: float, _y: float) -> glm.vec3:
        return glm.vec3(_x, _y, func(_x, _y))

    def get_UV(_x: float, _y: float) -> Tuple[float, float]:
        return (_x - x_range[0]) / (x_range[1] - x_range[0]), (_y - y_range[0]) / (y_range[1] - y_range[0])

    def get_normal(v1: glm.vec3, v2: glm.vec3) -> glm.vec3:
        return glm.normalize(glm.cross(v1, v2))

    for x in np.arange(x_range[0], x_range[1] - x_step, x_step):
        for y in np.arange(y_range[0], y_range[1] - y_step, y_step):
            P1 = get_vector(x, y)
            P2 = get_vector(x + x_step, y)
            P3 = get_vector(x, y + y_step)
            P4 = get_vector(x + x_step, y + y_step)

            UV1 = get_UV(x, y)
            UV2 = get_UV(x + x_step, y)
            UV3 = get_UV(x, y + y_step)
            UV4 = get_UV(x + x_step, y + y_step)

            n1 = get_normal(P2 - P1, P3 - P1)
            n2 = get_normal(P3 - P4, P2 - P4)

            vertices.extend((*P1, *UV1, *n1))
            vertices.extend((*P2, *UV2, *n1))
            vertices.extend((*P3, *UV3, *n1))

            vertices.extend((*P4, *UV4, *n2))
            vertices.extend((*P3, *UV3, *n2))
            vertices.extend((*P2, *UV2, *n2))

    vertices = np.array(vertices, dtype=np.float32)

    return vertices


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.resize(600, 600)
        self.setWindowTitle('OpenGL Renderer')

        self.GL_widget = GLWidget()
        self.initialize_ui()

        self.key_sensitivity = 0.1

        # main loop that calls draw multiple times
        timer = QTimer(self)
        timer.setInterval(1)  # time between frames in ms
        timer.timeout.connect(self.GL_widget.updateGL)
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
        camera.setTarget(glm.vec3(0, 0, 0))
        event.accept()

    def initialize_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        layout.addWidget(self.GL_widget)

        central_widget.setLayout(layout)


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        """
        creates the renderer here along with non OpenGL objects like cameras and lights
        """
        # enable multisampling
        sample_format = QGLFormat()
        sample_format.setSampleBuffers(True)
        sample_format.setSamples(4)
        super(GLWidget, self).__init__(sample_format, parent=parent)

        # mouse controls
        self.last_x = None
        self.last_y = None
        self.mouse_sensitivity = .005

        self.renderer = Renderer()

        # add cameras
        self.renderer.addCameras(Camera(pos=glm.vec3(0, -5, 10),
                                        fov=math.radians(45),
                                        z_min=0.1, z_max=100.0))

        self.renderer.activeCamera.setTarget(glm.vec3(0, 0, 0))

        # add lights
        self.renderer.addLights(Light(pos=glm.vec3(0.0, 0.0, 5),
                                      ambient=glm.vec3(1, 1, 1),
                                      diffuse=glm.vec3(1, 1, 1),
                                      specular=glm.vec3(1, 1, 1),
                                      k=glm.vec3(1, 0.2, 0.01)))

        self.x_range = (-5, 5)
        self.y_range = (-5, 5)

        print("Initialized widget")

    @staticmethod
    def graph_f(x, y):
        return abs(math.sin(x**2 + 2 * y)) ** 0.5

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

            # initialize meshes
            self.renderer.createMeshes(5)
            graph, light, x_axis, y_axis, z_axis = self.renderer.meshes

            graph.addVBO(get_func_vertex_data(self.graph_f, self.x_range, self.y_range, 0.05, 0.05),
                         (0, 1, 2), (3, 2, 3))
            graph.addTexture("textures/gold.png")

            light.addVBO(cubeVertices, (0, 1, 2), (3, 2, 3))
            light.addIBO(cubeIndices)

            x_axis.addVBO(cubeVertices, (0, 1, 2), (3, 2, 3))
            x_axis.addIBO(cubeIndices)
            x_axis.addTexture("textures/army.jpg")

            y_axis.addVBO(cubeVertices, (0, 1, 2), (3, 2, 3))
            y_axis.addIBO(cubeIndices)
            y_axis.addTexture("textures/lava.jpg")

            z_axis.addVBO(cubeVertices, (0, 1, 2), (3, 2, 3))
            z_axis.addIBO(cubeIndices)
            z_axis.addTexture("textures/paint.png")

            # initialize shaders
            self.renderer.addShaders(Shader("shaders/light", geometry=True),
                                     Shader("shaders/object", geometry=True))
            shader_light, shader_object = self.renderer.shaders

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

            print("Initialized OpenGL")

        except Exception as e:
            print(e)
            exit()

    def paintGL(self):
        self.renderer.clearBuffers()

        # camera and light
        camera = self.renderer.activeCamera

        view = self.renderer.view
        projection = self.renderer.projection

        # meshes and shaders
        graph, light, x_axis, y_axis, z_axis = self.renderer.meshes
        shader_light, shader_object = self.renderer.shaders

        # set the view and projection matrices for all shaders
        shader_light.setUniform("view", glm.value_ptr(view))
        shader_light.setUniform("projection", glm.value_ptr(projection))

        shader_object.setUniform("view", glm.value_ptr(view))
        shader_object.setUniform("projection", glm.value_ptr(projection))

        # set lights and camera uniforms
        shader_object.setUniform("camera_pos", camera.position)
        shader_object.setUniform("light.position", self.renderer.lights[0].position)

        # draw light
        model = glm.translate(glm.mat4(1.0), self.renderer.lights[0].position) * \
                glm.scale(glm.mat4(1.0), glm.vec3(0.1, 0.1, 0.1))
        shader_light.setUniform("model", glm.value_ptr(model))
        self.renderer.draw(light, shader_light, 0)

        # draw graph
        model = glm.mat4(1.0)
        shader_object.setUniform("model", glm.value_ptr(model))
        self.renderer.draw(graph, shader_object, 0)

        # draw axes
        model = glm.scale(glm.mat4(1.0), glm.vec3(10, 0.1, 0.1))
        shader_object.setUniform("model", glm.value_ptr(model))
        self.renderer.draw(x_axis, shader_object, 0)

        model = glm.scale(glm.mat4(1.0), glm.vec3(0.1, 10, 0.1))
        shader_object.setUniform("model", glm.value_ptr(model))
        self.renderer.draw(y_axis, shader_object, 0)

        model = glm.scale(glm.mat4(1.0), glm.vec3(0.1, 0.1, 10))
        shader_object.setUniform("model", glm.value_ptr(model))
        self.renderer.draw(z_axis, shader_object, 0)

    def resizeGL(self, width, height):
        GL.glViewport(0, 0, width, height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
