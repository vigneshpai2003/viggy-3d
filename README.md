# viggy-3d

This module is meant to be an alternative to using vpython.
Uses PySide 6 for OpenGL context.

Users can create models in Blender, Paint3D etc and export them as GLTF encoded files.
Supports nodes, meshes, materials, textures.
No support for animations, bones and skins.
No support for exporting models.

Ultimately meant to be a module for scientific visualization and basic 3D graphics.

Features:

 - Import GLTF 2.0 files (.glb and .gltf)
 - High level API for adding cameras, lights and models
 - Automatically detect uniforms in your GLSL code! 
 - Support for sky boxes
 - Embed in custom PySide application as a QOpenGLWidget

Coming Soon:

 - 'Primitive' objects such as spheres, cubes, planes, etc
 - Normal maps
 - PBR lighting effects
 - Instancing
 - Tool for showing normal vectors and mesh triangles
 - Different light casters
 - Basic tools for data visualization
    - scatter plots
    - vector fields
    - surfaces
    - time variate 3d functions
 - Basic GUI tools using PySide
