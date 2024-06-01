import numpy as np

class Edge:
    def __init__(self, start, stop):
        self.start = start
        self.stop  = stop


class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def addEdges(self, edgeList):
        self.edges += edgeList

    def outputNodes(self):
        print("\n --- Nodes --- ")
        for i, (x, y, z, _) in enumerate(self.nodes):
            print(" {0}: ({1}, {2}, {3})".format(i, x, y, z))

    def outputEdges(self):
        print("\n --- Edges --- ")
        for i, (node1, node2) in enumerate(self.edges):
            print(" {0}: ({1} -> {2})".format(i, node1, node2))


    def transform(self, matrix):
        """ Apply a transformation defined by a given matrix. """
        self.nodes = np.dot(self.nodes, matrix)

    @staticmethod
    def translationMatrix(dx=0, dy=0, dz=0):
        """ Return matrix for translation along vector (dx, dy, dz). """
        return np.array([[1,0,0,0],
                         [0,1,0,0],
                         [0,0,1,0],
                         [dx,dy,dz,1]])

    @staticmethod
    def rotateXMatrix(radians):
        """ Return matrix for rotating about the x-axis by 'radians' radians """
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[1, 0, 0, 0],
                        [0, c,-s, 0],
                        [0, s, c, 0],
                        [0, 0, 0, 1]])

    @staticmethod
    def rotateYMatrix(radians):
        """ Return matrix for rotating about the y-axis by 'radians' radians """ 
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[ c, 0, s, 0],
                        [ 0, 1, 0, 0],
                        [-s, 0, c, 0],
                        [ 0, 0, 0, 1]])


    @staticmethod
    def rotateZMatrix(radians):
        """ Return matrix for rotating about the z-axis by 'radians' radians """
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[c,-s, 0, 0],
                        [s, c, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])


    def translate(self, axis, d):
        """ Translate each node of a wireframe by d along a given axis. """
        if axis in ['x', 'y', 'z']:
            for node in self.nodes:
                if axis is 'x': node[0] += d
                elif axis is 'y': node[1] += d
                else: node[2] += d

    def scale(self, center, scale):
        """ Scale the wireframe from the centre of the screen. """
        center_x, center_y = center
        for node in self.nodes:
            node[0] = center_x + scale * (node[0] - center_x)
            node[1] = center_y + scale * (node[1] - center_y)
            node[2] *= scale

    def findCenter(self):
        """ Find the center of the wireframe. """
        num_nodes = len(self.nodes)
        meanX = sum([node[0] for node in self.nodes]) / num_nodes
        meanY = sum([node[1] for node in self.nodes]) / num_nodes
        meanZ = sum([node[2] for node in self.nodes]) / num_nodes
        return (meanX, meanY, meanZ)


    def rotateZ(self, c, radians):
        cx, cy, cz = c
        for node in self.nodes:
            x      = node[0] - cx
            y      = node[1] - cy
            d      = np.hypot(y, x)
            theta  = np.arctan2(y, x) + radians
            node[0] = cx + d * np.cos(theta)
            node[1] = cy + d * np.sin(theta)

    def rotateX(self, c, radians):
        cx, cy, cz = c
        for node in self.nodes:
            y      = node[1] - cy
            z      = node[2] - cz
            d      = np.hypot(y, z)
            theta  = np.arctan2(y, z) + radians
            node[2] = cz + d * np.cos(theta)
            node[1] = cy + d * np.sin(theta)
            
    def rotateY(self, c, radians):
        cx, cy, cz = c
        for node in self.nodes:
            x      = node[0] - cx
            z      = node[2] - cz
            d      = np.hypot(x, z)
            theta  = np.arctan2(x, z) + radians
            node[2] = cz + d * np.cos(theta)
            node[0] = cx + d * np.sin(theta)


if __name__ == "__main__":
    cube = Wireframe()
    cube_nodes = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    cube.addNodes(np.array(cube_nodes))
    cube.addEdges([(n, n + 4) for n in range(0, 4)])
    cube.addEdges([(n, n + 1) for n in range(0, 8, 2)])
    cube.addEdges([(n, n + 2) for n in (0, 1, 4, 5)])
    cube.outputNodes()
    cube.outputEdges()

