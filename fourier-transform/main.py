#!/usr/bin/env python3
# coding: utf-8

import sys, json
import numpy as np
import math, pygame

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

def translate_matrix(dx, dy):
    return np.array([
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1 ]
    ])

def rotate_matrix(a):
    return np.array([
        [np.cos(a), -np.sin(a), 0],
        [np.sin(a),  np.cos(a), 0],
        [        0,          0, 1]
    ])

def DFT(signal):
    X = []
    N = len(signal)
    P = -1j * 2 * math.pi / N

    for k in range(0, N):
        sum = 0 + 0j

        for n in range(0, N):
            sum += signal[n] * pow(math.e,  k * n * P)

        sum /= N
        re, im = sum.real, sum.imag

        X.append({
            'freq' : k,
            'ampl' : math.hypot(re, im),
            'phase': math.atan2(im, re)
        })

    return sorted(X, key=lambda x: x['ampl'], reverse=True)

class Screen(object):
    def __init__(self, w, h, caption=None):
        pygame.init()
        pygame.display.set_caption(caption if caption else '')

        self.width  = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))

        self.reset_transformation_m()

    def reset_transformation_m(self):
        self.tran_m = np.identity(3)

    def background(self, color):
        self.screen.fill(color)

    def update(self):
        pygame.display.flip()
        self.reset_transformation_m()

    def rotate(self, angle):
        self.tran_m = np.matmul(self.tran_m, rotate_matrix(angle))

    def translate(self, dx, dy):
        self.tran_m = np.matmul(self.tran_m, translate_matrix(dx, dy))

    def t_point(self, x, y):
        return list(map(int, self.tran_m.dot(np.array([x, y, 1]))[:-1]))

    def line(self, x1, y1, x2, y2, color, w=1):
        pygame.draw.line(
            self.screen, color,
            self.t_point(x1, y1),
            self.t_point(x2, y2),
            w
        )

    def circle(self, x, y, r, color, w=0):
        pygame.draw.circle(
            self.screen, color,
            self.t_point(x, y),
            int(r), w if r > w else 0
        )

class Simualtion(object):
    def __init__(self, screen, fps=60):
        self.time = 0
        self.path = []

        self.state  = -1
        self.signal = []

        self.fps = fps
        self.screen = screen
        self.fclock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type in [pygame.QUIT, pygame.KEYDOWN]:
                if hasattr(event, 'key') and event.key != pygame.K_ESCAPE:
                    continue

                pygame.quit(), exit()

            if event.type == pygame.MOUSEMOTION and self.state == 0:
                self.signal.append(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.time = 0
                self.path = []
                self.state = 0
                self.signal = []

            elif event.type == pygame.MOUSEBUTTONUP:
                if len(self.signal) == 0:
                    self.signal = [(0, 0)]

                self.state  = 1
                self.signal = DFT([
                    (a - self.screen.width/2) + (b - self.screen.height/2)*1j
                    for a, b in self.signal
                ])

    def update_state(self):
        if self.state == 1:
            self.path = [] if len(self.path) > len(self.signal) else self.path
            self.time = (self.time + 2 * math.pi / len(self.signal)) % (2 * math.pi)

    def draw_epicycles(self, x, y, fourier):
        for f in fourier:
            px, py = x, y

            x = x + f['ampl'] * math.cos(f['freq'] * self.time + f['phase'])
            y = y + f['ampl'] * math.sin(f['freq'] * self.time + f['phase'])

            self.screen.line  (px, py, x, y, (255, 0, 0), 4)
            self.screen.circle(px, py, f['ampl'], BLACK, 2)

        return x, y

    def draw_loop(self):
        self.screen.background(WHITE)

        if self.state == 1:
            self.screen.translate(self.screen.width/2, self.screen.height/2)
            self.path = [self.draw_epicycles(0, 0, self.signal)] + self.path

            for i in range(len(self.path) - 1):
                self.screen.line(*self.path[i], *self.path[i + 1], BLACK, 4)

        else:
            for i in range(len(self.signal) - 1):
                self.screen.line(*self.signal[i], *self.signal[i + 1], BLACK, 3)

    def main_loop(self):
        while True:
            self.handle_events()
            self.update_state()
            self.draw_loop()
            self.screen.update()
            self.fclock.tick(self.fps)

if __name__ == '__main__':
    app = Simualtion(Screen(800, 600, 'Fourier Transform'))
    app.main_loop()