from viggy.GLTFImporter import *

car = GLTFFile("extra/car.glb", True)
for node in car.nodes:
    print(node.globalTransform)
