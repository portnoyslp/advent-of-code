from aocd import data
import numpy as np
from math import sin, cos, radians


class Ferry:
    def __init__(self):
        self.position = np.array((0, 0))
        self.dir = np.array((1, 0))  # east = 1 in x dir
        self.op_dict = {'F': self.forward, 'R': self.right, 'L': self.left, 'S': self.south, 'N': self.north,
                        'W': self.west, 'E': self.east}

    def forward(self, dist):
        addend = self.dir * dist
        self.position = self.position + addend

    def right(self, degrees):
        rad = radians(degrees)
        rot = np.array([[cos(rad), sin(rad)], [-sin(rad), cos(rad)]])
        # rounding because assumption that degrees will always be in [90,180]
        self.dir = np.rint(np.dot(self.dir, rot))

    def left(self, degrees):
        self.right(-degrees)

    def south(self, dist):
        self.position += dist * np.array([0, 1])

    def north(self, dist):
        self.south(-dist)

    def east(self, dist):
        self.position += dist * np.array([1, 0])

    def west(self, dist):
        self.east(-dist)

    @classmethod
    def run_instructions(cls, input_str):
        ferry = cls()
        for inst in input_str.splitlines():
            op, val = inst[0], int(inst[1:])
            ferry.op_dict[op](val)
        return int(abs(ferry.position[0]) + abs(ferry.position[1]))


test_input = '''F10
N3
F7
R90
F11'''
assert Ferry.run_instructions(test_input) == 25
print('12a: ', Ferry.run_instructions(data))

class Ferry2(Ferry):
    def __init__(self):
        Ferry.__init__(self)
        self.waypoint = np.array((10, -1))

    def forward(self, dist):
        self.position = self.position + (self.waypoint * dist)

    def right(self, degrees):
        rad = radians(degrees)
        rot = np.array([[cos(rad), sin(rad)], [-sin(rad), cos(rad)]])
        # rounding because assumption that degrees will always be in [90,180]
        self.waypoint = np.rint(np.dot(self.waypoint, rot))

    def south(self, dist):
        self.waypoint += dist * np.array([0, 1])

    def east(self, dist):
        self.waypoint += dist * np.array([1, 0])

assert Ferry2.run_instructions(test_input) == 286
print('12b: ', Ferry2.run_instructions(data))
