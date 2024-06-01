import wireframe as wf
import cube
import pygame
import numpy as np


key_to_function = {
    pygame.K_LEFT: (lambda x: x.translateAll([-10, 0, 0])),
    pygame.K_RIGHT:(lambda x: x.translateAll([ 10, 0, 0])),
    pygame.K_DOWN: (lambda x: x.translateAll([0,  10, 0])),
    pygame.K_UP:   (lambda x: x.translateAll([0, -10, 0])),
    pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
    pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8)),
    pygame.K_q: (lambda x: x.rotateAll('X',  0.1)),
    pygame.K_w: (lambda x: x.rotateAll('X', -0.1)),
    pygame.K_a: (lambda x: x.rotateAll('Y',  0.1)),
    pygame.K_s: (lambda x: x.rotateAll('Y', -0.1)),
    pygame.K_z: (lambda x: x.rotateAll('Z',  0.1)),
    pygame.K_x: (lambda x: x.rotateAll('Z', -0.1))}


class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Menger Sponge wireframe')
        self.background = (10,10,50)
        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColor = (255,255,255)
        self.edgeColor = (200,200,200)
        self.nodeRadius = 4

    def run(self):
        """ Create a pygame screen until it is closed. """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
            self.display()
            pygame.display.flip()


    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """
        self.wireframes[name] = wireframe


    def translateAll(self, vector):
        """ Translate all wireframes along a given axis by d units. """
        matrix = wf.Wireframe.translationMatrix(*vector)
        for wireframe in iter(self.wireframes.values()):
            wireframe.transform(matrix)


    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """
        center_x = self.width/2
        center_y = self.height/2
        for wireframe in iter(self.wireframes.values()):
            wireframe.scale((center_x, center_y), scale)


    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """
        rotateFunction = 'rotate' + axis
        for wireframe in iter(self.wireframes.values()):
            center = wireframe.findCenter()
            getattr(wireframe, rotateFunction)(center, theta)


    def display(self):
        """ Draw the wireframes on the screen. """
        self.screen.fill(self.background)
        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for n1, n2 in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColor, wireframe.nodes[n1][:2], wireframe.nodes[n2][:2], 1)
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColor, (int(node[0]), int(node[1])), self.nodeRadius, 0)


class Sponge(cube.Cube):
    def __init__(self, pos, size):
        super().__init__(pos)
        self.cells = []

        for i in range(-1,2):
            for j in range(-1,2):
                for k in range(-1,2):
                    section = size / 3
                    self.cells.append(cube.Cube((int(pos[0]+i*section),
                                                 int(pos[1]+i*section),
                                                 int(pos[2]+i*section))))


if __name__ == '__main__':
    position = (250, 750, 0)
    pv = ProjectionViewer(1000, 1000)
    sponge = Sponge(position, position[1] - position[0])
    pv.addWireframe('parent', sponge)
    for n, cell in enumerate(sponge.cells):
        pv.addWireframe(f'cube{n}', cell)
    pv.run()