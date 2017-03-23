from vec3 import Vec
from math import sqrt
from random import random
from structs import HitRecord

class Sphere (object):

    __slots__ = ('center', 'radius', 'material')

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, ray, tmin, tmax, hit_rec):
        oc = ray.origin() - self.center
        a = Vec.dot(ray.direction(), ray.direction())
        b = Vec.dot(oc, ray.direction())
        c = Vec.dot(oc, oc) - self.radius*self.radius
        discriminant = b*b - a*c
        if discriminant > 0:
            temp = (-b - sqrt(b*b-a*c))/a
            if temp < tmax and temp > tmin:
                hit_rec.t = temp
                hit_rec.p = ray.point_at_paramater(hit_rec.t)
                hit_rec.n = (hit_rec.p - self.center) / self.radius
                hit_rec.mat = self.material
                return True
            temp = (-b + sqrt(b * b - a * c)) / a
            if temp < tmax and temp > tmin:
                hit_rec.t = temp
                hit_rec.p = ray.point_at_paramater(hit_rec.t)
                hit_rec.n = (hit_rec.p - self.center) / self.radius
                hit_rec.mat = self.material
                return True
        return False

    @staticmethod
    def random_in_unit_sphere():
        p = Vec(0, 0, 0)
        while True:
            p = 2.0 * Vec(random(), random(), random()) - Vec(1, 1, 1)
            if p.squared_length() < 1.0:
                break
        return p

class HitableList (list):

    def hit(self, ray, tmin, tmax, hit_rec):
        temp_rec = HitRecord()
        has_hit = False
        closest = tmax
        for i in range(len(self)):
            if self[i].hit(ray, tmin, closest, temp_rec):
                has_hit = True
                closest = temp_rec.t
                hit_rec.t = temp_rec.t
                hit_rec.p = temp_rec.p
                hit_rec.n = temp_rec.n
                hit_rec.mat = temp_rec.mat
        return has_hit

if __name__ == '__main__':
    pass
