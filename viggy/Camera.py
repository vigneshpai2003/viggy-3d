import glm


# TODO: create different types of camera motion functions using Key and Mouse events
# TODO: quaternion rendering

class Camera:
    def __init__(self, pos: glm.vec3, fov: float, z_min: float, z_max: float):
        """
        :param pos: initial position
        :param fov: field of view, optimal at 45 degrees
        :param z_min: minimum distance for rendering
        :param z_max: maximum distance for rendering
        """
        self.position = pos
        self.fov = fov
        self.zMin = z_min
        self.zMax = z_max
        self.__upAxis = glm.vec3(0, 1, 0)
        self.__xAxis = glm.vec3(1, 0, 0)  # the right axis
        self.__yAxis = glm.vec3(0, 1, 0)  # almost same as up axis
        self.__zAxis = glm.vec3(0, 0, 1)  # the axis coming out of the plane
        self.__view = glm.mat4(1.0)
        self.__projection = glm.mat4(1.0)

    @property
    def xAxis(self) -> glm.vec3:
        return self.__xAxis

    @property
    def yAxis(self) -> glm.vec3:
        return self.__yAxis

    @property
    def zAxis(self) -> glm.vec3:
        return self.__zAxis

    @property
    def view(self) -> glm.mat4:
        """
        :return: view matrix
        """
        return glm.lookAt(self.position,  # eye
                          self.position - self.__zAxis,  # center
                          self.__upAxis)  # up

    def projection(self, aspect: float) -> glm.mat4:
        """
        call wrapper function in Renderer to automatically calculate aspect ratio using viewport width / height
        :param aspect:
        :return: perspective projection matrix with given aspect ratio
        """
        return glm.perspective(self.fov, aspect, self.zMin, self.zMax)

    def setTarget(self, target: glm.vec3):
        """
        points the camera towards target vector
        """
        self.__zAxis = glm.normalize(self.position - target)

        xAxis = glm.cross(self.__upAxis, self.__zAxis)
        if glm.length(xAxis) == 0.0:
            self.__xAxis = glm.normalize(glm.cross(glm.vec3(.1, .1, .1), self.__zAxis))
        else:
            self.__xAxis = glm.normalize(xAxis)

        self.__yAxis = glm.normalize(glm.cross(self.__zAxis, self.__xAxis))
        self.__upAxis = glm.vec3(self.__yAxis)

    def setFront(self, front: glm.vec3):
        """
        points the camera in direction of front, front axis is negative of z axis
        """
        self.setTarget(self.position + front)

    def setUpAxis(self, up: glm.vec3):
        """
        change the up, x, y axis unchanging the z axis (roll camera)
        """
        self.__upAxis = up
        self.__xAxis = glm.normalize(glm.cross(self.__upAxis, self.__zAxis))
        self.__yAxis = glm.normalize(glm.cross(self.__zAxis, self.__xAxis))

    def moveX(self, step: float):
        self.position += self.__xAxis * step

    def moveY(self, step: float):
        self.position += self.__yAxis * step

    def moveZ(self, step: float):
        self.position -= self.__zAxis * step
