#!/usr/bin/env python3
# coding: utf-8

import sys
import random
import pygame

BLACK = [ 39,  47,  48]
GREEN = [  0, 255,   0]
BLUE  = [ 20, 108, 121]
WHITE = [255, 255, 255]

class Wall(object):
    def __init__(self, start, end):
        self.line = [start, end]
        self.exists = True

class Cell(object):
    def __init__(self, i, j, w):
        self.i, self.j = i, j
        self.x, self.y = x, y = j * w, i * w

        self.visited   = False
        self.walls = {
            'top'   : Wall([x, y], [x + w, y]),
            'left'  : Wall([x, y], [x, y + w]),
            'right' : Wall([x + w, y], [x + w, y + w]),
            'bottom': Wall([x, y + w], [x + w, y + w]),
        }

    def neighbours(self):
        i, j = self.i, self.j
        return [
            [i - 1, j], # top
            [i, j + 1], # right
            [i + 1, j], # bottom
            [i, j - 1]  # left
        ]

class Grid(object):
    def __init__(self, size, scale):
        self.size = size
        self.scale = scale

        self.rows = size[1] // scale
        self.cols = size[0] // scale

        self.grid = self.build_grid()

    def __getitem__(self, i):
        return self.grid[i]

    def __iter__(self):
        for i in range(self.rows):
            for j in range(self.cols):
                yield self[i][j]

    def is_valid_cell(self, i, j):
        return not any([
            i < 0,
            j < 0,
            i > self.rows - 1,
            j > self.cols - 1
        ])

    def get_cells(self, cells):
        for i, j in cells:
            if self.is_valid_cell(i, j):
                yield self.grid[i][j]

    def build_grid(self):
        return [
            [Cell(i, j, self.scale) for j in range(self.cols)]
            for i in range(self.rows)
        ]

class MazeGenerator(object):
    pygame.init()
    pygame.display.set_caption('hella lit maze generator')

    def __init__(self, size=(400, 320), scale=20, fps=60):
        self.size, self.scale, self.fps = size, scale, fps
        self.setup()

        self.clock  = pygame.time.Clock()
        self.screen = pygame.display.set_mode(list(map(sum, zip(size, [2, 2])))) # ik, looks awful

    def setup(self):
        self.stack = []
        self.curr_fps = self.fps
        self.grid = Grid(self.size, self.scale)

        self.curr_c = self.grid[0][0]
        self.curr_c.visited = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.curr_fps ^= 0 ^ self.fps

                if event.key == pygame.K_r:
                    self.setup()

                if event.key == pygame.K_s:
                    pygame.image.save(self.screen, 'maze.png')
                    print ('screen saved as maze.png')

    def remove_walls(self, a, b):
        order_x = {
                 1: ('left', 'right'),
                -1: ('right', 'left')}.get(a.j - b.j, None)
        order_y = {
                 1: ('top', 'bottom'),
                -1: ('bottom', 'top')}.get(a.i - b.i, None)

        for order in [order_x, order_y]:
            if order is not None:
                a.walls[order[0]].exists = False
                b.walls[order[1]].exists = False

    def update_state(self):
        neighbours = self.grid.get_cells(self.curr_c.neighbours())
        neighbours = [n for n in neighbours if n.visited == False]

        if len(neighbours) != 0:
            next_c = random.choice(neighbours)
            self.remove_walls(self.curr_c, next_c)
            self.stack.append(self.curr_c)

            self.curr_c = next_c
            self.curr_c.visited = True

        elif len(self.stack) != 0:
            self.curr_c = self.stack.pop(-1)

    def draw_loop(self):
        self.screen.fill(BLACK)

        for cell in self.grid:
            if cell.visited == True:
                rect = pygame.Rect(
                    cell.x, cell.y,
                    self.grid.scale, self.grid.scale
                )
                color = GREEN if cell == self.curr_c else BLUE
                pygame.draw.rect(self.screen, color, rect)

            for wall in cell.walls.values():
                if cell.visited and wall.exists:
                    pygame.draw.line(self.screen, WHITE, *wall.line, 2)

        pygame.display.update()

    def main_loop(self):
        while True:
            self.handle_events()
            self.draw_loop()
            self.update_state()
            self.clock.tick(self.curr_fps)

if __name__ == '__main__':
    generator = MazeGenerator((400, 400), int(sys.argv[1]), 10)
    generator.main_loop()