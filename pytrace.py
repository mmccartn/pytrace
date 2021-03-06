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

MAXIMUM_DEPTH = 50
BG_COL_A = RGB(249, 249, 249)
BG_COL_B = RGB(66, 139, 202)

def write_image(p, w, h, name='balls.png'):
    f = open(name, 'wb') # Taken from: http://pythonhosted.org/pypng/ex.html#colour
    w = png.Writer(w, h) # http://pythonhosted.org/pypng/png.html#png.Writer
    w.write(f, p)
    f.close()

def color(ray, world, depth):
    hit_rec = HitRecord()
    if world.hit(ray, 0.001, float('inf'), hit_rec):
        scattered = Ray()
        attenuation = Vec()
        hit_mat = hit_rec.mat
        if depth < MAXIMUM_DEPTH and hit_mat.scatter(ray, hit_rec, attenuation, scattered):
            return color(scattered, world, depth + 1).vec_mul(attenuation)
        else:
            return Vec()
    else:
        unit_dir = Vec.unit_vector(ray.direction)
        t = 0.5 * (unit_dir.y + 1)
        ti = 1 - t
        return Vec(
            ti * BG_COL_A.x + t * BG_COL_B.x,
            ti * BG_COL_A.y + t * BG_COL_B.y,
            ti * BG_COL_A.z + t * BG_COL_B.z
        )

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
            row.append(int(sqrt(col.x) * 255.99))
            row.append(int(sqrt(col.y) * 255.99))
            row.append(int(sqrt(col.z) * 255.99))
        output.put(RowResult(j, row))

def normalize_color_range(img):
    mcc = get_max_color_component(img)
    if mcc > 255.99:
        for r in range(len(img)):
            row = img[r]
            for c in range(len(row)):
                row[c] = (row[c] / mcc) * 255.99
    return img

def get_max_color_component(img):
    max_color_component = 0
    for r in range(len(img)):
        max_color_component = max([max_color_component] + img[r])
    return max_color_component

def make_image_sync(world, cam, width, height, samples):
    p = []
    range_width = range(width)
    range_samples = range(samples)
    for j in reversed(range(height)):
        row = []
        for i in range_width:
            col = Vec()
            for s in range_samples:
                u = (i + random()) / width
                v = (j + random()) / height
                ray = cam.get_ray(u, v)
                col.add(color(ray, world, 0))
            col.div(samples)
            row.append(int(sqrt(col.x) * 255.99))
            row.append(int(sqrt(col.y) * 255.99))
            row.append(int(sqrt(col.z) * 255.99))
        p.append(row)
    return p

def make_image(world, cam, width, height, samples):
    task_queue = Queue()
    done_queue = Queue()

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
        write_intermediate(results, width)
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

def write_intermediate(results, width):
    p = []
    results.sort(key=lambda x: x.index, reverse=True)
    for result in results:
        p.append(result.row)
    write_image(p, width, len(p), 'temp.png')

def main():
    w = 3840
    h = 2160
    s = 5000
    start_time = time()

    spheres = HitableList()
    spheres.append(Sphere(Vec(0, 0, -1), 0.5, Lambertian(RGB(92, 184, 92)))) # Center
    spheres.append(Sphere(Vec(0, -100.5, -1), 100, Lambertian(RGB(217, 83, 79)))) # Base
    spheres.append(Sphere(Vec(1, 0, -1), 0.5, Metal(RGB(255, 238, 173)))) # Right
    spheres.append(Sphere(Vec(-1, 0, -1), 0.5, Dialectric(1.5))) # Left

    lookfrom = Vec(0, 1, 4)
    lookat = Vec(0, 0, -1)
    dist_to_focus = (lookfrom - lookat).length()
    aperture = 0
    cam = Camera(w / h, 25, aperture, dist_to_focus, lookfrom, lookat)

    image = make_image(spheres, cam, w, h, s)

    normalize_color_range(image)
    write_image(image, w, h)
    print('Took %.2f seconds to process %d rays' % (time() - start_time, w*h*s))

if __name__ == '__main__':
    freeze_support()
    main()
