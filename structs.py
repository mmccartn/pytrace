from collections import namedtuple

RowResult = namedtuple('RowResult', ('index', 'row'))

class HitRecord(object):

    __slots__ = ('t', 'p', 'n', 'mat')

    def __init__(self, t=None, p=None, n=None, mat=None):
        self.t = t
        self.p = p
        self.n = n
        self.mat = mat

if __name__ == '__main__':
    pass
