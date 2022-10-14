# coding: utf-8

from .common import *
from re import findall

class Shape(object):
    def __init__(self, points, face_data, pos=[0, 0, 0]):
        self.pos = pos
        self.face_data = face_data

        self.points = [
            list(map(sum, zip(pos, point)))
            for point in points
        ]
        self.faces = [
            (list(map(lambda x: self.points[x], f[0])), hex_to_rgb(f[1]))
            for f in face_data
        ]

    def __str__(self):
        return 'Shape(pos={})'.format(str(self.pos))

    def __repr__(self):
        return self.__str__()

    @classmethod
    def load(cls, file_name, pos=(0, 0, 0)):
        return cls.loads(open(file_name, 'r').read(), pos)

    @staticmethod
    def loads(data, pos=(0, 0, 0)):
        load = lambda f, expr, data: list(map(f, findall(expr, data)))
        return Shape(**{
            'pos'      : pos,
            'points'   : load(eval, '\((.*?)\)\n', data),
            'face_data': load(lambda d: (eval(d[0]), d[1]), '\((.*?)\); #(\w+)', data)
        })

    def dump(self):
        return '// points\n{points}\n\n// face_data\n{face_data}'.format(
            points   ='\n'.join(map(str, self.points)),
            face_data='\n'.join('{}; #{}'.format(d, c) for d, c in self.face_data)
        )

#    @property
#    def faces(self):
#        return [
#            (list(map(lambda x: self.points[x], f[0])), hex_to_rgb(f[1]))
#            for f in self.face_data
#        ]