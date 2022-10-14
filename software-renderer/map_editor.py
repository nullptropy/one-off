#!/usr/bin/env python3
# coding: utf-8

import sys
import pygame

class MapEditor(object):
    pygame.init()
    pygame.display.set_caption('map editor')

    def __init__(self, axis, scale, size):
        self.axis = axis
        self.scale = scale
        self.s_size = [size] * 2
        self.screen = pygame.display.set_mode(self.s_size)

        self.dw = self.s_size[0] / scale
        self.dh = self.s_size[1] / scale

        self.points = []

    def cart_coords(self, point):
        w, h = self.s_size
        return [
            round( (point[0] - (w / 2)) / self.dw),
            round(-(point[1] - (h / 2)) / self.dh)
        ]

    def screen_coords(self, point):
        w, h = self.s_size
        return [
            int( point[0] * (w / self.scale) + w / 2),
            int(-point[1] * (h / self.scale) + h / 2)
        ]

    def add_coord(self, p):
        if p not in self.points:
            self.points.append(p)

    def del_coord(self, p):
        if p in self.points:
            self.points.pop(self.points.index(p))

    def draw_points(self):
        for pos in self.points:
            s_pos = self.screen_coords(pos)
            uleft = self.screen_coords((pos[0], pos[1] + 1))

            pygame.draw.rect(self.screen, [255, 0, 0], (*uleft, self.dw, self.dh))
            pygame.draw.circle(self.screen, [0, 0, 255], s_pos, 3)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.on_exit()

            elif event.type == pygame.MOUSEMOTION:
                pos = self.cart_coords(event.pos)

                if pygame.mouse.get_pressed()[0]:
                    self.add_coord(pos)

                elif pygame.mouse.get_pressed()[2]:
                    self.del_coord(pos)

    def draw_grid(self):
        w, h = self.s_size
        dw, dh = self.dw, self.dh

        for k in range(self.scale):
            pygame.draw.line(self.screen, [255] * 3, (dw * k, 0), (dw * k, h), 1)
            pygame.draw.line(self.screen, [255] * 3, (0, dh * k), (w, dh * k), 1)

        pygame.draw.line(self.screen, [0, 255, 0], (w / 2, 0), (w / 2, h))
        pygame.draw.line(self.screen, [0, 255, 0], (0, h / 2), (w, h / 2))

    def on_exit(self):
        for pos in self.points:
            pos.insert(self.axis, 0); print (pos)

        exit()

    def main(self):
        while True:
            self.screen.fill([0] * 3)
            self.draw_grid()
            self.handle_events()
            self.draw_points()
            pygame.display.flip()

if __name__ == '__main__':
    app = MapEditor(*map(int, sys.argv[1:]))
    app.main()