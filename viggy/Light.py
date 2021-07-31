import glm


class Light:
    def __init__(self, pos: glm.vec3,
                 ambient: glm.vec3, diffuse: glm.vec3, specular: glm.vec3,
                 k: glm.vec3):
        """
        :param pos:
        :param ambient:
        :param diffuse:
        :param specular:
        :param k: attenuation coefficients of x**0, x**1, x**2 respectively
        """
        self.position = pos
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.k = k
