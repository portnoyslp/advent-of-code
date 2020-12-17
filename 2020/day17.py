from aocd import data
from collections import defaultdict
import itertools


class ConwayCubes:
    def __init__(self):
        self.grid = defaultdict(bool)

    def parse_input(self, input_str):
        cubes = []
        for line in input_str.splitlines():
            if line != '':
                cubes.append([c for c in line])
        for j in range(len(cubes)):
            for i in range(len(cubes[j])):
                if cubes[j][i] == '#':
                    self.grid[(i, j, 0)] = True
        return self

    def run_step(self):
        # Get ranges of x,y,z
        mins, maxs = self.valid_ranges()

        neighbors = defaultdict(int)
        for (x, y, z) in itertools.product(range(mins[0] - 1, maxs[0] + 2), range(mins[1] - 1, maxs[1] + 2),
                                           range(mins[2] - 1, maxs[2] + 2)):
            # calculate neighbors of each cell from grid.
            n = 0
            for i, j, k in itertools.product(range(-1, 2), repeat=3):
                if (i, j, k) != (0, 0, 0):
                    n += 1 if self.grid[(x + i, y + j, z + k)] else 0
            neighbors[(x, y, z)] = n
        for key in neighbors:
            active = self.grid[key]
            if active:
                self.grid[key] = (neighbors[key] in [2, 3])
            else:
                self.grid[key] = neighbors[key] == 3

    def valid_ranges(self):
        mins = [1000] * 3
        maxs = [-1000] * 3
        for key in [k for k, v in self.grid.items() if v]:
            for i in range(0, 3):
                mins[i] = min(mins[i], key[i])
                maxs[i] = max(maxs[i], key[i])
        return mins, maxs

    def print_state(self):
        mins, maxs = self.valid_ranges()
        for z in range(mins[2], maxs[2] + 1):
            print(f'z={z}')
            for y in range(mins[1], maxs[1] + 1):
                line = []
                for x in range(mins[0], maxs[0] + 1):
                    line.append('#' if self.grid[(x, y, z)] else '.')
                print(''.join(line))
            print()

    def run_steps(self, n):
        for step in range(n):
            self.run_step()
            # self.print_state()
        return len([v for v in self.grid.values() if v])


assert ConwayCubes().parse_input('''.#.
..#
###''').run_steps(6) == 112
print('17a: ', ConwayCubes().parse_input(data).run_steps(6))
