from aocd import data
from intcode import Intcode
import numpy as np
import math


class TractorBeam:
    def __init__(self, machine):
        self.machine = machine

    def count_tractor(self):
        cnt = 0
        drawing = np.full([50, 50], '.')
        for x in range(50):
            for y in range(50):
                out = self.check_for_tractor_beam(x, y)
                if out == 1:
                    cnt += 1
                drawing[y][x] = '#' if out == 1 else '.'
        print('\n'.join([''.join(row) for row in drawing]))
        return cnt

    def check_for_tractor_beam(self, x, y):
        beam = Intcode(self.machine)
        beam.input([x, y])
        out = beam.execute()
        return out

    # The printing of the 50x50 version shows that, at the x coord of 49, the beam
    # spams 40-45 in the y direction. Therefore, as a guess, the beam will be 100
    # rows high around x-coord of 800, y of around 640, and maybe 200 high around 1600
    # (y of 1280). So, we're going to use those as the initial limits for a binary search.

    # One thing to note is that these are two lines:
    #   upper_slope = 40/50 ~ .8, lower_slope = 45/50 ~ .9
    # Before checking a coordinate, we clamp it so that it's in that range.

    # For each coord, see if (x,y), (x+99 y), and (x, y+99) are all in the tractor beam.
    # Based on that, we switch the x,y to a different quadrant

    def square_in_beam(self, x, y):
        ul = self.check_for_tractor_beam(x, y) == '#'
        ur = self.check_for_tractor_beam(x + 99, y) == '#'
        ll = self.check_for_tractor_beam(x, y + 99) == '#'
        return ul & ur & ll, ul, ur, ll

    def binary_search_for_tractor_beam(self):
        x_limits = [800, 1600]
        y_limits = [640, 1280]
        while x_limits[1] - x_limits[0] > 0 and y_limits[1] - y_limits[0] > 0:
            x_mid, y_mid = self.calculate_mid(x_limits, y_limits)
            square_fits, ul_in, ur_in, ll_in = self.square_in_beam(x_mid, y_mid)
            if square_fits:
                x_limits[1] = x_mid
                y_limits[1] = y_mid
                continue
            if ul_in:
                if not ur_in and not ll_in:
                    # We're too far up the neck, so go to the fourth quadrant.
                    x_limits[0] = x_mid
                    y_limits[0] = y_mid
                    continue
                if ur_in:
                    # A bit low, so shift up
                    y_limits[1] = y_mid
                    continue
                # A bit far right, shift left
                x_limits[1] = y_mid
                continue
            # The upper left is not in the beam. This shouldn't happen.
            raise RuntimeError('I goofed')
        return x_limits[0], y_limits[0]

    def calculate_mid(self, x_limits, y_limits):
        x_mid = (x_limits[0] + x_limits[1]) // 2
        y_mid = (y_limits[0] + y_limits[1]) // 2
        limits_for_y_mid = (.8 * x_mid, .9 * x_mid)
        if y_mid < limits_for_y_mid[0]:
            y_mid = math.ceil(limits_for_y_mid[0])
        elif y_mid > limits_for_y_mid[1]:
            y_mid = math.floor(limits_for_y_mid[1])
        return x_mid, y_mid


#print(f'19a: {TractorBeam(data).count_tractor()}')
print(f'19b: {TractorBeam(data).binary_search_for_tractor_beam()}')
