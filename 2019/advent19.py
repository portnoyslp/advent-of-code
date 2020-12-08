from aocd import data
from intcode import Intcode
import numpy as np

def count_tractor(machine):
    cnt = 0
    drawing = np.full([50,50], '.')
    for x in range(50):
        for y in range(50):
            beam = Intcode(machine)
            beam.input([x, y])
            out = beam.execute()
            if out == 1:
                cnt += 1
            drawing[y][x] = '#' if out == 1 else '.'
    print('\n'.join([''.join(row) for row in drawing]))
    return cnt

print(f'19a: {count_tractor(data)}')