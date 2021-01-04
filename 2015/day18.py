from aocd import data
import numpy as np
from scipy import signal


class ConwayLights:
    def __init__(self, init_state):
        vals = ('.', '#')
        ary = []
        for line in init_state.splitlines():
            ary.append([vals.index(x) for x in line])
        self.lights = np.array(ary, dtype=int)
        self.mask = np.ones([3, 3], dtype=int)
        self.mask[1, 1] = 0
        self.update_elements = np.vectorize(self.update)

    def update(self, val, num_neighbors):
        if val and (num_neighbors == 2 or num_neighbors == 3):
            return 1
        if not val and num_neighbors == 3:
            return 1
        return 0

    def step(self):
        num_neighbors = signal.convolve2d(self.lights, self.mask, mode='same', boundary='fill')
        self.lights = self.update_elements(self.lights, num_neighbors)

    def light_corners(self):
        self.lights[0,0] = 1
        self.lights[-1,-1] = 1
        self.lights[0,-1] = 1
        self.lights[-1,0] = 1

    def steps_and_count(self, num_steps, corners_always_on=False):
        for _ in range(num_steps):
            if corners_always_on:
                self.light_corners()
            self.step()
        if corners_always_on:
            self.light_corners()
        return np.sum(self.lights)


test_input = '''.#.#.#
...##.
#....#
..#...
#.#..#
####..'''
assert ConwayLights(test_input).steps_and_count(4) == 4
print('18a: ', ConwayLights(data).steps_and_count(100))
assert ConwayLights(test_input).steps_and_count(5, corners_always_on=True) == 17
print('18b: ', ConwayLights(data).steps_and_count(100, corners_always_on=True))
