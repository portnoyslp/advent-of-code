from aocd import data
import numpy as N
from scipy.ndimage import label
from functools import reduce

def local_minima(array2d):
    return ((array2d < N.roll(array2d,  1, 0)) &
        (array2d < N.roll(array2d, -1, 0)) &
        (array2d < N.roll(array2d,  1, 1)) &
        (array2d < N.roll(array2d, -1, 1)))

def risk_levels(data):
    arys = [N.fromiter(map(int,line), int) for line in data.splitlines()]
    start_ary = N.stack(arys)

    # pad starting array with a row of 10's around the edge, then use local_minima to find minima.
    minima = local_minima(N.pad(start_ary, 1, 'constant', constant_values=9))[1:-1,1:-1]
    risk_calc = N.vectorize(lambda v,b: v + 1 if b else 0)
    out_ary = risk_calc(start_ary, minima)
    return N.sum(out_ary)

def basin_sizes(data):
    arys = [N.fromiter(map(int,line), int) for line in data.splitlines()]
    start_ary = N.stack(arys)

    features = N.vectorize(lambda x: 0 if x == 9 else 1)(start_ary)
    labeled_ary, num_features = label(features)
    basin_sizes = sorted([N.count_nonzero(labeled_ary == x) for x in range(1, num_features + 1)])
    return reduce(lambda a, b: a * b, list(basin_sizes)[-3:])

test = """2199943210
3987894921
9856789892
8767896789
9899965678
"""
assert(risk_levels(test)) == 15
print('9a: ', risk_levels(data))

assert(basin_sizes(test)) == 1134
print('9b: ', basin_sizes(data))