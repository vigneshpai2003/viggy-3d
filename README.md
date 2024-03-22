# viggy-3d

Module for using raw OpenGL via a high level interface in python.
Uses PySide 6 for OpenGL context.

## Installation

Note that the necessary Qt dependencies must be installed on your system, on Ubuntu (wayland), these were the packages: `qtwayland5`, `libxcb-cursor0`, `libxkbcommon-x11-0`.

1. Clone and optionally create virtual environment

2. `pip install -r requirements.txt`

3. `pip install .`

   or

   `pip install -e .` (for editable installation)

Try running any of the examples in samples folder.

1. `cd samples`
2. `python example.py`

## Features:

Users can create models in Blender, Paint3D etc and export them as GLTF encoded files.
Supports nodes, meshes, materials, textures.
No support for animations, bones and skins.
No support for exporting models.

Ultimately meant to be a module for scientific visualization and basic 3D graphics.

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

![Model Rendering](https://github.com/vigneshpai2003/viggy-3d/blob/main/screenshots/model_rendering.png?raw=True)
