#!/usr/bin/env python

import sys
import numpy as np
import pygame as pg


class CyclicDemonCrystal(object):
    def __init__(self, width, height, color_set):
        self.width = width
        self.height = height
        self.arena = pg.display.get_surface()
        self.color_set = color_set
        self.current = pg.surfarray.pixels2d(self.arena)
        self.target = self.current.copy()
        self.populate()


    def populate(self):
        from random import choice, seed
        for y in range(0, self.height):
            for x in range(0, self.width):
                color = pg.Color(choice(self.color_set))
                self.current[x,y] = (color.r << 16) | (color.g << 8) | color.b
        seed()


    def advance_target_value(self, x, y):
        top = len(self.color_set)
        raw_color = self.current[x,y]
        color = ((raw_color >> 16 & 0xff), (raw_color >> 8 & 0xff), (raw_color & 0xff))
        next = (self.color_set.index(color) + 1) % top
        next_color = pg.Color(self.color_set[next])
        advance = (next_color.r << 16) | (next_color.g << 8) | next_color.b

        neighbors = (
            self.current[x, (y-1) % self.height],  # up
            self.current[(x-1) % self.width, y],   # left
            self.current[(x + 1) % self.width, y], # right
            self.current[x, (y+1) % self.height],  # down
        )

        if advance in neighbors:
             self.target[x,y] = advance
             # print(f"{self.color_set.index(color)} -> {next}")
        else:
             self.target[x,y] = self.current[x,y]


    def cycle(self):
        for y in range(self.height):
            for x in range(self.width):
                self.advance_target_value(x, y)
        for y in range(self.height):
            for x in range(self.width):
                self.current[x,y] = self.target[x,y]



if __name__ == "__main__":
    w, h = 1600, 1600
    pg.init()

    # pygame setup
    screen = pg.display.set_mode((w, h))
    clock = pg.time.Clock()
    running = True
    indexed_colors = [(0,0,0),
                      (255,0,0), (255,127,0), (127,127,0),
                      (0,255,0), (0,255,127), (0,127,127),
                      (0,0,255), (127, 127, 127), (0,127,255),
                      (255,255,255)]
    cdc = CyclicDemonCrystal(w, h, indexed_colors)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


        # RENDER YOUR GAME HERE
        cdc.cycle()
        # flip() the display to put your work on screen
        pg.display.flip()

        clock.tick()  # limits FPS to 60

    pg.quit()
