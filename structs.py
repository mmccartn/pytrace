from collections import namedtuple

PixelResult = namedtuple('PixelResult', ('index', 'color'))

class HitRecord(object):

    __slots__ = ('t', 'p', 'n', 'mat')

    def __init__(self, t, p, n, mat):
        self.t = t
        self.p = p
        self.n = n
        self.mat = mat

if __name__ == '__main__':
    pass
