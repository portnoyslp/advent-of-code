from aocd import data
import numpy as np

class AllOctopusesFlashed(Exception):
    """Exception raised for errors in the input.

    Attributes:
        step -- when the octopuses flashed
    """

    def __init__(self, step):
        self.step = step



def count_flashes(data, steps = 100):
    ary = np.stack([np.fromiter(map(int,line), int) for line in data.splitlines()])
    count = 0
    for step in range(0,steps):
        ary += 1
        flashed_coords = set()
        while True:
            locs = np.where(ary > 9)
            flashable_locs = list(zip(locs[0], locs[1]))

            flash_occurred = False
            for loc in flashable_locs:
                if loc not in flashed_coords:
                    flash_occurred = True
                    count += 1
                    flashed_coords.add(loc)
                    for x in range(0 if loc[0] < 1 else loc[0] - 1, 10 if loc[0] > 8 else loc[0] + 2):
                        for y in range(0 if loc[1] < 1 else loc[1] - 1, 10 if loc[1] > 8 else loc[1] + 2):
                            if x != loc[0] or y != loc[1]:
                                ary[x,y] += 1
            if not flash_occurred:
                break
        if len(flashed_coords) == 100:
            raise AllOctopusesFlashed(step + 1)
        ary[ary > 9] = 0
    return count

def find_all_flash(data):
    try:
        count_flashes(data, 1000000)
    except AllOctopusesFlashed as aof:
        return aof.step
    return -1

test="""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
assert count_flashes(test, 10) == 204
assert count_flashes(test) == 1656
print('11a: ', count_flashes(data))

assert find_all_flash(test) == 195
print('11b: ', find_all_flash(data))