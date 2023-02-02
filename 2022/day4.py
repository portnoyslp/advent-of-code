from aocd import lines
import re

def ranges(line):
    elves = line.split(',');
    e1 = [int(x) for x in elves[0].split('-')]
    e2 = [int(x) for x in elves[1].split('-')]
    return [e1, e2]

def full_overlap(line):
    elves = ranges(line)
    if elves[0][0] <= elves[1][0] and elves[0][1] >= elves[1][1]:
        return True
    if elves[1][0] <= elves[0][0] and elves[1][1] >= elves[0][1]:
        return True
    return False

def count_full_overlaps(lines):
    return sum(1 for line in lines if full_overlap(line))

def partial_overlap(line):
    elves = ranges(line)
    if elves[0][1] < elves[1][0]:
        return False
    if elves[1][1] < elves[0][0]:
        return False
    return True

def count_all_overlaps(lines):
    return sum(1 for line in lines if partial_overlap(line))

ex1 = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
assert count_full_overlaps(ex1.splitlines()) == 2
print('4a: ', count_full_overlaps(lines))

assert count_all_overlaps(ex1.splitlines()) == 4
print('4b: ', count_all_overlaps(lines))
