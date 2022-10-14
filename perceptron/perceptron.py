#!/usr/bin/env python3
# coding: utf-8

import sys, math, json
import random, pygame

RED   = [121,   0,   0]
BLUE  = [ 20, 108, 121]
BLACK = [ 39,  47,  48]
GREEN = [121, 180,  20]
WHITE = [200, 200, 200]

f_function = lambda x: x

def map_(n, a, b, c, d):
    return ((n - a) / (b - a)) * (d - c) + c

class Point(object):
    def __init__(self, x, y, label):
        self.values = (x, y, 1)
        self.bias, self.label = 1, label

    def __iter__(self):
        return iter(self.values)

    @staticmethod
    def random_point(f, r=1):
        x, y = random.uniform(-r, r), random.uniform(-r, r)
        return Point(x, y, 1 if y > f(x) else -1)

class Perceptron(object):
    def __init__(self, n, lr, ws=None):
        if ws is None:
            ws = [random.uniform(-1, 1) for _ in range(n)]

        self.lr = lr
        self.weights = ws

    def sign(self, n):
        return abs(n) / n if n != 0 else 1

    def guess(self, inputs):
        return self.sign(sum(i * w for i, w in zip(inputs, self.weights)))

    def guess_y(self, x):
        w0, w1, w2 = self.weights
        return -(w2/w1) - (w0/w1) * x

    def train(self, inputs, desired):
        self.weights = [
            w + i * self.lr * (desired - self.guess(inputs))
            for i, w in zip(inputs, self.weights)
        ]

    def dump(self, filepath):
        with open(filepath, 'w') as file:
            data = {
                'n' : len(self.weights),
                'lr': self.lr,
                'ws': self.weights
            }
            file.write(json.dumps(data, indent=4))

class Simulation(object):
    pygame.init()
    pygame.display.set_caption('perceptron')

    def __init__(self, input_n=100, fps=60, size=(400, 400),
                       train=True, model=None, tick=1):
        self.fps = fps
        self.size = size
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size)

        self.tick = tick
        self.count = 0
        self.train = train
        self.input_n = input_n
        self.data_set = self.new_dataset(input_n)
        self.perceptron = Perceptron(**model) if model else Perceptron(3, 0.1)

    def coords(self, x, y):
        return list(map(int, (
                map_(x, -1, 1, 0, self.size[0]),
            map_(y, -1, 1, self.size[1], 0)
        )))

    def new_dataset(self, n):
        return [Point.random_point(f_function) for _ in range(n)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.fps ^= (60 ^ 0)

                if event.key == pygame.K_s:
                    self.perceptron.dump('./model.json')

                if event.key == pygame.K_n:
                    self.data_set = self.new_dataset(self.input_n)

    def update(self, n):
        for _ in range(n):
            if self.train:
                input_data = self.data_set[self.count]
                self.perceptron.train(input_data.values, input_data.label)
                self.count = (self.count + 1) % len(self.data_set)

    def draw_loop(self):
        self.screen.fill([0]*3)

        for point in self.data_set:
            color  = GREEN if self.perceptron.guess(point.values) == point.label else RED
            color_ = BLACK  if point.label == 1 else WHITE

            pygame.draw.circle(self.screen, color, self.coords(*point.values[:2]), 6)
            pygame.draw.circle(self.screen, color_, self.coords(*point.values[:2]), 8, 1)

            # print (point.label == self.perceptron.guess(point.values))

        line_orig = (
            self.coords( 1, f_function( 1)),
            self.coords(-1, f_function(-1))
        )
        pygame.draw.line(self.screen, [110] * 3, *line_orig, 2)

        line_guess = (
            self.coords( 1, self.perceptron.guess_y( 1)),
            self.coords(-1, self.perceptron.guess_y(-1))
        )
        pygame.draw.line(self.screen, [255] * 3, *line_guess, 2)

        pygame.display.update()

    def main_loop(self):
        while True:
            self.handle_events()
            self.draw_loop()
            self.update(self.tick)
            self.clock.tick(self.fps)

if __name__ == '__main__':
    train, model = True, None

    if len(sys.argv) > 1:
        train, model = False, json.loads(open(sys.argv[1], 'r').read())

    simulation = Simulation(300, 0, (400, 400), train, model, 20)
    simulation.main_loop()
