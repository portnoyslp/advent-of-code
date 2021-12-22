from aocd import lines
from collections import defaultdict
import functools 

class ImageEnhance:
    def __init__(self, input_lines):
        self.enhancement_alg = list(map(lambda x: 0 if x == '.' else 1, input_lines[0]))
        # values is a dict from location to the False or True stored in that spot.
        self.values = defaultdict(bool)
        y = 0
        for line in input_lines[2:]:
            for x, ch in enumerate(line):
                self.values[(x,y)] = (ch == '#')
            y += 1
        self.times_enhanced_called = 0
        
    def enhance(self):
        world_background = self.enhancement_alg[0] if self.times_enhanced_called % 2 == 0 else False
        new_values = defaultdict(lambda: world_background)
        x_keys = sorted([key[0] for key in self.values.keys()])
        y_keys = sorted([key[1] for key in self.values.keys()])
        for x in range(x_keys[0] - 1, x_keys[-1] + 2):
            for y in range(y_keys[0] - 1, y_keys[-1] + 2):
                # replace 3x3 array with value in enhancement_alg.
                # This could probably be faster.
                val = 0
                for b in range(y-1, y+2):
                    for a in range(x-1, x+2):
                        val = val * 2 + (1 if self.values[(a,b)] else 0)
                new_values[(x,y)] = self.enhancement_alg[val]
        self.values = new_values
        return self

    def show(self):
        x_keys = sorted([key[0] for key in self.values.keys()])
        y_keys = sorted([key[1] for key in self.values.keys()])
        for y in range(y_keys[0], y_keys[-1] + 1):
            for x in range(x_keys[0], x_keys[-1] + 1):
                print('#' if self.values[(x,y)] else '.', end='')
            print('')
        print('')

    def count_pixels(self):
        return sum([x for x in self.values.values()])

def run_and_count(input_lines, times=2):
    image = ImageEnhance(input_lines)
    for _ in range(0, times):
        image.enhance()
    return image.count_pixels()

class AlternateVersion:
    def __init__(self, input_lines):
        self.enhancement_alg = list(map(lambda x: 0 if x == '.' else 1, input_lines[0]))
        self.initial_values = defaultdict(bool)
        y = 0
        for line in input_lines[2:]:
            for x, ch in enumerate(line):
                self.initial_values[(x,y)] = (ch == '#')
            y += 1
        self.times_enhanced_called = 0

    @functools.lru_cache(maxsize=None)
    def f(self, x, y, ts):
        if (ts == 0):
            return 1 if self.initial_values[(x,y)] else 0
        val = 256 * self.f(x - 1, y - 1, ts - 1) + 128 * self.f(x, y - 1, ts - 1) + 64 * self.f(x + 1, y - 1, ts - 1) +                 32 * self.f(x - 1, y, ts - 1) + 16 * self.f(x, y, ts -1) + 8 * self.f(x + 1, y, ts -1) +                 4 * self.f(x - 1, y + 1, ts -1) + 2 * self.f(x, y + 1, ts - 1) + self.f(x + 1, y + 1, ts -1)
        return 1 if self.enhancement_alg[val] else 0

def alternate_run_and_count(input_lines, steps=2):
    alternate = AlternateVersion(input_lines)
    sum = 0
    for x in range(-steps, steps + len(input_lines[2]) + steps):
        for y in range(-steps, steps + len(input_lines) - 2 + steps):
            sum += alternate.f(x,y,steps)
    return sum

test = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
'''

assert(run_and_count(test.splitlines()) == 35)
print('20a: ', run_and_count(lines))

assert(run_and_count(test.splitlines(), 50) == 3351)
print('20b: ', run_and_count(lines, 50))

assert(alternate_run_and_count(test.splitlines()) == 35)
assert(alternate_run_and_count(test.splitlines(), 50) == 3351)
print('20b: ', alternate_run_and_count(lines, 50))