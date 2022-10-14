# coding: utf-8

__all__ = (
    'pi', 'sin', 'cos', 'radians', 'array', 'matmult',
    'hex_to_rgb', 'distance', 'rotation_matrix', 'degrees'
)

from numpy import (
    pi, sin, cos, sqrt,
    array, matmul, radians, degrees
)

def matmult(p, q):
    return matmul(p, q.T).T

def hex_to_rgb(color):
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

def distance(p, q):
    return sqrt(sum(pow((p_i - q_i), 2) for p_i, q_i in zip(p, q)))

def rotation_matrix(a, b, c):
    sa, ca = sin(a), cos(a)
    sb, cb = sin(b), cos(b)
    sc, cc = sin(c), cos(c)
    return [
        (           cb*cc,           -cb*sc,     sb),
        (ca*sc + sa*sb*cc, ca*cc - sc*sa*sb, -cb*sa),
        (sc*sa - ca*sb*cc, ca*sc*sb + sa*cc,  ca*cb)
    ]