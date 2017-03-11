import png
from vec3 import Vec
from math import sqrt
from time import time
from sys import stdout
from random import random
from multiprocessing import Process, Queue, freeze_support

class Sphere (object):

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def hit(self, ray, tmin, tmax, hit_rec):
        oc = ray.origin() - self.center
        a = Vec.dot(ray.direction(), ray.direction())
        b = Vec.dot(oc, ray.direction())
        c = Vec.dot(oc, oc) - self.radius*self.radius
        discriminant = b*b - a*c
        if discriminant > 0:
            temp = (-b - sqrt(b*b-a*c))/a
            if temp < tmax and temp > tmin:
                hit_rec['t'] = temp
                hit_rec['p'] = ray.point_at_paramater(hit_rec['t'])
                hit_rec['n'] = (hit_rec['p'] - self.center) / self.radius
                return True
            temp = (-b + sqrt(b*b-a*c))/a
            if temp < tmax and temp > tmin:
                hit_rec['t'] = temp
                hit_rec['p'] = ray.point_at_paramater(hit_rec['t'])
                hit_rec['n'] = (hit_rec['p'] - self.center) / self.radius
                return True
        return False

class HitableList (list):

    def hit(self, ray, tmin, tmax, hit_rec):
        temp_rec = {}
        has_hit = False
        closest = tmax
        for i in range(len(self)):
            if self[i].hit(ray, tmin, closest, temp_rec):
                has_hit = True
                closest = temp_rec['t']
                hit_rec['t'] = temp_rec['t']
                hit_rec['p'] = temp_rec['p']
                hit_rec['n'] = temp_rec['n']
        return has_hit


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

class Camera (object):

    def __init__(self, ):
        self.lower_left = Vec(-2.0, -1.0, -1.0)
        self.horizontal = Vec(4.0, 0.0, 0.0)
        self.vertical = Vec(0.0, 2.0, 0.0)
        self.origin = Vec(0, 0, 0.0)

    def get_ray(self, u, v):
        return Ray(self.origin, self.lower_left + u*self.horizontal + v*self.vertical - self.origin)

def write_image(p, w=200, h=100, name='swatch.png'):
    f = open(name, 'wb') # Taken from: http://pythonhosted.org/pypng/ex.html#colour
    w = png.Writer(w, h) # http://pythonhosted.org/pypng/png.html#png.Writer
    w.write(f, p)
    f.close()

def color(ray, world):
    hit_rec = {}
    if world.hit(ray, 0.0, float('inf'), hit_rec):
        return 0.5 * Vec(hit_rec['n'].x + 1, hit_rec['n'].y+1, hit_rec['n'].z+1)
    else:
        unit_dir = Vec.unit_vector(ray.direction())
        t = 0.5 * (unit_dir.y + 1.0)
        return (1.0 - t) * Vec(1.0, 1.0, 1.0) + t * Vec(0.5, 0.7, 1.0)

def worker(input, output):
    for inp in iter(input.get, 'STOP'):
        col = Vec(0, 0, 0)
        for s in range(inp['samples']):
            u = (inp['i'] + random()) / inp['width']
            v = (inp['j'] + random()) / inp['height']
            ray = inp['cam'].get_ray(u, v)
            col += color(ray, inp['world'])
        col /= inp['samples']
        col.x *= 255.99
        col.y *= 255.99
        col.z *= 255.99
        output.put({'index': inp['index'], 'color': col})

def make_image(world, width=200, height=100, samples=10):
    task_queue = Queue()
    done_queue = Queue()

    lower_left = Vec(-2, -1, -1)
    horizontal = Vec(4, 0, 0)
    vertical = Vec(0, 2, 0)
    origin = Vec(0, 0, 0)
    cam = Camera()
    index = 0
    for j in reversed(range(height)):
        row = []
        for i in range(width):

            task_queue.put({
                'samples': samples,
                'i': i,
                'j': j,
                'width': width,
                'height': height,
                'cam': cam,
                'world': world,
                'index': index
            })
            index += 1

    print('All tasks logged.')
    stdout.flush()

    NUMBER_OF_PROCESSES = 8
    for proc in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    print('All tasks started.', index)
    stdout.flush()

    results = []
    for i in range(index):
        stdout.flush()
        results.append(done_queue.get())

    print('All tasks done.')
    stdout.flush()

    for proc in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    print('All tasks stopped.')
    stdout.flush()

    p = []
    index = 0
    results.sort(key=lambda x: x['index'], reverse=False)
    print('All tasks sorted.')
    for j in range(height):
        row = []
        for i in range(width):
            col = results[index]['color']
            row.append(col.x)
            row.append(col.y)
            row.append(col.z)
            index += 1
        p.append(row)

    return p

def main():
    w = 1920
    h = 1080
    s = 100
    start_time = time()
    spheres = HitableList()
    spheres.append(Sphere(Vec(0, 0, -1), 0.5))
    spheres.append(Sphere(Vec(0, -100.5, -1), 100))
    write_image(make_image(spheres, w, h, s), w, h)
    print('Took %.2f seconds to process %d rays' % (time() - start_time, w*h*s))

if __name__ == '__main__':
    freeze_support()
    main()
