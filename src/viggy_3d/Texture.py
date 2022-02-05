import OpenGL.GL as GL
from PIL import Image

import viggy_3d.GLTFImporter as gltf


GLMinFilter = {gltf.TextureMinFilter.NEAREST: GL.GL_NEAREST,
               gltf.TextureMinFilter.LINEAR: GL.GL_LINEAR,
               gltf.TextureMinFilter.NEAREST_MIPMAP_NEAREST: GL.GL_NEAREST_MIPMAP_NEAREST,
               gltf.TextureMinFilter.LINEAR_MIPMAP_NEAREST: GL.GL_LINEAR_MIPMAP_NEAREST,
               gltf.TextureMinFilter.NEAREST_MIPMAP_LINEAR: GL.GL_NEAREST_MIPMAP_LINEAR,
               gltf.TextureMinFilter.LINEAR_MIPMAP_LINEAR: GL.GL_LINEAR_MIPMAP_LINEAR,
               None: GL.GL_LINEAR}

GLMagFilter = {gltf.TextureMagFilter.NEAREST: GL.GL_NEAREST,
               gltf.TextureMagFilter.LINEAR: GL.GL_LINEAR,
               None: GL.GL_LINEAR}

GLWrap = {gltf.TextureWrap.REPEAT: GL.GL_REPEAT,
          gltf.TextureWrap.CLAMP_TO_EDGE: GL.GL_CLAMP_TO_EDGE,
          gltf.TextureWrap.MIRRORED_REPEAT: GL.GL_MIRRORED_REPEAT,
          None: GL.GL_REPEAT}


class Texture:
    def __init__(self, texture: gltf.Texture):
        self.textureID = GL.glGenTextures(1)

        GL.glBindTexture(GL.GL_TEXTURE_2D, self.textureID)

        # define texture image details
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GLMinFilter[texture.sampler.minFilter])
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GLMagFilter[texture.sampler.magFilter])
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GLWrap[texture.sampler.wrapS])
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GLWrap[texture.sampler.wrapT])

        img = Image.open(texture.image.path)
        # img = img.transpose(Image.FLIP_TOP_BOTTOM)  # needed due to internal storage format in GLSL

        # send data to OpenGL
        GL.glTexImage2D(GL.GL_TEXTURE_2D,  # texture type
                        0,
                        GL.GL_RGB,  # internal format
                        img.width, img.height,  # dims
                        0,  # border
                        GL.GL_RGB,  # OpenGL format
                        GL.GL_UNSIGNED_BYTE,  # data type
                        img.convert("RGB").tobytes())  # data

        if texture.sampler.minFilter in (gltf.TextureMinFilter.NEAREST_MIPMAP_NEAREST,
                                         gltf.TextureMinFilter.LINEAR_MIPMAP_NEAREST,
                                         gltf.TextureMinFilter.NEAREST_MIPMAP_LINEAR,
                                         gltf.TextureMinFilter.LINEAR_MIPMAP_LINEAR):
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)  # needed because of GL_LINEAR_MIPMAP_LINEAR

    def bind(self, unit: int):
        """
        bind to unit before drawing
        """
        GL.glActiveTexture(eval(f"GL.GL_TEXTURE{unit}"))
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.textureID)
