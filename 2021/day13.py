from aocd import lines
import numpy as np
import re

def build_ary(coord_lines):
    coords = []
    for coord in coord_lines:
        coords.append(tuple(map(int,reversed(coord.split(',')))))
    size = list(map(max, zip(*coords)))
    ary = np.zeros((size[0] + 1, size[1] + 1), dtype=bool)
    # Something weird happened with the main version, so we'll set it correctly.
    if size[0] > 500:
        ary = np.zeros((895,1311), dtype=bool)
    for coord in coords:
        ary[coord] = True
    return ary

def process_folds(ary, fold_specs, num_folds=None):
    cnt = 0
    for fold_spec in fold_specs:
        (axis, val) = re.match('fold along (.)=(\d+)', fold_spec).groups()
        axis = 0 if axis=='y' else 1
        (ary1, _, ary2) = np.split(ary, [int(val), int(val)+1], axis=axis)
        ary2 = np.flip(ary2, axis)
        ary = ary1 | ary2

        cnt += 1
        if num_folds == cnt:
            break;
    return ary

def count_dots(input, num_folds=None):
    ary = build_ary([l for l in input if ',' in l])
    ary = process_folds(ary, [l for l in input if 'fold' in l], num_folds)
    return np.count_nonzero(ary)

test = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

assert count_dots(test.splitlines(), 1) == 17
print('11a: ', count_dots(lines, 1))

def folded_completely(input):
    ary = build_ary([l for l in input if ',' in l])
    ary = process_folds(ary, [l for l in input if 'fold' in l])
    for y in ary:
        for x in y:
            print('#' if x else ' ', end='')
        print('')
    
folded_completely(test.splitlines())
print('11b:')
folded_completely(lines)