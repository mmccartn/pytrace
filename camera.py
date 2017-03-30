from ray import Ray
from vec3 import Vec
from math import pi, tan
from random import random

def random_in_unit_disk():
    p = Vec()
    while True:
        p.x = 2 * random()
        p.y = 2 * random()
        if Vec.dot(p, p) >= 1:
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
            rd = random_in_unit_disk().mul(self.lens_radius)
        else:
            rd = Vec()
        offset = (self.u * rd.x).add(self.v * rd.y)
        return Ray(
            self.origin + offset,
            offset.neg_add(self.lower_left + s*self.horizontal + t*self.vertical - self.origin)
        )

if __name__ == '__main__':
    pass
