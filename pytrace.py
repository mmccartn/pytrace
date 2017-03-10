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

def write_image(p, name='swatch.png', w=200, h=100):
    f = open(name, 'wb') # Taken from: http://pythonhosted.org/pypng/ex.html#colour
    w = png.Writer(w, h) # http://pythonhosted.org/pypng/png.html#png.Writer
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

def hit_sphere(center, radius, ray):
    oc = ray.origin() - center
    a = Vec.dot(ray.direction(), ray.direction())
    b = 2.0 * Vec.dot(oc, ray.direction())
    c = Vec.dot(oc, oc) - radius*radius
    discriminant = b*b - 4*a*c
    return discriminant > 0

def color(ray):
    if hit_sphere(Vec(0, 0, -1), 0.5, ray):
        return Vec(1, 0, 0)
    unit_dir = Vec.unit_vector(ray.direction())
    t = 0.5 * (unit_dir.y + 1.0)
    return (1.0 - t) * Vec(1.0, 1.0, 1.0) + t * Vec(0.5, 0.7, 1.0)

def make_gradiant(width=200, height=100):
    lower_left = Vec(-2, -1, -1)
    horizontal = Vec(4, 0, 0)
    vertical = Vec(0, 2, 0)
    origin = Vec(0, 0, 0)
    p = []
    for j in reversed(range(height)):
        row = []
        for i in range(width):
            u = i / width
            v = j / height
            ray = Ray(origin, lower_left + u*horizontal + v*vertical)
            col = color(ray)
            row.append(col.x * 255.0)
            row.append(col.y * 255.0)
            row.append(col.z * 255.0)
        p.append(row)
    return p

def main():
    write_image(make_gradiant())

if __name__ == '__main__':
    main()
