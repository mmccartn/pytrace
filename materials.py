from ray import Ray
from vec3 import Vec
from math import sqrt
from random import random
from hittables import Sphere

class Material (object):

    __slots__ = ('albedo', )

    def __init__(self, albedo):
        self.albedo = albedo

class Lambertian (Material):

    def scatter(self, r_in, hit_rec, attenuation, r_scattered):
        target = Sphere.random_in_unit_sphere().add(hit_rec.p).add(hit_rec.n)
        r_scattered.A = hit_rec.p
        r_scattered.B = target.sub(hit_rec.p)
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return True

class Emissive (Material):

    __slots__ = ('color', )

    def __init__(self, albedo, intensity=1.0):
        self.albedo = albedo
        self.color = intensity * self.albedo

class Metal (Material):

    __slots__ = ('fuzz', )

    def __init__(self, albedo, fuzz=1):
        super().__init__(albedo)
        self.fuzz = min(fuzz, 1)

    def scatter(self, r_in, hit_rec, attenuation, r_scattered):
        reflected = Vec.reflect_mv(Vec.unit_vector(r_in.direction), hit_rec.n)
        r_scattered.A = hit_rec.p
        r_scattered.B = Sphere.random_in_unit_sphere().mul(self.fuzz).add(reflected)
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return Vec.dot(r_scattered.direction, hit_rec.n) > 0

class Dialectric (object):

    __slots__ = ('ref_idx', )

    def __init__(self, ri):
        self.ref_idx = ri

    @staticmethod
    def refract(v, n, ior, refracted):
        uv = Vec.unit_vector(v)
        dt = Vec.dot(uv, n)
        disc = 1 - ior * ior * (1 - dt * dt)
        if disc > 0:
            sqrt_disc = sqrt(disc)
            refracted.x = ior * (uv.x - n.x * dt) - n.x * sqrt_disc
            refracted.y = ior * (uv.y - n.y * dt) - n.y * sqrt_disc
            refracted.z = ior * (uv.z - n.z * dt) - n.z * sqrt_disc
            return True
        else:
            return False

    @staticmethod
    def schlick(cosine, ref_idx):
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0
        return r0 + (1 - r0) * pow((1 - cosine), 5)

    def scatter(self, r_in, hit_rec, attenuation, r_scattered):
        r_in_dir = r_in.direction
        reflected = Vec.reflect(r_in_dir, hit_rec.n)
        attenuation.set(1, 1, 1)
        refracted = Vec()
        if Vec.dot(r_in_dir, hit_rec.n) > 0:
            outward_normal = -hit_rec.n
            ior = self.ref_idx
            cosine = ior * Vec.dot(r_in_dir, hit_rec.n) / r_in_dir.length()
        else:
            outward_normal = hit_rec.n
            ior = 1.0 / self.ref_idx
            cosine = -Vec.dot(r_in_dir, hit_rec.n) / r_in_dir.length()
        if Dialectric.refract(r_in_dir, outward_normal, ior, refracted):
            reflect_prob = Dialectric.schlick(cosine, self.ref_idx)
        else:
            r_scattered.A = hit_rec.p
            r_scattered.B = reflected
            reflect_prob = 1.0
        if random() < reflect_prob:
            r_scattered.A = hit_rec.p
            r_scattered.B = reflected
        else:
            r_scattered.A = hit_rec.p
            r_scattered.B = refracted
        return True

if __name__ == '__main__':
    pass
