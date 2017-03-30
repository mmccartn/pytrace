import vec3
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
        radius = self.radius
        center = self.center
        material = self.material
        direction = ray.direction
        oc = ray.origin - center
        a = Vec.dot(direction, direction)
        b = Vec.dot(oc, direction)
        c = Vec.dot(oc, oc) - radius*radius
        discriminant = b*b - a*c
        if discriminant > 0:
            temp = (-b - sqrt(b*b-a*c))/a
            if temp < tmax and temp > tmin:
                hit_rec.t = temp
                hit_rec.p = ray.point_at_paramater(hit_rec.t)
                hit_rec.n = (hit_rec.p - center) / radius
                hit_rec.mat = material
                return True
            temp = (-b + sqrt(b * b - a * c)) / a
            if temp < tmax and temp > tmin:
                hit_rec.t = temp
                hit_rec.p = ray.point_at_paramater(hit_rec.t)
                hit_rec.n = (hit_rec.p - center) / radius
                hit_rec.mat = material
                return True
        return False

    @staticmethod
    def random_in_unit_sphere():
        p = Vec()
        while True:
            p.x = 2 * random() - 1
            p.y = 2 * random() - 1
            p.z = 2 * random() - 1
            if p.squared_length() < 1:
                break
        return p

class HitableList (list):

    def hit(self, ray, tmin, tmax, hit_rec):
        temp_rec = HitRecord()
        has_hit = False
        closest = tmax
        for hittable in self:
            if hittable.hit(ray, tmin, closest, temp_rec):
                has_hit = True
                closest = temp_rec.t
                hit_rec.t = temp_rec.t
                hit_rec.p = temp_rec.p
                hit_rec.n = temp_rec.n
                hit_rec.mat = temp_rec.mat
        return has_hit

if __name__ == '__main__':
    pass
