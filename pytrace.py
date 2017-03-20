import png
from ray import Ray
from vec3 import Vec, RGB
from math import sqrt
from time import time
from sys import stdout
from random import random
from progressbar import ProgressBar
from hittables import HitableList, Sphere
from materials import Lambertian, Metal, Dialectric
from multiprocessing import Process, Queue, freeze_support, cpu_count

class Camera (object):

    def __init__(self, r=1.6):
        self.lower_left = Vec(-1.0 * r, -1.0, -1.0)
        self.horizontal = Vec(2.0 * r, 0.0, 0.0)
        self.vertical = Vec(0.0, 2.0, 0.0)
        self.origin = Vec(0, 0.25, 4)

    def get_ray(self, u, v):
        return Ray(self.origin, self.lower_left + u*self.horizontal + v*self.vertical - self.origin)

def write_image(p, w, h, name='balls.png'):
    print('Writing out to file: {0}'.format(name))
    f = open(name, 'wb') # Taken from: http://pythonhosted.org/pypng/ex.html#colour
    w = png.Writer(w, h) # http://pythonhosted.org/pypng/png.html#png.Writer
    w.write(f, p)
    f.close()

def color(ray, world, depth):
    hit_rec = {}
    if world.hit(ray, 0.001, float('inf'), hit_rec):
        scattered = Ray()
        attenuation = Vec()
        if depth < 50 and hit_rec['mat'].scatter(ray, hit_rec, attenuation, scattered):
            return attenuation * color(scattered, world, depth + 1)
        else:
            return Vec(0, 0, 0)
    else:
        unit_dir = Vec.unit_vector(ray.direction())
        t = 0.5 * (unit_dir.y + 1.0)
        return (1.0 - t) * RGB(249, 249, 249) + t * RGB(66, 139, 202)

def worker(input, output, state):
    for inp in iter(input.get, 'STOP'):
        col = Vec(0, 0, 0)
        for s in range(state['samples']):
            u = (inp['i'] + random()) / state['width']
            v = (inp['j'] + random()) / state['height']
            ray = state['cam'].get_ray(u, v)
            col += color(ray, state['world'], 0)
        col /= state['samples']
        col.x = sqrt(col.x) * 255.99
        col.y = sqrt(col.y) * 255.99
        col.z = sqrt(col.z) * 255.99
        output.put({'index': inp['index'], 'color': col})

def make_image(world, width, height, samples):
    task_queue = Queue()
    done_queue = Queue()

    state = {
        'samples': samples,
        'width': width,
        'height': height,
        'cam': Camera(),
        'world': world
    }

    index = 0
    for j in reversed(range(height)):
        for i in range(width):
            task_queue.put({'i': i, 'j': j, 'index': index})
            index += 1

    print('Starting {0} tasks in {1} processes.'.format(width*height, cpu_count()))
    stdout.flush()

    for proc in range(cpu_count()):
        Process(target=worker, args=(task_queue, done_queue, state)).start()

    results = []
    bar = ProgressBar(redirect_stdout=True, max_value=width*height)
    for i in range(index):
        bar.update(i)
        results.append(done_queue.get())
    bar.finish()

    for proc in range(cpu_count()):
        task_queue.put('STOP')

    print('Sorting.')
    stdout.flush()

    p = []
    index = 0
    results.sort(key=lambda x: x['index'], reverse=False)
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
    h = 1200
    s = 2048
    start_time = time()
    spheres = HitableList()
    spheres.append(Sphere(Vec(0, 0, -1), 0.5, Lambertian(RGB(92, 184, 92)))) # Center
    spheres.append(Sphere(Vec(0, -100.5, -1), 100, Lambertian(RGB(217, 83, 79)))) # Base
    spheres.append(Sphere(Vec(1, 0, -1), 0.5, Metal(RGB(255, 238, 173)))) # Right
    spheres.append(Sphere(Vec(-1, 0, -1), 0.5, Dialectric(1.5))) # Left
    write_image(make_image(spheres, w, h, s), w, h)
    print('Took %.2f seconds to process %d rays' % (time() - start_time, w*h*s))

if __name__ == '__main__':
    freeze_support()
    main()
