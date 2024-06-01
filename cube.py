import wireframe

class Cube(wireframe.Wireframe):
    def __init__(self, position):
        super().__init__()
        size = (position[0], position[1])
        nodes = [(x,y,z) for x in size for y in size for z in size]
        self.dimensions = position[1] - position[0]
        self.addNodes(nodes)
        self.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
        mat = self.translationMatrix(dz=position[2])
        self.transform(mat)
