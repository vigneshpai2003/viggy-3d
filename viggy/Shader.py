import ctypes
from typing import Dict, Union, Tuple, List

import OpenGL.GL.shaders
import OpenGL.GL as GL


class Shader:
    def __init__(self, shader_dir: str):
        """
        :param shader_dir: directory must contain vertex.gl, fragment.gl, and optionally geometry.gl
        """
        compiledShaders = []
        # key is uniform name and value is a tuple of uniform type followed by uniform location
        self.uniforms: Dict[str, Union[Tuple[str, int], Tuple[Tuple[Tuple[str, str]], List[int]]]] = dict()

        with open(shader_dir.rstrip('/') + "/vertex.gl", 'r') as f:
            compiledShaders.append(GL.shaders.compileShader(f.read(), GL.GL_VERTEX_SHADER))

        with open(shader_dir.rstrip('/') + "/fragment.gl", 'r') as f:
            compiledShaders.append(GL.shaders.compileShader(f.read(), GL.GL_FRAGMENT_SHADER))

        try:
            with open(shader_dir.rstrip('/') + "/geometry.gl", 'r') as f:
                compiledShaders.append(GL.shaders.compileShader(f.read(), GL.GL_GEOMETRY_SHADER))

        except FileNotFoundError:
            pass  # if no geometry shader

        self.program = GL.shaders.compileProgram(*compiledShaders)

        # delete after compiling program
        for shader in compiledShaders:
            GL.glDeleteShader(shader)

        # add uniforms
        for file in ("vertex.gl", "fragment.gl", "geometry.gl"):
            try:
                with open(shader_dir.rstrip('/') + f"/{file}", 'r') as f:
                    self.__addUniformsFromFile(f)
            except FileNotFoundError:
                pass

    def __addUniformsFromFile(self, f):
        f.seek(0)
        lines = f.readlines()

        # remove all empty lines
        while '' in lines:
            lines.remove('')

        # assume first non empty line is version line and remove it
        lines.pop(0)

        # remove all single line comments starting with '//'
        for i in range(len(lines)):
            lines[i] = lines[i][:lines[i].find('//')]

        code = ""
        for line in lines:
            code += line

        code = code.replace('\t', '')

        # remove multiline comments starting with '/*' and ending with '*/'
        while '/*' in code:
            code = code[:code.find('/*')] + code[code.find('*/') + 2:]

        lines = code.split(";")

        # remove whitespaces
        for i in range(len(lines)):
            lines[i] = lines[i].strip(' ')

        structs: Dict[str, Tuple[Tuple[str, str]]] = dict()

        # find all struct definitions
        for i in range(len(lines)):
            if lines[i].startswith('struct '):
                words = lines[i].split(' ')
                # remove empty strings
                while '' in words:
                    words.remove('')
                # words = ['struct', <structNamw>, '{', <type1>, <attribute1>]
                _, structName, _, type1, attribute1 = words
                struct = [(attribute1, type1)]

                i += 1

                while lines[i] != '}':
                    words = lines[i].split(' ')
                    # remove empty strings
                    while '' in words:
                        words.remove('')
                    # words = [<typeN>, <attributeN>]
                    typeN, attributeN = words
                    struct.append((attributeN, typeN))
                    i += 1

                structs[structName] = tuple(struct)

        # find all uniform declarations
        for i in range(len(lines)):
            if lines[i].startswith('uniform '):
                words = lines[i].split(' ')
                # remove empty strings
                while '' in words:
                    words.remove('')
                # words = ['uniform', <uniformType>, <uniformName>]
                _, uniformType, uniformName = words
                if uniformType in structs.keys():
                    self.addUniforms((uniformName, structs[uniformType]))
                else:
                    self.addUniforms((uniformName, uniformType))

    def addUniforms(self, *uniforms: Tuple[str, Union[str, Tuple[Tuple[str, str]]]]):
        """
        tuples of (name, type) pairs for each uniform
        finds location of each uniform and stores internally
        to calculate locations again or change type, pass the tuple again
        """
        OpenGL.GL.glUseProgram(self.program)
        for uniform in uniforms:
            uniformName, uniformType = uniform
            if type(uniformType) == str:
                uniform_location = GL.glGetUniformLocation(self.program, uniformName)
            elif type(uniformType) in (tuple, list):
                uniform_location = []
                for attribute, u_type in uniformType:
                    uniform_location.append(GL.glGetUniformLocation(self.program, f"{uniformName}.{attribute}"))
            else:
                raise Exception(f"uniform '{uniformName}' cannot have type: {uniformType}")
            self.uniforms[uniformName] = (uniformType, uniform_location)

    def setUniform(self, uniform_name: str, value):
        """
        sets the uniform to value using appropriate OpenGL function depending on type
        """
        GL.glUseProgram(self.program)

        try:
            # if setting an attribute of a struct
            if '.' in uniform_name:
                uniform_struct_name, uniform_attribute_name = uniform_name.split(".")
                uniform_struct, uniform_location = self.uniforms[uniform_struct_name]
                for i in range(len(uniform_struct)):
                    attr_name, attr_type = uniform_struct[i]
                    if attr_name == uniform_attribute_name:
                        getattr(self, f"_set_{attr_type}")(uniform_location[i], value)
            else:
                uniform_type, uniform_location = self.uniforms[uniform_name]
                # if setting a non struct variable
                if type(uniform_type) == str:
                    getattr(self, f"_set_{uniform_type}")(uniform_location, value)
                # if setting entire struct
                elif type(uniform_type) in (tuple, list):
                    for i in range(len(uniform_type)):
                        attr_name, attr_type = uniform_type[i]
                        getattr(self, f"_set_{attr_type}")(uniform_location[i], value[i])

        except AttributeError:
            raise Exception(f"uniform: {uniform_name} has invalid type")
        except TypeError:
            raise Exception(f"uniform: {uniform_name} has invalid value")

    def use(self):
        GL.glUseProgram(self.program)

    @staticmethod
    def _set_sampler2D(location: int, x: int):
        GL.glUniform1i(location, x)

    @staticmethod
    def _set_float(location: int, x):
        """
        set a vec1 type uniform
        """
        GL.glUniform1f(location, x)

    @staticmethod
    def _set_vec2(location: int, xy):
        """
        set a vec2 type uniform
        """
        GL.glUniform2f(location, *xy)

    @staticmethod
    def _set_vec3(location: int, xyz):
        """
        set a vec3 type uniform
        """
        GL.glUniform3f(location, *xyz)

    @staticmethod
    def _set_vec4(location: int, xyzw):
        """
        set a vec4 type uniform
        """
        GL.glUniform4f(location, *xyzw)

    @staticmethod
    def _set_mat4(location: int, matrix_ptr: ctypes.POINTER(ctypes.c_float)):
        """
        set a matrix4 type uniform
        """
        GL.glUniformMatrix4fv(location, 1, GL.GL_FALSE, matrix_ptr)
