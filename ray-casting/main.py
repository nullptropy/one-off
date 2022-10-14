#!/usr/bin/python3
# coding: utf-8

from random import randint
from arche import (
    draw, trans, pygame,
    State, ContextBuilder)

from math import cos, sin, hypot, radians

class Wall:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def show(self, ctx):
        pygame.draw.aaline(ctx.screen, (255, 255, 255), self.a, self.b)

class Ray:
    def __init__(self, pos, angle):
        self.pos = pos
        self.dir = [cos(angle), sin(angle)]

    def cast(self, wall):
        x1, y1, x2, y2 = (*wall.a, *wall.b)
        x3, y3, x4, y4 = (*self.pos, self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])

        if (den := (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)) != 0:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den * -1

            if (0 < t < 1) and u > 0:
                return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        
        return None

class Particle:
    def __init__(self, pos):
        self.surface = pygame.Surface((600, 600))
        self.surface.set_alpha(75)

        self.pos = pos
        self.rays = [
            Ray(pos, radians(a)) for a in range(0, 360, 1)]

    def update(self, x, y):
        self.pos = (x, y)

        for ray in self.rays:
            ray.pos = self.pos

    def cast(self, ctx, walls):
        x1, y1 = self.pos
        self.surface.fill((0, 0, 0))

        for ray in self.rays:
            nearest = (float('inf'), float('inf'))
    
            for wall in walls:
                if p := ray.cast(wall):
                    nearest = min(p, nearest, key=lambda c: hypot(x1 - c[0], y1 - c[1]))
            
            if nearest[0] != float('inf'):
                pygame.draw.line(self.surface, (255, 255, 255), self.pos, nearest, 1)

        ctx.screen.blit(self.surface, (0, 0))

    def show(self, ctx):
        pygame.draw.circle(ctx.screen, (255, 255, 255), self.pos, 16)

class MainState(State):
    def on_start(self):
        self.particle = Particle((300, 300))
        self.generate_walls()

    def generate_walls(self):
        self.walls = []

        for _ in range(5):
            x1, y1 = randint(0, 600), randint(0, 600)
            x2, y2 = randint(0, 600), randint(0, 600)
            self.walls.append(Wall((x1, y1), (x2, y2)))

        self.walls += [
            Wall((  0,   0), (600,   0)),
            Wall((  0,   0), (  0, 600)),
            Wall((600,   0), (600, 600)),
            Wall((  0, 600), (600, 600))]

    def handle_keydown_event(self, event):
        if event.key == pygame.K_r:
            self.generate_walls()

    def update(self, ctx, dt):
        self.particle.update(*pygame.mouse.get_pos())

    def draw(self, ctx, interpolation):
        draw.clear(ctx, (0, 0, 0))

        self.particle.cast(ctx, self.walls)
        self.particle.show(ctx)
        
        list(map(lambda b: b.show(ctx), self.walls[:-4]))

if __name__ == '__main__':
    ContextBuilder('ray casting', 600, 600) \
        .icon(pygame.Surface((1, 1))) \
        .show_mouse(False) \
        .grab_mouse(True) \
        .step(60) \
        .fps(75) \
        .build() \
        .run(MainState)
