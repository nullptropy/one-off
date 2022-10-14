# coding: utf-8

import math
import random

class Vector(object):
    def __init__(self, *args):
        self.values = args if args else (0, 0)

    def __str__(self):
        return str(self.values)

    def __add__(self, other):
        return Vector(*(p + q for p, q in zip(self, other)))

    def __sub__(self, other):
        return Vector(*(p - q for p, q in zip(self, other)))

    def __mul__(self, other):
        return Vector(*(p * q for p, q in zip(self, other)))

    def __div__(self, other):
        return Vector(*(p / q for p, q in zip(self, other)))

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, index):
        return self.values[index]

    def mag(self):
        return math.sqrt(sum(c ** 2 for c in self))

    def copy(self):
        return Vector(*self.values)

    def limit(self, max):
        return self if self.mag() < math.sqrt(max) else self.set_mag(max)

    def set_mag(self, n):
        return self.normalize() * Vector(n, n)

    def angle(self):
        return math.atan2(self[1], self[0])

    def tuple_int(self):
        return tuple(map(int, self.values))

    def normalize(self):
        return Vector(*(c / self.mag() for c in self))

    def distance(self, other):
        return math.sqrt(sum(pow(a - b, 2) for a, b in zip(self, other)))

    def rotate(self, angle):
        return Vector(
            math.cos(self.angle() + angle) * self.mag(),
            math.sin(self.angle() + angle) * self.mag()
        )

    @staticmethod
    def from_angle(angle, length=1):
        return Vector(
            math.cos(angle) * length,
            math.sin(angle) * length
        )

    @classmethod
    def random_vec(cls):
        return cls.from_angle(random.random() * 2 * math.pi)

    def line(self, r_x=None, r_y=None, ang=None):
        x, y = self.values

        r_x = r_x or self.mag()
        r_y = r_y or self.mag()
        ang = ang or self.angle()

        return (x, y), (x - r_x * math.cos(ang), y - r_y * math.sin(ang))