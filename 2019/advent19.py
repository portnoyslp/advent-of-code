from itertools import count

from aocd import data
from intcode import Intcode
import numpy as np
import math
from functools import lru_cache


class TractorBeam:
    def __init__(self, machine):
        self.machine = machine
        self.use_test_input = False
        self.test_input = []
        self.square_size = 100

    @classmethod
    def with_test_input(cls, test_input):
        beam = cls(None)
        beam.test_input = test_input.split('\n')
        beam.use_test_input = True
        beam.square_size = 10
        return beam

    def count_tractor(self):
        drawing = self.create_drawing(50)
        return np.count_nonzero(drawing == '#')

    def create_drawing(self, square_width):
        drawing = np.full([square_width, square_width], '.')
        for x in range(square_width):
            for y in range(square_width):
                out = self.check_for_tractor_beam(x, y)
                if out == 1:
                    drawing[y][x] = '#' if out == 1 else '.'
        return drawing

    @lru_cache(maxsize=None)
    def check_for_tractor_beam(self, x, y):
        if self.use_test_input:
            return 1 if self.test_input[y][x] != '.' else 0
        beam = Intcode(self.machine)
        beam.input([x, y])
        out = beam.execute()
        return out

    def find_cross_point_y(self, x, y1, y2):
        # binary search to find point where beam goes from on to off. Returns last point where on.
        # Assumes that we know that x,y1 is in the beam, and x,y2 is not.
        if y2 - y1 == 1:
            return y1
        mid = (y1 + y2) // 2
        if self.check_for_tractor_beam(x, mid):
            return self.find_cross_point_y(x, mid, y2)
        return self.find_cross_point_y(x, y1, mid)

    def check_beam_x(self, x, suggested_y):
        # given an x coordinate, find the bottom location where the beam turns off.  Use the suggestion
        # as a starting point.
        # then find the y-100 spot, and determine if x+100 at that point is at the edge of the beam.
        # Returns an indication of which direction to go:
        #  (-1, y_coord) -> beam is too wide at the y_coord, so we should try shrinking the x coord
        #  (1, y_coord) -> beam is too short, so try increasing x.
        #  (0, y_coord) -> we found a match
        if not self.check_for_tractor_beam(x, suggested_y):
            # Our starting point is not in the beam, so we skip from the y=0 until we find it.
            suggested_y = 0
            while not self.check_for_tractor_beam(x, suggested_y):
                suggested_y += self.square_size // 10
        if not self.check_for_tractor_beam(x, suggested_y + self.square_size):
            return self.check_horiz_beam(suggested_y, x)
        # Both top and bottom are in the beam, so skip down until we find a cross point.
        suggested_y += self.square_size
        while self.check_for_tractor_beam(x, suggested_y + self.square_size):
            suggested_y += self.square_size
        return self.check_horiz_beam(suggested_y, x)

    def check_horiz_beam(self, suggested_y, x):
        upper_left = self.find_cross_point_y(x, suggested_y, suggested_y + self.square_size) - self.square_size + 1
        if self.check_for_tractor_beam(x + self.square_size - 1, upper_left):
            # in beam, is it the edge?
            if not self.check_for_tractor_beam(x + self.square_size, upper_left):
                # match!
                return 0, upper_left
            return -1, upper_left
        # beam too short
        return 1, upper_left

    def search_for_tractor_square(self):
        x_limits = [800, 1600]
        if self.use_test_input:
            x_limits = [0, len(self.test_input)]
        # at x=100, the y-center was at 84
        # at x=50, the y-center was at 42.
        # So, the presumed center of the beam is at 0.84 * x
        def suggested_y(x):
            return round(x * 0.84)

        # Use binary search in x_limits to find best spot for beam.
        while True:
            x_mid = (x_limits[0] + x_limits[1]) // 2
            shift_dir, y_coord = self.check_beam_x(x_mid, suggested_y(x_mid))
            if shift_dir == 0:
                # Double-check things by moving left until we no longer have the ability to fit a square:
                while shift_dir == 0:
                    new_x = x_mid - 1
                    (shift_dir, new_y) = self.check_beam_x(new_x, y_coord)
                    if shift_dir == 0:
                        x_mid, y_coord = new_x, new_y
                return x_mid * 10000 + y_coord
            if shift_dir == 1:
                x_limits[0] = x_mid
            else:
                x_limits[1] = x_mid



#print(f'19a: {TractorBeam(data).count_tractor()}')
#print('\n'.join(f'{num} ' + ''.join(row) for (num, row) in enumerate(TractorBeam(data).create_drawing(50))))
test_beam = '''#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########'''
assert TractorBeam.with_test_input(test_beam).search_for_tractor_square() == 250020
print(f'19b: {TractorBeam(data).search_for_tractor_square()}')

x = y = 0
beam = TractorBeam(data)
while not beam.check_for_tractor_beam(x + 99, y):
    y += 1
    while not beam.check_for_tractor_beam(x, y + 99):
        x += 1
print(x*10000 + y)
