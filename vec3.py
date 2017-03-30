from math import sqrt

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
    def unit_vector(v):
        return v / v.length()

    @staticmethod
    def reflect(v, n):
        a = Vec.dot(v, n)
        return (2 * a * n).neg_add(v)

    @staticmethod
    def reflect_mv(v, n):
        a = 2 * Vec.dot(v, n)
        v.x = v.x - a * n.x
        v.y = v.y - a * n.y
        v.z = v.z - a * n.z
        return v

    def squared_length(self):
        return Vec.dot(self, self)

    def length(self):
        return sqrt(Vec.dot(self, self))

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y, self.z + v.z)

    def add(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def __neg__(self):
        return Vec(-self.x, -self.y, -self.z)

    def neg(self):
        self.x *= -1
        self.y *= -1
        self.z *= -1
        return self

    def neg_add(self, v):
        self.x = v.x - self.x
        self.y = v.y - self.y
        self.z = v.z - self.z
        return self

    def __sub__(self, v):
        return Vec(self.x - v.x, self.y - v.y, self.z - v.z)

    def sub(self, v):
        self.x = self.x - v.x
        self.y = self.y - v.y
        self.z = self.z - v.z
        return self

    def __mul__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x * v.x, self.y * v.y, self.z * v.z)
        else:
            return Vec(self.x * v, self.y * v, self.z * v)

    def mul(self, scalar):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self

    def vec_mul(self, v):
        self.x *= v.x
        self.y *= v.y
        self.z *= v.z
        return self

    def __rmul__(self, v):
        return self.__mul__(v)

    def __div__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x / v.x, self.y / v.y, self.z / v.z)
        else:
            return Vec(self.x / v, self.y / v, self.z / v)

    def vec_div(self, v):
        pass

    def div(self, scalar):
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return self

    def __truediv__(self, v):
        return self.__div__(v)

    def __floordiv__(self, v):
        return self.__div__(v)

    def __str__(self):
        return '(%.6f, %.6f, %.6f)' % (self.x, self.y, self.z)

    def __repr__(self):
        return self.__str__()

class RGB(Vec):

    def __init__(self, x=0, y=0, z=0):
        self.x = x / 255.99
        self.y = y / 255.99
        self.z = z / 255.99

if __name__ == '__main__':
    pass
