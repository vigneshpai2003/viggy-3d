import numpy as np


#                         coord             UV        normal
cubeVertices = np.array([-0.5, -0.5, +0.5, 0.0, 0.0, 0.0, 0.0, 1.0,  # +z
                         +0.5, -0.5, +0.5, 1.0, 0.0, 0.0, 0.0, 1.0,
                         +0.5, +0.5, +0.5, 1.0, 1.0, 0.0, 0.0, 1.0,
                         -0.5, +0.5, +0.5, 0.0, 1.0, 0.0, 0.0, 1.0,

                         +0.5, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, -1.0,  # -z
                         -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, -1.0,
                         -0.5, +0.5, -0.5, 1.0, 1.0, 0.0, 0.0, -1.0,
                         +0.5, +0.5, -0.5, 0.0, 1.0, 0.0, 0.0, -1.0,

                         +0.5, -0.5, +0.5, 0.0, 0.0, 1.0, 0.0, 0.0,  # +x
                         +0.5, -0.5, -0.5, 1.0, 0.0, 1.0, 0.0, 0.0,
                         +0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 0.0,
                         +0.5, +0.5, +0.5, 0.0, 1.0, 1.0, 0.0, 0.0,

                         -0.5, -0.5, -0.5, 0.0, 0.0, -1.0, 0.0, 0.0,  # -x
                         -0.5, -0.5, +0.5, 1.0, 0.0, -1.0, 0.0, 0.0,
                         -0.5, +0.5, +0.5, 1.0, 1.0, -1.0, 0.0, 0.0,
                         -0.5, +0.5, -0.5, 0.0, 1.0, -1.0, 0.0, 0.0,

                         -0.5, +0.5, +0.5, 0.0, 0.0, 0.0, 1.0, 0.0,  # +y
                         +0.5, +0.5, +0.5, 1.0, 0.0, 0.0, 1.0, 0.0,
                         +0.5, +0.5, -0.5, 1.0, 1.0, 0.0, 1.0, 0.0,
                         -0.5, +0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0,

                         -0.5, -0.5, -0.5, 0.0, 0.0, 0.0, -1.0, 0.0,  # -y
                         +0.5, -0.5, -0.5, 1.0, 0.0, 0.0, -1.0, 0.0,
                         +0.5, -0.5, +0.5, 1.0, 1.0, 0.0, -1.0, 0.0,
                         -0.5, -0.5, +0.5, 0.0, 1.0, 0.0, -1.0, 0.0], dtype=np.float32)

cubeIndices = np.array([[0, 1, 2], [2, 3, 0],  # +z
                        [4, 5, 6], [6, 7, 4],  # -z
                        [8, 9, 10], [10, 11, 8],  # +x
                        [12, 13, 14], [14, 15, 12],  # -x
                        [16, 17, 18], [18, 19, 16],  # +y
                        [20, 21, 22], [22, 23, 20]  # -y
                        ], dtype=np.uint32)
