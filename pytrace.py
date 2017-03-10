import png
from vec3 import Vec
#
# class PPM (object):
#
#     def __init__(self, name, num_rows, num_cols, max_val=255, magic_number=6):
#         self.name = name
#         self.max_val = max_val
#         self.num_rows = num_rows
#         self.num_cols = num_cols
#         self.magic_number = 'P' + magic_number
#         self.rows = []
#         self.rows.append([])
#         self.current_row_index = 0
#
#     def append_pixel(self, pixel):
#         if len(self.rows) >= self.num_cols:
#             self.rows.append([])
#             self.current_row_index += 1
#         self.rows[self.current_row_index].append(pixel)
#
#     def __str__(self):
#         for row in self.rows:
#             [str(p) for p in row].join('    ')
#             for pixel in row:
#                 pass


def test_png():
    # Taken from: http://pythonhosted.org/pypng/ex.html#colour
    p = [(255, 0, 0, 0, 255, 0, 0, 0, 255),
         (128, 0, 0, 0, 128, 0, 0, 0, 128)]
    f = open('swatch.png', 'wb')
    w = png.Writer(3, 2)  # http://pythonhosted.org/pypng/png.html#png.Writer
    w.write(f, p)
    f.close()

def test_png_2(width=200, height=100):
    p = []
    b = int(0.2 * 255.0)
    for ri in range(height):
        row = []
        r = int((ri / height) * 255.0)
        for ci in range(width):
            g = int((ci / width) * 255.0)
            row.append(r)
            row.append(g)
            row.append(b)
        p.append(row)
    f = open('swatch2.png', 'wb')
    w = png.Writer(width, height)
    w.write(f, p)
    f.close()


def main():
    test_png_2()

if __name__ == '__main__':
    main()
