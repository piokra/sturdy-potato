from math import sqrt
from typing import List

from pmath.rndgen.advanced import NormalDistribution01


def inp_vec_add(l: List, r: List):
    _len = min(len(l), len(r))
    for i in range(_len):
        l[i] += r[i]


def inp_vec_sub(l: List, r: List):
    _len = min(len(l), len(r))
    for i in range(_len):
        l[i] -= r[i]


def vec_add(l: List, r: List):
    ret = []
    _len = min(len(l), len(r))
    for i in range(_len):
        ret.append(l[i] + r[i])
    return ret


def vec_sub(l: List, r: List):
    ret = []
    _len = min(len(l), len(r))
    for i in range(_len):
        ret.append(l[i] - r[i])
    return ret


def inp_scl_mul(a: float, r: List):
    for i in range(len(r)):
        r[i] *= a


def scl_mul(a: float, r: List):
    ret = []
    for i in range(len(r)):
        ret[i] *= a
    return ret


def dot(l: List, r: List):
    ret = 0.0
    for x, y in zip(l, r):
        ret += x * y
    return ret


def inp_el_wise_mul(l: List, r: List):
    _len = min(len(l), len(r))
    for i in range(_len):
        l[i] *= r[i]


def el_wise_mul(l: List, r: List):
    ret = []
    for x, y in zip(l, r):
        ret.append(x * y)


def replace(l: List, r: List):
    l.clear()
    for el in r:
        l.append(r)


def lenght_squred(l: List):
    ret = 0.0
    for el in l:
        ret += el * el
    return ret


def dist_squared(l: List, r: List):
    ret = 0.0
    for xi, yi in zip(l, r):
        ret += (xi - yi) * (xi - yi)
    return ret


def length(l: List):
    return sqrt(lenght_squred(l))


def dist(l: List, r: List):
    return sqrt(dist_squared(l, r))


_normal_generators = []


def random_dir(dim: int):
    while dim > len(_normal_generators):
        _normal_generators.append(NormalDistribution01())

    point = list(_normal_generators[i].get() for i in range(dim))
    inp_scl_mul(1 / length(point), point)
    return point
