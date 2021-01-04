from aocd import data
import numpy as np
import re

class Lighting:
    def __init__(self, part=1):
        self.lights = np.zeros((1000, 1000))
        if part == 1:
            self.dispatch = {'turn on': self.turn_on, 'turn off': self.turn_off, 'toggle': self.toggle}
        else:
            self.dispatch = {'turn on': self.brighten, 'turn off': self.dim, 'toggle': self.inc_two}

    def turn_on(self, t1, t2):
        self.lights[t1[0]:t2[0]+1, t1[1]:t2[1]+1] = 1

    def turn_off(self, t1, t2):
        self.lights[t1[0]:t2[0]+1, t1[1]:t2[1]+1] = 0

    def toggle(self, t1, t2):
        xor_array = self.array_mask(t1, t2)
        self.lights = np.logical_xor(self.lights, xor_array)

    def array_mask(self, t1, t2, val=1):
        mask = np.zeros((1000, 1000))
        mask[t1[0]:t2[0] + 1, t1[1]:t2[1] + 1] = val
        return mask

    def brighten(self, t1, t2):
        self.lights = self.lights + self.array_mask(t1, t2)

    def inc_two(self, t1, t2):
        self.lights = self.lights + self.array_mask(t1, t2, 2)

    def dim(self, t1, t2):
        dec_array = self.array_mask(t1, t2)
        self.lights = self.lights - dec_array
        zeroes = np.zeros((1000, 1000))
        self.lights = np.maximum(self.lights, zeroes)

    def process_op(self, line):
        match = re.match(r'(turn o(n|ff)|toggle) (\d+),(\d+) through (\d+),(\d+)', line)
        op, _, x1, y1, x2, y2 = match.groups()
        self.dispatch[op]((int(x1), int(y1)), (int(x2), int(y2)))

    def run_lights(self, input_str):
        for line in input_str.splitlines():
            self.process_op(line)
        return np.sum(self.lights)


print('6a: ', Lighting().run_lights(data))
print('6b: ', Lighting(part=2).run_lights(data))
