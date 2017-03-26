import png
from math import sqrt
from time import time
from sys import stdout
from random import random
from progressbar import ProgressBar
from multiprocessing import Process, Queue, freeze_support, cpu_count

from ray import Ray
from vec3 import Vec, RGB
from camera import Camera
from hittables import HitableList, Sphere
from structs import RowResult, HitRecord
from materials import Lambertian, Metal, Dialectric, Emissive

MAXIMUM_COLOR_VALUE = 255.99

def write_image(p, w, h, name='balls.png'):
    print('Writing out to file: {0}'.format(name))
    f = open(name, 'wb') # Taken from: http://pythonhosted.org/pypng/ex.html#colour
    w = png.Writer(w, h) # http://pythonhosted.org/pypng/png.html#png.Writer
    w.write(f, p)
    f.close()

def color(ray, world, depth):
    hit_rec = HitRecord()
    if world.hit(ray, 0.001, float('inf'), hit_rec):
        scattered = Ray()
        attenuation = Vec()
        if type(hit_rec.mat) is Emissive:
            return hit_rec.mat.get_color()
        elif depth < 50 and hit_rec.mat.scatter(ray, hit_rec, attenuation, scattered):
            return attenuation * color(scattered, world, depth + 1)
        else:
            return Vec(0, 0, 0)
    else:
        unit_dir = Vec.unit_vector(ray.direction())
        t = 0.5 * (unit_dir.y + 1.0)
        return (1.0 - t) * RGB(249, 249, 249) + t * RGB(66, 139, 202)

def worker(input, output, state):
    samples, width, height, cam, world = state
    range_samples = range(samples)
    range_width = range(width)
    for j in iter(input.get, 'STOP'):
        row = []
        for i in range_width:
            col = Vec(0, 0, 0)
            for s in range_samples:
                u = (i + random()) / width
                v = (j + random()) / height
                ray = cam.get_ray(u, v)
                col += color(ray, world, 0)
            col /= samples
            row.append(int(sqrt(col.x) * MAXIMUM_COLOR_VALUE))
            row.append(int(sqrt(col.y) * MAXIMUM_COLOR_VALUE))
            row.append(int(sqrt(col.z) * MAXIMUM_COLOR_VALUE))
        output.put(RowResult(j, row))

def normalize_color_range(img):
    mcc = get_max_color_component(img)
    if mcc > MAXIMUM_COLOR_VALUE:
        for r in range(len(img)):
            row = img[r]
            for c in range(len(row)):
                row[c] = (row[c] / mcc) * MAXIMUM_COLOR_VALUE
    return img

def get_max_color_component(img):
    max_color_component = 0
    for r in range(len(img)):
        max_color_component = max([max_color_component] + img[r])
    return max_color_component

def make_image(world, width, height, samples):
    task_queue = Queue()
    done_queue = Queue()

    lookfrom = Vec(-3, 1, 4)
    lookat = Vec(0, 0, -1)
    dist_to_focus = (lookfrom - lookat).length()
    aperture = 0.01
    cam = Camera(width / height, 30, aperture, dist_to_focus, lookfrom, lookat)

    state = (samples, width, height, cam, world)

    row_index = 0
    for row_index in reversed(range(height)):
        task_queue.put(row_index)

    num_tasks = height
    num_cpus = cpu_count()

    print('Starting {0} tasks in {1} processes.'.format(num_tasks, num_cpus))
    stdout.flush()

    for proc in range(num_cpus):
        Process(target=worker, args=(task_queue, done_queue, state)).start()

    results = []
    bar = ProgressBar(redirect_stdout=True, max_value=num_tasks)
    for ti in range(num_tasks):
        bar.update(ti)
        results.append(done_queue.get())
    bar.finish()

    for proc in range(num_cpus):
        task_queue.put('STOP')

    print('Sorting.')
    stdout.flush()

    p = []
    results.sort(key=lambda x: x.index, reverse=True)
    for result in results:
        p.append(result.row)

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
    spheres.append(Sphere(Vec(1, 2, 0), 0.5, Emissive(RGB(254, 252, 255), 2))) # Above
    image = make_image(spheres, w, h, s)
    normalize_color_range(image)
    write_image(image, w, h)
    print('Took %.2f seconds to process %d rays' % (time() - start_time, w*h*s))

if __name__ == '__main__':
    freeze_support()
    main()
