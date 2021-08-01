import GLTFTools as gltf


class Model:
    def __init__(self, path, binary=False):
        self.root = gltf.GLTFFile(path, binary)

        for rootNode in self.root.scene.rootNodes:
            self.__processNode(rootNode)

    def __processNode(self, node: gltf.Node):
        self.__processMesh(node.mesh)

        for childNode in node.children:
            self.__processNode(childNode)

    def __processMesh(self, mesh: gltf.Mesh):
        for primitive in mesh.primitives:
            if primitive.mode is gltf.PrimitiveMode.TRIANGLES:
                pass
