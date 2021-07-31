# Viggy

This module is meant to be an alternative to using vpython.
Uses PySide 6 for OpenGL context.

Users can create models in Blender, Paint3D etc and export them as GLTF encoded files.
Supports nodes, meshes, materials, textures.
No support for animations, bones and skins.
No support for exporting models.

Ultimately meant to be a module for scientific visualization and basic 3D graphics.

Features:

 - Import GLTF 2.0 files (compatible with Paint3D and Blender)
 - High level API for adding cameras, lights and materials.
 - Automatically detect uniforms in your GLSL code!
 - Embed in custom PySide application as a QOpenGLWidget
 - Support for cube-maps
