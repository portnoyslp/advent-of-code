from aocd import data
import numpy as np

class TobogganRun:
    def __init__(self):
        pass
    def setField(self, input_str):
        lines = input_str.splitlines()
        self.field = []
        for line in input_str.splitlines():
            if (line == ''):
                continue
            self.field.append([c for c in line])
        return self
    def trees_hit(self, slope):
        trees_hit = 0
        xc = 0
        yc = 0
        while yc < len(self.field):
            xc = xc % len(self.field[0])
            if self.field[yc][xc] == '#': # tree
                trees_hit += 1
            xc += slope[0]
            yc += slope[1]
        return trees_hit

def run_toboggan(input_str, slope):
    return TobogganRun().setField(input_str).trees_hit(slope)

test_input = '''
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
'''
assert run_toboggan(test_input, (3, 1)) == 7

print(f"3a: {run_toboggan(data, (3, 1))}")

def multiple_slope_runs(input_str):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees_hit = map(lambda slope: run_toboggan(input_str, slope), slopes)
    return np.prod(list(trees_hit))

assert multiple_slope_runs(test_input) == 336

print(f"3b: {multiple_slope_runs(data)}")
