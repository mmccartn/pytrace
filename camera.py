from ray import Ray
from vec3 import Vec
from math import pi, tan
from random import random

def random_in_unit_disk():
    p = Vec()
    while True:
        p = 2.0 * Vec(random(), random(), 0) * Vec(1, 1, 0)
        if Vec.dot(p, p) >= 1.0:
            break
    return p

class Camera (object):

    __slots__ = ('lens_radius', 'origin', 'lower_left', 'horizontal', 'vertical', 'u', 'v')

    def __init__(self, aspect, vfov, aperture, focus_dist, lookfrom, lookat, vup=Vec(0, 1, 0)):
        self.lens_radius = aperture / 2
        theta = vfov * pi / 180
        half_height = tan(theta / 2)
        half_width = aspect * half_height

        self.origin = lookfrom

        w = Vec.unit_vector(lookfrom - lookat)
        u = Vec.unit_vector(Vec.cross(vup, w))
        v = Vec.cross(w, u)

        self.lower_left = self.origin - half_width * focus_dist * u - half_height * focus_dist * v - focus_dist * w
        self.horizontal = 2 * half_width * focus_dist * u
        self.vertical = 2 * half_height * focus_dist * v

        self.u = u
        self.v = v

    def get_ray(self, s, t):
        if self.lens_radius > 0:
            rd = self.lens_radius * random_in_unit_disk()
        else:
            rd = Vec()
        offset = self.u * rd.x + self.v * rd.y
        return Ray(self.origin + offset, self.lower_left + s*self.horizontal + t*self.vertical - self.origin - offset)

if __name__ == '__main__':
    pass
