"""
Incomplete Functionality
"""
from __future__ import annotations

import numpy as np


# TODO: load other filetypes
def loadObject(obj_file: str, UV=True, normals=True) -> np.ndarray:
    """
    :param obj_file: .obj file
    :param UV: whether to include UVs
    :param normals: whether to include normals
    :return: returns a vertex array of format (x, y, z, [U, V], [n.x, n.y, n.z]) for each vertex in each triangle
    """
    vertices = []

    obj_vertices = []
    obj_UV = []
    obj_normals = []

    with open(obj_file, 'r') as f:
        line = f.readline()

        while line:
            if line[:2] == 'vt':
                if UV:
                    obj_UV.append([float(i) for i in line[3:].split(' ')])
            elif line[:2] == 'vn':
                if normals:
                    obj_normals.append([float(i) for i in line[3:].split(' ')])
            elif line[0] == 'v':
                obj_vertices.append([float(i) for i in line[2:].split(' ')])
            elif line[0] == 'f':
                for data in line[2:].split(' '):
                    i, j, k = [int(i) for i in data.split('/')]
                    vertices.extend([*obj_vertices[i - 1]])
                    if UV:
                        vertices.extend([*obj_UV[j - 1]])
                    if normals:
                        vertices.extend([*obj_normals[k - 1]])
            line = f.readline()

    return np.array(vertices, dtype=np.float32)
