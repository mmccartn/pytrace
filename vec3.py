from math import sqrt
from random import random

class Vec(object):

    __slots__ = ('x', 'y', 'z')

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def copy(self, v):
        self.x = v.x
        self.y = v.y
        self.z = v.z

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def randomize(self):
        self.x = random()
        self.y = random()
        self.z = random()
        return self

    @staticmethod
    def from_vec(v):
        return Vec(v.x, v.y, v.z)

    @staticmethod
    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    @staticmethod
    def cross(v1, v2):
        x = v1.y * v2.z - v1.z * v2.y
        y = v1.x * v2.z - v1.z * v2.x
        z = v1.x * v2.y - v1.y * v2.x
        return Vec(x, -y, z)

    @staticmethod
    def normalize(v):
        return v / v.norm()

    @staticmethod
    def unit_vector(v):
        return Vec.normalize(v)

    @staticmethod
    def reflect(v, n):
        return v - 2 * Vec.dot(v, n) * n

    def norm(self):
        return sqrt(Vec.dot(self, self))

    def squared_length(self):
        return Vec.dot(self, self)

    def length(self):
        return self.norm()

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y, self.z + v.z)

    def __neg__(self):
        return Vec(-self.x, -self.y, -self.z)

    def __sub__(self, v):
        return self + (-v)

    def __mul__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x * v.x, self.y * v.y, self.z * v.z)
        else:
            return Vec(self.x * v, self.y * v, self.z * v)

    def __rmul__(self, v):
        return self.__mul__(v)

    def __div__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x / v.x, self.y / v.y, self.z / v.z)
        else:
            return Vec(self.x / v, self.y / v, self.z / v)

    def __truediv__(self, v):
        return self.__div__(v)

    def __floordiv__(self, v):
        return self.__div__(v)

    def __str__(self):
        return '(%.6f, %.6f, %.6f)' % (self.x, self.y, self.z)

class RGB(Vec):

    def __init__(self, x=0, y=0, z=0):
        self.x = x / 255.0
        self.y = y / 255.0
        self.z = z / 255.0

vec_one = Vec(1, 1, 1)

if __name__ == '__main__':
    pass
