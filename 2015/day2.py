from aocd import data
import re


def footage_required(package_str):
    dimensions = get_dim(package_str)
    sides = list(map(lambda x: x[0] * x[1], zip(dimensions, dimensions[1:] + dimensions[:1])))
    min_side = min(*sides)
    return sum(sides) * 2 + min_side


def get_dim(package_str):
    dimensions = tuple(map(int, re.match(r'^(\d+)x(\d+)x(\d+)', package_str).groups()))
    return dimensions


assert footage_required('2x3x4') == 58
assert footage_required('1x1x10') == 43


def all_footage(input_str):
    return sum([footage_required(line) for line in input_str.splitlines()])

print('2a ', all_footage(data))

def ribbon_required(package_str):
    d = get_dim(package_str)
    volume = d[0] * d[1] * d[2]
    return 2 * (sum(d) - max(d)) + volume

assert ribbon_required('2x3x4') == 34
assert ribbon_required('1x1x10') == 14

def ribbons(input_str):
    return sum([ribbon_required(line) for line in input_str.splitlines()])

print('2b ', ribbons(data))
