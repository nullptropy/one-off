# coding: utf-8

from .common import *

class Camera(object):
    def __init__(self, pos, rot, speed=0.2):
        self.pos = pos
        self.rot = rot
        self.speed = speed

    def __str__(self):
        return 'Camera(pos={}, rot={}, speed={})'.format(
            list(map(int, self.pos)),
            list(map(lambda r: int(degrees(r)), self.rot)),
            int(self.speed * 10)
        )

    def __repr__(self):
        return self.__str__()

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        self.__speed = max(radians(11.5), speed)

    def is_behind(self, point):
        # point -> relative_to_cam(point)
        return False if point[-1] > 0 else True

    def rotate(self, axis, angle):
        self.rot[axis] += radians(angle)
        self.rot[axis] %= 2*pi

    def turn_around(self, x, y):
        self.rotate(0, -y * 0.2)
        self.rotate(1, -x * 0.2)

    def relative_to_cam(self, p):
        return matmult(
            rotation_matrix(*self.rot),
            array([p[i] - self.pos[i] for i in range(len(p))])
        )

    def move(self, inf):
        raise NotImplementedError()

    def key_action(self, keys):
        raise NotImplementedError()