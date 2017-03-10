import png
from vec3 import Vec

class Ray (object):

    def __init__(self, a, b):
        self.A = a
        self.B = b

    def origin(self):
        return self.A

    def direction(self):
        return self.B

    def point_at_paramater(self, t):
        return self.A + t*self.B

    def __str__(self):
        return 'p(t) = {A} + t*{B}'.format(A=self.A, B=self.B)

def test_png(): # Taken from: http://pythonhosted.org/pypng/ex.html#colour
    p = [(255, 0, 0, 0, 255, 0, 0, 0, 255),
         (128, 0, 0, 0, 128, 0, 0, 0, 128)]
    f = open('swatch.png', 'wb')
    w = png.Writer(3, 2)  # http://pythonhosted.org/pypng/png.html#png.Writer
    w.write(f, p)
    f.close()

def test_png_2(width=200, height=100):
    p = []
    b = int(0.2 * 255.0)
    for ri in range(height):
        row = []
        r = int((ri / height) * 255.0)
        for ci in range(width):
            g = int((ci / width) * 255.0)
            row.append(r)
            row.append(g)
            row.append(b)
        p.append(row)
    f = open('swatch2.png', 'wb')
    w = png.Writer(width, height)
    w.write(f, p)
    f.close()

def test_ray():
    print(Ray(Vec(1, 2, 3), Vec(4, 5, 6)))

def main():
    test_ray()

if __name__ == '__main__':
    main()
