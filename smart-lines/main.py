#!/usr/bin/env python3
# coding: utf-8

import vector
import random
import pygame

BLUE  = [ 20, 108, 121]
BLACK = [ 39,  47,  48]

simulation_options = {
    'fps'      : 0,
    'size'     : (400, 400),
    'target'   : (1/4, 1/8),
    'mutrate'  : 0.05,
    'popsize'  : 100,
    'lifespan' : 230,
    'maxforce' : random.uniform(0.2, 2),
    'obstacles': [
        pygame.Rect(  0, 130, 230, 10 ),
        pygame.Rect(170, 250, 230, 10 ),
        #pygame.Rect(230, 130, 120, 10 ),
        pygame.Rect(220,  50,  10, 80 )
    ]
}

class DNA(object):
    def __init__(self, genes, mutrate, maxforce):
        self.genes = [gene.set_mag(maxforce) for gene in genes]
        self.mutrate = mutrate
        self.maxforce = maxforce

    def mutation(self):
        for n in range(len(self.genes)):
            if random.random() < self.mutrate:
                self.genes[n] = vector.Vector.random_vec().set_mag(self.maxforce)

    def crossover(self, parent):
        index = random.randint(0, len(self.genes))
        return DNA(
            self.genes[:index] + parent.genes[index:],
            self.mutrate, self.maxforce
        )

    @staticmethod
    def random_dna(n, mutrate, maxforce):
        return DNA(
            [vector.Vector.random_vec() for _ in range(n)],
            mutrate, maxforce
        )

class Dot(object):
    def __init__(self, dna, acc, vel, pos):
        self.acc, self.vel = acc, vel
        self.dna, self.pos = dna, pos

        self.fitness  = 0
        self.is_alive = True
        self.complete = False

    def calc_fitness(self, target, max_dist):
        self.fitness = 1 - (target.distance(self.pos) / max_dist)

        if self.complete:
            self.fitness *= 10000

        if not self.is_alive:
            self.fitness /= 10

    def update(self, gene_n, target):
        if self.pos.distance(target) < 20:
            self.pos = target.copy()
            self.complete = True

        if self.is_alive and not self.complete:
            self.acc += self.dna.genes[gene_n]
            self.vel += self.acc
            self.pos += self.vel
            self.acc *= vector.Vector(0, 0)
            self.vel = self.vel.limit(4)

class Population(object):
    def __init__(self, init_pos, target,
            max_dist, pop_size, lifespan, mutrate, maxforce):

        self.gene_n = 0
        self.target = target
        self.max_fit = 0
        self.max_dist = max_dist
        self.lifespan = lifespan
        self.init_pos = init_pos
        self.generation = 1
        self.population = []
        self.mating_pool = []

        for _ in range(pop_size):
            self.population.append(
                Dot(
                    DNA.random_dna(lifespan, mutrate, maxforce),
                    vector.Vector(), vector.Vector(), vector.Vector(*init_pos)
                )
            )

    def __iter__(self):
        return iter(self.population)

    def evaluate(self):
        self.max_fit = 0
        self.mating_pool.clear()

        for dot in self:
            dot.calc_fitness(self.target, self.max_dist)
            self.max_fit = dot.fitness if dot.fitness > self.max_fit else self.max_fit

        for dot in self:
            dot.fitness = dot.fitness / self.max_fit
            self.mating_pool += [dot] * pow(max(1, int(dot.fitness * 100)), 2)

        print ('    generation:', self.generation)
        print ('   max fitness:', self.max_fit)
        print ('succesful dots:', len([x for x in self if x.complete == True]))

    def selection(self):
        for n in range(len(self.population)):
            parent_a = random.choice(self.mating_pool).dna
            parent_b = random.choice(self.mating_pool).dna
            while parent_a == parent_b:
                parent_b = random.choice(self.population).dna

            child_dna = parent_a.crossover(parent_b)
            child_dna.mutation()

            self.population[n] = Dot(
                child_dna,
                vector.Vector(),
                vector.Vector(),
                vector.Vector(*self.init_pos)
            )

    def run(self):
        if self.gene_n == self.lifespan:
            self.evaluate()
            self.selection()
            self.gene_n = 0
            self.generation += 1

        for dot in self.population:
            dot.update(self.gene_n, self.target)

        self.gene_n += 1

class Simulation(object):
    pygame.init()
    pygame.display.set_caption('smart lines')

    def __init__(self, fps, size, target,
            mutrate, popsize, lifespan, maxforce, obstacles):

        self.fps = fps
        self.draw = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size)

        self.w, self.h = size
        self.target = vector.Vector(*size) * vector.Vector(*target)
        self.obstacles = obstacles
        self.population = Population(
            (self.w / 2, self.h - 50),
            self.target, vector.Vector(*size).mag(),
            popsize, lifespan, mutrate, maxforce
        )

    def is_dead(self, x, y):
        return any([
            x < 0,
            y < 0,
            x > self.w,
            y > self.h
        ] + [rect.collidepoint(x, y) for rect in self.obstacles])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.fps ^= (60 ^ 0)

                if event.key == pygame.K_d:
                    self.draw ^= (0 ^ 1)

    def update_state(self):
        for dot in self.population:
            if self.is_dead(*dot.pos):
                dot.is_alive = False

        self.population.run()

    def draw_loop(self):
        self.screen.fill(BLUE)

        pygame.draw.circle(self.screen, [110] * 3, self.target.tuple_int(), 20)

        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, [110] * 3, obstacle)

        for dot in self.population:
            line = dot.pos.line(20, 10, dot.vel.angle())
            pygame.draw.line(self.screen, BLACK, *line, 2)

        pygame.display.update()

    def main_loop(self):
        while True:
            self.handle_events()
            self.update_state()

            if self.draw:
                self.draw_loop()
                self.clock.tick(self.fps)

if __name__ == '__main__':
    simulation = Simulation(**simulation_options)
    simulation.main_loop()