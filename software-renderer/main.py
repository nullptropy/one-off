#!/usr/bin/env python3
# coding: utf-8

import sys
import random
import pygame

from libm.common import *
from libm.shape  import Shape
from libm.camera import Camera

SKY   = [128, 128, 255]
BLACK = [  0,   0,   0]
WHITE = [255, 255, 255]

move_keys = {
    pygame.K_q: [(1, 1), ( 1,  0)],
    pygame.K_e: [(1, 1), (-1,  0)],
    pygame.K_d: [(0, 2), ( 1,  1)],
    pygame.K_a: [(0, 2), (-1, -1)],
    pygame.K_w: [(2, 0), ( 1, -1)],
    pygame.K_s: [(2, 0), (-1,  1)]
}

class Camera(Camera):
    def move(self, inf):
        ca = cos(self.rot[1]) * self.speed
        sa = sin(self.rot[1]) * self.speed

        if inf[0][0] == 2:
            ca, sa = sa, ca

        axis_d = {0: ca, 1: self.speed, 2: sa}
        for axis, m in zip(*inf):
            self.pos[axis] += (axis_d[axis] * m)

    def key_action(self, keys):
        self.speed += {
            keys[pygame.K_PLUS] :  radians(1),
            keys[pygame.K_MINUS]: -radians(1)
        }.get(1, 0)

        for key in move_keys.keys():
            if keys[key]:
                self.move(move_keys[key])

class GameishWorld(object):
    pygame.init()
    pygame.mouse.set_visible(0)
    pygame.event.set_grab(True)
    pygame.display.set_caption('hella lit, witch')

    def __init__(self, shape, map_file, size=(300, 300), scale=20):
        self.s_size = size
        self.scale  = scale

        self.shapes = self.load_map(shape, map_file)
        self.screen = pygame.display.set_mode(size)

        self.font   = pygame.font.SysFont('monofur', 15)
        self.clock  = pygame.time.Clock()
        self.camera = Camera([0, 0, -5], [0, 0, 0])

    def project(self, p):
        return [p[_] * min(5 / 0.1, 5 / p[-1]) for _ in range(len(p) - 1)]

    def render_text(self, text, pos, color=BLACK):
        self.screen.blit(self.font.render(text, False, color), pos)

    def load_map(self, shape, map_file):
        pos_vals = map(eval, open(map_file, 'r').read().strip().split('\n'))
        return set([Shape.load(shape, pos_val) for pos_val in pos_vals])

    def coords(self, point):
        w, h = self.s_size
        return [
            int( point[0] * (w / self.scale) + w / 2),
            int(-point[1] * (h / self.scale) + h / 2)
        ]

    def handle_events(self):
        pressed_keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    pygame.event.set_grab(pygame.event.get_grab() ^ (0 ^ 1))

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); exit()

            if event.type == pygame.MOUSEMOTION:
                self.camera.turn_around(*pygame.mouse.get_rel())

        for object in [self.camera]:
            object.key_action(pressed_keys)

    def draw_shapes(self, shapes, width=0):
        faces = sum([shape.faces for shape in shapes], [])
        avg_d = []

        for index, (face, color) in enumerate(faces):
            avg_d.append([
                index,
                sum(map(lambda p: distance(p, self.camera.pos), face))
            ])

        for index, _ in sorted(avg_d, key=lambda x: x[1], reverse=True):
            face, color = faces[index]
            face = list(map(self.camera.relative_to_cam, face))

            if any(map(self.camera.is_behind, face)):
                continue # lulw

            pygame.draw.polygon(
                self.screen, color,
                list(map(self.coords, map(self.project, face))), width)

    def draw_loop(self):
        self.screen.fill(SKY)

        self.draw_shapes(self.shapes)
        self.render_text(f'pos: {self.camera}', (5, 21))
        self.render_text(f'fps: {round(self.clock.get_fps())}', (5, 3))

        pygame.display.update()

    def main_loop(self):
        while True:
            self.handle_events()
            self.draw_loop()
            self.clock.tick(60)

if __name__ == '__main__':
    app = GameishWorld(*sys.argv[1:], (500, 500))
    app.main_loop()