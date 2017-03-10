import Vec from vec3

class PPM (object):

    def __init__(self, name, num_rows, num_cols, max_val=255, magic_number=6):
        self.name = name
        self.max_val = max_val
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.magic_number = 'P' + magic_number
        self.rows = []
        self.rows.append([])
        self.current_row_index = 0

    def append_pixel(self, pixel):
        if len(self.rows) >= self.num_cols:
            self.rows.append([])
            self.current_row_index += 1
        self.rows[self.current_row_index].append(pixel)

    def __str__(self):
        for row in self.rows:
            [str(p) for p in row].join('    ')
            for pixel in row:
                pass

def main():
    pass

if __name__ == '__main__':
    main()
