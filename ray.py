
class Ray (object):

    __slots__ = ('A', 'B')

    def __init__(self, a=None, b=None):
        self.A = a
        self.B = b

    @property
    def origin(self):
        return self.A

    @property
    def direction(self):
        return self.B

    def point_at_paramater(self, t):
        return (t * self.B).add(self.A)

    def __str__(self):
        return 'p(t) = {A} + t*{B}'.format(A=self.A, B=self.B)

if __name__ == '__main__':
    pass
