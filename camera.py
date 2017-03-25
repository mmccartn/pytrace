from ray import Ray
from vec3 import Vec
from math import pi, tan

class Camera (object):

    __slots__ = ('origin', 'lower_left', 'horizontal', 'vertical')

    def __init__(self, aspect, vfov, lookfrom, lookat, vup=Vec(0, 1, 0)):
        theta = vfov * pi / 180
        half_height = tan(theta / 2)
        half_width = aspect * half_height

        self.origin = lookfrom

        w = Vec.unit_vector(lookfrom - lookat)
        u = Vec.unit_vector(Vec.cross(vup, w))
        v = Vec.cross(w, u)

        self.lower_left = self.origin - half_width * u - half_height * v - w
        self.horizontal = 2 * half_width * u
        self.vertical = 2 * half_height * v

    def get_ray(self, s, t):
        return Ray(self.origin, self.lower_left + s*self.horizontal + t*self.vertical - self.origin)

if __name__ == '__main__':
    pass
