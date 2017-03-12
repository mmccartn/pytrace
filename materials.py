from ray import Ray
from vec3 import Vec
from hittables import Sphere

class Material (object):

    def __init__(self, albedo):
        self.albedo = albedo

class Lambertian (Material):

    def scatter(self, r_in, hit_rec, attenuation, r_scattered):
        target = hit_rec['p'] + hit_rec['n'] + Sphere.random_in_unit_sphere()
        r_scattered.A = hit_rec['p']
        r_scattered.B = target - hit_rec['p']
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return True

class Metal (Material):

    def scatter(self, r_in, hit_rec, attenuation, r_scattered):
        reflected = Vec.reflect(Vec.unit_vector(r_in.direction()), hit_rec['n'])
        r_scattered.A = hit_rec['p']
        r_scattered.B = reflected
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return Vec.dot(r_scattered.direction(), hit_rec['n']) > 0

if __name__ == '__main__':
    pass
